from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    buy = run_closed_loop(SimConfig(scenario="dual-flow", seed=3701, steps=320, dual_flow=True, slippage=1.6))
    sell = run_closed_loop(SimConfig(scenario="opposite_signal_trap", seed=3702, steps=320, dual_flow=True, control_delay=10, slippage=1.8))

    max_total_v = max(max(buy.values), max(sell.values))
    asym = abs((sum(buy.deltas) / len(buy.deltas)) - (sum(sell.deltas) / len(sell.deltas)))
    verdict = "PASS" if max_total_v < 1.2 and asym < 0.01 else "FAIL"

    lines = [
        "# ALE_DUAL_FLOW_V2",
        "",
        f"- max_total_V: {max_total_v:.6f}",
        f"- asymmetry: {asym:.6f}",
        f"- collapse_any: {int(buy.collapse or sell.collapse)}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_DUAL_FLOW_V2.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
