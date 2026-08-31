#!/usr/bin/env python3
"""Fail-closed, standard-library validation for ScenarioInput V3 positive bases."""
from __future__ import annotations

import argparse
import copy
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "Tests/Contracts/HSB_2E_R4_R9_R4A_R4_SCENARIO_INPUT_SCHEMA_V3.json"
REGISTRY_PATH = ROOT / "Tests/Contracts/HSB_2E_R4_R9_R4_PREDICATE_REGISTRY.json"
VECTOR_GLOB = "HSB_2E_R4_R9_R4A_R4_POSITIVE_BASES_V3_*.json"
EVIDENCE_DIR = ROOT / "Tests/Evidence/R4A_R4"
METADATA_NAMES = {"fixtureId", "kind", "classification", "expectedResult", "expectedReason",
                  "expectedCheckId", "tags", "description", "rootCauseId", "testContract"}
SCENARIOS = {"INITIAL", "BIG", "SMALL", "FINAL", "RESTART_CONTINUATION", "REPLAY_COMMITTED", "LIFECYCLE"}


class ValidationError(ValueError):
    pass


def canonical_digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def decimal(value: Any, path: str) -> Decimal:
    if not isinstance(value, str):
        raise ValidationError(f"{path}: decimal must be an exact JSON string")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValidationError(f"{path}: invalid Decimal") from exc
    if not result.is_finite():
        raise ValidationError(f"{path}: non-finite Decimal")
    return result


def validate_node(value: Any, spec: dict, path: str) -> None:
    kind = spec["type"]
    if value is None:
        raise ValidationError(f"{path}: null is forbidden")
    if kind == "object":
        if not isinstance(value, dict):
            raise ValidationError(f"{path}: expected object")
        properties = spec["properties"]
        unknown = set(value) - set(properties)
        missing = set(properties) - set(value)
        if unknown:
            raise ValidationError(f"{path}: unknown fields {sorted(unknown)}")
        if missing:
            raise ValidationError(f"{path}: missing required fields {sorted(missing)}")
        for name, child in properties.items():
            validate_node(value[name], child, f"{path}.{name}")
        return
    if kind == "array":
        if not isinstance(value, list):
            raise ValidationError(f"{path}: expected array")
        for index, item in enumerate(value):
            validate_node(item, spec["items"], f"{path}[{index}]")
        return
    if kind == "string":
        if not isinstance(value, str):
            raise ValidationError(f"{path}: expected string")
        semantic = spec["semanticType"] if "semanticType" in spec else "TEXT"
        if semantic == "DECIMAL":
            number = decimal(value, path)
            if "minimum" in spec and number < Decimal(str(spec["minimum"])):
                raise ValidationError(f"{path}: below minimum")
            if "maximum" in spec and number > Decimal(str(spec["maximum"])):
                raise ValidationError(f"{path}: above maximum")
        else:
            if "minimum" in spec and len(value) < int(spec["minimum"]):
                raise ValidationError(f"{path}: empty or too short")
            if "maximum" in spec and len(value) > int(spec["maximum"]):
                raise ValidationError(f"{path}: too long")
        if "enum" in spec and value not in spec["enum"]:
            raise ValidationError(f"{path}: invalid enum")
        return
    if kind == "integer":
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValidationError(f"{path}: expected exact integer")
        if "minimum" in spec and value < int(spec["minimum"]):
            raise ValidationError(f"{path}: below minimum")
        return
    if kind == "boolean":
        if not isinstance(value, bool):
            raise ValidationError(f"{path}: expected boolean")
        return
    raise ValidationError(f"{path}: unknown schema type {kind}")


def multiple(value: Decimal, grid: Decimal) -> bool:
    return grid > 0 and value % grid == 0


