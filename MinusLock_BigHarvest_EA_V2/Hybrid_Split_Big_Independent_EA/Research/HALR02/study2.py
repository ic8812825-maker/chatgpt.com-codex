"""Fit on training and validation, certify under the declared nominal contract."""
import csv
from dataclasses import asdict, dataclass, replace
import json
import math
from pathlib import Path
import random
from statistics import mean, median
import sys
import unittest

from a3rc import Params
from comparators import SETTINGS
from exhaustive2 import NodeLimit, exact
from ledger2 import Limits, TICKS
from meta_rc import choose_m
from runner import run
from scenarios2 import sample, stress

LOSSES=(58,100,150,180,250,300,500)
COSTS=(0,10,20,30,50)
TRAIN=(202701,24)
VALID=(202702,96)
TEST=(202703,1200)


@dataclass(frozen=True,slots=True)
class Candidate:
    name: str
    p: Params
    limits: Limits

    @property
    def selector(self):
        return SETTINGS.get(self.name,(None,None))[1]

    def apply(self,s,journal=None):
        return run(self.name,s,self.limits,self.p,selector=self.selector,journal=journal)


def evaluate(c,paths):
    return [c.apply(s) for s in paths]


def tail(values, confidence):
    worst=sorted(values,reverse=True)
    mass=len(worst)*(1-confidence)
    k=int(mass)
    return (sum(worst[:k])+(mass-k)*worst[k])/mass


def summarize(results, ci=False):
    n=len(results)
    recover=sum(o.success for o in results)
    p=recover/n
    lo=hi=""
    if ci:
        z=1.95996398454
        center=(p+z*z/(2*n))/(1+z*z/n)
        half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
        lo,hi=max(0,center-half),min(1,center+half)
    times=[o.time for o in results if o.success]
    pnl=[o.pnl for o in results]
    losses=[-x for x in pnl]
    return dict(n=n,recoveries=recover,recovery_rate=p,wilson_lo=lo,wilson_hi=hi,
                flat=sum(o.flat for o in results),flat_rate=mean(o.flat for o in results),
                mean_pnl=mean(pnl),median_pnl=median(pnl),worst_pnl=min(pnl),
                intracycle=min(o.low for o in results),cvar95=tail(losses,.95),cvar99=tail(losses,.99),
                max_drawdown=max(o.drawdown for o in results),total_cost=sum(o.cost for o in results),
                max_cost_reserve=max(o.cost_with_reserve for o in results),
                max_gross=max(o.gross for o in results),max_net=max(o.net for o in results),
                margin_stress=max(o.margin for o in results),recovery_time=mean(times) if times else "",
                forced_exits=sum(o.forced for o in results),stopout=sum(o.margin_stopout for o in results),
                residual=sum(o.residual>0 for o in results),pending=sum(o.pending>0 for o in results),
                execution_failures=sum(o.failures for o in results),
                risk_violations=sum(bool(o.violations) for o in results),
                early_core_close=sum(o.core_closed_early for o in results))


def rank(stats):
    time=stats["recovery_time"] if stats["recovery_time"]!="" else math.inf
    return (stats["recovery_rate"],-stats["cvar99"],-stats["cvar95"],-stats["max_drawdown"],
            stats["mean_pnl"],-stats["total_cost"],-time)


def grid(limits):
    r=random.Random(3970)
    yield Candidate("K-EXECUTABLE",Params(),limits)
    yield Candidate("A3-RC",Params(),limits)
    for core in range(1,101):
        net=(29*core)%50+1
        p=Params(core,net,r.choice((0,75,140,225,300)),r.choice((1,2,3,5,8)),
                 r.choice((0,25,50,75)),r.choice((1,2,3)),r.choice((True,False)),
                 r.choice((0,5,15)),time_buffer=r.choice((0,0,0,1)),direction=r.choice((1,1,1,-1)))
        yield Candidate("A3-RC",p,replace(limits,gross=r.choice((200,300,500)),
                                         horizon=r.choice((4,6,8,8,12))))
    for depth in (2,4,6,8):
        for i in range(4):
            p=Params(core=r.choice((10,25,50,100)),net=r.choice((12,20,25,30,40,50)),
                     trigger=r.choice((0,75,140,225)),switches=r.choice((2,4,6,8)),
                     harvest=r.choice((25,50,75)),attempts=r.choice((1,2,3)),
                     neutral=r.choice((True,False)),reserve=r.choice((0,5,15)),depth=depth)
            yield Candidate("M-RC",p,replace(limits,gross=r.choice((200,300,500))))


