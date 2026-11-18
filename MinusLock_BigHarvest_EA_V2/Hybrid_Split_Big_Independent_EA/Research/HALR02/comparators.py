"""Decision-rule ports; all orders are confirmed by the HALR-02 Venue."""
from dataclasses import replace
from functools import lru_cache

from a3rc import Params, sign, target
from ledger2 import TICKS, fee
from meta_rc import D, choose_m, weights
from risk import close_plan, project

A3 = Params(trigger=140)
B4 = Params(core=100,net=25,trigger=75,harvest=25,switches=6,reserve=15)
J = Params(net=12,trigger=140,attempts=1)


def exit_now(m):
    return "SAFE",None,replace(m,exiting=True),None


def original_a3(v,p,m,env):
    b,q=v.book,v.quote
    if b.mark(q)-600*abs(b.net)-p.reserve*TICKS < -b.limits.loss*TICKS:
        return exit_now(m)
    move=q.mid-m.anchor
    if abs(move)>=p.trigger and m.switches<p.switches:
        plan=target(b,q,sign(move)*p.net,p.core,neutral=True)
        if plan is not None:
            return "ORIGINAL_A3",plan,replace(m,anchor=q.mid,switches=m.switches+1),None
    elif b.net and any(not t.original and t.side*(q.mid-t.entry)>p.trigger for t in b.tickets.values()):
        plan=target(b,q,round(b.net*(1-p.harvest/100)),p.core)
        if plan is not None:
            return "ORIGINAL_HARVEST",plan,m,None
    return "HOLD",(),m,None


def original_b4(v,p,m,env):
    b,q=v.book,v.quote
    if b.mark(q)-600*abs(b.net)-p.reserve*TICKS < -b.limits.loss*TICKS:
        return exit_now(m)
    if not m.b_mode:
        return "INITIAL_CLOSE",close_plan(b,q) or (),replace(m,b_mode=True),None
    move=q.mid-m.anchor
    if b.net:
        good=sign(b.net)*move
        if good<=-p.trigger/2:
            return "STOP",close_plan(b,q) or (),replace(m,anchor=q.mid),None
        if good>=p.trigger:
            plan=target(b,q,round(b.net*(1-p.harvest/100)))
            return "HARVEST",plan or (),replace(m,anchor=q.mid),None
    elif m.attempts<p.attempts and abs(move)>=p.trigger:
        return "OPEN",target(b,q,sign(move)*p.net) or (),replace(m,attempts=m.attempts+1,anchor=q.mid),None
    return "WAIT",(),m,None


def balanced(v,p,m,env):
    b,q=v.book,v.quote
    if not m.b_mode:
        return "INITIAL_CLOSE",close_plan(b,q) or (),replace(m,b_mode=True),None
    desired=b.net
    if not m.attempts and abs(q.mid)>=p.trigger:
        desired=sign(q.mid)*p.net
    # Historical comparison gate expressed in exact half-cents.
    mark=b.mark(q)
    future=mark-2*abs(desired-b.net)*(q.spread+q.slip+9)-2*abs(desired)*648
    margin=abs(desired)*(110000+q.mid+650)/3000
    if future<-180*TICKS or b.limits.capital+future/TICKS < 2*margin:
        return exit_now(m)
    if desired!=b.net:
        return "J_ENTRY",target(b,q,desired) or (),replace(m,attempts=1),None
    return "J_HOLD",(),m,None


@lru_cache(maxsize=100000)
def old_prob(depth,mark,net,original,last,size,budget):
    best=float(mark>0)
    if best or not depth:
        return best
    action=[(net, original,0),(0,False,0)]
    if not original:
        for n in (-size,size):
            opened=abs(n) if n*net<=0 else max(0,abs(n)-abs(net))
            action.append((n,False,58*opened))
    for n,a,c in action:
        if mark-c-600*abs(n)>=-budget:
            values=[old_prob(depth-1,mark-c+2*n*d,n,a,d,size,budget) for d in D]
            best=max(best,sum(v*w for v,w in zip(values,weights(last))))
    return best


def original_m(v,p,m,env):
    b,q=v.book,v.quote
    a=any(t.original for t in b.tickets.values())
    close=close_plan(b,q)
    opts=[("HOLD" if b.gross else "WAIT",(),m),("K_EXIT",close,replace(m,exiting=True))]
    if a:
        opts.append(("SWITCH_B",close,m))
    for s in (-b.orientation,b.orientation):
        opts.append(("RESIZE",target(b,q,s*p.net),m))
        if a:
            # Preserve both inherited tickets by submitting only the increment.
            from execution import Intent
            change=s*p.net-b.net
            opts.append(("WORKING",(Intent(sign(change),abs(change)),) if change else (),m))
    if b.net:
        opts.extend((("NEUTRAL",target(b,q,0),m),("HARVEST",target(b,q,round(b.net/2)),m)))
    depth=min(2,b.limits.horizon-v.step)
    last=min(D,key=lambda d:abs(d-(q.mid-v.previous_mid)))
    cap=(b.limits.loss-p.reserve)*TICKS
    best=None
    for label,plan,nxt in opts:
        trial=project(b,q,plan)
        if trial is None:
            continue
        mark=trial.mark(q)
        if trial.gross and mark-600*abs(trial.net)<-cap:
            continue
        original=any(t.original for t in trial.tickets.values())
        if nxt.exiting:
            prob=float(mark>0)
        else:
            prob=sum(old_prob(depth-1,mark+2*trial.net*d,trial.net,original,d,p.net,cap)*w
                     for d,w in zip(D,weights(last)))
        key=(prob,-trial.gross,-trial.spent,-abs(trial.net),not nxt.exiting)
        if best is None or key>best[0]:
            best=key,(label,plan,nxt,trial)
    return best[1] if best else exit_now(m)


SETTINGS = {"A3-original":(A3,original_a3), "M-original":(A3,original_m),
            "B4":(B4,original_b4), "J-Balanced":(J,balanced), "M-RC":(Params(),choose_m)}
