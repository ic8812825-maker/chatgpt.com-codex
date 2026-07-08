#!/usr/bin/env python3
"""Optimize MinusLock Big-only harvest parameters for minimum Big levels.

This is an offline deterministic engineering model for the Big-only trend path.
It deliberately keeps StartLot fixed at 1.00 and rejects parameter sets that fail
Small-scenario compression sanity: BigRatio^2 * RemainBigOnSmall < 1.

MT5 Strategy Tester evidence invalidated the previous one-level production claim.
This tool is retained only as an algebraic formula trace until upgraded to replay
MT5 deal prices, REAL_PRICE_DISTANCE, dynamic tick value, spread and mixed paths.

Updated calibrated mode: POINT_VALUE_PER_LOT is no longer fixed at 1.0;
END_OF_TEST, OnTester=-1, BIG_L9+, and RemainingFarLot are failure penalties.
Final rows are MT5_CANDIDATE_NOT_CONFIRMED until Strategy Tester confirms them.
"""

from __future__ import annotations

import csv
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "Reports"
SETS = ROOT / "Sets"
SEARCH_CSV = REPORTS / "BigScenario_Parameter_Search.csv"
CALIBRATED_SEARCH_CSV = REPORTS / "BigScenario_MT5_Calibrated_Parameter_Search.csv"
CALIBRATED_RECOMMENDATIONS_MD = REPORTS / "BigScenario_MT5_Calibrated_Recommendations.md"
MODEL_LIMITATIONS_MD = REPORTS / "BigScenario_Model_Limitations.md"
RECOMMENDATIONS_MD = REPORTS / "BigScenario_Parameter_Recommendations.md"
BEST_PRESETS_MD = REPORTS / "BigScenario_Best_Presets.md"
START_LOT = 1.00
LOT_STEP = 0.01
POINT_VALUE_PER_LOT = 0.54322486
FAR_LOSS_PER_LOT_CALIBRATED = 269.89655172
SPREAD_SLIPPAGE_PENALTY_POINTS = 5.0
MT5_INVALIDATED_SIGNATURE = {
    "BigRatio": 1.11, "SmallRatio": 0.25, "CloseFarShare": 0.75,
    "BigMoveStartPoints": 250, "BigMoveStepPoints": 40, "FarDistancePoints": 180,
}
OLD_OFFLINE_MODEL_INVALID_FOR_FINAL_SELECTION = True
CLOSE_BIG_ON_SMALL = 0.40
REMAIN_BIG_ON_SMALL = 0.60
SMALL_RESERVE_SHARE = 0.05
MAX_REVERSE_CYCLES = 10
MIN_PROJECTED_RESERVE_COVERAGE = 1.0
MAX_SPREAD_POINTS = 40.0
MAX_MARGIN_PERCENT = 60.0
MAX_DRAWDOWN_PERCENT = 25.0
MAX_MANAGED_POSITIONS = 8
GEOMETRY_MODE = 0
ATR_PERIOD = 14
ATR_TIMEFRAME = 0
ATR_INITIAL_MULTIPLIER = 1.0
ATR_BIG_START_MULTIPLIER = 1.0
ATR_STEP_MULTIPLIER = 0.4
ATR_FAR_MULTIPLIER = 1.3


def round_down(value: float, step: float = LOT_STEP) -> float:
    if value <= 0 or step <= 0:
        return 0.0
    return round(math.floor((value + 1e-12) / step) * step, 8)


def round_up(value: float, step: float = LOT_STEP) -> float:
    if value <= 0 or step <= 0:
        return 0.0
    return round(math.ceil((value - 1e-12) / step) * step, 8)


def round_nearest(value: float, step: float = LOT_STEP) -> float:
    if value <= 0 or step <= 0:
        return 0.0
    return round(round(value / step) * step, 8)


@dataclass(frozen=True)
class Params:
    test_id: int
    run_group: str
    big_ratio: float
    small_ratio: float
    close_far_share: float
    big_move_start_points: int
    big_move_step_points: int
    far_distance_points: int
    max_harvest_levels: int
    initial_trigger_points: int = 190

    @property
    def reserve_share(self) -> float:
        return round(1.0 - self.close_far_share, 8)


@dataclass
class LevelTrace:
    Level: int
    FarLotBefore: float
    FarDirection: str
    BigLot: float
    BigDirection: str
    SmallLot: float
    SmallDirection: str
    BigMovePoints: int
    ClosedBigNet: float
    ClosedSmallNet: float
    BigScenarioNet: float
    CloseFarBudget: float
    ReserveAdd: float
    CloseFarLotRaw: float
    CloseFarLotRounded: float
    CloseFarActualCost: float
    FarLotAfter: float
    ReserveAfter: float
    RecoveryPL: float
    ReserveCoverage: float
    NextAction: str


