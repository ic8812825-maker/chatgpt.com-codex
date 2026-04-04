from __future__ import annotations

from pathlib import Path
from statistics import mean

from ale_alc_certification_lib import SimConfig, markdown_table, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    scenarios = ["trend", "jump", "freeze", "dual-flow"]
    rows = []
    for i, sc in enumerate(scenarios):
        pred = run_closed_loop(SimConfig(scenario=sc, seed=200 + i))
        real = run_closed_loop(SimConfig(scenario=sc, seed=200 + i, slippage=1.15, spread=1.1))
        paired = min(len(pred.deltas), len(real.deltas))
        gaps = [abs(pred.deltas[t] - real.deltas[t]) for t in range(paired)]
        bias = mean(pred.deltas[t] - real.deltas[t] for t in range(paired)) if paired else 0.0
        rows.append(
            {
                "scenario": sc,
                "mean_gap": round(mean(gaps) if gaps else 0.0, 6),
                "worst_gap": round(max(gaps) if gaps else 0.0, 6),
                "bias": round(bias, 6),
            }
        )

    mean_gap = mean(r["mean_gap"] for r in rows)
    worst_gap = max(r["worst_gap"] for r in rows)
    bias = mean(r["bias"] for r in rows)
    verdict = "PASS" if mean_gap < 0.01 and worst_gap < 0.1 and abs(bias) < 0.01 else "FAIL"

    lines = [
        "# ALE_MODEL_REALITY_GAP",
        "",
        "Model-vs-real execution gap under matched seeds and stressed execution conditions.",
        "",
        "## Scenario breakdown",
        markdown_table(rows, ["scenario", "mean_gap", "worst_gap", "bias"]),
        "",
        "## KPI",
        f"- mean_gap: {mean_gap:.6f} (target < 0.01)",
        f"- worst_gap: {worst_gap:.6f} (target < 0.1)",
        f"- bias: {bias:.6f} (target ≈ 0)",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_MODEL_REALITY_GAP.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
