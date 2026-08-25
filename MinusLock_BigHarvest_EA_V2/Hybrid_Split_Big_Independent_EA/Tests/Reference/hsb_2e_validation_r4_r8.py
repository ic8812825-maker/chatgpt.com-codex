#!/usr/bin/env python3
"""Independent native R4-R8 authority, fill, economic, and commit validators."""
from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal, InvalidOperation
from typing import Any


CURRENT_CERTIFICATE_VERSION = 1
CURRENT_SCHEMA_VERSION = 8
PRICE_POLICY_REGISTRY_VERSION = 1
PRICE_POLICY_REGISTRY = {
    "EXACT_CLOSE_SIDE": {
        "policyId": "EXACT_CLOSE_SIDE",
        "symbolClass": "FX",
        "maximumDeviationTicks": 100,
        "validFrom": 0,
        "validUntil": 4_102_444_800,
        "normativeSourceId": "HSBI-PRICE-R8",
        "registryVersion": PRICE_POLICY_REGISTRY_VERSION,
    }
}
FORMULA_REGISTRY = {
    "INITIAL_NET_ACTUAL": ("INITIAL", "ACCOUNT_CURRENCY_AND_LOTS", "ROUND_DOWN", "HSBI-ECON-INITIAL-R8"),
    "BIG_ALLOCATION_DISJOINT": ("BIG", "ACCOUNT_CURRENCY_AND_LOTS", "ROUND_DOWN", "HSBI-ECON-BIG-R8"),
    "SMALL_RESIDUAL_ACTUAL": ("SMALL", "ACCOUNT_CURRENCY_AND_LOTS", "ROUND_DOWN", "HSBI-ECON-SMALL-R8"),
    "FINAL_RESERVE_ACTUAL": ("FINAL", "ACCOUNT_CURRENCY_AND_LOTS", "ROUND_DOWN", "HSBI-ECON-FINAL-R8"),
}
REQUIRED_FORMULAS = {
    "INITIAL": ("INITIAL_NET_ACTUAL",),
    "BIG": ("BIG_ALLOCATION_DISJOINT",),
    "SMALL": ("SMALL_RESIDUAL_ACTUAL",),
    "FINAL": ("FINAL_RESERVE_ACTUAL",),
}
COMMIT_OBJECT_KEYS = frozenset({"broker", "economic", "allocation", "persistence", "fsm"})


