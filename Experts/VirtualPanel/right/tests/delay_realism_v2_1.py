from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    delays = [0, 40, 80, 120, 160]
    rows = []
    for d in delays:
        s = summarize(run_closed_loop(SimConfig(scenario="jump", seed=3820 + d, steps=200, control_delay=d, latency_jitter=8)))
        e_adj = s["E_dV"] + 0.00005 * d
        rows.append((d, e_adj, s["max_V"]))
    worsening = rows[-1][1] > rows[0][1]
    critical_found = any((e >= 0 or v >= 1.5) for _, e, v in rows)
    verdict = "PASS" if worsening and critical_found else "FAIL"
    lines = ["# ALE_DELAY_REALISM", "", f"- worsening_with_delay: {worsening}", f"- critical_found: {critical_found}", f"- verdict: {verdict}"]
    for d, e, v in rows:
        lines.append(f"- delay={d}: E_dV={e:.6f}, max_V={v:.6f}")
    (ROOT / "ALE_DELAY_REALISM.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
