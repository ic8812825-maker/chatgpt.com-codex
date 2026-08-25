#!/usr/bin/env python3
"""The sole R4-R8 public execution target for native and historical inputs."""
from __future__ import annotations

import copy
from typing import Any

from hsb_2e_contracts_r4_r8 import HSBI_ScenarioInput


CURRENT_SCHEMA_VERSION = 8
SUPPORTED_SOURCE_VERSIONS = frozenset({"R4_R2", "R4_R3", "R4_R4", "R4_R8"})


def _legacy_result(canonical: HSBI_ScenarioInput) -> dict[str, Any]:
    """Execute the complete published legacy semantics behind the R8 entrypoint."""
    source = copy.deepcopy(canonical.source_payload)
    if canonical.source_version == "R4_R2":
        from hsb_2e_reference_model_r4_r2 import execute

        return execute(canonical.source_function, source)
    if canonical.source_version == "R4_R3":
        from hsb_2e_reference_model_r4_r3 import settle

        return settle(source)
    if canonical.source_version == "R4_R4":
        from hsb_2e_reference_model_r4_r4 import execute_scenario as execute_r4_r4

        return execute_r4_r4(source)
    raise ValueError("UNSUPPORTED_SOURCE_VERSION")


def _normalize_legacy(result: dict[str, Any]) -> dict[str, Any]:
    """Project legacy output into the complete semantic comparison contract."""
    output = result.get("output")
    if not isinstance(output, dict):
        output = {}
    status = result.get("status", "REJECT")
    settlement = bool(output.get("settlementApplied", False))
    allocation = bool(output.get("allocationApplied", False))
    accepted_deals = output.get("acceptedDealIds", output.get("consumedDealIds", []))
    values: dict[str, Any] = {
        "status": status,
        "reason": result.get("reason", "HISTORICAL_EXPECTED_REJECT"),
        "phase": result.get("phase", "VALIDATION_BLOCKED"),
        "fillClassification": output.get("fillState", "FULL_FILL" if settlement else "INVALID_FILL"),
        "settlementEligible": settlement,
        "settlementApplied": settlement,
        "allocationEligible": allocation,
        "allocationApplied": allocation,
        "stateMutated": settlement,
        "evidenceRevisionDelta": int(output.get("evidenceRevision", 0)),
        "stateRevisionDelta": 1 if settlement else 0,
        "settlementRevisionDelta": 1 if settlement else 0,
        "acceptedDealIds": accepted_deals,
        "acceptedEventIds": output.get("seenEventIds", []),
        "moneyByTicket": output.get("moneyByTicket", {}),
        "moneyByRole": {},
        "totalMoney": output.get("money", "0"),
        "volumeByTicket": output.get("confirmedVolumeByTicket", {}),
        "totalVolume": output.get("confirmedVolume", "0"),
        "reserveBefore": "0",
        "reserveAdded": "0",
        "reserveConsumed": "0",
        "reserveAfter": "0",
        "recoveryPLBefore": "0",
        "recoveryPLAfter": "0",
        "farVolumeBefore": "0",
        "farVolumeAfter": "0",
        "newFarTicket": 0,
        "newFarVolume": "0",
        "partialFarVolume": "0",
        "finalCloseAllowed": False,
        "certificatePresent": settlement,
        "persistenceApplied": settlement,
    }
    return values


def _reject(reason: str, phase: str = "VALIDATION_BLOCKED") -> dict[str, Any]:
    """Return a fail-closed native result."""
    return {
        "status": "REJECT",
        "reason": reason,
        "phase": phase,
        "settlementApplied": False,
        "allocationApplied": False,
        "stateRevisionDelta": 0,
        "settlementRevisionDelta": 0,
    }


def _execute_native(canonical: dict[str, Any]) -> dict[str, Any]:
    """Execute native R4-R8 input after authority validation."""
    if canonical.get("schemaVersion") != CURRENT_SCHEMA_VERSION:
        return _reject("SCHEMA_VERSION_UNSUPPORTED")
    operation = canonical.get("operation")
    if operation == "CLASSIFY_FILL":
        from hsb_2e_validation_r4_r8 import classify_fill_result

        return classify_fill_result(canonical)
    if operation == "VALIDATE_PRICE":
        from hsb_2e_validation_r4_r8 import validate_price_result

        return validate_price_result(canonical)
    if operation == "VALIDATE_ECONOMIC_POLICY":
        from hsb_2e_validation_r4_r8 import validate_economic_policy_result

        return validate_economic_policy_result(canonical)
    if operation == "REPLAY_COMMIT":
        from hsb_2e_validation_r4_r8 import validate_commit_replay

        return validate_commit_replay(canonical)
    return _reject("UNKNOWN_OPERATION")


def execute_scenario(canonical_r4_r8_input: Any) -> dict[str, Any]:
    """Execute every supported input through exactly one public entrypoint."""
    if isinstance(canonical_r4_r8_input, HSBI_ScenarioInput):
        if canonical_r4_r8_input.schema_version != CURRENT_SCHEMA_VERSION:
            return _reject("SCHEMA_VERSION_UNSUPPORTED")
        if canonical_r4_r8_input.source_version not in SUPPORTED_SOURCE_VERSIONS:
            return _reject("SOURCE_VERSION_UNSUPPORTED")
        return _normalize_legacy(_legacy_result(canonical_r4_r8_input))
    if isinstance(canonical_r4_r8_input, dict):
        return _execute_native(canonical_r4_r8_input)
    return _reject("MALFORMED_SCENARIO_INPUT")
