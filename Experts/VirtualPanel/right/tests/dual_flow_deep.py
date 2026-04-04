from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    buy_flow = run_closed_loop(SimConfig(scenario="dual-flow", seed=901, dual_flow=True, steps=260))
    sell_flow = run_closed_loop(SimConfig(scenario="dual-flow", seed=902, dual_flow=True, steps=260))

    max_total_v = max(max(buy_flow.values), max(sell_flow.values))
    buy_mean = sum(buy_flow.deltas) / max(1, len(buy_flow.deltas))
    sell_mean = sum(sell_flow.deltas) / max(1, len(sell_flow.deltas))
    asymmetry = abs(buy_mean - sell_mean)
    collapse = int(buy_flow.collapse or sell_flow.collapse)
    verdict = "PASS" if max_total_v < 1.2 and asymmetry < 0.01 and collapse == 0 else "FAIL"

    lines = [
        "# ALE_DUAL_FLOW_DEEP",
        "",
        f"- max_total_V: {max_total_v:.6f} (target < 1.2)",
        f"- asymmetry: {asymmetry:.6f} (target < 0.01)",
        f"- collapse: {collapse} (target = 0)",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_DUAL_FLOW_DEEP.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
