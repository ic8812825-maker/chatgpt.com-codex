from __future__ import annotations

import csv
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Iterable

try:
    from .minuslock_model import BIG, SMALL, INITIAL_PLUS_CUMULATIVE, ModelConfig, SimulationResult, simulate_sequence
except ImportError:  # pragma: no cover - direct script execution
    from minuslock_model import BIG, SMALL, INITIAL_PLUS_CUMULATIVE, ModelConfig, SimulationResult, simulate_sequence

ROOT = Path(__file__).resolve().parent
REPORT_DIR = ROOT / "reports"
SWEEP_CSV = REPORT_DIR / "parameter_geometry_sweep.csv"
TOP10_MD = REPORT_DIR / "parameter_geometry_top10.md"
REPORT_MD = REPORT_DIR / "parameter_geometry_report.md"
MT5_PLAN_MD = REPORT_DIR / "mt5_parameter_confirmation_plan.md"

BIG_RATIOS = [1.20, 1.25, 1.30, 1.35, 1.40]
SMALL_RATIOS = [0.35, 0.37, 0.40, 0.42, 0.45, 0.47, 0.50]
CLOSE_BIG_ON_SMALL_VALUES = [0.30, 0.35, 0.37, 0.40, 0.42, 0.45, 0.50]
SHARE_PAIRS = [(0.90, 0.10), (0.80, 0.20), (0.70, 0.30), (0.60, 0.40), (0.50, 0.50), (0.40, 0.60)]
MAX_HARVEST_LEVELS = [3, 5, 7, 10]
MAX_REVERSE_CYCLES = [3, 5, 10]

SCENARIOS = {
    "STRONG_BIG": [BIG, BIG, BIG],
    "REPEAT_BIG": [BIG, BIG, BIG, BIG, BIG],
    "SMALL_COMPRESSION": [SMALL, SMALL, SMALL],
    "REAL_FAIL_SEQUENCE": [BIG, SMALL, SMALL, BIG, SMALL],
    "CHOPPY": [BIG, SMALL, BIG, SMALL, BIG],
    "BAD_MARKET": [SMALL, SMALL, BIG, SMALL, SMALL],
    "STRESS": [SMALL, BIG, SMALL, BIG, SMALL, BIG, SMALL],
}


@dataclass(frozen=True)
class GeometryParams:
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
class SweepSummary:
    raw_combinations: int
    filtered_combinations: int
    tested_combinations: int
    scenarios_per_combination: int
    rows: list[dict]
    top10: list[dict]
    worst10: list[dict]
    current_candidate: dict
    balanced_candidate: dict
    strong_candidate: dict


def compression_ratio(big_ratio: float, remain_big_on_small: float) -> float:
    return round(big_ratio * remain_big_on_small, 4)


def big_net_power(big_ratio: float, small_ratio: float) -> float:
    return round(big_ratio * (1.0 - small_ratio), 4)


def is_valid_geometry_params(big_ratio: float, small_ratio: float, close_big_on_small: float) -> tuple[bool, str]:
    remain_big = round(1.0 - close_big_on_small, 2)
    compression = compression_ratio(big_ratio, remain_big)
    net_power = big_net_power(big_ratio, small_ratio)
    if big_ratio <= 1.00:
        return False, "BigRatio <= 1.00"
    if small_ratio <= 0:
        return False, "SmallRatio <= 0"
    if close_big_on_small <= 0:
        return False, "CloseBigOnSmall <= 0"
    if close_big_on_small >= 0.65:
        return False, "CloseBigOnSmall >= 0.65"
    if small_ratio >= 0.60:
        return False, "SmallRatio >= 0.60"
    if close_big_on_small >= small_ratio:
        return False, "CloseBigOnSmall >= SmallRatio"
    if compression >= 0.90:
        return False, "CompressionRatio >= 0.90"
    if compression <= 0.60:
        return False, "CompressionRatio <= 0.60"
    if net_power < 0.65:
        return False, "BigNetPower < 0.65"
    return True, "OK"


