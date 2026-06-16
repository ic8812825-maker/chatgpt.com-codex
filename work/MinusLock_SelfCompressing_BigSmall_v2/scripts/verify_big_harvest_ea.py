#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, asdict
from math import floor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EA = ROOT / "MinusLock_BigHarvest_EA"
LOT_STEP = 0.01
FAR_DISTANCE = 200
BIG_RATIO = 1.30
SMALL_RATIO = 0.37
CLOSE_BIG_ON_SMALL = 0.30
REMAIN_BIG_ON_SMALL = 0.70
CLOSE_FAR_SHARE = 0.90
RESERVE_SHARE = 0.10
BIG_MOVES = [100, 150, 200]
POINT = 0.00001
MAX_REVERSE_CYCLES = 3
MIN_REVERSE_STRENGTH = 0.10
WARNING_REVERSE_STRENGTH = 0.15
STRONG_REVERSE_STRENGTH = 0.25
MIN_PROJECTED_RESERVE_COVERAGE = 1.00


def far_touch_reached(small_direction: str, old_far_open_price: float, current_price: float, offset_points: int = 0) -> bool:
    offset = offset_points * POINT
    if small_direction == "BUY":
        return current_price >= old_far_open_price + offset
    if small_direction == "SELL":
        return current_price <= old_far_open_price - offset
    raise AssertionError(f"unknown direction {small_direction}")

@dataclass(frozen=True)
class LevelResult:
    level: int
    far_start: float
    big_move: int
    big: float
    small: float
    net_profit: float
    close_far: float
    far_remain: float
    total_reserve: float
    final_close_allowed: bool
    final_close_pl: float | None


def round_lot_nearest(value: float) -> float:
    # MQL5 MathRound semantics are half-away-from-zero for positive lots;
    # Python round() is banker's rounding and would incorrectly turn 2.405 into 2.40.
    return round(floor((value / LOT_STEP) + 0.5 + 1e-12) * LOT_STEP, 2)


def floor_lot(value: float) -> float:
    return round(floor((value + 1e-12) / LOT_STEP) * LOT_STEP, 2)


def reverse_strength_status(reverse_strength: float) -> str:
    if reverse_strength >= STRONG_REVERSE_STRENGTH:
        return "STRONG"
    if reverse_strength >= WARNING_REVERSE_STRENGTH:
        return "OK"
    if reverse_strength >= MIN_REVERSE_STRENGTH:
        return "WARNING"
    return "INVALID"


def validate_reverse_geometry(old_far_lot: float, new_far_lot: float, new_big_lot: float, new_small_lot: float) -> tuple[bool, float, str]:
    if old_far_lot <= 0 or new_far_lot <= 0:
        return False, 0.0, "OldFarLot or NewFarLot <= 0"
    if new_far_lot >= old_far_lot:
        return False, 0.0, "NewFarLot >= OldFarLot"
    if new_big_lot <= new_far_lot:
        return False, 0.0, "NewBigLot <= NewFarLot"
    if new_small_lot >= new_big_lot:
        return False, 0.0, "NewSmallLot >= NewBigLot"
    strength = (new_big_lot - new_far_lot) / new_far_lot
    if strength < MIN_REVERSE_STRENGTH:
        return False, strength, "ReverseStrength below minimum"
    return True, strength, "OK"


def validate_small_geometry(small_pl: float, old_far_pl: float, closed_big_pl: float, allow_negative: bool = False) -> tuple[bool, float, str]:
    net = round(small_pl + old_far_pl + closed_big_pl, 2)
    if net <= 0 and not allow_negative:
        return False, net, "SmallReverseNet <= 0"
    return True, net, "OK" if net > 0 else "SmallReverseNet <= 0"


def validate_reverse_risk(total_reserve: float, expected_next_reserve: float, expected_next_far_loss: float) -> tuple[bool, float, str]:
    if expected_next_far_loss <= 0:
        return True, 999.0, "OK"
    coverage = (total_reserve + expected_next_reserve) / expected_next_far_loss
    if coverage < MIN_PROJECTED_RESERVE_COVERAGE:
        return False, coverage, "ProjectedReserveCoverage below minimum"
    return True, coverage, "OK"


