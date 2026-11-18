"""Independent cash-flow replay, boundary probes, and full tiny trees."""
import importlib
from itertools import product
import json
from pathlib import Path

from pinned import source
source()
from execution import Intent, Quote, Venue
from ledger2 import Ledger, Limits
from risk import Envelope, gate, reservations
from runner import Cycle
from a3rc import Params
from comparators import SETTINGS
from exhaustive2 import exact, brute
from scenarios2 import stress

Oracle = importlib.import_module("02_MONEY_ORACLE").Oracle


def reconcile(journal, orientation):
    o = Oracle(orientation)
    n = 0
    for event in journal:
        if event["event"] == "QUOTE":
            mid,spread,slip=(event[k] for k in ("mid","spread","slip"))
            if event["step"]:
                o.carry(event["carry"])
        if event["event"] == "FILL":
            o.confirmed(event["side"],event["units"],event["ticket"],mid,spread,slip)
            assert o.liquidation(mid,spread,slip)==event["pnl"], event
            assert sum(leg.amount for leg in o.legs.values())==event["gross"]
            assert sum(leg.amount*leg.side for leg in o.legs.values())==event["net"]
            n += 1
    return o.liquidation(mid,spread,slip),n


def scenario_journal(name, p, selector, scenario, limits):
    from runner import run
    log = []
    out = run(name,scenario,limits,p,selector=selector,journal=log)
    return out,log


def audit():
    audits=[]
    for variant,p,sel in [("A3-RC",Params(),None),
                          ("M-RC",*SETTINGS["M-RC"]),
                          ("K-EXECUTABLE",Params(),None)]:
        comparisons=0
        for orientation in (-1,1):
            l=Limits(horizon=3)
            compressed=exact(variant,orientation,p,l,sel)[0]
            direct=brute(variant,orientation,p,l,sel)
            assert compressed==direct and direct.paths==125
            comparisons+=direct.paths
        fills=0
        for s in stress(8):
            result,journal=scenario_journal(variant,p,sel,s,Limits())
            mark,n=reconcile(journal,s.orientation)
            assert mark==round(result.pnl*200)
            fills+=n
        audits.append(dict(variant=variant,direct_tree_paths=comparisons,
                           stress_paths=88,reconciled_fills=fills))

    ledger=Ledger(1,Limits(loss=100,cost=30,horizon=2))
    v=Venue(ledger)
    v.advance(0,Quote(0))
    assert ledger.mark(v.quote)==-11600 and reservations(v,v.quote)==(0,5800,0,200)
    grid=[]
    for n in (0,13,14,15,50):
        plan=(Intent(-1,n,0),) if n else ()
        trial,status=gate(v,plan,Envelope())
        assert (trial is not None)==(n<=14)
        grid.append(dict(net=-n,admitted=trial is not None,result=status))
    v.advance(1,Quote(0,delay=1,unknown=True))
    tracked=v.submit(Intent(1,3),key="known-key")
    assert v.submit(Intent(1,3),key="known-key") is tracked
    assert reservations(v,v.quote)[2]==174 and gate(v,(),Envelope())[1]=="PENDING"
    v.cancel(tracked)
    v.advance(2,Quote(150,cancel_race=True))
    assert ledger.net==3

    return dict(status="PASS",cash_and_tree=audits,loss_gate_boundary=grid,
                pending_open_round_trip_ticks=174,late_fill_units=3)


if __name__=="__main__":
    print(json.dumps(audit(),indent=2))