def iter_raw_params() -> Iterable[GeometryParams]:
    for big_ratio, small_ratio, close_big, (close_far, reserve), max_levels, max_reverse in product(
        BIG_RATIOS,
        SMALL_RATIOS,
        CLOSE_BIG_ON_SMALL_VALUES,
        SHARE_PAIRS,
        MAX_HARVEST_LEVELS,
        MAX_REVERSE_CYCLES,
    ):
        yield GeometryParams(big_ratio, small_ratio, close_big, close_far, reserve, max_levels, max_reverse)


def _scenario_metrics(result: SimulationResult) -> dict:
    reverse_values = [r.ReverseStrength for r in result.rows if r.ReverseStrength > 0]
    return {
        "state": result.state,
        "pass_by_real_pl": result.state == "STATE_CLOSED_PROFIT" and result.cycle_final_pl > 0,
        "cycle_final_pl": result.cycle_final_pl,
        "real_recovery_pl_estimate": result.cycle_final_pl,
        "total_reserve": result.total_reserve,
        "far_remain_loss": result.rows[-1].FarRemainLoss if result.rows else 0.0,
        "final_close_allowed_level": result.worst_level if result.closed_profit else 0,
        "stop_max_levels": result.state == "STATE_UNCLOSED_CYCLE" or "STOP_MAX_LEVELS" in result.reason,
        "max_far_lot": result.max_far_lot,
        "final_far_lot": result.final_far_lot,
        "max_open_lots": result.max_open_lots,
        "max_margin_estimate": result.max_margin_estimate,
        "max_drawdown_estimate": result.max_drawdown_estimate,
        "number_of_big_harvest": result.number_of_big_harvest,
        "number_of_small_at_far": result.number_of_small_at_far,
        "reverse_strength_min": min(reverse_values) if reverse_values else 999.0,
        "worst_level": result.worst_level,
        "stop_reason": result.reason,
    }


def score_row(row: dict) -> int:
    score = 0
    score += 100 * int(row["PassCount"])
    score += 50 * int(row["PositivePLEstimateCount"])
    if 0.70 <= row["CompressionRatio"] <= 0.82:
        score += 30
    if row["BigNetPower"] >= 0.70:
        score += 20
    if row["ReverseStrengthMin"] >= 0.15:
        score += 20
    score -= 100 * int(row["StopMaxLevelsCount"])
    score -= 200 * int(row["InvalidGeometryCount"])
    if row["MaxDrawdownEstimate"] > 300:
        score -= 50
    if row["MaxOpenLots"] > 10:
        score -= 50
    if row["StrongBigState"] == "STATE_CLOSED_PROFIT":
        score += 100
    if row["RealFailSequencePL"] > row["BaselineCurrentRealFailPL"]:
        score += 30
    return score


