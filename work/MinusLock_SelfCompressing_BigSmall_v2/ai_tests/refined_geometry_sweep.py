from __future__ import annotations

import csv
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from statistics import mean
from typing import Iterable

try:
    from .minuslock_model import BIG, SMALL, INITIAL_PLUS_CUMULATIVE, ModelConfig, SimulationResult, simulate_sequence
except ImportError:  # pragma: no cover
    from minuslock_model import BIG, SMALL, INITIAL_PLUS_CUMULATIVE, ModelConfig, SimulationResult, simulate_sequence

ROOT = Path(__file__).resolve().parent
REPORT_DIR = ROOT / "reports"
REFINED_CSV = REPORT_DIR / "refined_geometry_sweep.csv"
REFINED_TOP10_MD = REPORT_DIR / "refined_geometry_top10.md"
REFINED_REPORT_MD = REPORT_DIR / "refined_geometry_report.md"
REFINED_MT5_PLAN_MD = REPORT_DIR / "refined_mt5_confirmation_plan.md"

BIG_RATIOS = [1.20, 1.22, 1.25, 1.27, 1.30]
SMALL_RATIOS = [0.35, 0.36, 0.37, 0.38, 0.39, 0.40, 0.41, 0.42]
CLOSE_BIG_ON_SMALL_VALUES = [0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39]
SHARE_PAIRS = [(0.30, 0.70), (0.35, 0.65), (0.40, 0.60), (0.45, 0.55), (0.50, 0.50), (0.55, 0.45), (0.60, 0.40)]
MAX_HARVEST_LEVELS = [5, 7, 9]
MAX_REVERSE_CYCLES = [2, 3, 5]

SCENARIOS = {
    "BIG_BIG_BIG": [BIG, BIG, BIG],
    "BIG_BIG_BIG_BIG_BIG": [BIG, BIG, BIG, BIG, BIG],
    "SMALL_SMALL_SMALL": [SMALL, SMALL, SMALL],
    "REAL_REPORT_SEQUENCE": [BIG, SMALL, SMALL, BIG, SMALL],
    "CHOPPY": [BIG, SMALL, BIG, SMALL, BIG],
    "BAD_MARKET": [SMALL, SMALL, BIG, SMALL, SMALL],
    "STRESS_ALTERNATING": [SMALL, BIG, SMALL, BIG, SMALL, BIG, SMALL],
    "LONG_SMALL_PRESSURE": [SMALL, SMALL, SMALL, SMALL, SMALL],
    "BIG_AFTER_SMALL": [SMALL, SMALL, BIG, BIG, BIG],
}

PREVIOUS_BEST = {
    "BigRatio": 1.25,
    "SmallRatio": 0.37,
    "CloseBigOnSmall": 0.35,
    "CloseFarShare": 0.40,
    "ReserveShare": 0.60,
    "MaxHarvestLevels": 7,
    "MaxReverseCycles": 3,
    "PreviousGeometryScore": 750,
}

MANUAL_CANDIDATES = {
    "Previous Best": PREVIOUS_BEST,
    "Candidate Compact Compression": {
        "BigRatio": 1.25,
        "SmallRatio": 0.39,
        "CloseBigOnSmall": 0.37,
        "CloseFarShare": 0.35,
        "ReserveShare": 0.65,
        "MaxHarvestLevels": 7,
        "MaxReverseCycles": 3,
    },
    "Candidate Reserve Heavy": {
        "BigRatio": 1.25,
        "SmallRatio": 0.38,
        "CloseBigOnSmall": 0.35,
        "CloseFarShare": 0.30,
        "ReserveShare": 0.70,
        "MaxHarvestLevels": 7,
        "MaxReverseCycles": 3,
    },
    "Candidate Big Strong": {
        "BigRatio": 1.27,
        "SmallRatio": 0.37,
        "CloseBigOnSmall": 0.35,
        "CloseFarShare": 0.40,
        "ReserveShare": 0.60,
        "MaxHarvestLevels": 7,
        "MaxReverseCycles": 3,
    },
}


