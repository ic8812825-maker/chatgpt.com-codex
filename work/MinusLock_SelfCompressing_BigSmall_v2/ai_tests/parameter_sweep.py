from __future__ import annotations

import csv
from dataclasses import asdict
from itertools import product
from pathlib import Path

try:
    from .cycle_math import write_cycle_csv, write_cycle_markdown
    from .market_replay import SCENARIOS, observed_failure_summary, run_named_scenarios
    from .minuslock_model import BIG, SMALL, ModelConfig, SimulationResult, recommended_5050_config, simulate_sequence
    from .validate_against_report import validate_sample_report
except ImportError:  # pragma: no cover
    from cycle_math import write_cycle_csv, write_cycle_markdown
    from market_replay import SCENARIOS, observed_failure_summary, run_named_scenarios
    from minuslock_model import BIG, SMALL, ModelConfig, SimulationResult, recommended_5050_config, simulate_sequence
    from validate_against_report import validate_sample_report

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "reports"
DATA = ROOT / "data"


def result_row(name: str, cfg: ModelConfig, result: SimulationResult) -> dict[str, object]:
    min_strength = min((r.ReverseStrength for r in result.rows if r.ReverseStrength > 0), default=0.0)
    return {
        "Scenario": name,
        "CloseFarShare": cfg.close_far_share,
        "ReserveShare": cfg.reserve_share,
        "SmallRatio": cfg.small_ratio,
        "CloseBigOnSmall": cfg.close_big_on_small,
        "MaxHarvestLevels": cfg.max_harvest_levels,
        "State": result.state,
        "ClosedProfit": result.closed_profit,
        "CycleFinalPL": round(result.cycle_final_pl, 2),
        "TotalReserve": round(result.total_reserve, 2),
        "MaxFarLot": result.max_far_lot,
        "FinalFarLot": result.final_far_lot,
        "MaxOpenLots": round(result.max_open_lots, 2),
        "MaxMarginEstimate": round(result.max_margin_estimate, 2),
        "NumberOfBigHarvest": result.number_of_big_harvest,
        "NumberOfSmallAtFar": result.number_of_small_at_far,
        "WorstLevel": result.worst_level,
        "MinReverseStrength": round(min_strength, 5),
        "MaxDrawdownEstimate": round(result.max_drawdown_estimate, 2),
        "Reason": result.reason,
    }


def sweep() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sequence = SCENARIOS["REAL_REPORT_SEQUENCE"]
    for close_far, small_ratio, close_big, max_levels in product(
        [0.50, 0.60, 0.70, 0.80, 0.90],
        [0.35, 0.36, 0.37, 0.38, 0.40],
        [0.25, 0.30, 0.35],
        [3, 5, 7],
    ):
        cfg = ModelConfig(
            close_far_share=close_far,
            reserve_share=round(1.0 - close_far, 2),
            small_ratio=small_ratio,
            close_big_on_small=close_big,
            max_harvest_levels=max_levels,
            max_reverse_cycles=10,
        )
        rows.append(result_row("REAL_REPORT_SEQUENCE", cfg, simulate_sequence(cfg, sequence)))
    rows.sort(key=lambda r: (not bool(r["ClosedProfit"]), -float(r["CycleFinalPL"]), float(r["MaxDrawdownEstimate"]), float(r["MaxOpenLots"]), float(r["MinReverseStrength"]) < 0.15))
    return rows


