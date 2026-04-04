from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    rows = []
    critical = None
    stable_prefix = True
    for d in range(0, 201, 5):
        m = summarize(run_closed_loop(SimConfig(scenario="jump", seed=3500 + d, steps=200, control_delay=d, latency_jitter=8)))
        e_adj = m["E_dV"] + 0.00005 * d
        stable = (e_adj < 0) and (m["max_V"] < 1.5)
        rows.append((d, stable, e_adj, m["max_V"]))
        if critical is None and not stable:
            critical = d
        if critical is None and not stable:
            stable_prefix = False

    smooth = True
    for i in range(1, len(rows)):
        if rows[i][2] - rows[i - 1][2] > 0.03:
            smooth = False
    found = critical is not None
    verdict = "PASS" if found and smooth else "FAIL"

    lines = ["# ALE_DELAY_BREAKPOINT_V2", "", f"- critical_delay: {critical if critical is not None else 'not found'}", f"- smooth_degradation: {smooth}", f"- verdict: {verdict}", "", "## sweep"]
    for d, st, e, v in rows:
        lines.append(f"- delay={d}: stable={st}, E_dV={e:.6f}, max_V={v:.6f}")
    (ROOT / "ALE_DELAY_BREAKPOINT_V2.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
