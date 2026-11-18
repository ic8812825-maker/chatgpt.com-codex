"""Shared frozen search, independent price laws, and paired economics."""
from collections import defaultdict
from csv import DictWriter
from dataclasses import asdict,dataclass,replace
import importlib
from itertools import combinations
import json
from math import log,sqrt
from pathlib import Path
from random import Random
from statistics import mean
import sys

from baseline_audit import source
from a3rc import Params,choose_a3
from ledger2 import Limits
from meta_rc import D,choose_b,choose_m,weights
from study2 import summarize,tail,rank

model=importlib.import_module("04_EXECUTION_SIMULATOR")
a3=importlib.import_module("05_A3_ER_POLICY")
meta=importlib.import_module("06_META_ER_POLICY")
ROUTES={"A3-RC":choose_a3,"A3-ER":a3.choose_er,"M-RC":choose_m,"M-ER":meta.choose_meta,
        "B4-RC":choose_b,"K-EXECUTABLE":None,"K-IDEAL":None}
FAMILIES=tuple(ROUTES)[:-2]
HORIZONS=(4,6,8,12,16,24)
LOSSES=(58,100,150,180,250,300,500)
COSTS=(20,30,40,50,75,100)
LAWS=("markov","iid","trend","reversion","reversal","regime")
GRID=(
    Params(),
    Params(core=10,net=12,trigger=0,switches=4,harvest=25,attempts=1,depth=2),
    Params(core=25,net=25,trigger=75,switches=4,harvest=50,attempts=2,depth=4),
    Params(core=50,net=30,trigger=140,switches=6,harvest=25,attempts=2,depth=4),
    Params(core=80,net=40,trigger=225,switches=6,harvest=75,attempts=2,depth=6),
    Params(core=1,net=50,trigger=300,switches=8,harvest=0,attempts=3,depth=8,reserve=5),
)


def samples(seed,n,h,profile,law):
    r=Random(seed)
    for i in range(n):
        orientation=r.choice((-1,1))
        draws=tuple(r.randrange(21) for _ in range(h+1))
        direction=r.choice((-1,1))
        prev=mid=0
        moves=[]
        for t in range(h):
            if law=="markov":
                d=r.choices(D,weights(prev))[0]
            elif law=="iid":
                d=r.choice(D)
            elif law=="trend":
                d=direction*r.choices((0,150,300,-150),(.15,.4,.4,.05))[0]
            elif law=="reversion":
                correction=-150*((mid>0)-(mid<0))
                d=correction if r.random()<.6 else r.choice(D)
            elif law=="reversal":
                d=direction*(1 if t%4<2 else -1)*r.choice((150,300,300))
            else:
                sign=direction if t<h//2 else -direction
                d=r.choice(D) if t%3==0 else sign*r.choice((0,150,300))
            prev=d
            mid+=d
            moves.append(d)
        yield model.Case(orientation,tuple(moves),profile,draws,law)


def evaluate(route,p,limits,scenarios,profile):
    c=model.PROFILES[profile] if route.endswith("-ER") else None
    return [model.replay(route,s,limits,p,ROUTES[route],contract=c) for s in scenarios]


def write(name,rows):
    with Path(name+".csv").open("w",newline="") as f:
        writer=DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows({k:round(v,9) if isinstance(v,float) else v for k,v in row.items()} for row in rows)


def key(data):
    return (data["risk_violations"]==0,*rank(data))


def select():
    selected={}
    tuning=[]
    for profile in ("E0","E1","E2"):
        for h in HORIZONS:
            ls=Limits(horizon=h)
            tr=list(samples(31001,48,h,profile,"markov"))
            va=list(samples(31002,96,h,profile,"markov"))
            for route in FAMILIES:
                scores=[]
                for i,p in enumerate(GRID):
                    r=summarize(evaluate(route,p,ls,tr,profile))
                    scores.append((key(r),i))
                order=sorted(scores,reverse=True)
                best=None
                for training,i in order[:2]:
                    p=GRID[i]
                    v=summarize(evaluate(route,p,ls,va,profile))
                    tuning.append(dict(profile=profile,horizon=h,policy=route,grid=i,
                                       train_feasible=training[0],validation_violations=v["risk_violations"],
                                       validation_recovery=v["recovery_rate"],validation_cvar99=v["cvar99"]))
                    if best is None or key(v)>best[0]:
                        best=(key(v),i)
                selected[profile,h,route]=best[1]
            print("frozen",profile,h,flush=True)
    write("08_TUNING_LOG",tuning)
    Path("08_FROZEN_GRID.json").write_text(json.dumps({
        "parameters":[asdict(p) for p in GRID],
        "selected":[dict(profile=e,horizon=h,policy=name,grid=i)
                    for (e,h,name),i in selected.items()]},indent=2)+"\n")
    return selected


