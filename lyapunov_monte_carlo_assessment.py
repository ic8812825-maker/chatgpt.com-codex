from __future__ import annotations
import json, math, random
from dataclasses import replace
from statistics import mean
from test_adaptive_ev_system import Params, Scenario, simulate_scenario

SCENARIOS = [
    Scenario(name="FLAT_LOW_VOL", mu=0.00, sigma=0.25, spread=0.18, atr=0.55),
    Scenario(name="TREND_UP_MODERATE", mu=0.06, sigma=0.35, spread=0.20, atr=0.70),
    Scenario(name="TREND_DOWN_MODERATE", mu=-0.06, sigma=0.35, spread=0.20, atr=0.70),
    Scenario(name="VOLATILE_MEAN_ZERO", mu=0.00, sigma=0.85, spread=0.25, atr=1.00),
    Scenario(name="SHOCK_REGIME", mu=0.01, sigma=0.65, spread=0.28, atr=1.10, shock_prob=0.05, shock_scale=1.8),
]


def monte_carlo_assessment(trials: int = 200, steps: int = 700) -> dict:
    rng = random.Random(20260501)
    summary = {s.name: {"pass": 0, "equity": []} for s in SCENARIOS}

    for t in range(trials):
        p = Params(
            alpha=rng.uniform(0.25, 0.45),
            delta_step=rng.uniform(0.24, 0.40),
            gamma=rng.uniform(0.07, 0.16),
            ls_min=rng.uniform(0.20, 0.35),
            d_max=2.0,
        )
        for i, scn in enumerate(SCENARIOS):
            r = simulate_scenario(scn, p, steps=steps, seed=10_000 + t * 10 + i)
            summary[scn.name]["pass"] += (r["verdict"] == "PASS")
            summary[scn.name]["equity"].append(r["equity"])

    return {
        k: {
            "pass_rate": round(v["pass"] / trials, 4),
            "avg_equity": round(mean(v["equity"]), 6),
            "p05_equity": round(sorted(v["equity"])[max(0, int(0.05 * len(v["equity"])) - 1)], 6),
        }
        for k, v in summary.items()
    }


def lyapunov_proxy(trials: int = 120, steps: int = 700) -> dict:
    """Proxy: average log sensitivity of risk functional under tiny perturbation.

    Risk functional R = max_drawdown + 0.5*survival_violations + max(0, -equity).
    Lambda_proxy = E[log((R_pert+eps)/(R_base+eps))]. Negative => contraction-like behavior.
    """
    rng = random.Random(20260502)
    eps = 1e-9
    per_scn = {s.name: [] for s in SCENARIOS}

    for t in range(trials):
        p = Params(alpha=0.3, delta_step=0.28, gamma=0.12, ls_min=0.25, d_max=2.0)
        p_pert = replace(
            p,
            pb=p.pb + rng.uniform(-0.03, 0.03),
            ps=p.ps + rng.uniform(-0.03, 0.03),
            alpha=min(0.5, max(0.2, p.alpha + rng.uniform(-0.02, 0.02))),
        )
        for i, scn in enumerate(SCENARIOS):
            rb = simulate_scenario(scn, p, steps=steps, seed=20_000 + t * 10 + i)
            rp = simulate_scenario(scn, p_pert, steps=steps, seed=20_000 + t * 10 + i)

            Rb = rb["max_drawdown"] + 0.5 * rb["survival_violations"] + max(0.0, -rb["equity"])
            Rp = rp["max_drawdown"] + 0.5 * rp["survival_violations"] + max(0.0, -rp["equity"])
            per_scn[scn.name].append(math.log((Rp + eps) / (Rb + eps)))

    return {k: round(mean(v), 6) for k, v in per_scn.items()}


def main():
    out = {
        "monte_carlo": monte_carlo_assessment(),
        "lyapunov_proxy": lyapunov_proxy(),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