def evaluate_params(params: GeometryParams, baseline_real_fail_pl: float = 0.0, label: str = "GRID") -> dict:
    cfg = params.to_config()
    scenario_metrics = {name: _scenario_metrics(simulate_sequence(cfg, seq)) for name, seq in SCENARIOS.items()}
    pass_count = sum(1 for m in scenario_metrics.values() if m["pass_by_real_pl"])
    positive_pl_count = sum(1 for m in scenario_metrics.values() if m["real_recovery_pl_estimate"] > 0)
    stop_count = sum(1 for m in scenario_metrics.values() if m["stop_max_levels"])
    invalid_count = sum(1 for m in scenario_metrics.values() if str(m["state"]).startswith("STATE_INVALID") or m["state"] == "STATE_REVERSE_LIMIT")
    reverse_min_values = [m["reverse_strength_min"] for m in scenario_metrics.values() if m["reverse_strength_min"] != 999.0]
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
        "SmallCloseGap": round(params.small_ratio - params.close_big_on_small, 4),
        "ScenarioCount": len(SCENARIOS),
        "PassCount": pass_count,
        "PositivePLEstimateCount": positive_pl_count,
        "StopMaxLevelsCount": stop_count,
        "InvalidGeometryCount": invalid_count,
        "StrongBigState": scenario_metrics["STRONG_BIG"]["state"],
        "RepeatBigState": scenario_metrics["REPEAT_BIG"]["state"],
        "SmallCompressionState": scenario_metrics["SMALL_COMPRESSION"]["state"],
        "RealFailSequenceState": scenario_metrics["REAL_FAIL_SEQUENCE"]["state"],
        "RealFailSequencePL": scenario_metrics["REAL_FAIL_SEQUENCE"]["real_recovery_pl_estimate"],
        "BaselineCurrentRealFailPL": baseline_real_fail_pl,
        "TotalReserveMax": max(m["total_reserve"] for m in scenario_metrics.values()),
        "FarRemainLossMax": max(m["far_remain_loss"] for m in scenario_metrics.values()),
        "FinalCloseAllowedLevelMax": max(m["final_close_allowed_level"] for m in scenario_metrics.values()),
        "MaxFarLot": max(m["max_far_lot"] for m in scenario_metrics.values()),
        "FinalFarLotMax": max(m["final_far_lot"] for m in scenario_metrics.values()),
        "MaxOpenLots": max(m["max_open_lots"] for m in scenario_metrics.values()),
        "MaxMarginEstimate": max(m["max_margin_estimate"] for m in scenario_metrics.values()),
        "MaxDrawdownEstimate": max(m["max_drawdown_estimate"] for m in scenario_metrics.values()),
        "NumberOfBigHarvest": sum(m["number_of_big_harvest"] for m in scenario_metrics.values()),
        "NumberOfSmallAtFar": sum(m["number_of_small_at_far"] for m in scenario_metrics.values()),
        "CompressionRatioMin": params.compression_ratio,
        "CompressionRatioMax": params.compression_ratio,
        "ReverseStrengthMin": min(reverse_min_values) if reverse_min_values else 0.0,
        "WorstLevel": max(m["worst_level"] for m in scenario_metrics.values()),
        "StopReason": "; ".join(sorted({m["stop_reason"] for m in scenario_metrics.values() if m["stop_reason"]})),
    }
    row["Score"] = score_row(row)
    return row


def _candidate(big: float, small: float, close_big: float, close_far: float, reserve: float, label: str) -> GeometryParams:
    return GeometryParams(big, small, close_big, close_far, reserve, 5, 10)


def run_geometry_sweep(write_reports: bool = True) -> SweepSummary:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    raw_params = list(iter_raw_params())
    current_params = _candidate(1.30, 0.37, 0.30, 0.70, 0.30, "CURRENT_70_30")
    current_candidate = evaluate_params(current_params, 0.0, "CURRENT_70_30")
    baseline_real_fail_pl = current_candidate["RealFailSequencePL"]

    rows: list[dict] = []
    filtered = 0
    for params in raw_params:
        valid, reason = is_valid_geometry_params(params.big_ratio, params.small_ratio, params.close_big_on_small)
        if not valid:
            filtered += 1
            continue
        row = evaluate_params(params, baseline_real_fail_pl, "GRID")
        row["FilterReason"] = reason
        rows.append(row)

    rows.sort(key=lambda r: (r["Score"], r["PassCount"], r["RealFailSequencePL"], -r["MaxDrawdownEstimate"], -r["MaxOpenLots"]), reverse=True)
    top10 = rows[:10]
    worst10 = sorted(rows, key=lambda r: (r["Score"], r["PassCount"], r["RealFailSequencePL"]))[:10]

    balanced_candidate = evaluate_params(_candidate(1.30, 0.42, 0.40, 0.50, 0.50, "BALANCED"), baseline_real_fail_pl, "BALANCED")
    strong_candidate = evaluate_params(_candidate(1.30, 0.45, 0.42, 0.50, 0.50, "STRONG_COMPRESSION"), baseline_real_fail_pl, "STRONG_COMPRESSION")
    valid_current, current_reason = is_valid_geometry_params(1.30, 0.37, 0.30)
    current_candidate["FilterReason"] = current_reason if not valid_current else "OK"

    summary = SweepSummary(
        raw_combinations=len(raw_params),
        filtered_combinations=filtered,
        tested_combinations=len(rows),
        scenarios_per_combination=len(SCENARIOS),
        rows=rows,
        top10=top10,
        worst10=worst10,
        current_candidate=current_candidate,
        balanced_candidate=balanced_candidate,
        strong_candidate=strong_candidate,
    )
    if write_reports:
        write_csv(summary)
        write_top10(summary)
        write_report(summary)
        write_mt5_plan(summary)
    return summary


