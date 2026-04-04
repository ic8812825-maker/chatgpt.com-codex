from __future__ import annotations

from pathlib import Path
from statistics import mean

from ale_alc_certification_lib import SimConfig, markdown_table, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    scenarios = [
        "flash_crash",
        "infinite_trend",
        "spread_explosion",
        "jump",
        "margin_cascade",
        "dual-flow",
    ]
    rows = []
    for i, sc in enumerate(scenarios):
        cfg = SimConfig(scenario=sc, seed=600 + i, slippage=1.8 if "spread" in sc else 1.3, spread=2.4 if "spread" in sc else 1.1, control_delay=8 if sc == "jump" else 0, dual_flow=(sc == "dual-flow"))
        m = summarize(run_closed_loop(cfg))
        rows.append({"scenario": sc, "E_dV": round(m["E_dV"], 6), "collapse": int(m["collapse"]), "max_V": round(m["max_V"], 6)})

    e_dv = mean(r["E_dV"] for r in rows)
    collapse_rate = mean(r["collapse"] for r in rows)
    max_v = max(r["max_V"] for r in rows)
    verdict = "PASS" if e_dv < 0 and collapse_rate < 0.05 and max_v < 3.0 else "FAIL"

    lines = [
        "# ALE_ADVERSARIAL_REPORT",
        "",
        markdown_table(rows, ["scenario", "E_dV", "collapse", "max_V"]),
        "",
        f"- E[ΔV]: {e_dv:.6f} (target < 0)",
        f"- collapse_rate: {collapse_rate:.6f} (target < 0.05)",
        f"- max(V): {max_v:.6f} (bounded)",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_ADVERSARIAL_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