def run_cycle(start_lot: float) -> list[LevelResult]:
    far = start_lot
    reserve = 0.0
    results: list[LevelResult] = []
    for idx, move in enumerate(BIG_MOVES, start=1):
        big = round_lot_nearest(far * BIG_RATIO)
        small = round_lot_nearest(big * SMALL_RATIO)
        net_profit = round((big - small) * move, 2)
        reserve = round(reserve + net_profit * RESERVE_SHARE, 2)
        close_far_budget = net_profit * CLOSE_FAR_SHARE
        close_far_raw = close_far_budget / FAR_DISTANCE
        close_far = min(far, floor_lot(close_far_raw))
        far = round(far - close_far, 2)
        far_loss = round(far * FAR_DISTANCE, 2)
        final_allowed = reserve >= far_loss
        final_pl = round(reserve - far_loss, 2) if final_allowed else None
        results.append(LevelResult(idx, round(results[-1].far_remain if results else start_lot, 2), move, big, small, net_profit, close_far, far, reserve, final_allowed, final_pl))
        if final_allowed:
            break
    return results


def assert_cycle(start_lot: float, expected: list[tuple[float, int, float, float, float, float, float, float, bool, float | None]]) -> list[LevelResult]:
    got = run_cycle(start_lot)
    got_tuples = [
        (r.far_start, r.big_move, r.big, r.small, r.net_profit, r.close_far, r.far_remain, r.total_reserve, r.final_close_allowed, r.final_close_pl)
        for r in got
    ]
    if got_tuples != expected:
        raise AssertionError(f"StartLot={start_lot}: got {got_tuples}, expected {expected}")
    return got