def canonical(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {str(key): canonical(child) for key, child in sorted(value.items())}
    if isinstance(value, (list, tuple)):
        return [canonical(child) for child in value]
    return value


def digest(value: Any) -> str:
    encoded = json.dumps(canonical(value), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def decimal_value(value: Any) -> Decimal | None:
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None
    return parsed if parsed.is_finite() else None


def reject(reason: str, phase: str = "VALIDATION_BLOCKED") -> dict[str, Any]:
    return {
        "status": "REJECT",
        "reason": reason,
        "phase": phase,
        "settlementApplied": False,
        "allocationApplied": False,
        "stateRevisionDelta": 0,
        "settlementRevisionDelta": 0,
    }


def pass_result(reason: str = "OK") -> dict[str, Any]:
    return {
        "status": "PASS",
        "reason": reason,
        "phase": "VALIDATED",
        "settlementApplied": False,
        "allocationApplied": False,
        "stateRevisionDelta": 0,
        "settlementRevisionDelta": 0,
    }


def classify_fill(confirmed: Any, requested: Any) -> str:
    confirmed_value = decimal_value(confirmed)
    requested_value = decimal_value(requested)
    if confirmed_value is None or requested_value is None or requested_value <= 0 or confirmed_value < 0:
        return "INVALID_FILL"
    if confirmed_value == 0:
        return "NO_FILL"
    if confirmed_value < requested_value:
        return "PARTIAL_FILL"
    if confirmed_value == requested_value:
        return "FULL_FILL"
    return "OVERFILL"


def classify_fill_result(canonical_input: dict[str, Any]) -> dict[str, Any]:
    classification = classify_fill(canonical_input.get("confirmedVolume"), canonical_input.get("requestedVolume"))
    if classification == "OVERFILL":
        result = reject("OVERFILL", "RECONCILIATION_REQUIRED")
        result["fillClassification"] = classification
        return result
    if classification == "INVALID_FILL":
        result = reject("INVALID_FILL")
        result["fillClassification"] = classification
        return result
    result = pass_result(classification)
    result["fillClassification"] = classification
    return result


def _price_registry_entry(policy: dict[str, Any]) -> dict[str, Any] | None:
    policy_id = policy.get("policyId")
    return PRICE_POLICY_REGISTRY.get(policy_id)


def validate_price_result(canonical_input: dict[str, Any]) -> dict[str, Any]:
    context = canonical_input.get("context")
    snapshot = canonical_input.get("snapshot")
    policy = canonical_input.get("pricePolicy")
    if not all(isinstance(value, dict) for value in (context, snapshot, policy)):
        return reject("PRICE_CONTRACT_MALFORMED")
    identity_fields = ("accountLogin", "symbol", "magic", "cycleId", "stateRevision", "snapshotId", "snapshotRevision")
    if any(snapshot.get(field) != context.get(field) for field in identity_fields):
        return reject("SNAPSHOT_CONTEXT_IDENTITY_MISMATCH")
    if policy.get("buyCloseSide") != "BID" or policy.get("sellCloseSide") != "ASK":
        return reject("NORMATIVE_CLOSE_SIDE_MISMATCH")
    authority = _price_registry_entry(policy)
    if authority is None:
        return reject("PRICE_POLICY_AUTHORITY_UNKNOWN")
    if policy.get("normativeSourceId") != authority["normativeSourceId"]:
        return reject("PRICE_POLICY_AUTHORITY_MISMATCH")
    deviation = policy.get("deviationTicks")
    if type(deviation) is not int or deviation < 0:
        return reject("PRICE_DEVIATION_POLICY_INVALID")
    if deviation > authority["maximumDeviationTicks"]:
        return reject("PRICE_DEVIATION_POLICY_EXCEEDED")
    if policy.get("symbol") != context.get("symbol"):
        return reject("PRICE_POLICY_SYMBOL_MISMATCH")
    if policy.get("tickSize") != context.get("tickSize") or policy.get("digits") != context.get("digits"):
        return reject("PRICE_POLICY_BROKER_PROPERTY_MISMATCH")
    bid = decimal_value(snapshot.get("bid"))
    ask = decimal_value(snapshot.get("ask"))
    price = decimal_value(canonical_input.get("executionPrice"))
    tick = decimal_value(context.get("tickSize"))
    if None in (bid, ask, price, tick) or bid <= 0 or ask < bid or tick <= 0:
        return reject("PRICE_NUMERIC_DOMAIN_INVALID")
    direction = canonical_input.get("positionDirection")
    center = bid if direction == "BUY" else ask if direction == "SELL" else None
    if center is None:
        return reject("POSITION_DIRECTION_INVALID")
    maximum_delta = tick * deviation
    if price < center - maximum_delta or price > center + maximum_delta:
        return reject("EXECUTION_PRICE_OUTSIDE_AUTHORIZED_RANGE")
    if price % tick != 0:
        return reject("EXECUTION_PRICE_OFF_TICK_GRID")
    return pass_result()


def validate_economic_policy_result(canonical_input: dict[str, Any]) -> dict[str, Any]:
    context = canonical_input.get("context")
    policy = canonical_input.get("economicPolicy")
    if not isinstance(context, dict) or not isinstance(policy, dict):
        return reject("ECONOMIC_POLICY_MALFORMED")
    scenario = policy.get("scenario")
    required = REQUIRED_FORMULAS.get(scenario)
    formula_ids = policy.get("formulaIds")
    source_ids = policy.get("normativeSourceIds")
    if required is None:
        return reject("ECONOMIC_SCENARIO_UNKNOWN")
    if not isinstance(formula_ids, list) or not formula_ids:
        return reject("ECONOMIC_FORMULA_REGISTRY_EMPTY")
    if len(formula_ids) != len(set(formula_ids)):
        return reject("ECONOMIC_FORMULA_DUPLICATE")
    if tuple(formula_ids) != required:
        return reject("ECONOMIC_FORMULA_AUTHORITY_MISMATCH")
    expected_sources = tuple(FORMULA_REGISTRY[formula_id][3] for formula_id in required)
    if not isinstance(source_ids, list) or not source_ids:
        return reject("ECONOMIC_NORMATIVE_SOURCE_REGISTRY_EMPTY")
    if tuple(source_ids) != expected_sources:
        return reject("ECONOMIC_NORMATIVE_SOURCE_AUTHORITY_MISMATCH")
    for formula_id in formula_ids:
        formula = FORMULA_REGISTRY.get(formula_id)
        if formula is None or formula[0] != scenario:
            return reject("ECONOMIC_FORMULA_SCENARIO_MISMATCH")
        if policy.get("units") != formula[1] or policy.get("roundingMode") != formula[2]:
            return reject("ECONOMIC_FORMULA_UNITS_MISMATCH")
    grid_fields = ("volumeStep", "volumeMin", "volumeMax", "tickSize")
    if any(policy.get(field) != context.get(field) for field in grid_fields):
        return reject("ECONOMIC_BROKER_GRID_MISMATCH")
    return pass_result()


def output_state_digest(state: dict[str, Any]) -> str:
    body = {
        key: value
        for key, value in state.items()
        if key not in {"certificate", "outputStateDigest"}
    }
    return digest(body)


def validate_commit_replay(canonical_input: dict[str, Any]) -> dict[str, Any]:
    state = canonical_input.get("persistedState")
    certificate = canonical_input.get("certificate")
    bundle = canonical_input.get("commitBundle")
    context = canonical_input.get("context")
    source_objects = canonical_input.get("sourceObjects")
    if not all(isinstance(value, dict) for value in (state, certificate, bundle, context, source_objects)):
        return reject("COMMIT_SOURCE_OBJECT_MISSING")
    if certificate.get("certificateVersion") != CURRENT_CERTIFICATE_VERSION:
        return reject("COMMIT_CERTIFICATE_VERSION_UNSUPPORTED")
    if set(bundle) != COMMIT_OBJECT_KEYS:
        if COMMIT_OBJECT_KEYS - set(bundle):
            return reject("COMMIT_SOURCE_OBJECT_MISSING")
        return reject("COMMIT_SOURCE_OBJECT_UNKNOWN")
    for name in sorted(COMMIT_OBJECT_KEYS):
        source_object = bundle[name]
        if not isinstance(source_object, dict) or source_object.get("digest") != digest(source_object.get("body")):
            return reject(f"COMMIT_{name.upper()}_RECOMPUTATION_MISMATCH")
        if source_object.get("body") != source_objects.get(name):
            return reject(f"COMMIT_{name.upper()}_RECOMPUTATION_MISMATCH")
        if certificate.get(f"{name}Digest") != source_object["digest"]:
            return reject(f"COMMIT_{name.upper()}_CERTIFICATE_MISMATCH")
    input_revision = certificate.get("inputRevision")
    output_revision = certificate.get("outputRevision")
    if type(input_revision) is not int or type(output_revision) is not int or output_revision != input_revision + 1:
        return reject("COMMIT_STATE_REVISION_DELTA_INVALID")
    if state.get("stateRevision") != output_revision or context.get("stateRevision") != output_revision:
        return reject("COMMIT_STATE_REVISION_MISMATCH")
    fsm_body = bundle["fsm"]["body"]
    if fsm_body.get("inputRevision") != input_revision or fsm_body.get("outputRevision") != output_revision:
        return reject("COMMIT_FSM_REVISION_MISMATCH")
    input_settlement = certificate.get("inputSettlementRevision")
    output_settlement = certificate.get("outputSettlementRevision")
    if type(input_settlement) is not int or output_settlement != input_settlement + 1:
        return reject("COMMIT_SETTLEMENT_REVISION_DELTA_INVALID")
    if state.get("settlementRevision") != output_settlement:
        return reject("COMMIT_SETTLEMENT_REVISION_MISMATCH")
    input_evidence = certificate.get("inputEvidenceRevision")
    output_evidence = certificate.get("outputEvidenceRevision")
    accepted_batch = certificate.get("acceptedBatchCount")
    expected_delta = 1 if type(accepted_batch) is int and accepted_batch > 0 else 0
    if type(input_evidence) is not int or output_evidence != input_evidence + expected_delta:
        return reject("COMMIT_EVIDENCE_REVISION_DELTA_INVALID")
    if state.get("evidenceRevision") != output_evidence:
        return reject("COMMIT_EVIDENCE_REVISION_MISMATCH")
    if state.get("outputStateDigest") != output_state_digest(state):
        return reject("COMMIT_OUTPUT_STATE_RECOMPUTATION_MISMATCH")
    if certificate.get("outputStateDigest") != state.get("outputStateDigest"):
        return reject("COMMIT_OUTPUT_STATE_CERTIFICATE_MISMATCH")
    certificate_body = {key: value for key, value in certificate.items() if key != "certificateDigest"}
    if certificate.get("certificateDigest") != digest(certificate_body):
        return reject("COMMIT_CERTIFICATE_DIGEST_INVALID")
    result = pass_result("ALREADY_COMMITTED")
    result["phase"] = "IDEMPOTENT_REPLAY"
    return result


def build_valid_commit() -> dict[str, Any]:
    """Build an independently recomputable native commit fixture."""
    bundle = {}
    source_objects = {}
    for name in sorted(COMMIT_OBJECT_KEYS):
        if name == "fsm":
            body = {"inputRevision": 3, "outputRevision": 4}
        else:
            body = {"kind": name, "value": 1}
        source_objects[name] = dict(body)
        bundle[name] = {"body": dict(body), "digest": digest(body)}
    state = {
        "stateRevision": 4,
        "settlementRevision": 8,
        "evidenceRevision": 11,
        "ledger": ["D1"],
    }
    state["outputStateDigest"] = output_state_digest(state)
    certificate = {
        "certificateVersion": CURRENT_CERTIFICATE_VERSION,
        "inputRevision": 3,
        "outputRevision": 4,
        "inputSettlementRevision": 7,
        "outputSettlementRevision": 8,
        "inputEvidenceRevision": 10,
        "outputEvidenceRevision": 11,
        "acceptedBatchCount": 1,
        "outputStateDigest": state["outputStateDigest"],
    }
    for name, source_object in bundle.items():
        certificate[f"{name}Digest"] = source_object["digest"]
    certificate["certificateDigest"] = digest(certificate)
    return {
        "schemaVersion": CURRENT_SCHEMA_VERSION,
        "operation": "REPLAY_COMMIT",
        "context": {"stateRevision": 4},
        "persistedState": state,
        "certificate": certificate,
        "commitBundle": bundle,
        "sourceObjects": source_objects,
    }
