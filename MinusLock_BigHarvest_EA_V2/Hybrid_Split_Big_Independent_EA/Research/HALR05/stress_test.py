"""Preregistered venue sensitivity and unchanged 88-scenario regression."""
from dataclasses import asdict
from hashlib import sha256
import importlib
from pathlib import Path
from statistics import mean
import sys

from main_test import aggregate,eligible,flatten_row,paired
from sim import CFG,NAMES,oracle,replay,run
from scenarios2 import stress
from economic_audit import ArchivedCase
io=importlib.import_module("04_CAUSAL_REPLAY")


def simulate(cases):
    matrix=[]
    counter=[]
    ideal=[]
    for e in cases:
        x=replay.run(e,"K-IDEAL","quote_fill")
        ideal.append(dict(month=e["month"],id=e["id"],analytic_pnl=x["pnl"],
                          evidence="ANALYTIC_NOT_EXECUTABLE"))
    for mode in CFG["execution"]:
        runs={k:[] for k in NAMES}
        selected=None
        for e in cases:
            for name in NAMES:
                o,t,a=run(e,name,mode)
                runs[name].append(flatten_row(e,mode,name,o,a))
                if selected is None and (o["violations"] or not o["flat"]):
                    selected=dict(mode=mode,policy=name,episode=e,outcome=o,
                                  independent=a,journal=t)
        p=[paired(m,k) for m,k in zip(runs["M-ER"],runs["K-EXECUTABLE"],strict=True)]
        d=[r["delta"] for r in p if r["delta"] is not None]
        for name,v in runs.items():
            matrix.append(dict(**aggregate(mode,name,v),paired_m_flat=len(d),
                               m_delta_vs_actual_k=mean(d) if d else None,
                               max_additional_m_loss=max(0,-min(d)) if d else None))
        if selected is not None:
            counter.append(selected)
    return matrix,counter,ideal


def archived():
    rows=[]
    worst={}
    for i,c in enumerate(stress(replay.limits().horizon)):
        sg=c.orientation
        entry=-300*sg+110000
        fixture={"entry":[0,entry-10,entry+10]}
        for name in NAMES:
            ctx=replay.venue.PROFILES["E1"] if name.endswith("-ER") else None
            trace=[]
            output=replay.venue.replay(name,ArchivedCase(c),replay.limits(),
                                      replay.Params(),replay.DEFAULTS[name],trace,ctx)
            o=asdict(output)
            a=oracle.check(fixture,trace,replay.limits(),o)
            rows.append(dict(policy=name,case=c.name,index=i,orientation=sg,
                             **{k:o[k] for k in ("pnl","low","flat","success","violations",
                                   "residual","pending","failures","cost","gross","net","margin","time")},
                             end_net=a["end_net"],fills=a["verified_fills"]))
            if name not in worst or o["pnl"]<worst[name]["outcome"]["pnl"]:
                worst[name]=dict(policy=name,case=c.name,index=i,orientation=sg,
                                 moves=c.moves,events=c.events,outcome=o,journal=trace)
    return rows,list(worst.values())


if __name__=="__main__":
    c=eligible(sys.argv[1])
    matrix,counter,ideal=simulate(c)
    a,b=archived()
    io.csv_out("08_EXECUTION_MATRIX",matrix)
    io.csv_out("08_STRESS_RESULTS",a)
    io.json_out("08_COUNTEREXAMPLES",dict(holdout=counter,archived_worst=b,
        scenario_source_hash=sha256((Path(__file__).parent/"01_DEPENDENCY_HASHES.json").read_bytes()).hexdigest()))
    if ideal:
        io.csv_out("08_ANALYTIC_K_IDEAL",ideal)
    print(len(matrix),len(a),len(counter))