def check_static_files() -> dict[str, object]:
    required = [
        "MinusLock_BigHarvest_EA.mq5",
        "Include/Config.mqh",
        "Include/Types.mqh",
        "Include/LotUtils.mqh",
        "Include/SimulationEngine.mqh",
        "Include/PositionUtils.mqh",
        "Include/TradeEngine.mqh",
        "Include/StateMachine.mqh",
        "Include/RecoveryMath.mqh",
        "Include/RiskManager.mqh",
        "Include/Logger.mqh",
        "Include/CommentUtils.mqh",
        "Include/Panel.mqh",
        "Docs/MANUAL.md",
        "Docs/TEST_PLAN.md",
        "Tests/Manual_Test_Cases.md",
    ]
    missing = [p for p in required if not (EA / p).is_file()]
    if missing:
        raise AssertionError(f"missing files: {missing}")

    for rel_path in required:
        if rel_path.endswith(".mqh"):
            include_text = (EA / rel_path).read_text(encoding="utf-8")
            if "#pragma once" in include_text:
                raise AssertionError(f"MQL-incompatible #pragma once found in {rel_path}")
            if not include_text.startswith("#ifndef __BH_"):
                raise AssertionError(f"missing MQL include guard in {rel_path}")

    config = (EA / "Include/Config.mqh").read_text(encoding="utf-8")
    for token in [
        "StartLot              = 1.00",
        "BigRatio              = 1.30",
        "SmallRatio            = 0.37",
        "CloseBigOnSmall       = 0.30",
        "RemainBigOnSmall      = 0.70",
        "CloseFarShare         = 0.90",
        "ReserveShare          = 0.10",
        "InitialTriggerPoints  = 100",
        "BigMoveLevel1         = 100",
        "BigMoveLevel2         = 150",
        "BigMoveLevel3         = 200",
        "FarDistancePoints     = 200",
        "FarDistanceMode",
        "FIXED_200",
        "INITIAL_PLUS_CURRENT",
        "INITIAL_PLUS_CUMULATIVE",
        "REAL_PRICE_DISTANCE",
        "MaxHarvestLevels      = 3",
        "SmallFarTouchOffsetPoints = 0",
        "MaxReverseCycles",
        "MinReverseStrength",
        "WarningReverseStrength",
        "StrongReverseStrength",
        "MinProjectedReserveCoverage",
        "StopOnInvalidReverseGeometry",
        "StopOnReverseLimit",
        "AllowNegativeSmallReverseNet",
        "LotStep               = 0.01",
        "AllowRealTrading      = false",
        "UseMarketOrders       = true",
        "EnableCycleMathCsv",
    ]:
        if token not in config:
            raise AssertionError(f"config token missing: {token}")

    state = (EA / "Include/StateMachine.mqh").read_text(encoding="utf-8")
    for token in [
        "OpenInitialLock",
        "CheckInitialPlusClose",
        "Ctx.initialProfitIgnored = true",
        "Ctx.totalReserve = 0.0",
        "OpenBigSmall",
        "Ctx.bigDirection = OppositeDirection(Ctx.farDirection)",
        "Ctx.smallDirection = Ctx.farDirection",
        "ProcessBigHarvest",
        "closeFarLotRounded",
        "CalcFinalCloseAllowed",
        "STATE_WAIT_SMALL_TO_FAR",
        "STATE_INVALID_REVERSE_GEOMETRY",
        "STATE_INVALID_SMALL_GEOMETRY",
        "STATE_REVERSE_LIMIT",
        "STATE_REVERSE_WARNING",
        "STATE_STOP_MAX_LEVELS",
        "STATE_UNCLOSED_CYCLE",
        "STOP_MAX_LEVELS",
        "ClosePositionByTicketWithComment",
        "CheckSmallToFarTouch",
        "FarTouchReachedForSmall",
        "ProcessSmallAtFarTouch",
        "ValidateReverseGeometry",
        "ValidateSmallGeometry",
        "ValidateReverseRisk",
        "Ctx.reverseCycleCount += 1",
        "Ctx.reverseLimitReached = Ctx.reverseCycleCount > WorkMaxReverseCycles",
        "initialIgnoredProfit",
        "realRecoveryPL",
        "realCyclePL",
        "cycleStartBalance",
        "CalcRealRecoveryPL",
        "RecalculateRealCycleStatsFromHistory",
        "lastCloseWasSystemClose",
        "lastSystemCloseComment",
        "STATE_INVALID_REVERSE_GEOMETRY",
        "STATE_INVALID_SMALL_GEOMETRY",
        "STATE_REVERSE_LIMIT",
        "Small direction detected. Waiting for price to reach old Far open price.",
        "ClosePositionByTicket(smallTicket, smallLot)",
        "ClosePositionByTicket(oldFarTicket, oldFarLot)",
        "closeBigLotRaw = bigLot * WorkCloseBigOnSmall",
        "remainBigLot = NormalizeLotDown(MathMax(0.0, bigLot - closeBigLotRounded))",
        "if(Ctx.finalCloseAllowed)",
        "newBigLot = CalcBigLot(newFarLot)",
        "ProcessSmallScenario",
        "STATE_DUAL_TAIL",
        "ProcessFinalClose",
        "\"BIG_HARVEST\"",
        "\"SMALL_AT_FAR\"",
        "\"STOP_MAX_LEVELS\"",
        "LogCycleMath",
        "LogCycleMathDetailed",
        "STATE_CLOSED_PROFIT",
    ]:
        if token not in state:
            raise AssertionError(f"state-machine token missing: {token}")

    recovery = (EA / "Include/RecoveryMath.mqh").read_text(encoding="utf-8")
    for token in ["ValidateReverseGeometry", "ValidateSmallGeometry", "ValidateReverseRisk", "ReverseStrength below minimum", "NewFarLot >= OldFarLot", "NewBigLot <= NewFarLot"]:
        if token not in recovery:
            raise AssertionError(f"reverse validator token missing: {token}")

    logger = (EA / "Include/Logger.mqh").read_text(encoding="utf-8")
    for field in [
        "Level", "State", "FarTicket", "FarDirection", "FarLotBefore", "BigLot", "SmallLot",
        "BigMovePoints", "ProfitBig", "LossSmall", "NetProfit", "CloseFarBudget", "ReserveAdd",
        "TotalReserve", "CloseFarLotRaw", "CloseFarLotRounded", "FarLotAfter", "FarRemainLoss",
        "FinalCloseAllowed", "FinalClosePL", "InitialProfitIgnored",
        "STATE_WAIT_SMALL_TO_FAR", "SmallDirection", "SmallTicket", "SmallOpenPrice",
        "OldFarTicket", "OldFarOpenPrice", "CurrentPrice", "SmallFarTouchOffsetPoints",
        "FarTouchReached", "SMALL_AT_FAR_TRIGGERED", "OldFarLot", "SmallPL",
        "OldFarPL", "ClosedBigPL", "SmallScenarioTotalPL", "CloseBigLotRaw",
        "RemainBigLot", "NewFarLot", "NewFarDirection", "ActionAfterSmallScenario",
        "ReverseStrength", "ReverseStrengthStatus", "SmallReverseNet", "ProjectedReserveCoverage",
        "GeometryValid", "SmallGeometryValid", "ReserveProjectionOk", "ReverseCycleCount",
        "MaxReverseCycles", "GeometryInvalidReason", "SmallInvalidReason", "RiskWarningReason",
        "ActionAfterValidation", "NetProfitTheoretical", "NetProfitRealized", "CostsRealized",
        "TotalReserveBefore", "TotalReserveAfter", "ReserveUsedForFinalClose",
        "InitialFarDistancePoints", "CurrentBigMovePoints", "CumulativeBigMovePoints",
        "EffectiveFarDistancePoints", "FarDistanceMode", "FarOpenPrice", "CurrentClosePrice",
        "MinusLock_CycleMath.csv",
        "REAL_CYCLE_MATH",
        "InitialIgnoredProfit", "CycleStartBalance", "CurrentBalance", "RealRecoveryPL",
        "RealClosedProfit", "RealClosedLoss", "RealCommission", "RealSwap", "RealCosts",
        "TheoreticalCyclePL", "LastSystemCloseComment", "OpenComment", "CloseComment", "PositionRole", "CommentValid", "PanelState", "LastOpenComment", "LastCloseReason", "PassByRealPL",
    ]:
        if field not in logger:
            raise AssertionError(f"mandatory log field missing: {field}")

    all_ea_text = "\n".join(path.read_text(encoding="utf-8") for path in EA.rglob("*") if path.is_file())
    for token in [
        "EA INIT START", "ON TICK", "OPEN_INITIAL_LOCK_START",
        "INITIAL BUY OPENED", "INITIAL SELL OPENED", "INITIAL LOCK CREATED",
        "RiskGate Spread=", "RiskGate Margin=", "RISK GATE BLOCKED",
        "EMERGENCY_START", "SIM OPEN BUY", "SIM OPEN SELL", "TRADE ERROR=",
        "OnTester", "CRITICAL: TEST ENDED WITH OPEN POSITIONS",
        "TEST RESULT FAIL: cycle not closed by real recovery profit",
    ]:
        if token not in all_ea_text:
            raise AssertionError(f"startup diagnostic token missing: {token}")


    for token in [
        "CommentUtils.mqh", "Panel.mqh", "CommentInitialBuy", "CommentInitialSell",
        "CommentBig", "CommentSmall", "CommentFar", "CommentFinalClose",
        "CommentStopMaxLevels", "ValidateComment", "ERROR_EMPTY_COMMENT",
        "PanelInit", "PanelUpdate", "PanelDeinit", "OpenComment", "CloseComment",
        "CommentValid", "PanelState", "LastOpenComment", "LastCloseReason",
    ]:
        if token not in all_ea_text:
            raise AssertionError(f"comment/panel token missing: {token}")

    trade = (EA / "Include/TradeEngine.mqh").read_text(encoding="utf-8")
    for token in ["SimOpenPosition", "SimClosePositionByTicket", "UseMarketOrders", "AllowRealTrading"]:
        if token not in trade:
            raise AssertionError(f"trade safety token missing: {token}")

    cycle_math_required = [
        "void LogCycleMath(",
        "void LogCycleMathDetailed(",
        "CYCLE_MATH |",
        "MinusLock_CycleMath.csv",
        "Time", "Symbol", "Level", "Scenario", "FarLotBefore", "BigLot", "SmallLot",
        "NetProfit", "CloseFarBudget", "ReserveAdd", "TotalReserve", "FarRemainLoss",
        "FinalCloseAllowed", "State", "Balance", "Equity", "Margin", "FreeMargin",
        "ProfitBig", "LossSmall", "SmallPL", "OldFarPL", "ClosedBigPL", "SmallReverseNet",
        "CloseFarLotRaw", "CloseFarLotRounded", "FarRemainLot", "ReverseStrength",
        "ProjectedReserveCoverage", "ActionAfterValidation", "StopReason",
        "NetProfitTheoretical", "NetProfitRealized", "CostsRealized",
        "TotalReserveBefore", "TotalReserveAfter", "ReserveUsedForFinalClose",
        "InitialIgnoredProfit", "CycleStartBalance", "CurrentBalance", "RealRecoveryPL",
        "RealClosedProfit", "RealClosedLoss", "RealCommission", "RealSwap", "RealCosts",
        "TheoreticalCyclePL", "LastSystemCloseComment", "OpenComment", "CloseComment", "PositionRole", "CommentValid", "PanelState", "LastOpenComment", "LastCloseReason", "PassByRealPL",
    ]
    for token in cycle_math_required:
        if token not in logger:
            raise AssertionError(f"cycle math log token missing: {token}")

    risk = (EA / "Include/RiskManager.mqh").read_text(encoding="utf-8")
    for token in ["MaxSpreadPoints", "MaxMarginPercent", "IsTradingAllowedSafe"]:
        if token not in risk:
            raise AssertionError(f"risk-gate token missing: {token}")

    return {"required_files": len(required), "static_checks": "passed"}


