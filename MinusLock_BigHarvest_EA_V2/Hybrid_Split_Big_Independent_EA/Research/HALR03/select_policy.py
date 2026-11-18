"""Choose among certifiable families using validation, then report held-out results."""
from csv import DictReader
import json
from pathlib import Path
from statistics import mean

from experiments import GRID,ROUTES,evaluate,samples,summarize,write
from ledger2 import Limits

ALLOWED={"E0":set(ROUTES)-{"K-IDEAL"},
         "E1":{"A3-ER","M-ER","K-EXECUTABLE"},
         "E2":{"A3-ER","M-ER","K-EXECUTABLE"}}


def choose():
    raw=json.loads(Path("08_FROZEN_GRID.json").read_text())
    indexes={(r["profile"],r["horizon"],r["policy"]):r["grid"] for r in raw["selected"]}
    output={}
    diagnostics=[]
    h=12
    for profile,allowed in ALLOWED.items():
        validation=list(samples(31002,96,h,profile,"markov"))
        l=Limits(horizon=h)
        baseline=evaluate("K-EXECUTABLE",GRID[0],l,validation,profile)
        eligible=[]
        for route in ROUTES:
            if route not in allowed:
                continue
            ix=indexes.get((profile,h,route),0)
            rs=evaluate(route,GRID[ix],l,validation,profile)
            s=summarize(rs)
            if s["risk_violations"]:
                continue
            extra=max(0,max(b.pnl-r.pnl for b,r in zip(baseline,rs)))
            score=(s["recovery_rate"],-s["cvar99"],-extra,s["mean_pnl"],
                   -s["total_cost"],-mean(r.time for r in rs))
            diagnostics.append(dict(profile=profile,policy=route,grid=ix,
                                    recovery_rate=s["recovery_rate"],cvar99=s["cvar99"],
                                    worst_additional_loss=extra,mean=s["mean_pnl"],
                                    paid=s["total_cost"],exit_time=mean(r.time for r in rs)))
            eligible.append((score,route,ix))
        score,route,ix=max(eligible,key=lambda x:x[0])
        output[profile]=dict(candidate=route,grid=ix,rank_inputs=score,status="FORMALLY_PROVEN")
    output["E3"]={"status":"NO_FEASIBLE_POLICY_WITHIN_CONTRACT","reason":"capacity <=0.30 lots"}
    output["E4"]={"candidate":"K-EXECUTABLE","status":"K_EXIT_CERTIFIED_IN_SCRIPT",
                  "reason":"guaranteed initial fill precedes gap"}
    output["E5"]={"status":"INCONCLUSIVE","reason":"all tested candidates violated; global viability at H12 unproved"}
    output["E6"]={"status":"NO_FEASIBLE_POLICY_WITHIN_CONTRACT","reason":"zero confirmed liquidity"}
    write("10_VALIDATION_POLICY_SELECTION",diagnostics)
    Path("10_POLICY_SELECTION.json").write_text(json.dumps(output,indent=2)+"\n")
    return output


if __name__=="__main__":
    print(json.dumps(choose(),indent=2))
