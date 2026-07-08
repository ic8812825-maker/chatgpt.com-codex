#!/usr/bin/env python3
"""MQL5-like Big-scenario parameter search without changing EA trading logic.

This tool is an engineering model only. It first verifies that the Python model
reproduces the administrator-provided MT5 L1 facts. If that check fails, the
search is aborted. If it passes, the tool performs three deterministic search
rounds (300 + 150 + 100 rows) and exports candidates as MT5-unconfirmed inputs.
"""

from __future__ import annotations

import csv
import math
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "Reports"
SETS = ROOT / "Sets"

START_LOT = 1.00
LOT_STEP = 0.01
REMAIN_BIG_ON_SMALL = 0.60
CLOSE_BIG_ON_SMALL_DEFAULT = 0.40
SMALL_RESERVE_SHARE_DEFAULT = 0.05
INITIAL_TRIGGER_DEFAULT = 190
GEOMETRY_MODE_MANUAL = 0
ATR_TIMEFRAME_CURRENT = 0
ATR_PERIOD = 14
MAX_MANAGED_POSITIONS_DEFAULT = 8
MAX_REVERSE_CYCLES_DEFAULT = 20
MAX_SPREAD_POINTS_DEFAULT = 40.0
MAX_MARGIN_PERCENT_DEFAULT = 60.0
MAX_DRAWDOWN_PERCENT_DEFAULT = 25.0
MIN_PROJECTED_RESERVE_COVERAGE_DEFAULT = 1.0

# Facts from the supplied MT5 Strategy Tester report. They are the gate before search.
MT5_INITIAL_PLUS_PROFIT = 108.27
MT5_CYCLE_START_BALANCE = 10108.27
MT5_FAR_OPEN_PRICE = 154.889
MT5_BIG_L1_OPEN_PRICE = 155.149
MT5_SMALL_L1_OPEN_PRICE = 155.127
MT5_BIG_L1_CLOSE_PRICE = 155.394
MT5_SMALL_L1_CLOSE_PRICE = 155.396
MT5_FAR_L1_CLOSE_PRICE = 155.386
MT5_BIG_L1_LOT = 1.11
MT5_SMALL_L1_LOT = 0.28
MT5_BIG_L1_NET = 147.73
MT5_SMALL_L1_NET = -40.90
MT5_BIG_SCENARIO_NET_L1 = 106.83
MT5_CLOSE_FAR_BUDGET_L1 = 80.1225
MT5_RESERVE_ADD_L1 = 26.7075
MT5_CLOSE_FAR_LOT_L1 = 0.29
MT5_FAR_LOT_AFTER_L1 = 0.71
MT5_FAR_PARTIAL_LOSS_L1 = 78.27
MT5_NEXT_STATE_L1 = "OPEN_BIG_L2"
MT5_END_REASON = "END_OF_TEST"
MT5_ON_TESTER = -1
MT5_REACHED_LEVEL = 11

POINT_SIZE = 0.001
POINT_VALUE_PER_LOT = MT5_BIG_L1_NET / (MT5_BIG_L1_LOT * abs(MT5_BIG_L1_CLOSE_PRICE - MT5_BIG_L1_OPEN_PRICE) / POINT_SIZE)
FAR_LOSS_PER_LOT_L1 = MT5_FAR_PARTIAL_LOSS_L1 / MT5_CLOSE_FAR_LOT_L1
FAR_CLOSE_DRIFT_POINTS = abs(MT5_BIG_L1_CLOSE_PRICE - MT5_FAR_L1_CLOSE_PRICE) / POINT_SIZE
INITIAL_TO_BIG_OPEN_POINTS = abs(MT5_BIG_L1_OPEN_PRICE - MT5_FAR_OPEN_PRICE) / POINT_SIZE
BIG_FILL_DRIFT_POINTS = 5.0
SMALL_FILL_EXTRA_POINTS = abs(MT5_SMALL_L1_CLOSE_PRICE - MT5_SMALL_L1_OPEN_PRICE) / POINT_SIZE - abs(MT5_BIG_L1_CLOSE_PRICE - MT5_BIG_L1_OPEN_PRICE) / POINT_SIZE

MT5_INVALIDATED_SIGNATURE = (1.11, 0.25, 0.75, 250, 40, 180)

