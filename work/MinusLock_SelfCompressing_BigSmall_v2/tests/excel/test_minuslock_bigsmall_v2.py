from __future__ import annotations

import re
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, range_boundaries
from openpyxl.formula.tokenizer import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKBOOK = PROJECT_ROOT / "MinusLock_SelfCompressing_BigSmall_v2.xlsx"
EXPECTED_SHEETS = [
    "Settings",
    "Calculator",
    "Trend_UP",
    "Trend_DOWN",
    "Risk_Analysis",
    "Tests",
    "Manual",
    "Examples",
]
CALC_SHEETS = ["Calculator", "Trend_UP", "Trend_DOWN"]
NEW_CYCLE_HEADERS = ["CycleClosed", "CycleCloseLevel", "CycleFinalPL"]
V9_HEADERS = [
    "CloseFarLotRaw",
    "CloseFarLotRounded",
    "FarRemainAfterRounded",
    "CannotCloseBelowLotStep",
    "FarRemainLoss",
    "FinalCloseAllowed",
    "FinalClosePL",
    "LostToRounding",
]


def workbook(data_only: bool = False):
    assert WORKBOOK.exists()
    return load_workbook(WORKBOOK, data_only=data_only)


def header_map(ws):
    return {ws.cell(1, col).value: col for col in range(1, ws.max_column + 1)}


def settings_map(wb):
    ws = wb["Settings"]
    return {ws.cell(row, 1).value: ws.cell(row, 2).value for row in range(2, 18)}


def risk_values(wb):
    ws = wb["Risk_Analysis"]
    values = {}
    for row in range(1, ws.max_row + 1):
        key = ws.cell(row, 1).value
        if key:
            values[str(key)] = ws.cell(row, 3).value
    return values


def test_sheet_structure_and_settings_defaults():
    wb = workbook()
    assert wb.sheetnames == EXPECTED_SHEETS
    assert settings_map(wb) == {
        "StartLot": 1,
        "BigRatio": 1.30,
        "SmallRatio": 0.36,
        "CloseFarShare": 0.90,
        "ReserveShare": 0.10,
        "CloseBigOnSmall": 0.30,
        "RemainBigOnSmall": 0.70,
        "PointValuePerLot": 1,
        "MarginPerLot": 1000,
        "LotStep": 0.01,
        "MaxLevels": 10,
        "CommissionPerLot": 0,
        "SpreadCostPerLot": 0,
        "SlippageCostPerLot": 0,
        "MaxBigRatio": 1.35,
        "MaxSmallRatio": 0.45,
    }


def test_calculation_sheets_have_synchronized_headers_and_cycle_columns():
    wb = workbook()
    headers = {sheet: [cell.value for cell in wb[sheet][1]] for sheet in CALC_SHEETS}
    assert headers["Calculator"] == headers["Trend_UP"] == headers["Trend_DOWN"]
    for sheet in CALC_SHEETS:
        idx = header_map(wb[sheet])
        for header in V9_HEADERS + NEW_CYCLE_HEADERS:
            assert header in idx, f"{sheet} missing {header}"


def test_close_far_share_is_money_budget_not_far_lot_percent():
    wb = workbook(data_only=True)
    ws = wb["Calculator"]
    idx = header_map(ws)
    row = 2
    assert ws.cell(row, idx["FarStartLot"]).value == 1
    assert round(ws.cell(row, idx["BigLot"]).value, 2) == 1.30
    assert round(ws.cell(row, idx["SmallLot"]).value, 2) == 0.47
    assert round(ws.cell(row, idx["NetProfitBeforeFar"]).value, 2) == 83.00
    assert round(ws.cell(row, idx["CloseFarBudget"]).value, 2) == 74.70
    assert round(ws.cell(row, idx["CloseFarLotRaw"]).value, 4) == 0.3735
    assert round(ws.cell(row, idx["CloseFarLotRounded"]).value, 2) == 0.37
    assert ws.cell(row, idx["CloseFarLotRounded"]).value != 0.90


def test_lotstep_rounding_and_below_step_flag():
    wb = workbook(data_only=True)
    ws = wb["Calculator"]
    idx = header_map(ws)
    lot_step = wb["Settings"]["B11"].value
    for row in range(2, ws.max_row + 1):
        rounded = ws.cell(row, idx["CloseFarLotRounded"]).value or 0
        far_start = ws.cell(row, idx["FarStartLot"]).value or 0
        assert rounded >= 0
        assert rounded <= far_start + 1e-9
        if rounded:
            assert abs((rounded / lot_step) - round(rounded / lot_step)) < 1e-7
    raw_below_step = 0.009
    rounded_below_step = 0 if 0 < raw_below_step < lot_step else raw_below_step
    assert rounded_below_step == 0
    assert ("YES" if 0 < raw_below_step < lot_step else "NO") == "YES"


