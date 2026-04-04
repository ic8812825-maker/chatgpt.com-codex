from __future__ import annotations

from pathlib import Path
from statistics import mean

from ale_alc_certification_lib import SimConfig, markdown_table, percentile, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    rows = []
    tails = []
    cvars = []
    for i, sc in enumerate(["trend", "jump", "freeze", "spread_explosion"]):
        r = run_closed_loop(SimConfig(scenario=sc, seed=3000 + i, steps=260))
        e = mean(r.deltas)
        c = mean(sorted(r.deltas)[int(0.95 * len(r.deltas)) :])
        t = percentile(r.deltas, 0.99)
        tails.append(t)
        cvars.append(c)
        rows.append({"scenario": sc, "E_dV": round(e, 6), "CVaR95": round(c, 6), "max_spike": round(t, 6)})

    verdict = "PASS" if mean(cvars) < 0.08 and max(tails) < 0.15 else "FAIL"
    lines = [
        "# ALE_OBJECTIVE_ALIGNMENT_V2",
        "",
        markdown_table(rows, ["scenario", "E_dV", "CVaR95", "max_spike"]),
        "",
        f"- cvar_mean: {mean(cvars):.6f}",
        f"- tail_max: {max(tails):.6f}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_OBJECTIVE_ALIGNMENT_V2.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
