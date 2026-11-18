"""Reconstruct HALR-02 stress constraints from external quotes and confirmed fills."""
import csv
import importlib
import json
from dataclasses import asdict,replace
from pathlib import Path

from baseline_audit import reconcile,scenario_journal
from pinned import source
source()
from a3rc import Params
from audit2 import configured
from execution import Intent,Quote,Venue
from ledger2 import Ledger,Limits
from runner import run
from scenarios2 import Scenario,stress

Oracle=importlib.import_module("02_MONEY_ORACLE").Oracle
TERMINAL={"REJECTED","FILLED","CANCELLED","EXPIRED"}


def first_unsafe(log,orientation,limits,outcome):
    o=Oracle(orientation)
    spent=0
    active={}
    prev_mid=0
    snap=None
    fills=[]
    first=None
    action=""
    gross,net=200,0
    for e in log:
        event=e["event"]
        if event=="QUOTE":
            fills=[]
            q=e
            before=(net,gross)
            waiting=len(active)
            action=""
            move=e["mid"]-prev_mid
            prev_mid=e["mid"]
            if e["step"]:
                o.carry(e["carry"])
                spent+=e["carry"]*gross
        elif event=="CREATED":
            active[e["order"]]=[e["side"],e["units"],e["ticket"]]
            action=f'{e["side"]:+d}/{e["units"]}/{e["ticket"]}'
        elif event=="FILL":
            o.confirmed(e["side"],e["units"],e["ticket"],q["mid"],q["spread"],q["slip"])
            spent+=e["units"]*(q["spread"]+2*q["slip"]+limits.commission)
            active[e["order"]][1]-=e["units"]
            net,gross=e["net"],e["gross"]
            fills.append([e["side"],e["units"],e["ticket"]])
        elif event in TERMINAL:
            active.pop(e["order"],None)
        elif e["order"] is None:
            action=event
        mark=o.liquidation(q["mid"],q["spread"],q["slip"])
        fee=q["spread"]+2*q["slip"]+limits.commission
        pending_open=sum(n for _,n,ticket in active.values() if ticket is None)
        violations=[]
        if mark < -200*limits.loss:violations.append("LOSS")
        if spent+fee*(gross+2*pending_open)>200*limits.cost:violations.append("COST")
        if (200*limits.capital+mark)*limits.leverage*10000 < (
                gross*max(0,220000+2*q["mid"]+q["spread"])*limits.margin_level):
            violations.append("MARGIN")
        if abs(net)>limits.net or gross>limits.gross:violations.append("EXPOSURE")
        snap=dict(first_event=q["step"],phase=event,net_before=before[0]/100,
                  gross_before=before[1]/100,capacity=q["capacity"],pending_before=waiting,
                  intended=action,confirmed=json.dumps(fills),movement=move,
                  spread=q["spread"],slip=q["slip"],pnl_at_event=mark/200,
                  first_constraint="|".join(violations))
        if violations and first is None:
            first=snap
    if first is None and outcome.violations:
        first=dict(snap,first_constraint=outcome.violations)
    if first and not first["intended"]:
        first["intended"]="pre-decision"
    return first


