#!/usr/bin/env python3
"""Fourteen independent certificate/source/revision adversarial cases."""
from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path
from typing import Callable


def run(root: str) -> bool:
    project = Path(root).resolve()
    sys.path.insert(0, str(project / "Tests/Reference"))
    from hsb_2e_reference_model_r4_r8 import execute_scenario
    from hsb_2e_validation_r4_r8 import build_valid_commit, digest, output_state_digest

    def reseal(case: dict) -> None:
        certificate = case["certificate"]
        certificate["certificateDigest"] = digest(
            {key: value for key, value in certificate.items() if key != "certificateDigest"}
        )

    def object_case(name: str) -> dict:
        case = build_valid_commit()
        case["commitBundle"][name]["body"]["value"] = 999
        case["commitBundle"][name]["digest"] = digest(case["commitBundle"][name]["body"])
        case["certificate"][f"{name}Digest"] = case["commitBundle"][name]["digest"]
        reseal(case)
        return case

    cases: list[tuple[str, dict, str]] = []
    output_digest = build_valid_commit()
    output_digest["persistedState"]["outputStateDigest"] = "f" * 64
    cases.append(("R8_CERT_OUTPUT_STATE", output_digest, "COMMIT_OUTPUT_STATE_RECOMPUTATION_MISMATCH"))
    for name in ("broker", "economic", "allocation", "persistence", "fsm"):
        cases.append(
            (
                f"R8_CERT_{name.upper()}",
                object_case(name),
                f"COMMIT_{name.upper()}_RECOMPUTATION_MISMATCH",
            )
        )
    version = build_valid_commit()
    version["certificate"]["certificateVersion"] = 999
    reseal(version)
    cases.append(("R8_CERT_VERSION", version, "COMMIT_CERTIFICATE_VERSION_UNSUPPORTED"))
    state_revision = build_valid_commit()
    state_revision["persistedState"]["stateRevision"] = 999
    state_revision["persistedState"]["outputStateDigest"] = output_state_digest(state_revision["persistedState"])
    state_revision["certificate"]["outputStateDigest"] = state_revision["persistedState"]["outputStateDigest"]
    reseal(state_revision)
    cases.append(("R8_CERT_STATE_REVISION", state_revision, "COMMIT_STATE_REVISION_MISMATCH"))
    settlement = build_valid_commit()
    settlement["persistedState"]["settlementRevision"] = 999
    settlement["persistedState"]["outputStateDigest"] = output_state_digest(settlement["persistedState"])
    settlement["certificate"]["outputStateDigest"] = settlement["persistedState"]["outputStateDigest"]
    reseal(settlement)
    cases.append(("R8_CERT_SETTLEMENT_REVISION", settlement, "COMMIT_SETTLEMENT_REVISION_MISMATCH"))
    evidence = build_valid_commit()
    evidence["persistedState"]["evidenceRevision"] = 999
    evidence["persistedState"]["outputStateDigest"] = output_state_digest(evidence["persistedState"])
    evidence["certificate"]["outputStateDigest"] = evidence["persistedState"]["outputStateDigest"]
    reseal(evidence)
    cases.append(("R8_CERT_EVIDENCE_REVISION", evidence, "COMMIT_EVIDENCE_REVISION_MISMATCH"))
    relation = build_valid_commit()
    relation["certificate"]["outputRevision"] = 5
    reseal(relation)
    cases.append(("R8_CERT_REVISION_RELATION", relation, "COMMIT_STATE_REVISION_DELTA_INVALID"))
    missing = build_valid_commit()
    del missing["commitBundle"]["economic"]
    cases.append(("R8_CERT_MISSING_SOURCE", missing, "COMMIT_SOURCE_OBJECT_MISSING"))
    extra = build_valid_commit()
    extra["commitBundle"]["unknown"] = {"body": {}, "digest": digest({})}
    cases.append(("R8_CERT_EXTRA_SOURCE", extra, "COMMIT_SOURCE_OBJECT_UNKNOWN"))
    mutually_altered = object_case("economic")
    cases.append(("R8_CERT_MUTUALLY_ALTERED", mutually_altered, "COMMIT_ECONOMIC_RECOMPUTATION_MISMATCH"))

    checks = []
    for check_id, case, expected_reason in cases:
        actual = execute_scenario(case)
        passed = actual["status"] == "REJECT" and actual["reason"] == expected_reason
        checks.append((check_id, passed, expected_reason, actual["reason"]))
    valid = execute_scenario(build_valid_commit())
    checks.append(("R8_CERT_VALID_REPLAY", valid["reason"] == "ALREADY_COMMITTED", "ALREADY_COMMITTED", valid["reason"]))
    for check_id, passed, expected_reason, actual_reason in checks:
        print(f"{check_id}|{'PASS' if passed else 'FAIL'}|EXPECTED={expected_reason}|ACTUAL={actual_reason}")
    result = all(passed for _, passed, _, _ in checks)
    print(f"CERTIFICATE_VERSION_VALIDATION={'PASS' if result else 'FAIL'}")
    print(f"STATE_REVISION_CERTIFICATE_BINDING={'PASS' if result else 'FAIL'}")
    print(f"SETTLEMENT_REVISION_BINDING={'PASS' if result else 'FAIL'}")
    print(f"EVIDENCE_REVISION_BINDING={'PASS' if result else 'FAIL'}")
    print(f"RESULT={'PASS' if result else 'FAIL'}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    raise SystemExit(0 if run(args.root) else 1)