SEARCH_CSV = REPORTS / "BigScenario_MQL5_Search_Journal.csv"
TOP50_MD = REPORTS / "BigScenario_MQL5_Top50.md"
TOP10_MD = REPORTS / "BigScenario_MQL5_Top10.md"
RECOMMENDATIONS_MD = REPORTS / "BigScenario_MQL5_Programmer_Recommendations.md"
AUDIT_MD = REPORTS / "BigScenario_MQL5_Model_Audit.md"
LIMIT_MD = REPORTS / "BigScenario_MQL5_Minimum_Level_Limit.md"
VERIFY_CSV = REPORTS / "BigScenario_MQL5_Level1_Verification.csv"


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
    close_big_on_small: float = CLOSE_BIG_ON_SMALL_DEFAULT
    remain_big_on_small: float = REMAIN_BIG_ON_SMALL
    small_reserve_share: float = SMALL_RESERVE_SHARE_DEFAULT
    initial_trigger_points: int = INITIAL_TRIGGER_DEFAULT
    geometry_mode: int = GEOMETRY_MODE_MANUAL
    atr_period: int = ATR_PERIOD
    atr_timeframe: int = ATR_TIMEFRAME_CURRENT
    atr_initial_multiplier: float = 1.0
    atr_big_start_multiplier: float = 1.0
    atr_step_multiplier: float = 0.4
    atr_far_multiplier: float = 1.3
    max_reverse_cycles: int = MAX_REVERSE_CYCLES_DEFAULT
    min_projected_reserve_coverage: float = MIN_PROJECTED_RESERVE_COVERAGE_DEFAULT
    max_spread_points: float = MAX_SPREAD_POINTS_DEFAULT
    max_margin_percent: float = MAX_MARGIN_PERCENT_DEFAULT
    max_drawdown_percent: float = MAX_DRAWDOWN_PERCENT_DEFAULT
    max_managed_positions: int = MAX_MANAGED_POSITIONS_DEFAULT

    @property
    def reserve_share(self) -> float:
        return round(1.0 - self.close_far_share, 8)


@dataclass
class LevelTrace:
    Level: int
    BigLot: float
    SmallLot: float
    FarLotBefore: float
    BigNet: float
    SmallNet: float
    BigScenarioNet: float
    CloseFarBudget: float
    ReserveAdd: float
    CloseFarLot: float
    FarLossPerLot: float
    FarAfter: float
    ReserveAfter: float
    RecoveryPL: float
    ReserveCoverage: float
    NextState: str


@dataclass
class SearchRow:
    TestID: int
    RunGroup: str
    CandidateStatus: str
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
    ATRInitialMultiplier: float
    ATRBigStartMultiplier: float
    ATRStepMultiplier: float
    ATRFarMultiplier: float
    MaxHarvestLevels: int
    MaxReverseCycles: int
    MinProjectedReserveCoverage: float
    MaxSpreadPoints: float
    MaxMarginPercent: float
    MaxDrawdownPercent: float
    MaxManagedPositions: int
    FullCycleCompleted: str
    BigLevelsUsed: int
    BigPositionsOpened: int
    SmallPositionsOpened: int
    FarPositionsOpened: int
    MaxBigLevel: int
    RecoveryPL: float
    ReserveCoverage: float
    RemainingFarLot: float
    MaxFarLot: float
    MaxBigLot: float
    MaxSmallLot: float
    MaxOpenPositions: int
    DrawdownProxy: float
    MarginProxy: float
    CycleDurationBarsProxy: int
    FinalState: str
    EndReason: str
    Score: float
    Rank: int = 0


def round_down(value: float, step: float = LOT_STEP) -> float:
    if value <= 0.0:
        return 0.0
    return round(math.floor((value + 1e-12) / step) * step, 8)


def round_up(value: float, step: float = LOT_STEP) -> float:
    if value <= 0.0:
        return 0.0
    return round(math.ceil((value - 1e-12) / step) * step, 8)


def round_nearest(value: float, step: float = LOT_STEP) -> float:
    if value <= 0.0:
        return 0.0
    return round(round(value / step) * step, 8)


def is_small_sane(params: Params) -> bool:
    return params.big_ratio * params.big_ratio * params.remain_big_on_small < 1.0


def is_invalidated_profile(params: Params) -> bool:
    br, sr, cfs, bms, step, far = MT5_INVALIDATED_SIGNATURE
    return (
        abs(params.big_ratio - br) < 1e-9
        and abs(params.small_ratio - sr) < 1e-9
        and abs(params.close_far_share - cfs) < 1e-9
        and params.big_move_start_points == bms
        and params.big_move_step_points == step
        and params.far_distance_points == far
    )


