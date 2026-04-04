from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    stable_until = 0
    critical = None
    rows = []
    for d in range(0, 201):
        m = summarize(run_closed_loop(SimConfig(scenario="jump", seed=800 + d, steps=120, control_delay=d, latency_jitter=3)))
        stable = m["max_V"] < 2.5 and m["collapse"] == 0.0 and m["E_dV"] < 0.01
        rows.append((d, stable, m["max_V"], m["E_dV"]))
        if stable:
            stable_until = d
        elif critical is None:
            critical = d
            break

    lines = [
        "# ALE_DELAY_BREAKPOINT_DEEP",
        "",
        f"- stable_until: {stable_until}",
        f"- critical_delay: {critical if critical is not None else 'not found <=200'}",
        "",
        "## boundary samples",
    ]
    for r in rows[-10:]:
        lines.append(f"- delay={r[0]} stable={r[1]} max_V={r[2]:.6f} E_dV={r[3]:.6f}")

    (ROOT / "ALE_DELAY_BREAKPOINT_DEEP.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
