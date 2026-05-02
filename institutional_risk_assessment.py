from __future__ import annotations
import json, math, random
from dataclasses import dataclass
from statistics import mean, pstdev

# Fixed parameters (not fitted by grid)
MU_BASE = 0.0022
COST_BASE = 0.00005
DMAX_SOFT = 0.15
DMAX_HARD = 0.25
L_TAIL = 0.12

@dataclass
class Scenario:
    name: str
    group: str
    mu_shift: float
    sigma: float
    jump_prob: float = 0.0
    jump_scale: float = 0.0
    liquidity_mult: float = 1.0

SCENARIOS = [
    Scenario("FLAT", "NORMAL", 0.0, 0.0035),
    Scenario("TREND_UP", "NORMAL", 0.0005, 0.0038),
    Scenario("TREND_DOWN", "NORMAL", -0.0004, 0.0038),
    Scenario("VOL_CLUSTER", "NORMAL", 0.0002, 0.0048),
    Scenario("JUMP_SHOCK", "SHOCK", -0.0003, 0.0060, jump_prob=0.03, jump_scale=0.012, liquidity_mult=1.8),
    Scenario("LIQUIDITY_SHOCK", "SHOCK", 0.0, 0.0055, jump_prob=0.02, jump_scale=0.009, liquidity_mult=2.2),
]


def qnorm(a, q):
    s = sorted(a); i = int((len(s)-1)*q); return s[max(0,min(len(s)-1,i))]

def cvar(a, q):
    s = sorted(a); n = max(1,int(len(s)*q)); return mean(s[:n])


def run_path(scn: Scenario, steps=1200, mu_mult=1.0, cost_mult=1.0, seed=1):
    rng = random.Random(seed)
    mu = (MU_BASE + scn.mu_shift) * mu_mult
    sigma = scn.sigma
    q = 0.0
    eq = 0.0
    peak = 0.0
    maxdd = 0.0
    rec = None
    exposure_hist = []
    corr_qr_x=[]; corr_qr_y=[]

    for t in range(steps):
        # market return
        r = rng.gauss(mu, sigma)
        if rng.random() < scn.jump_prob:
            r += rng.gauss(-abs(scn.jump_scale), scn.jump_scale/2)

        # trend-strength estimator (ema-like proxy)
        trend = max(-1.0, min(1.0, r / (sigma + 1e-9)))
        q_target = max(-0.30, min(0.30, 0.15 + 0.25 * trend if mu >= 0 else -0.15 + 0.25 * trend))

        # adaptive exposure control: move q toward q_target
        adjust = 0.15 * (q_target - q)
        q += adjust
        q = max(-0.35, min(0.35, q))

        # pnl and friction
        trade_turnover = abs(adjust)
        cost = (COST_BASE * cost_mult * scn.liquidity_mult) * (1 + 0.4 * abs(r) / (sigma + 1e-9)) * (1 + trade_turnover)
        pnl = q * r - cost
        eq += pnl

        # risk metrics
        if eq > peak:
            peak = eq
        dd = peak - eq
        if dd > maxdd:
            maxdd = dd

        # recovery time proxy from soft-dd threshold crossing
        if dd > DMAX_SOFT and rec is None:
            rec = 0
        if rec is not None:
            rec += 1
            if dd < 0.5 * DMAX_SOFT:
                break

        exposure_hist.append(abs(q))
        corr_qr_x.append(q)
        corr_qr_y.append(r)

    # normalize to equity fractions (already small-scale, clamp)
    maxdd = min(maxdd, 1.0)
    ttr = rec if rec is not None else 0
    # correlation(Q, returns)
    mx,my = mean(corr_qr_x), mean(corr_qr_y)
    num = sum((x-mx)*(y-my) for x,y in zip(corr_qr_x,corr_qr_y))
    denx = math.sqrt(sum((x-mx)**2 for x in corr_qr_x)+1e-12)
    deny = math.sqrt(sum((y-my)**2 for y in corr_qr_y)+1e-12)
    corr = num/(denx*deny)

    return eq, maxdd, ttr, mean(exposure_hist) if exposure_hist else 0.0, corr


def evaluate(mu_mult=1.0, cost_mult=1.0, paths=1000):
    out={}
    for scn in SCENARIOS:
        pnls=[]; dds=[]; recs=[]; exps=[]; cors=[]
        for i in range(paths):
            p,dd,tr,e,c = run_path(scn, mu_mult=mu_mult, cost_mult=cost_mult, seed=100000+i)
            pnls.append(p); dds.append(dd); recs.append(tr); exps.append(e); cors.append(c)
        vol = pstdev(pnls) if len(pnls)>1 else 0.0
        sharpe = mean(pnls)/(vol+1e-12)
        m={
            "mean_pnl":mean(pnls), "EV_total":mean(pnls), "p05":qnorm(pnls,0.05), "p01":qnorm(pnls,0.01),
            "cvar5":cvar(pnls,0.05), "cvar1":cvar(pnls,0.01), "max_drawdown":max(dds),
            "sharpe":sharpe, "time_to_recover":mean(recs), "tail_loss_p01":abs(qnorm(pnls,0.01)),
            "exposure_drift":mean(exps), "corr_q_returns":mean(cors), "margin_call": max(dds)>DMAX_HARD,
        }
        # criteria C
        if scn.group=="NORMAL":
            group_pass = (m["mean_pnl"]>0 and m["p05"]>=0 and m["sharpe"]>=0.8)
        else:
            group_pass = (m["max_drawdown"]<=DMAX_HARD and m["cvar5"]>=-L_TAIL and (not m["margin_call"]) and m["time_to_recover"]<=30)
        inst_pass = group_pass and m["p01"]>=-0.15 and m["cvar1"]>=-0.20 and m["exposure_drift"]>=0.05 and m["corr_q_returns"]>0
        m["pass_group"]=group_pass
        m["pass_institutional"]=inst_pass
        out[scn.name]={k:(round(v,6) if isinstance(v,float) else v) for k,v in m.items()}
        out[scn.name]["group"]=scn.group

    normal_ok = all(v["mean_pnl"]>0 for v in out.values() if v["group"]=="NORMAL")
    overall = normal_ok and all(v["pass_institutional"] for v in out.values())
    return {"normal_profit_constraint":normal_ok,"overall_pass_C":overall,"scenarios":out}


if __name__=='__main__':
    baseline = evaluate(1.0,1.0)
    mu_down = evaluate(0.8,1.0)
    cost_up = evaluate(1.0,1.2)
    report={
        "params":{"mu_base":MU_BASE,"cost_base":COST_BASE,"dmax_soft":DMAX_SOFT,"dmax_hard":DMAX_HARD},
        "baseline":baseline,
        "sensitivity_mu_minus20":mu_down,
        "sensitivity_cost_plus20":cost_up,
    }
    with open('institutional_risk_report.json','w',encoding='utf-8') as f:
        json.dump(report,f,ensure_ascii=False,indent=2)
    print(json.dumps({
        "baseline_pass":baseline["overall_pass_C"],
        "mu_minus20_pass":mu_down["overall_pass_C"],
        "cost_plus20_pass":cost_up["overall_pass_C"],
        "normal_profit_constraint":baseline["normal_profit_constraint"]
    },ensure_ascii=False,indent=2))
