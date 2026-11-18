"""Independent consistency audit and matched-horizon replay."""
from collections import Counter
from csv import DictReader
from dataclasses import asdict,replace
import json
import math
from pathlib import Path

from a3rc import Params
from ledger2 import Limits
from execution import Intent
from runner import Cycle,run
from scenarios2 import Scenario,sample
from study2 import Candidate,TEST,evaluate,summarize,write


def load(name):
    with open(name+".csv") as f:
        return list(DictReader(f))


def configured(row,h=None):
    p=Params(**json.loads(row["params"]))
    l=Limits(horizon=h or int(row["horizon"]),gross=int(row["gross_cap"]))
    return Candidate(row["policy"],p,l)


class StrictCoreCycle(Cycle):
    """Diagnostic ablation: loss/expiry exits retain the preset original floor."""
    def exit(self):
        if self.book.mark(self.v.quote)>0:
            return super().exit()
        b,v=self.book,self.v
        if v.active:
            return
        loser=1 if b.orientation>0 else 0
        while b.gross:
            for i,t in b.tickets.items():
                floor=self.params.core if i==loser else 0
                n=min(t.units-floor,b.limits.net+t.side*b.net)
                if n>0:
                    if not self.execute((Intent(-t.side,n,i),)):
                        return
                    break
            else:
                break
        self.finish=not b.gross and not v.active


def strict_replay(c,paths):
    outcomes=[]
    for scenario in paths:
        cy=StrictCoreCycle(c.name,scenario.orientation,c.limits,c.p)
        mid=0
        for t in range(c.limits.horizon+1):
            cy.step(t,scenario.quote(t,mid))
            if cy.finish:
                break
            if t<c.limits.horizon:
                mid+=scenario.moves[t]
        outcomes.append(cy.result())
    return outcomes


def main():
    comp={r["label"]:r for r in load("COMPARISON_RESULTS")}
    paths=list(sample(*TEST))
    matched=[]
    outcomes={}
    for name in ("A3-selected","M-selected"):
        for h in (8,12):
            c=configured(comp[name],h)
            outcomes[name,h]=evaluate(c,paths)
            s=summarize(outcomes[name,h],True)
            assert s["flat"]==len(paths) and not s["risk_violations"], (name,h)
            if h==int(comp[name]["horizon"]):
                assert s["recoveries"]==int(comp[name]["recoveries"])
            matched.append(dict(label=name,horizon=h,**s))
    write("MATCHED_HORIZON",matched)
    half=math.sqrt(2*math.log(40)/len(paths))
    differences=[]
    for h in (8,12):
        a,b=outcomes["A3-selected",h],outcomes["M-selected",h]
        d=(sum(x.success for x in a)-sum(x.success for x in b))/len(paths)
        differences.append(dict(horizon=h,difference=d,lo95=d-half,hi95=d+half))
    write("MATCHED_HORIZON_PAIRED",differences)
    a3=configured(comp["A3-selected"])
    comparison=[dict(mode="Safe",**summarize(outcomes["A3-selected",a3.limits.horizon],True)),
                dict(mode="StrictCoreDiagnostic",**summarize(strict_replay(a3,paths),True))]
    write("CORE_CLOSURE_ABLATION",comparison)
    exact=load("EXHAUSTIVE_RESULTS")
    coverage=Counter()
    for r in exact:
        if r["status"]=="COMPLETE":
            assert int(r["paths"])==5**int(r["horizon"])
            assert int(r["violations"])==int(r["residual"])==0
            assert int(r["flat"])==int(r["paths"])
            coverage[r["label"],r["horizon"]]+=int(r["paths"])
    assert all(coverage[name,"8"]==781250 for name in ("A3-selected","M-selected","K-EXECUTABLE"))
    frontier=load("COST_BUDGET_FRONTIER")
    assert len(frontier)==35
    assert all(not r["policy"] for r in frontier if int(r["cost_budget"])<29)
    compact=[]
    for name,settings in (
        ("no_liquidity",dict(capacity=0)),
        ("spread_before_action",dict(spread=100)),
        ("uncertain_until_deadline",dict(unknown=True)),
    ):
        s=Scenario(1,(0,),name,tuple((t,tuple(settings.items())) for t in (0,1)))
        trace=[]
        outcome=run("K-EXECUTABLE",s,Limits(horizon=1),journal=trace)
        assert outcome.violations
        compact.append(dict(case=name,quote=settings,scenario=asdict(s),
                            outcome=asdict(outcome),journal=trace))
    Path("MINIMAL_COUNTEREXAMPLES.json").write_text(json.dumps(compact,indent=2)+"\n")
    result=dict(compared_policy_rows=len(comp),budget_rows=len(frontier),
                matched_horizon_rows=len(matched),complete_cases=dict((f"{a}/{b}",c)
                for (a,b),c in coverage.items()),minimal_witnesses=len(compact))
    Path("AUDIT_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(result)


if __name__=="__main__":
    main()
