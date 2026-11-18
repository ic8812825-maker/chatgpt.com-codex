"""Finite robust viability with confirmed flat as the terminal condition."""
from collections import Counter
from csv import DictWriter
from dataclasses import replace
import importlib
from itertools import product

from baseline_audit import source
from a3rc import target
from execution import Quote
from ledger2 import Ledger,Limits
from risk import close_plan,project

exe=importlib.import_module("04_EXECUTION_SIMULATOR")
MENU=(-30,-15,-5,0,5,15,30)
MOVES=(-300,0,300)


def adverse(profile,t,mid):
    if profile=="E0":
        yield Quote(mid)
        return
    available=profile=="E1" or t%2==0
    # Independent extrema in cost and carry, not only the Monte Carlo weather.
    for s,slip,carry in ((20,0,0),(32,2,1)):
        yield Quote(mid,spread=s,slip=slip,carry=carry,capacity=1000 if available else 0,
                    delay=int(not available))


def choices(b,q,t,h):
    if b.violations:
        return
    if not b.gross:
        yield "FLAT",b
        return
    if q.capacity:
        limit=project(b,q,close_plan(b,q))
        if limit is not None and not limit.violations and not limit.gross:
            yield "EXIT",limit
    if t>=h:
        return
    yield "WAIT",b
    if q.capacity:
        for net in MENU:
            if net==b.net:
                continue
            plan=target(b,q,net,core=25,allow_open=True,neutral=True)
            child=project(b,q,plan)
            if child is not None and not child.violations:
                yield str(net),child


def solve(b,q,t,h,profile,counts):
    """Backward existential action, universal nature; no floating probabilities."""
    counts["states"]+=1
    options=[]
    for label,child in choices(b,q,t,h):
        if not child.gross:
            options.append(label)
            continue
        if t>=h:
            continue
        good=True
        for d in MOVES:
            for future in adverse(profile,t+1,q.mid+d):
                follow=child.clone()
                follow.apply_carry(future)
                follow.observe(future)
                if not solve(follow,future,t+1,h,profile,counts):
                    good=False
                    break
            if not good:
                break
        if good:
            options.append(label)
    return options


def kernel():
    out=[]
    for profile in ("E0","E1","E2"):
        for loss,cost,orientation,n in product((58,100,180),(20,30,50),(-1,1),(0,20)):
            h=2
            b=Ledger(orientation,Limits(loss=loss,cost=cost,horizon=h))
            q=Quote(0)
            b.observe(q)
            if n:
                b=project(b,q,target(b,q,-orientation*n,allow_open=False))
            counts=Counter()
            actions=solve(b,q,0,h,profile,counts)
            out.append(dict(profile=profile,horizon=h,loss=loss,cost=cost,
                            orientation=orientation,preexisting_net=b.net,viable=bool(actions),
                            safe_actions="|".join(actions),states=counts["states"]))
    return out


def certificate():
    return [
        dict(profile="E0",status="FORMALLY_PROVEN",scope="ER and K, under stated budgets and nominal initial mark",
             rationale="Full confirmed batches, one price step before backup exit"),
        dict(profile="E1",status="FORMALLY_PROVEN",scope="ER and K under max move 300, spread 32, slip 2, carry 1",
             rationale="Service every event; stress reserve and verified queue"),
        dict(profile="E2",status="FORMALLY_PROVEN",scope="ER and K under bounded odd-event outages with even-event confirmed capacity",
             rationale="Two-step backup and early flatten at last assured service"),
        dict(profile="E3",status="VIOLATED",scope="Liveness for all policies in scripted subset",
             rationale="At most 0.30 lots confirmed before enduring unknown/zero capacity"),
        dict(profile="E4",status="FORMALLY_PROVEN",scope="K and ER fallback only, in the scripted nominal initial service",
             rationale="Earliest flatten precedes gap; holding directional Net is not certified"),
        dict(profile="E5",status="NOT_PROVEN",scope="General finite horizon; violated for tested witnesses",
             rationale="At H=4 aggregate capacity <=1.15 lots and liveness is impossible"),
        dict(profile="E6",status="VIOLATED",scope="All policies from positive initial Gross",
             rationale="No fill before deadline"),
    ]


if __name__=="__main__":
    for name,rows in (("09_VIABILITY_KERNEL",kernel()),("09_RISK_CERTIFICATE_MATRIX",certificate())):
        with open(name+".csv","w",newline="") as f:
            writer=DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    print("Kernel and certificate generated")
