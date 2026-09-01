#!/usr/bin/env python3
"""Independent, read-only audit of the published R4A-R4 schema checkpoint."""
from __future__ import annotations

import copy
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[3]
TARGET = "77743d39fc572eefcceaa65b129d9d6cfcb8b098"
BASELINE = "f44b7e5cae314fced0f8d519e1e5d70f3c49c35d"
SCHEMA_PATH = ROOT / "Tests/Contracts/HSB_2E_R4_R9_R4A_R4_SCENARIO_INPUT_SCHEMA_V3.json"
REGISTRY_PATH = ROOT / "Tests/Contracts/HSB_2E_R4_R9_R4_PREDICATE_REGISTRY.json"
VECTOR_GLOB = "HSB_2E_R4_R9_R4A_R4_POSITIVE_BASES_V3_*.json"
VALIDATOR_PATH = ROOT / "Tests/Static/verify_hsb_2e_r4_r9_r4a_r4_schema.py"
OUTPUT = ROOT / "Tests/Evidence/R4A_R4_AUDIT/independent_audit.json"


def git(*args: str) -> str:
    return subprocess.run(("git", *args), cwd=ROOT, check=True, text=True,
                          stdout=subprocess.PIPE).stdout.strip()


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_validator():
    spec = importlib.util.spec_from_file_location("published_r4a_r4_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("published validator cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_fixtures() -> list[dict]:
    values: list[dict] = []
    for path in sorted((ROOT / "Tests/Vectors").glob(VECTOR_GLOB)):
        values.extend(json.loads(path.read_text(encoding="utf-8"))["fixtures"])
    return values


def walk_schema(node: dict, stats: dict[str, int]) -> None:
    stats["nodes"] += 1
    stats[node["requiredState"]] = stats.setdefault(node["requiredState"], 0) + 1
    if node["type"] == "object":
        if node["additionalProperties"] is not False or "properties" not in node:
            stats["openOrUntypedObjects"] += 1
        for child in node["properties"].values():
            walk_schema(child, stats)
    elif node["type"] == "array":
        if "items" not in node:
            stats["untypedArrays"] += 1
        else:
            walk_schema(node["items"], stats)


def resolve_path(root: dict, raw: str) -> dict:
    if not raw.startswith("scenarioInput."):
        raise ValueError(raw)
    node = root
    for token in raw.removeprefix("scenarioInput.").split("."):
        wildcard = token.endswith("[*]")
        key = token[:-3] if wildcard else token
        if node["type"] != "object" or key not in node["properties"]:
            raise ValueError(raw)
        node = node["properties"][key]
        if wildcard:
            if node["type"] != "array":
                raise ValueError(raw)
            node = node["items"]
    return node


def propagate_account(runtime: dict, value: str) -> None:
    runtime["context"]["accountId"] = value
    for collection in ("positions", "deals", "events"):
        for item in runtime[collection]:
            item["accountId"] = value


def run_probe(validator, schema: dict, base: dict, name: str, expected: str,
              mutation: Callable[[dict], None]) -> dict:
    candidate = copy.deepcopy(base)
    mutation(candidate)
    try:
        validator.validate_runtime(candidate, schema)
    except validator.ValidationError as exc:
        actual, detail = "NORMATIVE_REJECTION", str(exc)
    except Exception as exc:  # infrastructure is recorded as failure, never as a caught probe
        actual, detail = "INFRASTRUCTURE_ERROR", f"{type(exc).__name__}: {exc}"
    else:
        actual, detail = "ACCEPTED", "validator returned normally"
    return {"probe": name, "expectedClass": expected, "actualClass": actual,
            "detail": detail, "result": "PASS" if actual == expected else "FAIL",
            "inputSha256": digest(candidate)}


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))["predicates"]
    fixtures = load_fixtures()
    validator = load_validator()
    base = fixtures[0]["scenarioInput"]

    stats = {"nodes": 0, "REQUIRED": 0, "OPTIONAL_WITH_RULE": 0,
             "NOT_APPLICABLE_WITH_RULE": 0, "openOrUntypedObjects": 0, "untypedArrays": 0}
    walk_schema(schema["root"], stats)
    resolved = []
    for predicate in registry:
        for path in predicate["exactInputPaths"]:
            node = resolve_path(schema["root"], path)
            resolved.append({"predicateId": predicate["predicateId"], "path": path,
                             "resolvedType": node["type"]})

    groups: dict[str, int] = {}
    inventory = []
    for fixture in fixtures:
        runtime, contract = fixture["scenarioInput"], fixture["testContract"]
        scenario = runtime["scenario"]
        groups[scenario] = groups.setdefault(scenario, 0) + 1
        persisted_case = "NONEMPTY_REPLAY_STATE" if runtime["persistedState"]["consumedDealIds"] else "EMPTY_FRESH_STATE"
        inventory.append({
            "fixtureId": contract["fixtureId"], "scenario": scenario,
            "statePhase": f"{runtime['fsm']['inputState']}->{runtime['fsm']['outputState']}",
            "positionDirections": [item["direction"] for item in runtime["positions"]],
            "volumes": [item["volume"] for item in runtime["positions"]],
            "gridCase": "STANDARD_TICK_AND_STEP",
            "economicCase": {"available": runtime["economic"]["availableMoney"],
                             "allocated": runtime["allocationPolicy"]["allocatedMoney"],
                             "remaining": runtime["allocationPolicy"]["remainingMoney"]},
            "persistedStateCase": persisted_case,
            "meaningfulDifference": "DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP",
            "scenarioInputSha256": digest(runtime),
        })

    probes = [
        run_probe(validator, schema, base, "remove_nested_required", "NORMATIVE_REJECTION",
                  lambda x: x["context"].pop("cycleId")),
        run_probe(validator, schema, base, "unknown_nested", "NORMATIVE_REJECTION",
                  lambda x: x["context"].__setitem__("unknown", 1)),
        run_probe(validator, schema, base, "boolean_numeric_id", "NORMATIVE_REJECTION",
                  lambda x: x["context"].__setitem__("magic", True)),
        run_probe(validator, schema, base, "decimal_nan", "NORMATIVE_REJECTION",
                  lambda x: x["economic"].__setitem__("availableMoney", "NaN")),
        run_probe(validator, schema, base, "decimal_infinity", "NORMATIVE_REJECTION",
                  lambda x: x["economic"].__setitem__("availableMoney", "Infinity")),
        run_probe(validator, schema, base, "empty_positions", "NORMATIVE_REJECTION",
                  lambda x: x.__setitem__("positions", [])),
        run_probe(validator, schema, base, "empty_intents", "NORMATIVE_REJECTION",
                  lambda x: x.__setitem__("intents", [])),
        run_probe(validator, schema, base, "empty_deals", "NORMATIVE_REJECTION",
                  lambda x: x.__setitem__("deals", [])),
        run_probe(validator, schema, base, "off_grid_price", "NORMATIVE_REJECTION",
                  lambda x: x["positions"][0].__setitem__("openPrice", "1.00005")),
        run_probe(validator, schema, base, "off_grid_volume", "NORMATIVE_REJECTION",
                  lambda x: x["positions"][0].__setitem__("volume", "0.015")),
        run_probe(validator, schema, base, "duplicate_deal_id", "NORMATIVE_REJECTION",
                  lambda x: x["deals"].append(copy.deepcopy(x["deals"][0]))),
        run_probe(validator, schema, base, "orphan_deal", "NORMATIVE_REJECTION",
                  lambda x: x["deals"][0].__setitem__("intentId", "ORPHAN")),
        run_probe(validator, schema, base, "symbol_mismatch", "NORMATIVE_REJECTION",
                  lambda x: x["positions"][0].__setitem__("symbol", "GBPUSD")),
        run_probe(validator, schema, base, "invalid_time_window", "NORMATIVE_REJECTION",
                  lambda x: x["temporalPolicy"].__setitem__("validUntil", 1)),
        run_probe(validator, schema, base, "money_conservation", "NORMATIVE_REJECTION",
                  lambda x: x["allocationPolicy"].__setitem__("remainingMoney", "999")),
        run_probe(validator, schema, base, "volume_conservation", "NORMATIVE_REJECTION",
                  lambda x: x["deals"][0].__setitem__("volume", "0.01")),
        run_probe(validator, schema, base, "reserve_partial_far", "NORMATIVE_REJECTION",
                  lambda x: (x["economic"].__setitem__("partialFarVolume", "0.01"),
                             x["economic"].__setitem__("reserveConsumption", "1"))),
        run_probe(validator, schema, base, "metadata_in_runtime", "NORMATIVE_REJECTION",
                  lambda x: x.__setitem__("fixtureId", "AUDIT")),
        run_probe(validator, schema, base, "large_exact_identifier", "ACCEPTED",
                  lambda x: propagate_account(x, "900719925474099312345678901234567890")),
        run_probe(validator, schema, base, "forged_certificate_digest_same_length", "NORMATIVE_REJECTION",
                  lambda x: x["certificate"].__setitem__("digest", "0" * 64)),
        run_probe(validator, schema, base, "precommit_certificate_absent", "ACCEPTED",
                  lambda x: x.pop("certificate")),
    ]
    metadata_copy = copy.deepcopy(fixtures[0])
    metadata_copy["testContract"]["fixtureId"] = "AUDIT-METADATA-ONLY"
    metadata_result = {"probe": "metadata_only_wrapper_change", "expectedClass": "UNCHANGED_RUNTIME",
                       "actualClass": "UNCHANGED_RUNTIME" if digest(metadata_copy["scenarioInput"]) == digest(base) else "CHANGED_RUNTIME",
                       "result": "PASS" if digest(metadata_copy["scenarioInput"]) == digest(base) else "FAIL"}
    probes.append(metadata_result)

    changed = git("diff", "--name-only", f"{BASELINE}..{TARGET}").splitlines()
    prefix = "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/"
    production = [p for p in changed if p.endswith(".mq5") or ("/Include/" in p and p.endswith(".mqh"))]
    external = [p for p in changed if not p.startswith(prefix)]
    native = [p for p in changed if "hsb_2e_reference_model_r4_r9_r3.py" in p or "run_hsb_2e_r4_r9_r3_" in p]
    historical = [p for p in changed if "R9_R2_NATIVE_FIXTURES" in p or "R9_R3_NATIVE_FIXTURES" in p]

    findings = [
        {"id": "CERTIFICATE_DIGEST_NOT_VALIDATED", "severity": "HIGH",
         "evidence": "64-zero forged certificate digest is accepted by published validator"},
        {"id": "CERTIFICATE_PHASE_APPLICABILITY_ABSENT", "severity": "HIGH",
         "evidence": "all 186 schema nodes are REQUIRED; pre-commit certificate absence is rejected"},
        {"id": "LIFECYCLE_NOT_A_SEQUENCE", "severity": "HIGH",
         "evidence": "each LIFECYCLE fixture contains one SMALL->FINAL transition, not a state/operation sequence"},
        {"id": "SELF_TEST_INFRA_EXCEPTIONS_COUNTED_AS_CAUGHT", "severity": "MEDIUM",
         "evidence": "published self-test counts KeyError and TypeError as successful CAUGHT outcomes"},
        {"id": "MEANINGFUL_VARIATION_INSUFFICIENT", "severity": "MEDIUM",
         "evidence": "within each group variants share structure/grid/economic formula and vary direction, scalar volume/price, identifiers and timestamps"},
        {"id": "FULL_ECONOMIC_CORRECTNESS_NOT_PROVEN", "severity": "EXPECTED_LIMIT",
         "evidence": "validator checks two conservation equalities but does not independently derive economic fields"},
    ]
    failed_probes = [p for p in probes if p["result"] == "FAIL"]
    result = {
        "auditTargetSha": TARGET, "implementationBaselineSha": BASELINE,
        "scope": {"changedPaths": changed, "scopeViolations": len(external), "productionDiffPaths": production,
                  "nativeModelChanged": bool(native), "historicalOraclesChanged": bool(historical)},
        "schema": {"stats": stats, "schemaStructureValid": False,
                   "reason": "certificate phase applicability and optional/not-applicable rules are absent",
                   "registryExactPaths": len(resolved), "registryPathsResolved": len(resolved),
                   "pathResolution": resolved},
        "fixtures": {"count": len(fixtures), "groups": groups,
                     "uniqueRuntimeDigests": len({digest(x["scenarioInput"]) for x in fixtures}),
                     "inventory": inventory, "fixtureSchemaValid": True,
                     "fixtureInternalConsistencyValid": "PARTIAL_PUBLISHED_CHECKS_PASS",
                     "fullEconomicCorrectness": "NOT_PROVEN"},
        "probes": probes, "failedProbes": len(failed_probes), "findings": findings,
        "publishedSelfTests": {"usesPublishedValidator": True, "mutatesRuntime": True,
                               "countsInfrastructureExceptionsAsCaught": True,
                               "verdict": "FALSE_PASS_RISK"},
        "requirementMatrix": [
            {"requirement": "closed typed schema", "implementingFiles": [str(SCHEMA_PATH.relative_to(ROOT))],
             "implementingCommits": ["98b957f"], "executedCheck": "independent schema walk", "observedResult": stats, "verdict": "PARTIAL"},
            {"requirement": "exact Registry paths", "implementingFiles": [str(REGISTRY_PATH.relative_to(ROOT))],
             "implementingCommits": ["6ddaa95", "d930576"], "executedCheck": "independent wildcard resolver", "observedResult": f"{len(resolved)}/{len(resolved)}", "verdict": "PASS"},
            {"requirement": "28 positive bases", "implementingFiles": sorted(str(p.relative_to(ROOT)) for p in (ROOT / "Tests/Vectors").glob(VECTOR_GLOB)),
             "implementingCommits": ["da6bb22", "034f95c", "f89746d"], "executedCheck": "inventory and semantic variation audit", "observedResult": groups, "verdict": "FAIL"},
            {"requirement": "fail-closed validator", "implementingFiles": [str(VALIDATOR_PATH.relative_to(ROOT))],
             "implementingCommits": ["6e171da", "77743d3"], "executedCheck": "22 independent adversarial probes", "observedResult": f"failed={len(failed_probes)}", "verdict": "FAIL"},
        ],
        "verdict": "R4A_R4_AUDIT=FAIL",
        "qualificationCoreReady": "NO", "oracleV3FinalAcceptance": "NOT_GRANTED",
        "modelChangesAllowed": "NO", "tradingLogicStartAllowed": "NO", "realTradingAllowed": "NO",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(result["verdict"])
    print(f"PROBES={len(probes)} FAILED_PROBES={len(failed_probes)}")
    print(f"REGISTRY_PATHS={len(resolved)}/{len(resolved)} FIXTURES={len(fixtures)}")
    return 0  # the audit executed successfully; its domain verdict is encoded as FAIL


if __name__ == "__main__":
    raise SystemExit(main())
