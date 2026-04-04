from __future__ import annotations

from pathlib import Path
from statistics import mean

from ale_alc_certification_lib import SimConfig, markdown_table, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    cases = [
        ("cascade_failure", SimConfig("margin_cascade", seed=1601, steps=280, slippage=2.0, spread=4.0)),
        ("fake_stability_trap", SimConfig("fake_stability_trap", seed=1602, steps=280, slippage=1.6, spread=2.2)),
        ("opposite_signal_trap", SimConfig("opposite_signal_trap", seed=1603, steps=280, dual_flow=True, control_delay=8, latency_jitter=12)),
    ]
    rows = []
    for name, cfg in cases:
        m = summarize(run_closed_loop(cfg))
        rows.append({"scenario": name, "E_dV": round(m["E_dV"], 6), "collapse": int(m["collapse"]), "P_dV_le_0": round(m["P_dV_le_0"], 6)})

    collapse = mean(r["collapse"] for r in rows)
    e_dv = mean(r["E_dV"] for r in rows)
    verdict = "PASS" if collapse < 0.01 and e_dv < 0 else "FAIL"

    lines = [
        "# ALE_ADVERSARIAL_HARDENED",
        "",
        markdown_table(rows, ["scenario", "E_dV", "P_dV_le_0", "collapse"]),
        "",
        f"- collapse_rate: {collapse:.6f}",
        f"- E[ΔV]: {e_dv:.6f}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_ADVERSARIAL_HARDENED.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