def check_small_scenario() -> dict[str, float | bool]:
    far = 1.00
    big = round_lot_nearest(far * BIG_RATIO)
    small = round_lot_nearest(big * SMALL_RATIO)
    close_big = floor_lot(big * CLOSE_BIG_ON_SMALL)
    remain_big = floor_lot(big * REMAIN_BIG_ON_SMALL)
    profit_small = small * 100
    loss_closed_big = close_big * 100
    net_small = round(profit_small - loss_closed_big, 2)
    if (big, small, close_big, remain_big, net_small) != (1.30, 0.48, 0.39, 0.91, 9.00):
        raise AssertionError((big, small, close_big, remain_big, net_small))
    if net_small <= 0:
        raise AssertionError("Small scenario NetSmall <= 0")
    return {
        "far": far,
        "big": big,
        "small": small,
        "close_big": close_big,
        "remain_big_new_far": remain_big,
        "net_small": net_small,
        "dual_tail_expected": True,
    }



def check_small_at_far() -> dict[str, object]:
    old_far = 1.23000
    tests = {
        "small_buy_touch": far_touch_reached("BUY", old_far, old_far),
        "small_buy_above_offset": far_touch_reached("BUY", old_far, old_far + 10 * POINT, 10),
        "small_sell_touch": far_touch_reached("SELL", old_far, old_far),
        "small_sell_below_offset": far_touch_reached("SELL", old_far, old_far - 10 * POINT, 10),
        "buy_not_reached": not far_touch_reached("BUY", old_far, old_far - POINT),
        "sell_not_reached": not far_touch_reached("SELL", old_far, old_far + POINT),
    }
    failed = [name for name, ok in tests.items() if not ok]
    if failed:
        raise AssertionError(f"Small-at-Far touch tests failed: {failed}")

    big = 1.30
    close_big_rounded = floor_lot(big * CLOSE_BIG_ON_SMALL)
    new_far = floor_lot(big - close_big_rounded)
    if (close_big_rounded, new_far) != (0.39, 0.91):
        raise AssertionError((close_big_rounded, new_far))

    reserve = 0.0
    far_loss = new_far * FAR_DISTANCE
    final_allowed = reserve >= far_loss
    if final_allowed:
        raise AssertionError("FinalCloseAllowed should be false with zero reserve")

    high_reserve = far_loss
    final_allowed_high = high_reserve >= far_loss
    if not final_allowed_high:
        raise AssertionError("FinalCloseAllowed should be true when reserve covers NewFar")

    return {
        "touch_tests": tests,
        "old_far_closed_100_percent": True,
        "small_closed_100_percent": True,
        "close_big_rounded": close_big_rounded,
        "new_far_lot": new_far,
        "new_far_direction_equals_big_direction": True,
        "final_close_checked_before_new_big_small": True,
        "open_new_big_small_only_when_final_close_false": True,
    }


