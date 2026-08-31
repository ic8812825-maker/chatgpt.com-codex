#!/usr/bin/env python3
"""Adversarial self-tests for the R4A-R4 schema/completeness boundary."""
from __future__ import annotations

import copy
import json

import verify_hsb_2e_r4_r9_r4a_r4_schema as verifier


def main() -> int:
    schema = json.loads(verifier.SCHEMA_PATH.read_text(encoding="utf-8"))
    original = verifier.load_fixtures()[0]["scenarioInput"]
    cases = []

    def add(name, mutate):
        cases.append((name, mutate))

    add("missing_required", lambda x: x["context"].pop("accountId"))
    add("unknown_field", lambda x: x.__setitem__("unknown", 1))
    add("wrong_type", lambda x: x["context"].__setitem__("magic", "8812825"))
    add("nan", lambda x: x["economic"].__setitem__("availableMoney", "NaN"))
    add("infinity", lambda x: x["economic"].__setitem__("availableMoney", "Infinity"))
    add("empty_id", lambda x: x["context"].__setitem__("cycleId", ""))
    add("float_identifier", lambda x: x["context"].__setitem__("accountId", 1.5))
    add("negative_volume", lambda x: x["positions"][0].__setitem__("volume", "-0.01"))
    add("off_grid_volume", lambda x: x["positions"][0].__setitem__("volume", "0.015"))
    add("off_grid_price", lambda x: x["positions"][0].__setitem__("openPrice", "1.10005"))
    add("ask_below_bid", lambda x: x["broker"].__setitem__("ask", "0.9000"))
    add("timestamp_window", lambda x: x["temporalPolicy"].__setitem__("validUntil", 1))
    add("duplicate_deal", lambda x: x["deals"].append(copy.deepcopy(x["deals"][0])))
    add("duplicate_event", lambda x: x["events"].append(copy.deepcopy(x["events"][0])))
    add("missing_position", lambda x: x.__setitem__("positions", []))
    add("missing_intent", lambda x: x.__setitem__("intents", []))
    add("orphan_deal", lambda x: x["deals"][0].__setitem__("intentId", "NO-SUCH-INTENT"))
    add("wrong_symbol", lambda x: x["positions"][0].__setitem__("symbol", "GBPUSD"))
    add("wrong_magic", lambda x: x["positions"][0].__setitem__("magic", 42))
    add("wrong_ticket", lambda x: x["intents"][0].__setitem__("positionTicket", "NO-TICKET"))
    add("wrong_direction", lambda x: x["intents"][0].__setitem__("direction", x["positions"][0]["direction"]))
    add("revision_mismatch", lambda x: x["fsm"].__setitem__("outputRevision", x["fsm"]["inputRevision"] + 2))
    add("money_conservation", lambda x: x["allocationPolicy"].__setitem__("remainingMoney", "999"))
    add("volume_conservation", lambda x: x["deals"][0].__setitem__("volume", "0.01"))
    add("reserve_misuse", lambda x: (x["economic"].__setitem__("partialFarVolume", "0.01"), x["economic"].__setitem__("reserveConsumption", "1")))
    add("dual_tail", lambda x: x["economic"].__setitem__("tailCount", 2))
    add("invalid_fsm_revision", lambda x: x["fsm"].__setitem__("outputRevision", x["fsm"]["inputRevision"]))
    add("empty_digest", lambda x: x["certificate"].__setitem__("digest", ""))
    add("metadata_in_runtime", lambda x: x.__setitem__("fixtureId", "LEAK"))
    add("invalid_enum", lambda x: x.__setitem__("scenario", "UNKNOWN"))

    caught, details = 0, []
    for name, mutate in cases:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        try:
            verifier.validate_runtime(candidate, schema)
        except (verifier.ValidationError, KeyError, TypeError):
            caught += 1
            details.append({"case": name, "result": "CAUGHT"})
        else:
            details.append({"case": name, "result": "SURVIVED"})
    try:
        verifier.validate_unique_runtime_inputs([original, copy.deepcopy(original)])
    except verifier.ValidationError:
        duplicate_caught = True
    else:
        duplicate_caught = False
    details.append({"case": "duplicated_runtime_input", "result": "CAUGHT" if duplicate_caught else "SURVIVED"})
    if duplicate_caught:
        caught += 1
    result = {"schemaSelfTestsRequired": 30, "schemaSelfTestsExecuted": len(details),
              "schemaSelfTestsCaught": caught, "schemaSelfTestsFailed": len(details) - caught,
              "cases": details, "result": "PASS" if caught == len(details) else "FAIL"}
    if "--publish-evidence" in __import__("sys").argv:
        verifier.EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        path = verifier.EVIDENCE_DIR / "schema_adversarial_self_tests.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"SCHEMA_SELF_TESTS_REQUIRED={result['schemaSelfTestsRequired']}")
    print(f"SCHEMA_SELF_TESTS_EXECUTED={result['schemaSelfTestsExecuted']}")
    print(f"SCHEMA_SELF_TESTS_CAUGHT={result['schemaSelfTestsCaught']}")
    print(f"SCHEMA_SELF_TESTS_FAILED={result['schemaSelfTestsFailed']}")
    print(f"RESULT={result['result']}")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