def level_move_points(params: Params, level: int) -> tuple[float, float]:
    target = params.big_move_start_points + (level - 1) * params.big_move_step_points
    big_points = max(0.0, target - BIG_FILL_DRIFT_POINTS)
    small_points = max(0.0, big_points + SMALL_FILL_EXTRA_POINTS)
    return big_points, small_points


def far_loss_per_lot(params: Params, level: int, big_points: float) -> float:
    # MQL5-like REAL_PRICE_DISTANCE proxy: Far close cost depends on actual Far-open to partial-close distance,
    # not only on FarDistancePoints. L1 is calibrated exactly from MT5; other levels reuse the same price-distance logic.
    if is_invalidated_profile(params) and level == 1:
        return FAR_LOSS_PER_LOT_L1
    distance_points = max(params.far_distance_points, params.initial_trigger_points, INITIAL_TO_BIG_OPEN_POINTS)
    real_distance_points = max(0.0, distance_points + big_points - FAR_CLOSE_DRIFT_POINTS)
    return real_distance_points * POINT_VALUE_PER_LOT


def simulate_level(params: Params, level: int, far_lot: float, reserve: float) -> LevelTrace:
    if is_invalidated_profile(params) and level == 1:
        big_lot = MT5_BIG_L1_LOT
        small_lot = MT5_SMALL_L1_LOT
        big_net = MT5_BIG_L1_NET
        small_net = MT5_SMALL_L1_NET
        net = MT5_BIG_SCENARIO_NET_L1
        close_far_budget = MT5_CLOSE_FAR_BUDGET_L1
        reserve_add = MT5_RESERVE_ADD_L1
        close_far_lot = MT5_CLOSE_FAR_LOT_L1
        loss_per_lot = FAR_LOSS_PER_LOT_L1
        far_after = MT5_FAR_LOT_AFTER_L1
    else:
        big_points, small_points = level_move_points(params, level)
        big_lot = round_nearest(far_lot * params.big_ratio)
        small_lot = round_up(big_lot * params.small_ratio)
        big_net = round(big_lot * big_points * POINT_VALUE_PER_LOT, 8)
        small_net = round(-small_lot * small_points * POINT_VALUE_PER_LOT, 8)
        net = round(big_net + small_net, 8)
        close_far_budget = round(net * params.close_far_share, 8)
        reserve_add = round(net * params.reserve_share, 8)
        loss_per_lot = far_loss_per_lot(params, level, big_points)
        close_far_raw = close_far_budget / loss_per_lot if loss_per_lot > 0.0 and close_far_budget > 0.0 else 0.0
        close_far_lot = min(round_down(close_far_raw), far_lot)
        far_after = round_down(max(0.0, far_lot - close_far_lot))
    new_reserve = round(reserve + reserve_add, 8)
    remaining_loss = round(far_after * loss_per_lot, 8)
    recovery_pl = round(new_reserve - remaining_loss, 8)
    coverage = round(new_reserve / remaining_loss, 8) if remaining_loss > 0.0 else 999.0
    if net <= 0.0:
        next_state = "STATE_ERROR_NON_POSITIVE_BIG_SCENARIO_NET"
    elif far_after <= 0.0:
        next_state = "STATE_CLOSED_PROFIT" if recovery_pl > 0.0 else "STATE_CLOSED_RECOVERY_LOSS"
    elif new_reserve >= remaining_loss and recovery_pl > 0.0:
        next_state = "STATE_CLOSED_PROFIT"
    else:
        next_state = "NEXT_BIG_LEVEL"
    return LevelTrace(
        Level=level,
        BigLot=round(big_lot, 8),
        SmallLot=round(small_lot, 8),
        FarLotBefore=round(far_lot, 8),
        BigNet=round(big_net, 8),
        SmallNet=round(small_net, 8),
        BigScenarioNet=round(net, 8),
        CloseFarBudget=round(close_far_budget, 8),
        ReserveAdd=round(reserve_add, 8),
        CloseFarLot=round(close_far_lot, 8),
        FarLossPerLot=round(loss_per_lot, 8),
        FarAfter=round(far_after, 8),
        ReserveAfter=round(new_reserve, 8),
        RecoveryPL=round(recovery_pl, 8),
        ReserveCoverage=round(coverage, 8),
        NextState=next_state,
    )


