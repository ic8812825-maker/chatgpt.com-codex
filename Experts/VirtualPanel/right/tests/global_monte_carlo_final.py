from __future__ import annotations

from pathlib import Path
from statistics import mean

from ale_alc_certification_lib import SimConfig, run_closed_loop_fast, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    scenarios = ["trend", "jump", "freeze", "dual-flow", "flash_crash", "spread_explosion", "margin_cascade"]
    total = 0
    rows = []
    for i in range(5000):
        sc = scenarios[i % len(scenarios)]
        cfg = SimConfig(
            scenario=sc,
            seed=12000 + i,
            steps=40,
            dual_flow=(sc == "dual-flow"),
            slippage=1.0 + (i % 5) * 0.15,
            spread=1.0 + (i % 4) * 0.1,
            mpc_horizon=2,
        )
        rows.append(summarize(run_closed_loop_fast(cfg)))
        total += 1

    e_dv = mean(r["E_dV"] for r in rows)
    p_non_pos = mean(r["P_dV_le_0"] for r in rows)
    cvar = mean(r["cvar_95"] for r in rows)
    verdict = "PASS" if e_dv < 0 and 0.70 <= p_non_pos <= 0.95 and cvar < 0.08 else "FAIL"

    lines = [
        "# ALE_GLOBAL_MONTE_CARLO_FINAL",
        "",
        f"- total_runs: {total}",
        f"- E[ΔV]: {e_dv:.6f}",
        f"- P(ΔV<=0): {p_non_pos:.6f}",
        f"- CVaR95: {cvar:.6f}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_GLOBAL_MONTE_CARLO_FINAL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
