"""Расширенный тестовый стенд для системы «Адаптивная система поиска положительного EV».

Запускает сценарии разных рыночных режимов, автоматически подбирает
параметры в ограниченном диапазоне и формирует единый отчёт.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import itertools
import json
import math
import random
from typing import Dict, List, Tuple


@dataclass
class Params:
    lb0: float = 1.0
    ls0: float = 1.0
    pb: float = 100.0
    ps: float = 101.0
    spread: float = 0.20
    atr: float = 0.80
    alpha: float = 0.35
    delta_step: float = 0.35
    gamma: float = 0.18
    d_max: float = 2.00
    ls_min: float = 0.30


@dataclass
class Scenario:
    name: str
    mu: float
    sigma: float
    spread: float
    atr: float
    shock_prob: float = 0.0
    shock_scale: float = 0.0


def p_avg(lb: float, ls: float, pb: float, ps: float) -> float:
    return (lb * pb + ls * ps) / (lb + ls)


def delta_from_vol(spread: float, atr: float, alpha: float) -> float:
    return spread + alpha * atr


def survival(delta: float, ls: float, step: float, lb: float) -> bool:
    return delta * ls > step * lb


def rebalance_ratio(price: float, pb: float, ps: float, spread: float, delta: float) -> float:
    num = price - pb - spread / 2 + delta
    den = ps - price - spread / 2 - delta
    if abs(den) < 1e-12:
        return math.inf
    return num / den


def simulate_scenario(scn: Scenario, cfg: Params, steps: int = 700, seed: int = 42) -> Dict[str, float]:
    rng = random.Random(seed)

    lb, ls = cfg.lb0, cfg.ls0
    pb, ps = cfg.pb, cfg.ps
    price = (pb + ps) / 2
    equity = 0.0
    peak = 0.0
    max_dd = 0.0
    cycles = 0
    survival_violations = 0

    # адаптивные параметры
    delta = delta_from_vol(scn.spread, scn.atr, cfg.alpha)
    step = cfg.delta_step
    gamma = cfg.gamma

    for t in range(steps):
        # режимные шоки
        shock = 0.0
        if rng.random() < scn.shock_prob:
            shock = scn.shock_scale * rng.gauss(0, 1)

        price = price + scn.mu + scn.sigma * rng.gauss(0, 1) + shock
        center = p_avg(lb, ls, pb, ps)

        # простая адаптация режима
        local_vol = abs(price - center)
        if local_vol > 2.0 * step:
            gamma_eff = max(0.07, gamma * 0.65)   # STRESS: режем агрессию
            step_eff = min(0.7, step * 1.15)      # увеличиваем шаг
            delta_eff = min(1.5, delta * 1.10)    # увеличиваем edge
        else:
            gamma_eff = gamma
            step_eff = step
            delta_eff = delta

        if abs(price - center) > step_eff:
            ratio = rebalance_ratio(price, pb, ps, scn.spread, delta_eff)
            if math.isfinite(ratio) and ratio > 0:
                # ограничитель скорости позиции
                d_lb = min(gamma_eff, lb * 0.12)
                d_ls = min(d_lb * ratio, ls * 0.12)

                # защита минимального SELL
                if ls - d_ls < cfg.ls_min:
                    d_ls = max(0.0, ls - cfg.ls_min)

                lb -= d_lb
                ls -= d_ls

                # частичное переоткрытие SELL с небольшим сдвигом
                reopen = d_ls * 0.92
                ls += reopen
                ps = price + scn.spread / 2

                # proxy-PnL цикла
                cost = scn.spread * (d_lb + d_ls + reopen) * 0.5
                cycle_pnl = delta_eff * d_ls - cost
                equity += cycle_pnl
                cycles += 1

                # периодическая пересборка якорей
                if t % 120 == 0 and t > 0:
                    pb = price - scn.spread / 2

        if not survival(delta_eff, ls, step_eff, lb):
            survival_violations += 1
            # аварийная коррекция
            gamma = max(0.06, gamma * 0.90)
            step = min(0.8, step * 1.05)
            delta = min(1.8, delta * 1.10)

        peak = max(peak, equity)
        max_dd = max(max_dd, peak - equity)

    # критерий PASS по сценарию
    verdict = "PASS" if (equity > 0 and max_dd <= cfg.d_max and survival_violations == 0) else "FAIL"

    return {
        "scenario": scn.name,
        "steps": steps,
        "cycles": cycles,
        "equity": round(equity, 6),
        "max_drawdown": round(max_dd, 6),
        "survival_violations": survival_violations,
        "verdict": verdict,
    }


def evaluate_all_scenarios(cfg: Params, scenarios: List[Scenario], steps: int = 700) -> Tuple[bool, List[Dict[str, float]]]:
    results = []
    all_pass = True
    for i, scn in enumerate(scenarios):
        res = simulate_scenario(scn, cfg, steps=steps, seed=42 + i)
        results.append(res)
        if res["verdict"] != "PASS":
            all_pass = False
    return all_pass, results


def improve_until_all_pass(scenarios: List[Scenario], max_rounds: int = 12) -> Tuple[Params, List[Dict[str, float]], List[Dict[str, object]]]:
    base = Params()
    log: List[Dict[str, object]] = []

    grid_alpha = [0.30, 0.35, 0.40, 0.45]
    grid_step = [0.28, 0.32, 0.35, 0.40]
    grid_gamma = [0.12, 0.15, 0.18, 0.22]
    grid_lsmin = [0.25, 0.30, 0.35]

    best_cfg = base
    best_results: List[Dict[str, float]] = []

    for rnd in range(1, max_rounds + 1):
        found = False
        for alpha, step, gamma, lsmin in itertools.product(grid_alpha, grid_step, grid_gamma, grid_lsmin):
            cfg = Params(
                alpha=alpha,
                delta_step=step,
                gamma=gamma,
                ls_min=lsmin,
                d_max=2.0,
            )
            all_pass, results = evaluate_all_scenarios(cfg, scenarios)
            failures = [r["scenario"] for r in results if r["verdict"] != "PASS"]
            log.append(
                {
                    "round": rnd,
                    "params": asdict(cfg),
                    "all_pass": all_pass,
                    "failed_scenarios": failures,
                }
            )
            if all_pass:
                best_cfg = cfg
                best_results = results
                found = True
                break

        if found:
            return best_cfg, best_results, log

        # если не нашли, ужесточаем защиту для следующего раунда
        grid_alpha = [min(x + 0.03, 0.55) for x in grid_alpha]
        grid_step = [min(x + 0.03, 0.55) for x in grid_step]
        grid_gamma = [max(x - 0.02, 0.08) for x in grid_gamma]

    # fallback: вернуть лучший из последнего прохода (пусть и с FAIL)
    best_cfg = Params(alpha=grid_alpha[0], delta_step=grid_step[0], gamma=grid_gamma[0], ls_min=0.35, d_max=2.0)
    _, best_results = evaluate_all_scenarios(best_cfg, scenarios)
    return best_cfg, best_results, log


def write_report(path: Path, cfg: Params, results: List[Dict[str, float]], improvement_log: List[Dict[str, object]]) -> None:
    passed = all(r["verdict"] == "PASS" for r in results)
    lines = [
        "# Отчет тестирования системы Adaptive EV",
        "",
        f"- Итог: **{'PASS (все сценарии)' if passed else 'FAIL (есть провалы)'}**",
        "- Использованные оптимизированные параметры:",
        f"  - alpha={cfg.alpha}",
        f"  - delta_step={cfg.delta_step}",
        f"  - gamma={cfg.gamma}",
        f"  - ls_min={cfg.ls_min}",
        "",
        "## Результаты по сценариям",
    ]

    for r in results:
        lines.extend(
            [
                f"- **{r['scenario']}**: verdict={r['verdict']}, equity={r['equity']}, max_dd={r['max_drawdown']}, "
                f"survival_violations={r['survival_violations']}, cycles={r['cycles']}",
            ]
        )

    lines.extend(
        [
            "",
            "## JSON (results)",
            "```json",
            json.dumps(results, ensure_ascii=False, indent=2),
            "```",
            "",
            "## JSON (improvement_log, last 20 entries)",
            "```json",
            json.dumps(improvement_log[-20:], ensure_ascii=False, indent=2),
            "```",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    scenarios = [
        Scenario(name="FLAT_LOW_VOL", mu=0.00, sigma=0.25, spread=0.18, atr=0.55),
        Scenario(name="TREND_UP_MODERATE", mu=0.06, sigma=0.35, spread=0.20, atr=0.70),
        Scenario(name="TREND_DOWN_MODERATE", mu=-0.06, sigma=0.35, spread=0.20, atr=0.70),
        Scenario(name="VOLATILE_MEAN_ZERO", mu=0.00, sigma=0.85, spread=0.25, atr=1.00),
        Scenario(name="SHOCK_REGIME", mu=0.01, sigma=0.65, spread=0.28, atr=1.10, shock_prob=0.05, shock_scale=1.8),
    ]

    cfg, results, improvement_log = improve_until_all_pass(scenarios)

    report_path = Path("adaptive_ev_test_report.md")
    write_report(report_path, cfg, results, improvement_log)

    improvements_path = Path("adaptive_ev_implemented_improvements.md")
    improvements_path.write_text(
        "# Реализованные улучшения в тестовом стенде\n\n"
        "1. Добавлен мультисценарный прогон: флэт, тренд вверх, тренд вниз, высокая волатильность, shock-режим.\n"
        "2. Реализован цикл test->improve->retest через grid search параметров alpha/delta_step/gamma/ls_min.\n"
        "3. Добавлена режимная адаптация (STRESS): снижение gamma, рост delta_step и delta при всплесках отклонения.\n"
        "4. Введена защита минимального SELL (ls_min) и ограничитель скорости изменения позиции.\n"
        "5. Добавлена аварийная коррекция параметров при нарушении survival-условия.\n"
        "6. Добавлена периодическая пересборка якорей позиции (pb/ps) для ограничения структурного дрейфа.\n"
        "7. Финальный отчет содержит результаты всех сценариев и лог последних итераций улучшения.\n",
        encoding="utf-8",
    )

    print(json.dumps({"optimized_params": asdict(cfg), "results": results}, ensure_ascii=False))
    print(f"Отчет сохранен: {report_path}")
    print(f"Лог улучшений сохранен: {improvements_path}")
