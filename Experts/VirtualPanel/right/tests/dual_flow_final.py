from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    buy = run_closed_loop(SimConfig(scenario="dual-flow", seed=901, dual_flow=True, steps=320, slippage=1.3))
    sell = run_closed_loop(SimConfig(scenario="dual-flow", seed=902, dual_flow=True, steps=320, slippage=1.5))

    buy_pnl_proxy = -sum(buy.deltas)
    sell_pnl_proxy = -sum(sell.deltas)
    dominance = abs(buy_pnl_proxy - sell_pnl_proxy)

    runaway = max(abs(v1 - v2) for v1, v2 in zip(buy.values[: min(len(buy.values), len(sell.values))], sell.values[: min(len(buy.values), len(sell.values))]))
    feedback_explode = max(buy.values) > 2.7 or max(sell.values) > 2.7

    max_total_v = max(max(buy.values), max(sell.values))
    asymmetry = abs((sum(buy.deltas) / max(1, len(buy.deltas))) - (sum(sell.deltas) / max(1, len(sell.deltas))))
    verdict = "PASS" if max_total_v < 1.2 and asymmetry < 0.01 and runaway < 0.8 and not feedback_explode else "FAIL"

    lines = [
        "# ALE_DUAL_FLOW_FINAL",
        "",
        f"- max_total_V: {max_total_v:.6f}",
        f"- asymmetry: {asymmetry:.6f}",
        f"- dominance_abs: {dominance:.6f}",
        f"- runaway_metric: {runaway:.6f}",
        f"- feedback_explode: {feedback_explode}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_DUAL_FLOW_FINAL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