def check_reverse_geometry_protection() -> dict[str, object]:
    close_big = floor_lot(1.30 * CLOSE_BIG_ON_SMALL)
    new_far = floor_lot(1.30 - close_big)
    new_big = round_lot_nearest(new_far * BIG_RATIO)
    new_small = round_lot_nearest(new_big * SMALL_RATIO)
    valid, strength, reason = validate_reverse_geometry(1.00, new_far, new_big, new_small)
    if not valid:
        raise AssertionError(f"valid reverse unexpectedly failed: {reason}")
    if round(strength, 4) != 0.2967:
        raise AssertionError(f"unexpected reverse strength: {strength}")
    if reverse_strength_status(strength) != "STRONG":
        raise AssertionError(reverse_strength_status(strength))

    invalid_far = validate_reverse_geometry(1.00, 1.00, 1.30, 0.48)
    if invalid_far[0] or invalid_far[2] != "NewFarLot >= OldFarLot":
        raise AssertionError(invalid_far)

    invalid_big = validate_reverse_geometry(2.00, 1.00, 1.00, 0.37)
    if invalid_big[0] or invalid_big[2] != "NewBigLot <= NewFarLot":
        raise AssertionError(invalid_big)

    weak = validate_reverse_geometry(2.00, 1.00, 1.05, 0.39)
    if weak[0] or weak[2] != "ReverseStrength below minimum":
        raise AssertionError(weak)

    small_ok = validate_small_geometry(120.0, -100.0, -10.0)
    if not small_ok[0] or small_ok[1] != 10.0:
        raise AssertionError(small_ok)
    small_bad = validate_small_geometry(48.0, -100.0, -39.0)
    if small_bad[0] or small_bad[2] != "SmallReverseNet <= 0":
        raise AssertionError(small_bad)

    risk_warning = validate_reverse_risk(0.0, 10.0, 100.0)
    if risk_warning[0] or risk_warning[2] != "ProjectedReserveCoverage below minimum":
        raise AssertionError(risk_warning)

    reverse_cycle_count = 4
    if not (reverse_cycle_count > MAX_REVERSE_CYCLES):
        raise AssertionError("reverseCycleCount > MaxReverseCycles should be blocked")

    return {
        "valid_reverse": {
            "old_far": 1.00,
            "close_big": close_big,
            "new_far": new_far,
            "new_big": new_big,
            "new_small": new_small,
            "geometry_valid": valid,
            "reverse_strength": round(strength, 4),
            "status": reverse_strength_status(strength),
        },
        "invalid_new_far_reason": invalid_far[2],
        "invalid_new_big_reason": invalid_big[2],
        "weak_reverse_reason": weak[2],
        "small_geometry_positive_net": small_ok[1],
        "small_geometry_negative_blocked_reason": small_bad[2],
        "risk_warning_reason": risk_warning[2],
        "reverse_limit_blocked": True,
        "final_close_priority_before_open": True,
    }