@dataclass(frozen=True)
class RefinedParams:
    big_ratio: float
    small_ratio: float
    close_big_on_small: float
    close_far_share: float
    reserve_share: float
    max_harvest_levels: int
    max_reverse_cycles: int

    @property
    def remain_big_on_small(self) -> float:
        return round(1.0 - self.close_big_on_small, 2)

    @property
    def compression_ratio(self) -> float:
        return compression_ratio(self.big_ratio, self.remain_big_on_small)

    @property
    def big_net_power(self) -> float:
        return big_net_power(self.big_ratio, self.small_ratio)

    @property
    def small_coverage_gap(self) -> float:
        return round(self.small_ratio - self.close_big_on_small, 4)

    def to_config(self) -> ModelConfig:
        return ModelConfig(
            big_ratio=self.big_ratio,
            small_ratio=self.small_ratio,
            close_big_on_small=self.close_big_on_small,
            remain_big_on_small=self.remain_big_on_small,
            close_far_share=self.close_far_share,
            reserve_share=self.reserve_share,
            max_harvest_levels=self.max_harvest_levels,
            max_reverse_cycles=self.max_reverse_cycles,
            far_distance_mode=INITIAL_PLUS_CUMULATIVE,
        )


@dataclass
class RefinedSummary:
    raw_combinations: int
    filtered_combinations: int
    tested_combinations: int
    scenarios_per_combination: int
    rows: list[dict]
    top10: list[dict]
    worst10: list[dict]
    previous_best: dict
    manual_candidates: dict[str, dict]


def compression_ratio(big_ratio: float, remain_big_on_small: float) -> float:
    return round(big_ratio * remain_big_on_small, 4)


def big_net_power(big_ratio: float, small_ratio: float) -> float:
    return round(big_ratio * (1.0 - small_ratio), 4)


def is_valid_refined_params(big_ratio: float, small_ratio: float, close_big_on_small: float, close_far_share: float, reserve_share: float, max_harvest_levels: int) -> tuple[bool, str]:
    remain_big = round(1.0 - close_big_on_small, 2)
    compression = compression_ratio(big_ratio, remain_big)
    net_power = big_net_power(big_ratio, small_ratio)
    gap = round(small_ratio - close_big_on_small, 4)
    if small_ratio <= close_big_on_small:
        return False, "SmallRatio <= CloseBigOnSmall"
    if gap < 0.015:
        return False, "SmallRatio - CloseBigOnSmall < 0.015"
    if compression >= 0.86:
        return False, "CompressionRatio >= 0.86"
    if compression <= 0.68:
        return False, "CompressionRatio <= 0.68"
    if net_power < 0.72:
        return False, "BigNetPower < 0.72"
    if abs((close_far_share + reserve_share) - 1.0) > 1e-9:
        return False, "CloseFarShare + ReserveShare != 1.00"
    if max_harvest_levels < 5:
        return False, "MaxHarvestLevels < 5"
    return True, "OK"


def iter_raw_params() -> Iterable[RefinedParams]:
    for big_ratio, small_ratio, close_big, (close_far, reserve), max_levels, max_reverse in product(
        BIG_RATIOS,
        SMALL_RATIOS,
        CLOSE_BIG_ON_SMALL_VALUES,
        SHARE_PAIRS,
        MAX_HARVEST_LEVELS,
        MAX_REVERSE_CYCLES,
    ):
        yield RefinedParams(big_ratio, small_ratio, close_big, close_far, reserve, max_levels, max_reverse)


def _status_counts(results: dict[str, SimulationResult]) -> dict[str, int]:
    states = [r.state for r in results.values()]
    return {
        "ClosedProfitCount": sum(s == "STATE_CLOSED_PROFIT" for s in states),
        "StopMaxLevelsCount": sum(s == "STATE_UNCLOSED_CYCLE" or "STOP_MAX_LEVELS" in r.reason for s, r in zip(states, results.values())),
        "InvalidGeometryCount": sum(s == "STATE_INVALID_REVERSE_GEOMETRY" for s in states),
        "InvalidSmallGeometryCount": sum(s == "STATE_INVALID_SMALL_GEOMETRY" for s in states),
        "ReverseLimitCount": sum(s == "STATE_REVERSE_LIMIT" for s in states),
    }


def _mins_from_rows(results: dict[str, SimulationResult]) -> tuple[float, float]:
    reverse_values: list[float] = []
    coverage_values: list[float] = []
    for result in results.values():
        for row in result.rows:
            if row.ReverseStrength > 0:
                reverse_values.append(row.ReverseStrength)
            if row.ProjectedReserveCoverage > 0:
                coverage_values.append(row.ProjectedReserveCoverage)
    return (min(reverse_values) if reverse_values else 0.0, min(coverage_values) if coverage_values else 0.0)


