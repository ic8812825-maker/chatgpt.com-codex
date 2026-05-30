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
REQUIRED_V3_HEADERS = [
    "RealizedFarLoss",
    "ClosedLotsForCosts",
    "CostPerLot",
    "OldFarClosedLot",
    "BlockedReason",
    "ActiveOldFarLot",
    "ActiveNewFarLot",
    "DualTailTotalLot",
    "ManualOldFarCloseLot",
    "ManualNewFarCloseLot",
    "ManualClosePL",
    "ManualAllowNewLevel",
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


def workbook():
    assert WORKBOOK.exists()
    return load_workbook(WORKBOOK, data_only=False)


def header_map(ws):
    return {ws.cell(1, column).value: column for column in range(1, ws.max_column + 1)}


def settings_map(wb):
    ws = wb["Settings"]
    return {ws.cell(row, 1).value: ws.cell(row, 2).value for row in range(2, 18)}


def big_side_v3_model(
    far_start: float,
    big_lot: float,
    small_lot: float,
    big_profit_points: float,
    small_points: float,
    far_loss_points: float,
    commission_per_lot: float,
    spread_cost_per_lot: float,
    slippage_cost_per_lot: float,
    params: Params = Params(),
):
    cost_per_lot = commission_per_lot + spread_cost_per_lot + slippage_cost_per_lot
    profit_big = big_lot * big_profit_points * params.point_value_per_lot
    loss_small = small_lot * abs(small_points) * params.point_value_per_lot
    loss_per_lot = max(0, far_loss_points * params.point_value_per_lot)
    costs_before_far = (big_lot + small_lot) * cost_per_lot
    net_profit_before_far = profit_big - loss_small - costs_before_far
    close_far_budget = net_profit_before_far * params.close_far_share if net_profit_before_far > 0 else 0
    close_far_lot = 0 if loss_per_lot <= 0 else min(far_start, max(0, close_far_budget / loss_per_lot))
    realized_far_loss = close_far_lot * loss_per_lot
    costs_far_close = close_far_lot * cost_per_lot
    closed_lots_for_costs = big_lot + small_lot + close_far_lot
    costs = closed_lots_for_costs * cost_per_lot
    net_profit = profit_big - loss_small - costs
    reserve_add = net_profit_before_far - realized_far_loss if net_profit_before_far > 0 else 0
    balance_after = net_profit_before_far - realized_far_loss - costs_far_close
    return {
        "profit_big": profit_big,
        "loss_small": loss_small,
        "cost_per_lot": cost_per_lot,
        "costs_before_far": costs_before_far,
        "net_profit_before_far": net_profit_before_far,
        "close_far_budget": close_far_budget,
        "close_far_lot": close_far_lot,
        "realized_far_loss": realized_far_loss,
        "costs_far_close": costs_far_close,
        "closed_lots_for_costs": closed_lots_for_costs,
        "costs": costs,
        "net_profit": net_profit,
        "reserve_add": reserve_add,
        "balance_after": balance_after,
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


def test_v3_required_columns_exist_on_all_calculation_sheets():
    wb = workbook()
    for sheet in ["Calculator", "Trend_UP", "Trend_DOWN"]:
        headers = header_map(wb[sheet])
        for required in REQUIRED_V3_HEADERS:
            assert required in headers, f"{sheet} missing {required}"


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
    assert wb["Trend_UP"]["E2"].value == '=IF($B2="BLOCKED","",IF($C2="SELL","BUY","SELL"))'
    assert wb["Trend_UP"]["H2"].value == '=IF($B2="BLOCKED","",$C2)'
    assert wb["Trend_DOWN"]["C2"].value == "BUY"
    assert wb["Trend_DOWN"]["E2"].value == '=IF($B2="BLOCKED","",IF($C2="SELL","BUY","SELL"))'
    assert wb["Trend_DOWN"]["H2"].value == '=IF($B2="BLOCKED","",$C2)'


def test_calculator_big_side_formulas_close_big_small_and_use_monetary_budget():
    ws = workbook()["Calculator"]
    assert ws["AN2"].value == '=IF($B2="BIG_SIDE",1,IF($B2="SMALL_SIDE",Settings!$B$7,0))'
    assert ws["AO2"].value == '=IF(OR($B2="BIG_SIDE",$B2="SMALL_SIDE"),1,0)'
    assert ws["T2"].value == '=IF(AND($B2="BIG_SIDE",$AX2>0),$AX2*Settings!$B$5,0)'
    assert ws["X2"].value == '=IF($B2="BIG_SIDE",IF($AX2>0,$AX2-$AS2,0),IF($S2>0,$S2*0.5,0))'


def test_costs_per_lot_are_multiplied_by_closed_lots():
    ws = workbook()["Calculator"]
    assert ws["AU2"].value == "=Settings!$B$13+Settings!$B$14+Settings!$B$15"
    assert ws["AT2"].value == '=IF($B2="BIG_SIDE",$G2+$J2+$V2,IF($B2="SMALL_SIDE",$J2+$AL2+$AV2,0))'
    assert ws["R2"].value == "=$AT2*$AU2"
    model = big_side_v3_model(1.0, 1.15, 0.44, 200 / 1.15, -60 / 0.44, 100, 5, 3, 2)
    assert round(model["closed_lots_for_costs"], 4) == 1.8382
    assert model["cost_per_lot"] == 10
    assert round(model["costs"], 3) == 18.382


def test_realized_far_loss_formula():
    ws = workbook()["Calculator"]
    assert ws["AS2"].value == '=IF($B2="BIG_SIDE",$V2*$U2,0)'
    model = big_side_v3_model(1.0, 1.15, 0.44, 200 / 1.15, -60 / 0.44, 100, 5, 3, 2)
    assert round(model["close_far_budget"], 2) == 24.82
    assert round(model["close_far_lot"], 4) == 0.2482
    assert round(model["realized_far_loss"], 2) == 24.82


def test_big_side_balance_after_realized_far_loss():
    ws = workbook()["Calculator"]
    assert ws["AA2"].value == '=IF($B2="BLOCKED",$Z2+$BF2,IF($B2="BIG_SIDE",$Z2+$AX2-$AS2-$AZ2,IF($B2="SMALL_SIDE",$Z2+$S2+$AI2,$Z2+$S2)))'
    model = big_side_v3_model(1.0, 1.15, 0.44, 200 / 1.15, -60 / 0.44, 100, 5, 3, 2)
    expected_balance = model["net_profit_before_far"] - model["realized_far_loss"] - model["costs_far_close"]
    assert round(model["balance_after"], 3) == round(expected_balance, 3)
    assert model["balance_after"] < model["net_profit_before_far"]


def test_reserve_add_uses_net_profit_before_far_minus_realized_far_loss():
    ws = workbook()["Calculator"]
    assert ws["X2"].value == '=IF($B2="BIG_SIDE",IF($AX2>0,$AX2-$AS2,0),IF($S2>0,$S2*0.5,0))'
    model = big_side_v3_model(1.0, 1.15, 0.44, 200 / 1.15, -60 / 0.44, 100, 5, 3, 2)
    assert round(model["reserve_add"], 2) == round(model["net_profit_before_far"] - model["realized_far_loss"], 2)


def test_zero_division_and_negative_net_profit_are_guarded():
    zero_loss = big_side_v3_model(1.0, 1.15, 0.44, 200 / 1.15, -60 / 0.44, 0, 5, 3, 2)
    assert zero_loss["close_far_lot"] == 0
    negative = big_side_v3_model(1.0, 1.15, 0.44, 100 / 1.15, -120 / 0.44, 100, 5, 3, 2)
    assert negative["net_profit_before_far"] < 0
    assert negative["close_far_budget"] == 0
    assert negative["reserve_add"] == 0
    assert negative["close_far_lot"] == 0


def test_small_side_close_remain_and_self_compression():
    first = small_side_model(1.0)
    assert first["big_lot"] == 1.15
    assert round(first["close_big"], 3) == 0.253
    assert round(first["remain_big"], 3) == 0.897
    assert round(first["new_far_start"], 3) == 0.897
    second = small_side_model(0.897)
    assert second["big_lot"] == 1.03
    assert round(0.897 * 1.15 * 0.78, 6) == 0.804609
    assert second["new_far_start"] < 0.897


def test_old_far_close_pl_affects_small_side_balance():
    ws = workbook()["Calculator"]
    assert ws["AA2"].value.endswith('IF($B2="SMALL_SIDE",$Z2+$S2+$AI2,$Z2+$S2)))')
    assert ws["AV2"].value == '=IF($B2="SMALL_SIDE",IF($AH2="YES",$D2,IFERROR(MIN($D2,MAX(0,$AI2/$U2)),0)),0)'
    balance_before = 1000
    flip_net = 50
    old_far_close_pl = -20
    assert balance_before + flip_net + old_far_close_pl == 1030


def test_dual_tail_blocks_next_level():
    ws = workbook()["Calculator"]
    assert ws["AK2"].value == '=IF(AND($AJ2>0,$AG2>0),TRUE,FALSE)'
    assert ws["AQ2"].value.startswith('=IF($B2="BLOCKED",IF($BC2=0,"STOP_CLEARED"')
    assert '"STOP"' in ws["AQ2"].value
    assert 'IF($AK2=TRUE,"DUAL_TAIL"' in ws["AQ2"].value
    assert ws["AP2"].value == '=IF(AND($AQ2="MANUAL_READY",$BG2="YES"),"YES",IF(OR($AQ2="DUAL_TAIL",$AQ2="DANGER",$AQ2="STOP",$AQ2="STOP_CLEARED",$AQ2="MANUAL_READY"),"NO","YES"))'
    assert ws["B3"].value.startswith('=IF(AND($AQ2="MANUAL_READY",$BG2="YES")')
    assert '"BLOCKED"' in ws["B3"].value
    assert ws["AW3"].value == '=IF($B3="BLOCKED","Заблокировано: DUAL_TAIL сохраняет оба хвоста до ручного закрытия","")'


def test_blocked_next_level_zeroes_big_and_small_lots():
    ws = workbook()["Calculator"]
    assert ws["F3"].value == '=IF($B3="BLOCKED",0,MAX(0,$D3*Settings!$B$3))'
    assert ws["G3"].value == '=IF($B3="BLOCKED",0,IFERROR(MAX(0,ROUND($F3/Settings!$B$11,0)*Settings!$B$11),0))'
    assert ws["I3"].value == '=IF($B3="BLOCKED",0,MAX(0,$G3*Settings!$B$4))'
    assert ws["J3"].value == '=IF($B3="BLOCKED",0,IFERROR(MAX(0,ROUND($I3/Settings!$B$11,0)*Settings!$B$11),0))'
    assert ws["AQ3"].value.startswith('=IF($B3="BLOCKED",IF($BC3=0,"STOP_CLEARED"')
    assert '"STOP"' in ws["AQ3"].value


def test_margin_balance_reserve_and_limit_status_formulas():
    ws = workbook()["Calculator"]
    assert ws["AB2"].value == '=IF($B2="BLOCKED",$BC2,$D2+$G2+$J2)'
    assert ws["AD2"].value == "=$AB2*Settings!$B$10"
    assert ws["AE2"].value == "=$AC2*Settings!$B$10"
    assert "IFERROR($G2/$D2,0)>Settings!$B$16" in ws["AQ2"].value
    assert "IFERROR($J2/$G2,0)>Settings!$B$17" in ws["AQ2"].value
    open_lots_before = 1.00 + 1.15 + 0.44
    assert round(open_lots_before, 2) == 2.59
    assert open_lots_before * 1000 == 2590


def test_risk_analysis_includes_realized_far_loss():
    wb = workbook()
    ws = wb["Risk_Analysis"]
    metrics = {ws.cell(row, 1).value: ws.cell(row, 3).value for row in range(2, ws.max_row + 1)}
    assert "Total Realized Far Loss" in metrics
    assert metrics["Total Realized Far Loss"] == "=SUM(Calculator!AS2:AS11)"
    assert "+SUM(Calculator!AS2:AS11)" in metrics["Total Closed Loss"]
    assert "=COUNTIF(Calculator!AQ2:AQ11,\"STOP\")" == metrics["Stop Count"]


def test_tests_sheet_is_detailed_and_has_v3_tests():
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
    assert ws.max_row >= 40
    statuses = [ws.cell(row, 7).value for row in range(2, ws.max_row + 1)]
    assert set(statuses) == {"PASS"}
    test_names = {ws.cell(row, 2).value for row in range(2, ws.max_row + 1)}
    for required in [
        "RealizedFarLoss formula",
        "BIG_SIDE BalanceAfter includes far loss",
        "Total Closed Loss includes RealizedFarLoss",
        "DUAL_TAIL blocks next level",
        "Costs per lot multiplied",
        "OldFarClosePL affects SMALL_SIDE balance",
    ]:
        assert required in test_names


def test_risk_analysis_examples_and_manual_v2_anchors():
    wb = workbook()
    risk_names = [wb["Risk_Analysis"].cell(row, 1).value for row in range(2, wb["Risk_Analysis"].max_row + 1)]
    for required in [
        "Total Closed Profit",
        "Total Closed Loss",
        "Total Realized Far Loss",
        "Final Balance",
        "Final Reserve",
        "Max Margin",
        "Max Open Lots",
        "Final Far Lot",
        "Number of BIG_SIDE",
        "Number of SMALL_SIDE",
        "Dual Tail Count",
        "Danger Count",
        "Stop Count",
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


def test_dual_tail_persists_old_and_new_tail():
    ws = workbook()["Calculator"]
    headers = header_map(ws)
    assert "ActiveOldFarLot" in headers
    assert "ActiveNewFarLot" in headers
    assert "DualTailTotalLot" in headers
    assert ws["BA4"].value == '=IF($AK4=TRUE,MAX(0,$AJ4-$BD4),IF($B4="BLOCKED",MAX(0,$BA3-$BD4),0))'
    assert ws["BB4"].value == '=IF($AK4=TRUE,MAX(0,$AG4-$BE4),IF($B4="BLOCKED",MAX(0,$BB3-$BE4),0))'
    assert ws["BC4"].value == "=$BA4+$BB4"


def test_blocked_rows_keep_dual_tail_total_lot():
    ws = workbook()["Calculator"]
    assert ws["B5"].value.startswith('=IF(AND($AQ4="MANUAL_READY",$BG4="YES")')
    assert ws["BA5"].value == '=IF($AK5=TRUE,MAX(0,$AJ5-$BD5),IF($B5="BLOCKED",MAX(0,$BA4-$BD5),0))'
    assert ws["BB5"].value == '=IF($AK5=TRUE,MAX(0,$AG5-$BE5),IF($B5="BLOCKED",MAX(0,$BB4-$BE5),0))'
    assert ws["BA6"].value == '=IF($AK6=TRUE,MAX(0,$AJ6-$BD6),IF($B6="BLOCKED",MAX(0,$BA5-$BD6),0))'
    assert ws["BB6"].value == '=IF($AK6=TRUE,MAX(0,$AG6-$BE6),IF($B6="BLOCKED",MAX(0,$BB5-$BE6),0))'
    assert ws["BC5"].value == "=$BA5+$BB5"
    assert ws["BC6"].value == "=$BA6+$BB6"


def test_blocked_rows_keep_margin_from_both_tails():
    ws = workbook()["Calculator"]
    assert ws["AB5"].value == '=IF($B5="BLOCKED",$BC5,$D5+$G5+$J5)'
    assert ws["AC5"].value == '=IF($B5="BLOCKED",$BC5,IF($B5="BIG_SIDE",$W5,IF($AK5=TRUE,$BC5,$AG5)))'
    assert ws["AE5"].value == "=$AC5*Settings!$B$10"
    assert ws["AB6"].value == '=IF($B6="BLOCKED",$BC6,$D6+$G6+$J6)'
    assert ws["AC6"].value == '=IF($B6="BLOCKED",$BC6,IF($B6="BIG_SIDE",$W6,IF($AK6=TRUE,$BC6,$AG6)))'
    assert ws["AE6"].value == "=$AC6*Settings!$B$10"


def test_old_tail_cannot_disappear_without_manual_close():
    ws = workbook()["Calculator"]
    assert ws["BD5"].value == 0
    assert "MAX(0,$BA4-$BD5)" in ws["BA5"].value
    assert "MAX(0,$BA5-$BD6)" in ws["BA6"].value


def test_manual_close_reduces_active_tail_lots():
    ws = workbook()["Calculator"]
    assert "MAX(0,$BA4-$BD5)" in ws["BA5"].value
    assert "MAX(0,$BB4-$BE5)" in ws["BB5"].value
    assert ws["AA5"].value == '=IF($B5="BLOCKED",$Z5+$BF5,IF($B5="BIG_SIDE",$Z5+$AX5-$AS5-$AZ5,IF($B5="SMALL_SIDE",$Z5+$S5+$AI5,$Z5+$S5)))'


def test_manual_ready_requires_single_remaining_tail():
    ws = workbook()["Calculator"]
    status_formula = ws["AQ5"].value
    assert 'AND($BA5=0,$BB5>0)' in status_formula
    assert 'AND($BA5>0,$BB5=0)' in status_formula
    assert '"MANUAL_READY"' in status_formula
    assert '"STOP_CLEARED"' in status_formula


def test_new_level_requires_manual_allow_after_dual_tail():
    ws = workbook()["Calculator"]
    assert ws["BG5"].value == "NO"
    assert ws["AP5"].value == '=IF(AND($AQ5="MANUAL_READY",$BG5="YES"),"YES",IF(OR($AQ5="DUAL_TAIL",$AQ5="DANGER",$AQ5="STOP",$AQ5="STOP_CLEARED",$AQ5="MANUAL_READY"),"NO","YES"))'
    assert ws["B6"].value.startswith('=IF(AND($AQ5="MANUAL_READY",$BG5="YES")')