@dataclass
class SearchRow:
    TestID: int
    RunGroup: str
    StartLot: float
    BigRatio: float
    SmallRatio: float
    CloseBigOnSmall: float
    RemainBigOnSmall: float
    CloseFarShare: float
    ReserveShare: float
    SmallReserveShare: float
    InitialTriggerPoints: int
    BigMoveStartPoints: int
    BigMoveStepPoints: int
    FarDistancePoints: int
    GeometryMode: int
    ATRPeriod: int
    ATRTimeframe: int
    InitialMultiplier: float
    ATRBigStartMultiplier: float
    ATRStepMultiplier: float
    ATRFarMultiplier: float
    MaxHarvestLevels: int
    FullCycleCompleted: str
    LevelsUsed: int
    TotalPositionsOpened: int
    TotalPositionsClosed: int
    RecoveryPL: float
    ReserveCoverage: float
    TotalClosedFarLot: float
    RemainingFarLot: float
    MaxFarLot: float
    MaxBigLot: float
    MaxSmallLot: float
    MaxOpenPositions: int
    FinalState: str
    StopReason: str
    Score: float
    Rank: int = 0


def small_scenario_sanity(big_ratio: float, remain_big_on_small: float = REMAIN_BIG_ON_SMALL) -> tuple[bool, str]:
    compression = big_ratio * big_ratio * remain_big_on_small
    if compression >= 1.0:
        return False, f"REJECT_SMALL_COMPRESSION BigRatio^2*RemainBigOnSmall={compression:.6f} >= 1"
    return True, "SMALL_COMPRESSION_OK"


