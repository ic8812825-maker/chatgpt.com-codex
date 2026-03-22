#!/usr/bin/env python3
"""Unified entrypoint for structure-agnostic ALE audit run.
Usage: python run_full_audit.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEST_RUNNER = ROOT / "Experts/VirtualPanel/right/tests/run_unit_tests.py"
LYAPUNOV_RUNNER = ROOT / "Experts/VirtualPanel/right/run_lyapunov_audit.py"

REQUIRED_REPORTS = [
    "Experts/VirtualPanel/right/ale/ALE_SYSTEM_MAP.md",
    "Experts/VirtualPanel/right/ale/ALE_FUNCTION_AUDIT.md",
    "Experts/VirtualPanel/right/ale/ALE_GEOMETRY_REPORT.md",
    "Experts/VirtualPanel/right/ale/ALE_LYAPUNOV_REPORT.md",
    "Experts/VirtualPanel/right/ale/ALE_SYSTEM_STRESS_REPORT.md",
    "Experts/VirtualPanel/right/ale/ALE_CONTROL_AUDIT.md",
    "Experts/VirtualPanel/right/ale/ALE_FINAL_VERDICT.md",
    "Experts/VirtualPanel/right/ale/ALE_LYAPUNOV_PROOF.md",
    "Experts/VirtualPanel/right/ale/ALE_CONTROL_LATENCY_REPORT.md",
    "Experts/VirtualPanel/right/ale/ALE_TAIL_EFFECTIVENESS_REPORT.md",
    "Experts/VirtualPanel/right/ale/ALE_STABILITY_REPORT.md",
    "Experts/VirtualPanel/right/ale/ALE_RISK_CONTROL_FINAL.md",
    "Experts/VirtualPanel/right/ale/ALE_FINAL_TRUTH.md",
    "Experts/VirtualPanel/right/ale/ALE_CONTROL_LYAPUNOV_AUDIT.md",
]


def run_cmd(cmd: list[str]) -> int:
    print("$", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(ROOT))


def main() -> int:
    if not TEST_RUNNER.exists():
        print(f"ERROR: missing test runner: {TEST_RUNNER}")
        return 2

    code = run_cmd([sys.executable, str(TEST_RUNNER)])
    if code != 0:
        print("Audit test runner failed.")
        return code

    if LYAPUNOV_RUNNER.exists():
        code = run_cmd([sys.executable, str(LYAPUNOV_RUNNER)])
        if code != 0:
            print("Lyapunov audit runner failed.")
            return code

    missing = [p for p in REQUIRED_REPORTS if not (ROOT / p).exists()]
    if missing:
        print("Missing required reports:")
        for p in missing:
            print(" -", p)
        return 3

    print("Audit completed. Required reports present.")
    for p in REQUIRED_REPORTS:
        print(" -", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
