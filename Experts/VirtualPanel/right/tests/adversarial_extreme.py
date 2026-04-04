from __future__ import annotations

from pathlib import Path
from statistics import mean

from ale_alc_certification_lib import SimConfig, markdown_table, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    scenarios = [
        ("cascade_margin", SimConfig("margin_cascade", seed=700, slippage=1.8, spread=1.8, latency_jitter=15)),
        ("spread_x10", SimConfig("spread_explosion", seed=701, slippage=2.0, spread=10.0, latency_jitter=10)),
        ("latency_jitter", SimConfig("jump", seed=702, control_delay=10, latency_jitter=25, slippage=1.6)),
        ("asym_buy", SimConfig("dual-flow", seed=703, dual_flow=True, slippage=1.4)),
        ("asym_sell", SimConfig("dual-flow", seed=704, dual_flow=True, slippage=1.8)),
    ]
    rows = []
    for name, cfg in scenarios:
        m = summarize(run_closed_loop(cfg))
        rows.append({"scenario": name, "E_dV": round(m["E_dV"], 6), "collapse": int(m["collapse"]), "P_dV_le_0": round(m["P_dV_le_0"], 6)})

    collapse = mean(r["collapse"] for r in rows)
    e_dv = mean(r["E_dV"] for r in rows)
    verdict = "PASS" if collapse < 0.05 and e_dv < 0 else "FAIL"

    lines = [
        "# ALE_ADVERSARIAL_EXTREME",
        "",
        markdown_table(rows, ["scenario", "E_dV", "P_dV_le_0", "collapse"]),
        "",
        f"- collapse_rate: {collapse:.6f}",
        f"- E[ΔV]: {e_dv:.6f}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_ADVERSARIAL_EXTREME.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
