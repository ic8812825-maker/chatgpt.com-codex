#!/usr/bin/env python3
"""Structural validator for Stage 3.1.3 documentation; it does not prove trading math."""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "Docs"
MANUAL = DOCS / "HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md"
GLOSSARY = DOCS / "HYBRID_SPLIT_BIG_GLOSSARY_AND_DIMENSIONS_RU.md"
REPORT = DOCS / "STAGE_3_1_3_GLOSSARY_AND_DIMENSIONS_REPORT_RU.md"
START = "<!-- STAGE_3_1_3_CANONICAL_TABLE_START -->"
END = "<!-- STAGE_3_1_3_CANONICAL_TABLE_END -->"
COLS = ["Canonical term", "Русское название", "Profile", "Type", "Unit", "Sign", "Projected/Actual", "Authoritative source", "Rounding", "Tolerance", "Aliases", "Status"]
VALID_STATUS = {"APPROVED_TERM", "DOCUMENTED_NOT_APPROVED", "UNRESOLVED_PARAMETER_PROFILE", "UNRESOLVED_BUSINESS_POLICY", "UNRESOLVED_MODE_ROUTING", "MISSING_DEFINITION"}
UNRESOLVED = {x for x in VALID_STATUS if x.startswith("UNRESOLVED") or x == "MISSING_DEFINITION"}

def fail(message: str) -> None:
    raise AssertionError(message)

def extract_table(text: str) -> tuple[str, list[dict[str, str]]]:
    if text.count(START) != 1 or text.count(END) != 1:
        fail("canonical table markers must occur exactly once")
    raw = text.split(START, 1)[1].split(END, 1)[0].strip()
    lines = [line for line in raw.splitlines() if line.startswith("|")]
    header = [x.strip() for x in lines[0].strip("|").split("|")]
    if header != COLS:
        fail(f"unexpected columns: {header}")
    rows = []
    for line in lines[2:]:
        values = [x.strip() for x in line.strip("|").split("|")]
        if len(values) != len(COLS):
            fail(f"malformed canonical row: {line}")
        rows.append(dict(zip(COLS, values)))
    return raw, rows

def matrix(text: str, heading: str, minimum_rows: int) -> bool:
    match = re.search(rf"^### {re.escape(heading)}\n\n(.*?)(?=\n### |\n## |\Z)", text, re.M | re.S)
    if not match:
        return False
    rows = [x for x in match.group(1).splitlines() if x.startswith("|")]
    return len(rows) >= minimum_rows + 2 and all(len(x.split("|")) >= 5 for x in rows)

def main() -> int:
    manual, glossary, report = (p.read_text(encoding="utf-8") for p in (MANUAL, GLOSSARY, REPORT))
    manual_table, terms = extract_table(manual)
    glossary_table, glossary_terms = extract_table(glossary)
    if manual_table != glossary_table or terms != glossary_terms:
        fail("manual and appendix canonical tables differ")
    names = [r["Canonical term"] for r in terms]
    duplicates = len(names) - len(set(names))
    missing_type = sum(not r["Type"] for r in terms)
    missing_unit = sum(not r["Unit"] for r in terms)
    missing_sign = sum(not r["Sign"] for r in terms)
    missing_pa = sum(not r["Projected/Actual"] for r in terms)
    missing_source = sum(not r["Authoritative source"] for r in terms)
    missing_status = sum(not r["Status"] for r in terms)
    invalid_status = sum(r["Status"] not in VALID_STATUS for r in terms)
    if len(terms) < 120 or any((duplicates, missing_type, missing_unit, missing_sign, missing_pa, missing_source, missing_status, invalid_status)):
        fail("canonical term structural validation failed")
    # Extended records prove that unresolved rows carry both a conflict and a resolution stage.
    unresolved_names = [r["Canonical term"] for r in terms if r["Status"] in UNRESOLVED]
    missing_conflict = missing_stage = heading_only = 0
    for name in names:
        m = re.search(rf"^### {re.escape(name)}\n(.*?)(?=^### |\Z)", glossary, re.M | re.S)
        if not m:
            fail(f"missing extended record: {name}")
        record = m.group(1)
        required = ["CanonicalName:", "Краткое определение:", "Размерность:", "Знак:", "Источник:", "Authoritative source:", "Projected/Actual class:", "Rounding:", "Tolerance:", "MQL5 mapping:", "Python mapping:", "Статус определения:"]
        if any(field not in record for field in required):
            fail(f"incomplete extended record: {name}")
        definition = re.search(r"Краткое определение:\s*(.+)", record)
        heading_only += int(not definition or definition.group(1).lstrip().startswith("#"))
        if name in unresolved_names:
            missing_conflict += int("Conflict: `HSB-DOC-CONFLICT-" not in record)
            missing_stage += int("Resolution stage: `" not in record)
    matrix_results = {
        "SOURCE_OF_TRUTH_MATRIX": matrix(manual, "Source-of-truth matrix", 10),
        "SIGN_MATRIX": matrix(manual, "Sign matrix", 5),
        "TOLERANCE_MATRIX": matrix(manual, "Tolerance matrix", 9),
        "ROUNDING_MATRIX": matrix(manual, "Rounding namespaces", 9),
        "ARCHITECTURE_MATRIX": matrix(manual, "Architecture matrix", 8),
    }
    if not all(matrix_results.values()) or heading_only or missing_conflict or missing_stage:
        fail("matrix or unresolved-record validation failed")
    bare_big = int("Big" in names)
    bare_reserve = int("Reserve" in names)
    # These are structural class-separation checks: each lifecycle class is represented by a distinct canonical term/type.
    name_set = set(names)
    raw_mix = int(not {"RawLot", "NormalizedLot", "RequestedLot", "ActualPositionLot"}.issubset(name_set))
    projected_mix = int(not {"ProjectedData", "ConfirmedData", "ReconciledData"}.issubset(name_set))
    money_lot_mix = sum(r["Unit"] == "lot" and r["Type"].startswith("MONEY") for r in terms)
    outputs = {
        "CANONICAL_TERMS": len(terms), "DUPLICATE_CANONICAL_NAMES": duplicates,
        "MISSING_TYPE": missing_type, "MISSING_UNIT": missing_unit, "MISSING_SIGN": missing_sign,
        "MISSING_PROJECTED_ACTUAL_CLASS": missing_pa, "MISSING_SOURCE": missing_source,
        "MISSING_STATUS": missing_status, "INVALID_STATUS": invalid_status,
        "AMBIGUOUS_BARE_BIG_TERMS": bare_big, "AMBIGUOUS_BARE_RESERVE_TERMS": bare_reserve,
        "RAW_NORMALIZED_MIXING": raw_mix, "PROJECTED_ACTUAL_MIXING": projected_mix,
        "MONEY_LOT_MIXING": money_lot_mix, "HEADING_ONLY_DEFINITIONS": heading_only,
        "UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID": missing_conflict,
        "UNRESOLVED_ITEMS_WITHOUT_RESOLUTION_STAGE": missing_stage,
    }
    for k, v in outputs.items(): print(f"{k}={v}")
    for k, v in matrix_results.items(): print(f"{k}={'PASS' if v else 'FAIL'}")
    if "STAGE_3_1_3_STATUS=PASS" not in report or "Этап 3.1.4 не выполнялся." not in report:
        fail("stage report status/control missing")
    print("BUSINESS_MATHEMATICS_PROVED=NO")
    print("STAGE_3_1_3_VALIDATION=PASS")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"STAGE_3_1_3_VALIDATION=FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
