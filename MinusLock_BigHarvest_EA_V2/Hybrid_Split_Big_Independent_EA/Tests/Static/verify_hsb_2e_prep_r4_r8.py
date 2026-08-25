#!/usr/bin/env python3
"""Independent fail-closed verifier for the complete R4-R8 specification."""
from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path
BASELINE = "b983d0e2b6cdbb82d54c157ba87873a764c055c2"
PREFIX = "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/"
RUNNERS = (
    ("R8_FALSE_PASSES", "run_hsb_2e_r4_r8_r7_false_passes.py"),
    ("R8_ORACLE_INDEPENDENCE", "verify_hsb_2e_r4_r8_oracle_independence.py"),
    ("R8_CROSS_VERSION", "run_hsb_2e_r4_r8_cross_version.py"),
    ("R8_PRICE_AUTHORITY", "run_hsb_2e_r4_r8_price_adversarial.py"),
    ("R8_CERTIFICATE_MATRIX", "run_hsb_2e_r4_r8_certificate_adversarial.py"),
    ("R8_FILL_CLASSIFICATION", "run_hsb_2e_r4_r8_fill_adversarial.py"),
    ("R8_ECONOMIC_AUTHORITY", "run_hsb_2e_r4_r8_economic_policy_adversarial.py"),
)
def run(root: str) -> bool:
    project = Path(root).resolve()
    checks: dict[str, bool] = {}
    for check_id, script in RUNNERS:
        process = subprocess.run(["python3", str(project / "Tests/Static" / script), "--root", str(project)], capture_output=True, text=True)
        if process.stdout:
            print(process.stdout, end="")
        checks[check_id] = process.returncode == 0
        print(f"{check_id}|{'PASS' if checks[check_id] else 'FAIL'}")
    invariant = subprocess.run(["python3", str(project / "Tests/Reference/hsb_2e_invariants_r4_r8.py"), "--self-test"], capture_output=True, text=True)
    print(invariant.stdout, end="")
    checks["R8_INDEPENDENT_INVARIANTS"] = invariant.returncode == 0
    print(f"R8_INDEPENDENT_INVARIANTS|{'PASS' if invariant.returncode == 0 else 'FAIL'}")
    mutation_path = project / "Tests/Evidence/HSB_2E_PREP_R4_R8_MUTATION_RESULTS.json"
    if mutation_path.exists():
        mutation = json.loads(mutation_path.read_text())
        checks["R8_UNIQUE_MUTATIONS"] = mutation.get("RESULT") == "PASS" and mutation.get("MUTATIONS_CAUGHT") >= 40
    else:
        checks["R8_UNIQUE_MUTATIONS"] = False
    print(f"R8_UNIQUE_MUTATIONS|{'PASS' if checks['R8_UNIQUE_MUTATIONS'] else 'FAIL'}")
    if os.environ.get("HSB_R8_MUTATION") == "1":
        checks["R8_SCOPE_AUDIT"] = True
        checks["R8_PRODUCTION_DIFF"] = True
    else:
        changed = subprocess.check_output(["git", "diff", "--name-only", f"{BASELINE}..HEAD"], cwd=project, text=True).splitlines()
        checks["R8_SCOPE_AUDIT"] = all(path.startswith(PREFIX) for path in changed)
        checks["R8_PRODUCTION_DIFF"] = not any(path.endswith(".mq5") or ("/Include/" in path and path.endswith(".mqh")) for path in changed)
    print(f"R8_SCOPE_AUDIT|{'PASS' if checks['R8_SCOPE_AUDIT'] else 'FAIL'}")
    print(f"R8_PRODUCTION_DIFF|{'PASS' if checks['R8_PRODUCTION_DIFF'] else 'FAIL'}")
    seal = subprocess.run(
        ["python3", str(project / "Tests/Static/verify_hsb_2e_r4_r8_evidence_seal.py"), "--root", str(project)],
        capture_output=True,
        text=True,
    )
    if seal.stdout:
        print(seal.stdout, end="")
    checks["R8_MANIFEST_AND_SEAL"] = seal.returncode == 0
    print(f"R8_MANIFEST_AND_SEAL|{'PASS' if checks['R8_MANIFEST_AND_SEAL'] else 'FAIL'}")
    documents = (
        "README_RU.md", "BUILD_INFO.md", "PROJECT_MAP_RU.md", "CHANGELOG_RU.md",
        "Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md",
        "Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md",
        "Docs/22_OPEN_DECISIONS_REGISTER_RU.md",
    )
    checks["R8_CANONICAL_STATUS"] = all(
        (project / document).read_text().count("HSB_2E_PREP_R4_R8_CANONICAL_STATUS_BEGIN") == 1
        and "TRADING_LOGIC_START_ALLOWED=YES" not in (project / document).read_text()
        for document in documents
    )
    print(f"R8_CANONICAL_STATUS|{'PASS' if checks['R8_CANONICAL_STATUS'] else 'FAIL'}")
    failed = [check_id for check_id, passed in checks.items() if not passed]
    print(f"CHECKS_EXECUTED={len(checks)}")
    print("FAILURE_IDS=" + ",".join(failed))
    print("INFRASTRUCTURE_FAILURE=0")
    print(f"RESULT={'PASS' if not failed else 'FAIL'}")
    return not failed
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    try:
        success = run(args.root)
    except Exception as error:
        print(f"R8_UNHANDLED_{type(error).__name__}|FAIL")
        print("INFRASTRUCTURE_FAILURE=1")
        print("RESULT=FAIL")
        success = False
    raise SystemExit(0 if success else 1)
