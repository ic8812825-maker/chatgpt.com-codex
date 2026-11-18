"""Analyze the locked independent panels; no fitting code is run here."""
from collections import defaultdict
from hashlib import sha256
import json
from math import ceil,sqrt
from pathlib import Path
from random import Random
from statistics import mean,median
import sys

from learning import VARIANTS,tracks,read,publish_csv,rdb
from replay import FILL_MODELS,run


def block_ci(rows,alpha,metric):
    by=defaultdict(list)
    for row in rows:
        value=metric(row)
        if value is not None:
            by[row["month"]].append(value)
    if len(by)<4:
        return ("","")
    blocks=[(sum(seq),len(seq)) for _,seq in sorted(by.items())]
    rng=Random(48211)
    r=[]
    for _ in range(4000):
        sample=rng.choices(blocks,k=len(blocks))
        r.append(sum(x[0] for x in sample)/sum(x[1] for x in sample))
    r.sort()
    q=lambda u:r[min(len(r)-1,max(0,ceil(u*len(r))-1))]
    return q(alpha/2),q(1-alpha/2)


def cvar(values,p=.99):
    if not values:
        return ""
    r=sorted(values,reverse=True)
    n=(1-p)*len(values)
    k=int(n)
    return (sum(r[:k])+(n-k)*r[k])/n


def wilson(k,n):
    if not n:return "",""
    p=k/n
    z=1.95996398454
    c=(p+z*z/(2*n))/(1+z*z/n)
    e=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    return max(0,c-e),min(1,c+e)


def summarize(panel,mode,policy,results):
    n=len(results)
    r=[x["outcome"] for x in results]
    terminal=[o["pnl"] for o in r if o["flat"]]
    candidates=[x["delta"] for x in results if x["delta"] is not None]
    newcost=[o["cost"] for o in r]
    realized_losses=[-p for p in terminal]
    lo,hi=wilson(sum(o["success"] for o in r),n)
    corrected=6 if panel=="S2/30" and mode=="quote_fill" else 1
    lower,upper=block_ci(results,.05/corrected,lambda x:x["delta"])
    recover_low,recover_high=block_ci(results,.05/corrected,lambda x:x["recovery_delta"])
    paired_months={x["month"] for x in results if x["delta"] is not None}
    return dict(panel=panel,mode=mode,policy=policy,n=n,clusters=len({x["month"] for x in results}),
                recoveries=sum(o["success"] for o in r),
                recovery_rate=mean(o["success"] for o in r),wilson_low=lo,wilson_high=hi,
                recovery_delta_low=recover_low,recovery_delta_high=recover_high,
                flat=len(terminal),flat_rate=len(terminal)/n,paired_flat=len(candidates),
                paired_clusters=len(paired_months),paired_mean=mean(candidates) if candidates else "",
                paired_low=lower,paired_high=upper,mean_terminal=mean(terminal) if terminal else "",
                median_terminal=median(terminal) if terminal else "",
                cvar95_realized=cvar(realized_losses,.95),cvar99_realized=cvar(realized_losses,.99),
                cvar99_all_marks=cvar([-o["pnl"] for o in r],.99),worst_mark=min(o["pnl"] for o in r),
                worst_intracycle=min(o["low"] for o in r),max_drawdown=max(o["drawdown"] for o in r),
                worst_realized=min(terminal) if terminal else "",
                max_additional_loss=max(0,-min(candidates)) if candidates else "",
                mean_new_cost=mean(newcost),max_cost_reserve=max(o["cost_with_reserve"] for o in r),
                peak_gross=max(o["gross"] for o in r),peak_net=max(o["net"] for o in r),
                peak_margin_equity=max(o["margin"] for o in r),
                mean_elapsed_ms_to_flat=mean(o["elapsed_ms"] for o in r if o["flat"]) if terminal else "",
                mean_events=mean(o["quote_events"] for o in r),mean_attempts=mean(o["attempts"] for o in r),
                residual_count=sum(o["residual"]>0 for o in r),pending_count=sum(o["pending"]>0 for o in r),
                risk_violations=sum(bool(o["violations"]) for o in r),
                execution_failures=sum(o["failures"] for o in r),
                no_certificate=sum(o["decision"]=="NO_CERTIFIED_ACTION" for o in r),
                incomplete=sum(not x["complete"] for x in results))


def row(e,result,k):
    return dict(month=e["month"],id=e["id"],complete=e["complete"],
                outcome=result,k_outcome=k,
                delta=result["pnl"]-k["pnl"] if result["flat"] and k["flat"] else None,
                recovery_delta=int(result["success"])-int(k["success"]))


def analyze(cases,frozen,modes=FILL_MODELS):
    grouped=defaultdict(list)
    for e in cases:
        panel=tracks(e)
        for mode in modes:
            model=frozen.get(f"{panel}/{mode}",{})
            k=run(e,"K-EXECUTABLE",mode)
            for policy in VARIANTS:
                outcome=k if policy=="K-EXECUTABLE" else run(e,policy,mode,rdb.RDBCycle,model)
                grouped[panel,mode,policy].append(row(e,outcome,k))
    return grouped


def freeze():
    table=Path("trained.json").read_bytes()
    calendar=json.loads(Path("periods.json").read_text())
    config=dict(calendar=calendar,model_sha256=sha256(table).hexdigest(),
                contract_sha256=sha256(Path("contract.json").read_bytes()).hexdigest(),
                engine_hashes={n:sha256(Path(n).read_bytes()).hexdigest() for n in
                    ("06_RDB_POLICY.py","07_RISK_GATE.py","replay.py","holdout.py","04_CAUSAL_REPLAY.py")},
                cluster_draws=4000,bootstrap_seed=48211,primary_family=6,
                execution_evidence="MODEL_ONLY")
    Path("08_FROZEN_CONFIG.json").write_text(json.dumps(config,indent=2)+"\n")
    Path("08_TRAINED_TABLES.json").write_bytes(table)


def read_frozen():
    f=json.loads(Path("08_FROZEN_CONFIG.json").read_text())
    table=Path("08_TRAINED_TABLES.json").read_bytes()
    assert sha256(table).hexdigest()==f["model_sha256"]
    assert sha256(Path("contract.json").read_bytes()).hexdigest()==f["contract_sha256"]
    assert all(sha256(Path(n).read_bytes()).hexdigest()==h for n,h in f["engine_hashes"].items())
    return json.loads(table),f


def main(folder):
    model,frozen=read_frozen()
    cases=[e for e in read(folder) if e["fold"]=="final_test"]
    assert {e["month"] for e in cases}==set(frozen["calendar"]["final_test"])
    all_panels=analyze(cases,model)
    scores=[summarize(*key,r) for key,r in all_panels.items()]
    publish_csv("08_PAIRED_RESULTS.csv",scores)
    primary=[]
    for (panel,mode,policy),r in all_panels.items():
        if panel!="S2/30":
            continue
        for item in r:
            a,k=item["outcome"],item["k_outcome"]
            primary.append(dict(panel=panel,mode=mode,policy=policy,month=item["month"],id=item["id"],
                                complete=item["complete"],pnl=a["pnl"],k_pnl=k["pnl"],
                                flat=a["flat"],k_flat=k["flat"],delta=item["delta"],
                                residual=a["residual"],pending=a["pending"],violations=a["violations"],
                                decision=a["decision"],elapsed_ms=a["elapsed_ms"],attempts=a["attempts"]))
    publish_csv("08_PRIMARY_PATHS.csv",primary)


if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=="--freeze":
        freeze()
    else:
        main(sys.argv[1])
