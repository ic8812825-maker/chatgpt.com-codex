"""Describe the observable start-feasibility subgroup without refitting."""
from csv import DictReader
from pathlib import Path
import sys

from holdout import analyze,read_frozen,summarize
from learning import publish_csv,read,rdb
from replay import Params,initial_state,limits,quote,venue


def activation(e,mode):
    c=venue.ExecutionCycle("A3-ER",e["orientation"],limits(),Params(),
                           envelope=venue.PROFILES["E1"])
    initial_state(c,e)
    c.v.advance(0,quote(e["obs"][0],0,mode))
    risk_flags=rdb.risk.violations(c.book,c.v.quote)
    v,_=rdb.risk.close_assessment(c.v)
    b=rdb.risk.balances(c.book,c.v.quote)
    level=(c.book.limits.capital*200+b["mark"])*c.book.limits.leverage*100 / c.book.margin_numerator(c.v.quote)
    return risk_flags,v,level


if __name__=="__main__":
    mode="quote_fill"
    selected=[e for e in read(sys.argv[1]) if
              e["fold"]=="final_test" and e["scheme"]=="S2" and e["interval"]==30]
    audit=[]
    qualified=[]
    for e in selected:
        flags,close_flags,level=activation(e,mode)
        if not flags and not close_flags:
            qualified.append(e)
        audit.append(dict(id=e["id"],month=e["month"],margin_percent=level,
                          initial_violations="|".join(flags),close_gate="|".join(close_flags),
                          qualified=not (flags or close_flags)))
    publish_csv("08_FEASIBILITY_AT_ACTIVATION.csv",audit)
    model,_=read_frozen()
    x=analyze(qualified,model,(mode,))
    publish_csv("08_FEASIBLE_SUBGROUP.csv",[summarize(*k,r) for k,r in x.items()])
    print(len(qualified),len(selected))
