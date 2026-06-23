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
import itertools
import math
import random
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from typing import Dict, Iterable, Iterator, List, Tuple

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
    "ClosedRecoveryLossCount", "CompressionRatio", "NewBigToOldFarRatio", "Score", "Verdict",
]


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


def aggregate_results(run_id: int, p: Params, results: List[ScenarioResult]) -> Dict[str, object]:
    pls = [r.recovery_pl for r in results]
    dds = [r.max_dd for r in results]
    gross_profit = sum(x for x in pls if x > 0.0)
    gross_loss = abs(sum(x for x in pls if x < 0.0))
    max_dd = max(dds) if dds else 0.0
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
        StopMaxLevelsCount=sum(r.stop_max for r in results),
        ClosedProfitCount=sum(r.closed_profit for r in results),
        ClosedRecoveryLossCount=sum(r.closed_recovery_loss for r in results),
        CompressionViolationCount=sum(r.compression_violation for r in results),
        CompressionRatio=round(max(r.compression_ratio for r in results), 4),
        NewBigToOldFarRatio=round(max(r.new_big_to_old_far_ratio for r in results), 4),
        ProfitFactorOffline=round(gross_profit / gross_loss, 4) if gross_loss > 0.0 else round(gross_profit, 4),
        RecoveryFactorOffline=round(mean(pls) / max_dd, 4) if max_dd > 0.0 else round(mean(pls), 4),
        MaxAllowedDD=INITIAL_DEPOSIT * p.MaxDrawdownPercent / 100.0,
        MaxAllowedMargin=INITIAL_DEPOSIT * p.MaxMarginPercent / 100.0,
        RejectedReason=validate_params(p),
    )
    metrics["Score"] = score_candidate(metrics)
    metrics["Verdict"] = verdict(metrics)
    return metrics


def grid_size() -> int:
    return math.prod(len(v) for v in RANGES.values())


def iter_full_grid() -> Iterator[Params]:
    keys = list(RANGES)
    for values in itertools.product(*(RANGES[k] for k in keys)):
        raw = dict(zip(keys, values))
        close_big, remain_big = raw.pop("ClosePair")
        close_far, reserve = raw.pop("ReservePair")
        yield Params(CloseBigOnSmall=close_big, RemainBigOnSmall=remain_big, CloseFarShare=close_far, ReserveShare=reserve, **raw)


def sample_params(limit: int, seed: int) -> List[Params]:
    """Deterministically sample a large grid while covering every allowed value."""
    rng = random.Random(seed)
    keys = list(RANGES)
    generated: List[Params] = []
    seen = set()

    def build(raw: dict) -> Params:
        raw = dict(raw)
        close_big, remain_big = raw.pop("ClosePair")
        close_far, reserve = raw.pop("ReservePair")
        return Params(CloseBigOnSmall=close_big, RemainBigOnSmall=remain_big, CloseFarShare=close_far, ReserveShare=reserve, **raw)

    # Coverage pass: each range value is forced into at least one sampled combination.
    for key in keys:
        for value in RANGES[key]:
            raw = {k: rng.choice(RANGES[k]) for k in keys}
            raw[key] = value
            p = build(raw)
            if p not in seen:
                generated.append(p)
                seen.add(p)

    while len(generated) < limit:
        raw = {k: rng.choice(RANGES[k]) for k in keys}
        p = build(raw)
        if p not in seen:
            generated.append(p)
            seen.add(p)
    return generated


