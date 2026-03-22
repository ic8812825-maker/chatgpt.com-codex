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
    rows = []
    for delay in [0, 2, 5, 8, 12, 16]:
        random.seed(500 + delay)
        out = m.simulate(
            "adv_liquidity_freeze",
            runs=1200,
            steps=500,
            k=1.4,
            R=140,
            alpha=0.5,
            with_control=True,
            with_alc=True,
            spread_mult=8.0,
            control_delay=delay,
            slippage_mult=2.0,
        )
        rows.append((delay, out))

    baseline_seed = 777
    random.seed(baseline_seed)
    no_control = m.simulate(
        "adv_liquidity_freeze",
        runs=1200,
        steps=500,
        k=1.4,
        R=140,
        alpha=0.5,
        with_control=False,
        with_alc=True,
        spread_mult=8.0,
        control_delay=0,
        slippage_mult=2.0,
    )

    path = ALE_ROOT / "ALE_CONTROL_LATENCY_REPORT.md"
    lines = [
        "# ALE_CONTROL_LATENCY_REPORT",
        "",
        "Latency sensitivity under adversarial liquidity-freeze conditions.",
        "",
        "| delay_ticks | P(collapse) | avg_drawdown | activity_ratio | control_intensity |",
        "|---:|---:|---:|---:|---:|",
    ]

    for d, r in rows:
        lines.append(
            f"| {d} | {r['p_collapse']:.4f} | {r['avg_max_drawdown']:.4f} | {r['activity_ratio']:.4f} | {r['control_intensity']:.4f} |"
        )

    best = min(rows, key=lambda x: x[1]["p_collapse"])
    worst = max(rows, key=lambda x: x[1]["p_collapse"])

    lines += [
        "",
        "## Baseline (no control)",
        f"- P(collapse): {no_control['p_collapse']:.4f}",
        f"- avg_drawdown: {no_control['avg_max_drawdown']:.4f}",
        "",
        "## Conclusion",
        f"- Best delay by collapse-risk: {best[0]} ticks (P={best[1]['p_collapse']:.4f}).",
        f"- Worst delay by collapse-risk: {worst[0]} ticks (P={worst[1]['p_collapse']:.4f}).",
        "- Non-monotonic behavior indicates latency interacts with spread/slippage shocks.",
        "- Delays that materially increase P(collapse) are treated as unstable operation points.",
    ]

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