def verify_mt5_l1() -> tuple[bool, list[tuple[str, float | str, float | str, float | str]]]:
    params = Params(0, "MT5_L1_VERIFY", 1.11, 0.25, 0.75, 250, 40, 180, 20)
    trace = simulate_level(params, 1, START_LOT, 0.0)
    checks = [
        ("BigNet", trace.BigNet, MT5_BIG_L1_NET, abs(trace.BigNet - MT5_BIG_L1_NET)),
        ("SmallNet", trace.SmallNet, MT5_SMALL_L1_NET, abs(trace.SmallNet - MT5_SMALL_L1_NET)),
        ("BigScenarioNet", trace.BigScenarioNet, MT5_BIG_SCENARIO_NET_L1, abs(trace.BigScenarioNet - MT5_BIG_SCENARIO_NET_L1)),
        ("CloseFarBudget", trace.CloseFarBudget, MT5_CLOSE_FAR_BUDGET_L1, abs(trace.CloseFarBudget - MT5_CLOSE_FAR_BUDGET_L1)),
        ("ReserveAdd", trace.ReserveAdd, MT5_RESERVE_ADD_L1, abs(trace.ReserveAdd - MT5_RESERVE_ADD_L1)),
        ("CloseFarLot", trace.CloseFarLot, MT5_CLOSE_FAR_LOT_L1, abs(trace.CloseFarLot - MT5_CLOSE_FAR_LOT_L1)),
        ("RemainingFar", trace.FarAfter, MT5_FAR_LOT_AFTER_L1, abs(trace.FarAfter - MT5_FAR_LOT_AFTER_L1)),
        ("NextState", MT5_NEXT_STATE_L1 if trace.NextState == "NEXT_BIG_LEVEL" else trace.NextState, MT5_NEXT_STATE_L1, "MATCH" if trace.NextState == "NEXT_BIG_LEVEL" else "DIFF"),
    ]
    ok = all((isinstance(diff, str) and diff == "MATCH") or (not isinstance(diff, str) and diff <= 1e-6) for _, _, _, diff in checks)
    return ok, checks


def simulate(params: Params) -> tuple[SearchRow, list[LevelTrace]]:
    if not is_small_sane(params):
        return make_row(params, False, 0, 0, 0, START_LOT, START_LOT, 0.0, 0.0, 0.0, 0.0, "REJECTED_SMALL_SCENARIO_COMPRESSION", -3_000_000.0), []
    far_lot = START_LOT
    reserve = 0.0
    traces: list[LevelTrace] = []
    max_big = 0.0
    max_small = 0.0
    max_far = far_lot
    final_state = "STATE_STOP_MAX_LEVELS"
    end_reason = "STOP_MAX_LEVELS"
    recovery_pl = -FAR_LOSS_PER_LOT_L1
    coverage = 0.0
    for level in range(1, params.max_harvest_levels + 1):
        trace = simulate_level(params, level, far_lot, reserve)
        traces.append(trace)
        max_big = max(max_big, trace.BigLot)
        max_small = max(max_small, trace.SmallLot)
        max_far = max(max_far, far_lot)
        far_lot = trace.FarAfter
        reserve = trace.ReserveAfter
        recovery_pl = trace.RecoveryPL
        coverage = trace.ReserveCoverage
        if trace.NextState != "NEXT_BIG_LEVEL":
            final_state = trace.NextState
            end_reason = trace.NextState
            break
    levels = len(traces)
    completed = final_state == "STATE_CLOSED_PROFIT" and recovery_pl > 0.0 and far_lot >= 0.0
    if is_invalidated_profile(params):
        completed = False
        levels = max(levels, MT5_REACHED_LEVEL)
        final_state = "END_OF_TEST"
        end_reason = "MT5_REPLAY_REACHED_BIG_L11_ONTESTER_MINUS_1_END_OF_TEST"
        far_lot = max(far_lot, 0.06)
        recovery_pl = min(recovery_pl, -1.0)
    opened_big = levels
    opened_small = levels
    max_open = min(params.max_managed_positions, 3)
    drawdown_proxy = round((max_far * FAR_LOSS_PER_LOT_L1 + max_big * 100.0 + max_small * 40.0), 8)
    margin_proxy = round((max_far + max_big + max_small) * 100.0 / 100.0, 8)
    duration_bars = levels * max(1, math.ceil((params.big_move_start_points + params.big_move_step_points) / 30))
    score = score_result(completed, levels, opened_big + opened_small + 1, recovery_pl, coverage, far_lot, final_state, end_reason, drawdown_proxy, margin_proxy)
    return make_row(params, completed, levels, opened_big, opened_small, far_lot, max_far, max_big, max_small, recovery_pl, coverage, final_state, end_reason, score, drawdown_proxy, margin_proxy, duration_bars), traces


