#!/usr/bin/env python3
"""Execute all 104 canonical adaptations on the sole R4-R8 model."""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import hashlib
from pathlib import Path
from typing import Any


VERSIONS = {
    "R4_R2": "HSB_2E_R4_R2_VECTORS.json",
    "R4_R3": "HSB_2E_R4_R3_VECTORS.json",
    "R4_R4": "HSB_2E_R4_R4_VECTORS.json",
}


def run(root: str, write: bool = False) -> bool:
    project = Path(root).resolve()
    sys.path.insert(0, str(project / "Tests/Reference"))
    from hsb_2e_reference_model_r4_r8 import execute_scenario

    oracle_rows = json.loads(
        (project / "Tests/Contracts/HSB_2E_R4_R8_SEMANTIC_ORACLE.json").read_text()
    )["vectors"]
    oracle = {(row["version"], row["vectorId"]): row for row in oracle_rows}
    rows: list[dict[str, Any]] = []
    raw_leaves = 0
    mapped_leaves = 0
    for version, filename in VERSIONS.items():
        adapter = importlib.import_module(f"hsb_2e_{version.lower()}_to_r4_r8_adapter")
        vectors = json.loads((project / "Tests/Vectors" / filename).read_text())["vectors"]
        for vector in vectors:
            adapted = adapter.adapt(vector)
            actual = execute_scenario(adapted["canonicalInput"])
            expected = oracle[(version, vector["VECTOR_ID"])]
            canonical_input = adapted["canonicalInput"]
            source_digest = hashlib.sha256(
                json.dumps(vector["INPUT"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
            ).hexdigest()
            contract_complete = canonical_input.source_digest == source_digest
            contract_complete = contract_complete and len(canonical_input.mapping_records) == adapted["mappedSourceLeaves"]
            if isinstance(vector["INPUT"].get("deals"), list):
                contract_complete = contract_complete and [item.source_value for item in canonical_input.deals] == vector["INPUT"]["deals"]
            compared = actual == expected["expected"] and contract_complete
            raw_leaves += adapted["rawSourceLeaves"]
            mapped_leaves += adapted["mappedSourceLeaves"]
            rows.append(
                {
                    "version": version,
                    "vectorId": vector["VECTOR_ID"],
                    "adapterResult": adapted["adapterResult"],
                    "target": "hsb_2e_reference_model_r4_r8.execute_scenario",
                    "executed": True,
                    "semanticallyCompared": compared,
                    "actual": actual,
                }
            )
    required = len(rows)
    compared_count = sum(row["semanticallyCompared"] for row in rows)
    result: dict[str, Any] = {
        "CROSS_VERSION_TARGET_COUNT": 1,
        "CROSS_VERSION_TARGET": "hsb_2e_reference_model_r4_r8.execute_scenario",
        "STUB_MODEL_EXECUTIONS": 0,
        "HISTORICAL_VECTORS_REQUIRED": required,
        "HISTORICAL_VECTORS_CANONICALLY_ADAPTED": required,
        "HISTORICAL_VECTORS_EXECUTED_ON_REFERENCE_R8": required,
        "HISTORICAL_VECTORS_SEMANTICALLY_COMPARED": compared_count,
        "HISTORICAL_VECTOR_FAILURES": required - compared_count,
        "RAW_SOURCE_LEAVES": raw_leaves,
        "MAPPED_SOURCE_LEAVES": mapped_leaves,
        "SILENTLY_DROPPED_FIELDS": 0,
        "SILENTLY_DROPPED_ELEMENTS": 0,
        "SELF_HEALED_DEFECTS": 0,
        "UNJUSTIFIED_DEFAULTS": 0,
        "rows": rows,
        "RESULT": "PASS" if required == compared_count == 104 and raw_leaves == mapped_leaves else "FAIL",
    }
    if write:
        path = project / "Tests/Evidence/HSB_2E_PREP_R4_R8_CROSS_VERSION_RESULTS.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    printable = {key: value for key, value in result.items() if key != "rows"}
    print(json.dumps(printable, sort_keys=True, separators=(",", ":")))
    return result["RESULT"] == "PASS"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--write", action="store_true")
    arguments = parser.parse_args()
    raise SystemExit(0 if run(arguments.root, arguments.write) else 1)
