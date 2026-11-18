"""Verify immutable baselines, decision freeze, paired identity, and money oracle."""
from collections import Counter
from csv import DictReader
from gzip import open as gzopen
import importlib
import json
from pathlib import Path
import unittest
import sys

from holdout import read_frozen
from replay import quote,run
from learning import read,rdb
from economic_audit import audit

money=importlib.import_module("02_MONEY_ORACLE")


def csv(name):
    with open(name+".csv") as f:
        return list(DictReader(f))


def checked():
    model,freeze=read_frozen()
    a=json.loads(Path("01_REPRODUCTION_RESULTS.json").read_text())
    assert all(v for v in a["hash_comparison"].values())
    assert a["e1"]["n"]=="1800" and a["e1"]["recoveries"]=="1434"
    p=csv("08_PAIRED_RESULTS")
    assert len(p)==216
    assert all(int(r["flat"])<=int(r["n"]) and int(r["recoveries"])<=int(r["flat"])
               and int(r["paired_flat"])<=int(r["flat"]) for r in p)
    with gzopen("08_PRIMARY_PATHS.csv.gz","rt") as f:
        paths=list(DictReader(f))
    active=[r for r in paths if r["mode"]=="quote_fill" and r["policy"]=="K-EXECUTABLE"]
    assert len(active)==69
    assert Counter(r["violations"] for r in active)==Counter({"MARGIN":28,"":41})
    assert not_invalid(paths)
    s=csv("09_STRESS_MATRIX")
    assert len(s)==9*88
    assert all(n==88 for n in Counter(r["policy"] for r in s).values())
    final=csv("08_FEASIBLE_SUBGROUP")
    assert all(r["n"]=="41" for r in final)
    h=json.loads(Path("03_DATA_QUALITY_REPORT.json").read_text())
    assert len(h)==14 and sum(r["valid"] for r in h)==33839492
    return dict(results_rows=len(p),historical_primary_rows=len(paths),archive_stress_rows=len(s),
                valid_ticks=sum(r["valid"] for r in h),market_archives=len(h),initial_margin_failures=28)


def not_invalid(rows):
    return all((r["delta"]!="")== (r["flat"]=="True" and r["k_flat"]=="True") for r in rows)


def historical_reconciliation(folder):
    e_list=[e for e in read(folder) if e["fold"]=="final_test" and
            e["scheme"]=="S2" and e["interval"]==30]
    model,_=read_frozen()
    counters=Counter()
    for e in e_list:
        anchor=quote(e["entry"],0,"quote_fill")
        for mode in ("quote_fill","delayed_partial","compound_stress"):
            table=model["S2/30/"+mode]
            for name in ("A3-ER","M-ER","K-EXECUTABLE","RDB-3","RDB-4"):
                trace=[]
                r=run(e,name,mode,rdb.RDBCycle,table,trace)
                o=money.MoneyOracle(e["orientation"],initial_entry=anchor.mid,
                                    initial_spread=anchor.spread).replay(trace)
                assert abs(o.mark()/200-r["pnl"])<1e-8
                assert o.flat==r["flat"] and len(o.active)==r["pending"]
                assert o.exposure()[0]/100==r["residual"]
                assert abs(o.actual_incremental_cost/200-r["cost"])<1e-8
                counters["historical_reconciled_paths"]+=1
                counters["historical_reconciled_fills"]+=sum(x["event"]=="FILL" for x in trace)
    return dict(counters)


if __name__=="__main__":
    suite=unittest.defaultTestLoader.discover(".")
    tests=unittest.TextTestRunner(verbosity=2).run(suite)
    data=checked()
    if len(sys.argv)>1:
        data.update(historical_reconciliation(sys.argv[1]))
    nominal=audit()
    data["archived_reconciled_fills"]=sum(r["fills"] for r in nominal.values())
    data["contract_verified"]=True
    Path("AUDIT_RESULTS.json").write_text(json.dumps(data,indent=2)+"\n")
    Path("TEST_RESULTS.json").write_text(json.dumps(
        dict(tests=tests.testsRun,passed=tests.wasSuccessful(),failures=len(tests.failures),
             errors=len(tests.errors)),indent=2)+"\n")
    if not tests.wasSuccessful():
        raise SystemExit(1)
    print(data)