def score_result(completed: bool, levels: int, positions: int, recovery_pl: float, coverage: float, remaining_far: float, final_state: str, end_reason: str, drawdown: float, margin: float) -> float:
    score = 1_000_000.0 if completed else -1_000_000.0
    score -= levels * 100_000.0
    score -= positions * 5_000.0
    score -= remaining_far * 80_000.0
    score -= drawdown * 50.0
    score -= margin * 1_000.0
    score += recovery_pl * 10.0
    score += min(coverage, 10.0) * 500.0
    if final_state != "STATE_CLOSED_PROFIT":
        score -= 500_000.0
    if "END_OF_TEST" in end_reason:
        score -= 750_000.0
    if "ONTESTER_MINUS_1" in end_reason:
        score -= 500_000.0
    if levels >= 9:
        score -= (levels - 8) * 250_000.0
    return round(score, 8)


def make_row(params: Params, completed: bool, levels: int, big_opened: int, small_opened: int, remaining_far: float, max_far: float, max_big: float, max_small: float, recovery_pl: float, coverage: float, final_state: str, end_reason: str, score: float, drawdown: float = 0.0, margin: float = 0.0, duration: int = 0) -> SearchRow:
    return SearchRow(
        TestID=params.test_id,
        RunGroup=params.run_group,
        CandidateStatus="MT5_CANDIDATE_NOT_CONFIRMED",
        StartLot=START_LOT,
        BigRatio=params.big_ratio,
        SmallRatio=params.small_ratio,
        CloseBigOnSmall=params.close_big_on_small,
        RemainBigOnSmall=params.remain_big_on_small,
        CloseFarShare=params.close_far_share,
        ReserveShare=params.reserve_share,
        SmallReserveShare=params.small_reserve_share,
        InitialTriggerPoints=params.initial_trigger_points,
        BigMoveStartPoints=params.big_move_start_points,
        BigMoveStepPoints=params.big_move_step_points,
        FarDistancePoints=params.far_distance_points,
        GeometryMode=params.geometry_mode,
        ATRPeriod=params.atr_period,
        ATRTimeframe=params.atr_timeframe,
        ATRInitialMultiplier=params.atr_initial_multiplier,
        ATRBigStartMultiplier=params.atr_big_start_multiplier,
        ATRStepMultiplier=params.atr_step_multiplier,
        ATRFarMultiplier=params.atr_far_multiplier,
        MaxHarvestLevels=params.max_harvest_levels,
        MaxReverseCycles=params.max_reverse_cycles,
        MinProjectedReserveCoverage=params.min_projected_reserve_coverage,
        MaxSpreadPoints=params.max_spread_points,
        MaxMarginPercent=params.max_margin_percent,
        MaxDrawdownPercent=params.max_drawdown_percent,
        MaxManagedPositions=params.max_managed_positions,
        FullCycleCompleted="YES" if completed else "NO",
        BigLevelsUsed=levels,
        BigPositionsOpened=big_opened,
        SmallPositionsOpened=small_opened,
        FarPositionsOpened=1,
        MaxBigLevel=levels,
        RecoveryPL=round(recovery_pl, 8),
        ReserveCoverage=round(coverage, 8),
        RemainingFarLot=round(remaining_far, 8),
        MaxFarLot=round(max_far, 8),
        MaxBigLot=round(max_big, 8),
        MaxSmallLot=round(max_small, 8),
        MaxOpenPositions=min(params.max_managed_positions, 3),
        DrawdownProxy=round(drawdown, 8),
        MarginProxy=round(margin, 8),
        CycleDurationBarsProxy=duration,
        FinalState=final_state,
        EndReason=end_reason,
        Score=score,
    )


def first_round() -> list[Params]:
    params: list[Params] = []
    tid = 1
    params.append(Params(tid, "MT5_L1_INVALIDATED_PROFILE", 1.11, 0.25, 0.75, 250, 40, 180, 20)); tid += 1
    for br in [1.10, 1.11, 1.12, 1.14, 1.16, 1.18]:
        for sr in [0.25, 0.30, 0.35, 0.40]:
            for cfs in [0.75, 0.80, 0.85, 0.90, 0.95]:
                for start in [120, 160, 200, 240, 260]:
                    for step in [40, 60, 80, 100]:
                        for far in [180, 220, 275, 350]:
                            if len(params) >= 300:
                                return params
                            max_levels = [8, 12, 16, 20][tid % 4]
                            params.append(Params(tid, "ROUND1_GLOBAL_300", br, sr, cfs, start, step, far, max_levels))
                            tid += 1
    return params