def paired(panel,left,right,a,b,inference=True):
    w=sum(x.success and not y.success for x,y in zip(a,b))
    l=sum(y.success and not x.success for x,y in zip(a,b))
    t=sum(x.success and y.success for x,y in zip(a,b))
    n=len(a)
    d=(w-l)/n
    half=sqrt(2*log(40)/n)
    # Bonferroni across 21 pairs within one panel; no statement across all panels.
    family=sqrt(2*log(40*21)/n)
    return dict(panel=panel,left=left,right=right,n=n,only_left=w,only_right=l,both=t,
                neither=n-w-l-t,difference=d,lo95=max(-1,d-half) if inference else "",
                hi95=min(1,d+half) if inference else "",
                family_lo95=max(-1,d-family) if inference else "",
                family_hi95=min(1,d+family) if inference else "")


def economics(panel,route,items,reference):
    aa=[(a,b) for a,b in zip(items,reference) if a.flat and b.flat]
    n=len(items)
    deltas=[a.pnl-b.pnl for a,b in aa]
    marks=[a.pnl-b.pnl for a,b in zip(items,reference)]
    return dict(panel=panel,policy=route,n=n,paired_flat=len(aa),paired_flat_rate=len(aa)/n,
                expected_delta=mean(deltas) if deltas else "",
                p_delta_positive=mean(d>0 for d in deltas) if deltas else "",
                p_delta_negative=mean(d<0 for d in deltas) if deltas else "",
                additional_cvar95=tail([-d for d in deltas],.95) if deltas else "",
                additional_cvar99=tail([-d for d in deltas],.99) if deltas else "",
                max_additional_loss=max(0,-min(deltas)) if deltas else "",
                mean_extra_cost=mean(a.cost-b.cost for a,b in zip(items,reference)),
                mean_extra_time=mean(a.time-b.time for a,b in aa) if aa else "",
                residual_rate=mean(not a.flat for a in items),
                k_residual_rate=mean(not b.flat for b in reference),
                worst_estimated_delta_including_open=min(marks))


def main():
    if "--frozen" in sys.argv:
        payload=json.loads(Path("08_FROZEN_GRID.json").read_text())
        selected={(r["profile"],r["horizon"],r["policy"]):r["grid"] for r in payload["selected"]}
    else:
        selected=select()
    rows,pairs,increment=[],[],[]
    panels=[
        (e,h,"markov",180,50,1800 if h==12 else 240)
        for e in ("E0","E1","E2") for h in HORIZONS
    ]
    panels += [("E1",12,law,180,50,512) for law in LAWS if law!="markov"]
    panels += [(e,12,"markov",180,50,256) for e in ("E3","E4","E5","E6")]
    panels += [("E1",12,"risk_sensitivity",b,50,240) for b in LOSSES if b!=180]
    panels += [("E1",12,"cost_sensitivity",180,c,240) for c in COSTS if c!=50]
    for index,(profile,h,law,loss,cost,n) in enumerate(panels):
        panel=f"{profile}/{h}/{law}/{loss}/{cost}"
        settings=Limits(horizon=h,loss=loss,cost=cost)
        case_law="markov" if law.endswith("sensitivity") else law
        # Fix common random input across sensitivities. Ordinary test panels use disjoint seeds.
        seed=(31299 if law.endswith("sensitivity") else 31400+index)
        scenarios=list(samples(seed,n,h,profile,case_law))
        base=evaluate("K-EXECUTABLE",GRID[0],settings,scenarios,profile)
        outcome={}
        for route in ROUTES:
            ix=selected.get((profile,h,route),selected.get(("E0",h,route),0))
            v=base if route=="K-EXECUTABLE" else evaluate(route,GRID[ix],settings,scenarios,profile)
            outcome[route]=v
            result=summarize(v,ci=profile not in ("E3","E4","E5","E6"))
            rows.append(dict(panel=panel,profile=profile,horizon=h,generator=law,
                             loss_budget=loss,cost_budget=cost,policy=route,grid=ix,seed=seed,**result))
            if route not in ("K-EXECUTABLE","K-IDEAL"):
                increment.append(economics(panel,route,v,base))
        for a,b in combinations(ROUTES,2):
            pairs.append(paired(panel,a,b,outcome[a],outcome[b],profile in ("E0","E1","E2")))
        print("tested",panel,flush=True)
    write("08_ROBUSTNESS_MATRIX",rows)
    write("08_PAIRED_COMPARISON",pairs)
    feasible=[r for r in rows if r["generator"]=="markov" and r["horizon"]==12
              and r["profile"] in ("E0","E1","E2") and r["policy"]!="K-IDEAL"
              and not r["risk_violations"]]
    keep=[]
    axes=("recovery_rate","worst_pnl","cvar99","max_cost_reserve")
    def vector(r):
        return tuple(r[k]*(1 if i<2 else -1) for i,k in enumerate(axes))
    for r in feasible:
        x=vector(r)
        y=[vector(j) for j in feasible if j["profile"]==r["profile"]]
        if not any(a!=x and all(i>=j for i,j in zip(a,x)) for a in y):
            keep.append(r)
    write("08_RECOVERY_RISK_FRONTIER",keep)
    write("10_INCREMENTAL_VALUE_VS_K",increment)


if __name__=="__main__":
    main()
