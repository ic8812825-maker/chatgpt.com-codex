from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from openpyxl import load_workbook

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


@dataclass
class Params:
    start_lot: float = 1.0
    big_ratio: float = 1.15
    small_ratio: float = 0.38
    close_far_share: float = 0.20
    reserve_share: float = 0.80
    close_big_on_small: float = 0.22
    remain_big_on_small: float = 0.78
    point_value_per_lot: float = 1.0
    margin_per_lot: float = 1000.0
    lot_step: float = 0.01
    max_big_ratio: float = 1.20
    max_small_ratio: float = 0.45


def round_lot(value: float, step: float = 0.01) -> float:
    return round(round(value / step) * step, 10)


def big_side_model(
    far_start: float,
    big_profit: float,
    loss_small: float,
    commission: float,
    spread: float,
    slippage: float,
    loss_per_lot: float,
    params: Params = Params(),
):
    costs = commission + spread + slippage
    net_profit = big_profit - loss_small - costs
    close_far_budget = net_profit * params.close_far_share if net_profit > 0 else 0
    reserve_add = net_profit * params.reserve_share if net_profit > 0 else 0
    close_far_lot = 0 if loss_per_lot <= 0 else min(far_start, max(0, close_far_budget / loss_per_lot))
    far_remain = max(0, far_start - close_far_lot)
    status = "WARNING" if loss_per_lot <= 0 or net_profit <= 0 or reserve_add == 0 else "OK"
    return {
        "costs": costs,
        "net_profit": net_profit,
        "close_far_budget": close_far_budget,
        "reserve_add": reserve_add,
        "close_far_lot": close_far_lot,
        "far_remain": far_remain,
        "status": status,
    }


def small_side_model(far_start: float, params: Params = Params()):
    big_lot = round_lot(far_start * params.big_ratio, params.lot_step)
    close_big = big_lot * params.close_big_on_small
    remain_big = big_lot * params.remain_big_on_small
    return {
        "big_lot": big_lot,
        "close_big": close_big,
        "remain_big": remain_big,
        "new_far_start": remain_big,
    }


def workbook():
    assert WORKBOOK.exists()
    return load_workbook(WORKBOOK, data_only=False)


def settings_map(wb):
    ws = wb["Settings"]
    return {ws.cell(row, 1).value: ws.cell(row, 2).value for row in range(2, 18)}


def test_sheet_structure_is_exact():
    assert workbook().sheetnames == EXPECTED_SHEETS


def test_settings_defaults_and_editable_cells():
    wb = workbook()
    settings = settings_map(wb)
    expected = {
        "StartLot": 1,
        "BigRatio": 1.15,
        "SmallRatio": 0.38,
        "CloseFarShare": 0.20,
        "ReserveShare": 0.80,
        "CloseBigOnSmall": 0.22,
        "RemainBigOnSmall": 0.78,
        "PointValuePerLot": 1,
        "MarginPerLot": 1000,
        "LotStep": 0.01,
        "MaxLevels": 10,
        "CommissionPerLot": 0,
        "SpreadCostPerLot": 0,
        "SlippageCostPerLot": 0,
        "MaxBigRatio": 1.20,
        "MaxSmallRatio": 0.45,
    }
    assert settings == expected
    for row in range(2, 18):
        assert wb["Settings"].cell(row, 2).data_type == "n"


def test_big_and_small_formula_math():
    assert round_lot(1.00 * 1.15) == 1.15
    assert round_lot(0.80 * 1.15) == 0.92
    small_raw = 1.15 * 0.38
    small_lot = round_lot(small_raw)
    assert small_raw == 0.43699999999999994
    assert small_lot == 0.44
    assert small_lot / 1.15 <= 0.45


def test_direction_sheets_have_v2_direction_logic():
    wb = workbook()
    assert wb["Trend_UP"]["C2"].value == "SELL"
    assert wb["Trend_UP"]["E2"].value == '=IF(C2="SELL","BUY","SELL")'
    assert wb["Trend_UP"]["H2"].value == "=C2"
    assert wb["Trend_DOWN"]["C2"].value == "BUY"
    assert wb["Trend_DOWN"]["E2"].value == '=IF(C2="SELL","BUY","SELL")'
    assert wb["Trend_DOWN"]["H2"].value == "=C2"


def test_calculator_big_side_formulas_close_big_small_and_use_monetary_budget():
    wb = workbook()
    ws = wb["Calculator"]
    assert ws["AN2"].value == '=IF(B2="BIG_SIDE",1,IF(B2="SMALL_SIDE",Settings!$B$7,0))'
    assert ws["AO2"].value == '=IF(OR(B2="BIG_SIDE",B2="SMALL_SIDE"),1,0)'
    assert ws["S2"].value == '=IF(B2="BIG_SIDE",N2-P2-R2,O2-Q2-R2)'
    assert ws["T2"].value == '=IF(AND(B2="BIG_SIDE",S2>0),S2*Settings!$B$5,0)'
    assert ws["X2"].value == '=IF(B2="BIG_SIDE",IF(S2>0,S2*Settings!$B$6,0),IF(S2>0,S2*0.5,0))'