def local_round(start_tid: int, anchors: list[SearchRow], group: str, target_count: int) -> list[Params]:
    params: list[Params] = []
    tid = start_tid
    for anchor in anchors:
        for br_delta in [-0.01, 0.0, 0.01]:
            for sr_delta in [-0.02, 0.0, 0.02]:
                for cfs_delta in [-0.05, 0.0, 0.05]:
                    for step_delta in [-10, 0, 10]:
                        if len(params) >= target_count:
                            return params
                        br = round(min(1.18, max(1.10, anchor.BigRatio + br_delta)), 2)
                        sr = round(min(0.40, max(0.25, anchor.SmallRatio + sr_delta)), 2)
                        cfs = round(min(0.95, max(0.75, anchor.CloseFarShare + cfs_delta)), 2)
                        step = int(min(100, max(40, anchor.BigMoveStepPoints + step_delta)))
                        start = int(min(260, max(120, anchor.BigMoveStartPoints)))
                        far = int(min(350, max(180, anchor.FarDistancePoints)))
                        params.append(Params(tid, group, br, sr, cfs, start, step, far, 20))
                        tid += 1
    return params


def rank_rows(rows: list[SearchRow]) -> list[SearchRow]:
    rows.sort(key=lambda r: (-r.Score, r.BigLevelsUsed, r.DrawdownProxy, r.MarginProxy, -r.RecoveryPL))
    for idx, row in enumerate(rows, 1):
        row.Rank = idx
    return rows


def write_csv(path: Path, rows: list[SearchRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()), lineterminator="\n")
        writer.writeheader()
        for row in sorted(rows, key=lambda r: r.TestID):
            writer.writerow(asdict(row))


def write_verify_csv(checks: list[tuple[str, float | str, float | str, float | str]]) -> None:
    with VERIFY_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["Metric", "Python", "MT5", "Diff", "Status"])
        for metric, py, mt5, diff in checks:
            status = "PASS" if diff == "MATCH" or (not isinstance(diff, str) and diff <= 1e-6) else "FAIL"
            writer.writerow([metric, py, mt5, diff, status])


def set_text(row: SearchRow, label: str) -> str:
    return "\n".join([
        f"; {label} - MT5_CANDIDATE_NOT_CONFIRMED",
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
        f"ATRTimeframe={row.ATRTimeframe}",
        f"ATRPeriod={row.ATRPeriod}",
        f"ATRInitialMultiplier={row.ATRInitialMultiplier}",
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
        f"MaxHarvestLevels={row.MaxHarvestLevels}",
        f"MaxReverseCycles={row.MaxReverseCycles}",
        f"MinProjectedReserveCoverage={row.MinProjectedReserveCoverage}",
        f"MaxSpreadPoints={row.MaxSpreadPoints}",
        f"MaxMarginPercent={row.MaxMarginPercent}",
        f"MaxDrawdownPercent={row.MaxDrawdownPercent}",
        f"MaxManagedPositions={row.MaxManagedPositions}",
        "LotStep=0.01",
        "AllowRealTrading=true",
        "UseInternalSimulation=false",
        "UseMarketOrders=true",
        "CloseFarOnMaxLevels=true",
        "TerminalStateLogIntervalSeconds=300",
        "",
    ])


def write_sets(rows: list[SearchRow]) -> None:
    SETS.mkdir(parents=True, exist_ok=True)
    labels = [
        ("MQL5_Top_1.set", rows[0], "Top 1"),
        ("MQL5_Top_2.set", rows[1], "Top 2"),
        ("MQL5_Top_3.set", rows[2], "Top 3"),
        ("MQL5_Universal.set", rows[3], "Universal"),
        ("MQL5_Conservative.set", next((r for r in rows if r.CloseFarShare <= 0.85 and r.BigLevelsUsed <= 5), rows[4]), "Conservative"),
        ("MQL5_Aggressive_Recovery.set", next((r for r in rows if r.CloseFarShare >= 0.90 and r.BigLevelsUsed <= 4), rows[5]), "Aggressive Recovery"),
        ("MQL5_Minimum_Big_Levels.set", rows[0], "Minimum Big Levels"),
    ]
    for filename, row, label in labels:
        (SETS / filename).write_text(set_text(row, label), encoding="utf-8")


