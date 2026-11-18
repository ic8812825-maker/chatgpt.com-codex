"""Finite supported-path checks and explicit counterexamples."""
import csv
import importlib
from itertools import product
import json
from pathlib import Path
from dataclasses import asdict,replace

from replay import limits,venue,Quote,Params
from economic_audit import ArchivedCase
from scenarios2 import stress
rdb=importlib.import_module("06_RDB_POLICY")
risk=importlib.import_module("07_RISK_GATE")


def simulation(profile,h,moves,extreme=False,orientation=1,show=False):
    l=replace(limits(),horizon=h)
    case=venue.Case(orientation,moves,profile)
    trace=[] if show else None
    cy=rdb.RDBCycle("RDB-1",dict(orientation=orientation,
                  contract=profile,features=dict(spread=20,range30=50,momentum=300)),{},l,trace)
    mid=0
    for t in range(h+1):
        q=case.quote(t,mid)
        if extreme and t and profile in ("E1","E2"):
            q=replace(q,spread=32,slip=2,carry=1)
        cy.step(t,q)
        if cy.finish:
            break
        if t<h:
            mid+=case.next_move(t,cy.book.net)
    return cy.result(),trace


def bounded():
    results={}
    for profile in ("E0","E1","E2"):
        tested=0
        for h in (3,4):
            for s in (-1,1):
                for moves in product((-300,0,300),repeat=h):
                    result,_=simulation(profile,h,moves,extreme=True,orientation=s)
                    assert result.flat and not result.violations, (profile,h,s,moves,result)
                    tested+=1
        results[profile]=tested
    return results


def witnesses():
    out=[]
    for key,mode in (("liquidity_absent","E6"),("unknown_ends","E3"),
                     ("partial_opposing","E5")):
        for h in range(1,5):
            r,log=simulation(mode,h,(300,)*h,show=True)
            if r.violations:
                out.append(dict(witness=key,profile=mode,horizon=h,
                                variant="RDB-1",outcome=asdict(r),trace=log))
                break
    wanted={"reject_gap","spread","partial","second_reject","delay","stopout_gap"}
    seen=set()
    for s in stress(12):
        if s.name in wanted-seen:
            selector=importlib.import_module("05_A3_ER_POLICY").choose_er
            a=[]
            o=venue.replay("A3-ER",ArchivedCase(s),limits(),Params(),selector,a,venue.PROFILES["E1"])
            q=[]
            k=venue.replay("K-EXECUTABLE",ArchivedCase(s),limits(),Params(),journal=q)
            if o.violations or k.violations:
                seen.add(s.name)
                out.append(dict(witness=s.name,profile="archived",horizon=12,
                                variant="A3-ER" if o.violations else "K-EXECUTABLE",
                                outcome=asdict(o if o.violations else k),
                                k=asdict(k),orientation=s.orientation,moves=s.moves,
                                events=s.events,trace=a if o.violations else q))
    # At least one quote with large spread and a directional partial followed by gap.
    q0=Quote(0,capacity=50)
    c=venue.ExecutionCycle("K-EXECUTABLE",1,replace(limits(),horizon=1),Params(),journal=[])
    c.step(0,q0)
    c.step(1,Quote(4000,spread=100,slip=4,capacity=0))
    out.append(dict(witness="joint_gap_and_spread",profile="outside_envelope",horizon=1,
                    variant="K-EXECUTABLE",outcome=asdict(c.result()),trace=c.v.journal))
    return out


if __name__=="__main__":
    proof=bounded()
    cases=witnesses()
    assert all(c["outcome"]["violations"] for c in cases)
    Path("07_COUNTEREXAMPLES.json").write_text(json.dumps(cases,indent=1)+"\n")
    matrix=[]
    for profile in ("E0","E1","E2","E3","E4","E5","E6","historical"):
        if profile in proof:
            status="PROVEN"
            scope="RDB-0..4, explicit guaranteed service, initially feasible, projected actions"
        elif profile in ("E3","E6"):
            status="VIOLATED"
            scope="required FLAT impossible under stated initial Gross and service"
        elif profile=="E4":
            status="PROVEN"
            scope="EXIT_K only when guaranteed initial full service precedes gap"
        elif profile=="E5":
            status="VIOLATED"
            scope="some finite horizons/paths; general H12 feasibility NOT_PROVEN"
        else:
            status="NOT_PROVEN"
            scope="real prices; assumed, unconfirmed broker fills"
        matrix.append(dict(profile=profile,status=status,scope=scope,short_paths_checked=proof.get(profile,0)))
    with open("07_CERTIFICATE_MATRIX.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(matrix[0]),lineterminator="\n")
        w.writeheader()
        w.writerows(matrix)
    print(dict(bounded=proof,witnesses=len(cases)))