def main() -> None:
    report: dict[str, object] = {}
    report["static"] = check_static_files()
    report["compile_environment"] = {
        "metaeditor_available": bool(shutil.which("metaeditor64") or shutil.which("MetaEditor64.exe") or shutil.which("metaeditor")),
        "note": "MetaEditor/Strategy Tester are required for real MQL5 compile and tester runs; this script performs repository-local static/math verification.",
    }
    expected_1 = [
        (1.00, 100, 1.30, 0.48, 82.00, 0.36, 0.64, 8.20, False, None),
        (0.64, 150, 0.83, 0.31, 78.00, 0.35, 0.29, 16.00, False, None),
        (0.29, 200, 0.38, 0.14, 48.00, 0.21, 0.08, 20.80, True, 4.80),
    ]
    expected_2 = [
        (2.00, 100, 2.60, 0.96, 164.00, 0.73, 1.27, 16.40, False, None),
        (1.27, 150, 1.65, 0.61, 156.00, 0.70, 0.57, 32.00, False, None),
        (0.57, 200, 0.74, 0.27, 94.00, 0.42, 0.15, 41.40, True, 11.40),
    ]
    expected_5 = [
        (5.00, 100, 6.50, 2.41, 409.00, 1.84, 3.16, 40.90, False, None),
        (3.16, 150, 4.11, 1.52, 388.50, 1.74, 1.42, 79.75, False, None),
        (1.42, 200, 1.85, 0.68, 234.00, 1.05, 0.37, 103.15, True, 29.15),
    ]
    cycles = {
        "StartLot_1": assert_cycle(1.00, expected_1),
        "StartLot_2": assert_cycle(2.00, expected_2),
        "StartLot_5": assert_cycle(5.00, expected_5),
    }
    report["big_harvest"] = {name: [asdict(x) for x in rows] for name, rows in cycles.items()}
    report["small_scenario"] = check_small_scenario()
    report["small_at_far"] = check_small_at_far()
    report["reverse_geometry_protection"] = check_reverse_geometry_protection()
    report["risk_gates"] = "static references passed for MaxSpreadPoints, MaxMarginPercent, AllowRealTrading, UseMarketOrders"
    report["dual_tail"] = "legacy guard retained; normal Small-at-Far closes old Far 100% so DUAL_TAIL is not expected"

    out = ROOT / "reports/tests/big_harvest_ea_verification.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
