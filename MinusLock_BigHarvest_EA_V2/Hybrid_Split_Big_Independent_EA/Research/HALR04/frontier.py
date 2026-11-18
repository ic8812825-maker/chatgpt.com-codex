"""Economic frontier, archived stress replay, and causal sensitivities."""
from collections import defaultdict
from csv import DictReader
from dataclasses import asdict,replace
import json
from statistics import mean

from economic_audit import ArchivedCase
from learning import VARIANTS,publish_csv,read,rdb
from replay import DEFAULTS,FILL_MODELS,Params,initial_state,limits,quote,run,venue
from holdout import analyze,cvar,read_frozen,row,summarize
from scenarios2 import stress


def core_replay(case,policy,table):
    if policy=="K-IDEAL":
        out=asdict(venue.replay(policy,ArchivedCase(case),limits(),Params()))
        out.update(attempts=0,elapsed_ms=0,quote_events=1,decision="ANALYTIC")
        return out
    trace=[]
    l=limits()
    if policy in DEFAULTS or policy=="RDB-0":
        name="K-EXECUTABLE" if policy=="RDB-0" else policy
        selected=DEFAULTS[name]
        options={"envelope":venue.PROFILES["E1"]} if name.endswith("-ER") else {}
        c=venue.ExecutionCycle(name,case.orientation,l,Params(),selector=selected,journal=trace,**options)
    else:
        e=dict(orientation=case.orientation,features=dict(spread=case.quote(0,0).spread,
              range30=None,momentum=None),contract="E1")
        c=rdb.RDBCycle(policy,e,table,l,trace)
    path=ArchivedCase(case)
    mid=0
    for t in range(l.horizon+1):
        c.step(t,path.quote(t,mid))
        if c.finish:
            break
        if t<l.horizon:
            mid+=path.next_move(t,c.book.net)
    out=asdict(c.result())
    out.update(attempts=sum(r["event"]=="CREATED" for r in trace),elapsed_ms=0,
               quote_events=t+1,decision=getattr(c,"initial_decision",policy))
    return out


def archive(table):
    all_rows=[]
    aggregate=defaultdict(list)
    for i,case in enumerate(stress(limits().horizon)):
        k=core_replay(case,"K-EXECUTABLE",table)
        for name in VARIANTS:
            o=k if name=="K-EXECUTABLE" else core_replay(case,name,table)
            d=o["pnl"]-k["pnl"] if o["flat"] and k["flat"] else None
            rec=dict(scenario=case.name,index=i,orientation=case.orientation,policy=name,
                     mark=o["pnl"],shortfall=o["low"],k_mark=k["pnl"],
                     paired_realized_delta=d if d is not None else "",flat=o["flat"],k_flat=k["flat"],
                     residual=o["residual"],pending=o["pending"],amount_paid=o["cost"],
                     reserve_peak=o["cost_with_reserve"],gross=o["gross"],net=o["net"],margin=o["margin"],
                     violations=o["violations"],failures=o["failures"],recovered=o["success"],
                     attempts=o["attempts"],quote_events=o["quote_events"],decision=o["decision"])
            all_rows.append(rec)
            aggregate[name].append(rec)
    assert all(len(r)==88 for r in aggregate.values())
    return all_rows,aggregate


def pareto(rows):
    selected=[r for r in rows if r["policy"]!="K-IDEAL" and r["panel"]=="S2/30"]
    eligible=[r for r in selected if r["risk_violations"]=="0" and r["flat"]==r["n"]]
    def vector(r):
        return tuple(float(r[key])*s for key,s in zip(
            ("recovery_rate","mean_terminal","cvar99_realized","worst_realized","mean_new_cost",
             "flat_rate","execution_failures"),(1,1,-1,1,-1,1,-1)))
    def frontier(r):
        if r not in eligible:
            return "INFEASIBLE"
        this=vector(r)
        for other in eligible:
            if r["mode"]!=other["mode"]:
                continue
            a=vector(other)
            if a!=this and all(x>=y for x,y in zip(a,this)):
                return "DOMINATED"
        return "NONDOMINATED"
    return [dict(**r,frontier=frontier(r)) for r in selected]


def reprice(e,same_spread=None,cap_movement=None,rebase=False):
    v=dict(e)
    last_input=last_output=None
    q=[]
    _,first_bid,first_ask=e["obs"][0]
    offset=110000-(first_bid+first_ask)/2 if rebase else 0
    for t,b,a in e["obs"]:
        observed=(b+a)/2+offset
        if last_input is None or cap_movement is None:
            mid=observed
        else:
            d=max(-cap_movement,min(cap_movement,observed-last_input))
            mid=last_output+d
        last_input,last_output=observed,mid
        spread=a-b if same_spread is None else same_spread
        q.append((t,mid-spread/2,mid+spread/2))
    v["obs"]=q
    if same_spread is not None or rebase:
        t,b,a=e["entry"]
        mid=(b+a)/2+offset
        spread=a-b if same_spread is None else same_spread
        v["entry"]=(t,mid-spread/2,mid+spread/2)
    return v


