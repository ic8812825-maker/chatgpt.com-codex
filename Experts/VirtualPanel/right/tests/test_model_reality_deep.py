from __future__ import annotations

from pathlib import Path
from statistics import mean

from ale_alc_certification_lib import ACTIONS, SimConfig, markdown_table, percentile, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    scenarios = ["trend", "jump", "freeze", "dual-flow"]
    rows = []
    per_action = {a: [] for a in ACTIONS}
    all_gaps = []
    all_bias = []

    for i, sc in enumerate(scenarios):
        pred = run_closed_loop(SimConfig(scenario=sc, seed=210 + i))
        real = run_closed_loop(SimConfig(scenario=sc, seed=210 + i, slippage=1.3, spread=1.25))
        n = min(len(pred.deltas), len(real.deltas), len(pred.actions))
        gaps = []
        signed = []
        for t in range(n):
            g = abs(pred.deltas[t] - real.deltas[t])
            s = pred.deltas[t] - real.deltas[t]
            gaps.append(g)
            signed.append(s)
            per_action[pred.actions[t]].append(g)
        all_gaps.extend(gaps)
        all_bias.extend(signed)
        rows.append({"scenario": sc, "mean_gap": round(mean(gaps), 6), "bias": round(mean(signed), 6), "tail95": round(percentile(gaps, 0.95), 6)})

    global_bias = mean(all_bias) if all_bias else 0.0
    tail95 = percentile(all_gaps, 0.95)
    action_rows = [{"action": a, "gap": round(mean(v), 6) if v else 0.0} for a, v in per_action.items() if v]
    verdict = "PASS" if abs(global_bias) < 0.01 and tail95 < 0.1 else "FAIL"

    lines = [
        "# ALE_MODEL_REALITY_DEEP",
        "",
        "## Scenario gap",
        markdown_table(rows, ["scenario", "mean_gap", "bias", "tail95"]),
        "",
        "## Per-action gap",
        markdown_table(action_rows, ["action", "gap"]),
        "",
        f"- global_bias_direction: {global_bias:.6f}",
        f"- top5% tail_gap: {tail95:.6f}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_MODEL_REALITY_DEEP.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
