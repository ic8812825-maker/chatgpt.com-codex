import json
import itertools
from test_adaptive_ev_system import Scenario, Params, simulate_scenario

scenarios = [
    Scenario(name="FLAT_LOW_VOL", mu=0.00, sigma=0.25, spread=0.18, atr=0.55),
    Scenario(name="TREND_UP_MODERATE", mu=0.06, sigma=0.35, spread=0.20, atr=0.70),
    Scenario(name="TREND_DOWN_MODERATE", mu=-0.06, sigma=0.35, spread=0.20, atr=0.70),
    Scenario(name="VOLATILE_MEAN_ZERO", mu=0.00, sigma=0.85, spread=0.25, atr=1.00),
    Scenario(name="SHOCK_REGIME", mu=0.01, sigma=0.65, spread=0.28, atr=1.10, shock_prob=0.05, shock_scale=1.8),
]

cycles = 20
best = None
for alpha, step, gamma, lsmin in itertools.product([0.30,0.35,0.40], [0.28,0.32,0.36], [0.08,0.10,0.12], [0.25,0.30,0.35]):
    cfg = Params(alpha=alpha, delta_step=step, gamma=gamma, ls_min=lsmin, d_max=2.0)
    summary = []
    all_positive = True
    for i, scn in enumerate(scenarios):
        res = [simulate_scenario(scn, cfg, steps=700, seed=1000 + i*100 + k) for k in range(cycles)]
        pass_rate = sum(1 for r in res if r['verdict']=='PASS') / cycles
        avg_equity = sum(r['equity'] for r in res) / cycles
        ok = pass_rate >= 0.60 and avg_equity > 0
        all_positive = all_positive and ok
        summary.append({"scenario": scn.name, "pass_rate": round(pass_rate,2), "avg_equity": round(avg_equity,6), "ok": ok})
    score = sum(x['pass_rate'] for x in summary)
    cand = {"params": {"alpha":alpha,"delta_step":step,"gamma":gamma,"ls_min":lsmin}, "all_positive": all_positive, "score":score, "summary":summary}
    if best is None or (cand['all_positive'] and not best['all_positive']) or (cand['all_positive']==best['all_positive'] and cand['score']>best['score']):
        best = cand
    if all_positive:
        break

print(json.dumps({"cycles":cycles, **best}, ensure_ascii=False, indent=2))
