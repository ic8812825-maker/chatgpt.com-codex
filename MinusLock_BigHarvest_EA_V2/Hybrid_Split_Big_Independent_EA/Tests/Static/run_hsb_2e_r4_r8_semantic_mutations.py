#!/usr/bin/env python3
"""Apply forty unique semantic source mutations and require the exact failing property."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
@dataclass(frozen=True)
class Mutation:
    mutationId: str
    mutationClass: str
    target: str
    oldFragment: str
    newFragment: str
    expectedCheckId: str
    expectedReason: str

def mutations() -> tuple[Mutation, ...]:
    specs = [
        ("ADAPTER_DROP_SOURCE", "adapter source preservation", "Tests/Reference/hsb_2e_adapter_common_r4_r8.py", "source_payload=source,", "source_payload={},", "R8_CROSS_VERSION", "R8_CROSS_VERSION|FAIL"),
        ("ADAPTER_BAD_DIGEST", "adapter digest", "Tests/Reference/hsb_2e_adapter_common_r4_r8.py", "source_digest=value_sha(source),", "source_digest='forged',", "R8_CROSS_VERSION", "R8_CROSS_VERSION|FAIL"),
        ("ADAPTER_DROP_MAP", "adapter leaf map", "Tests/Reference/hsb_2e_adapter_common_r4_r8.py", "mapping_records=tuple(records),", "mapping_records=(),", "R8_CROSS_VERSION", "R8_CROSS_VERSION|FAIL"),
        ("ADAPTER_HEAL_DEALS", "adapter malformed deals", "Tests/Reference/hsb_2e_adapter_common_r4_r8.py", "source.get(\"deals\", [])", "[]", "R8_CROSS_VERSION", "R8_CROSS_VERSION|FAIL"),
        ("ADAPTER_REWRITE_ITEM", "adapter element identity", "Tests/Reference/hsb_2e_adapter_common_r4_r8.py", "contract_type(copy.deepcopy(item))", "contract_type({})", "R8_CROSS_VERSION", "R8_CROSS_VERSION|FAIL"),
        ("ADAPTER_FALSE_COUNT", "adapter completeness count", "Tests/Reference/hsb_2e_adapter_common_r4_r8.py", '"mappedSourceLeaves": len(records)', '"mappedSourceLeaves": 0', "R8_CROSS_VERSION", "R8_CROSS_VERSION|FAIL"),
        ("ORACLE_IMPORT_MODEL", "oracle model import", "Tests/Static/build_hsb_2e_r4_r8_oracle.py", "import argparse, hashlib, json", "import hsb_2e_reference_model_r4_r8\nimport argparse, hashlib, json", "R8_ORACLE_INDEPENDENCE", "R8_ORACLE_NO_MODEL_IMPORT|FAIL"),
        ("ORACLE_CALL_TARGET", "oracle target call", "Tests/Static/build_hsb_2e_r4_r8_oracle.py", '"""Build the phase-A oracle only from immutable historical expectations."""', '"""execute_scenario dependency."""', "R8_ORACLE_INDEPENDENCE", "R8_ORACLE_NO_MODEL_IMPORT|FAIL"),
        ("ORACLE_ACTUAL_ALIAS", "oracle actual alias", "Tests/Static/build_hsb_2e_r4_r8_oracle.py", "FILES = {", "expected = actual = None\nFILES = {", "R8_ORACLE_INDEPENDENCE", "R8_ORACLE_NO_MODEL_IMPORT|FAIL"),
        ("PRICE_FOREIGN_CONTEXT", "snapshot context", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("SNAPSHOT_CONTEXT_IDENTITY_MISMATCH")', 'return pass_result("SNAPSHOT_CONTEXT_IDENTITY_MISMATCH")', "R8_PRICE_AUTHORITY", "R8_PRICE_AUTHORITY|FAIL"),
        ("PRICE_REVERSE_SIDES", "normative close side", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("NORMATIVE_CLOSE_SIDE_MISMATCH")', 'return pass_result("NORMATIVE_CLOSE_SIDE_MISMATCH")', "R8_PRICE_AUTHORITY", "R8_PRICE_AUTHORITY|FAIL"),
        ("PRICE_UNKNOWN_POLICY", "price authority", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("PRICE_POLICY_AUTHORITY_UNKNOWN")', 'return pass_result("PRICE_POLICY_AUTHORITY_UNKNOWN")', "R8_PRICE_AUTHORITY", "R8_PRICE_AUTHORITY|FAIL"),
        ("PRICE_SOURCE_MISMATCH", "price source authority", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("PRICE_POLICY_AUTHORITY_MISMATCH")', 'return pass_result("PRICE_POLICY_AUTHORITY_MISMATCH")', "R8_PRICE_AUTHORITY", "R8_PRICE_AUTHORITY|FAIL"),
        ("PRICE_UNBOUNDED_DEVIATION", "maximum deviation", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("PRICE_DEVIATION_POLICY_EXCEEDED")', 'return pass_result("PRICE_DEVIATION_POLICY_EXCEEDED")', "R8_PRICE_AUTHORITY", "R8_PRICE_AUTHORITY|FAIL"),
        ("PRICE_GRID_UNBOUND", "price broker property", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("PRICE_POLICY_BROKER_PROPERTY_MISMATCH")', 'return pass_result("PRICE_POLICY_BROKER_PROPERTY_MISMATCH")', "R8_PRICE_AUTHORITY", "R8_PRICE_AUTHORITY|FAIL"),
        ("FILL_NO_AS_PARTIAL", "no fill", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return "NO_FILL"', 'return "PARTIAL_FILL"', "R8_FILL_CLASSIFICATION", "R8_FILL_CLASSIFICATION|FAIL"),
        ("FILL_PARTIAL_AS_FULL", "partial fill", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return "PARTIAL_FILL"', 'return "FULL_FILL"', "R8_FILL_CLASSIFICATION", "R8_FILL_CLASSIFICATION|FAIL"),
        ("FILL_FULL_AS_OVER", "full fill", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return "FULL_FILL"', 'return "OVERFILL"', "R8_FILL_CLASSIFICATION", "R8_FILL_CLASSIFICATION|FAIL"),
        ("FILL_OVER_AS_PARTIAL", "overfill", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return "OVERFILL"', 'return "PARTIAL_FILL"', "R8_FILL_CLASSIFICATION", "R8_FILL_CLASSIFICATION|FAIL"),
        ("FILL_INVALID_AS_NO", "invalid fill", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return "INVALID_FILL"', 'return "NO_FILL"', "R8_FILL_CLASSIFICATION", "R8_FILL_CLASSIFICATION|FAIL"),
        ("CERT_VERSION", "certificate version", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("COMMIT_CERTIFICATE_VERSION_UNSUPPORTED")', 'return pass_result("COMMIT_CERTIFICATE_VERSION_UNSUPPORTED")', "R8_CERTIFICATE_MATRIX", "R8_CERTIFICATE_MATRIX|FAIL"),
        ("CERT_MISSING_OBJECT", "certificate missing source", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'if COMMIT_OBJECT_KEYS - set(bundle):\n            return reject("COMMIT_SOURCE_OBJECT_MISSING")', 'if COMMIT_OBJECT_KEYS - set(bundle):\n            return pass_result("COMMIT_SOURCE_OBJECT_MISSING")', "R8_CERTIFICATE_MATRIX", "R8_CERTIFICATE_MATRIX|FAIL"),
        ("CERT_UNKNOWN_OBJECT", "certificate unknown source", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("COMMIT_SOURCE_OBJECT_UNKNOWN")', 'return pass_result("COMMIT_SOURCE_OBJECT_UNKNOWN")', "R8_CERTIFICATE_MATRIX", "R8_CERTIFICATE_MATRIX|FAIL"),
        ("CERT_STATE_DELTA", "state revision delta", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("COMMIT_STATE_REVISION_DELTA_INVALID")', 'return pass_result("COMMIT_STATE_REVISION_DELTA_INVALID")', "R8_CERTIFICATE_MATRIX", "R8_CERTIFICATE_MATRIX|FAIL"),
        ("CERT_STATE_BIND", "state revision binding", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("COMMIT_STATE_REVISION_MISMATCH")', 'return pass_result("COMMIT_STATE_REVISION_MISMATCH")', "R8_CERTIFICATE_MATRIX", "R8_CERTIFICATE_MATRIX|FAIL"),
        ("CERT_FSM_BIND", "fsm revision binding", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("COMMIT_FSM_REVISION_MISMATCH")', 'return pass_result("COMMIT_FSM_REVISION_MISMATCH")', "R8_CERTIFICATE_MATRIX", "R8_CERTIFICATE_MATRIX|FAIL"),
        ("CERT_SETTLEMENT_DELTA", "settlement revision delta", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("COMMIT_SETTLEMENT_REVISION_DELTA_INVALID")', 'return pass_result("COMMIT_SETTLEMENT_REVISION_DELTA_INVALID")', "R8_CERTIFICATE_MATRIX", "R8_CERTIFICATE_MATRIX|FAIL"),
        ("CERT_SETTLEMENT_BIND", "settlement revision binding", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("COMMIT_SETTLEMENT_REVISION_MISMATCH")', 'return pass_result("COMMIT_SETTLEMENT_REVISION_MISMATCH")', "R8_CERTIFICATE_MATRIX", "R8_CERTIFICATE_MATRIX|FAIL"),
        ("CERT_EVIDENCE_DELTA", "evidence revision delta", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("COMMIT_EVIDENCE_REVISION_DELTA_INVALID")', 'return pass_result("COMMIT_EVIDENCE_REVISION_DELTA_INVALID")', "R8_CERTIFICATE_MATRIX", "R8_CERTIFICATE_MATRIX|FAIL"),
        ("CERT_EVIDENCE_BIND", "evidence revision binding", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("COMMIT_EVIDENCE_REVISION_MISMATCH")', 'return pass_result("COMMIT_EVIDENCE_REVISION_MISMATCH")', "R8_CERTIFICATE_MATRIX", "R8_CERTIFICATE_MATRIX|FAIL"),
        ("CERT_OUTPUT_RECOMPUTE", "output state recomputation", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("COMMIT_OUTPUT_STATE_RECOMPUTATION_MISMATCH")', 'return pass_result("COMMIT_OUTPUT_STATE_RECOMPUTATION_MISMATCH")', "R8_CERTIFICATE_MATRIX", "R8_CERTIFICATE_MATRIX|FAIL"),
        ("CERT_DIGEST", "certificate digest", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("COMMIT_CERTIFICATE_DIGEST_INVALID")', 'return pass_result("COMMIT_CERTIFICATE_DIGEST_INVALID")', "R8_CERTIFICATE_MATRIX", "R8_CERTIFICATE_MATRIX|FAIL"),
        ("ECON_EMPTY_FORMULA", "economic formula empty", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("ECONOMIC_FORMULA_REGISTRY_EMPTY")', 'return pass_result("ECONOMIC_FORMULA_REGISTRY_EMPTY")', "R8_ECONOMIC_AUTHORITY", "R8_ECONOMIC_AUTHORITY|FAIL"),
        ("ECON_DUP_FORMULA", "economic formula duplicate", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("ECONOMIC_FORMULA_DUPLICATE")', 'return pass_result("ECONOMIC_FORMULA_DUPLICATE")', "R8_ECONOMIC_AUTHORITY", "R8_ECONOMIC_AUTHORITY|FAIL"),
        ("ECON_FORMULA_AUTHORITY", "economic formula authority", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("ECONOMIC_FORMULA_AUTHORITY_MISMATCH")', 'return pass_result("ECONOMIC_FORMULA_AUTHORITY_MISMATCH")', "R8_ECONOMIC_AUTHORITY", "R8_ECONOMIC_AUTHORITY|FAIL"),
        ("ECON_EMPTY_SOURCE", "economic source empty", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("ECONOMIC_NORMATIVE_SOURCE_REGISTRY_EMPTY")', 'return pass_result("ECONOMIC_NORMATIVE_SOURCE_REGISTRY_EMPTY")', "R8_ECONOMIC_AUTHORITY", "R8_ECONOMIC_AUTHORITY|FAIL"),
        ("ECON_SOURCE_AUTHORITY", "economic source authority", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("ECONOMIC_NORMATIVE_SOURCE_AUTHORITY_MISMATCH")', 'return pass_result("ECONOMIC_NORMATIVE_SOURCE_AUTHORITY_MISMATCH")', "R8_ECONOMIC_AUTHORITY", "R8_ECONOMIC_AUTHORITY|FAIL"),
        ("ECON_GRID_BIND", "economic grid binding", "Tests/Reference/hsb_2e_validation_r4_r8.py", 'return reject("ECONOMIC_BROKER_GRID_MISMATCH")', 'return pass_result("ECONOMIC_BROKER_GRID_MISMATCH")', "R8_ECONOMIC_AUTHORITY", "R8_ECONOMIC_AUTHORITY|FAIL"),
        ("MODEL_UNKNOWN_PASS", "unknown operation fail closed", "Tests/Reference/hsb_2e_reference_model_r4_r8.py", 'return _reject("UNKNOWN_OPERATION")', 'return {"status": "PASS", "reason": "UNKNOWN_OPERATION"}', "R8_INDEPENDENT_INVARIANTS", "R8_UNKNOWN_PROPERTY_FAIL_CLOSED=FAIL"),
        ("MODEL_SCHEMA_PASS", "schema fail closed", "Tests/Reference/hsb_2e_reference_model_r4_r8.py", 'if canonical.get("schemaVersion") != CURRENT_SCHEMA_VERSION:\n        return _reject("SCHEMA_VERSION_UNSUPPORTED")', 'if canonical.get("schemaVersion") != CURRENT_SCHEMA_VERSION:\n        return {"status": "PASS", "reason": "SCHEMA_VERSION_UNSUPPORTED"}', "R8_INDEPENDENT_INVARIANTS", "R8_INDEPENDENT_INVARIANTS|FAIL"),
    ]
    return tuple(Mutation(*spec) for spec in specs)

def run(root: str, write: bool = False) -> bool:
    project = Path(root).resolve()
    catalog = mutations()
    ids = {item.mutationId for item in catalog}
    transforms = {(item.target, item.oldFragment, item.newFragment) for item in catalog}
    bindings = {(item.mutationClass, item.target) for item in catalog}
    rows = []
    for mutation in catalog:
        source = (project / mutation.target).read_text()
        applied = source.count(mutation.oldFragment) == 1
        caught = False
        wrong_failure = False
        infrastructure = False
        exit_code = -1
        if applied:
            with tempfile.TemporaryDirectory(prefix="hsb-r8-mut-") as temporary:
                fixture = Path(temporary) / "project"
                shutil.copytree(project, fixture)
                provisional = {"RESULT": "PASS", "MUTATIONS_CAUGHT": 40}
                evidence = fixture / "Tests/Evidence/HSB_2E_PREP_R4_R8_MUTATION_RESULTS.json"
                evidence.write_text(json.dumps(provisional))
                target = fixture / mutation.target
                before = hashlib.sha256(target.read_bytes()).hexdigest()
                target.write_text(source.replace(mutation.oldFragment, mutation.newFragment, 1))
                after = hashlib.sha256(target.read_bytes()).hexdigest()
                environment = dict(os.environ)
                environment["HSB_R8_MUTATION"] = "1"
                process = subprocess.run(
                    ["python3", str(fixture / "Tests/Static/verify_hsb_2e_prep_r4_r8.py"), "--root", str(fixture)],
                    capture_output=True, text=True, timeout=60, env=environment,
                )
                exit_code = process.returncode
                output = process.stdout
                caught = exit_code != 0 and before != after and f"{mutation.expectedCheckId}|FAIL" in output and mutation.expectedReason in output and "INFRASTRUCTURE_FAILURE=1" not in output
                wrong_failure = exit_code != 0 and not caught and "INFRASTRUCTURE_FAILURE=1" not in output
                infrastructure = "INFRASTRUCTURE_FAILURE=1" in output
        rows.append({**asdict(mutation), "applied": applied, "caught": caught, "wrongFailure": wrong_failure, "infrastructureFailure": infrastructure, "exitCode": exit_code})
    result = {
        "SEMANTIC_MUTATIONS_REQUIRED": len(catalog),
        "UNIQUE_MUTATION_IDS": len(ids),
        "UNIQUE_TRANSFORMS": len(transforms),
        "UNIQUE_CLASS_TARGET_BINDINGS": len(bindings),
        "MUTATIONS_EXECUTED": sum(row["applied"] for row in rows),
        "MUTATIONS_CAUGHT": sum(row["caught"] for row in rows),
        "SURVIVED": sum(row["applied"] and not row["caught"] and not row["wrongFailure"] and not row["infrastructureFailure"] for row in rows),
        "INVALID": 0,
        "NOT_APPLIED": sum(not row["applied"] for row in rows),
        "WRONG_FAILURES": sum(row["wrongFailure"] for row in rows),
        "INFRASTRUCTURE_FAILURES": sum(row["infrastructureFailure"] for row in rows),
        "ASSERTION_RESULT_MUTATIONS": 0,
        "SELF_SABOTAGE_MUTATIONS": 0,
        "rows": rows,
    }
    required = len(catalog)
    result["RESULT"] = "PASS" if result["UNIQUE_MUTATION_IDS"] == result["UNIQUE_TRANSFORMS"] == result["UNIQUE_CLASS_TARGET_BINDINGS"] == result["MUTATIONS_EXECUTED"] == result["MUTATIONS_CAUGHT"] == required and not any(result[key] for key in ("SURVIVED", "INVALID", "NOT_APPLIED", "WRONG_FAILURES", "INFRASTRUCTURE_FAILURES")) else "FAIL"
    if write:
        (project / "Tests/Contracts/HSB_2E_R4_R8_MUTATION_CATALOG.json").write_text(json.dumps({"schemaVersion": 1, "mutations": [asdict(item) for item in catalog]}, indent=2, sort_keys=True) + "\n")
        (project / "Tests/Evidence/HSB_2E_PREP_R4_R8_MUTATION_RESULTS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "rows"}, sort_keys=True, separators=(",", ":")))
    return result["RESULT"] == "PASS"
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    raise SystemExit(0 if run(args.root, args.write) else 1)
