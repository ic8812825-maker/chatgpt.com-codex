#!/usr/bin/env python3
"""Verify immutable R4-R7 artifacts against the published baseline."""
from __future__ import annotations
import argparse, hashlib, subprocess
from pathlib import Path
BASELINE = "b983d0e2b6cdbb82d54c157ba87873a764c055c2"
PREFIX = "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/"
FILES = (
    "Tests/Reference/hsb_2e_reference_model_r4_r7.py",
    "Tests/Reference/hsb_2e_invariants_r4_r7.py",
    "Tests/Static/run_hsb_2e_r4_r7_cross_version.py",
    "Tests/Static/run_hsb_2e_r4_r7_semantic_mutations.py",
    "Tests/Static/verify_hsb_2e_prep_r4_r7.py",
    "Tests/Evidence/HSB_2E_PREP_R4_R7_MANIFEST.json",
    "Tests/Evidence/HSB_2E_PREP_R4_R7_EVIDENCE_SEAL_SHA256.txt",
)
def run(root: str) -> bool:
    project = Path(root).resolve()
    checks = []
    for relative in FILES:
        expected = subprocess.check_output(["git", "show", f"{BASELINE}:{PREFIX}{relative}"], cwd=project)
        actual = (project / relative).read_bytes()
        unchanged = hashlib.sha256(expected).digest() == hashlib.sha256(actual).digest()
        checks.append(unchanged)
        print(f"R7_PROTECTED|{relative}|{'UNCHANGED' if unchanged else 'CHANGED'}")
    result = all(checks)
    print("R7_CANONICAL_STATUS_MISMATCH=EXPECTED_AFTER_R4_R8")
    print(f"RESULT={'PASS' if result else 'FAIL'}")
    return result
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    raise SystemExit(0 if run(args.root) else 1)