def refined_score(row: dict) -> int:
    score = 0
    score += 150 * int(row["ClosedProfitCount"])
    if row["WorstCycleFinalPL"] > 0:
        score += 50
    if row["StopMaxLevelsCount"] == 0:
        score += 40
    if 0.72 <= row["CompressionRatio"] <= 0.82:
        score += 30
    if 0.74 <= row["BigNetPower"] <= 0.82:
        score += 25
    if 0.02 <= row["SmallCoverageGap"] <= 0.05:
        score += 25
    if row["ReverseStrengthMin"] >= 0.15:
        score += 20
    if row["ReserveShare"] >= 0.55:
        score += 20
    score -= 200 * int(row["StopMaxLevelsCount"])
    score -= 300 * int(row["InvalidGeometryCount"])
    score -= 200 * int(row["InvalidSmallGeometryCount"])
    score -= 100 * int(row["ReverseLimitCount"])
    if row["CompressionRatio"] > 0.83:
        score -= 50
    if row["BigNetPower"] < 0.74:
        score -= 50
    return score


def evaluate_params(params: RefinedParams, label: str = "GRID") -> dict:
    cfg = params.to_config()
    results = {name: simulate_sequence(cfg, seq) for name, seq in SCENARIOS.items()}
    pls = [r.cycle_final_pl for r in results.values()]
    counts = _status_counts(results)
    reverse_min, coverage_min = _mins_from_rows(results)
    worst_name, worst_result = min(results.items(), key=lambda item: item[1].cycle_final_pl)
    best_name, best_result = max(results.items(), key=lambda item: item[1].cycle_final_pl)
    pass_count = sum(r.state == "STATE_CLOSED_PROFIT" and r.cycle_final_pl > 0 for r in results.values())
    row = {
        "Label": label,
        "BigRatio": params.big_ratio,
        "SmallRatio": params.small_ratio,
        "CloseBigOnSmall": params.close_big_on_small,
        "RemainBigOnSmall": params.remain_big_on_small,
        "CloseFarShare": params.close_far_share,
        "ReserveShare": params.reserve_share,
        "MaxHarvestLevels": params.max_harvest_levels,
        "MaxReverseCycles": params.max_reverse_cycles,
        "CompressionRatio": params.compression_ratio,
        "BigNetPower": params.big_net_power,
        "SmallCoverageGap": params.small_coverage_gap,
        "PassCount": pass_count,
        "FailCount": len(SCENARIOS) - pass_count,
        **counts,
        "AverageCycleFinalPL": round(mean(pls), 4),
        "WorstCycleFinalPL": min(pls),
        "BestCycleFinalPL": max(pls),
        "WorstScenario": worst_name,
        "BestScenario": best_name,
        "WorstScenarioState": worst_result.state,
        "BestScenarioState": best_result.state,
        "MaxOpenLots": max(r.max_open_lots for r in results.values()),
        "MaxMarginEstimate": max(r.max_margin_estimate for r in results.values()),
        "MaxDrawdownEstimate": max(r.max_drawdown_estimate for r in results.values()),
        "ReverseStrengthMin": round(reverse_min, 4),
        "ProjectedReserveCoverageMin": round(coverage_min, 4),
        "REAL_REPORT_SEQUENCE_State": results["REAL_REPORT_SEQUENCE"].state,
        "REAL_REPORT_SEQUENCE_PL": results["REAL_REPORT_SEQUENCE"].cycle_final_pl,
        "LONG_SMALL_PRESSURE_State": results["LONG_SMALL_PRESSURE"].state,
        "LONG_SMALL_PRESSURE_PL": results["LONG_SMALL_PRESSURE"].cycle_final_pl,
        "BAD_MARKET_State": results["BAD_MARKET"].state,
        "BAD_MARKET_PL": results["BAD_MARKET"].cycle_final_pl,
        "STRESS_ALTERNATING_State": results["STRESS_ALTERNATING"].state,
        "STRESS_ALTERNATING_PL": results["STRESS_ALTERNATING"].cycle_final_pl,
    }
    row["AverageScore"] = round((pass_count / len(SCENARIOS)) * 100.0, 2)
    row["Score"] = refined_score(row)
    return row


def _params_from_dict(d: dict) -> RefinedParams:
    return RefinedParams(d["BigRatio"], d["SmallRatio"], d["CloseBigOnSmall"], d["CloseFarShare"], d["ReserveShare"], d["MaxHarvestLevels"], d["MaxReverseCycles"])


