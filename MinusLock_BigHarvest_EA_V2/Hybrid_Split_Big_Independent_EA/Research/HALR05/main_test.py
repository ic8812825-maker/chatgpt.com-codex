"""Run the preregistered primary contrast on all eligible activations."""
from collections import Counter
from csv import DictReader
from gzip import compress
import importlib
import json
from pathlib import Path
from statistics import mean,median
import sys

from inference import decide,summary,tail
from sim import CFG,run
io=importlib.import_module("04_CAUSAL_REPLAY")


def flatten_row(e,mode,policy,out,oracle):
    return dict(month=e["month"],id=e["id"],complete=e["complete"],mode=mode,
                policy=policy,**{k:out[k] for k in (
                    "pnl","flat","success","low","gross","net","margin","cost",
                    "cost_with_reserve","residual","pending","violations","failures","elapsed_ms","quote_events",
                    "attempts")},
                final_net=oracle["end_net"],exit_reserve=oracle["reserve_exit"],
                confirmed_fills=oracle["verified_fills"])


def aggregate(mode,name,rows,counts=None):
    n=len(rows)
    f=[r for r in rows if r["flat"]]
    realized=[r["pnl"] for r in f]
    losses=[-p for p in realized]
    return dict(mode=mode,policy=name,n=n,clusters=len({x["month"] for x in rows}),
                **(counts or {}),
                recovered=sum(r["success"] for r in rows),
                recovery_rate=sum(r["success"] for r in rows)/n if n else None,
                flat=len(f),flat_rate=len(f)/n if n else None,
                violations=sum(bool(r["violations"]) for r in rows),
                mean_realized=mean(realized) if f else None,
                median_realized=median(realized) if f else None,
                cvar95_realized=tail(losses,.95),cvar99_realized=tail(losses,.99),
                mean_mark=mean(r["pnl"] for r in rows) if n else None,
                cvar99_all_marks=tail([-r["pnl"] for r in rows],.99),
                worst_mark=min((r["pnl"] for r in rows),default=None),
                worst_low=min((r["low"] for r in rows),default=None),
                worst_realized=min(realized,default=None),
                mean_paid=mean(r["cost"] for r in rows) if n else None,
                max_expense_and_reserve=max((r["cost_with_reserve"] for r in rows),default=None),
                max_gross=max((r["gross"] for r in rows),default=None),
                max_abs_net=max((r["net"] for r in rows),default=None),
                max_abs_final_net=max((abs(r["final_net"]) for r in rows),default=None),
                max_margin_equity=max((r["margin"] for r in rows),default=None),
                mean_flat_ms=mean(r["elapsed_ms"] for r in f) if f else None,
                residual_count=sum(r["residual"]>0 for r in rows),
                pending_count=sum(r["pending"]>0 for r in rows),
                execution_failures=sum(r["failures"] for r in rows))


def paired(m,k):
    return dict(month=m["month"],id=m["id"],complete=m["complete"],
                m_pnl=m["pnl"],k_pnl=k["pnl"],m_flat=m["flat"],k_flat=k["flat"],
                delta=m["pnl"]-k["pnl"] if m["flat"] and k["flat"] else None,
                m_violations=m["violations"],k_violations=k["violations"])


def eligible(folder):
    io.months()
    p=Path(folder)/"eligible.json"
    doses=json.loads(p.read_text())
    assert len({e["id"] for e in doses})==len(doses)
    assert {e["month"] for e in doses}.issubset(CFG["calendar"])
    with open("04_EPISODE_LEDGER.csv") as f:
        recorded={r["id"] for r in DictReader(f) if r["eligible"]=="True"}
    assert recorded=={e["id"] for e in doses}
    return doses


def main(folder):
    c=eligible(folder)
    mode=CFG["primary_mode"]
    series={p:[] for p in ("M-ER","K-EXECUTABLE")}
    trace_manifest=[]
    for e in c:
        for name in series:
            a,t,v=run(e,name,mode)
            series[name].append(flatten_row(e,mode,name,a,v))
            trace_manifest.append(dict(id=e["id"],policy=name,journal=t,oracle=v))
    with open("04_EPISODE_LEDGER.csv") as f:
        ledger=list(DictReader(f))
    counts=Counter(r["status"] for r in ledger)
    counts={"potential":len(ledger),"activated":counts["ELIGIBLE"]+counts["EXCLUDED"],
            "eligible":counts["ELIGIBLE"],"excluded":counts["EXCLUDED"],
            "incomplete_eligible":sum(not e["complete"] for e in c)}
    pairs=[paired(m,k) for m,k in zip(series["M-ER"],series["K-EXECUTABLE"],strict=True)]
    statistics=summary(pairs,CFG["bootstrap"])
    n_archives=sum("valid" in r for r in json.loads(Path("04_DATA_QUALITY.json").read_text()))
    d=decide(pairs,statistics,CFG,n_archives)
    d["statistics"]=statistics
    d["selection"]=counts
    io.json_out("07_CONFIRMATORY_DECISION",d)
    results=[aggregate(mode,name,rows,counts) for name,rows in series.items()]
    for r in results:
        r.update(paired_flat=statistics["paired_flat"],paired_mean=statistics["paired_mean"],
                 paired_lcb95=statistics["month"].get("mean",{}).get("0.05"),
                 paired_ci_low=statistics["month"].get("mean",{}).get("0.025"),
                 paired_ci_high=statistics["month"].get("mean",{}).get("0.975"),
                 max_additional_loss=statistics["worst_extra_loss"])
    io.csv_out("07_PRIMARY_RESULTS",results)
    if pairs:
        io.csv_out("07_PAIRED_RESULTS",pairs)
    else:
        Path("07_PAIRED_RESULTS.csv").write_text("month,id,delta\n")
    events="".join(json.dumps(row,separators=(",",":"))+"\n" for row in trace_manifest)
    Path("07_CONFIRMED_JOURNALS.jsonl.gz").write_bytes(compress(events.encode(),mtime=0))
    print(d["status"], counts, d.get("failed_barriers"))


if __name__=="__main__":
    main(sys.argv[1])