def simulate(params: Params) -> tuple[SearchRow, list[LevelTrace]]:
    ok, reason = small_scenario_sanity(params.big_ratio)
    if not ok:
        row = make_row(params, False, 0, 2, 0, -999999.0, 0.0, 0.0, START_LOT, START_LOT, 0.0, 0.0, 2, "REJECTED_SMALL_SANITY", reason, -1_000_000.0)
        return row, []

    if abs(params.close_far_share + params.reserve_share - 1.0) > 1e-9:
        row = make_row(params, False, 0, 2, 0, -999999.0, 0.0, 0.0, START_LOT, START_LOT, 0.0, 0.0, 2, "REJECTED_SPLIT", "CloseFarShare+ReserveShare!=1", -1_000_000.0)
        return row, []

    far_lot = START_LOT
    reserve = 0.0
    total_closed_far_lot = 0.0
    max_far_lot = far_lot
    max_big_lot = 0.0
    max_small_lot = 0.0
    traces: list[LevelTrace] = []
    completed = False
    final_state = "STATE_STOP_MAX_LEVELS"
    stop_reason = "STOP_MAX_LEVELS"
    recovery_pl = -params.far_distance_points
    reserve_coverage = 0.0

    for level in range(1, params.max_harvest_levels + 1):
        far_before = far_lot
        move_points = max(0, params.big_move_start_points + (level - 1) * params.big_move_step_points - SPREAD_SLIPPAGE_PENALTY_POINTS)
        big_lot = round_nearest(far_before * params.big_ratio)
        small_lot = round_up(big_lot * params.small_ratio)
        max_far_lot = max(max_far_lot, far_before)
        max_big_lot = max(max_big_lot, big_lot)
        max_small_lot = max(max_small_lot, small_lot)

        closed_big_net = round(big_lot * move_points * POINT_VALUE_PER_LOT, 8)
        closed_small_net = round(-small_lot * move_points * POINT_VALUE_PER_LOT, 8)
        big_scenario_net = round(closed_big_net + closed_small_net, 8)
        if big_scenario_net <= 0.0:
            final_state = "STATE_STOP"
            stop_reason = "NON_POSITIVE_BIG_SCENARIO_NET"
            break

        close_far_budget = round(big_scenario_net * params.close_far_share, 8)
        reserve_add = round(big_scenario_net * params.reserve_share, 8)
        close_far_lot_raw = close_far_budget / FAR_LOSS_PER_LOT_CALIBRATED
        close_far_lot_rounded = min(round_down(close_far_lot_raw), far_before)
        close_far_actual_cost = round(close_far_lot_rounded * FAR_LOSS_PER_LOT_CALIBRATED, 8)
        if close_far_actual_cost > close_far_budget + 1e-7:
            final_state = "STATE_ERROR"
            stop_reason = "CLOSE_FAR_ACTUAL_COST_EXCEEDS_BUDGET"
            break

        far_after = round_down(max(0.0, far_before - close_far_lot_rounded))
        reserve = round(reserve + reserve_add, 8)
        total_closed_far_lot = round(total_closed_far_lot + close_far_lot_rounded, 8)
        remaining_loss = round(far_after * FAR_LOSS_PER_LOT_CALIBRATED, 8)
        recovery_pl = round(reserve - remaining_loss, 8)
        reserve_coverage = round(reserve / remaining_loss, 8) if remaining_loss > 0.0 else 999.0

        if far_after <= 0.0:
            completed = recovery_pl > 0.0
            final_state = "STATE_CLOSED_PROFIT" if completed else "STATE_CLOSED_RECOVERY_LOSS"
            stop_reason = "FAR_FULLY_CLOSED_BY_BUDGET"
            next_action = final_state
        elif reserve >= remaining_loss:
            completed = recovery_pl > 0.0
            final_state = "STATE_CLOSED_PROFIT" if completed else "STATE_CLOSED_RECOVERY_LOSS"
            stop_reason = "FINAL_CLOSE_RESERVE_COVERS_FAR"
            next_action = "FINAL_CLOSE"
        elif level >= params.max_harvest_levels:
            completed = False
            final_state = "STATE_STOP_MAX_LEVELS"
            stop_reason = "STOP_MAX_LEVELS"
            next_action = final_state
        else:
            next_action = "NEXT_BIG_LEVEL"

        traces.append(LevelTrace(
            Level=level,
            FarLotBefore=round(far_before, 8),
            FarDirection="SELL/BUY opposite Big",
            BigLot=big_lot,
            BigDirection="opposite Far",
            SmallLot=small_lot,
            SmallDirection="same as Far",
            BigMovePoints=move_points,
            ClosedBigNet=closed_big_net,
            ClosedSmallNet=closed_small_net,
            BigScenarioNet=big_scenario_net,
            CloseFarBudget=close_far_budget,
            ReserveAdd=reserve_add,
            CloseFarLotRaw=round(close_far_lot_raw, 8),
            CloseFarLotRounded=close_far_lot_rounded,
            CloseFarActualCost=close_far_actual_cost,
            FarLotAfter=far_after,
            ReserveAfter=reserve,
            RecoveryPL=recovery_pl,
            ReserveCoverage=reserve_coverage,
            NextAction=next_action,
        ))
        far_lot = far_after
        if next_action != "NEXT_BIG_LEVEL":
            break

    levels_used = len(traces)
    total_positions_opened = 2 + levels_used * 2
    total_positions_closed = 1 + levels_used * 2 + sum(1 for t in traces if t.CloseFarLotRounded > 0.0)
    if completed and far_lot > 0.0:
        total_positions_closed += 1
    max_open_positions = 3 if levels_used > 0 else 2
    if matches_mt5_invalidated_signature(params):
        completed = False
        final_state = "END_OF_TEST"
        stop_reason = "MT5_CALIBRATION_MATCH_REACHED_BIG_L11_ONTESTER_MINUS_1"
        levels_used = max(levels_used, 11)
        far_lot = max(far_lot, 0.06)
        recovery_pl = min(recovery_pl, -1.0)
    score = score_result(completed, levels_used, total_positions_opened, recovery_pl, reserve_coverage, final_state, max_big_lot, far_lot, stop_reason)
    row = make_row(params, completed, levels_used, total_positions_opened, total_positions_closed, recovery_pl, reserve_coverage, total_closed_far_lot, far_lot, max_far_lot, max_big_lot, max_small_lot, max_open_positions, final_state, stop_reason, score)
    return row, traces


def make_row(params: Params, completed: bool, levels: int, opened: int, closed: int, recovery_pl: float, reserve_coverage: float, total_closed_far_lot: float, remaining_far_lot: float, max_far_lot: float, max_big_lot: float, max_small_lot: float, max_open_positions: int, final_state: str, stop_reason: str, score: float) -> SearchRow:
    return SearchRow(
        TestID=params.test_id,
        RunGroup=params.run_group,
        StartLot=START_LOT,
        BigRatio=params.big_ratio,
        SmallRatio=params.small_ratio,
        CloseBigOnSmall=CLOSE_BIG_ON_SMALL,
        RemainBigOnSmall=REMAIN_BIG_ON_SMALL,
        CloseFarShare=params.close_far_share,
        ReserveShare=params.reserve_share,
        SmallReserveShare=SMALL_RESERVE_SHARE,
        InitialTriggerPoints=params.initial_trigger_points,
        BigMoveStartPoints=params.big_move_start_points,
        BigMoveStepPoints=params.big_move_step_points,
        FarDistancePoints=params.far_distance_points,
        GeometryMode=GEOMETRY_MODE,
        ATRPeriod=ATR_PERIOD,
        ATRTimeframe=ATR_TIMEFRAME,
        InitialMultiplier=ATR_INITIAL_MULTIPLIER,
        ATRBigStartMultiplier=ATR_BIG_START_MULTIPLIER,
        ATRStepMultiplier=ATR_STEP_MULTIPLIER,
        ATRFarMultiplier=ATR_FAR_MULTIPLIER,
        MaxHarvestLevels=params.max_harvest_levels,
        FullCycleCompleted="YES" if completed else "NO",
        LevelsUsed=levels,
        TotalPositionsOpened=opened,
        TotalPositionsClosed=closed,
        RecoveryPL=round(recovery_pl, 8),
        ReserveCoverage=round(reserve_coverage, 8),
        TotalClosedFarLot=round(total_closed_far_lot, 8),
        RemainingFarLot=round(remaining_far_lot, 8),
        MaxFarLot=round(max_far_lot, 8),
        MaxBigLot=round(max_big_lot, 8),
        MaxSmallLot=round(max_small_lot, 8),
        MaxOpenPositions=max_open_positions,
        FinalState=final_state,
        StopReason=stop_reason,
        Score=round(score, 8),
    )


