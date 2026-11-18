"""Use actual bid/ask quotes at causal half-hour observation timestamps."""
from collections import Counter
from csv import DictWriter
from dataclasses import replace
import importlib
import json
from pathlib import Path
from statistics import mean

from baseline_audit import source
from a3rc import Params,choose_a3
from execution import Quote
from ledger2 import Limits
from meta_rc import choose_b,choose_m
from scan_historical import FOLDS

engine=importlib.import_module("04_EXECUTION_SIMULATOR")
a3=importlib.import_module("05_A3_ER_POLICY")
meta=importlib.import_module("06_META_ER_POLICY")
H=12
MODELS={"A3-RC":choose_a3,"A3-ER":a3.choose_er,"M-RC":choose_m,"M-ER":meta.choose_meta,
        "B4-RC":choose_b,"K-EXECUTABLE":None}


def quote(record):
    _,_,bid,ask=record
    return Quote((bid+ask)/2-110000,spread=ask-bid)


def episodes(records,h=H):
    anchors=[]
    rejected=0
    start=0
    while start<len(records)-1:
        anchor=records[start]
        j=start+1
        while j<len(records) and records[j][0]-records[j-1][0]<=4:
            change=quote(records[j]).mid-quote(anchor).mid
            if abs(change)>=300:
                window=records[j:j+h+1]
                intact=len(window)==h+1 and all(b[0]-a[0]<=4 for a,b in zip(window,window[1:]))
                if intact:
                    anchors.append((1 if change>0 else -1,anchor,window))
                else:
                    rejected+=1
                # Purge entry and full horizon, with a further H-slot embargo.
                start=j+2*h+1
                break
            j+=1
        else:
            start=j
    return anchors,rejected


def replay_history(variant,selector,episode,mode):
    orientation,anchor,window=episode
    assumed=engine.PROFILES["E1"]
    limits=Limits(horizon=H)
    kwargs={"envelope":assumed} if variant.endswith("-ER") else {}
    cy=engine.ExecutionCycle(variant,orientation,limits,Params(),selector=selector,**kwargs)
    initial=quote(anchor)
    cy.memory=replace(cy.memory,anchor=quote(window[0]).mid)
    cy.book.tickets={i:replace(t,entry=initial.mid) for i,t in cy.book.tickets.items()}
    cy.book.initial_cost=(initial.spread+limits.commission)*200
    for t,tick in enumerate(window):
        q=quote(tick)
        if mode=="bounded_slip":
            q=replace(q,slip=2)
        elif mode=="delayed_partial":
            q=replace(q,slip=2,delay=int(t%3==0),capacity=25 if t%3==0 else 1000,
                      rejects=int(t==2),unknown=t==10)
        cy.step(t,q)
        if cy.finish:
            break
    return cy.result()


if __name__=="__main__":
    summary=[]
    quality=json.loads(Path("07_DATA_QUALITY_REPORT.json").read_text())
    quality["episodes"]={}
    for month,fold in FOLDS.items():
        records=json.loads(Path(f"../slots-{month}.json").read_text())
        cases,drops=episodes(records)
        if not cases:
            print("No covered complete episodes",month)
        quality["episodes"][fold]=dict(count=len(cases),incomplete_removed=drops)
        for scenario in ("quote_fill","bounded_slip","delayed_partial"):
            for strategy,selector in MODELS.items():
                a=[replay_history(strategy,selector,e,scenario) for e in cases]
                flat=[x.pnl for x in a if x.flat]
                summary.append(dict(month=month,fold=fold,execution=scenario,variant=strategy,n=len(a),
                                    recoveries=sum(o.success for o in a),flat=len(flat),
                                    violations=sum(bool(o.violations) for o in a),
                                    realized_mean=mean(flat) if flat else "",
                                    worst_liquidation_mark=min((o.pnl for o in a),default=""),
                                    residual_count=sum(not o.flat for o in a),
                                    stopout=sum(o.margin_stopout for o in a)))
    with open("07_HISTORICAL_RESULTS.csv","w",newline="") as f:
        w=DictWriter(f,fieldnames=list(summary[0]),lineterminator="\n")
        w.writeheader()
        w.writerows(summary)
    Path("07_DATA_QUALITY_REPORT.json").write_text(json.dumps(quality,indent=2)+"\n")