def short_route(e,name,h,table):
    kw={"envelope":venue.PROFILES["E1"]} if name.endswith("-ER") else {}
    l=replace(limits(),horizon=h)
    trace=[]
    if name.startswith("RDB-"):
        c=rdb.RDBCycle(name,e,table,l,trace)
    else:
        c=venue.ExecutionCycle(name,e["orientation"],l,Params(),
                               selector=DEFAULTS[name],journal=trace,**kw)
    initial_state(c,e)
    for t,rec in enumerate(e["obs"][:h+1]):
        c.step(t,quote(rec,t,"quote_fill"))
        if c.finish:
            break
    r=asdict(c.result())
    r.update(elapsed_ms=e["obs"][t][0]-e["obs"][0][0],quote_events=t+1,
             attempts=sum(x["event"]=="CREATED" for x in trace),
             decision=getattr(c,"initial_decision",name))
    return r


def effects(cases,table):
    r=[]
    for policy in ("A3-ER","M-ER","K-EXECUTABLE","RDB-3"):
        for label,p in (("actual_quotes",{}),("constant_20_model",{"same_spread":20}),
                        ("clipped_300_model",{"cap_movement":300}),
                        ("rebase_1_1000_model",{"rebase":True})):
            a=[run(reprice(e,**p),policy,"quote_fill",rdb.RDBCycle,table) for e in cases]
            r.append(dict(component=label,policy=policy,horizon=12,
                          n=len(a),flat=sum(x["flat"] for x in a),recovery=sum(x["success"] for x in a),
                          mean_realized=mean(x["pnl"] for x in a if x["flat"]) if any(x["flat"] for x in a) else "",
                          violations=sum(bool(x["violations"]) for x in a)))
        for h in (4,8,12):
            a=[short_route(e,policy,h,table) for e in cases]
            r.append(dict(component="horizon_sensitivity",policy=policy,horizon=h,
                          n=len(a),flat=sum(x["flat"] for x in a),recovery=sum(x["success"] for x in a),
                          mean_realized=mean(x["pnl"] for x in a if x["flat"]) if any(x["flat"] for x in a) else "",
                          violations=sum(bool(x["violations"]) for x in a)))
    return r


def regime(cases,table):
    raw=defaultdict(list)
    for e in cases:
        k=run(e,"K-EXECUTABLE")
        leaf=rdb.buckets(e["features"])[0]
        for name in ("RDB-1","RDB-2","RDB-3","RDB-4"):
            o=run(e,name,"quote_fill",rdb.RDBCycle,table)
            raw[leaf,name,o["decision"]].append(row(e,o,k))
    result=[]
    for (group,route,decision),rows in sorted(raw.items()):
        delta=[x["delta"] for x in rows if x["delta"] is not None]
        result.append(dict(group=group,route=route,decision=decision,n=len(rows),
                           clusters=len({x["month"] for x in rows}),paired_flat=len(delta),
                           mean_delta=mean(delta) if delta else "",
                           violations=sum(bool(x["outcome"]["violations"]) for x in rows)))
    return result


if __name__=="__main__":
    import sys
    model,cfg=read_frozen()
    with open("08_PAIRED_RESULTS.csv") as f:
        oos=list(DictReader(f))
    publish_csv("09_ECONOMIC_FRONTIER.csv",pareto(oos))
    archive_rows,catalog=archive(model["S2/30/quote_fill"])
    publish_csv("09_STRESS_MATRIX.csv",archive_rows)
    summaries=[]
    vals=[]
    for r in oos:
        if r["panel"]=="S2/30":
            vals.append(dict(panel=r["mode"],policy=r["policy"],samples=r["n"],clusters=r["clusters"],
                             paired_flat=r["paired_flat"],delta=r["paired_mean"],low=r["paired_low"],
                             high=r["paired_high"],worst_additional_loss=r["max_additional_loss"],
                             risk_violations=r["risk_violations"],residual=r["residual_count"],
                             pending=r["pending_count"]))
    for policy,r in catalog.items():
        paired=[x["paired_realized_delta"] for x in r if x["paired_realized_delta"]!=""]
        n=len(r)
        risk=sum(bool(x["violations"]) for x in r)
        residual=sum(x["residual"]>0 for x in r)
        pending=sum(x["pending"]>0 for x in r)
        sums=dict(policy=policy,scenarios=n,flat=sum(x["flat"] for x in r),recovery=sum(x["recovered"] for x in r),
                  violations=risk,residual=residual,pending=pending,worst_mark=min(x["mark"] for x in r),
                  worst_intracycle=min(x["shortfall"] for x in r),cvar99_mark=cvar([-x["mark"] for x in r]),
                  failures=sum(x["failures"] for x in r))
        summaries.append(sums)
        vals.append(dict(panel="archive_88",policy=policy,samples=n,clusters="",
                         paired_flat=len(paired),delta=mean(paired) if paired else "",low="",high="",
                         worst_additional_loss=max(0,-min(paired)) if paired else "",risk_violations=risk,
                         residual=residual,pending=pending))
    publish_csv("09_STRESS_SUMMARY.csv",summaries)
    publish_csv("09_PAIRED_VALUE_VS_K.csv",vals)
    initial=read(sys.argv[1])
    crisis=[e for e in initial if e["month"]=="202003" and e["interval"]==30]
    windows=analyze(crisis,model)
    publish_csv("09_CRISIS_RESULTS.csv",[summarize(*k,v) for k,v in windows.items()])
    final=[e for e in initial if e["fold"]=="final_test" and e["scheme"]=="S2" and e["interval"]==30]
    publish_csv("09_MECHANISM_SENSITIVITY.csv",effects(final,model["S2/30/quote_fill"]))
    publish_csv("09_BOUNDARY_BY_REGIME.csv",regime(final,model["S2/30/quote_fill"]))
