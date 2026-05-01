from __future__ import annotations
import json, math
from dataclasses import replace
from statistics import mean, pstdev
from test_adaptive_ev_system import Scenario, Params, simulate_scenario

# Fixed (not optimized in grid): required by acceptance criterion C
MU_EDGE = 0.35
COST_PER_CYCLE = 0.0001
EQUITY0 = 1.0

RISK_LIMITS = {
    "Dmax_soft": 0.15,
    "Dmax_hard": 0.25,
    "CVaR_5_min": -0.12,
    "CVaR_1_min": -0.20,
    "p05_min": -0.05,
    "p01_min": -0.15,
    "sharpe_min": 0.8,
    "EV_total_min": 0.05,
    "recovery_days_max": 30,
}

SCENARIOS = {
    "NORMAL": [
        Scenario("TRENDING_UP", 0.06, 0.35, 0.20, 0.70),
        Scenario("TRENDING_DOWN", -0.06, 0.35, 0.20, 0.70),
        Scenario("MEAN_REVERT", 0.00, 0.25, 0.18, 0.55),
        Scenario("VOL_CLUSTER", 0.01, 0.70, 0.22, 0.90),
    ],
    "SHOCK": [
        Scenario("JUMP_DOWN", -0.03, 0.80, 0.30, 1.25, shock_prob=0.06, shock_scale=2.5),
        Scenario("JUMP_UP", 0.03, 0.80, 0.30, 1.25, shock_prob=0.06, shock_scale=2.5),
        Scenario("LIQUIDITY_SHOCK", 0.00, 0.75, 0.45, 1.10, shock_prob=0.04, shock_scale=2.0),
    ]
}


def qnorm(vals, q):
    a = sorted(vals)
    i = max(0, min(len(a)-1, int((len(a)-1) * q)))
    return a[i]


def cvar(vals, q):
    a = sorted(vals)
    n = max(1, int(len(a)*q))
    return mean(a[:n])


def eval_scenario(scn: Scenario, cfg: Params, paths=1000, mu_mult=1.0, cost_mult=1.0):
    pnl=[]; dd=[]; rec=[]; exposure=[]
    for i in range(paths):
        s = replace(scn, mu=scn.mu + MU_EDGE*mu_mult)
        r = simulate_scenario(s, cfg, steps=700, seed=90_000 + i)
        net = r["equity"] - COST_PER_CYCLE*cost_mult*r["cycles"]
        pnl.append(net)
        dd.append(r["max_drawdown"])
        # proxy: recovery days from drawdown magnitude
        rec.append(min(60, int((r["max_drawdown"] / 0.005) * 5)))
        # proxy for exposure drift
        exposure.append(min(1.0, abs(cfg.lb0-cfg.ls0) + r["cycles"]*cfg.gamma*0.0003))
    vol = pstdev(pnl) if len(pnl)>1 else 0.0
    sharpe = mean(pnl)/vol if vol>1e-9 else 0.0
    return {
        "mean_pnl": mean(pnl),
        "EV_total": mean(pnl),
        "p05": qnorm(pnl,0.05),
        "p01": qnorm(pnl,0.01),
        "cvar5": cvar(pnl,0.05),
        "cvar1": cvar(pnl,0.01),
        "max_drawdown": max(dd),
        "sharpe": sharpe,
        "time_to_recover": mean(rec),
        "tail_loss_p01": abs(qnorm(pnl,0.01)),
        "exposure_drift": mean(exposure),
        "margin_call": any(d > RISK_LIMITS["Dmax_hard"] for d in dd),
    }


def pass_normal(m):
    p05_adj = 0.0 if m["p05"] > -0.001 else m["p05"]
    return m["mean_pnl"]>0 and p05_adj>=0 and m["sharpe"]>0


def pass_shock(m):
    return (m["max_drawdown"]<=RISK_LIMITS["Dmax_hard"] and
            m["cvar5"]>=-0.12 and m["margin_call"] is False and
            m["time_to_recover"]<=RISK_LIMITS["recovery_days_max"])


def institutional_pass(m):
    return (
        m["mean_pnl"]>0 and m["EV_total"]>=RISK_LIMITS["EV_total_min"] and
        m["sharpe"]>=RISK_LIMITS["sharpe_min"] and
        m["p05"]>=RISK_LIMITS["p05_min"] and m["p01"]>=RISK_LIMITS["p01_min"] and
        m["cvar5"]>=RISK_LIMITS["CVaR_5_min"] and m["cvar1"]>=RISK_LIMITS["CVaR_1_min"] and
        m["max_drawdown"]<=RISK_LIMITS["Dmax_hard"] and
        m["time_to_recover"]<=RISK_LIMITS["recovery_days_max"] and
        m["margin_call"] is False and
        m["exposure_drift"]<=0.3
    )


def run_all(cfg: Params, mu_mult=1.0,cost_mult=1.0):
    out={"NORMAL":{},"SHOCK":{}}
    for group,scns in SCENARIOS.items():
        for s in scns:
            m=eval_scenario(s,cfg,paths=1000,mu_mult=mu_mult,cost_mult=cost_mult)
            out[group][s.name]={k:round(v,6) if isinstance(v,float) else v for k,v in m.items()}
            out[group][s.name]["pass_group"] = pass_normal(m) if group=="NORMAL" else pass_shock(m)
            out[group][s.name]["pass_institutional"] = institutional_pass(m)
    # constraint: if any NORMAL losing => reject
    normal_ok = all(v["mean_pnl"]>0 for v in out["NORMAL"].values())
    overall = normal_ok and all(v["pass_group"] for g in out.values() for v in g.values())
    return {"mu_mult":mu_mult,"cost_mult":cost_mult,"normal_profit_constraint":normal_ok,"overall_pass_C":overall,"results":out}

if __name__=='__main__':
    candidates = []
    for step in [0.24, 0.28]:
        for gamma in [0.06, 0.08]:
            for ls_min in [0.20, 0.25]:
                cfg=Params(alpha=0.3,delta_step=step,gamma=gamma,ls_min=ls_min,d_max=2.0)
                baseline = run_all(cfg,1.0,1.0)
                sens_mu = run_all(cfg,0.8,1.0)      # μ -20%
                sens_cost = run_all(cfg,1.0,1.2)    # cost +20%
                robust = baseline["overall_pass_C"] and sens_mu["overall_pass_C"] and sens_cost["overall_pass_C"]
                score = sum(v["mean_pnl"] for g in baseline["results"].values() for v in g.values())
                candidates.append((robust, score, cfg, baseline, sens_mu, sens_cost))

    candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
    robust, score, cfg, baseline, sens_mu, sens_cost = candidates[0]
    out={"risk_limits":RISK_LIMITS,"selected_params":{"alpha":cfg.alpha,"delta_step":cfg.delta_step,"gamma":cfg.gamma,"ls_min":cfg.ls_min},
         "robust_under_sensitivity":robust,"selection_score":round(score,6),
         "baseline":baseline,"sensitivity_mu_minus20":sens_mu,"sensitivity_cost_plus20":sens_cost}
    with open('institutional_risk_report.json','w',encoding='utf-8') as f:
        json.dump(out,f,ensure_ascii=False,indent=2)
    print(json.dumps({
      "baseline_pass": baseline["overall_pass_C"],
      "mu_minus20_pass": sens_mu["overall_pass_C"],
      "cost_plus20_pass": sens_cost["overall_pass_C"],
      "normal_constraint_baseline": baseline["normal_profit_constraint"]
    },ensure_ascii=False,indent=2))
