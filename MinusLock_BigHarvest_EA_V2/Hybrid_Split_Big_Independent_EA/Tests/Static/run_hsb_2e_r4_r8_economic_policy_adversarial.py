#!/usr/bin/env python3
"""Adversarial economic formula authority and broker-grid checks."""
from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path


def valid_input() -> dict:
    context = {"volumeStep": "0.01", "volumeMin": "0.01", "volumeMax": "10", "tickSize": "0.00001"}
    policy = {
        "scenario": "INITIAL",
        "formulaIds": ["INITIAL_NET_ACTUAL"],
        "normativeSourceIds": ["HSBI-ECON-INITIAL-R8"],
        "units": "ACCOUNT_CURRENCY_AND_LOTS",
        "roundingMode": "ROUND_DOWN",
        **context,
    }
    return {"schemaVersion": 8, "operation": "VALIDATE_ECONOMIC_POLICY", "context": context, "economicPolicy": policy}


def run(root: str) -> bool:
    project = Path(root).resolve()
    sys.path.insert(0, str(project / "Tests/Reference"))
    from hsb_2e_reference_model_r4_r8 import execute_scenario

    cases = []
    cases.append(("R8_ECONOMIC_VALID", execute_scenario(valid_input())["status"] == "PASS"))
    empty_formula = valid_input()
    empty_formula["economicPolicy"]["formulaIds"] = []
    cases.append(("R8_ECONOMIC_FORMULA_AUTHORITY", execute_scenario(empty_formula)["reason"] == "ECONOMIC_FORMULA_REGISTRY_EMPTY"))
    empty_source = valid_input()
    empty_source["economicPolicy"]["normativeSourceIds"] = []
    cases.append(("R8_ECONOMIC_SOURCE_AUTHORITY", execute_scenario(empty_source)["reason"] == "ECONOMIC_NORMATIVE_SOURCE_REGISTRY_EMPTY"))
    grid = valid_input()
    grid["economicPolicy"]["volumeStep"] = "0.02"
    cases.append(("R8_ECONOMIC_BROKER_GRID", execute_scenario(grid)["reason"] == "ECONOMIC_BROKER_GRID_MISMATCH"))
    duplicate = valid_input()
    duplicate["economicPolicy"]["formulaIds"] = ["INITIAL_NET_ACTUAL", "INITIAL_NET_ACTUAL"]
    cases.append(("R8_ECONOMIC_DUPLICATE_FORMULA", execute_scenario(duplicate)["reason"] == "ECONOMIC_FORMULA_DUPLICATE"))
    for check_id, passed in cases:
        print(f"{check_id}|{'PASS' if passed else 'FAIL'}")
    result = all(passed for _, passed in cases)
    print(f"ECONOMIC_FORMULA_AUTHORITY={'PASS' if result else 'FAIL'}")
    print(f"ECONOMIC_NORMATIVE_SOURCE_AUTHORITY={'PASS' if result else 'FAIL'}")
    print(f"ECONOMIC_BROKER_GRID_BINDING={'PASS' if result else 'FAIL'}")
    print(f"RESULT={'PASS' if result else 'FAIL'}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    raise SystemExit(0 if run(args.root) else 1)