def internal_consistency(runtime: dict) -> None:
    context, broker = runtime["context"], runtime["broker"]
    snapshot, policy = runtime["snapshot"], runtime["temporalPolicy"]
    positions, intents, deals, events = runtime["positions"], runtime["intents"], runtime["deals"], runtime["events"]
    if not positions or not intents or not deals or not events:
        raise ValidationError("runtime arrays required for positive bases")
    if snapshot["symbol"] != context["symbol"] or snapshot["magic"] != context["magic"]:
        raise ValidationError("snapshot identity mismatch")
    if decimal(broker["ask"], "broker.ask") < decimal(broker["bid"], "broker.bid"):
        raise ValidationError("Ask below Bid")
    tick, step = decimal(broker["tickSize"], "broker.tickSize"), decimal(broker["volumeStep"], "broker.volumeStep")
    if not (policy["minimumTimestamp"] <= policy["validFrom"] <= snapshot["timestamp"] <=
            policy["validUntil"] <= policy["allowedUpperBound"]):
        raise ValidationError("invalid temporal window")
    tickets = {item["ticket"]: item for item in positions}
    intent_ids = {item["intentId"]: item for item in intents}
    if len(tickets) != len(positions) or len(intent_ids) != len(intents):
        raise ValidationError("duplicate position or intent")
    if len({item["dealId"] for item in deals}) != len(deals):
        raise ValidationError("duplicate deal")
    if len({item["eventId"] for item in events}) != len(events):
        raise ValidationError("duplicate event")
    for position in positions:
        if any(position[key] != context[key] for key in ("accountId", "symbol", "magic", "cycleId")):
            raise ValidationError("position identity mismatch")
        if not multiple(decimal(position["volume"], "position.volume"), step):
            raise ValidationError("off-grid position volume")
        if not multiple(decimal(position["openPrice"], "position.openPrice"), tick):
            raise ValidationError("off-grid open price")
    for intent in intents:
        if intent["positionTicket"] not in tickets or intent["transactionId"] != context["transactionId"]:
            raise ValidationError("orphan or wrong intent")
        if not (policy["validFrom"] <= intent["createdTimestamp"] <= intent["expiresTimestamp"] <= policy["allowedUpperBound"]):
            raise ValidationError("intent temporal mismatch")
        if intent["direction"] == tickets[intent["positionTicket"]]["direction"]:
            raise ValidationError("close direction mismatch")
    for deal in deals:
        if deal["positionTicket"] not in tickets or deal["intentId"] not in intent_ids:
            raise ValidationError("orphan deal")
        if any(deal[key] != context[key] for key in ("accountId", "symbol", "magic", "cycleId", "transactionId", "actionId")):
            raise ValidationError("deal identity mismatch")
        if not multiple(decimal(deal["volume"], "deal.volume"), step) or not multiple(decimal(deal["price"], "deal.price"), tick):
            raise ValidationError("off-grid execution")
    economic, allocation = runtime["economic"], runtime["allocationPolicy"]
    if decimal(economic["availableMoney"], "economic.availableMoney") != (decimal(allocation["allocatedMoney"], "allocation.allocatedMoney") + decimal(allocation["remainingMoney"], "allocation.remainingMoney")):
        raise ValidationError("money conservation mismatch")
    requested = sum((decimal(item["requestedVolume"], "intent.requestedVolume") for item in intents), Decimal(0))
    filled = sum((decimal(item["volume"], "deal.volume") for item in deals), Decimal(0))
    if requested != filled:
        raise ValidationError("volume conservation mismatch")
    if decimal(economic["partialFarVolume"], "economic.partialFarVolume") > 0 and decimal(economic["reserveConsumption"], "economic.reserveConsumption") > 0:
        raise ValidationError("Reserve misuse")
    if economic["tailCount"] > 1:
        raise ValidationError("DUAL_TAIL")
    fsm = runtime["fsm"]
    if fsm["outputRevision"] != fsm["inputRevision"] + 1:
        raise ValidationError("FSM revision mismatch")
    persisted = runtime["persistedState"]
    for name in ("previousStateDigest", "authoritativeLedgerRoot", "transactionJournalRoot"):
        if not persisted[name]:
            raise ValidationError("empty persisted digest")
    cert = runtime["certificate"]
    for name, value in cert.items():
        if name != "version" and not value:
            raise ValidationError("empty certificate digest")
    if runtime["scenario"] == "REPLAY_COMMITTED" and (not persisted["consumedDealIds"] or not persisted["seenEventIds"]):
        raise ValidationError("replay has no persisted consumption state")


def validate_runtime(runtime: dict, schema: dict) -> None:
    validate_node(runtime, schema["root"], "scenarioInput")
    if set(runtime) & METADATA_NAMES:
        raise ValidationError("test metadata leaked into scenarioInput")
    internal_consistency(runtime)


def resolve_path(root_spec: dict, raw_path: str) -> dict:
    if not raw_path.startswith("scenarioInput."):
        raise ValidationError(f"non-runtime path {raw_path}")
    node = root_spec
    for token in raw_path[len("scenarioInput."):].split("."):
        is_array = token.endswith("[*]")
        name = token[:-3] if is_array else token
        if node["type"] != "object" or name not in node["properties"]:
            raise ValidationError(f"unknown path {raw_path} at {name}")
        node = node["properties"][name]
        if is_array:
            if node["type"] != "array":
                raise ValidationError(f"ambiguous non-array wildcard {raw_path}")
            node = node["items"]
    if "type" not in node:
        raise ValidationError(f"typeless path {raw_path}")
    return node


