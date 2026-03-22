from __future__ import annotations
import random
from statistics import mean
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent))
    from common import load_runner_module, ALE_ROOT
    from lyapunov_builder import (
        LyapunovState,
        lyapunov_value_improved,
        lyapunov_value_baseline,
        IMPROVED_COEFFS,
        BASE_COEFFS,
    )
else:
    from .common import load_runner_module, ALE_ROOT
    from .lyapunov_builder import (
        LyapunovState,
        lyapunov_value_improved,
        lyapunov_value_baseline,
        IMPROVED_COEFFS,
        BASE_COEFFS,
    )


def _percentile(series: list[float], q: float) -> float:
    if not series:
        return 0.0
    data = sorted(series)
    idx = int(round((len(data) - 1) * q))
    return data[max(0, min(len(data) - 1, idx))]


def run_path(mode: str, steps: int = 1200, seed: int = 1):
    m = load_runner_module()
    random.seed(seed)

    price = 1.0
    adverse = 0.0
    n = 1
    k = 1.3
    alpha = 0.5
    l0 = 0.01
    equity0 = 30000.0
    pip_value = 10.0 / 10000.0
    R = 150.0

    base_vals, improved_vals = [], []
    dd_series, ex_series, mu_series, depth_series, dist_series, loss_series = [], [], [], [], [], []

    for t in range(steps):
        r = m.market_step(mode, t + 1, steps)
        new_price = max(1e-8, price * (2.718281828 ** r))
        dpips = (new_price - price) * 10000.0
        adverse = max(0.0, adverse - dpips)
        price = new_price

        target_n = min(70, 1 + int(adverse // max(1.0, R)))
        if target_n > n:
            n = target_n

        # get control telemetry from existing simulator in lightweight online proxy
        block_proxy = max(0.0, min(1.0, (n / 60.0) * 0.7 + (adverse / 4500.0) * 0.3))
        comp_proxy = max(0.0, n - target_n + 1)

        margin = m.margin_req(l0, k, n, alpha, 100000.0, 100.0)
        exposure = m.lots_sum(l0, k, n, alpha)
        floating = exposure * adverse * pip_value
        equity = equity0 - floating
        dd = max(0.0, (equity0 - equity) / max(1.0, equity0))
        margin_usage = margin / max(1.0, equity0)

        dd_series.append(dd)
        ex_series.append(exposure)
        mu_series.append(margin_usage)
        depth_series.append(float(n))
        dist_series.append(adverse)
        loss_series.append(floating)

        dyn = {
            "drawdown": max(0.15, _percentile(dd_series, 0.95)),
            "exposure": max(1.0, _percentile(ex_series, 0.95)),
            "margin_usage": max(0.2, _percentile(mu_series, 0.95)),
            "depth": max(5.0, _percentile(depth_series, 0.95)),
            "distance_to_be": max(150.0, _percentile(dist_series, 0.95)),
            "unrealized_loss": max(1000.0, _percentile(loss_series, 0.95)),
        }

        s = LyapunovState(
            drawdown=dd,
            exposure=exposure,
            margin_usage=margin_usage,
            depth=float(n),
            distance_to_be=adverse,
            unrealized_loss=floating,
            control_intensity=block_proxy,
            latency_ticks=0.0,
            compressions_triggered=comp_proxy,
        )
        base_vals.append(lyapunov_value_baseline(s))
        improved_vals.append(lyapunov_value_improved(s, dynamic_ranges=dyn))
    return base_vals, improved_vals


def summarize(mode: str, seed: int):
    base_vals, vals = run_path(mode, seed=seed)
    base_deltas = [base_vals[i + 1] - base_vals[i] for i in range(len(base_vals) - 1)]
    deltas = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
    return {
        "mode": mode,
        "base_E_dV": mean(base_deltas),
        "E_dV": mean(deltas),
        "worst_dV": max(deltas),
        "min_dV": min(deltas),
        "V_start": vals[0],
        "V_end": vals[-1],
        "series": vals,
    }


def sparkline(series):
    chars = "▁▂▃▄▅▆▇█"
    mn, mx = min(series), max(series)
    if mx - mn < 1e-12:
        return chars[0] * 80
    out = []
    step = max(1, len(series) // 80)
    for i in range(0, len(series), step):
        v = series[i]
        idx = int((v - mn) / (mx - mn) * (len(chars) - 1))
        out.append(chars[idx])
    return "".join(out[:80])


def _status(edv: float) -> str:
    if edv < -1e-4:
        return "stable"
    if edv <= 2e-4:
        return "near-stable"
    return "unstable"


def generate_report():
    modes = [
        ("random", 101),
        ("trend", 102),
        ("adv_monotonic", 104),
        ("adv_jump_cluster", 105),
        ("adv_liquidity_gap", 106),
        ("adv_liquidity_freeze", 107),
    ]
    rows = [summarize(m, s) for m, s in modes]

    path = ALE_ROOT / "ALE_LYAPUNOV_PROOF.md"
    lines = [
        "# ALE_LYAPUNOV_PROOF",
        "",
        "## Baseline vs Improved V(state)",
        "Baseline: V = Σ ai*xi (fixed normalization).",
        "Improved: dynamic quantile normalization + log-compression + control/latency/compression terms + dd-margin coupling.",
        "",
        "### Baseline coefficients",
        f"- {BASE_COEFFS}",
        "### Improved coefficients",
        f"- {IMPROVED_COEFFS}",
        "",
        "## ΔV analysis by mode",
        "| mode | baseline E[ΔV] | improved E[ΔV] | worst ΔV | V_start | V_end | status |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['mode']} | {r['base_E_dV']:.6f} | {r['E_dV']:.6f} | {r['worst_dV']:.6f} | {r['V_start']:.4f} | {r['V_end']:.4f} | {_status(r['E_dV'])} |"
        )

    lines += ["", "## V(t) text-graphs (improved)"]
    for r in rows:
        lines.append(f"### {r['mode']}")
        lines.append(sparkline(r["series"]))
        lines.append("")

    unstable = [r for r in rows if _status(r["E_dV"]) == "unstable"]
    improved_count = sum(1 for r in rows if r["E_dV"] < r["base_E_dV"])
    lines += [
        "## Lyapunov result",
        f"- Modes with lower E[ΔV] vs baseline: {improved_count}/{len(rows)}",
        f"- Remaining unstable modes: {len(unstable)}/{len(rows)}",
        "- Conclusion: instability is reduced but not fully eliminated in adversarial tails." if unstable else "- Conclusion: no unstable modes in sampled grid.",
    ]

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    generate_report()
