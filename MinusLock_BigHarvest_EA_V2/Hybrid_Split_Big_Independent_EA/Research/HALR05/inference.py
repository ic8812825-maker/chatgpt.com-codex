"""Calendar-block estimates, chronology sensitivities and fixed decision barriers."""
from collections import defaultdict
from math import ceil
from random import Random
from statistics import mean,median


def tail(losses,p):
    if not losses:return None
    ordered=sorted(losses,reverse=True)
    mass=(1-p)*len(losses)
    i=int(mass)
    return (sum(ordered[:i])+(mass-i)*ordered[i])/mass


def key(row,two):
    month=row["month"]
    return month[:4]+str((int(month[4:])-1)//3) if two else month


def block(rows,cfg,quarter=False):
    groups=defaultdict(list)
    for r in rows:
        if r["delta"] is not None:
            groups[key(r,quarter)].append(r)
    if len(groups)<4:return {}
    g=[v for _,v in sorted(groups.items())]
    rng=Random(cfg["seed"])
    average=[]
    tails=[]
    for _ in range(cfg["replicates"]):
        picked=[r for v in rng.choices(g,k=len(g)) for r in v]
        average.append(mean(r["delta"] for r in picked))
        tails.append(tail([-r["m_pnl"] for r in picked],.99)-tail([-r["k_pnl"] for r in picked],.99))
    def quantiles(data):
        data.sort()
        return {str(p):data[max(0,ceil(p*len(data))-1)] for p in (.025,.05,.95,.975)}
    return dict(groups=len(g),mean=quantiles(average),delta_cvar99=quantiles(tails))


def decide(rows,stats,config,archive_count):
    eligible=len(rows)
    if not eligible:
        return dict(status="BLOCKED_INSUFFICIENT_DATA",reason="NO_ELIGIBLE_ACTIVATIONS")
    bars=config["barriers"]
    valid=[r for r in rows if r["delta"] is not None]
    m={r["month"] for r in rows}
    q=stats.get("month",{})
    three=stats.get("quarter",{})
    fail=[]
    if archive_count!=bars["complete_months"]:fail.append("INCOMPLETE_CALENDAR")
    if len(m)<bars["min_eligible_month_clusters"]:fail.append("LOW_POWER")
    if len(rows)!=len(valid):fail.append("NONFLAT_PAIRS")
    if any(r["m_violations"] or r["k_violations"] for r in rows):fail.append("RISK_VIOLATIONS")
    if q.get("mean",{}).get("0.05",float("-inf"))<=0:fail.append("LCB_NOT_POSITIVE")
    if three.get("mean",{}).get("0.05",float("-inf"))<=0:fail.append("THREE_MONTH_LCB_NOT_POSITIVE")
    if not stats["leave_one_out"] or min(stats["leave_one_out"].values())<=0:
        fail.append("INFLUENTIAL_MONTH")
    if stats["tail_delta"] is not None and stats["tail_delta"]>bars["max_incremental_cvar99_usd"]:
        fail.append("EXTRA_CVAR99")
    if stats["worst_extra_loss"] is not None and stats["worst_extra_loss"]>bars["max_additional_loss_usd"]:
        fail.append("EXTRA_WORST_LOSS")
    if not fail:
        status="CONFIRMATORY_ADVANTAGE_SUPPORTED"
    elif any(f in fail for f in ("NONFLAT_PAIRS","RISK_VIOLATIONS","EXTRA_CVAR99","EXTRA_WORST_LOSS")) or (
            q and q["mean"]["0.95"]<0):
        status="NEGATIVE_EVIDENCE"
    elif "LOW_POWER" in fail or "INCOMPLETE_CALENDAR" in fail:
        status="INCONCLUSIVE"
    else:
        status="NO_CONFIRMED_ADVANTAGE"
    return dict(status=status,failed_barriers=fail,eligible=len(rows),blocks=len(m),
                valid_archives=archive_count,paired_flat=len(valid),
                evidence="MODEL_ONLY",production_ready="NO")


def summary(rows,cfg):
    v=[r for r in rows if r["delta"] is not None]
    r=[x["delta"] for x in v]
    m=sorted({x["month"] for x in v})
    return dict(paired_flat=len(v),paired_mean=mean(r) if r else None,
                paired_median=median(r) if r else None,
                positive=sum(d>0 for d in r),negative=sum(d<0 for d in r),ties=sum(d==0 for d in r),
                tail_delta=tail([-x["m_pnl"] for x in v],.99)-tail([-x["k_pnl"] for x in v],.99) if v else None,
                worst_extra_loss=max(0,-min(r)) if r else None,
                month=block(rows,cfg),quarter=block(rows,cfg,quarter=True),
                leave_one_out={k:mean(x["delta"] for x in v if x["month"]!=k) for k in m if len(m)>1})
