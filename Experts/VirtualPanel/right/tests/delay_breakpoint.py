from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    critical_delay = None
    stable_until = 0
    rows = []
    for delay in range(0, 201):
        m = summarize(run_closed_loop(SimConfig(scenario="jump", seed=700 + delay, control_delay=delay)))
        stable = (m["max_V"] < 2.5) and (m["collapse"] == 0.0)
        rows.append((delay, stable, m["max_V"]))
        if stable:
            stable_until = delay
        elif critical_delay is None:
            critical_delay = delay
            break

    lines = [
        "# ALE_DELAY_BREAKPOINT",
        "",
        f"- stable_until_delay: {stable_until}",
        f"- critical_delay: {critical_delay if critical_delay is not None else 'not reached up to 200'}",
        "",
        "## first failures / boundary samples",
    ]
    for delay, stable, max_v in rows[max(0, len(rows)-8):]:
        lines.append(f"- delay={delay}: stable={stable}, max_V={max_v:.6f}")

    (ROOT / "ALE_DELAY_BREAKPOINT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
