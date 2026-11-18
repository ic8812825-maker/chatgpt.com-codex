"""Independently check first observations, frozen sources, and economic identities."""
from bisect import bisect_left
from collections import Counter,defaultdict
from csv import DictReader
from decimal import Decimal
from hashlib import sha256
import importlib
import json
from pathlib import Path
import sys

from pinned import setup,PINS
paths=setup()
import data_scan
from data_scan import DAY,MINUTE,T0,load_ticks
from inference import summary,decide
from sim import CFG
from baseline_check import hashes

io=importlib.import_module("04_CAUSAL_REPLAY")
data_checks=importlib.import_module("data_checks")


def read(name):
    with open(name+".csv") as f:
        return list(DictReader(f))


def firsts(folder,ledger):
    months=defaultdict(list)
    for r in ledger:
        months[r["month"]].append(r)
    from datetime import date
    tested=0
    present={r["month"] for r in json.loads(Path("04_DATA_QUALITY.json").read_text()) if "valid" in r}
    for month,rows in months.items():
        if month not in present:
            assert all(r["status"]=="ARCHIVE_MISSING" for r in rows)
            continue
        ts,b,a=load_ticks(folder,month)
        for r in rows:
            day=date.fromisoformat(r["id"]).toordinal()-T0
            start=day*DAY+480*MINUTE
            stop=day*DAY+840*MINUTE
            idx=bisect_left(ts,start)
            if idx==len(ts) or ts[idx]>=start+5*MINUTE:
                assert r["status"]=="NO_ANCHOR"
                continue
            assert [ts[idx]+18000000,b[idx],a[idx]]==[
                int(r[k]) for k in ("anchor_utc_ms","anchor_bid","anchor_ask")]
            mid=b[idx]+a[idx]
            j=idx+1
            while j<len(ts) and ts[j]<stop and abs(b[j]+a[j]-mid)<600:
                j+=1
            if j==len(ts) or ts[j]>=stop:
                assert r["status"]=="NO_ACTIVATION"
            else:
                assert (ts[j]+18000000,b[j],a[j])==tuple(
                    int(r[k]) for k in ("activation_utc_ms","activation_bid","activation_ask"))
                assert r["status"] in ("ELIGIBLE","EXCLUDED")
            tested+=1
    return tested


def pareto(execution):
    rows=[]
    modes={r["mode"] for r in execution}
    for mode in sorted(modes):
        ref={r["policy"]:r for r in execution if r["mode"]==mode}
        for name,x in ref.items():
            ok=x["flat"]==x["n"] and x["violations"]=="0"
            vals=(float(x["mean_realized"]),-float(x["cvar99_realized"]),
                  float(x["worst_realized"]),-float(x["mean_paid"]),float(x["flat_rate"]),
                  -float(x["execution_failures"])) if ok else ()
            dominates=False
            if vals:
                for n,r in ref.items():
                    if n==name or r["flat"]!=r["n"] or r["violations"]!="0":
                        continue
                    y=(float(r["mean_realized"]),-float(r["cvar99_realized"]),
                       float(r["worst_realized"]),-float(r["mean_paid"]),float(r["flat_rate"]),
                       -float(r["execution_failures"]))
                    dominates|=y!=vals and all(b>=a for a,b in zip(vals,y))
            k=ref["K-EXECUTABLE"]
            rows.append(dict(mode=mode,policy=name,mean_pnl=x["mean_realized"],
                             cvar99=x["cvar99_realized"],worst=x["worst_mark"],
                             cost=x["mean_paid"],flat=x["flat"],n=x["n"],
                             execution_failures=x["execution_failures"],violations=x["violations"],
                             cvar99_added_vs_k=float(x["cvar99_realized"])-float(k["cvar99_realized"])
                               if x["cvar99_realized"] and k["cvar99_realized"] else "",
                             eligible_frontier="INADMISSIBLE" if not vals else
                                               "DOMINATED" if dominates else "NONDOMINATED"))
    return rows


def audit(folder):
    io.months()
    assert hashes(paths)==json.loads(Path("01_DEPENDENCY_HASHES.json").read_text())
    for n,h in json.loads(Path("06_ADAPTER_HASHES.json").read_text()).items():
        assert sha256(Path(n).read_bytes()).hexdigest()==h,n
    previous=json.loads(Path("03_HOLDOUT_MANIFEST.json").read_text())["previous_historical_months"]
    assert set(CFG["calendar"]).isdisjoint(previous)
    data=data_checks.check(folder)
    ledger=read("04_EPISODE_LEDGER")
    n=firsts(folder,ledger)
    rows=read("07_PAIRED_RESULTS")
    assert len(rows)==data["eligible"]
    assert {x["id"] for x in rows}=={r["id"] for r in ledger if r["eligible"]=="True"}
    for r in rows:
        settled=r["m_flat"]==r["k_flat"]=="True"
        assert settled==bool(r["delta"])
        if settled:
            assert abs(Decimal(r["m_pnl"])-Decimal(r["k_pnl"])-Decimal(r["delta"])) < Decimal("1e-10")
    reported=json.loads(Path("07_CONFIRMATORY_DECISION.json").read_text())
    numeric=[{**r,"m_pnl":float(r["m_pnl"]),"k_pnl":float(r["k_pnl"]),
              "delta":float(r["delta"]) if r["delta"] else None} for r in rows]
    s=summary(numeric,CFG["bootstrap"])
    assert s==reported["statistics"]
    assert decide(numeric,s,CFG,data["archives"])["status"]==reported["status"]
    archive=read("08_STRESS_RESULTS")
    assert all(count==88 for count in Counter(r["policy"] for r in archive).values())
    io.csv_out("09_ECONOMIC_FRONTIER",pareto(read("08_EXECUTION_MATRIX")))
    return dict(passed=True,source_pins=PINS,previous_month_overlap=0,locked_hashes_verified=True,
                first_observation_checks=n,primary_rows=len(rows),archived_stress_rows=len(archive),
                primary_cluster_statistics_reproduced=True,**data)


if __name__=="__main__":
    a=audit(Path(sys.argv[1]))
    io.json_out("09_INDEPENDENT_AUDIT",a)
    print(a)