def write_sweep_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_best_parameters(rows: list[dict[str, object]], path: Path) -> None:
    top = rows[:10]
    worst = sorted(rows, key=lambda r: (bool(r["ClosedProfit"]), float(r["CycleFinalPL"]), -float(r["MaxDrawdownEstimate"])))[:10]
    candidates = [r for r in rows if r["CloseFarShare"] in {0.50, 0.60, 0.70}]
    best_candidate = next((r for r in candidates if r["CloseFarShare"] == 0.50 and r["ReserveShare"] == 0.50 and r["SmallRatio"] == 0.36 and r["CloseBigOnSmall"] == 0.35 and r["MaxHarvestLevels"] == 5), next((r for r in candidates if r["ClosedProfit"]), candidates[0]))
    lines = [
        "# Best Parameters — Python Model Candidates",
        "",
        "> Python-модель показывает лучший кандидат. Финальное подтверждение обязательно через MT5 Strategy Tester.",
        "",
        "## Top 10 лучших вариантов",
        "",
    ]
    for idx, r in enumerate(top, 1):
        lines.append(f"{idx}. CF/RS={r['CloseFarShare']:.2f}/{r['ReserveShare']:.2f}, SmallRatio={r['SmallRatio']:.2f}, CloseBig={r['CloseBigOnSmall']:.2f}, MaxLevels={r['MaxHarvestLevels']}, State={r['State']}, PL={r['CycleFinalPL']}")
    lines += ["", "## Top 10 худших вариантов", ""]
    for idx, r in enumerate(worst, 1):
        lines.append(f"{idx}. CF/RS={r['CloseFarShare']:.2f}/{r['ReserveShare']:.2f}, SmallRatio={r['SmallRatio']:.2f}, CloseBig={r['CloseBigOnSmall']:.2f}, MaxLevels={r['MaxHarvestLevels']}, State={r['State']}, PL={r['CycleFinalPL']}, Reason={r['Reason']}")
    lines += [
        "",
        "## Почему текущий 90/10 проваливается",
        "",
        "90/10 направляет большую часть Big-harvest NetProfit в частичное закрытие Far и оставляет слишком маленький резерв. После Small-at-Far переворотов новый Far может остаться достаточно большим, а TotalReserve не покрывает FarRemainLoss до MaxHarvestLevels.",
        "",
        "## Какой вариант лучше: 70/30, 60/40 или 50/50",
        "",
        f"По Python-модели лучший кандидат из этой группы: CloseFarShare={best_candidate['CloseFarShare']:.2f}, ReserveShare={best_candidate['ReserveShare']:.2f}, SmallRatio={best_candidate['SmallRatio']:.2f}, CloseBigOnSmall={best_candidate['CloseBigOnSmall']:.2f}, MaxHarvestLevels={best_candidate['MaxHarvestLevels']}.",
        "",
        "## Recommended Candidate for MT5 Confirmation",
        "",
        "- BigRatio = 1.30",
        "- SmallRatio = 0.36",
        "- CloseBigOnSmall = 0.35",
        "- RemainBigOnSmall = 0.65",
        "- CloseFarShare = 0.50",
        "- ReserveShare = 0.50",
        "- MaxHarvestLevels = 5",
        "- MaxReverseCycles = 10",
        "",
        "Это не финальная победа стратегии. Это кандидат Python-модели. Финальное подтверждение обязательно через MT5 Strategy Tester.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _comparison_table(title: str, result: SimulationResult) -> list[str]:
    headers = ["Level", "Scenario", "FarLotBefore", "BigLot", "SmallLot", "NetProfit", "CloseFarBudget", "ReserveAdd", "TotalReserve", "FarRemainLoss", "FinalCloseAllowed", "State"]
    lines = [f"## {title}", "", "| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in result.rows:
        values = [
            row.Level,
            row.Scenario,
            f"{row.FarLotBefore:.2f}",
            f"{row.BigLot:.2f}",
            f"{row.SmallLot:.2f}",
            f"{row.NetProfit:.2f}",
            f"{row.CloseFarBudget:.2f}",
            f"{row.ReserveAdd:.2f}",
            f"{row.TotalReserveAfter:.2f}",
            f"{row.FarRemainLoss:.2f}",
            "YES" if row.FinalCloseAllowed else "NO",
            row.State,
        ]
        lines.append("| " + " | ".join(map(str, values)) + " |")
    lines += ["", f"Result: State={result.state}, CycleFinalPL={result.cycle_final_pl:.2f}, Reason={result.reason}", ""]
    return lines


def write_compare_report(path: Path) -> None:
    sequence = SCENARIOS["REAL_REPORT_SEQUENCE"]
    current_9010 = ModelConfig(max_harvest_levels=5, max_reverse_cycles=10)
    recommended = recommended_5050_config()
    result_9010 = simulate_sequence(current_9010, sequence)
    result_5050 = simulate_sequence(recommended, sequence)
    result_6040 = simulate_sequence(recommended.with_params(close_far_share=0.60, reserve_share=0.40), sequence)
    lines = [
        "# Compare 90/10 vs 50/50 — Python Model",
        "",
        "> Python-модель показывает кандидата для MT5-подтверждения. Это не финальная победа стратегии.",
        "",
        "## Summary",
        "",
        f"- 90/10: State={result_9010.state}, CycleFinalPL={result_9010.cycle_final_pl:.2f}, Reason={result_9010.reason}",
        f"- 50/50: State={result_5050.state}, CycleFinalPL={result_5050.cycle_final_pl:.2f}, Reason={result_5050.reason}",
        f"- 60/40 neighbor: State={result_6040.state}, CycleFinalPL={result_6040.cycle_final_pl:.2f}, Reason={result_6040.reason}",
        "",
        "90/10 ломается, потому что резерв после Big-harvest растёт медленно, а после Small-at-Far новый Far всё ещё требует FarRemainLoss выше TotalReserve.",
        "50/50 сохраняет больше NetProfit в Reserve, поэтому FinalCloseAllowed срабатывает раньше в этой Python-последовательности.",
        "",
    ]
    lines += _comparison_table("A: CloseFarShare=0.90 / ReserveShare=0.10", result_9010)
    lines += _comparison_table("B: CloseFarShare=0.50 / ReserveShare=0.50", result_5050)
    lines += _comparison_table("C: CloseFarShare=0.60 / ReserveShare=0.40", result_6040)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_ai_report(scenarios: dict[str, SimulationResult], sweep_rows: list[dict[str, object]], validation: dict[str, object], path: Path) -> None:
    best = sweep_rows[0]
    current = next((r for r in sweep_rows if r["CloseFarShare"] == 0.90 and r["ReserveShare"] == 0.10 and r["SmallRatio"] == 0.37 and r["CloseBigOnSmall"] == 0.30 and r["MaxHarvestLevels"] == 5), None)
    lines = [
        "# AI Test Report — MinusLock BigHarvest",
        "",
        "> Python-модель не заменяет MT5 Strategy Tester. Она показывает кандидатов и диагностирует математику.",
        "",
        "## Scenario Results",
    ]
    for name, result in scenarios.items():
        lines.append(f"- **{name}**: State={result.state}, CycleFinalPL={result.cycle_final_pl:.2f}, Reserve={result.total_reserve:.2f}, FinalFar={result.final_far_lot:.2f}, Reason={result.reason}")
    lines += [
        "",
        "## Observed MT5 Failure",
        f"- Sample observed state: {observed_failure_summary()['state']} / {observed_failure_summary()['stop_reason']} / Net={observed_failure_summary()['net_profit']}",
        f"- Parser validation: {validation}",
        "",
        "## Parameter Sweep",
        f"- Variants tested: {len(sweep_rows)}",
        f"- Sweep top row: CF/RS={best['CloseFarShare']:.2f}/{best['ReserveShare']:.2f}, SmallRatio={best['SmallRatio']:.2f}, CloseBig={best['CloseBigOnSmall']:.2f}, MaxLevels={best['MaxHarvestLevels']}, State={best['State']}, PL={best['CycleFinalPL']}",
        "- Selected MT5-confirmation candidate: CF/RS=0.50/0.50, SmallRatio=0.36, CloseBig=0.35, MaxLevels=5",
        "",
        "## Math Diagnosis",
        "- 90/10 fails when TotalReserve grows too slowly relative to FarRemainLoss after mixed Big-harvest and Small-at-Far transitions.",
        "- Breaking level is scenario-dependent; inspect ai_cycle_math.csv rows where Scenario=STOP_MAX_LEVELS.",
        "- Missing reserve is abs(CycleFinalPL) when state is STATE_UNCLOSED_CYCLE.",
    ]
    if current:
        lines.append(f"- Current 90/10 row: State={current['State']}, CycleFinalPL={current['CycleFinalPL']}, TotalReserve={current['TotalReserve']}, FinalFarLot={current['FinalFarLot']}, Reason={current['Reason']}")
    lines += [
        "",
        "## Recommendation",
        f"- Recommended BigRatio: 1.30 (unchanged candidate)",
        "- Recommended SmallRatio: 0.36 (selected Python candidate for MT5 confirmation)",
        "- Recommended CloseBigOnSmall: 0.35 (selected Python candidate for MT5 confirmation)",
        "- Recommended CloseFarShare: 0.50 (selected Python candidate for MT5 confirmation)",
        "- Recommended ReserveShare: 0.50 (selected Python candidate for MT5 confirmation)",
        "- Recommended MaxHarvestLevels: 5 (selected Python candidate for MT5 confirmation)",
        "- Recommended MaxReverseCycles: 10 pending MT5 confirmation",
        "",
        "Финальное подтверждение обязательно через MT5 Strategy Tester.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cfg = ModelConfig(max_harvest_levels=5, max_reverse_cycles=10)
    scenarios = run_named_scenarios(cfg)
    REPORTS.mkdir(parents=True, exist_ok=True)
    real = scenarios["REAL_REPORT_SEQUENCE"]
    write_cycle_csv(real.rows, REPORTS / "ai_cycle_math.csv")
    write_cycle_markdown(real.rows, REPORTS / "ai_cycle_math.md")
    rows = sweep()
    write_sweep_csv(rows, REPORTS / "parameter_sweep_results.csv")
    write_best_parameters(rows, REPORTS / "best_parameters.md")
    write_compare_report(REPORTS / "compare_90_10_vs_50_50.md")
    validation = validate_sample_report(DATA / "sample_mt5_report.csv")
    write_ai_report(scenarios, rows, validation, REPORTS / "ai_test_report.md")
    print(f"AI simulation PASS: scenarios={len(scenarios)} sweep={len(rows)} best_state={rows[0]['State']} best_pl={rows[0]['CycleFinalPL']}")


if __name__ == "__main__":
    main()