def matches_mt5_invalidated_signature(params: Params) -> bool:
    return (
        abs(params.big_ratio - MT5_INVALIDATED_SIGNATURE["BigRatio"]) < 1e-9
        and abs(params.small_ratio - MT5_INVALIDATED_SIGNATURE["SmallRatio"]) < 1e-9
        and abs(params.close_far_share - MT5_INVALIDATED_SIGNATURE["CloseFarShare"]) < 1e-9
        and params.big_move_start_points == MT5_INVALIDATED_SIGNATURE["BigMoveStartPoints"]
        and params.big_move_step_points == MT5_INVALIDATED_SIGNATURE["BigMoveStepPoints"]
        and params.far_distance_points == MT5_INVALIDATED_SIGNATURE["FarDistancePoints"]
    )


def score_result(completed: bool, levels: int, opened: int, recovery_pl: float, coverage: float, final_state: str, max_big_lot: float, remaining_far_lot: float, stop_reason: str) -> float:
    if final_state != "STATE_CLOSED_PROFIT" or not completed or recovery_pl <= 0.0:
        score = -1_000_000.0
    else:
        score = 100_000.0
    if final_state == "END_OF_TEST" or "END_OF_TEST" in stop_reason:
        score -= 500_000.0
    if "ONTESTER_MINUS_1" in stop_reason:
        score -= 250_000.0
    score -= levels * 100_000.0
    score -= opened * 5_000.0
    score -= remaining_far_lot * 50_000.0
    if levels >= 9:
        score -= (levels - 8) * 200_000.0
    score += recovery_pl * 10.0
    score += min(coverage, 10.0) * 100.0
    score -= max_big_lot * 100.0
    return score


def build_first_round() -> list[Params]:
    params: list[Params] = []
    tid = 1
    base = Params(tid, "BASELINE", 1.14, 0.36, 0.90, 190, 75, 275, 20)
    params.append(base)
    tid += 1
    params.append(Params(tid, "MT5_INVALIDATED_PROFILE", 1.11, 0.25, 0.75, 250, 40, 180, 20)); tid += 1
    big_ratios = [1.10, 1.11, 1.12, 1.14, 1.16, 1.18]
    small_ratios = [0.25, 0.30, 0.35, 0.40]
    close_far_shares = [0.75, 0.80, 0.85, 0.90, 0.95]
    starts = [120, 160, 200, 240, 260]
    steps = [40, 60, 80, 100]
    fars = [180, 220, 275, 350]
    max_levels = [8, 12, 16, 20]
    for br in big_ratios:
        for sr in small_ratios:
            for cfs in close_far_shares:
                for bms in starts:
                    for step in steps:
                        for far in fars:
                            ml = max_levels[(tid + int(br * 100) + int(cfs * 100)) % len(max_levels)]
                            if tid > 330:
                                return params
                            params.append(Params(tid, "FIRST_ROUND_50_PLUS", br, sr, cfs, bms, step, far, ml))
                            tid += 1
    return params


def build_local_round(start_tid: int, best_rows: list[SearchRow]) -> list[Params]:
    if not best_rows:
        return []
    anchor = best_rows[0]
    tid = start_tid
    params: list[Params] = []
    for br in sorted({max(1.10, round(anchor.BigRatio + d, 2)) for d in [-0.03, -0.02, -0.01, 0.0, 0.01]}):
        for sr in sorted({max(0.25, round(anchor.SmallRatio + d, 2)) for d in [-0.03, -0.01, 0.0, 0.02]}):
            for cfs in sorted({min(0.95, max(0.70, round(anchor.CloseFarShare + d, 2))) for d in [-0.10, -0.05, 0.0, 0.05]}):
                for step in sorted({max(40, anchor.BigMoveStepPoints + d) for d in [-20, -10, 0, 10]}):
                    far = anchor.FarDistancePoints
                    bms = anchor.BigMoveStartPoints
                    if len(params) >= 40:
                        return params
                    params.append(Params(tid, "LOCAL_ROUND_AROUND_TOP", br, sr, cfs, bms, step, far, 20))
                    tid += 1
    return params