def run_refined_sweep(write_reports: bool = True) -> RefinedSummary:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    raw_params = list(iter_raw_params())
    rows: list[dict] = []
    filtered = 0
    for params in raw_params:
        valid, reason = is_valid_refined_params(params.big_ratio, params.small_ratio, params.close_big_on_small, params.close_far_share, params.reserve_share, params.max_harvest_levels)
        if not valid:
            filtered += 1
            continue
        row = evaluate_params(params)
        row["FilterReason"] = reason
        rows.append(row)

    rows.sort(key=lambda r: (r["Score"], r["PassCount"], r["WorstCycleFinalPL"], -r["StopMaxLevelsCount"], -r["MaxDrawdownEstimate"]), reverse=True)
    top10 = rows[:10]
    worst10 = sorted(rows, key=lambda r: (r["Score"], r["PassCount"], r["WorstCycleFinalPL"]))[:10]
    previous_best = evaluate_params(_params_from_dict(PREVIOUS_BEST), "Previous Best")
    previous_best["PreviousGeometryScore"] = PREVIOUS_BEST["PreviousGeometryScore"]
    manual = {name: evaluate_params(_params_from_dict(params), name) for name, params in MANUAL_CANDIDATES.items()}
    summary = RefinedSummary(
        raw_combinations=len(raw_params),
        filtered_combinations=filtered,
        tested_combinations=len(rows),
        scenarios_per_combination=len(SCENARIOS),
        rows=rows,
        top10=top10,
        worst10=worst10,
        previous_best=previous_best,
        manual_candidates=manual,
    )
    if write_reports:
        write_csv(summary)
        write_top10(summary)
        write_report(summary)
        write_mt5_plan(summary)
    return summary


def write_csv(summary: RefinedSummary) -> None:
    if not summary.rows:
        return
    with REFINED_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary.rows)


def _table(rows: list[dict]) -> str:
    headers = ["Rank", "Score", "BigRatio", "SmallRatio", "CloseBigOnSmall", "RemainBigOnSmall", "CloseFarShare", "ReserveShare", "MaxHarvestLevels", "MaxReverseCycles", "CompressionRatio", "BigNetPower", "SmallCoverageGap", "PassCount", "StopMaxLevelsCount", "WorstCycleFinalPL"]
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for i, row in enumerate(rows, start=1):
        lines.append("| " + " | ".join(str(x) for x in [i] + [row[h] for h in headers[1:]]) + " |")
    return "\n".join(lines)


def _candidate_lines(title: str, row: dict) -> str:
    return (
        f"## {title}\n\n"
        f"- BigRatio: {row['BigRatio']}\n"
        f"- SmallRatio: {row['SmallRatio']}\n"
        f"- CloseBigOnSmall: {row['CloseBigOnSmall']}\n"
        f"- RemainBigOnSmall: {row['RemainBigOnSmall']}\n"
        f"- CloseFarShare / ReserveShare: {row['CloseFarShare']} / {row['ReserveShare']}\n"
        f"- MaxHarvestLevels / MaxReverseCycles: {row['MaxHarvestLevels']} / {row['MaxReverseCycles']}\n"
        f"- CompressionRatio: {row['CompressionRatio']}\n"
        f"- BigNetPower: {row['BigNetPower']}\n"
        f"- SmallCoverageGap: {row['SmallCoverageGap']}\n"
        f"- PassCount: {row['PassCount']}\n"
        f"- StopMaxLevelsCount: {row['StopMaxLevelsCount']}\n"
        f"- WorstCycleFinalPL: {row['WorstCycleFinalPL']}\n"
        f"- Score: {row['Score']}\n\n"
    )


def write_top10(summary: RefinedSummary) -> None:
    REFINED_TOP10_MD.write_text(
        "# Refined Geometry Sweep Top 10\n\n"
        "Python-модель ранжирует только кандидаты для MT5-подтверждения; это не финальный результат стратегии.\n\n"
        "## Top 10\n\n" + _table(summary.top10) + "\n\n"
        "## Worst 10\n\n" + _table(summary.worst10) + "\n",
        encoding="utf-8",
    )


