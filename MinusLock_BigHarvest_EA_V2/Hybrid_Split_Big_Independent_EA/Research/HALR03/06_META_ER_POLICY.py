"""Meta policy, with exact named delegates and a reduced Bellman ranking."""
from dataclasses import replace
import importlib
from math import fsum

from pinned import source
source()
from meta_rc import D,bellman,choices_b4,choose_b,choose_k,weights
from ledger2 import fee,TICKS
from risk import gate

a3=importlib.import_module("05_A3_ER_POLICY")
DELEGATES={"A3-ER":a3.choose_er,"B4-RC":choose_b,"K-EXECUTABLE":choose_k}


def choose_meta(v,p,m,env):
    ctx=a3.context(v,env)
    if ctx is None or not a3.observed_contract(v,env):
        return "SAFE",None,replace(m,exiting=True),None
    if v.step%env.stride:
        return a3.choose_er(v,p,m,env)
    q,b=v.quote,v.book
    if m.b_mode:
        options=[]
        for label,plan,nxt in choices_b4(v,p,m):
            trial,_=gate(v,plan,ctx)
            if trial is not None:
                options.append((label,plan,nxt,trial))
    else:
        options=list(a3.er_options(v,p,m,env))
        switch=a3.er_close(v,p,m,env,keep_running=True)
        if switch:
            options.append(switch)
    close=a3.er_close(v,p,m,env)
    if close:
        options.append(close)
    prev=min(D,key=lambda x:abs(x-(q.mid-v.previous_mid)))
    depth=min(p.depth,b.limits.horizon-v.step)
    best=None
    for label,plan,nxt,trial in options:
        mark=trial.mark(q)
        score=float(mark>0),float(mark)
        if not nxt.exiting and depth:
            rem=trial.limits.cost*TICKS-trial.spent-trial.exit_cost(q)
            allowance=rem if nxt.b_mode and nxt.attempts<p.attempts else -1
            values=[bellman(depth-1,mark+2*trial.net*d,trial.net,d,
                            (b.limits.loss-p.reserve)*TICKS,p.net,allowance,
                            2*fee(q,b.limits)) for d in D]
            score=tuple(fsum(x[i]*w for x,w in zip(values,weights(prev))) for i in (0,1))
        key=(*score,-trial.spent-trial.exit_cost(q),-abs(trial.net))
        if best is None or key>best[0]:
            best=key,(label,plan,nxt,trial)
    return best[1] if best else ("SAFE",None,replace(m,exiting=True),None)