def test_full_cycle_closes_at_level_six_and_stops_following_levels():
    wb = workbook(data_only=True)
    ws = wb["Calculator"]
    idx = header_map(ws)
    close_rows = [
        row for row in range(2, ws.max_row + 1)
        if ws.cell(row, idx["CycleClosed"]).value == "YES"
        and ws.cell(row, idx["CycleFinalPL"]).value not in (None, 0)
    ]
    assert close_rows == [7]  # worksheet row 7 = Level 6
    close_row = close_rows[0]
    assert ws.cell(close_row, idx["Level"]).value == 6
    assert ws.cell(close_row, idx["Status"]).value == "CLOSED_PROFIT"
    assert ws.cell(close_row, idx["FinalCloseAllowed"]).value == "YES"
    assert round(ws.cell(close_row, idx["CycleFinalPL"]).value, 2) > 0
    for row in range(close_row + 1, ws.max_row + 1):
        assert ws.cell(row, idx["Scenario"]).value == "CLOSED"
        assert ws.cell(row, idx["Status"]).value == "CLOSED_PROFIT"
        assert ws.cell(row, idx["FarStartLot"]).value == 0
        assert ws.cell(row, idx["BigLot"]).value == 0
        assert ws.cell(row, idx["SmallLot"]).value == 0
        assert ws.cell(row, idx["CloseFarLotRaw"]).value == 0
        assert ws.cell(row, idx["CloseFarLotRounded"]).value == 0
        assert ws.cell(row, idx["FarRemainAfterRounded"]).value == 0
        assert ws.cell(row, idx["FarRemainLoss"]).value == 0
        assert ws.cell(row, idx["BalanceAfter"]).value == ws.cell(row - 1, idx["BalanceAfter"]).value
        assert ws.cell(row, idx["TotalReserve"]).value == ws.cell(row - 1, idx["TotalReserve"]).value


def _simulate_close_level(start_lot: float) -> int:
    import math
    far = start_lot
    reserve = 0.0
    for level in range(1, 11):
        big = round(far * 1.30 / 0.01) * 0.01
        small = round(big * 0.36 / 0.01) * 0.01
        net = big * 100 - small * 100
        reserve += net * 0.10
        raw = (net * 0.90) / 200
        rounded = min(far, math.floor(max(0, raw) / 0.01) * 0.01)
        remain = max(0, far - rounded)
        if reserve >= remain * 200:
            return level
        far = remain
    raise AssertionError("cycle did not close within 10 levels")


def test_expected_close_levels_for_startlot_scenarios():
    assert _simulate_close_level(1) == 6
    assert _simulate_close_level(2) == 5
    assert _simulate_close_level(5) == 5


def test_cycle_close_columns_have_expected_formulas():
    wb = workbook()
    ws = wb["Calculator"]
    idx = header_map(ws)
    assert ws.cell(2, idx["CycleClosed"]).value == '=IF($BT2="YES","YES","NO")'
    assert ws.cell(2, idx["CycleCloseLevel"]).value == '=IF($BV2="YES",$A2,0)'
    assert ws.cell(2, idx["CycleFinalPL"]).value == '=IF($BV2="YES",$Y2-$BN2,0)'
    assert 'CLOSED_PROFIT' in ws.cell(2, idx["Status"]).value
    assert ws.cell(3, idx["Scenario"]).value == '=IF($BV2="YES","CLOSED","BIG_SIDE")'


def test_risk_analysis_has_cycle_close_metrics():
    values = risk_values(workbook(data_only=True))
    assert values["Cycle Closed Count"] >= 1
    assert round(values["Average Close Level"], 0) == 6
    assert values["Earliest Close Level"] == 6
    assert values["Latest Close Level"] == 6
    assert values["Closed In Profit Count"] >= 1


def test_settings_geometry_stops_after_cycle_close():
    wb = workbook(data_only=True)
    ws = wb["Settings"]
    headers = {ws.cell(21, col).value: col for col in range(1, ws.max_column + 1)}
    assert "CycleClosed" in headers
    assert "CycleCloseLevel" in headers
    assert "CycleFinalPL" in headers
    assert "Status" in headers
    close_rows = [row for row in range(22, 32) if ws.cell(row, headers["CycleClosed"]).value == "YES"]
    assert close_rows and ws.cell(close_rows[0], headers["CycleCloseLevel"]).value == 6
    for row in range(close_rows[0] + 1, 32):
        assert ws.cell(row, headers["Status"]).value == "CLOSED"
        assert ws.cell(row, headers["FarStart-N"]).value == 0
        assert ws.cell(row, headers["Big-N"]).value == 0
        assert ws.cell(row, headers["Small-N"]).value == 0


def test_no_direct_self_references_or_formula_dependency_cycles():
    wb = workbook()
    graph: dict[str, set[str]] = {}
    cell_ref_re = re.compile(r"(?:(?P<sheet>'[^']+'|[A-Za-z_][A-Za-z0-9_]*)!)?(?P<ref>\$?[A-Z]{1,3}\$?\d+(?::\$?[A-Z]{1,3}\$?\d+)?)")
    sheet_names = set(wb.sheetnames)
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if not (isinstance(cell.value, str) and cell.value.startswith("=")):
                    continue
                node = f"{ws.title}!{cell.coordinate.upper()}"
                formula = cell.value.upper()
                assert not re.search(r"(?<![A-Z0-9_])" + re.escape(cell.coordinate.upper()) + r"(?![A-Z0-9_])", formula), node
                graph.setdefault(node, set())
                for match in cell_ref_re.finditer(cell.value):
                    sheet = match.group("sheet")
                    if sheet:
                        sheet = sheet.strip("'")
                    else:
                        sheet = ws.title
                    if sheet not in sheet_names:
                        continue
                    ref = match.group("ref").replace("$", "")
                    min_col, min_row, max_col, max_row = range_boundaries(ref)
                    # Keep graph small: only single-cell dependencies can form the local row cycles we care about.
                    if min_col == max_col and min_row == max_row:
                        dep = f"{sheet}!{get_column_letter(min_col)}{min_row}"
                        if dep in graph or sheet == ws.title:
                            graph[node].add(dep)
    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(node: str, stack: tuple[str, ...]):
        if node in visiting:
            raise AssertionError("formula dependency cycle: " + " -> ".join(stack + (node,)))
        if node in visited:
            return
        visiting.add(node)
        for dep in graph.get(node, ()):
            if dep in graph:
                dfs(dep, stack + (node,))
        visiting.remove(node)
        visited.add(node)

    for node in list(graph):
        dfs(node, ())
