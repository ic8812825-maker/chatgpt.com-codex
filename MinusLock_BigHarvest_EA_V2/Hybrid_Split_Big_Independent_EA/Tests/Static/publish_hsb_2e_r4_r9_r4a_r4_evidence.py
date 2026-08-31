#!/usr/bin/env python3
"""Publish detailed immutable/protection and scope evidence for the R4A-R4 checkpoint."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

import verify_hsb_2e_r4_r9_r4a_r4_schema as verifier

BASELINE = "f44b7e5cae314fced0f8d519e1e5d70f3c49c35d"


def git(*args: str) -> str:
    return subprocess.run(("git", *args), cwd=verifier.ROOT, check=True, text=True,
                          stdout=subprocess.PIPE).stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    verifier.EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    registry_path = verifier.ROOT / "Tests/Contracts/HSB_2E_R4_R9_R4A_R1_PROTECTED_ARTIFACTS.json"
    protected_registry = json.loads(registry_path.read_text(encoding="utf-8"))
    rows, mismatches = [], 0
    for entry in protected_registry["files"]:
        if entry["protectionClass"] == "STATUS_DOCUMENT_EXCEPTION":
            continue
        path = verifier.ROOT / entry["path"]
        actual_blob = git("hash-object", str(path))
        actual_sha = sha256(path)
        actual_last = git("log", "-1", "--format=%H", "--", entry["path"])
        result = "PASS" if actual_blob == entry["gitBlobSha"] and actual_sha == entry["sha256"] else "FAIL"
        mismatches += result == "FAIL"
        rows.append({"path": entry["path"], "expectedGitBlobSha": entry["gitBlobSha"],
                     "actualGitBlobSha": actual_blob, "expectedSha256": entry["sha256"],
                     "actualSha256": actual_sha, "introducedCommit": entry["introducedCommit"],
                     "actualLastChangedCommit": actual_last, "protectionClass": entry["protectionClass"],
                     "result": result})
    changed = [line for line in git("diff", "--name-only", f"{BASELINE}..HEAD").splitlines() if line]
    prefix = "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/"
    external = [path for path in changed if not path.startswith(prefix)]
    production = [path for path in changed if path.endswith(".mq5") or "/Include/" in path and path.endswith(".mqh")]
    summary = {"baseline": BASELINE, "protectedFilesRequired": len(rows), "protectedFilesVerified": len(rows),
               "protectedFileMismatches": mismatches, "files": rows,
               "scope": {"changedPaths": changed, "scopeViolations": len(external), "externalPaths": external},
               "production": {"productionDiffPaths": production, "productionMql5LogicChanged": "NO" if not production else "YES"},
               "nativeModelChanged": "NO" if not any("hsb_2e_reference_model_r4_r9_r3.py" in p for p in changed) else "YES",
               "historicalOraclesChanged": "NO" if mismatches == 0 else "YES",
               "result": "PASS" if not mismatches and not external and not production else "FAIL"}
    (verifier.EVIDENCE_DIR / "protected_scope_production_audit.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result = verifier.execute()
    (verifier.EVIDENCE_DIR / "schema_positive_validation.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PROTECTED_FILES_REQUIRED={len(rows)}")
    print(f"PROTECTED_FILES_VERIFIED={len(rows)}")
    print(f"PROTECTED_FILE_MISMATCHES={mismatches}")
    print(f"SCOPE_VIOLATIONS={len(external)}")
    print(f"PRODUCTION_DIFF_PATHS={len(production)}")
    print(f"RESULT={summary['result']}")
    return 0 if summary["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
