from __future__ import annotations
import random
from statistics import mean
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent))
    from common import load_runner_module, ALE_ROOT
    from lyapunov_builder import LyapunovState, lyapunov_value, COEFFS
else:
    from .common import load_runner_module, ALE_ROOT
    from .lyapunov_builder import LyapunovState, lyapunov_value, COEFFS


def run_path(mode: str, steps: int = 1200, seed: int = 1):
    m = load_runner_module()
    random.seed(seed)

    price = 1.0
    adverse = 0.0
    n = 1
    k = 1.3
    alpha = 1.0
    l0 = 0.01
    equity0 = 30000.0
    pip_value = 10.0 / 10000.0
    R = 150.0

    vals = []
    for t in range(steps):
        r = m.market_step(mode, t + 1, steps)
        new_price = max(1e-8, price * (2.718281828 ** r))
        dpips = (new_price - price) * 10000.0
        adverse = max(0.0, adverse - dpips)
        price = new_price

        target_n = min(70, 1 + int(adverse // max(1.0, R)))
        if target_n > n:
            n = target_n

        margin = m.margin_req(l0, k, n, alpha, 100000.0, 100.0)
        exposure = m.lots_sum(l0, k, n, alpha)
        floating = exposure * adverse * pip_value
        equity = equity0 - floating
        dd = max(0.0, (equity0 - equity) / max(1.0, equity0))
        margin_usage = margin / max(1.0, equity0)

        s = LyapunovState(
            drawdown=dd,
            exposure=exposure,
            margin_usage=margin_usage,
            depth=float(n),
            distance_to_be=adverse,
            unrealized_loss=floating,
        )
        vals.append(lyapunov_value(s))
    return vals


def summarize(mode: str, seed: int):
    vals = run_path(mode, seed=seed)
    deltas = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
    return {
        "mode": mode,
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


def generate_report():
    modes = [
        ("random", 101),
        ("trend", 102),
        ("shock", 103),
        ("adv_monotonic", 104),
        ("adv_jump_cluster", 105),
        ("adv_liquidity_gap", 106),
        ("adv_liquidity_freeze", 107),
    ]
    rows = [summarize(m, s) for m, s in modes]

    verdict = []
    for r in rows:
        if r["E_dV"] < 0:
            v = "stable"
        elif abs(r["E_dV"]) < 1e-4:
            v = "borderline"
        else:
            v = "unstable"
        verdict.append((r["mode"], v))

    path = ALE_ROOT / "ALE_LYAPUNOV_PROOF.md"
    lines = [
        "# ALE_LYAPUNOV_PROOF",
        "",
        "## V(state) formula",
        "V = a1*drawdown + a2*|exposure| + a3*margin_usage + a4*depth + a5*distance_to_be + a6*unrealized_loss (normalized)",
        "",
        "### Coefficients",
        f"- {COEFFS}",
        "",
        "## ΔV analysis by mode",
        "| mode | E[ΔV] | worst ΔV | V_start | V_end | status |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        status = next(v for m, v in verdict if m == r["mode"])
        lines.append(f"| {r['mode']} | {r['E_dV']:.6f} | {r['worst_dV']:.6f} | {r['V_start']:.4f} | {r['V_end']:.4f} | {status} |")

    lines += ["", "## V(t) text-graphs"]
    for r in rows:
        lines.append(f"### {r['mode']}")
        lines.append(sparkline(r["series"]))
        lines.append("")

    has_positive = any(r["E_dV"] > 0 for r in rows)
    lines += [
        "## Lyapunov existence/result",
        "- [x] Lyapunov exists" if rows else "- [ ] Lyapunov exists",
        "- [ ] Lyapunov does NOT exist" if rows else "- [x] Lyapunov does NOT exist",
        f"- Stability conclusion: {'UNSTABLE modes detected' if has_positive else 'No positive E[ΔV] detected in sampled modes'}",
    ]

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    generate_report()
