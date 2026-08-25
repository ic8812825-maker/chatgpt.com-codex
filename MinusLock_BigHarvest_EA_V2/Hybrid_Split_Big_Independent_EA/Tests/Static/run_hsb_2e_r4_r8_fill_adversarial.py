#!/usr/bin/env python3
"""Independent fill classification and overfill reconciliation checks."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def run(root: str) -> bool:
    project = Path(root).resolve()
    sys.path.insert(0, str(project / "Tests/Reference"))
    from hsb_2e_reference_model_r4_r8 import execute_scenario

    expected = {
        "0": "NO_FILL",
        "0.5": "PARTIAL_FILL",
        "1": "FULL_FILL",
        "1.1": "OVERFILL",
        "-1": "INVALID_FILL",
    }
    checks = []
    for confirmed, classification in expected.items():
        result = execute_scenario(
            {
                "schemaVersion": 8,
                "operation": "CLASSIFY_FILL",
                "requestedVolume": "1",
                "confirmedVolume": confirmed,
            }
        )
        passed = result["fillClassification"] == classification
        if classification == "OVERFILL":
            passed = passed and result["status"] == "REJECT"
            passed = passed and result["phase"] == "RECONCILIATION_REQUIRED"
            passed = passed and result["reason"] == "OVERFILL"
            passed = passed and result["stateRevisionDelta"] == 0
            passed = passed and result["settlementRevisionDelta"] == 0
        checks.append((f"R8_FILL_{classification}", passed))
    for check_id, passed in checks:
        print(f"{check_id}|{'PASS' if passed else 'FAIL'}")
    result = all(passed for _, passed in checks)
    print(f"OVERFILL_CLASSIFICATION={'PASS' if result else 'FAIL'}")
    print(f"OVERFILL_RECONCILIATION={'PASS' if result else 'FAIL'}")
    print(f"RESULT={'PASS' if result else 'FAIL'}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    raise SystemExit(0 if run(args.root) else 1)
