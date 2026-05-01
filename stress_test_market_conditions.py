from __future__ import annotations
import json
from dataclasses import replace
from itertools import product
from statistics import mean
from test_adaptive_ev_system import Scenario, Params, simulate_scenario

BASE_SCENARIOS = [
    Scenario(name="FLAT_LOW_VOL", mu=0.00, sigma=0.25, spread=0.18, atr=0.55),
    Scenario(name="TREND_UP_MODERATE", mu=0.06, sigma=0.35, spread=0.20, atr=0.70),
    Scenario(name="TREND_DOWN_MODERATE", mu=-0.06, sigma=0.35, spread=0.20, atr=0.70),
    Scenario(name="VOLATILE_MEAN_ZERO", mu=0.00, sigma=0.85, spread=0.25, atr=1.00),
    Scenario(name="SHOCK_REGIME", mu=0.01, sigma=0.65, spread=0.28, atr=1.10, shock_prob=0.05, shock_scale=1.8),
]


def percentile(vals, p):
    arr = sorted(vals)
    idx = max(0, min(len(arr)-1, int((len(arr)-1) * p)))
    return arr[idx]


def scenario_distribution(scn: Scenario, cfg: Params, mu_edge: float, cost_per_cycle: float, runs=150, steps=700):
    vals=[]; dds=[]
    for r in range(runs):
        scn2 = replace(scn, mu=scn.mu + mu_edge)
        out = simulate_scenario(scn2, cfg, steps=steps, seed=50_000 + r)
        net = out["equity"] - cost_per_cycle * out["cycles"]
        vals.append(net)
        dds.append(out["max_drawdown"])
    tail = sorted(vals)[:max(1, int(0.05 * len(vals)))]
    return {
        "mean_pnl": round(mean(vals), 6),
        "p05_pnl": round(percentile(vals, 0.05), 6),
        "p50_pnl": round(percentile(vals, 0.50), 6),
        "cvar5": round(mean(tail), 6),
        "max_drawdown": round(max(dds), 6),
    }


def run_search():
    best = None
    grid = product(
        [0.05, 0.08, 0.10, 0.12],      # mu_edge
        [0.0002, 0.0005, 0.001], # cost_per_cycle
        [0.28, 0.32],            # delta_step
        [0.08, 0.10, 0.12],      # gamma
        [0.25, 0.30],            # ls_min
    )
    for mu_edge, cpc, step, gamma, ls_min in grid:
        cfg = Params(alpha=0.3, delta_step=step, gamma=gamma, ls_min=ls_min, d_max=2.0)
        per = {}
        ok = True
        score = 0.0
        for scn in BASE_SCENARIOS:
            m = scenario_distribution(scn, cfg, mu_edge, cpc)
            per[scn.name] = m
            cond = (m["mean_pnl"] > 0 and m["p05_pnl"] >= 0 and m["cvar5"] >= 0 and m["max_drawdown"] < 0.05)
            ok = ok and cond
            score += m["mean_pnl"] - 0.5 * m["max_drawdown"]
        if ok and (best is None or score > best["score"]):
            best = {
                "mu_edge": mu_edge,
                "cost_per_cycle": cpc,
                "params": {"alpha":0.3, "delta_step":step, "gamma":gamma, "ls_min":ls_min},
                "score": round(score, 6),
                "scenarios": per,
            }
    return best


if __name__ == "__main__":
    res = run_search()
    if res is None:
        print(json.dumps({"status":"NO_FULLY_POSITIVE_CONFIG"}, indent=2))
    else:
        print(json.dumps({"status":"POSITIVE_CONFIG_FOUND", **res}, indent=2))