def test_big_side_numeric_cost_budget_and_tail_close_cases():
    result = big_side_model(
        far_start=1.0,
        big_profit=200,
        loss_small=60,
        commission=5,
        spread=3,
        slippage=2,
        loss_per_lot=100,
    )
    assert result["costs"] == 10
    assert result["net_profit"] == 130
    assert result["close_far_budget"] == 26
    assert result["reserve_add"] == 104
    assert result["close_far_lot"] == 0.26
    assert result["far_remain"] == 0.74
    assert result["status"] == "OK"


def test_zero_division_and_negative_net_profit_are_guarded():
    zero_loss = big_side_model(1.0, 200, 60, 5, 3, 2, 0)
    assert zero_loss["close_far_lot"] == 0
    assert zero_loss["status"] == "WARNING"
    negative = big_side_model(1.0, 100, 120, 5, 3, 2, 100)
    assert negative["net_profit"] == -30
    assert negative["close_far_budget"] == 0
    assert negative["reserve_add"] == 0
    assert negative["close_far_lot"] == 0
    assert negative["status"] == "WARNING"


def test_small_side_close_remain_and_self_compression():
    first = small_side_model(1.0)
    assert first["big_lot"] == 1.15
    assert round(first["close_big"], 3) == 0.253
    assert round(first["remain_big"], 3) == 0.897
    assert round(first["new_far_start"], 3) == 0.897
    second = small_side_model(0.897)
    assert second["big_lot"] == 1.03
    # The exact v2 compression before lot-step rounding is 0.804609.
    assert round(0.897 * 1.15 * 0.78, 6) == 0.804609
    assert second["new_far_start"] < 0.897


def test_dual_tail_and_new_level_block_formulas():
    ws = workbook()["Calculator"]
    assert ws["AK2"].value == '=IF(AND(AJ2>0,AG2>0),TRUE,FALSE)'
    assert ws["AQ2"].value.startswith('=IF(AK2=TRUE,"DUAL_TAIL"')
    assert ws["AP2"].value == '=IF(OR(AQ2="DUAL_TAIL",AQ2="DANGER",AQ2="STOP"),"NO","YES")'


def test_margin_balance_reserve_and_limit_status_formulas():
    ws = workbook()["Calculator"]
    assert ws["AB2"].value == "=D2+G2+J2"
    assert ws["AD2"].value == "=AB2*Settings!$B$10"
    assert ws["AE2"].value == "=AC2*Settings!$B$10"
    assert ws["AA2"].value == "=Z2+S2"
    assert "IFERROR(G2/D2,999)>Settings!$B$16" in ws["AQ2"].value
    assert "IFERROR(J2/G2,999)>Settings!$B$17" in ws["AQ2"].value
    open_lots_before = 1.00 + 1.15 + 0.44
    assert round(open_lots_before, 2) == 2.59
    assert open_lots_before * 1000 == 2590


def test_tests_sheet_is_detailed_and_has_at_least_25_tests():
    ws = workbook()["Tests"]
    assert [ws.cell(1, c).value for c in range(1, 9)] == [
        "Test ID",
        "Test Name",
        "Input",
        "Expected",
        "Actual",
        "Formula Checked",
        "Status",
        "Comment",
    ]
    assert ws.max_row >= 26
    statuses = [ws.cell(row, 7).value for row in range(2, ws.max_row + 1)]
    assert set(statuses) == {"PASS"}


def test_risk_analysis_examples_and_manual_v2_anchors():
    wb = workbook()
    risk_names = [wb["Risk_Analysis"].cell(row, 1).value for row in range(2, 14)]
    for required in [
        "Total Closed Profit",
        "Total Closed Loss",
        "Final Balance",
        "Final Reserve",
        "Max Margin",
        "Max Open Lots",
        "Final Far Lot",
        "Number of BIG_SIDE",
        "Number of SMALL_SIDE",
        "Dual Tail Count",
        "Danger Count",
        "Final Status",
    ]:
        assert required in risk_names
    examples = "\n".join(str(wb["Examples"].cell(row, col).value or "") for row in range(1, wb["Examples"].max_row + 1) for col in range(1, 5))
    assert "Пример 1. Тренд вверх" in examples
    assert "BIG_SIDE" in examples
    assert "Пример 2. Разворот вниз" in examples
    assert "SMALL_SIDE" in examples
    manual = "\n".join(str(wb["Manual"].cell(row, 1).value or "") for row in range(1, wb["Manual"].max_row + 1))
    for text in [
        "Close Big = 100%",
        "Close Small = 100%",
        "NetProfit = ProfitBig - LossSmall - Commission - SpreadCost - SlippageCost",
        "Основной режим системы — **денежный**",
        "20% — это денежный бюджет",
        "Close Big = 22%",
        "Remain Big = 78%",
        "DUAL_TAIL",
        "STOP",
        "Small не должен накапливаться",
    ]:
        assert text in manual
