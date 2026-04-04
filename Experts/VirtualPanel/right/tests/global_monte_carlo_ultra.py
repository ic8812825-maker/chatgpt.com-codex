from __future__ import annotations

from pathlib import Path
from statistics import mean

from ale_alc_certification_lib import SimConfig, run_closed_loop_fast, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    scenarios = ["trend", "jump", "freeze", "dual-flow", "flash_crash", "spread_explosion", "margin_cascade", "fake_stability_trap", "opposite_signal_trap"]
    metrics = []
    for i in range(10000):
        sc = scenarios[i % len(scenarios)]
        cfg = SimConfig(
            scenario=sc,
            seed=22000 + i,
            steps=45,
            dual_flow=(sc in ("dual-flow", "opposite_signal_trap")),
            slippage=1.0 + (i % 5) * 0.12,
            spread=1.0 + (i % 4) * 0.08,
        )
        metrics.append(summarize(run_closed_loop_fast(cfg)))

    e_dv = mean(m["E_dV"] for m in metrics)
    p_non_pos = mean(m["P_dV_le_0"] for m in metrics)
    cvar = mean(m["cvar_95"] for m in metrics)
    collapse = mean(m["collapse"] for m in metrics)
    verdict = "PASS" if e_dv < 0 and 0.75 <= p_non_pos <= 0.90 and cvar < 0.09 and collapse == 0.0 else "FAIL"

    lines = [
        "# ALE_GLOBAL_MONTE_CARLO_ULTRA",
        "",
        "- runs: 10000",
        f"- E[ΔV]: {e_dv:.6f}",
        f"- P(ΔV<=0): {p_non_pos:.6f}",
        f"- CVaR95: {cvar:.6f}",
        f"- collapse_rate: {collapse:.6f}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_GLOBAL_MONTE_CARLO_ULTRA.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