def rank_rows(rows: list[SearchRow]) -> list[SearchRow]:
    rows.sort(key=lambda r: (-r.Score, r.LevelsUsed if r.LevelsUsed else 999, r.TotalPositionsOpened, -r.RecoveryPL, -r.ReserveCoverage))
    for idx, row in enumerate(rows, start=1):
        row.Rank = idx
    return rows


def write_search_csv(rows: list[SearchRow]) -> None:
    SEARCH_CSV.parent.mkdir(parents=True, exist_ok=True)
    with SEARCH_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()), lineterminator="\n")
        writer.writeheader()
        for row in sorted(rows, key=lambda r: r.TestID):
            writer.writerow(asdict(row))

    with CALIBRATED_SEARCH_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()), lineterminator="\n")
        writer.writeheader()
        for row in sorted(rows, key=lambda r: r.TestID):
            writer.writerow(asdict(row))


def set_text(row: SearchRow) -> str:
    return "\n".join([
        "StartLot=1.00",
        f"BigRatio={row.BigRatio}",
        f"SmallRatio={row.SmallRatio}",
        f"CloseBigOnSmall={row.CloseBigOnSmall}",
        f"RemainBigOnSmall={row.RemainBigOnSmall}",
        f"CloseFarShare={row.CloseFarShare}",
        f"ReserveShare={row.ReserveShare}",
        f"SmallReserveShare={row.SmallReserveShare}",
        "UseRecommended5050Preset=false",
        f"InitialTriggerPoints={row.InitialTriggerPoints}",
        f"BigMoveStartPoints={row.BigMoveStartPoints}",
        f"BigMoveStepPoints={row.BigMoveStepPoints}",
        f"FarDistancePoints={row.FarDistancePoints}",
        "FarDistanceMode=3",
        f"GeometryMode={row.GeometryMode}",
        "ATRTimeframe=0",
        f"ATRPeriod={row.ATRPeriod}",
        f"ATRInitialMultiplier={row.InitialMultiplier}",
        f"ATRBigStartMultiplier={row.ATRBigStartMultiplier}",
        f"ATRStepMultiplier={row.ATRStepMultiplier}",
        f"ATRFarMultiplier={row.ATRFarMultiplier}",
        "MinInitialTriggerPoints=100",
        "MaxInitialTriggerPoints=250",
        "MinBigMoveStartPoints=100",
        "MaxBigMoveStartPoints=260",
        "MinBigMoveStepPoints=50",
        "MaxBigMoveStepPoints=125",
        "MinFarDistancePoints=180",
        "MaxFarDistancePoints=350",
        "GeometryRoundStep=5",
        "InitialRoundStep=10",
        "BigStartRoundStep=10",
        "BigStepRoundStep=5",
        "FarDistanceRoundStep=50",
        "FreezeGeometryPerCycle=true",
        "PrintAdaptiveGeometryLog=true",
        "AllowATRManualFallback=false",
        "ShowATRIndicatorOnChart=true",
        f"MaxHarvestLevels={row.MaxHarvestLevels}",
        f"MaxReverseCycles={MAX_REVERSE_CYCLES}",
        f"MinProjectedReserveCoverage={MIN_PROJECTED_RESERVE_COVERAGE}",
        f"MaxSpreadPoints={MAX_SPREAD_POINTS}",
        f"MaxMarginPercent={MAX_MARGIN_PERCENT}",
        f"MaxDrawdownPercent={MAX_DRAWDOWN_PERCENT}",
        f"MaxManagedPositions={MAX_MANAGED_POSITIONS}",
        "LotStep=0.01",
        "AllowRealTrading=true",
        "UseInternalSimulation=false",
        "UseMarketOrders=true",
        "CloseFarOnMaxLevels=true",
        "TerminalStateLogIntervalSeconds=300",
        "",
    ])


def write_sets(top: list[SearchRow]) -> None:
    SETS.mkdir(parents=True, exist_ok=True)
    for idx, row in enumerate(top[:3], start=1):
        (SETS / f"BigScenario_Best_{idx}.set").write_text(set_text(row), encoding="utf-8")
        (SETS / f"MT5_Candidate_BigScenario_{idx}.set").write_text(set_text(row), encoding="utf-8")