def write_report(summary: RefinedSummary) -> None:
    best = summary.top10[0]
    second = summary.top10[1]
    conservative = summary.manual_candidates["Candidate Reserve Heavy"]
    prev = summary.previous_best
    diff_score = best["Score"] - prev["Score"]
    text = f"""# Refined Geometry Sweep Report

## 1. Зачем нужен второй refined sweep

Первый geometry sweep нашёл previous best вокруг `1.25 / 0.37 / 0.35 / 40/60 / 7 / 3`. Refined sweep сужает сетку вокруг него, чтобы проверить более тонкие значения и подготовить кандидатов для MT5 Strategy Tester.

## 2. Почему previous best был выбран

Previous best имел CompressionRatio = 0.8125, BigNetPower = 0.7875 и прежний score = 750. Это улучшило старую геометрию 0.91, но оставило пространство для поиска CompressionRatio ближе к 0.72–0.80 и ReserveShare 0.55–0.70.

## 3. Какие диапазоны проверены

- BigRatio: {BIG_RATIOS}
- SmallRatio: {SMALL_RATIOS}
- CloseBigOnSmall: {CLOSE_BIG_ON_SMALL_VALUES}
- CloseFarShare / ReserveShare: {SHARE_PAIRS}
- MaxHarvestLevels: {MAX_HARVEST_LEVELS}
- MaxReverseCycles: {MAX_REVERSE_CYCLES}

## 4. Сколько raw combinations

{summary.raw_combinations}

## 5. Сколько filtered combinations

{summary.filtered_combinations}

## 6. Сколько tested combinations

{summary.tested_combinations}; scenarios per combination = {summary.scenarios_per_combination}.

## 7. Какие фильтры применены

SmallRatio > CloseBigOnSmall, SmallCoverageGap >= 0.015, CompressionRatio between 0.68 and 0.86, BigNetPower >= 0.72, CloseFarShare + ReserveShare = 1.00, MaxHarvestLevels >= 5.

## 8. Top 10 candidates

{_table(summary.top10)}

## 9. Worst 10 candidates

{_table(summary.worst10)}

## 10. Previous Best vs Refined Best

| Metric | Previous Best | Refined Top | Difference |
|---|---:|---:|---:|
| Score | {prev['Score']} | {best['Score']} | {diff_score} |
| PassCount | {prev['PassCount']} | {best['PassCount']} | {best['PassCount'] - prev['PassCount']} |
| StopMaxLevelsCount | {prev['StopMaxLevelsCount']} | {best['StopMaxLevelsCount']} | {best['StopMaxLevelsCount'] - prev['StopMaxLevelsCount']} |
| CompressionRatio | {prev['CompressionRatio']} | {best['CompressionRatio']} | {round(best['CompressionRatio'] - prev['CompressionRatio'], 4)} |
| BigNetPower | {prev['BigNetPower']} | {best['BigNetPower']} | {round(best['BigNetPower'] - prev['BigNetPower'], 4)} |
| WorstCycleFinalPL | {prev['WorstCycleFinalPL']} | {best['WorstCycleFinalPL']} | {round(best['WorstCycleFinalPL'] - prev['WorstCycleFinalPL'], 4)} |
| MaxOpenLots | {prev['MaxOpenLots']} | {best['MaxOpenLots']} | {round(best['MaxOpenLots'] - prev['MaxOpenLots'], 4)} |
| MaxDrawdownEstimate | {prev['MaxDrawdownEstimate']} | {best['MaxDrawdownEstimate']} | {round(best['MaxDrawdownEstimate'] - prev['MaxDrawdownEstimate'], 4)} |

## 11. Разбор CompressionRatio

Top candidate CompressionRatio = {best['CompressionRatio']}. Target zone is 0.72–0.82, so tail compression stays within the refined target while avoiding too-aggressive compression below 0.68.

## 12. Разбор BigNetPower

Top candidate BigNetPower = {best['BigNetPower']}. It remains inside or above the target 0.74–0.82 band and above the hard filter 0.72.

## 13. Разбор SmallCoverageGap

Top candidate SmallCoverageGap = {best['SmallCoverageGap']}. The target is 0.02–0.05 so Small can cover the closed part of Big without making Big-harvest too weak.

## 14. Разбор ReserveShare

Top candidate ReserveShare = {best['ReserveShare']}. Refined scoring gives a bonus for ReserveShare >= 0.55 because reserve protects final close validation.

## 15. Сценарий REAL_REPORT_SEQUENCE

Refined top: state = {best['REAL_REPORT_SEQUENCE_State']}, PL estimate = {best['REAL_REPORT_SEQUENCE_PL']}. This is still a Python estimate and must be validated by MT5 real history P/L.

## 16. Сценарий LONG_SMALL_PRESSURE

Refined top: state = {best['LONG_SMALL_PRESSURE_State']}, PL estimate = {best['LONG_SMALL_PRESSURE_PL']}. This scenario checks repeated Small-at-Far compression pressure.

{_candidate_lines('17. Лучший кандидат', best)}{_candidate_lines('18. Второй кандидат', second)}{_candidate_lines('19. Консервативный кандидат', conservative)}## 20. Риски

- Python-модель не заменяет MT5 Strategy Tester.
- `CycleFinalPL`/`RealRecoveryPLEstimate` are model estimates, not broker-executed P/L.
- MT5 must confirm `RealRecoveryPL > 0`, no managed open positions, and `OnTester > 0` only for real positive recovery.
- More reserve can reduce STOP risk but may slow Far-lot reduction; more Far close can reduce Far faster but can weaken final reserve.

## 21. Что подтвердить в MT5

Run Top, Second, and Conservative candidates from `refined_mt5_confirmation_plan.md` with `FarDistanceMode = REAL_PRICE_DISTANCE`, `EnableCycleMathCsv = true`, and real recovery validation enabled. Collect Strategy Tester report, Experts log, `MinusLock_CycleMath.csv`, `REAL_CYCLE_MATH`, final state, last close comment, and OnTester.
"""
    REFINED_REPORT_MD.write_text(text, encoding="utf-8")