def metadata(c):
    return dict(policy=c.name,horizon=c.limits.horizon,gross_cap=c.limits.gross,
                params=json.dumps(asdict(c.p),sort_keys=True,separators=(",",":")))


def write(name, rows):
    with Path(name+".csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows({k:round(v,9) if isinstance(v,float) else v for k,v in r.items()} for r in rows)


def fixed_models(loss,cost):
    l=Limits(loss=loss,cost=cost)
    result=[Candidate("K-IDEAL",Params(),l),Candidate("K-EXECUTABLE",Params(),l),
            Candidate("A3-RC",Params(),l)]
    result += [Candidate(key,p,l) for key,(p,_) in SETTINGS.items() if key!="M-RC"]
    result += [Candidate("M-RC",Params(depth=d),l) for d in (2,4,6,8)]
    return result


def optimize():
    train,valid,test=(list(sample(*seed)) for seed in (TRAIN,VALID,TEST))
    opt,front,chosen=[],[],{}
    feasible_winners={}
    for loss in LOSSES:
        for cost in COSTS:
            l=Limits(loss=loss,cost=cost)
            if cost<29:
                front.append(dict(loss_budget=loss,cost_budget=cost,policy="",horizon="",
                                  recovery_rate="",wilson_lo="",wilson_hi="",worst="",cvar99="",
                                  max_cost="",risk_violations="",flat_rate="",
                                  status="NO_FEASIBLE_RECOVERY_POLICY"))
                continue
            by_family={}
            for c in grid(l):
                score=summarize(evaluate(c,train))
                if not score["risk_violations"]:
                    by_family.setdefault(c.name,[]).append((rank(score),c))
            rows=[]
            for family,items in by_family.items():
                for train_rank,c in sorted(items,key=lambda item:item[0],reverse=True)[:4]:
                    score=summarize(evaluate(c,valid))
                    opt.append(dict(loss_budget=loss,cost_budget=cost,**metadata(c),
                                    training_recovery=train_rank[0],**score))
                    if not score["risk_violations"]:
                        rows.append((rank(score),c))
            if not rows:
                raise AssertionError("nominal K should be feasible")
            rows.sort(key=lambda row:row[0],reverse=True)
            best=rows[0][1]
            for f in ("A3-RC","M-RC","K-EXECUTABLE"):
                local=next((c for _,c in rows if c.name==f),None)
                if local:
                    feasible_winners[loss,cost,f]=local
            chosen[loss,cost]=best
            s=summarize(evaluate(best,test),True)
            if s["risk_violations"]:
                raise AssertionError((best,s))
            front.append(dict(loss_budget=loss,cost_budget=cost,policy=best.name,horizon=best.limits.horizon,
                              recovery_rate=s["recovery_rate"],wilson_lo=s["wilson_lo"],
                              wilson_hi=s["wilson_hi"],worst=s["worst_pnl"],cvar99=s["cvar99"],
                              max_cost=s["max_cost_reserve"],risk_violations=s["risk_violations"],
                              flat_rate=s["flat_rate"],
                              status="NO_FEASIBLE_RECOVERY_POLICY" if loss==58
                                     else "RISK_PROVEN_WITHIN_MODEL"))
        print("optimized",loss,flush=True)

    write("COST_BUDGET_FRONTIER",front)
    write("OPTIMAL_PARAMETERS",opt)
    selected=[]
    for (loss,cost),c in chosen.items():
        selected.append(dict(loss_budget=loss,cost_budget=cost,**metadata(c)))
    write("SELECTED_POLICIES",selected)
    points=[r for r in front if r["policy"]]
    axes=("recovery_rate","worst","cvar99","max_cost")
    values=[tuple(r[k]*(1 if i<2 else -1) for i,k in enumerate(axes)) for r in points]
    keep=[r for r,x in zip(points,values)
          if not any(y!=x and all(a>=b for a,b in zip(y,x)) for y in values)]
    write("RECOVERY_RISK_FRONTIER",keep)
    return test,feasible_winners


def paired(policies, test, base_out):
    output=[]
    n=len(test)
    half=math.sqrt(2*math.log(40)/n)  # distribution-free paired difference in [-1, 1]
    for name,results in policies.items():
        if name=="K-EXECUTABLE":
            continue
        a=sum(r.success and not s.success for r,s in zip(results,base_out))
        b=sum(s.success and not r.success for r,s in zip(results,base_out))
        value=(a-b)/n
        output.append(dict(candidate=name,baseline="K-EXECUTABLE",n=n,only_candidate=a,
                           only_baseline=b,recovery_difference=value,lo95=max(-1,value-half),
                           hi95=min(1,value+half),mean_pnl_delta=mean(r.pnl-s.pnl for r,s in zip(results,base_out))))
    if "A3-selected" in policies and "M-selected" in policies:
        a,b=policies["A3-selected"],policies["M-selected"]
        x=sum(r.success and not s.success for r,s in zip(a,b))
        y=sum(s.success and not r.success for r,s in zip(a,b))
        d=(x-y)/n
        output.append(dict(candidate="A3-selected",baseline="M-selected",n=n,only_candidate=x,
                           only_baseline=y,recovery_difference=d,lo95=max(-1,d-half),
                           hi95=min(1,d+half),mean_pnl_delta=mean(r.pnl-s.pnl for r,s in zip(a,b))))
    return output


def compare(test,winners):
    profiles=[(c.name+(f"-d{c.p.depth}" if c.name=="M-RC" else ""),c)
              for c in fixed_models(180,50)]
    for family,name in (("A3-RC","A3-selected"),("M-RC","M-selected")):
        c=winners[180,50,family]
        profiles.append((name,c))
    summary_rows,stress_rows,journals={},[],[]
    results={}
    for label,c in profiles:
        results[label]=evaluate(c,test)
        summary_rows[label]=dict(label=label,**metadata(c),**summarize(results[label],True))
        cases=list(stress(c.limits.horizon))
        for i,s in enumerate(cases):
            outcome=c.apply(s)
            record=dict(label=label,orientation=s.orientation,case=s.name,index=i,
                        moves=" ".join(map(str,s.moves)),events=json.dumps(s.events),
                        adaptive=s.adaptive,**asdict(outcome))
            stress_rows.append(record)
            if outcome.violations and not any(j["label"]==label and j["case"]==s.name for j in journals):
                trace=[]
                c.apply(s,journal=trace)
                journals.append(dict(label=label,case=s.name,scenario=record,journal=trace))
    write("COMPARISON_RESULTS",list(summary_rows.values()))
    write("ADVERSARIAL_RESULTS",stress_rows)
    write("PAIRED_COMPARISON",paired(results,test,results["K-EXECUTABLE"]))
    Path("COUNTEREXAMPLE_JOURNALS.jsonl").write_text(
        "".join(json.dumps(j,separators=(",",":"))+"\n" for j in journals))
    return profiles


def exhaustive(profiles):
    rows=[]
    focus=[(k,c) for k,c in profiles if k in ("A3-selected","M-selected","K-EXECUTABLE")]
    for label,c in focus:
        for h in (4,6,8,12):
            l=replace(c.limits,horizon=h)
            for o in (-1,1):
                print("exhaustive",label,h,o,flush=True)
                try:
                    result,nodes=exact(c.name,o,c.p,l,c.selector,node_limit=90000)
                    status="COMPLETE"
                    x=dict(result._asdict())
                    x["worst"]/=TICKS
                    x["low"]/=TICKS
                except NodeLimit as e:
                    nodes=e.args[0]
                    status="NODE_LIMIT_REACHED"
                    x={k:"" for k in ("paths","successes","violations","worst","low","residual","flat")}
                rows.append(dict(label=label,horizon=h,orientation=o,expected=5**h,
                                 memo_states=nodes,status=status,**x))
    write("EXHAUSTIVE_RESULTS",rows)


def unit_tests():
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover("."))
    Path("TEST_RESULTS.json").write_text(json.dumps(
        dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
             passed=result.wasSuccessful(),python=sys.version.split()[0]),indent=2)+"\n")
    if not result.wasSuccessful():
        raise SystemExit(1)


if __name__=="__main__":
    unit_tests()
    test,winners=optimize()
    profiles=compare(test,winners)
    exhaustive(profiles)
