"""Admissible A, B and K decisions with a bounded continuation model."""
from dataclasses import replace
from functools import lru_cache
from math import fsum

from a3rc import choices_a3, choose_a3, sign, target
from ledger2 import TICKS, fee
from risk import close_plan, gate

D = (-300,-150,0,150,300)


def weights(previous):
    return tuple((1+5*(d==previous))/10 for d in D)


@lru_cache(maxsize=150000)
def bellman(depth, mark, net, previous, budget, quantum, entry_budget, price):
    """Bellman value in the quotient: hold, stop, or one new entry from flat."""
    if mark>0:
        return 1.,float(mark)
    best = 0.,float(mark)
    if not depth:
        return best

    def continuation(after, exposure, opening):
        if after-600*abs(exposure)<-budget:
            return 0.,float(after)
        values = [bellman(depth-1,after+2*exposure*d,exposure,d,budget,quantum,
                          -1 if opening else entry_budget,price) for d in D]
        return tuple(fsum(v[i]*w for v,w in zip(values,weights(previous))) for i in (0,1))

    best = max(best,continuation(mark,net,False))
    if not net and previous and price*quantum<=entry_budget:
        best = max(best,continuation(mark-price*quantum,sign(previous)*quantum,True))
    return best


def choices_b4(v,p,m):
    b,q = v.book,v.quote
    move = q.mid-m.anchor
    if b.net and b.net*move<=-abs(b.net)*max(1,p.trigger//2):
        yield "B_STOP",close_plan(b,q),replace(m,anchor=q.mid)
    elif b.net and b.net*move>=abs(b.net)*p.trigger:
        n = sign(b.net)*(abs(b.net)*(100-p.harvest)//100)
        plan = target(b,q,n,allow_open=False)
        if plan:
            yield "B_HARVEST",plan,replace(m,anchor=q.mid)
    elif not b.gross and m.attempts<p.attempts and abs(move)>=p.trigger and move:
        plan = target(b,q,sign(move)*p.net)
        if plan:
            yield "B_OPEN",plan,replace(m,anchor=q.mid,attempts=m.attempts+1)
    yield "B_WAIT" if not b.gross else "B_HOLD",(),m


def choose_b(v,p,m,env):
    if not m.b_mode:
        plan = close_plan(v.book,v.quote)
        options = [("SWITCH_B",plan,replace(m,b_mode=True,anchor=v.quote.mid))]
    else:
        options = choices_b4(v,p,m)
    for label,plan,nxt in options:
        trial,_ = gate(v,plan,env)
        if trial is not None:
            return label,plan,nxt,trial
    return "SAFE",None,replace(m,exiting=True),None


def choose_k(v,p,m,env):
    plan=close_plan(v.book,v.quote)
    trial,_=gate(v,plan,env)
    if trial is not None:
        return "K_EXIT",plan,replace(m,exiting=True),trial
    return "SAFE",None,replace(m,exiting=True),None


DELEGATES = {"A3":choose_a3,"B4-RC":choose_b,"K":choose_k}


def choose_m(v,p,m,env):
    b,q = v.book,v.quote
    close=close_plan(b,q)
    options=list(choices_b4(v,p,m) if m.b_mode else choices_a3(v,p,m))
    if not m.b_mode:
        options.append(("SWITCH_B",close,replace(m,b_mode=True,anchor=q.mid)))
    options.append(("K_EXIT",close,replace(m,exiting=True)))
    previous=min(D,key=lambda d:abs(d-(q.mid-v.previous_mid)))
    depth=min(p.depth,b.limits.horizon-p.time_buffer-v.step)
    best=None
    for label,plan,nxt in options:
        trial,_=gate(v,plan,env)
        if trial is None:
            continue
        mark=trial.mark(q)
        score=(float(mark>0),float(mark))
        if not nxt.exiting and depth>0:
            rem=b.limits.cost*TICKS-trial.spent-trial.exit_cost(q)
            future_entry=rem if nxt.b_mode and nxt.attempts<p.attempts else -1
            price=2*fee(q,b.limits)
            outcomes=[bellman(depth-1,mark+2*trial.net*d,trial.net,d,
                              (b.limits.loss-p.reserve)*TICKS,p.net,future_entry,price)
                      for d in D]
            score=tuple(fsum(vv[i]*w for vv,w in zip(outcomes,weights(previous))) for i in (0,1))
        key=(*score,-trial.spent-trial.exit_cost(q),-abs(trial.net))
        if best is None or key>best[0]:
            best=key,(label,plan,nxt,trial)
    if best:
        return best[1]
    return "SAFE",None,replace(m,exiting=True),None