def write_csv(summary: SweepSummary) -> None:
    if not summary.rows:
        return
    with SWEEP_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary.rows)


def _row_table(rows: list[dict]) -> str:
    headers = ["Rank", "Score", "BigRatio", "SmallRatio", "CloseBigOnSmall", "RemainBigOnSmall", "CloseFarShare", "ReserveShare", "MaxHarvestLevels", "MaxReverseCycles", "CompressionRatio", "BigNetPower", "PassCount", "StopMaxLevelsCount", "RealFailSequencePL"]
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for idx, row in enumerate(rows, start=1):
        values = [idx] + [row[h] for h in headers[1:]]
        lines.append("| " + " | ".join(str(v) for v in values) + " |")
    return "\n".join(lines)


def write_top10(summary: SweepSummary) -> None:
    TOP10_MD.write_text(
        "# Parameter Geometry Top 10\n\n"
        "Python-модель ранжирует кандидаты только для MT5-подтверждения; это не финальная победа стратегии.\n\n"
        "## Top 10\n\n" + _row_table(summary.top10) + "\n\n"
        "## Worst 10\n\n" + _row_table(summary.worst10) + "\n",
        encoding="utf-8",
    )


def _candidate_block(title: str, row: dict) -> str:
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
        f"- PassCount: {row['PassCount']} из {row['ScenarioCount']}\n"
        f"- StopMaxLevelsCount: {row['StopMaxLevelsCount']}\n"
        f"- RealFailSequencePL estimate: {row['RealFailSequencePL']}\n"
        f"- Score: {row['Score']}\n"
        f"- FilterReason: {row.get('FilterReason', 'OK')}\n\n"
    )


def write_report(summary: SweepSummary) -> None:
    best = summary.top10[0]
    text = f"""# Parameter Geometry Sweep Report

## 1. Цель подбора

Проведён полный Python-sweep геометрии MinusLock_BigHarvest_EA, чтобы найти кандидаты для MT5 Strategy Tester. PASS в модели считается только как предварительный кандидат: финально подтверждать нужно по RealRecoveryPL в MT5.

## 2. Почему текущая геометрия слабая

Текущий набор 1.30 / 0.37 / 0.30 даёт CompressionRatio = 1.30 × 0.70 = 0.91, то есть хвост после Small-at-Far уменьшается только примерно на 9%. Этот набор был отфильтрован правилом: {summary.current_candidate.get('FilterReason', 'OK')}.

## 3. Формула CompressionRatio

```text
CompressionRatio = BigRatio × RemainBigOnSmall
RemainBigOnSmall = 1 - CloseBigOnSmall
NewFarLot = OldFarLot × CompressionRatio
```

## 4. Формула BigNetPower

```text
BigNetPower = BigRatio × (1 - SmallRatio)
```

## 5. Фильтры плохих комбинаций

Raw combinations: {summary.raw_combinations}. Filtered combinations: {summary.filtered_combinations}. Tested combinations: {summary.tested_combinations}. Scenarios per combination: {summary.scenarios_per_combination}.

Фильтры: CloseBigOnSmall < SmallRatio, CompressionRatio между 0.60 и 0.90, BigNetPower >= 0.65, SmallRatio < 0.60, CloseBigOnSmall < 0.65.

## 6. Таблица Top 10

{_row_table(summary.top10)}

## 7. Таблица Worst 10

{_row_table(summary.worst10)}

{_candidate_block('8. Проверка текущего кандидата', summary.current_candidate)}{_candidate_block('9. Проверка сбалансированного кандидата', summary.balanced_candidate)}{_candidate_block('10. Проверка сильного сжатия', summary.strong_candidate)}## 11. Лучший найденный набор

- BigRatio: {best['BigRatio']}
- SmallRatio: {best['SmallRatio']}
- CloseBigOnSmall: {best['CloseBigOnSmall']}
- RemainBigOnSmall: {best['RemainBigOnSmall']}
- CloseFarShare: {best['CloseFarShare']}
- ReserveShare: {best['ReserveShare']}
- MaxHarvestLevels: {best['MaxHarvestLevels']}
- MaxReverseCycles: {best['MaxReverseCycles']}
- CompressionRatio: {best['CompressionRatio']}
- BigNetPower: {best['BigNetPower']}
- Score: {best['Score']}

## 12. Почему он выбран

Кандидат выбран Python-score: закрытые сценарии, положительная оценка recovery P/L, CompressionRatio в целевой зоне 0.70–0.82, BigNetPower >= 0.70, ReverseStrengthMin >= 0.15 и меньше штрафов за STOP_MAX_LEVELS/invalid geometry. Это математический кандидат, а не финальное доказательство прибыльности.

## 13. Риски

- Python-модель не заменяет MT5 Strategy Tester.
- RealRecoveryPLEstimate не учитывает реальные спреды, комиссии, свопы, проскальзывание и исполнение брокера.
- Все top-кандидаты нужно проверять с `FarDistanceMode = REAL_PRICE_DISTANCE` и `EnableCycleMathCsv = true`.
- OnTester в MT5 должен возвращать PASS только при `RealRecoveryPL > 0`.

## 14. Какие параметры нужно подтвердить в MT5

Подтвердить Top candidate, Second candidate и Conservative candidate из `mt5_parameter_confirmation_plan.md`; собрать Strategy Tester report, Experts log, `MinusLock_CycleMath.csv`, `REAL_CYCLE_MATH`, итоговый state и OnTester.
"""
    REPORT_MD.write_text(text, encoding="utf-8")


