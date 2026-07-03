#!/usr/bin/env python3
"""Trace Big-scenario math without MT5.

Approved model:
    BigScenarioNet = ClosedBigNet + ClosedSmallNet
    CloseFarBudget = BigScenarioNet * CloseFarShare
    ReserveAdd = BigScenarioNet * ReserveShare

The simulator deliberately does not import EA code or change trading logic. It is an
independent trace tool for audit, CSV and Markdown reporting.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "Reports"
CSV_PATH = REPORTS / "BigScenario_Trace.csv"
MD_PATH = REPORTS / "BigScenario_Trace_Report.md"


def round_nearest(value: float, step: float) -> float:
    return round(round(value / step) * step, 8) if value > 0 and step > 0 else 0.0


def round_up(value: float, step: float) -> float:
    if value <= 0 or step <= 0:
        return 0.0
    import math
    return round(math.ceil((value - 1e-12) / step) * step, 8)


def round_down(value: float, step: float) -> float:
    if value <= 0 or step <= 0:
        return 0.0
    import math
    return round(math.floor((value + 1e-12) / step) * step, 8)


@dataclass
class TraceRow:
    Scenario: str
    Level: int
    FarLotBefore: float
    BigLot: float
    SmallLot: float
    ClosedBigNet: float
    ClosedSmallNet: float
    BigScenarioNet: float
    CloseFarShare: float
    ReserveShare: float
    CloseFarBudget: float
    ReserveAdd: float
    CloseFarLotRaw: float
    CloseFarLotRounded: float
    CloseFarActualCost: float
    FarLotAfter: float
    ReserveAfter: float
    RecoveryPL: float
    ReserveCoverage: float
    CanFinalClose: str
    NextAction: str
    InvariantStatus: str


def check_invariants(row: TraceRow, previous_reserve: float, lot_step: float) -> None:
    eps = 1e-7
    assert abs(row.BigScenarioNet - (row.ClosedBigNet + row.ClosedSmallNet)) <= eps, row
    assert abs(row.CloseFarBudget - row.BigScenarioNet * row.CloseFarShare) <= eps, row
    assert abs(row.ReserveAdd - row.BigScenarioNet * row.ReserveShare) <= eps, row
    assert abs((row.CloseFarBudget + row.ReserveAdd) - row.BigScenarioNet) <= eps, row
    assert row.CloseFarActualCost <= row.CloseFarBudget + eps, row
    assert row.ReserveAfter >= previous_reserve - eps, row
    assert abs(row.FarLotAfter - round_down(row.FarLotBefore - row.CloseFarLotRounded, lot_step)) <= eps, row
    assert row.CloseFarLotRounded <= row.FarLotBefore + eps, row


def simulate(
    *,
    scenario: str,
    start_lot: float,
    big_ratio: float,
    small_ratio: float,
    close_far_share: float,
    reserve_share: float,
    close_big_on_small: float,
    remain_big_on_small: float,
    lot_step: float,
    point_value_per_lot: float,
    far_distance_points: float,
    big_move_points: float,
    max_levels: int,
) -> list[TraceRow]:
    if abs(close_far_share + reserve_share - 1.0) > 1e-9:
        raise ValueError("CloseFarShare + ReserveShare must equal 1.0")
    if abs(close_big_on_small + remain_big_on_small - 1.0) > 1e-9:
        raise ValueError("CloseBigOnSmall + RemainBigOnSmall must equal 1.0")

    far_lot = start_lot
    reserve = 0.0
    rows: list[TraceRow] = []
    far_loss_per_lot = far_distance_points * point_value_per_lot

    for level in range(1, max_levels + 1):
        far_before = far_lot
        big_lot = round_nearest(far_before * big_ratio, lot_step)
        small_lot = round_up(big_lot * small_ratio, lot_step)
        closed_big_net = round(big_lot * big_move_points * point_value_per_lot, 8)
        closed_small_net = round(-small_lot * big_move_points * point_value_per_lot, 8)
        big_scenario_net = round(closed_big_net + closed_small_net, 8)
        close_far_budget = round(big_scenario_net * close_far_share, 8) if big_scenario_net > 0 else 0.0
        reserve_add = round(big_scenario_net * reserve_share, 8) if big_scenario_net > 0 else 0.0
        close_far_lot_raw = close_far_budget / far_loss_per_lot if far_loss_per_lot > 0 else 0.0
        close_far_lot_rounded = min(round_down(close_far_lot_raw, lot_step), far_before)
        close_far_actual_cost = round(close_far_lot_rounded * far_loss_per_lot, 8)
        far_after = round_down(max(0.0, far_before - close_far_lot_rounded), lot_step)
        previous_reserve = reserve
        reserve = round(reserve + reserve_add, 8)
        remaining_loss = round(far_after * far_loss_per_lot, 8)
        recovery_pl = round(reserve - remaining_loss, 8)
        reserve_coverage = round(reserve / remaining_loss, 8) if remaining_loss > 0 else 999.0
        can_final_close = reserve >= remaining_loss and far_after > 0
        if far_after <= 0:
            next_action = "CYCLE_CLOSED_FAR_ZERO"
        elif can_final_close:
            next_action = "FINAL_CLOSE"
        elif level >= max_levels:
            next_action = "STOP_MAX_LEVELS"
        else:
            next_action = "NEXT_BIG_LEVEL"

        row = TraceRow(
            Scenario=scenario,
            Level=level,
            FarLotBefore=round(far_before, 8),
            BigLot=big_lot,
            SmallLot=small_lot,
            ClosedBigNet=closed_big_net,
            ClosedSmallNet=closed_small_net,
            BigScenarioNet=big_scenario_net,
            CloseFarShare=close_far_share,
            ReserveShare=reserve_share,
            CloseFarBudget=close_far_budget,
            ReserveAdd=reserve_add,
            CloseFarLotRaw=round(close_far_lot_raw, 8),
            CloseFarLotRounded=close_far_lot_rounded,
            CloseFarActualCost=close_far_actual_cost,
            FarLotAfter=far_after,
            ReserveAfter=reserve,
            RecoveryPL=recovery_pl,
            ReserveCoverage=reserve_coverage,
            CanFinalClose="YES" if can_final_close else "NO",
            NextAction=next_action,
            InvariantStatus="PASS",
        )
        check_invariants(row, previous_reserve, lot_step)
        rows.append(row)
        far_lot = far_after
        if next_action in {"FINAL_CLOSE", "CYCLE_CLOSED_FAR_ZERO", "STOP_MAX_LEVELS"}:
            break

    return rows


def summarize(rows: list[TraceRow]) -> dict[str, float | int | str]:
    return {
        "Scenario": rows[0].Scenario,
        "LevelsToFinalClose": len(rows),
        "TotalClosedFarLot": round(sum(r.CloseFarLotRounded for r in rows), 8),
        "RemainingFarLot": rows[-1].FarLotAfter,
        "ReserveAfter": rows[-1].ReserveAfter,
        "RecoveryPL": rows[-1].RecoveryPL,
        "ReserveCoverage": rows[-1].ReserveCoverage,
        "FinalAction": rows[-1].NextAction,
    }


def write_csv(rows: Iterable[TraceRow], path: Path = CSV_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_report(rows_by_scenario: dict[str, list[TraceRow]], path: Path = MD_PATH) -> None:
    lines: list[str] = []
    lines.append("# Big Scenario Trace Report")
    lines.append("")
    lines.append("## Approved model")
    lines.append("")
    lines.append("`BigScenarioNet = ClosedBigNet + ClosedSmallNet` is the approved Big-scenario harvest base. The simulator verifies that `CloseFarBudget` and `ReserveAdd` are calculated only from `BigScenarioNet`, and that reserve is not used for partial Far close.")
    lines.append("")
    for scenario, rows in rows_by_scenario.items():
        lines.append(f"## Trace: {scenario}")
        lines.append("")
        lines.append("| Level | FarLotBefore | BigLot | SmallLot | ClosedBigNet | ClosedSmallNet | BigScenarioNet | CloseFarBudget | ReserveAdd | CloseFarLotRounded | FarLotAfter | ReserveAfter | RecoveryPL | ReserveCoverage | NextAction |")
        lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for r in rows:
            lines.append(f"| {r.Level} | {r.FarLotBefore:.2f} | {r.BigLot:.2f} | {r.SmallLot:.2f} | {r.ClosedBigNet:.2f} | {r.ClosedSmallNet:.2f} | {r.BigScenarioNet:.2f} | {r.CloseFarBudget:.2f} | {r.ReserveAdd:.2f} | {r.CloseFarLotRounded:.2f} | {r.FarLotAfter:.2f} | {r.ReserveAfter:.2f} | {r.RecoveryPL:.2f} | {r.ReserveCoverage:.4f} | {r.NextAction} |")
        lines.append("")
        summary = summarize(rows)
        lines.append(f"Summary: TotalClosedFarLot={summary['TotalClosedFarLot']}, RemainingFarLot={summary['RemainingFarLot']}, ReserveAfter={summary['ReserveAfter']}, LevelsToFinalClose={summary['LevelsToFinalClose']}, RecoveryPL={summary['RecoveryPL']}, ReserveCoverage={summary['ReserveCoverage']}, FinalAction={summary['FinalAction']}.")
        lines.append("")
    if "90_10" in rows_by_scenario and "20_80" in rows_by_scenario:
        s90 = summarize(rows_by_scenario["90_10"])
        s20 = summarize(rows_by_scenario["20_80"])
        lines.append("## 90/10 vs 20/80 comparison")
        lines.append("")
        lines.append("| Metric | 90/10 | 20/80 | Expected profile |")
        lines.append("|---|---:|---:|---|")
        lines.append(f"| TotalClosedFarLot | {s90['TotalClosedFarLot']} | {s20['TotalClosedFarLot']} | 90/10 closes Far faster |")
        lines.append(f"| RemainingFarLot | {s90['RemainingFarLot']} | {s20['RemainingFarLot']} | 90/10 leaves less Far |")
        lines.append(f"| ReserveAfter | {s90['ReserveAfter']} | {s20['ReserveAfter']} | 20/80 builds reserve faster |")
        lines.append(f"| LevelsToFinalClose | {s90['LevelsToFinalClose']} | {s20['LevelsToFinalClose']} | profile-dependent |")
        lines.append(f"| RecoveryPL | {s90['RecoveryPL']} | {s20['RecoveryPL']} | reserve/Far tradeoff |")
        lines.append(f"| ReserveCoverage | {s90['ReserveCoverage']} | {s20['ReserveCoverage']} | profile-dependent |")
        lines.append("")
        lines.append("Conclusion: 90/10 maximizes the part of `BigScenarioNet` allocated to partial Far close and does not use reserve for that partial close. 20/80 accumulates reserve faster but reduces Far more slowly.")
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def default_runs(args: argparse.Namespace) -> dict[str, list[TraceRow]]:
    common = dict(
        start_lot=args.start_lot,
        big_ratio=args.big_ratio,
        small_ratio=args.small_ratio,
        close_big_on_small=args.close_big_on_small,
        remain_big_on_small=args.remain_big_on_small,
        lot_step=args.lot_step,
        point_value_per_lot=args.point_value_per_lot,
        far_distance_points=args.far_distance_points,
        big_move_points=args.big_move_points,
        max_levels=args.max_levels,
    )
    return {
        "90_10": simulate(scenario="90_10", close_far_share=0.90, reserve_share=0.10, **common),
        "20_80": simulate(scenario="20_80", close_far_share=0.20, reserve_share=0.80, **common),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate Big-scenario trace without MT5")
    parser.add_argument("--start-lot", type=float, default=1.00)
    parser.add_argument("--big-ratio", type=float, default=1.15)
    parser.add_argument("--small-ratio", type=float, default=0.25)
    parser.add_argument("--close-far-share", type=float, default=None)
    parser.add_argument("--reserve-share", type=float, default=None)
    parser.add_argument("--close-big-on-small", type=float, default=0.40)
    parser.add_argument("--remain-big-on-small", type=float, default=0.60)
    parser.add_argument("--lot-step", type=float, default=0.01)
    parser.add_argument("--point-value-per-lot", type=float, default=1.0)
    parser.add_argument("--far-distance-points", type=float, default=200.0)
    parser.add_argument("--big-move-points", type=float, default=100.0)
    parser.add_argument("--max-levels", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.close_far_share is not None or args.reserve_share is not None:
        if args.close_far_share is None or args.reserve_share is None:
            raise SystemExit("Both --close-far-share and --reserve-share are required for custom run")
        rows_by_scenario = {
            "custom": simulate(
                scenario="custom",
                start_lot=args.start_lot,
                big_ratio=args.big_ratio,
                small_ratio=args.small_ratio,
                close_far_share=args.close_far_share,
                reserve_share=args.reserve_share,
                close_big_on_small=args.close_big_on_small,
                remain_big_on_small=args.remain_big_on_small,
                lot_step=args.lot_step,
                point_value_per_lot=args.point_value_per_lot,
                far_distance_points=args.far_distance_points,
                big_move_points=args.big_move_points,
                max_levels=args.max_levels,
            )
        }
    else:
        rows_by_scenario = default_runs(args)
    all_rows = [row for rows in rows_by_scenario.values() for row in rows]
    write_csv(all_rows)
    write_report(rows_by_scenario)
    print(f"BIG_SCENARIO_TRACE_SIMULATION_PASS csv={CSV_PATH} report={MD_PATH}")
    for scenario, rows in rows_by_scenario.items():
        print(summarize(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
