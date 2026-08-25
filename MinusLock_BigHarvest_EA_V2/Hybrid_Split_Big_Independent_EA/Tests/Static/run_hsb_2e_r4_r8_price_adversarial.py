#!/usr/bin/env python3
"""Adversarial checks for the immutable execution-price authority."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path


def valid_input() -> dict:
    context = {
        "accountLogin": 1,
        "symbol": "EURUSD",
        "magic": 7,
        "cycleId": "C",
        "stateRevision": 3,
        "snapshotId": "S",
        "snapshotRevision": 2,
        "tickSize": "0.00001",
        "digits": 5,
    }
    return {
        "schemaVersion": 8,
        "operation": "VALIDATE_PRICE",
        "context": context,
        "snapshot": {**context, "bid": "1.10000", "ask": "1.10010"},
        "pricePolicy": {
            "policyId": "EXACT_CLOSE_SIDE",
            "normativeSourceId": "HSBI-PRICE-R8",
            "symbol": "EURUSD",
            "tickSize": "0.00001",
            "digits": 5,
            "deviationTicks": 10,
            "buyCloseSide": "BID",
            "sellCloseSide": "ASK",
        },
        "positionDirection": "BUY",
        "executionPrice": "1.10000",
    }


def run(root: str) -> bool:
    project = Path(root).resolve()
    sys.path.insert(0, str(project / "Tests/Reference"))
    from hsb_2e_reference_model_r4_r8 import execute_scenario

    cases = []
    normal = execute_scenario(valid_input())
    cases.append(("R8_PRICE_VALID", normal["status"] == "PASS"))
    excessive = valid_input()
    excessive["pricePolicy"]["deviationTicks"] = 10_000_000_000
    excessive["executionPrice"] = "99999.00000"
    excessive_result = execute_scenario(excessive)
    cases.append(("R8_PRICE_MAXIMUM_DEVIATION", excessive_result["status"] == "REJECT" and excessive_result["reason"] == "PRICE_DEVIATION_POLICY_EXCEEDED"))
    foreign = valid_input()
    foreign["snapshot"]["accountLogin"] = 99
    foreign_result = execute_scenario(foreign)
    cases.append(("R8_PRICE_SNAPSHOT_CONTEXT", foreign_result["status"] == "REJECT" and foreign_result["reason"] == "SNAPSHOT_CONTEXT_IDENTITY_MISMATCH"))
    sides = valid_input()
    sides["pricePolicy"]["buyCloseSide"] = "ASK"
    sides_result = execute_scenario(sides)
    cases.append(("R8_PRICE_BUY_BID", sides_result["status"] == "REJECT" and sides_result["reason"] == "NORMATIVE_CLOSE_SIDE_MISMATCH"))
    sell = valid_input()
    sell["positionDirection"] = "SELL"
    sell["executionPrice"] = "1.10010"
    cases.append(("R8_PRICE_SELL_ASK", execute_scenario(sell)["status"] == "PASS"))
    unknown = valid_input()
    unknown["pricePolicy"]["policyId"] = "UNKNOWN"
    unknown_result = execute_scenario(unknown)
    cases.append(("R8_PRICE_POLICY_AUTHORITY", unknown_result["status"] == "REJECT" and unknown_result["reason"] == "PRICE_POLICY_AUTHORITY_UNKNOWN"))
    source = valid_input()
    source["pricePolicy"]["normativeSourceId"] = "FOREIGN"
    source_result = execute_scenario(source)
    cases.append(("R8_PRICE_SOURCE_AUTHORITY", source_result["status"] == "REJECT" and source_result["reason"] == "PRICE_POLICY_AUTHORITY_MISMATCH"))
    broker = valid_input()
    broker["pricePolicy"]["tickSize"] = "0.1"
    broker_result = execute_scenario(broker)
    cases.append(("R8_PRICE_BROKER_PROPERTIES", broker_result["status"] == "REJECT" and broker_result["reason"] == "PRICE_POLICY_BROKER_PROPERTY_MISMATCH"))
    for check_id, passed in cases:
        print(f"{check_id}|{'PASS' if passed else 'FAIL'}")
    result = all(passed for _, passed in cases)
    print(f"PRICE_DEVIATION_AUTHORITY={'PASS' if result else 'FAIL'}")
    print(f"RESULT={'PASS' if result else 'FAIL'}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    raise SystemExit(0 if run(args.root) else 1)
