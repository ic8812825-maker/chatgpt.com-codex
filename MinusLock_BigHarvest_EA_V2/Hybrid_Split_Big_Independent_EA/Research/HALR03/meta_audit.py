"""Independent finite action-tree benchmark and delegation parity."""
import csv
from dataclasses import replace
import importlib
import json
from math import fsum
from pathlib import Path

from baseline_audit import source
from a3rc import Params,Memory,target,choose_a3
from execution import Quote
from ledger2 import Limits,Ledger,fee,TICKS
from meta_rc import D,bellman,weights
from risk import gate,close_plan,Envelope

model=importlib.import_module("04_EXECUTION_SIMULATOR")
a3=importlib.import_module("05_A3_ER_POLICY")
meta=importlib.import_module("06_META_ER_POLICY")
MENU=(-40,-20,-10,0,10,20,40)


def small_value(venue,p,m,ctx,mode=None):
    """Exact over the declared finite menu with optimal redecision after each move."""
    b,q,t=venue.book,venue.quote,venue.step
    if b.mark(q)>0 or t==b.limits.horizon:
        return float(b.mark(q)>0)
    candidates = []
    if mode=="heuristic":
        choice=meta.choose_meta(venue,p,m,ctx)
        if choice[3] is not None:
            candidates.append((choice[2],choice[3]))
    else:
        specs = [((),m),(close_plan(b,q),replace(m,exiting=True))]
        if not m.b_mode:
            specs.append((close_plan(b,q),replace(m,b_mode=True)))
        for n in MENU:
            specs.append((target(b,q,n,p.core if not m.b_mode else 0,neutral=p.neutral),m))
        specs.extend((plan,nxt) for _,plan,nxt,_ in a3.er_options(venue,p,m,ctx))
        for plan,nxt in specs:
            trial,_=gate(venue,plan,ctx)
            if trial is not None:
                candidates.append((nxt,trial))
    def value(nxt,trial):
        if nxt.exiting:
            return float(trial.mark(q)>0)
        nxt_values=[]
        for move in D:
            follow=model.Venue(trial.clone())
            follow.quote=q
            follow.advance(t+1,Quote(q.mid+move))
            nxt_values.append(small_value(follow,p,nxt,ctx))
        prev=min(D,key=lambda d:abs(d-(q.mid-venue.previous_mid)))
        return fsum(x*w for x,w in zip(nxt_values,weights(prev)))
    return max((value(nxt,trial) for nxt,trial in candidates),default=0.)


def bellman_table():
    full=[]
    ctx=model.PROFILES["E0"]
    for orientation in (-1,1):
        for budget in (100,180,250):
            for start in (0,150,-150):
                b=Ledger(orientation,Limits(loss=budget,horizon=2))
                v=model.Venue(b)
                v.quote=Quote(0)
                v.advance(0,Quote(start))
                p=Params(trigger=0,net=20,depth=2)
                m=Memory()
                true=small_value(v,p,m,ctx)
                scored=small_value(v,p,m,ctx,"heuristic")
                reduced=bellman(2,b.mark(v.quote),b.net,start,budget*TICKS,p.net,-1,
                                2*fee(v.quote,b.limits))[0]
                assert scored <= true+1e-12
                full.append(dict(orientation=orientation,budget=budget,first_mid=start,
                                 reduced_at_current_net=reduced,full_menu=true,
                                 heuristic_root_then_full=scored,root_regret=true-scored))
    return full


def parity():
    from meta_rc import choose_b,choose_k
    check=[]
    for label,sel in [("A3-ER",a3.choose_er),("B4-RC",choose_b),("K-EXECUTABLE",choose_k)]:
        count=0
        for path in [(300,)*6,(0,)*6,(-300,300)*3,(150,150,-150,300,0,-300)]:
            for orientation in (-1,1):
                c=model.Case(orientation,path)
                kwargs=dict(limits=Limits(horizon=6),params=Params())
                if label=="A3-ER":
                    kwargs["contract"]=model.PROFILES["E0"]
                a,b=[],[]
                u=model.replay(label,c,**kwargs,selector=sel,journal=a)
                # Both paths use the same runtime identity, including K's initial EXIT.
                def delegate(v,p,m,e):
                    return meta.DELEGATES[label](v,p,m,e)
                r=model.replay(label,c,**kwargs,selector=delegate,journal=b)
                assert (u,a)==(r,b)
                count+=1
        check.append(dict(delegate=label,identical_paths=count))
    return check


if __name__=="__main__":
    rows=bellman_table()
    with Path("06_BELLMAN_GAP_ANALYSIS.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    Path("06_DELEGATE_PARITY.json").write_text(json.dumps(parity(),indent=2)+"\n")