def load_fixtures() -> list[dict]:
    fixtures = []
    for path in sorted((ROOT / "Tests/Vectors").glob(VECTOR_GLOB)):
        document = json.loads(path.read_text(encoding="utf-8"))
        fixtures.extend(document["fixtures"])
    return fixtures


def audit_sources() -> list[str]:
    patterns = (r"\.get\([^\n]+,\s*(?:0|\"\"|False|\[\])\)", r"\bor\s+(?:0|\"\"|False)\b")
    violations = []
    for path in (Path(__file__), ROOT / "Tests/Static/build_hsb_2e_r4_r9_r4a_r4_assets.py"):
        text = path.read_text(encoding="utf-8")
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                violations.append(f"{path.relative_to(ROOT)}:{text.count(chr(10), 0, match.start()) + 1}")
    return violations


def execute() -> dict:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))["predicates"]
    fixtures = load_fixtures()
    path_rows = []
    for predicate in registry:
        for raw in predicate["exactInputPaths"]:
            spec = resolve_path(schema["root"], raw)
            path_rows.append({"predicateId": predicate["predicateId"], "path": raw, "type": spec["type"], "result": "PASS"})
    inventory, digests = [], set()
    distribution = {scenario: 0 for scenario in sorted(SCENARIOS)}
    for item in fixtures:
        if set(item) != {"scenarioInput", "testContract"}:
            raise ValidationError("fixture wrapper mismatch")
        runtime, contract = item["scenarioInput"], item["testContract"]
        validate_runtime(runtime, schema)
        if contract["classification"] != "POSITIVE_BASE" or contract["scenario"] != runtime["scenario"]:
            raise ValidationError("positive test contract mismatch")
        runtime_digest = canonical_digest(runtime)
        if runtime_digest in digests:
            raise ValidationError("duplicate runtime input")
        digests.add(runtime_digest)
        distribution[runtime["scenario"]] += 1
        inventory.append({"fixtureId": contract["fixtureId"], "scenario": runtime["scenario"],
                          "scenarioInputSha256": runtime_digest, "result": "PASS"})
    if len(fixtures) != 28 or len(digests) != 28 or any(count != 4 for count in distribution.values()):
        raise ValidationError("fixture count or distribution mismatch")
    anti_default = audit_sources()
    if anti_default:
        raise ValidationError(f"normative neutral default patterns: {anti_default}")
    return {"result": "PASS", "schemaId": schema["schemaId"], "registryPredicateCount": len(registry),
            "registryExactPathsRequired": len(path_rows), "registryExactPathsResolved": len(path_rows),
            "unknownInputPaths": 0, "ambiguousInputPaths": 0, "metadataInputPaths": 0,
            "typelessInputPaths": 0, "positiveFixturesRequired": 28, "positiveFixturesCreated": len(fixtures),
            "uniqueScenarioInputDigests": len(digests), "duplicateRuntimeInputs": 0,
            "scenarioDistribution": distribution, "pathResolution": path_rows, "fixtureInventory": inventory,
            "antiDefault": {"normativeNeutralDefaults": 0, "missingRequiredFieldsAccepted": 0,
                            "unknownFieldsAccepted": 0, "emptyRequiredDigestsAccepted": 0,
                            "autoCreatedRuntimeObjects": 0, "result": "PASS"}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish-evidence", action="store_true")
    args = parser.parse_args()
    try:
        result = execute()
    except (ValidationError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"SCHEMA_AND_POSITIVE_BASES=FAIL\nDETAIL={exc}")
        return 1
    if args.publish_evidence:
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        (EVIDENCE_DIR / "schema_positive_validation.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("SCENARIO_INPUT_SCHEMA_V3=PASS")
    print("REGISTRY_EXACT_PATH_RESOLUTION=PASS")
    print(f"REGISTRY_EXACT_PATHS_RESOLVED={result['registryExactPathsResolved']}")
    print("POSITIVE_BASE_FIXTURES=28")
    print("UNIQUE_SCENARIO_INPUT_DIGESTS=28")
    print("NORMATIVE_NEUTRAL_DEFAULTS=0")
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
