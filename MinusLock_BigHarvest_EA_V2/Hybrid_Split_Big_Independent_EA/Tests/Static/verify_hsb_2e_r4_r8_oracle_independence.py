#!/usr/bin/env python3
"""Verify phase-A oracle ancestry and absence of test-target dependencies."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ORACLE_COMMIT_SUBJECT = "HSB.2E-PREP-R4-R8: зафиксирован независимый нормативный oracle"
FORBIDDEN = (
    "hsb_2e_reference_model_r4_r8",
    "execute_scenario",
    "execute_historical",
    "expected = actual",
    "expectedStatus = result",
)


def run(root: str) -> bool:
    project = Path(root).resolve()
    builder = (project / "Tests/Static/build_hsb_2e_r4_r8_oracle.py").read_text()
    oracle_path = project / "Tests/Contracts/HSB_2E_R4_R8_SEMANTIC_ORACLE.json"
    provenance_path = project / "Tests/Evidence/HSB_2E_PREP_R4_R8_ORACLE_PROVENANCE.json"
    history = subprocess.check_output(
        ["git", "log", "--format=%H%x00%s", "--", str(oracle_path.relative_to(project))],
        cwd=project,
        text=True,
    ).splitlines()
    oracle_commits = [line for line in history if line.endswith("\x00" + ORACLE_COMMIT_SUBJECT)]
    oracle = json.loads(oracle_path.read_text())
    provenance = json.loads(provenance_path.read_text())
    checks = {
        "R8_ORACLE_SINGLE_PREIMPLEMENTATION_COMMIT": len(oracle_commits) == 1,
        "R8_ORACLE_NO_MODEL_IMPORT": not any(token in builder for token in FORBIDDEN),
        "R8_ORACLE_ROWS": len(oracle.get("vectors", [])) == 104,
        "R8_ORACLE_PROVENANCE": len(provenance.get("entries", [])) == 104 * 33,
    }
    for check_id, passed in checks.items():
        print(f"{check_id}|{'PASS' if passed else 'FAIL'}")
    print(f"ORACLE_SHA256={hashlib.sha256(oracle_path.read_bytes()).hexdigest()}")
    print(f"CIRCULAR_ORACLE_DEPENDENCIES={0 if checks['R8_ORACLE_NO_MODEL_IMPORT'] else 1}")
    result = all(checks.values())
    print(f"RESULT={'PASS' if result else 'FAIL'}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    arguments = parser.parse_args()
    raise SystemExit(0 if run(arguments.root) else 1)
