"""Historical observation and shared confirmed execution for frozen policies."""
from dataclasses import asdict,replace
import importlib
import json
from pathlib import Path

from dependencies import setup
setup()
from a3rc import Params
from execution import Quote
from ledger2 import Limits
from meta_rc import choose_b
from runner import ideal

venue=importlib.import_module("04_EXECUTION_SIMULATOR")
a3=importlib.import_module("05_A3_ER_POLICY")
meta=importlib.import_module("06_META_ER_POLICY")
C=json.loads(Path(__file__).with_name("contract.json").read_text())
FILL_MODELS=("quote_fill","bounded_slip","delayed_partial","compound_stress")
DEFAULTS={"A3-ER":a3.choose_er,"M-ER":meta.choose_meta,
          "K-EXECUTABLE":None,"K-IDEAL":None}


def limits():
    return Limits(loss=C["full_loss_usd"],cost=C["new_cost_usd"],
                  net=C["max_net_units"],gross=C["max_gross_units"],
                  capital=C["capital"],leverage=C["leverage"],margin_level=C["margin_level_bps"],
                  stopout=C["stopout_bps"],commission=C["commission_half_cents_per_unit_one_side"],
                  horizon=C["horizon"])


def quote(record,t,mode):
    stamp,bid,ask=record
    q=Quote((bid+ask)/2-110000,spread=ask-bid)
    if mode=="bounded_slip":
        q=replace(q,slip=2)
    elif mode=="delayed_partial":
        q=replace(q,slip=2,delay=int(t%3==0),capacity=25 if t%3==0 else 1000,
                  rejects=int(t==2),unknown=t==10)
    elif mode=="compound_stress":
        q=replace(q,spread=ask-bid+(40 if t>=3 else 0),slip=4,
                  delay=int(t%3==0),capacity=25 if t<6 else 0,
                  rejects=int(t==2),unknown=t>=8)
    elif mode!="quote_fill":
        raise ValueError(mode)
    return q


def initial_state(c,episode):
    q0=quote(episode["entry"],0,"quote_fill")
    c.book.tickets={i:replace(t,entry=q0.mid) for i,t in c.book.tickets.items()}
    c.book.initial_cost=(q0.spread+c.book.limits.commission)*C["initial_gross_units"]
    c.memory=replace(c.memory,anchor=quote(episode["obs"][0],0,"quote_fill").mid)


def run(episode,policy,mode="quote_fill",rdb_class=None,trained=None,journal=None):
    l=limits()
    if policy=="K-IDEAL":
        q0=quote(episode["entry"],0,"quote_fill")
        q1=quote(episode["obs"][0],0,"quote_fill")
        cost=q1.spread+l.commission
        mark=-(q0.spread+l.commission)-cost
        r=asdict(ideal(l))
        r.update(pnl=mark,low=mark,drawdown=-mark,cost=cost,cost_with_reserve=cost,
                 violations=("COST" if cost>l.cost else "")+("|LOSS" if -mark>l.loss else ""),
                 elapsed_ms=0,quote_events=1,attempts=0,decision="ANALYTIC")
        return r
    trace=[] if journal is None else journal
    if policy.startswith("RDB-") and policy!="RDB-0":
        c=rdb_class(policy,episode,trained,l,trace)
    else:
        name="K-EXECUTABLE" if policy=="RDB-0" else policy
        kw={"envelope":venue.PROFILES["E1"]} if name.endswith("-ER") else {}
        c=venue.ExecutionCycle(name,episode["orientation"],l,Params(),selector=DEFAULTS[name],
                               journal=trace,**kw)
    initial_state(c,episode)
    for t,rec in enumerate(episode["obs"]):
        c.step(t,quote(rec,t,mode))
        if c.finish:
            break
    result=asdict(c.result())
    result.update(elapsed_ms=episode["obs"][t][0]-episode["obs"][0][0],quote_events=t+1,
                  attempts=sum(e["event"]=="CREATED" for e in trace),
                  decision=getattr(c,"initial_decision",policy if policy!="RDB-0" else "EXIT_K"))
    return result
