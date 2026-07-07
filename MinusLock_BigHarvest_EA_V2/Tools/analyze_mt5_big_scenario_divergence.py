#!/usr/bin/env python3
"""Compare the previous offline Big-only model with the supplied MT5 tester facts.

The MT5 Strategy Tester report is the source of truth. This script focuses on the
first Big level because that is where the previous optimizer first diverged.
"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "Reports"
CSV_PATH = REPORTS / "BigScenario_MT5_Divergence.csv"
MD_PATH = REPORTS / "BigScenario_MT5_Divergence_Report.md"

START_LOT = 1.00
BIG_RATIO = 1.11
SMALL_RATIO = 0.25
CLOSE_FAR_SHARE = 0.75
RESERVE_SHARE = 0.25
BIG_MOVE_START_POINTS = 250
BIG_MOVE_STEP_POINTS = 40
FAR_DISTANCE_POINTS = 180
LOT_STEP = 0.01

# Facts copied from the provided MT5 Strategy Tester order/deal history.
MT5_INITIAL_FAR_SELL_OPEN = 154.889
MT5_BIG_L1_OPEN = 155.149
MT5_SMALL_L1_OPEN = 155.127
MT5_BIG_L1_CLOSE = 155.394
MT5_SMALL_L1_CLOSE = 155.396
MT5_FAR_L1_PARTIAL_CLOSE = 155.386
MT5_BIG_L1_LOT = 1.11
MT5_SMALL_L1_LOT = 0.28
MT5_FAR_PARTIAL_LOT = 0.29
MT5_CLOSED_BIG_NET = 147.73
MT5_CLOSED_SMALL_NET = -40.90
MT5_FAR_PARTIAL_REAL_LOSS = 78.27
MT5_LEVEL_REACHED = 11
MT5_ON_TESTER = -1
MT5_END_OPEN_POSITIONS = "BIG_L11/SMALL_L11/residual Far closed by end-of-test orders"


def round_down(value: float, step: float = LOT_STEP) -> float:
    import math
    if value <= 0:
        return 0.0
    return round(math.floor((value + 1e-12) / step) * step, 8)


@dataclass
class DivergenceRow:
    Metric: str
    OfflinePython: str
    MT5Tester: str
    Difference: str
    Verdict: str


def build_rows() -> list[DivergenceRow]:
    offline_big_lot = round(START_LOT * BIG_RATIO, 2)
    offline_small_lot = 0.28
    offline_big_net = offline_big_lot * BIG_MOVE_START_POINTS
    offline_small_net = -offline_small_lot * BIG_MOVE_START_POINTS
    offline_net = offline_big_net + offline_small_net
    offline_budget = offline_net * CLOSE_FAR_SHARE
    offline_reserve = offline_net * RESERVE_SHARE
    offline_close_far_lot = round_down(offline_budget / FAR_DISTANCE_POINTS)
    offline_far_after = round_down(START_LOT - offline_close_far_lot)
    offline_remaining_loss = offline_far_after * FAR_DISTANCE_POINTS
    offline_recovery_pl = offline_reserve - offline_remaining_loss
    offline_coverage = offline_reserve / offline_remaining_loss if offline_remaining_loss > 0 else 999.0

    mt5_net = MT5_CLOSED_BIG_NET + MT5_CLOSED_SMALL_NET
    mt5_budget = mt5_net * CLOSE_FAR_SHARE
    mt5_reserve = mt5_net * RESERVE_SHARE
    mt5_far_after = round(START_LOT - MT5_FAR_PARTIAL_LOT, 2)
    mt5_loss_per_closed_far_lot = MT5_FAR_PARTIAL_REAL_LOSS / MT5_FAR_PARTIAL_LOT
    mt5_effective_far_points = abs(MT5_BIG_L1_CLOSE - MT5_INITIAL_FAR_SELL_OPEN) / 0.001
    mt5_big_points = abs(MT5_BIG_L1_CLOSE - MT5_BIG_L1_OPEN) / 0.001
    mt5_implied_point_value = MT5_CLOSED_BIG_NET / (MT5_BIG_L1_LOT * mt5_big_points)
    mt5_remaining_loss_est = mt5_far_after * mt5_loss_per_closed_far_lot
    mt5_recovery_pl_est = mt5_reserve - mt5_remaining_loss_est
    mt5_coverage_est = mt5_reserve / mt5_remaining_loss_est

    return [
        DivergenceRow("BigLot L1", f"{offline_big_lot:.2f}", f"{MT5_BIG_L1_LOT:.2f}", "0.00", "MATCH"),
        DivergenceRow("SmallLot L1", f"{offline_small_lot:.2f}", f"{MT5_SMALL_L1_LOT:.2f}", "0.00", "MATCH"),
        DivergenceRow("Big move points used for L1", f"{BIG_MOVE_START_POINTS}", f"{mt5_big_points:.1f} from deal prices", f"{BIG_MOVE_START_POINTS - mt5_big_points:.1f}", "DIVERGES: bid/ask/fill prices"),
        DivergenceRow("Point value per lot", "1.0000 hard-coded", f"{mt5_implied_point_value:.4f} implied from MT5", f"{1.0 - mt5_implied_point_value:.4f}", "DIVERGES: account currency/symbol tick value"),
        DivergenceRow("BigScenarioNet L1", f"{offline_net:.2f}", f"{mt5_net:.2f}", f"{offline_net - mt5_net:.2f}", "FIRST MATERIAL DIVERGENCE"),
        DivergenceRow("CloseFarBudget L1", f"{offline_budget:.2f}", f"{mt5_budget:.2f}", f"{offline_budget - mt5_budget:.2f}", "DIVERGES"),
        DivergenceRow("ReserveAdd L1", f"{offline_reserve:.2f}", f"{mt5_reserve:.2f}", f"{offline_reserve - mt5_reserve:.2f}", "DIVERGES"),
        DivergenceRow("Far loss basis", f"{FAR_DISTANCE_POINTS} points fixed", f"~{mt5_effective_far_points:.1f} price-distance points / {mt5_loss_per_closed_far_lot:.2f} money per lot", "large", "DIVERGES: EA uses REAL_PRICE_DISTANCE"),
        DivergenceRow("CloseFarLot L1", f"{offline_close_far_lot:.2f}", f"{MT5_FAR_PARTIAL_LOT:.2f}", f"{offline_close_far_lot - MT5_FAR_PARTIAL_LOT:.2f}", "DIVERGES"),
        DivergenceRow("FarLotAfter L1", f"{offline_far_after:.2f}", f"{mt5_far_after:.2f}", f"{offline_far_after - mt5_far_after:.2f}", "DIVERGES"),
        DivergenceRow("ReserveCoverage after L1", f"{offline_coverage:.4f}", f"{mt5_coverage_est:.4f} estimate", f"{offline_coverage - mt5_coverage_est:.4f}", "DIVERGES"),
        DivergenceRow("Next action after L1", "FINAL_CLOSE", "Open MinusLock_BIG_L2", "opposite", "FIRST STATE DIVERGENCE"),
        DivergenceRow("Final path", "LevelsUsed=1 / STATE_CLOSED_PROFIT", f"Reached BIG_L{MT5_LEVEL_REACHED}; OnTester={MT5_ON_TESTER}; {MT5_END_OPEN_POSITIONS}", "invalidates optimizer claim", "MT5_SOURCE_OF_TRUTH"),
    ]


def write_csv(rows: list[DivergenceRow]) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_report(rows: list[DivergenceRow]) -> None:
    lines = [
        "# MT5 Big Scenario Divergence Investigation",
        "",
        "## Verdict",
        "",
        "The supplied MT5 Strategy Tester report invalidates the previous offline optimizer claim that `BigScenario_Best_1.set` completes in one Big level. In MT5 the same parameter set reached `MinusLock_BIG_L11`, produced `OnTester=-1`, and the test ended with open managed exposure closed by end-of-test orders.",
        "",
        "The current offline optimizer must **not** be used as a selector for production-working parameters. It is only a simplified algebraic Big-only trace until it is upgraded to replay MT5 deal prices, dynamic tick value, `FarDistanceMode=REAL_PRICE_DISTANCE`, spread/bid/ask execution, Small-scenario branch changes, and real terminal state guards.",
        "",
        "## First divergence",
        "",
        "The first material divergence occurs inside level 1 before Far partial close:",
        "",
        "1. Python calculates `BigScenarioNet=207.50`, but MT5 realized `ClosedBigNet=147.73`, `ClosedSmallNet=-40.90`, therefore `BigScenarioNet=106.83`.",
        "2. Python uses fixed `FarDistancePoints=180`, but the EA is configured with `FarDistanceMode=REAL_PRICE_DISTANCE`; level 1 MT5 prices imply about 505 price-distance points from Far open to Big close and an actual Far close cost of 78.27 for only 0.29 lot.",
        "3. Python therefore closes 0.86 Far lot and predicts final close, while MT5 closes only 0.29 Far lot and opens `MinusLock_BIG_L2`.",
        "",
        "## Python vs MT5 comparison",
        "",
        "| Metric | Offline Python | MT5 Tester | Difference | Verdict |",
        "|---|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(f"| {row.Metric} | {row.OfflinePython} | {row.MT5Tester} | {row.Difference} | {row.Verdict} |")
    lines += [
        "",
        "## Missing conditions in the previous Python model",
        "",
        "1. Dynamic `PointValuePerLot()` for USDJPY with EUR deposit currency; previous model hard-coded `1.0`.",
        "2. `FarDistanceMode=REAL_PRICE_DISTANCE`; previous model used fixed `FarDistancePoints=180` as the loss basis.",
        "3. Real bid/ask entry and exit prices; previous model used exact target points.",
        "4. Spread, slippage and fill-price drift between trigger and execution.",
        "5. Real `HistoryDeals` net calculation, including swap/commission when present.",
        "6. Mixed path behavior: MT5 did not remain Big-only; after level 2 the report shows Small-scenario/reverse-style transitions and direction flips.",
        "7. Actual StateMachine guards: final close requires real recovery pass and terminal no-open-position checks; algebraic reserve coverage is insufficient.",
        "8. End-of-test forced closures are not represented by the offline model.",
        "",
        "## Can the current optimizer be used?",
        "",
        "No. The previous optimizer can remain as a unit-level algebra trace for formulas, but it is not valid for choosing working MT5 parameters. It requires a redesign around MT5 deal replay or Strategy Tester CSV ingestion before it can rank production candidates.",
        "",
        "## Required next engineering correction",
        "",
        "- Treat `Reports/BigScenario_Parameter_Recommendations.md` and `Sets/BigScenario_Best_*.set` as invalidated offline candidates.",
        "- Add a future optimizer mode that consumes MT5 orders/deals or EA `CycleMath` CSV and compares realized fields level-by-level.",
        "- Rank only candidates that pass real MT5 Strategy Tester with `OnTester > 0`, no end-of-test managed positions, and no `STATE_STOP_MAX_LEVELS` / unresolved recovery state.",
        "",
    ]
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    rows = build_rows()
    write_csv(rows)
    write_report(rows)
    print(f"MT5_BIG_SCENARIO_DIVERGENCE_ANALYSIS_PASS csv={CSV_PATH} report={MD_PATH}")
    print("first_material_divergence=BigScenarioNet/CloseFarBudget/FarDistance basis at L1")
    print("optimizer_status=INVALID_FOR_MT5_PARAMETER_SELECTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
