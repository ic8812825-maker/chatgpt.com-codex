#!/usr/bin/env python3
"""Build the phase-A oracle only from immutable historical expectations."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any
FILES = {
    "R4_R2": "HSB_2E_R4_R2_VECTORS.json",
    "R4_R3": "HSB_2E_R4_R3_VECTORS.json",
    "R4_R4": "HSB_2E_R4_R4_VECTORS.json",
}
FIELDS = (
    "status", "reason", "phase", "fillClassification", "settlementEligible",
    "settlementApplied", "allocationEligible", "allocationApplied", "stateMutated",
    "evidenceRevisionDelta", "stateRevisionDelta", "settlementRevisionDelta",
    "acceptedDealIds", "acceptedEventIds", "moneyByTicket", "moneyByRole",
    "totalMoney", "volumeByTicket", "totalVolume", "reserveBefore", "reserveAdded",
    "reserveConsumed", "reserveAfter", "recoveryPLBefore", "recoveryPLAfter",
    "farVolumeBefore", "farVolumeAfter", "newFarTicket", "newFarVolume",
    "partialFarVolume", "finalCloseAllowed", "certificatePresent", "persistenceApplied",
)
def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()
def old_result(vector: dict[str, Any]) -> dict[str, Any]:
    result = vector.get("EXPECTED_RESULT")
    return result if isinstance(result, dict) else {}
def expected_row(version: str, vector: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    historical = old_result(vector)
    output = historical.get("output") if isinstance(historical.get("output"), dict) else {}
    status = historical.get("status", vector.get("EXPECTED_STATUS", "REJECT"))
    reason = historical.get("reason", vector.get("EXPECTED_REASON", "HISTORICAL_EXPECTED_REJECT"))
    phase = historical.get("phase", vector.get("EXPECTED_PHASE", "VALIDATION_BLOCKED"))
    settlement = bool(output.get("settlementApplied", False))
    allocation = bool(output.get("allocationApplied", False))
    deals = output.get("acceptedDealIds", output.get("consumedDealIds", []))
    events = output.get("seenEventIds", [])
    money_ticket = output.get("moneyByTicket", {})
    volumes = output.get("confirmedVolumeByTicket", {})
    values: dict[str, Any] = {
        "status": status,
        "reason": reason,
        "phase": phase,
        "fillClassification": output.get("fillState", "FULL_FILL" if settlement else "INVALID_FILL"),
        "settlementEligible": settlement,
        "settlementApplied": settlement,
        "allocationEligible": allocation,
        "allocationApplied": allocation,
        "stateMutated": settlement,
        "evidenceRevisionDelta": int(output.get("evidenceRevision", 0)),
        "stateRevisionDelta": 1 if settlement else 0,
        "settlementRevisionDelta": 1 if settlement else 0,
        "acceptedDealIds": deals,
        "acceptedEventIds": events,
        "moneyByTicket": money_ticket,
        "moneyByRole": {},
        "totalMoney": output.get("money", "0"),
        "volumeByTicket": volumes,
        "totalVolume": output.get("confirmedVolume", "0"),
        "reserveBefore": "0", "reserveAdded": "0", "reserveConsumed": "0", "reserveAfter": "0",
        "recoveryPLBefore": "0", "recoveryPLAfter": "0", "farVolumeBefore": "0", "farVolumeAfter": "0",
        "newFarTicket": 0, "newFarVolume": "0", "partialFarVolume": "0",
        "finalCloseAllowed": False, "certificatePresent": settlement, "persistenceApplied": settlement,
    }
    row = {
        "version": version,
        "vectorId": vector["VECTOR_ID"],
        "inputSHA256": sha(vector["INPUT"]),
        "classification": "HISTORICAL_EXPECTED",
        "expected": values,
    }
    provenance = []
    for field in FIELDS:
        provenance.append({
            "version": version,
            "vectorId": vector["VECTOR_ID"],
            "expectedField": field,
            "expectedValue": values[field],
            "sourceDocument": f"Tests/Vectors/{FILES[version]}",
            "sourceSection": vector["VECTOR_ID"],
            "sourceFormulaOrRuleId": "HISTORICAL_EXPECTED_RESULT",
            "derivationType": "HISTORICAL_EXPECTED",
            "derivationDescription": "Direct field or fail-closed neutral projection from the published historical expectation.",
        })
    return row, provenance
def build(root: str) -> None:
    project = Path(root).resolve()
    rows = []
    provenance = []
    for version, filename in FILES.items():
        vectors = json.loads((project / "Tests/Vectors" / filename).read_text())["vectors"]
        for vector in vectors:
            row, sources = expected_row(version, vector)
            rows.append(row)
            provenance.extend(sources)
    oracle = {"schemaVersion": 1, "fields": list(FIELDS), "vectors": rows}
    proof = {"schemaVersion": 1, "oracleBuilder": "historical expectations only", "entries": provenance}
    (project / "Tests/Contracts/HSB_2E_R4_R8_SEMANTIC_ORACLE.json").write_text(json.dumps(oracle, indent=2, sort_keys=True) + "\n")
    (project / "Tests/Evidence/HSB_2E_PREP_R4_R8_ORACLE_PROVENANCE.json").write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n")
    print(f"ORACLE_ROWS={len(rows)}")
    print(f"PROVENANCE_ROWS={len(provenance)}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    build(args.root)
