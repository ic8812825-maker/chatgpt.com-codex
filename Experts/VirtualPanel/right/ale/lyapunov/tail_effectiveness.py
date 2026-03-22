from __future__ import annotations
import random
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent))
    from common import load_runner_module, ALE_ROOT
else:
    from .common import load_runner_module, ALE_ROOT


def run():
    m = load_runner_module()

    modes = ["shock", "adv_jump_cluster", "adv_liquidity_gap", "adv_liquidity_freeze"]
    rows = []
    for i, mode in enumerate(modes):
        random.seed(900 + i)
        base = m.simulate(mode, runs=1200, steps=520, k=1.4, R=140, alpha=0.5, with_control=False, with_alc=True)
        random.seed(900 + i)
        ctrl = m.simulate(mode, runs=1200, steps=520, k=1.4, R=140, alpha=0.5, with_control=True, with_alc=True)
        rows.append((mode, base, ctrl))

    path = ALE_ROOT / "ALE_TAIL_EFFECTIVENESS_REPORT.md"
    lines = [
        "# ALE_TAIL_EFFECTIVENESS_REPORT",
        "",
        "Tail-risk effectiveness of control layer on stress-heavy regimes.",
        "",
        "| mode | P(collapse) base | P(collapse) ctrl | Δrisk | pnl base | pnl ctrl |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    improved = 0
    for mode, base, ctrl in rows:
        delta = base["p_collapse"] - ctrl["p_collapse"]
        if delta > 0:
            improved += 1
        lines.append(
            f"| {mode} | {base['p_collapse']:.4f} | {ctrl['p_collapse']:.4f} | {delta:.4f} | {base['avg_pnl']:.4f} | {ctrl['avg_pnl']:.4f} |"
        )

    lines += [
        "",
        "## Summary",
        f"- Modes with risk improvement: {improved}/{len(rows)}.",
        "- A negative Δrisk means control worsened tail risk in that regime.",
        "- Stability requires preserving positive activity while reducing collapse probability.",
    ]

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
