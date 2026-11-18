"""Causal selection between frozen recoveries and certified flatten."""
from collections import defaultdict
from dataclasses import replace
import importlib
from random import Random
from statistics import mean

from replay import venue,a3,meta,Params

risk=importlib.import_module("07_RISK_GATE")
ROUTES={"RECOVER_A3_ER":"A3-ER","RECOVER_M_ER":"M-ER"}
ROUTE_SELECTORS={"RECOVER_A3_ER":a3.choose_er,"RECOVER_M_ER":meta.choose_meta}


def buckets(features):
    spread=features.get("spread")
    vol=features.get("range30")
    trend=features.get("momentum")
    s="narrow" if spread is not None and spread<=12 else "wide"
    v="low" if vol is not None and vol<=100 else "high"
    m="aligned" if trend is not None and trend>0 else "other"
    return (f"{s}/{v}/{m}",s,"all")


def estimate(samples):
    stable=[d for d in samples if d[2]]
    d=[x[1] for x in stable]
    clusters=defaultdict(list)
    for month,delta,_ in stable:
        clusters[month].append(delta)
    distinct=sorted(clusters)
    # Equal-weight month bootstrap, conditional on the observed month blocks.
    center=mean(d) if d else 0.
    lower=None
    if len(distinct)>=4 and len(d)>=16:
        rng=Random(44617)
        by_month=[mean(clusters[m]) for m in distinct]
        dist=sorted(mean(rng.choices(by_month,k=len(by_month))) for _ in range(1000))
        lower=dist[49]
    return dict(n=len(d),months=len(distinct),total=len(samples),
                mean=center,shrunk=center*len(d)/(len(d)+8),
                lower95_block=lower,valid_all=len(d)==len(samples))


def fit(records):
    samples=defaultdict(list)
    for e,results in records:
        baseline=results["K-EXECUTABLE"]
        for label,name in ROUTES.items():
            r=results[name]
            valid=baseline["flat"] and r["flat"] and not (baseline["violations"] or r["violations"])
            delta=r["pnl"]-baseline["pnl"] if valid else 0
            for group in buckets(e["features"]):
                samples[(label,group)].append((e["month"],delta,valid))
    result={r:{} for r in ROUTES}
    for (label,group),data in samples.items():
        result[label][group]=estimate(data)
    return result


def decide(version,features,model):
    if version=="RDB-1":
        return "RECOVER_A3_ER",dict(source="static_gate",group="")
    if version not in ("RDB-2","RDB-3","RDB-4"):
        raise ValueError(version)
    options=[]
    for label in (("RECOVER_A3_ER",) if version=="RDB-2" else tuple(ROUTES)):
        groups=(model or {}).get(label,{})
        for group in buckets(features):
            row=groups.get(group)
            if row is None:
                continue
            if row["n"]<8 or row["months"]<2:
                continue
            x=row["shrunk"]
            if version=="RDB-4":
                if not row["valid_all"] or row["lower95_block"] is None:
                    continue
                x=row["lower95_block"]
            if x>0:
                options.append((x,label,dict(row,group=group,source="causal_training")))
            break
    if options:
        _,label,report=max(options,key=lambda x:x[0])
        return label,report
    return "EXIT_K",dict(source="no_positive_supported_edge",group="")


class RDBCycle(venue.ExecutionCycle):
    """Decision uses frozen evidence at activation; subsequent actions recheck risk."""
    def __init__(self,version,episode,model,limits,journal):
        ctx=venue.PROFILES[episode.get("contract","E1")]
        super().__init__(version,episode["orientation"],limits,Params(),ctx,journal=journal)
        self.version=version
        self.entry_features=episode["features"]
        self.trained=model
        self.current_route=None
        self.initial_decision=None

    def report(self,label,reason=(),**more):
        self.v.emit(label,reason="|".join(reason),**more)
        if self.initial_decision is None:
            self.initial_decision=label

    def try_exit(self):
        v=self.v
        bad,_=risk.close_assessment(v)
        if not bad:
            self.report("EXIT_K")
            v.emit("SUBMIT_EXIT")
            self.exit()
            return
        self.report("NO_CERTIFIED_ACTION",bad)
        # A full executable remediation may remove residual risk even when an
        # already-breached cost or loss bound makes a certificate impossible.
        if risk.service_now(v,self.book.gross) and not v.active:
            v.emit("UNCERTIFIED_REMEDIAL_EXIT")
            self.exit()

    def step(self,t,q):
        v,b=self.v,self.book
        v.advance(t,q)
        v.emit("OBSERVE")
        self.monitor()
        v.emit("RISK_CHECK",**risk.observed_pending(v))
        if not b.gross and not v.active:
            self.finish=True
            v.emit("FLAT_CONFIRMED")
            return
        if v.active:
            self.report("SAFE_MANAGE_PENDING",("PENDING",))
            v.emit("WAIT_ACK")
            for order in v.active:
                if order.intent.ticket is None:
                    v.cancel(order)
            return
        stop=not b.level_ok(q,b.limits.stopout)
        self.stopout |= stop
        if stop:
            self.forced=1
        if self.memory.exiting or b.mark(q)>0 or stop or t>=b.limits.horizon or b.violations:
            self.memory=replace(self.memory,exiting=True)
            self.try_exit()
        else:
            if self.current_route is None:
                self.current_route,meta=decide(self.version,self.entry_features,self.trained)
                v.emit("DECIDE",route=self.current_route,**meta)
            if self.current_route=="EXIT_K":
                self.memory=replace(self.memory,exiting=True)
                self.try_exit()
            else:
                label,plan,nxt,_=ROUTE_SELECTORS[self.current_route](v,self.params,self.memory,self.env)
                bad,_=risk.assess(v,plan,self.env)
                if label=="SAFE" or bad:
                    v.emit("RECOVERY_DENIED",why="|".join(bad) or label)
                    self.core_closed_early|=bool(t<b.limits.horizon and b.gross)
                    self.memory=replace(self.memory,exiting=True)
                    self.try_exit()
                else:
                    self.report(self.current_route,allocation=label)
                    if self.execute(plan):
                        self.memory=nxt
                        v.emit("RECONCILE")
                        if nxt.exiting:
                            self.try_exit()
                    else:
                        self.memory=replace(self.memory,exiting=True)
                        v.emit("WAIT_ACK")
        if self.finish:
            v.emit("FLAT_CONFIRMED")
