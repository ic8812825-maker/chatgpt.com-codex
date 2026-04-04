from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, markdown_table, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    rows = []
    prev_strength = 0.0
    non_decreasing = True
    for d in [0, 20, 40, 60, 80, 100, 120, 150, 200]:
        res = run_closed_loop(SimConfig(scenario="jump", seed=1700 + d, steps=180, control_delay=d, latency_jitter=5))
        m = summarize(res)
        strength = sum(res.control_strength) / max(1, len(res.control_strength))
        if strength + 1e-9 < prev_strength:
            non_decreasing = False
        prev_strength = strength
        rows.append({"delay": d, "E_dV": round(m["E_dV"], 6), "strength": round(strength, 6)})

    all_negative = all(r["E_dV"] < 0 for r in rows)
    verdict = "PASS" if all_negative and non_decreasing else "FAIL"
    lines = [
        "# ALE_DELAY_ADAPTIVE",
        "",
        markdown_table(rows, ["delay", "E_dV", "strength"]),
        "",
        f"- E[ΔV] negative for all delays: {all_negative}",
        f"- control_strength increases with delay: {non_decreasing}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_DELAY_ADAPTIVE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
