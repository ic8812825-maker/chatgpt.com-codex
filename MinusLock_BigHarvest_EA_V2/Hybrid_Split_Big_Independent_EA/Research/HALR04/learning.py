"""Frozen fold routing, training deltas, and validation-only ablation."""
from collections import defaultdict
import csv
import importlib
import json
from pathlib import Path
from statistics import mean

from replay import FILL_MODELS,run
rdb=importlib.import_module("06_RDB_POLICY")
BASE=("A3-ER","M-ER","K-EXECUTABLE")
VARIANTS=BASE+("K-IDEAL","RDB-0","RDB-1","RDB-2","RDB-3","RDB-4")


def read(folder):
    return json.loads((Path(folder)/"episodes.json").read_text())


def tracks(e):
    return f'{e["scheme"]}/{e["interval"]}'


def publish_csv(name,data):
    with Path(name).open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator="\n")
        w.writeheader()
        w.writerows(data)


def evaluate_baseline(cases):
    return [(e,{p:run(e,p,m) for p in BASE},m) for e in cases for m in FILL_MODELS]


def tables(rows):
    pools=defaultdict(list)
    for e,out,mode in rows:
        pools[(tracks(e),mode)].append((e,out))
    return {f"{version}/{mode}":rdb.fit(data) for (version,mode),data in sorted(pools.items())}


def validation(cases):
    initial=[e for e in cases if e["fold"]=="training"]
    validation=[e for e in cases if e["fold"]=="validation"]
    baseline=evaluate_baseline(initial)
    result=[]
    diagnostics=[]
    for month in sorted({e["month"] for e in validation}):
        prepared=tables(baseline)
        slice=[e for e in validation if e["month"]==month]
        for e,out,mode in evaluate_baseline(slice):
            table=prepared.get(f"{tracks(e)}/{mode}",{})
            for policy in VARIANTS:
                log=[]
                r=out[policy] if policy in out else run(e,policy,mode,rdb.RDBCycle,table,log)
                q=out["K-EXECUTABLE"]
                d=r["pnl"]-q["pnl"] if r["flat"] and q["flat"] else None
                result.append(dict(month=month,scheme=e["scheme"],interval=e["interval"],mode=mode,
                                   policy=policy,success=r["success"],flat=r["flat"],
                                   violations=bool(r["violations"]),delta=d,mark=r["pnl"],
                                   decision=r["decision"]))
                if len(diagnostics)<500 and e["scheme"]=="S2" and e["interval"]==30 and policy.startswith("RDB-"):
                    for row in log:
                        diagnostics.append(dict(month=month,id=e["id"],mode=mode,policy=policy,
                                                step=row["step"],event=row["event"],
                                                details=json.dumps({k:v for k,v in row.items() if k not in ("event","step")},sort_keys=True)))
        baseline.extend(evaluate_baseline(slice))
    out=[]
    grouped=defaultdict(list)
    for r in result:
        grouped[(r["scheme"],r["interval"],r["mode"],r["policy"])].append(r)
    for (scheme,interval,mode,policy),rows in sorted(grouped.items()):
        delta=[r["delta"] for r in rows if r["delta"] is not None]
        out.append(dict(scheme=scheme,interval=interval,mode=mode,policy=policy,trials=len(rows),
                        clusters=len({r["month"] for r in rows}),success=sum(r["success"] for r in rows),
                        flat=sum(r["flat"] for r in rows),violations=sum(r["violations"] for r in rows),
                        paired_flat=len(delta),mean_paired_delta=mean(delta) if delta else "",
                        initial_recover=sum(r["decision"].startswith("RECOVER") for r in rows)))
    publish_csv("06_ABLATIONS.csv",out)
    publish_csv("06_DECISION_TRACE.csv",diagnostics)
    return tables(baseline)


if __name__=="__main__":
    import sys
    state=validation(read(sys.argv[1]))
    Path("trained.json").write_text(json.dumps(state,indent=2,sort_keys=True)+"\n")