def write_mt5_plan(summary: SweepSummary) -> None:
    candidates = [summary.top10[0], summary.top10[1], summary.balanced_candidate]
    names = ["Top candidate", "Second candidate", "Conservative candidate"]
    lines = ["# MT5 Parameter Confirmation Plan", "", "Python-модель показывает кандидатов. Финальное подтверждение обязательно через MT5 Strategy Tester.", ""]
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
        "## Reports to collect",
        "",
        "- Strategy Tester report",
        "- Experts journal with CYCLE_MATH and REAL_CYCLE_MATH",
        "- MQL5/Files/MinusLock_CycleMath.csv",
        "- OnTester value",
        "- Final state and last system close comment",
        "- Open-position check for the MagicNumber",
        "",
        "## PASS criteria",
        "",
        "- State = STATE_CLOSED_PROFIT",
        "- RealRecoveryPL > 0",
        "- OnTester > 0 and equals real recovery result, not theoretical CycleFinalPL",
        "- No managed positions remain open",
        "- No STOP_MAX_LEVELS / STATE_UNCLOSED_CYCLE / STATE_ERROR",
        "",
        "## FAIL criteria",
        "",
        "- RealRecoveryPL <= 0",
        "- OnTester = -1",
        "- STOP_MAX_LEVELS, invalid reverse geometry, reverse limit, or unmanaged open positions",
        "- Missing CYCLE_MATH / REAL_CYCLE_MATH diagnostics",
        "",
    ]
    MT5_PLAN_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> SweepSummary:
    summary = run_geometry_sweep(write_reports=True)
    best = summary.top10[0]
    print(
        "GEOMETRY_SWEEP PASS: "
        f"raw={summary.raw_combinations} filtered={summary.filtered_combinations} "
        f"tested={summary.tested_combinations} scenarios={summary.scenarios_per_combination} "
        f"top_score={best['Score']} top=BigRatio:{best['BigRatio']} SmallRatio:{best['SmallRatio']} "
        f"CloseBigOnSmall:{best['CloseBigOnSmall']} CloseFarShare:{best['CloseFarShare']} ReserveShare:{best['ReserveShare']}"
    )
    print(f"CSV: {SWEEP_CSV}")
    print(f"Report: {REPORT_MD}")
    print(f"MT5 plan: {MT5_PLAN_MD}")
    return summary


if __name__ == "__main__":
    main()