def witnesses():
    h=3
    named=[
        ("refusal_before_gap",(300,300,-4000),{2:dict(rejects=100)}, "A3-RC"),
        ("no_liquidity",(0,0,0),{t:dict(capacity=0) for t in range(4)},"K-EXECUTABLE"),
        ("one_leg",(300,0,0),{0:dict(capacity=50)},"K-EXECUTABLE"),
        ("unknown_then_fill",(0,0,0),{0:dict(unknown=True)},"K-EXECUTABLE"),
        ("wide_open",(0,0,0),{0:dict(spread=100)},"K-EXECUTABLE"),
        ("delay",(300,0,0),{0:dict(delay=1)},"K-EXECUTABLE"),
        ("capacity",(0,0,0),{t:dict(capacity=1) for t in range(4)},"K-EXECUTABLE"),
        ("stopout",(300,300,-90000),{2:dict(rejects=100)},"A3-RC"),
        ("repeat_safe",(0,0,0),{t:dict(rejects=100) for t in range(4)},"K-EXECUTABLE"),
    ]
    result=[]
    for key,moves,settings,policy in named:
        def build(length):
            return Scenario(1,moves[:length],key,tuple((i,tuple(v.items())) for i,v in settings.items() if i<=length))
        # Preserve the mechanism and shrink only where it survives a shorter horizon.
        condition={
            "refusal_before_gap":lambda r,j:"LOSS" in r.violations and r.failures>0,
            "no_liquidity":lambda r,j:not r.flat,
            "one_leg":lambda r,j:"LOSS" in r.violations and r.flat,
            "unknown_then_fill":lambda r,j:any(e["event"]=="UNKNOWN" for e in j) and r.flat,
            "wide_open":lambda r,j:"COST" in r.violations,
            "delay":lambda r,j:any(e["event"]=="FILL" and e["step"]>0 for e in j) and r.flat,
            "capacity":lambda r,j:not r.flat and any(e["event"]=="PARTIAL" for e in j),
            "stopout":lambda r,j:r.margin_stopout,
            "repeat_safe":lambda r,j:r.failures>=2 and not r.flat,
        }[key]
        pool=[]
        for length in range(h+1):
            s=build(length)
            log=[]
            r=run(policy,s,Limits(horizon=length),Params(),journal=log)
            pool.append((length,s,r,log))
        match=next((item for item in pool if condition(*item[2:])),None)
        length,s,r,log=match or pool[-1]
        result.append(dict(mechanism=key,matched=match is not None,horizon=length,
                           scenario=asdict(s),outcome=asdict(r),journal=log))
    v=Venue(Ledger(1,Limits()),[])
    v.advance(0,Quote(0,delay=1))
    order=v.submit(Intent(1,10))
    v.cancel(order)
    v.advance(1,Quote(150,cancel_race=True))
    assert order.state.value=="FILLED"
    result.append(dict(mechanism="cancel_race",matched=True,horizon=1,journal=v.journal))
    return result


def main():
    root=source()
    with (root/"COMPARISON_RESULTS.csv").open() as f:
        comp=list(csv.DictReader(f))
    with (root/"ADVERSARIAL_RESULTS.csv").open() as f:
        original={(r["label"],int(r["index"])):r for r in csv.DictReader(f)}
    failures=[]
    for mode in comp:
        c=configured(mode)
        label=mode["label"]
        for index,s in enumerate(stress(c.limits.horizon)):
            outcome,log=scenario_journal(c.name,c.p,c.selector,s,c.limits)
            ref=original[label,index]
            assert outcome.violations==ref["violations"] and abs(outcome.pnl-float(ref["pnl"]))<1e-7
            if not outcome.violations:
                continue
            assert reconcile(log,s.orientation)[0]==round(outcome.pnl*200)
            k=run("K-EXECUTABLE",s,c.limits)
            if s.name in ("no_liquidity","unknown"):
                category="UNAVOIDABLE_FROM_INITIAL_STATE"
            elif not k.violations:
                category="PREVENTABLE"
            else:
                category="EXECUTION_DEPENDENT"
            v=first_unsafe(log,s.orientation,c.limits,outcome)
            failures.append(dict(scenario=f'{c.limits.horizon}/{index}/{s.name}',policy=label,
                                 orientation=s.orientation,**v,constraints=outcome.violations,
                                 final_pnl=outcome.pnl,residual=outcome.residual,
                                 classification=category,causal_alternative="K-EXECUTABLE" if category=="PREVENTABLE" else "",
                                 k_pnl=k.pnl,k_flat=k.flat,k_violations=k.violations))
    with Path("03_FAILURE_TAXONOMY.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(failures[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(failures)
    Path("03_MINIMAL_COUNTEREXAMPLES.json").write_text(json.dumps(witnesses(),indent=1)+"\n")
    print(len(original),len(failures))


if __name__=="__main__":
    main()
