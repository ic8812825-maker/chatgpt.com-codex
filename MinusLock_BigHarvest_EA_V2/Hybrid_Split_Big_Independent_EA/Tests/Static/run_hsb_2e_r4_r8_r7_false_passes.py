#!/usr/bin/env python3
"""Reproduce the thirteen independently reported R4-R7 false passes."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any


def _sha(value: Any, canon: Any) -> str:
    encoded = json.dumps(canon(value), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def _reseal_state(state: dict[str, Any], model: Any, digest: Any) -> None:
    certificate = state["commitCertificate"]
    state["committedOutputDigest"] = model.output_digest(state)
    certificate = replace(
        certificate,
        outputStateDigest=state["committedOutputDigest"],
        certificateDigest="",
    )
    state["commitCertificate"] = replace(
        certificate,
        certificateDigest=digest(certificate.body()),
    )


def run(root: str, write: bool = False) -> bool:
    project = Path(root).resolve()
    sys.path.insert(0, str(project / "Tests/Reference"))
    import hsb_2e_reference_model_r4_r7 as model
    from hsb_2e_provenance_model_r4_r7 import canon, digest
    from hsb_2e_test_fixtures_r4_r7 import broker_fixture

    cross_source = (project / "Tests/Static/run_hsb_2e_r4_r7_cross_version.py").read_text()
    mutation_source = (project / "Tests/Static/run_hsb_2e_r4_r7_semantic_mutations.py").read_text()
    invariant_source = (project / "Tests/Reference/hsb_2e_invariants_r4_r7.py").read_text()
    static_cases: list[tuple[str, dict[str, Any], bool, str, str]] = [
        (
            "FP-R8-001",
            {"source": cross_source},
            "hsb_2e_historical_model_r4_r7" in cross_source,
            "PASS",
            "STUB_HISTORICAL_TARGET",
        ),
        (
            "FP-R8-002",
            {"source": cross_source},
            "expected={'version'" in cross_source and "actual[f]" in cross_source,
            "PASS",
            "CIRCULAR_ORACLE",
        ),
        (
            "FP-R8-003",
            {"source": mutation_source},
            "NAMES=[" in mutation_source and "n%len(BASE)" in mutation_source,
            "PASS",
            "SIX_TRANSFORMS_REUSED",
        ),
        (
            "FP-R8-004",
            {"source": mutation_source},
            "target,old,new,check,probe=BASE[n%len(BASE)]" in mutation_source,
            "PASS",
            "MUTATION_CLASS_TARGET_MISMATCH",
        ),
        (
            "FP-R8-005",
            {"source": invariant_source},
            "checks={k:ok for k in CHECK_IDS}" in invariant_source,
            "PASS",
            "SHARED_BOOLEAN_INVARIANTS",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for case_id, exact_input, reproduced, status, reason in static_cases:
        rows.append(
            {
                "caseId": case_id,
                "exactInput": exact_input,
                "exactInputSHA256": _sha(exact_input, canon),
                "historicalStatus": status if reproduced else "FAIL",
                "historicalReason": reason,
                "falsePassReproduced": reproduced,
            }
        )

    price = broker_fixture("INITIAL")
    object.__setattr__(price["pricePolicy"], "deviationTicks", 10_000_000_000)
    object.__setattr__(price["pricePolicy"], "policyDigest", digest(price["pricePolicy"].body()))
    object.__setattr__(price["dealRecords"][0], "price", model.D("99999.00000"))
    object.__setattr__(price["dealRecords"][0], "recordDigest", digest(price["dealRecords"][0].body()))

    committed_input = broker_fixture("INITIAL")
    committed = model.execute_scenario(committed_input)["state"]

    bad_version = copy.deepcopy(committed)
    certificate = replace(bad_version["commitCertificate"], certificateVersion=999, certificateDigest="")
    bad_version["commitCertificate"] = replace(certificate, certificateDigest=digest(certificate.body()))

    bad_state_revision = copy.deepcopy(committed)
    bad_state_revision["stateRevision"] = 999
    _reseal_state(bad_state_revision, model, digest)

    bad_settlement_revision = copy.deepcopy(committed)
    bad_settlement_revision["settlementRevision"] = 999
    _reseal_state(bad_settlement_revision, model, digest)

    replay_inputs: list[tuple[str, dict[str, Any], dict[str, Any], str, str]] = []
    for case_id, state in (
        ("FP-R8-007", bad_version),
        ("FP-R8-008", bad_state_revision),
        ("FP-R8-009", bad_settlement_revision),
    ):
        replay = broker_fixture("INITIAL")
        replay["persistedState"] = state
        replay["context"]["stateRevision"] = state["stateRevision"]
        replay_inputs.append((case_id, replay, model.execute_scenario(replay), "PASS", "ALREADY_COMMITTED"))

    overfill = broker_fixture("INITIAL")
    object.__setattr__(overfill["dealRecords"][0], "volume", model.D("1.10"))
    object.__setattr__(overfill["dealRecords"][0], "recordDigest", digest(overfill["dealRecords"][0].body()))

    empty_formula = broker_fixture("INITIAL")
    object.__setattr__(empty_formula["economicPolicy"], "formulaIds", ())
    object.__setattr__(empty_formula["economicPolicy"], "policyDigest", digest(empty_formula["economicPolicy"].body()))

    empty_sources = broker_fixture("INITIAL")
    object.__setattr__(empty_sources["economicPolicy"], "normativeSourceIds", ())
    object.__setattr__(empty_sources["economicPolicy"], "policyDigest", digest(empty_sources["economicPolicy"].body()))

    bad_grid = broker_fixture("INITIAL")
    object.__setattr__(bad_grid["economicPolicy"], "volumeStep", model.D("0.02"))
    object.__setattr__(bad_grid["economicPolicy"], "policyDigest", digest(bad_grid["economicPolicy"].body()))

    dynamic_inputs = [
        ("FP-R8-006", price, model.execute_scenario(price), "PASS", "OK"),
        *replay_inputs,
        ("FP-R8-010", overfill, model.execute_scenario(overfill), "UNAVAILABLE", "COMMIT_FULL_FILL_UNPROVEN"),
        ("FP-R8-011", empty_formula, model.execute_scenario(empty_formula), "PASS", "OK"),
        ("FP-R8-012", empty_sources, model.execute_scenario(empty_sources), "PASS", "OK"),
        ("FP-R8-013", bad_grid, model.execute_scenario(bad_grid), "PASS", "OK"),
    ]
    for case_id, exact_input, actual, status, reason in dynamic_inputs:
        reproduced = actual["status"] == status and actual["reason"] == reason
        rows.append(
            {
                "caseId": case_id,
                "exactInput": canon(exact_input),
                "exactInputSHA256": _sha(exact_input, canon),
                "historicalStatus": actual["status"],
                "historicalReason": actual["reason"],
                "falsePassReproduced": reproduced,
            }
        )
    reproduced_count = sum(row["falsePassReproduced"] for row in rows)
    result = {
        "schemaVersion": 1,
        "R7_FALSE_PASSES_REQUIRED": 13,
        "R7_FALSE_PASSES_REPRODUCED": reproduced_count,
        "cases": rows,
        "RESULT": "PASS" if reproduced_count == 13 else "FAIL",
    }
    if write:
        vector_path = project / "Tests/Vectors/HSB_2E_R4_R8_R7_FALSE_PASSES.json"
        evidence_path = project / "Tests/Evidence/HSB_2E_PREP_R4_R8_R7_FALSE_PASS_REPRODUCTION.json"
        vector_path.write_text(json.dumps({"schemaVersion": 1, "cases": rows}, indent=2, sort_keys=True) + "\n")
        evidence_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    printable = {key: value for key, value in result.items() if key != "cases"}
    print(json.dumps(printable, sort_keys=True, separators=(",", ":")))
    return result["RESULT"] == "PASS"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--write", action="store_true")
    arguments = parser.parse_args()
    raise SystemExit(0 if run(arguments.root, arguments.write) else 1)
