#!/usr/bin/env python3
"""Validate V2.4.22 offline optimization artifacts before delivery."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "Optimization_Report.csv"
BEST_PATH = ROOT / "Best_Parameters.md"
SETS_DIR = ROOT / "Sets"
MIN_ROWS = 100_000
REQUIRED_COLUMNS = {
    "StabilityScore",
    "RobustnessScore",
    "FinalRank",
    "CoverageRatio",
    "IsSelectableForSetFile",
}
REQUIRED_SECTIONS = [
    "## TOP ACCEPT",
    "## TOP REJECTED",
    "## Why rejected",
    "## Sensitivity Analysis",
    "## Stability analysis",
    "## Robustness analysis",
]
SET_KEY_FIELDS = [
    "StartLot",
    "BigRatio",
    "SmallRatio",
    "CloseBigOnSmall",
    "RemainBigOnSmall",
    "CloseFarShare",
    "ReserveShare",
    "SmallReserveShare",
    "InitialTriggerPoints",
    "BigMoveStartPoints",
    "BigMoveStepPoints",
    "FarDistancePoints",
    "MaxHarvestLevels",
    "MaxReverseCycles",
    "MaxSpreadPoints",
    "MaxMarginPercent",
    "MaxDrawdownPercent",
]


def fail(reason: str) -> int:
    print("OPTIMIZATION_OUTPUT_VALIDATION_FAIL")
    print(f"reason={reason}")
    return 1


def read_csv_rows() -> List[Dict[str, str]]:
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_set_file(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def as_float(value: str) -> float:
    return float(str(value).strip())


def same_numeric(left: str, right: str) -> bool:
    try:
        return abs(as_float(left) - as_float(right)) < 1e-9
    except ValueError:
        return str(left).strip() == str(right).strip()


def matching_rows(rows: Iterable[Dict[str, str]], set_values: Dict[str, str]) -> List[Dict[str, str]]:
    matches: List[Dict[str, str]] = []
    for row in rows:
        ok = True
        for field in SET_KEY_FIELDS:
            if field in set_values and field in row and not same_numeric(set_values[field], row[field]):
                ok = False
                break
        if ok:
            matches.append(row)
    return matches


def section_text(report: str, heading: str) -> str:
    start = report.find(heading)
    if start < 0:
        return ""
    next_heading = report.find("\n## ", start + 1)
    if next_heading < 0:
        return report[start:]
    return report[start:next_heading]


def table_verdicts(section: str) -> List[str]:
    verdicts: List[str] = []
    verdict_index = -1
    for line in section.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if "Verdict" in cells:
            verdict_index = cells.index("Verdict")
            continue
        if cells and verdict_index >= 0 and verdict_index < len(cells):
            verdicts.append(cells[verdict_index])
    return verdicts


def main() -> int:
    if not CSV_PATH.exists():
        return fail(f"missing_csv={CSV_PATH}")
    if not BEST_PATH.exists():
        return fail(f"missing_best_parameters={BEST_PATH}")
    if not SETS_DIR.exists():
        return fail(f"missing_sets_dir={SETS_DIR}")

    rows = read_csv_rows()
    if len(rows) < MIN_ROWS:
        return fail(f"csv_rows_below_minimum rows={len(rows)} minimum={MIN_ROWS}")
    if not rows:
        return fail("csv_empty")

    columns = set(rows[0].keys())
    missing = sorted(REQUIRED_COLUMNS - columns)
    if missing:
        return fail(f"missing_required_columns={','.join(missing)}")

    accepted = [row for row in rows if row.get("Verdict") == "ACCEPT"]
    rejected = [row for row in rows if row.get("Verdict") != "ACCEPT"]
    if not accepted:
        return fail("no_accept_rows")
    if not rejected:
        return fail("no_rejected_rows_for_diagnostics")

    bad_selectable = [row.get("RunID", "?") for row in rejected if row.get("IsSelectableForSetFile") != "NO"]
    if bad_selectable:
        return fail(f"rejected_rows_selectable run_ids={bad_selectable[:10]}")

    max_rejected_rank = max(as_float(row["FinalRank"]) for row in rejected)
    min_accepted_rank = min(as_float(row["FinalRank"]) for row in accepted)
    if max_rejected_rank >= min_accepted_rank:
        return fail(f"rejected_finalrank_not_below_accept max_rejected={max_rejected_rank} min_accept={min_accepted_rank}")

    report = BEST_PATH.read_text(encoding="utf-8")
    if "These are offline candidates, not MT5-approved parameters." not in report:
        return fail("missing_offline_not_mt5_warning")
    for section in REQUIRED_SECTIONS:
        if section not in report:
            return fail(f"missing_report_section={section}")

    top_accept_verdicts = table_verdicts(section_text(report, "## TOP ACCEPT"))
    if not top_accept_verdicts or any(v != "ACCEPT" for v in top_accept_verdicts):
        return fail(f"top_accept_contains_non_accept verdicts={top_accept_verdicts[:5]}")

    top_rejected_verdicts = table_verdicts(section_text(report, "## TOP REJECTED"))
    if not top_rejected_verdicts or any(v == "ACCEPT" for v in top_rejected_verdicts):
        return fail(f"top_rejected_contains_accept verdicts={top_rejected_verdicts[:5]}")

    selectable = [row for row in accepted if row.get("IsSelectableForSetFile") == "YES"]
    for set_path in sorted(SETS_DIR.glob("*.set")):
        set_values = parse_set_file(set_path)
        matches = matching_rows(selectable, set_values)
        if not matches:
            return fail(f"set_file_not_backed_by_accepted_selectable_csv_row file={set_path.name}")

    aggressive_set = SETS_DIR / "USDJPY_M30_AGGRESSIVE.set"
    aggressive_marker = SETS_DIR / "USDJPY_M30_AGGRESSIVE_NOT_FOUND.txt"
    aggressive_accept = [row for row in selectable if as_float(row.get("StartLot", "0")) >= 0.50]
    if not aggressive_accept and aggressive_set.exists():
        return fail("aggressive_set_exists_without_aggressive_accept_candidate")
    if not aggressive_accept and not aggressive_marker.exists():
        return fail("aggressive_not_found_marker_missing")

    lowlot_001_accept = [row for row in selectable if abs(as_float(row.get("StartLot", "0")) - 0.01) < 1e-9]
    if not lowlot_001_accept and "LOWLOT_0_01_NOT_FOUND" not in report:
        return fail("missing_lowlot_0_01_not_found_marker")

    print("OPTIMIZATION_OUTPUT_VALIDATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