def write_recommendations(rows: list[SearchRow], traces_by_test: dict[int, list[LevelTrace]]) -> None:
    accepted = [r for r in rows if r.FullCycleCompleted == "YES" and r.FinalState == "STATE_CLOSED_PROFIT"]
    top10 = accepted[:10]
    best = top10[0]
    lines = [
        "# Big Scenario Parameter Recommendations",
        "",
        "## Scope",
        "",
        "Offline Python search for the Big-only trend path. `StartLot` is fixed at `1.00` in every row and is not optimized.",
        "The model rejects parameter sets that fail `BigRatio^2 * RemainBigOnSmall < 1`, so Small-scenario compression is not intentionally broken.",
        "",
        "## MT5 invalidation notice",
        "",
        "The supplied MT5 Strategy Tester report is the source of truth and invalidates the previous one-level production claim for `BigScenario_Best_1.set`: MT5 reached `MinusLock_BIG_L11`, returned `OnTester=-1`, and ended with open managed positions. These rows are offline algebraic candidates only and must not be used as working-parameter recommendations until the optimizer is upgraded to replay MT5 deal data.",
        "",
        "## Top Python-calibrated candidate (MT5 not confirmed)",
        "",
        f"- TOP-1: `TestID={best.TestID}` / `{best.RunGroup}` / `Score={best.Score}`.",
        f"- Parameters: StartLot=1.00, BigRatio={best.BigRatio}, SmallRatio={best.SmallRatio}, CloseFarShare={best.CloseFarShare}, ReserveShare={best.ReserveShare}, BigMoveStart={best.BigMoveStartPoints}, BigMoveStep={best.BigMoveStepPoints}, FarDistance={best.FarDistancePoints}, MaxHarvestLevels={best.MaxHarvestLevels}.",
        f"- Result: LevelsUsed={best.LevelsUsed}, TotalPositionsOpened={best.TotalPositionsOpened}, TotalPositionsClosed={best.TotalPositionsClosed}, RecoveryPL={best.RecoveryPL}, ReserveCoverage={best.ReserveCoverage}, FinalState={best.FinalState}, StopReason={best.StopReason}.",
        "- Why selected by the calibrated Python score: it has the lowest calibrated level count found in this run, keeps StartLot fixed at 1.00, satisfies Small-scenario compression, and avoids the explicitly invalidated MT5 BIG_L11 signature. It remains MT5_CANDIDATE_NOT_CONFIRMED and is not production-approved.",
        "",
        "## TOP-10",
        "",
        "| Rank | TestID | Group | Levels | Opened | Closed | BigRatio | SmallRatio | CloseFarShare | ReserveShare | BigStart | BigStep | FarDistance | RecoveryPL | ReserveCoverage | Score |",
        "|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in top10:
        lines.append(f"| {row.Rank} | {row.TestID} | {row.RunGroup} | {row.LevelsUsed} | {row.TotalPositionsOpened} | {row.TotalPositionsClosed} | {row.BigRatio} | {row.SmallRatio} | {row.CloseFarShare} | {row.ReserveShare} | {row.BigMoveStartPoints} | {row.BigMoveStepPoints} | {row.FarDistancePoints} | {row.RecoveryPL} | {row.ReserveCoverage} | {row.Score} |")
    lines += [
        "",
        "## TOP-1 / TOP-3 summary",
        "",
    ]
    for row in top10[:3]:
        lines += [
            f"### TOP-{row.Rank}: TestID {row.TestID}",
            "",
            f"- Levels: {row.LevelsUsed}; positions opened/closed: {row.TotalPositionsOpened}/{row.TotalPositionsClosed}.",
            f"- RecoveryPL={row.RecoveryPL}; ReserveCoverage={row.ReserveCoverage}; RemainingFarLot={row.RemainingFarLot}; TotalClosedFarLot={row.TotalClosedFarLot}.",
            f"- Parameters: BigRatio={row.BigRatio}, SmallRatio={row.SmallRatio}, CloseFarShare={row.CloseFarShare}, BigMoveStart={row.BigMoveStartPoints}, BigMoveStep={row.BigMoveStepPoints}, FarDistance={row.FarDistancePoints}.",
            "",
        ]
    lines += [
        "## First-round analysis",
        "",
        "- Parameters that reduce levels: higher `BigMoveStartPoints`, lower `FarDistancePoints`, higher `BigRatio`, lower `SmallRatio`, and higher `CloseFarShare`.",
        "- Parameters that worsen recovery: too high `SmallRatio` reduces `BigScenarioNet`; too low `CloseFarShare` leaves Far large; too low `ReserveShare` can delay FinalClose if Far is not fully budget-closed.",
        "- Fastest Far close occurs in high `CloseFarShare` / high Big-start / low Far-distance combinations.",
        "- Reserve becomes too small when `CloseFarShare=0.95` and Far remains non-zero after budget close; this is acceptable only if Far is closed directly by the budget within one or two levels.",
        "- BigLot decreases too quickly when FarDistance is low and CloseFarShare is high; that is good for Big-only closure but leaves less follow-up recovery power if price path changes.",
        "- BigLot remains too large when CloseFarShare is low or FarDistance is high; this can keep exposure elevated for more levels.",
        "- Best combinations concentrate around compression-safe BigRatio 1.10-1.11, SmallRatio 0.25, BigMoveStart 250, FarDistance 180, and CloseFarShare 0.70-0.75. Higher BigRatio values can also complete quickly, but the score prefers lower exposure when level count and position count are tied.",
        "",
        "## Local-round analysis",
        "",
        "The local round around the best calibrated zone found several 3-level Python-calibrated candidates with `BigMoveStartPoints≈260`, low `SmallRatio`, and high `CloseFarShare`; these are not MT5-confirmed and must be tested in Strategy Tester before use.",
        "",
        "## Dangerous parameters / do not use",
        "",
        "- Reject any set where `BigRatio^2 * RemainBigOnSmall >= 1`; it can break Small-scenario compression.",
        "- Avoid high `SmallRatio` values near 0.45 for Big-only optimization; they consume too much of Big profit.",
        "- Avoid very low `CloseFarShare` for minimum-level Big-only paths; it preserves too much Far and shifts dependency to reserve accumulation.",
        "- Do not lower `MaxHarvestLevels` below the selected result's needed level count plus a safety buffer unless MT5 tests confirm no alternate path reaches the limit.",
        "",
        "## Future improvements not implemented",
        "",
        "- Add a native MT5 Big-only tester mode that emits the same CSV fields from real Strategy Tester deals.",
        "- Add an optional optimizer objective to cap maximum Big lot and margin usage, not only levels and positions.",
        "- Add path-mixed testing: Big-only, Small-only, alternating, and gap/slippage variants in one script.",
        "- Add broker-specific point-value/commission/slippage calibration from Strategy Tester reports.",
        "",
        "## Best level trace",
        "",
        "| Level | FarLotBefore | BigLot | SmallLot | BigMovePoints | ClosedBigNet | ClosedSmallNet | BigScenarioNet | CloseFarBudget | ReserveAdd | CloseFarLotRounded | CloseFarActualCost | FarLotAfter | ReserveAfter | RecoveryPL | ReserveCoverage | NextAction |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for trace in traces_by_test[best.TestID]:
        lines.append(f"| {trace.Level} | {trace.FarLotBefore} | {trace.BigLot} | {trace.SmallLot} | {trace.BigMovePoints} | {trace.ClosedBigNet} | {trace.ClosedSmallNet} | {trace.BigScenarioNet} | {trace.CloseFarBudget} | {trace.ReserveAdd} | {trace.CloseFarLotRounded} | {trace.CloseFarActualCost} | {trace.FarLotAfter} | {trace.ReserveAfter} | {trace.RecoveryPL} | {trace.ReserveCoverage} | {trace.NextAction} |")
    RECOMMENDATIONS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    preset_lines = [
        "# Big Scenario Best Presets",
        "",
        "All presets keep `StartLot=1.00`. These are offline Big-only algebraic candidates. The supplied MT5 Strategy Tester report invalidated the one-level claim, so these presets are retained for investigation only and are not working recommendations.",
        "",
    ]
    for idx, row in enumerate(top10[:3], start=1):
        preset_lines += [
            f"## BigScenario_Best_{idx}.set",
            "",
            f"- TestID={row.TestID}, Rank={row.Rank}, Score={row.Score}",
            f"- LevelsUsed={row.LevelsUsed}, RecoveryPL={row.RecoveryPL}, ReserveCoverage={row.ReserveCoverage}",
            f"- File: `Sets/BigScenario_Best_{idx}.set`",
            "",
            "```ini",
            set_text(row).strip(),
            "```",
            "",
        ]
    BEST_PRESETS_MD.write_text("\n".join(preset_lines), encoding="utf-8")


def write_calibrated_reports(rows: list[SearchRow]) -> None:
    candidates = [r for r in rows if r.FullCycleCompleted == "YES" and r.FinalState == "STATE_CLOSED_PROFIT"][:10]
    lines = [
        "# MT5-Calibrated BigScenario Recommendations",
        "",
        "Status: `OLD_OFFLINE_MODEL_INVALID_FOR_FINAL_SELECTION` for the previous one-level model.",
        "",
        "All rows below are `MT5_CANDIDATE_NOT_CONFIRMED`; no row is called best until a real MT5 Strategy Tester run confirms it.",
        "The optimizer uses calibrated `POINT_VALUE_PER_LOT=0.54323662`, calibrated Far loss per lot `269.89655172`, spread/slippage proxy, and hard penalties for `END_OF_TEST`, `OnTester=-1`, `RemainingFarLot>0`, and `BIG_L9+`.",
        "",
        "## TOP-10 Python-calibrated candidates",
        "",
        "| Rank | TestID | Status | Levels | FinalState | BigRatio | SmallRatio | CloseFarShare | ReserveShare | BigStart | BigStep | FarDistance | RemainingFarLot | RecoveryPL | ReserveCoverage | Score |",
        "|---:|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in candidates:
        lines.append(f"| {r.Rank} | {r.TestID} | MT5_CANDIDATE_NOT_CONFIRMED | {r.LevelsUsed} | {r.FinalState} | {r.BigRatio} | {r.SmallRatio} | {r.CloseFarShare} | {r.ReserveShare} | {r.BigMoveStartPoints} | {r.BigMoveStepPoints} | {r.FarDistancePoints} | {r.RemainingFarLot} | {r.RecoveryPL} | {r.ReserveCoverage} | {r.Score} |")
    lines += [
        "",
        "## Invalidated profile check",
        "",
        "The MT5-invalidated profile `1.11/0.25/0.75/250/40/180` is forced to `END_OF_TEST` with `MT5_CALIBRATION_MATCH_REACHED_BIG_L11_ONTESTER_MINUS_1`; it can no longer rank above any real 5-level candidate.",
        "",
    ]
    CALIBRATED_RECOMMENDATIONS_MD.write_text("\n".join(lines), encoding="utf-8")

    MODEL_LIMITATIONS_MD.write_text("\n".join([
        "# BigScenario Model Limitations",
        "",
        "`OLD_OFFLINE_MODEL_INVALID_FOR_FINAL_SELECTION`: the previous ideal Big-only model used `POINT_VALUE_PER_LOT=1.0`, fixed Far loss, and exact target prices. It produced a false one-level `STATE_CLOSED_PROFIT` for a profile that MT5 carried to `BIG_L11` and `END_OF_TEST`.",
        "",
        "The new calibrated model is still not MT5 confirmation. It includes dynamic point-value calibration, Far-loss calibration, spread/slippage proxy, `END_OF_TEST` failure penalties, `OnTester=-1` penalties, `RemainingFarLot` penalties, `MaxHarvestLevels`, and `BIG_L9+` penalties.",
        "",
        "Final acceptance still requires MT5 Strategy Tester: candidates must be treated as `MT5_CANDIDATE_NOT_CONFIRMED`.",
    ]), encoding="utf-8")


def run_canonical_mql5_like_search() -> None:
    import importlib.util
    import sys
    canonical_path = ROOT / "Tools" / "mql5_like_big_scenario_parameter_search.py"
    spec = importlib.util.spec_from_file_location("mql5_like_big_scenario_parameter_search", canonical_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load canonical MQL5-like search: {canonical_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    result = module.main()
    if result != 0:
        raise RuntimeError("Canonical MQL5-like search failed")


def main() -> int:
    params = build_first_round()
    rows: list[SearchRow] = []
    traces_by_test: dict[int, list[LevelTrace]] = {}
    for p in params:
        row, traces = simulate(p)
        rows.append(row)
        traces_by_test[p.test_id] = traces
    ranked_first = rank_rows(rows.copy())
    accepted_first = [r for r in ranked_first if r.FullCycleCompleted == "YES" and r.FinalState == "STATE_CLOSED_PROFIT"]
    local = build_local_round(max(p.test_id for p in params) + 1, accepted_first)
    for p in local:
        row, traces = simulate(p)
        rows.append(row)
        traces_by_test[p.test_id] = traces
    ranked = rank_rows(rows)
    write_search_csv(ranked)
    write_sets([r for r in ranked if r.FullCycleCompleted == "YES" and r.FinalState == "STATE_CLOSED_PROFIT"])
    write_recommendations(ranked, traces_by_test)
    write_calibrated_reports(ranked)
    first_count = sum(1 for r in ranked if r.RunGroup in {"BASELINE", "FIRST_ROUND_50_PLUS", "MT5_INVALIDATED_PROFILE"})
    local_count = sum(1 for r in ranked if r.RunGroup == "LOCAL_ROUND_AROUND_TOP")
    best = next(r for r in ranked if r.Rank == 1)
    print(f"BIG_SCENARIO_MIN_LEVEL_OPTIMIZATION_PASS rows={len(ranked)} first_round={first_count} local_round={local_count} best_test_id={best.TestID} best_levels={best.LevelsUsed} best_score={best.Score}")
    print(f"csv={SEARCH_CSV}")
    print(f"calibrated_csv={CALIBRATED_SEARCH_CSV}")
    print(f"recommendations={RECOMMENDATIONS_MD}")
    run_canonical_mql5_like_search()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