def choose_categories(rows: List[Dict[str, object]]) -> Dict[str, Dict[str, object]]:
    """Pick distinct category representatives.

    Safe/Balanced/LowLot are chosen from ACCEPT rows whenever available.
    Aggressive may be a stress candidate if no high-lot row survives every
    offline scenario; the report keeps its Verdict so MT5 users see the risk.
    """
    accepted = [r for r in rows if r["Verdict"] == "ACCEPT"]
    score_sorted = sorted(accepted or rows, key=lambda r: r["Score"], reverse=True)
    used: set[int] = set()

    def pick(pool: List[Dict[str, object]], key, reverse=True) -> Dict[str, object]:
        candidates = [r for r in pool if int(r["RunID"]) not in used]
        if not candidates:
            candidates = pool or score_sorted
        row = sorted(candidates, key=key, reverse=reverse)[0]
        used.add(int(row["RunID"]))
        return row

    safe_pool = [r for r in accepted if r["StartLot"] <= 0.10 and r["MaxDD_Max"] <= 120 and r["MaxMarginUsed"] <= 2500]
    balanced_pool = [r for r in accepted if r["RecoveryPL_Min"] > 0.0]
    lowlot_pool = [r for r in accepted if r["StartLot"] in (0.01, 0.05, 0.10)]
    aggressive_pool = [r for r in accepted if r["StartLot"] >= 0.50]
    if not aggressive_pool:
        aggressive_pool = [r for r in rows if r["StartLot"] >= 0.50 and r["CompressionViolationCount"] == 0]

    return {
        "SAFE": pick(safe_pool or score_sorted, key=lambda r: (-r["MaxDD_Max"], r["Score"], r["RecoveryPL_Min"])),
        "BALANCED": pick(balanced_pool or score_sorted, key=lambda r: (r["Score"], r["RecoveryPL_Min"])),
        "AGGRESSIVE": pick(aggressive_pool or score_sorted, key=lambda r: (r["Verdict"] == "ACCEPT", r["StartLot"], r["Score"])),
        "LOWLOT_SAFE": pick(lowlot_pool or score_sorted, key=lambda r: (-r["StartLot"], -r["MaxDD_Max"], r["Score"])),
    }


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_best_parameters(path: Path, rows: List[Dict[str, object]], selected: Dict[str, Dict[str, object]], args, scenarios: List[Scenario], rejected_count: int) -> None:
    top20 = sorted(rows, key=lambda r: r["Score"], reverse=True)[:20]
    lines = [
        "# Offline Best Parameters for MinusLock_BigHarvest_EA_V2",
        "",
        "## Scope and limitations",
        "",
        "This report is generated without MT5. It is a deterministic offline filter, not a replacement for MetaTrader Strategy Tester.",
        "It uses the strict success rule `RecoveryPL = FinalBalance - CycleStartBalance`; AccountPL versus InitialDeposit is diagnostic only.",
        "InitialIgnoredProfit is excluded from pass/fail, matching the EA realRecoveryPL / OnTester contract.",
        "",
        "## Optimization model",
        "",
        f"- Synthetic scenarios: {scenario_names(scenarios)}.",
        f"- Sampled combinations: {args.max_runs:,} from a theoretical grid of {grid_size():,} combinations.",
        f"- Mathematically rejected or unstable rows in CSV: {rejected_count:,}.",
        "- P/L model: `Lot × Points × PointValuePerLot` minus spread/slippage/commission costs.",
        "- Compression filter: `BigRatio² × RemainBigOnSmall < 1` plus simulated `NewBig < OldFar` checks.",
        "- STOP_MAX_LEVELS, STATE_CLOSED_RECOVERY_LOSS, compression violations and drawdown/margin breaches receive hard penalties.",
        "",
        "## Selected parameter sets",
        "",
    ]
    for category, row in selected.items():
        lines += [
            f"### {category}",
            "",
            f"- StartLot={row['StartLot']}, BigRatio={row['BigRatio']}, SmallRatio={row['SmallRatio']}",
            f"- CloseBigOnSmall={row['CloseBigOnSmall']} / RemainBigOnSmall={row['RemainBigOnSmall']}",
            f"- CloseFarShare={row['CloseFarShare']} / ReserveShare={row['ReserveShare']}, SmallReserveShare={row['SmallReserveShare']}",
            f"- Trigger/steps: Initial={row['InitialTriggerPoints']}, BigStart={row['BigMoveStartPoints']}, BigStep={row['BigMoveStepPoints']}, FarDistance={row['FarDistancePoints']}",
            f"- MaxHarvestLevels={row['MaxHarvestLevels']}, MaxReverseCycles={row['MaxReverseCycles']}, MaxSpreadPoints={row['MaxSpreadPoints']}",
            f"- RecoveryPL mean/min/max: {row['RecoveryPL_Mean']} / {row['RecoveryPL_Min']} / {row['RecoveryPL_Max']}",
            f"- MaxDD={row['MaxDD_Max']}, MaxMarginUsed={row['MaxMarginUsed']}, Score={row['Score']}, Verdict={row['Verdict']}",
            ("- Why selected: ACCEPT row with the best available score inside its risk category and no false AccountPL pass."
             if row["Verdict"] == "ACCEPT"
             else "- Why selected: stress-only candidate; offline model rejects it, so it must not be treated as a default until MT5 proves recovery profitability."),
            "",
        ]
    lines += [
        "## Top-20 by score",
        "",
        "| Rank | RunID | Score | Verdict | StartLot | BigRatio | SmallRatio | CloseBig | Reserve | RecoveryPL_Min | MaxDD | StopMax | LossCount |",
        "|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for rank, row in enumerate(top20, 1):
        lines.append(
            f"| {rank} | {row['RunID']} | {row['Score']} | {row['Verdict']} | {row['StartLot']} | {row['BigRatio']} | {row['SmallRatio']} | {row['CloseBigOnSmall']} | {row['ReserveShare']} | {row['RecoveryPL_Min']} | {row['MaxDD_Max']} | {row['StopMaxLevelsCount']} | {row['ClosedRecoveryLossCount']} |"
        )
    lines += [
        "",
        "## Rejected parameter causes",
        "",
        "Rows are rejected for failed compression math, simulated `NewBig >= OldFar`, margin/drawdown pressure, STOP_MAX_LEVELS, closed recovery loss, or non-positive minimum recovery across scenarios.",
        "The most sensitive parameters are BigRatio, RemainBigOnSmall, FarDistancePoints, MaxHarvestLevels and CloseFarShare/ReserveShare.",
        "Do not raise BigRatio or RemainBigOnSmall until `BigRatio² × RemainBigOnSmall < 1` and simulated `NewBig < OldFar` still hold.",
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
    parser.add_argument("--max-runs", type=int, default=25000, help="number of sampled combinations to evaluate")
    parser.add_argument("--seed", type=int, default=20260623, help="deterministic random seed")
    parser.add_argument("--output", type=Path, default=ROOT / "Optimization_Report.csv")
    parser.add_argument("--best", type=Path, default=ROOT / "Best_Parameters.md")
    parser.add_argument("--sets-dir", type=Path, default=ROOT / "Sets")
    args = parser.parse_args()

    scenarios = build_scenarios(max_levels=10)
    rows: List[Dict[str, object]] = []
    for run_id, params in enumerate(sample_params(args.max_runs, args.seed), 1):
        reject = validate_params(params)
        if reject:
            results = [ScenarioResult(s.name, -9999.0, 9999.0, 9999.0, True, False, True, True, 9.99, 9.99, 0.0, "REJECTED", 0) for s in scenarios]
        else:
            results = [simulate_scenario(params, s) for s in scenarios]
        row = aggregate_results(run_id, params, results)
        rows.append(row)

    rows = sorted(rows, key=lambda r: r["Score"], reverse=True)
    selected = choose_categories(rows)
    for category, row in selected.items():
        row["Category"] = category

    write_csv(args.output, rows)
    write_best_parameters(args.best, rows, selected, args, scenarios, sum(1 for r in rows if r["Verdict"] != "ACCEPT"))

    set_names = {
        "SAFE": "USDJPY_M30_SAFE.set",
        "BALANCED": "USDJPY_M30_BALANCED.set",
        "AGGRESSIVE": "USDJPY_M30_AGGRESSIVE.set",
        "LOWLOT_SAFE": "USDJPY_M30_LOWLOT_SAFE.set",
    }
    for category, row in selected.items():
        write_set_file(args.sets_dir / set_names[category], row_for_set(row))

    print(f"OFFLINE_OPTIMIZER PASS sampled={args.max_runs} theoretical_grid={grid_size()} scenarios={len(scenarios)}")
    for category, row in selected.items():
        print(f"{category}: RunID={row['RunID']} Score={row['Score']} Verdict={row['Verdict']} RecoveryPL_Min={row['RecoveryPL_Min']}")
    print(f"Wrote {args.output}")
    print(f"Wrote {args.best}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
