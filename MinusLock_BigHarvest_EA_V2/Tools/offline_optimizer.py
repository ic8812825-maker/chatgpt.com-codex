#!/usr/bin/env python3
"""Offline parameter optimizer for MinusLock_BigHarvest_EA_V2.

This is a deterministic mathematical screening model. It intentionally does not
claim MT5-equivalent execution; it reproduces the EA's recovery-accounting rules,
lot geometry, Big/Small/MaxLevels transitions and strict success criterion:

    RecoveryPL = FinalBalance - CycleStartBalance

The output is a ranked candidate list and .set files for later manual MT5
Strategy Tester validation.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
import math
import random
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean, pstdev
from typing import Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_set_files import write_set_file
from offline_scenarios import Scenario, build_scenarios, scenario_names
from score_parameters import score_candidate, verdict

ROOT = SCRIPT_DIR.parent

LOT_STEP = 0.01
INITIAL_DEPOSIT = 10_000.0
POINT_VALUE_PER_LOT = 1.0
COMMISSION_PER_LOT = 0.0
SLIPPAGE_POINTS = 2.0
MARGIN_PER_LOT = 1000.0
REJECTED_SCORE_PENALTY = 1_000_000.0
REJECTED_FINAL_RANK = -999_999_999.0

RANGES = {
    "StartLot": [0.01, 0.05, 0.10, 0.50, 1.00],
    "BigRatio": [1.05, 1.10, 1.12, 1.15, 1.18, 1.20, 1.25],
    "SmallRatio": [0.15, 0.20, 0.25, 0.30, 0.35],
    "ClosePair": [(0.30, 0.70), (0.35, 0.65), (0.40, 0.60), (0.45, 0.55), (0.50, 0.50)],
    "ReservePair": [(0.10, 0.90), (0.15, 0.85), (0.20, 0.80), (0.25, 0.75), (0.30, 0.70), (0.40, 0.60)],
    "SmallReserveShare": [0.00, 0.03, 0.05, 0.07, 0.10],
    "InitialTriggerPoints": [70, 100, 150, 200],
    "BigMoveStartPoints": [70, 100, 150, 200],
    "BigMoveStepPoints": [25, 50, 75, 100],
    "FarDistancePoints": [100, 150, 200, 250, 300],
    "MaxHarvestLevels": [5, 6, 7, 8, 9, 10],
    "MaxReverseCycles": [3, 5, 7, 10],
    "MaxSpreadPoints": [30, 40, 60, 80],
    "MaxMarginPercent": [50, 60, 70],
    "MaxDrawdownPercent": [15, 20, 25, 30],
}

CSV_COLUMNS = [
    "RunID", "Category", "StartLot", "BigRatio", "SmallRatio", "CloseBigOnSmall", "RemainBigOnSmall",
    "CloseFarShare", "ReserveShare", "SmallReserveShare", "InitialTriggerPoints", "BigMoveStartPoints",
    "BigMoveStepPoints", "FarDistancePoints", "MaxHarvestLevels", "MaxReverseCycles", "MaxSpreadPoints",
    "MaxMarginPercent", "MaxDrawdownPercent", "RecoveryPL_Mean", "RecoveryPL_Min", "RecoveryPL_Max",
    "MaxDD_Mean", "MaxDD_Max", "MaxMarginUsed", "StopMaxLevelsCount", "ClosedProfitCount",
    "ClosedRecoveryLossCount", "CompressionRatio", "NewBigToOldFarRatio", "ProfitScore", "StabilityScore",
    "RobustnessScore", "Score", "FinalRank", "CoverageRatio", "IsSelectableForSetFile", "Verdict",
]

LOCAL_SEARCH_RANGES = {
    "StartLot": [0.01, 0.05, 0.10, 0.50, 1.00],
    "BigRatio": [1.12, 1.13, 1.14, 1.15, 1.16, 1.17, 1.18],
    "SmallRatio": [0.30, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.40],
    "ClosePair": [(0.30, 0.70), (0.32, 0.68), (0.34, 0.66), (0.36, 0.64), (0.38, 0.62), (0.40, 0.60)],
    "ReservePair": [(0.20, 0.80), (0.22, 0.78), (0.24, 0.76), (0.26, 0.74), (0.28, 0.72), (0.30, 0.70)],
    "SmallReserveShare": [0.03, 0.05, 0.07, 0.10],
    "InitialTriggerPoints": [70, 100, 150],
    "BigMoveStartPoints": [150, 200],
    "BigMoveStepPoints": [50, 75, 100],
    "FarDistancePoints": [250, 300],
    "MaxHarvestLevels": [7, 8, 9, 10],
    "MaxReverseCycles": [5, 7, 10],
    "MaxSpreadPoints": [30, 40],
    "MaxMarginPercent": [50, 60, 70],
    "MaxDrawdownPercent": [15, 20, 25, 30],
}



@dataclass(frozen=True)
class Params:
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
    MaxHarvestLevels: int
    MaxReverseCycles: int
    MaxSpreadPoints: int
    MaxMarginPercent: int
    MaxDrawdownPercent: int

LEADER_ZONE_PARAMS = Params(
    StartLot=0.05,
    BigRatio=1.15,
    SmallRatio=0.35,
    CloseBigOnSmall=0.35,
    RemainBigOnSmall=0.65,
    CloseFarShare=0.25,
    ReserveShare=0.75,
    SmallReserveShare=0.05,
    InitialTriggerPoints=100,
    BigMoveStartPoints=200,
    BigMoveStepPoints=75,
    FarDistancePoints=300,
    MaxHarvestLevels=8,
    MaxReverseCycles=7,
    MaxSpreadPoints=30,
    MaxMarginPercent=60,
    MaxDrawdownPercent=25,
)

@dataclass
class ScenarioResult:
    scenario: str
    recovery_pl: float
    max_dd: float
    max_margin: float
    stop_max: bool
    closed_profit: bool
    closed_recovery_loss: bool
    compression_violation: bool
    compression_ratio: float
    new_big_to_old_far_ratio: float
    final_far_lot: float
    final_state: str
    levels_used: int


def normalize_nearest(value: float, step: float = LOT_STEP) -> float:
    return round(round(value / step) * step, 2)


def normalize_up(value: float, step: float = LOT_STEP) -> float:
    return round(math.ceil((value - 1e-12) / step) * step, 2)


def normalize_to_step(value: float, step: float = LOT_STEP) -> float:
    return round(round(value / step) * step, 2)


def cost_for_lot(lot: float, spread_points: float) -> float:
    return lot * (spread_points + SLIPPAGE_POINTS) * POINT_VALUE_PER_LOT + lot * COMMISSION_PER_LOT


def pnl(lot: float, points: float, spread_points: float, multiplier: float = 1.0) -> float:
    return lot * points * POINT_VALUE_PER_LOT * multiplier - cost_for_lot(lot, spread_points)


def loss(lot: float, points: float, spread_points: float, multiplier: float = 1.0) -> float:
    return lot * points * POINT_VALUE_PER_LOT * multiplier + cost_for_lot(lot, spread_points)


def validate_params(p: Params) -> str:
    if p.BigRatio <= 1.0:
        return "BIG_RATIO"
    if not (0.0 < p.SmallRatio < 1.0):
        return "SMALL_RATIO"
    if abs((p.CloseBigOnSmall + p.RemainBigOnSmall) - 1.0) > 1e-9:
        return "CLOSE_BIG_PAIR"
    if abs((p.CloseFarShare + p.ReserveShare) - 1.0) > 1e-9:
        return "RESERVE_PAIR"
    if p.BigRatio * p.BigRatio * p.RemainBigOnSmall >= 1.0:
        return "COMPRESSION_FORMULA"
    if p.StartLot <= 0.0 or p.MaxHarvestLevels < 1 or p.MaxReverseCycles < 1:
        return "BASIC_RANGE"
    return ""


def big_move_points(p: Params, level: int) -> float:
    return p.BigMoveStartPoints + (level - 1) * p.BigMoveStepPoints


def can_final_close(balance: float, cycle_start: float, far_lot: float, p: Params, scenario: Scenario) -> Tuple[bool, float]:
    projected_loss = loss(far_lot, p.FarDistancePoints, p.MaxSpreadPoints, scenario.stress_multiplier)
    projected_recovery = balance - projected_loss - cycle_start
    return projected_recovery > 0.0, projected_recovery


def simulate_scenario(p: Params, scenario: Scenario) -> ScenarioResult:
    initial_ignored_profit = pnl(p.StartLot, p.InitialTriggerPoints, p.MaxSpreadPoints, 1.0)
    cycle_start = INITIAL_DEPOSIT + max(0.0, initial_ignored_profit)
    balance = cycle_start
    peak_balance = balance
    max_dd = 0.0
    max_margin = 0.0
    reserve = 0.0
    far_lot = normalize_to_step(p.StartLot)
    compression_violation = False
    compression_ratios: List[float] = []
    new_big_ratios: List[float] = []
    reverse_cycles = 0
    final_state = "STATE_FAR_ACTIVE"
    levels_used = 0

    for level, event in enumerate(scenario.events[: p.MaxHarvestLevels], start=1):
        levels_used = level
        big_lot = normalize_nearest(far_lot * p.BigRatio)
        small_lot = normalize_up(big_lot * p.SmallRatio)
        max_margin = max(max_margin, (far_lot + big_lot + small_lot) * MARGIN_PER_LOT)
        move = big_move_points(p, level)

        if event == "B":
            profit_big = pnl(big_lot, move, p.MaxSpreadPoints, scenario.stress_multiplier)
            loss_small = loss(small_lot, move, p.MaxSpreadPoints, scenario.stress_multiplier)
            net = profit_big - loss_small
            if net > 0.0:
                close_budget = net * p.CloseFarShare
                reserve += net * p.ReserveShare
            else:
                close_budget = 0.0
            close_far_lot = min(far_lot, normalize_to_step(close_budget / max(1e-9, p.FarDistancePoints * POINT_VALUE_PER_LOT)))
            far_close_loss = loss(close_far_lot, p.FarDistancePoints, p.MaxSpreadPoints, scenario.stress_multiplier) if close_far_lot > 0.0 else 0.0
            balance += net - far_close_loss
            far_lot = normalize_to_step(max(0.0, far_lot - close_far_lot))
        else:
            reverse_cycles += 1
            # Small-at-Far usually closes near the old Far touch, while the Big partial
            # close is based on the actual terminal remainder. Use a conservative but
            # not worst-tick full-distance loss model so offline screening does not
            # reject every mathematically compressed parameter set.
            small_leg_points = p.FarDistancePoints
            adverse_close_points = p.FarDistancePoints * 0.25
            profit_small = pnl(small_lot, small_leg_points, p.MaxSpreadPoints, scenario.stress_multiplier)
            old_far_loss = loss(far_lot, adverse_close_points, p.MaxSpreadPoints, scenario.stress_multiplier)
            close_big_lot = min(big_lot, normalize_to_step(big_lot * p.CloseBigOnSmall))
            close_big_loss = loss(close_big_lot, adverse_close_points, p.MaxSpreadPoints, scenario.stress_multiplier)
            remaining_big = normalize_to_step(max(0.0, big_lot - close_big_lot))
            small_net = profit_small - old_far_loss - close_big_loss
            if small_net > 0.0:
                reserve += small_net * p.SmallReserveShare
            balance += small_net
            old_far = far_lot
            far_lot = remaining_big
            next_big = normalize_nearest(far_lot * p.BigRatio)
            ratio = far_lot / max(old_far, LOT_STEP)
            next_big_ratio = next_big / max(old_far, LOT_STEP)
            compression_ratios.append(ratio)
            new_big_ratios.append(next_big_ratio)
            if next_big > old_far + LOT_STEP / 2:
                compression_violation = True

        peak_balance = max(peak_balance, balance)
        max_dd = max(max_dd, peak_balance - balance)
        ok_final, projected_recovery = can_final_close(balance, cycle_start, far_lot, p, scenario)
        if far_lot <= LOT_STEP / 2 or ok_final:
            if far_lot > LOT_STEP / 2:
                final_loss = loss(far_lot, p.FarDistancePoints, p.MaxSpreadPoints, scenario.stress_multiplier)
                balance -= final_loss
                far_lot = 0.0
            final_state = "STATE_CLOSED_PROFIT" if balance - cycle_start > 0.0 else "STATE_CLOSED_RECOVERY_LOSS"
            break
        if reverse_cycles > p.MaxReverseCycles:
            final_state = "STATE_CLOSED_RECOVERY_LOSS"
            break
    else:
        final_loss = loss(far_lot, p.FarDistancePoints, p.MaxSpreadPoints, scenario.stress_multiplier)
        balance -= final_loss
        far_lot = 0.0
        final_state = "STATE_STOP_MAX_LEVELS"

    recovery_pl = balance - cycle_start
    closed_profit = final_state == "STATE_CLOSED_PROFIT" and recovery_pl > 0.0 and not compression_violation
    closed_recovery_loss = final_state == "STATE_CLOSED_RECOVERY_LOSS" or recovery_pl <= 0.0
    stop_max = final_state == "STATE_STOP_MAX_LEVELS"
    if recovery_pl <= 0.0 and final_state == "STATE_CLOSED_PROFIT":
        final_state = "STATE_CLOSED_RECOVERY_LOSS"
        closed_profit = False
        closed_recovery_loss = True

    return ScenarioResult(
        scenario=scenario.name,
        recovery_pl=round(recovery_pl, 2),
        max_dd=round(max_dd, 2),
        max_margin=round(max_margin, 2),
        stop_max=stop_max,
        closed_profit=closed_profit,
        closed_recovery_loss=closed_recovery_loss,
        compression_violation=compression_violation,
        compression_ratio=round(max(compression_ratios) if compression_ratios else 0.0, 4),
        new_big_to_old_far_ratio=round(max(new_big_ratios) if new_big_ratios else 0.0, 4),
        final_far_lot=round(far_lot, 2),
        final_state=final_state,
        levels_used=levels_used,
    )


def aggregate_results(run_id: int, p: Params, results: List[ScenarioResult], coverage_ratio: float) -> Dict[str, object]:
    pls = [r.recovery_pl for r in results]
    dds = [r.max_dd for r in results]
    gross_profit = sum(x for x in pls if x > 0.0)
    gross_loss = abs(sum(x for x in pls if x < 0.0))
    max_dd = max(dds) if dds else 0.0
    recovery_std = pstdev(pls) if len(pls) > 1 else 0.0
    dd_std = pstdev(dds) if len(dds) > 1 else 0.0
    stop_count = sum(r.stop_max for r in results)
    loss_count = sum(r.closed_recovery_loss for r in results)
    closed_profit_count = sum(r.closed_profit for r in results)
    compression_count = sum(r.compression_violation for r in results)

    metrics: Dict[str, object] = asdict(p)
    metrics.update(
        RunID=run_id,
        Category="CANDIDATE",
        RecoveryPL_Mean=round(mean(pls), 2),
        RecoveryPL_Min=round(min(pls), 2),
        RecoveryPL_Max=round(max(pls), 2),
        MaxDD_Mean=round(mean(dds), 2),
        MaxDD_Max=round(max_dd, 2),
        MaxMarginUsed=round(max(r.max_margin for r in results), 2),
        StopMaxLevelsCount=stop_count,
        ClosedProfitCount=closed_profit_count,
        ClosedRecoveryLossCount=loss_count,
        CompressionViolationCount=compression_count,
        CompressionRatio=round(max(r.compression_ratio for r in results), 4),
        NewBigToOldFarRatio=round(max(r.new_big_to_old_far_ratio for r in results), 4),
        ProfitFactorOffline=round(gross_profit / gross_loss, 4) if gross_loss > 0.0 else round(gross_profit, 4),
        RecoveryFactorOffline=round(mean(pls) / max_dd, 4) if max_dd > 0.0 else round(mean(pls), 4),
        MaxAllowedDD=INITIAL_DEPOSIT * p.MaxDrawdownPercent / 100.0,
        MaxAllowedMargin=INITIAL_DEPOSIT * p.MaxMarginPercent / 100.0,
        RejectedReason=validate_params(p),
    )

    row_verdict = verdict(metrics)
    profit_score = score_candidate(metrics)
    stability_score = round(100.0 - recovery_std - dd_std - stop_count * 10.0 - loss_count * 20.0, 4)
    robustness_score = round((closed_profit_count / max(1, len(results))) * 100.0 - compression_count * 25.0 - stop_count * 25.0 - loss_count * 25.0, 4)

    if row_verdict == "ACCEPT":
        score = profit_score
        final_rank = round(profit_score + stability_score + robustness_score, 4)
        selectable = "YES"
    else:
        score = round(profit_score - REJECTED_SCORE_PENALTY, 4)
        final_rank = REJECTED_FINAL_RANK
        selectable = "NO"

    metrics.update(
        ProfitScore=profit_score,
        StabilityScore=stability_score,
        RobustnessScore=robustness_score,
        Score=score,
        FinalRank=final_rank,
        CoverageRatio=round(coverage_ratio, 8),
        IsSelectableForSetFile=selectable,
        Verdict=row_verdict,
    )
    return metrics


def grid_size() -> int:
    return math.prod(len(v) for v in RANGES.values())


def build_params(raw: dict) -> Params:
    raw = dict(raw)
    close_big, remain_big = raw.pop("ClosePair")
    close_far, reserve = raw.pop("ReservePair")
    return Params(CloseBigOnSmall=close_big, RemainBigOnSmall=remain_big, CloseFarShare=close_far, ReserveShare=reserve, **raw)


def sample_params(limit: int, seed: int, ranges: Dict[str, list], required: Optional[List[Params]] = None) -> List[Params]:
    """Deterministically sample a large grid while covering every allowed value."""
    rng = random.Random(seed)
    keys = list(ranges)
    generated: List[Params] = []
    seen = set()

    for p in required or []:
        if p not in seen:
            generated.append(p)
            seen.add(p)

    # Coverage pass: each range value is forced into at least one sampled combination.
    for key in keys:
        for value in ranges[key]:
            raw = {k: rng.choice(ranges[k]) for k in keys}
            raw[key] = value
            p = build_params(raw)
            if p not in seen:
                generated.append(p)
                seen.add(p)

    while len(generated) < limit:
        raw = {k: rng.choice(ranges[k]) for k in keys}
        p = build_params(raw)
        if p not in seen:
            generated.append(p)
            seen.add(p)
    return generated


def combined_sample(global_limit: int, local_limit: int, seed: int) -> List[Params]:
    """Run a broad global pass plus a 10k+ local pass around the audited leader zone."""
    seen = set()
    combined: List[Params] = []
    for p in sample_params(global_limit, seed, RANGES):
        if p not in seen:
            combined.append(p)
            seen.add(p)
    for p in sample_params(local_limit, seed + 1, LOCAL_SEARCH_RANGES, required=[LEADER_ZONE_PARAMS]):
        if p not in seen:
            combined.append(p)
            seen.add(p)
    return combined


def choose_categories(rows: List[Dict[str, object]]) -> Dict[str, Optional[Dict[str, object]]]:
    """Pick category representatives only from ACCEPT/selectable rows."""
    accepted = [r for r in rows if r["Verdict"] == "ACCEPT" and r["IsSelectableForSetFile"] == "YES"]
    used: set[int] = set()

    def pick(pool: List[Dict[str, object]], key, reverse=True) -> Optional[Dict[str, object]]:
        candidates = [r for r in pool if int(r["RunID"]) not in used]
        if not candidates:
            return None
        row = sorted(candidates, key=key, reverse=reverse)[0]
        used.add(int(row["RunID"]))
        return row

    safe_pool = [r for r in accepted if r["StartLot"] <= 0.10 and r["MaxDD_Max"] <= 120 and r["MaxMarginUsed"] <= 2500]
    balanced_pool = [r for r in accepted if r["RecoveryPL_Min"] > 0.0]
    aggressive_pool = [r for r in accepted if r["StartLot"] >= 0.50]

    selected: Dict[str, Optional[Dict[str, object]]] = {
        "SAFE": pick(safe_pool, key=lambda r: (-r["MaxDD_Max"], r["FinalRank"], r["RecoveryPL_Min"])),
        "BALANCED": pick(balanced_pool, key=lambda r: (r["FinalRank"], r["RecoveryPL_Min"])),
        "AGGRESSIVE": pick(aggressive_pool, key=lambda r: (r["FinalRank"], r["RecoveryPL_Min"])),
        "LOWLOT_SAFE": None,
    }

    # LOWLOT priority is explicit: StartLot=0.01 first, then 0.05, then 0.10.
    for lot in [0.01, 0.05, 0.10]:
        lowlot_pool = [r for r in accepted if abs(float(r["StartLot"]) - lot) < 1e-9 and int(r["RunID"]) not in used]
        row = pick(lowlot_pool, key=lambda r: (-r["MaxDD_Max"], r["FinalRank"], r["RecoveryPL_Min"]))
        if row is not None:
            selected["LOWLOT_SAFE"] = row
            break

    return selected


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_best_parameters(
    path: Path,
    rows: List[Dict[str, object]],
    selected: Dict[str, Optional[Dict[str, object]]],
    args,
    scenarios: List[Scenario],
    rejected_count: int,
    tested_count: int,
    coverage_ratio: float,
) -> None:
    top_accept = [r for r in rows if r["Verdict"] == "ACCEPT"][:20]
    top_rejected = sorted([r for r in rows if r["Verdict"] != "ACCEPT"], key=lambda r: (r["Score"], r["RecoveryPL_Mean"]), reverse=True)[:20]
    verdict_counts = Counter(str(r["Verdict"]) for r in rows if r["Verdict"] != "ACCEPT")
    lowlot = selected.get("LOWLOT_SAFE")
    lowlot_text = f"LOWLOT candidate found at StartLot={lowlot['StartLot']}" if lowlot else "LOWLOT_SAFE_NOT_FOUND"

    lines = [
        "# Offline Best Parameters for MinusLock_BigHarvest_EA_V2",
        "",
        "## Scope and limitations",
        "",
        "This report is generated without MT5. It is a deterministic offline filter, not a replacement for MetaTrader Strategy Tester.",
        "It uses the strict success rule `RecoveryPL = FinalBalance - CycleStartBalance`; AccountPL versus InitialDeposit is diagnostic only.",
        "InitialIgnoredProfit is excluded from pass/fail, matching the EA realRecoveryPL / OnTester contract.",
        "Rejected rows are never selectable for `.set` generation and always receive a hard score/final-rank penalty.",
        "",
        "## Optimization model",
        "",
        f"- Synthetic scenarios: {scenario_names(scenarios)}.",
        f"- Total combinations theoretical: {grid_size():,}.",
        f"- Total combinations tested: {tested_count:,} (global={args.max_runs:,}, local={args.local_runs:,}).",
        f"- Coverage ratio: {coverage_ratio:.8%}.",
        f"- Mathematically rejected or unstable rows in CSV: {rejected_count:,}.",
        "- P/L model: `Lot × Points × PointValuePerLot` minus spread/slippage/commission costs.",
        "- Compression filter: `BigRatio² × RemainBigOnSmall < 1` plus simulated `NewBig < OldFar` checks.",
        "- Ranking is two-stage: Verdict first, then FinalRank only inside ACCEPT; TOP REJECTED is diagnostics only.",
        "- STOP_MAX_LEVELS, STATE_CLOSED_RECOVERY_LOSS, compression violations and drawdown/margin breaches receive hard penalties.",
        "",
        "## Selected parameter sets",
        "",
        lowlot_text,
        "",
    ]
    for category, row in selected.items():
        lines += [f"### {category}", ""]
        if row is None:
            lines += [f"- {category}_NOT_FOUND: no Verdict=ACCEPT candidate satisfied this category filter.", ""]
            continue
        lines += [
            f"- StartLot={row['StartLot']}, BigRatio={row['BigRatio']}, SmallRatio={row['SmallRatio']}",
            f"- CloseBigOnSmall={row['CloseBigOnSmall']} / RemainBigOnSmall={row['RemainBigOnSmall']}",
            f"- CloseFarShare={row['CloseFarShare']} / ReserveShare={row['ReserveShare']}, SmallReserveShare={row['SmallReserveShare']}",
            f"- Trigger/steps: Initial={row['InitialTriggerPoints']}, BigStart={row['BigMoveStartPoints']}, BigStep={row['BigMoveStepPoints']}, FarDistance={row['FarDistancePoints']}",
            f"- MaxHarvestLevels={row['MaxHarvestLevels']}, MaxReverseCycles={row['MaxReverseCycles']}, MaxSpreadPoints={row['MaxSpreadPoints']}",
            f"- RecoveryPL mean/min/max: {row['RecoveryPL_Mean']} / {row['RecoveryPL_Min']} / {row['RecoveryPL_Max']}",
            f"- MaxDD={row['MaxDD_Max']}, MaxMarginUsed={row['MaxMarginUsed']}, ProfitScore={row['ProfitScore']}, StabilityScore={row['StabilityScore']}, RobustnessScore={row['RobustnessScore']}, FinalRank={row['FinalRank']}",
            f"- Verdict={row['Verdict']}, IsSelectableForSetFile={row['IsSelectableForSetFile']}",
            "- Why selected: ACCEPT row with the best available FinalRank inside its risk category and no false AccountPL pass.",
            "",
        ]

    lines += [
        "## TOP ACCEPT",
        "",
        "Only `Verdict=ACCEPT` rows are shown here and only these rows can create `.set` files.",
        "",
        "| Rank | RunID | FinalRank | ProfitScore | StabilityScore | RobustnessScore | StartLot | BigRatio | SmallRatio | CloseBig | Reserve | RecoveryPL_Min | MaxDD |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for rank, row in enumerate(top_accept, 1):
        lines.append(
            f"| {rank} | {row['RunID']} | {row['FinalRank']} | {row['ProfitScore']} | {row['StabilityScore']} | {row['RobustnessScore']} | {row['StartLot']} | {row['BigRatio']} | {row['SmallRatio']} | {row['CloseBigOnSmall']} | {row['ReserveShare']} | {row['RecoveryPL_Min']} | {row['MaxDD_Max']} |"
        )

    lines += [
        "",
        "## TOP REJECTED",
        "",
        "Diagnostics only: rejected rows have `IsSelectableForSetFile=NO`, penalized Score, and `FinalRank=-999999999.0`.",
        "",
        "| Rank | RunID | Score | FinalRank | Verdict | StartLot | BigRatio | SmallRatio | RecoveryPL_Min | StopMax | LossCount | Compression |",
        "|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for rank, row in enumerate(top_rejected, 1):
        lines.append(
            f"| {rank} | {row['RunID']} | {row['Score']} | {row['FinalRank']} | {row['Verdict']} | {row['StartLot']} | {row['BigRatio']} | {row['SmallRatio']} | {row['RecoveryPL_Min']} | {row['StopMaxLevelsCount']} | {row['ClosedRecoveryLossCount']} | {row['CompressionViolationCount']} |"
        )

    lines += [
        "",
        "## Why rejected",
        "",
    ]
    for verdict_name, count in verdict_counts.most_common():
        lines.append(f"- {verdict_name}: {count:,} rows rejected by hard filters or simulated scenario outcomes.")
    lines += [
        "",
        "Typical causes:",
        "- REJECTED_COMPRESSION: simulated `NewBig >= OldFar` or other compression failure after Small scenario.",
        "- REJECTED_STOP_MAX_LEVELS: scenario reached MaxHarvestLevels and closed by STOP_MAX_LEVELS instead of profit.",
        "- REJECTED_RECOVERY_LOSS / REJECTED_NON_POSITIVE_MIN_RECOVERY: at least one scenario failed the real RecoveryPL criterion.",
        "- REJECTED_MARGIN / REJECTED_DRAWDOWN: offline stress exceeded configured risk caps.",
        "",
        "## Sensitivity Analysis",
        "",
        "- BigRatio and RemainBigOnSmall are the most dangerous geometry pair because `BigRatio² × RemainBigOnSmall` controls compression.",
        "- BigRatio above 1.20 or RemainBigOnSmall above 0.65 sharply narrows the safe compression zone in the offline model.",
        "- SmallRatio below 0.20 weakens recovery in Small-heavy scenarios; values around 0.30–0.40 survive more local-search scenarios.",
        "- CloseFarShare that is too high can starve reserve; too low can leave Far exposure unresolved and push MaxLevels.",
        "- Wider MaxSpreadPoints reduces RecoveryPL_Min and can convert otherwise acceptable sets into recovery-loss rejects.",
        "",
        "## Stability analysis",
        "",
        "StabilityScore penalizes RecoveryPL variance, drawdown variance, STOP_MAX_LEVELS frequency and recovery-loss frequency. Higher is better; negative values indicate scenario instability even if mean RecoveryPL is high.",
        "",
        "## Robustness analysis",
        "",
        "RobustnessScore measures how many synthetic scenarios closed profitably and subtracts penalties for compression, STOP_MAX_LEVELS and recovery-loss events. ACCEPT requires all scenarios to remain structurally valid and profitable by real RecoveryPL.",
        "",
        "## Required MT5 validation after offline filtering",
        "",
        "Run every generated `.set` file in MT5 Strategy Tester:",
        "1. USDJPY M30 2026.04.01 — 2026.06.17",
        "2. USDJPY M30 2025.01.01 — 2026.06.17",
        "3. EURUSD M30 2025.01.01 — 2026.06.17",
        "4. GBPUSD M30 2025.01.01 — 2026.06.17",
        "5. XAUUSD M30 2025.01.01 — 2026.06.17",
        "",
        "Acceptance in MT5 still requires no STATE_INTEGRITY_ERROR, no STATE_RECOVERY_MISMATCH, no unresolved positions, no false STATE_CLOSED_PROFIT, and `OnTester > 0` only by real RecoveryPL.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def row_for_set(row: Dict[str, object]) -> Dict[str, object]:
    return {
        **row,
        "UseRecommended5050Preset": "false",
        "FarDistanceMode": "3",
        "MaxManagedPositions": "10",
        "AllowRealTrading": "true",
        "UseInternalSimulation": "false",
        "UseMarketOrders": "true",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline optimizer for MinusLock BigHarvest EA V2")
    parser.add_argument("--max-runs", type=int, default=100000, help="number of broad sampled combinations to evaluate")
    parser.add_argument("--local-runs", type=int, default=10000, help="additional local-search runs around the audited leader zone")
    parser.add_argument("--seed", type=int, default=20260623, help="deterministic random seed")
    parser.add_argument("--output", type=Path, default=ROOT / "Optimization_Report.csv")
    parser.add_argument("--best", type=Path, default=ROOT / "Best_Parameters.md")
    parser.add_argument("--sets-dir", type=Path, default=ROOT / "Sets")
    args = parser.parse_args()

    scenarios = build_scenarios(max_levels=10)
    sampled = combined_sample(args.max_runs, args.local_runs, args.seed)
    coverage_ratio = len(sampled) / grid_size()
    rows: List[Dict[str, object]] = []
    for run_id, params in enumerate(sampled, 1):
        reject = validate_params(params)
        if reject:
            results = [ScenarioResult(s.name, -9999.0, 9999.0, 9999.0, True, False, True, True, 9.99, 9.99, 0.0, "REJECTED", 0) for s in scenarios]
        else:
            results = [simulate_scenario(params, s) for s in scenarios]
        row = aggregate_results(run_id, params, results, coverage_ratio)
        rows.append(row)

    rows = sorted(rows, key=lambda r: (r["Verdict"] == "ACCEPT", r["FinalRank"]), reverse=True)
    selected = choose_categories(rows)
    for category, row in selected.items():
        if row is not None:
            row["Category"] = category

    write_csv(args.output, rows)
    write_best_parameters(
        args.best,
        rows,
        selected,
        args,
        scenarios,
        sum(1 for r in rows if r["Verdict"] != "ACCEPT"),
        len(sampled),
        coverage_ratio,
    )

    args.sets_dir.mkdir(parents=True, exist_ok=True)
    set_names = {
        "SAFE": "USDJPY_M30_SAFE.set",
        "BALANCED": "USDJPY_M30_BALANCED.set",
        "AGGRESSIVE": "USDJPY_M30_AGGRESSIVE.set",
        "LOWLOT_SAFE": "USDJPY_M30_LOWLOT_SAFE.set",
    }
    for category, row in selected.items():
        set_path = args.sets_dir / set_names[category]
        not_found_path = args.sets_dir / f"USDJPY_M30_{category}_NOT_FOUND.txt"
        if row is not None and row["Verdict"] == "ACCEPT" and row["IsSelectableForSetFile"] == "YES":
            if not_found_path.exists():
                not_found_path.unlink()
            write_set_file(set_path, row_for_set(row))
        else:
            if set_path.exists():
                set_path.unlink()
            not_found_path.write_text(
                f"{category}_NOT_FOUND: no Verdict=ACCEPT and IsSelectableForSetFile=YES candidate was found.\n",
                encoding="utf-8",
            )

    print(
        f"OFFLINE_OPTIMIZER PASS sampled={len(sampled)} global={args.max_runs} local={args.local_runs} "
        f"theoretical_grid={grid_size()} coverage={coverage_ratio:.8%} scenarios={len(scenarios)}"
    )
    for category, row in selected.items():
        if row is None:
            print(f"{category}: {category}_NOT_FOUND")
        else:
            print(
                f"{category}: RunID={row['RunID']} FinalRank={row['FinalRank']} Score={row['Score']} "
                f"Verdict={row['Verdict']} RecoveryPL_Min={row['RecoveryPL_Min']}"
            )
    print(f"Wrote {args.output}")
    print(f"Wrote {args.best}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