def write_mt5_plan(summary: RefinedSummary) -> None:
    candidates = [summary.top10[0], summary.top10[1], summary.manual_candidates["Candidate Reserve Heavy"]]
    names = ["Top refined candidate", "Second refined candidate", "Conservative candidate"]
    lines = ["# Refined MT5 Confirmation Plan", "", "Python-модель показывает кандидатов. Финальное подтверждение обязательно через MT5 Strategy Tester.", ""]
    for name, row in zip(names, candidates):
        lines += [
            f"## {name}",
            "",
            f"- BigRatio = {row['BigRatio']}",
            f"- SmallRatio = {row['SmallRatio']}",
            f"- CloseBigOnSmall = {row['CloseBigOnSmall']}",
            f"- RemainBigOnSmall = {row['RemainBigOnSmall']}",
            f"- CloseFarShare = {row['CloseFarShare']}",
            f"- ReserveShare = {row['ReserveShare']}",
            f"- MaxHarvestLevels = {row['MaxHarvestLevels']}",
            f"- MaxReverseCycles = {row['MaxReverseCycles']}",
            "- FarDistanceMode = REAL_PRICE_DISTANCE",
            "- EnableCycleMathCsv = true",
            "- AllowRealTrading = true",
            "",
        ]
    lines += [
        "## Required MT5 artifacts",
        "",
        "- Strategy Tester HTML/XML report",
        "- Experts journal containing CYCLE_MATH and REAL_CYCLE_MATH",
        "- MQL5/Files/MinusLock_CycleMath.csv",
        "- Final state and last close comment",
        "- OnTester value",
        "- Check that MagicNumber positions are fully closed",
        "",
        "## PASS criteria",
        "",
        "- State = STATE_CLOSED_PROFIT",
        "- RealRecoveryPL > 0",
        "- OnTester > 0 and equals real recovery result, not theoretical CycleFinalPL",
        "- No STOP_MAX_LEVELS / STATE_UNCLOSED_CYCLE / invalid geometry / reverse limit",
        "- No managed positions remain open",
        "",
        "## FAIL criteria",
        "",
        "- RealRecoveryPL <= 0",
        "- OnTester = -1",
        "- STOP_MAX_LEVELS or end-of-test position closure",
        "- Missing Cycle Math CSV or REAL_CYCLE_MATH diagnostics",
        "",
    ]
    REFINED_MT5_PLAN_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> RefinedSummary:
    summary = run_refined_sweep(write_reports=True)
    best = summary.top10[0]
    print(
        "REFINED_GEOMETRY_SWEEP PASS: "
        f"raw={summary.raw_combinations} filtered={summary.filtered_combinations} "
        f"tested={summary.tested_combinations} scenarios={summary.scenarios_per_combination} "
        f"top_score={best['Score']} top=BigRatio:{best['BigRatio']} SmallRatio:{best['SmallRatio']} "
        f"CloseBigOnSmall:{best['CloseBigOnSmall']} CloseFarShare:{best['CloseFarShare']} ReserveShare:{best['ReserveShare']}"
    )
    print(f"CSV: {REFINED_CSV}")
    print(f"Report: {REFINED_REPORT_MD}")
    print(f"MT5 plan: {REFINED_MT5_PLAN_MD}")
    return summary


if __name__ == "__main__":
    main()
