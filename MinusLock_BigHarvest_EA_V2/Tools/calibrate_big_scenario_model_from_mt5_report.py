#!/usr/bin/env python3
"""Calibrate the Big-scenario Python model from the supplied MT5 tester report.

The report text supplied by the administrator is treated as source-of-truth data.
This utility reconstructs the first material divergence and exports calibration
constants used by the optimizer: dynamic point value, realized Far loss per lot,
end-of-test failure markers, and level-by-level MT5 lot/deal facts.
"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "Reports"
DIFF_MD = REPORTS / "Python_vs_MT5_BigScenario_Diff.md"
DIFF_CSV = REPORTS / "Python_vs_MT5_BigScenario_Diff.csv"

START_LOT = 1.00
LOT_STEP = 0.01
BIG_RATIO = 1.11
SMALL_RATIO = 0.25
CLOSE_FAR_SHARE = 0.75
RESERVE_SHARE = 0.25
BIG_MOVE_START_POINTS = 250
FAR_DISTANCE_POINTS = 180
OLD_POINT_VALUE_PER_LOT = 1.0
OLD_OFFLINE_MODEL_STATUS = "OLD_OFFLINE_MODEL_INVALID_FOR_FINAL_SELECTION"

MT5_INITIAL_BUY_PROFIT = 108.27
MT5_CYCLE_START_BALANCE = 10108.27
MT5_ON_TESTER = -1
MT5_FINAL_STATE = "END_OF_TEST_WITH_OPEN_MANAGED_POSITIONS"
MT5_END_REASON = "END_OF_TEST"
MT5_LEVEL_REACHED = 11
MT5_INITIAL_FAR_OPEN = 154.889
MT5_BIG_L1_OPEN = 155.149
MT5_SMALL_L1_OPEN = 155.127
MT5_BIG_L1_CLOSE = 155.394
MT5_SMALL_L1_CLOSE = 155.396
MT5_FAR_L1_PARTIAL_CLOSE = 155.386
MT5_CLOSED_BIG_NET = 147.73
MT5_CLOSED_SMALL_NET = -40.90
MT5_FAR_PARTIAL_LOT = 0.29
MT5_FAR_PARTIAL_REAL_LOSS = 78.27

MT5_LEVEL_LOTS = [
    (1, 1.11, 0.28), (2, 0.79, 0.20), (3, 0.52, 0.13),
    (4, 0.34, 0.09), (5, 0.27, 0.07), (6, 0.18, 0.05),
    (7, 0.14, 0.04), (8, 0.12, 0.03), (9, 0.11, 0.03),
    (10, 0.10, 0.03), (11, 0.07, 0.02),
]


def round_down(value: float, step: float = LOT_STEP) -> float:
    import math
    if value <= 0:
        return 0.0
    return round(math.floor((value + 1e-12) / step) * step, 8)


@dataclass(frozen=True)
class Calibration:
    point_value_per_lot: float
    far_loss_per_lot_l1: float
    mt5_big_scenario_net_l1: float
    mt5_close_far_budget_l1: float
    mt5_reserve_add_l1: float
    mt5_far_after_l1: float
    mt5_reserve_after_l1: float
    mt5_recovery_pl_est_l1: float
    mt5_reserve_coverage_est_l1: float
    mt5_level_reached: int
    mt5_on_tester: int
    mt5_end_reason: str


@dataclass(frozen=True)
class DiffRow:
    Level: int
    PythonBigLot: float
    MT5BigLot: float
    PythonSmallLot: float
    MT5SmallLot: float
    PythonBigScenarioNet: float
    MT5BigScenarioNet: float
    PythonFarAfter: float
    MT5FarAfter: float
    PythonReserve: float
    MT5Reserve: float
    Diff: str


def build_calibration() -> Calibration:
    mt5_big_points = abs(MT5_BIG_L1_CLOSE - MT5_BIG_L1_OPEN) / 0.001
    point_value = MT5_CLOSED_BIG_NET / (1.11 * mt5_big_points)
    mt5_net = MT5_CLOSED_BIG_NET + MT5_CLOSED_SMALL_NET
    mt5_budget = mt5_net * CLOSE_FAR_SHARE
    mt5_reserve = mt5_net * RESERVE_SHARE
    far_loss_per_lot = MT5_FAR_PARTIAL_REAL_LOSS / MT5_FAR_PARTIAL_LOT
    mt5_far_after = round(START_LOT - MT5_FAR_PARTIAL_LOT, 2)
    remaining_loss = mt5_far_after * far_loss_per_lot
    return Calibration(
        point_value_per_lot=round(point_value, 8),
        far_loss_per_lot_l1=round(far_loss_per_lot, 8),
        mt5_big_scenario_net_l1=round(mt5_net, 8),
        mt5_close_far_budget_l1=round(mt5_budget, 8),
        mt5_reserve_add_l1=round(mt5_reserve, 8),
        mt5_far_after_l1=mt5_far_after,
        mt5_reserve_after_l1=round(mt5_reserve, 8),
        mt5_recovery_pl_est_l1=round(mt5_reserve - remaining_loss, 8),
        mt5_reserve_coverage_est_l1=round(mt5_reserve / remaining_loss, 8),
        mt5_level_reached=MT5_LEVEL_REACHED,
        mt5_on_tester=MT5_ON_TESTER,
        mt5_end_reason=MT5_END_REASON,
    )


def build_diff_rows(cal: Calibration) -> list[DiffRow]:
    py_big_lot = round(START_LOT * BIG_RATIO, 2)
    py_small_lot = 0.28
    py_net = py_big_lot * BIG_MOVE_START_POINTS * OLD_POINT_VALUE_PER_LOT - py_small_lot * BIG_MOVE_START_POINTS * OLD_POINT_VALUE_PER_LOT
    py_budget = py_net * CLOSE_FAR_SHARE
    py_reserve = py_net * RESERVE_SHARE
    py_far_after = round_down(START_LOT - round_down(py_budget / FAR_DISTANCE_POINTS))
    rows = [DiffRow(
        Level=1,
        PythonBigLot=py_big_lot,
        MT5BigLot=1.11,
        PythonSmallLot=py_small_lot,
        MT5SmallLot=0.28,
        PythonBigScenarioNet=round(py_net, 2),
        MT5BigScenarioNet=round(cal.mt5_big_scenario_net_l1, 2),
        PythonFarAfter=py_far_after,
        MT5FarAfter=cal.mt5_far_after_l1,
        PythonReserve=round(py_reserve, 2),
        MT5Reserve=round(cal.mt5_reserve_after_l1, 2),
        Diff="FIRST_MATERIAL_DIVERGENCE: Python overstates net/budget and predicts FINAL_CLOSE; MT5 opens BIG_L2",
    )]
    remaining_far = cal.mt5_far_after_l1
    reserve = cal.mt5_reserve_after_l1
    for level, big_lot, small_lot in MT5_LEVEL_LOTS[1:]:
        rows.append(DiffRow(
            Level=level,
            PythonBigLot=0.0,
            MT5BigLot=big_lot,
            PythonSmallLot=0.0,
            MT5SmallLot=small_lot,
            PythonBigScenarioNet=0.0,
            MT5BigScenarioNet=0.0,
            PythonFarAfter=0.0,
            MT5FarAfter=round(remaining_far, 2),
            PythonReserve=0.0,
            MT5Reserve=round(reserve, 2),
            Diff="OLD_PYTHON_ALREADY_STOPPED; MT5_CONTINUED_LEVEL_SEQUENCE",
        ))
    return rows


def write_outputs(cal: Calibration, rows: list[DiffRow]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    with DIFF_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    lines = [
        "# Python vs MT5 BigScenario Diff",
        "",
        f"Status: `{OLD_OFFLINE_MODEL_STATUS}`.",
        "",
        "The administrator-supplied MT5 Strategy Tester report is the calibration source. The old Python model is not allowed to be used as the final selector because it predicted `LevelsUsed=1 / STATE_CLOSED_PROFIT` while MT5 reached `BIG_L11`, returned `OnTester=-1`, and closed remaining exposure only by `END_OF_TEST` forced deals.",
        "",
        "## Recovered MT5 calibration fields",
        "",
        f"- InitialIgnoredProfit: `{MT5_INITIAL_BUY_PROFIT}`.",
        f"- CycleStartBalance: `{MT5_CYCLE_START_BALANCE}`.",
        f"- RecoveryPL estimate after L1: `{cal.mt5_recovery_pl_est_l1}`.",
        f"- Big levels observed: `BIG_L1` ... `BIG_L{cal.mt5_level_reached}`.",
        f"- L1 partial Far close: `{MT5_FAR_PARTIAL_LOT}` lot for loss `{MT5_FAR_PARTIAL_REAL_LOSS}`.",
        f"- Far remaining after L1: `{cal.mt5_far_after_l1}`.",
        f"- Reserve after L1: `{cal.mt5_reserve_after_l1}`.",
        f"- Final state: `{MT5_FINAL_STATE}`.",
        f"- End reason: `{cal.mt5_end_reason}`.",
        f"- Dynamic point value per lot calibrated from MT5 L1 Big deal: `{cal.point_value_per_lot}`.",
        f"- Far loss per lot calibrated from MT5 L1 Far partial close: `{cal.far_loss_per_lot_l1}`.",
        "",
        "## Level diff",
        "",
        "| Level | Python BigLot | MT5 BigLot | Python SmallLot | MT5 SmallLot | Python BigScenarioNet | MT5 BigScenarioNet | Python FarAfter | MT5 FarAfter | Python Reserve | MT5 Reserve | Diff |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(f"| {row.Level} | {row.PythonBigLot} | {row.MT5BigLot} | {row.PythonSmallLot} | {row.MT5SmallLot} | {row.PythonBigScenarioNet} | {row.MT5BigScenarioNet} | {row.PythonFarAfter} | {row.MT5FarAfter} | {row.PythonReserve} | {row.MT5Reserve} | {row.Diff} |")
    lines += [
        "",
        "## First divergence",
        "",
        "The first divergence is level 1 `BigScenarioNet`: Python calculated `207.50`, MT5 realized `106.83`. Because of this, Python overestimated `CloseFarBudget`, closed `0.86` Far lot in the model, and declared `STATE_CLOSED_PROFIT`; MT5 could close only `0.29` Far lot and opened `BIG_L2`.",
        "",
        "## Mandatory optimizer rule",
        "",
        "Any parameter profile matching this MT5-invalidated signature must be scored as failed: `END_OF_TEST`, `OnTester=-1`, `RemainingFarLot>0`, and `BIG_L9+` are hard penalties. Final rows may be called only `MT5_CANDIDATE_NOT_CONFIRMED` until a new MT5 Strategy Tester run confirms them.",
        "",
    ]
    DIFF_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    cal = build_calibration()
    rows = build_diff_rows(cal)
    write_outputs(cal, rows)
    print(f"BIG_SCENARIO_MT5_CALIBRATION_PASS diff={DIFF_MD} csv={DIFF_CSV}")
    print(f"status={OLD_OFFLINE_MODEL_STATUS}")
    print(f"point_value_per_lot={cal.point_value_per_lot} far_loss_per_lot={cal.far_loss_per_lot_l1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
