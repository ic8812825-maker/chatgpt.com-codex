from __future__ import annotations

from pathlib import Path
from statistics import mean

from ale_alc_certification_lib import SimConfig, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    scenarios = ["trend", "jump", "freeze", "dual-flow", "flash_crash", "spread_explosion"]
    rows = []
    total_runs = 0
    for sc in scenarios:
        for j in range(400):  # 6 * 400 = 2400
            cfg = SimConfig(scenario=sc, seed=1200 + len(rows) * 1000 + j, dual_flow=(sc == "dual-flow"))
            m = summarize(run_closed_loop(cfg))
            rows.append(m)
            total_runs += 1

    e_dv = mean(r["E_dV"] for r in rows)
    collapse = mean(r["collapse"] for r in rows)
    stability = mean(1.0 if r["max_V"] < 2.5 else 0.0 for r in rows)
    verdict = "PASS" if e_dv < 0 and collapse <= 0.001 and stability > 0.99 else "FAIL"

    lines = [
        "# ALE_GLOBAL_MONTE_CARLO",
        "",
        f"- total_runs: {total_runs}",
        f"- E[ΔV]: {e_dv:.6f}",
        f"- collapse_rate: {collapse:.6f}",
        f"- stability_ratio: {stability:.6f}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_GLOBAL_MONTE_CARLO.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