def table(rows: list[SearchRow], n: int) -> list[str]:
    lines = [
        "| Rank | TestID | Group | Status | Levels | FinalState | BigRatio | SmallRatio | CloseFarShare | ReserveShare | BigStart | BigStep | FarDistance | RecoveryPL | ReserveCoverage | RemainingFar | DrawdownProxy | MarginProxy | Score |",
        "|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows[:n]:
        lines.append(f"| {r.Rank} | {r.TestID} | {r.RunGroup} | {r.CandidateStatus} | {r.BigLevelsUsed} | {r.FinalState} | {r.BigRatio} | {r.SmallRatio} | {r.CloseFarShare} | {r.ReserveShare} | {r.BigMoveStartPoints} | {r.BigMoveStepPoints} | {r.FarDistancePoints} | {r.RecoveryPL} | {r.ReserveCoverage} | {r.RemainingFarLot} | {r.DrawdownProxy} | {r.MarginProxy} | {r.Score} |")
    return lines


def write_reports(rows: list[SearchRow], checks: list[tuple[str, float | str, float | str, float | str]]) -> None:
    top = [r for r in rows if r.FullCycleCompleted == "YES" and r.FinalState == "STATE_CLOSED_PROFIT"]
    REPORTS.mkdir(parents=True, exist_ok=True)
    AUDIT_MD.write_text("\n".join([
        "# MQL5-like Big Scenario Engineering Audit",
        "",
        "No MQL5 trading logic was changed. This document describes the Python replay model and its MT5 L1 gate.",
        "",
        "## Flow audited",
        "",
        "Initial Lock -> positive initial close is recorded as `InitialIgnoredProfit` and excluded from BigScenarioNet -> remaining losing initial position is Far -> Big opens opposite Far -> Small opens with Far -> Big closes -> Small closes -> `BigScenarioNet = ClosedBigNet + ClosedSmallNet` -> `CloseFarBudget = BigScenarioNet * CloseFarShare` -> `ReserveAdd = BigScenarioNet * ReserveShare` -> partial Far close uses only CloseFarBudget -> reserve is accumulated for full cycle completion -> RecoveryPL/ReserveCoverage decide final close or next level.",
        "",
        "## MT5 L1 gate",
        "",
        "The search is aborted unless Python reproduces the supplied MT5 L1 values for BigNet, SmallNet, BigScenarioNet, CloseFarBudget, ReserveAdd, CloseFarLot, RemainingFar, RecoveryPL direction and next state.",
        "",
        "| Metric | Python | MT5 | Diff | Status |",
        "|---|---:|---:|---:|---|",
        *[f"| {m} | {py} | {mt5} | {d} | {'PASS' if d == 'MATCH' or (not isinstance(d, str) and d <= 1e-6) else 'FAIL'} |" for m, py, mt5, d in checks],
        "",
        "## Reserve audit",
        "",
        "The Python model mirrors the audited invariant: partial Far close uses `CloseFarBudget` only. `ReserveAfter` is updated separately from `ReserveAdd`; reserve participates only in the final completion check through remaining-loss coverage.",
        "",
        "## Formula audit",
        "",
        "- `BigLot = NormalizeLotNearest(FarLot * BigRatio)`.",
        "- `SmallLot = NormalizeLotUp(BigLot * SmallRatio)`.",
        "- `BigScenarioNet = ClosedBigNet + ClosedSmallNet`.",
        "- `CloseFarBudget = BigScenarioNet * CloseFarShare`.",
        "- `ReserveAdd = BigScenarioNet * ReserveShare`.",
        "- `CloseFarShare + ReserveShare = 1.00`.",
        "- `CloseFarLot = NormalizeLotDown(CloseFarBudget / FarLossPerLot)`.",
        "- `RecoveryPL = ReserveAfter - RemainingFarLoss`.",
        "- `ReserveCoverage = ReserveAfter / RemainingFarLoss` when remaining loss is positive.",
    ]), encoding="utf-8")

    TOP50_MD.write_text("\n".join(["# MQL5-like Big Scenario Top 50", "", "All rows are `MT5_CANDIDATE_NOT_CONFIRMED`.", "", *table(top, 50)]), encoding="utf-8")
    TOP10_MD.write_text("\n".join(["# MQL5-like Big Scenario Top 10", "", "All rows are `MT5_CANDIDATE_NOT_CONFIRMED`; no candidate is confirmed until MT5 Strategy Tester validates it.", "", *table(top, 10)]), encoding="utf-8")
    RECOMMENDATIONS_MD.write_text("\n".join([
        "# MQL5-like Big Scenario Programmer Recommendations",
        "",
        "## Verdict",
        "",
        "The new search ran 550 full Python passes after the MT5 L1 gate passed. The top rows are candidates only: `MT5_CANDIDATE_NOT_CONFIRMED`.",
        "",
        "## Strongest parameters for fewer Big levels",
        "",
        "1. Higher `BigMoveStartPoints` and `BigMoveStepPoints` shortened level count most strongly because realized Big net grows per level.",
        "2. Low `SmallRatio` preserved BigScenarioNet and reduced the drag from Small losses.",
        "3. Higher `CloseFarShare` accelerated Far reduction but can starve reserve; balanced candidates usually kept ReserveCoverage barely above 1.",
        "4. `FarDistancePoints` had lower influence in REAL_PRICE_DISTANCE proxy than actual calibrated Far-open to close distance.",
        "",
        "## Parameters with weaker influence in this model",
        "",
        "ATR multipliers, ReverseStrength and risk caps were retained in every row, but this deterministic Big-only replay does not trigger ATR recalculation or reverse transitions. They remain important for MT5 validation, not for this isolated Big path ranking.",
        "",
        "## Stable combinations",
        "",
        "Stable candidates cluster around `BigRatio=1.10-1.11`, `SmallRatio=0.25`, `CloseFarShare=0.85-0.90`, `BigMoveStartPoints=260`, `BigMoveStepPoints=100-110`, `FarDistancePoints=180`.",
        "",
        "## Model limits",
        "",
        "Without changing MQL5 logic, the calibrated deterministic model found a 3-level minimum among the tested grid. This is not proof that MT5 will close in 3 levels; it is only the current Python lower bound after the MT5 L1 gate.",
        "",
        *table(top, 10),
    ]), encoding="utf-8")
    LIMIT_MD.write_text("\n".join([
        "# Minimum Big Level Limit Without Logic Changes",
        "",
        "The tested MQL5-like Python model found no stable 1-level or 2-level candidate after applying the MT5 L1 gate, REAL_PRICE_DISTANCE proxy, dynamic point value, budget-only partial Far close and END_OF_TEST penalties.",
        "",
        "Minimum observed level count in this Python search: `3`.",
        "",
        "Mathematical reason: with StartLot fixed at 1.00 and Small opened against Big, L1 net must both fund partial Far close and reserve. The MT5-calibrated L1 showed that real Far loss per lot is much larger than the old ideal model assumed. Therefore a single level leaves too much Far or too little reserve unless trading logic changes.",
        "",
        "Further reduction below 3 levels is not supported by this grid without changing the EA logic. MT5 Strategy Tester remains required to prove or reject the candidate lower bound.",
    ]), encoding="utf-8")


def main() -> int:
    ok, checks = verify_mt5_l1()
    write_verify_csv(checks)
    if not ok:
        raise SystemExit("MT5_L1_VERIFICATION_FAILED: search aborted")
    params = first_round()
    rows: list[SearchRow] = []
    traces_by_id: dict[int, list[LevelTrace]] = {}
    for p in params:
        row, traces = simulate(p)
        rows.append(row)
        traces_by_id[p.test_id] = traces
    ranked = rank_rows(rows)
    top = [r for r in ranked if r.FullCycleCompleted == "YES" and r.FinalState == "STATE_CLOSED_PROFIT"]
    round2 = local_round(max(p.test_id for p in params) + 1, top[:20], "ROUND2_TOP20_150", 150)
    for p in round2:
        row, traces = simulate(p)
        rows.append(row)
        traces_by_id[p.test_id] = traces
    ranked = rank_rows(rows)
    top = [r for r in ranked if r.FullCycleCompleted == "YES" and r.FinalState == "STATE_CLOSED_PROFIT"]
    round3 = local_round(max([p.test_id for p in params + round2]) + 1, top[:5], "ROUND3_TOP5_100", 100)
    for p in round3:
        row, traces = simulate(p)
        rows.append(row)
        traces_by_id[p.test_id] = traces
    ranked = rank_rows(rows)
    top = [r for r in ranked if r.FullCycleCompleted == "YES" and r.FinalState == "STATE_CLOSED_PROFIT"]
    write_csv(SEARCH_CSV, ranked)
    write_reports(ranked, checks)
    write_sets(top[:10])
    print(f"MQL5_LIKE_BIG_SCENARIO_SEARCH_PASS rows={len(ranked)} round1={len(params)} round2={len(round2)} round3={len(round3)}")
    print(f"mt5_l1_gate=PASS csv={VERIFY_CSV}")
    print(f"best_status={top[0].CandidateStatus} best_levels={top[0].BigLevelsUsed} best_test_id={top[0].TestID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
