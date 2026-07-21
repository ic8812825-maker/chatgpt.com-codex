#!/usr/bin/env python3
"""Reproducible analytical/numerical proof harness for Hybrid Split Big.

This is deliberately labelled as a broker-model proof, not an MT5 execution
proof. It produces the mandatory 100-scenario evidence and counterexamples.
"""
from __future__ import annotations
import csv, math, sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hybrid_geometry_model import Broker, Candidate, evaluate, monotonicity_trace, reverse_count, select_minimum_safe_new_far

ROOT=Path(__file__).resolve().parents[1]
BEST=Candidate("core_target",2.0,.8,.2,.9,.3,1.10,.05,.99,.01)

def write(path, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def big_rows():
    rows=[]; lots=[.01,.05,.1,.5,1,2,5,10]; distances=[100,200,300,500,1000]; steps=[.001,.01,.1]
    for i in range(100):
        b=Broker(lot_step=steps[i%3],min_lot=steps[i%3],spread_points=20*(1+(i//20)%3),commission_per_lot=2*(1+(i//10)%2),slippage_points=(i%6)*10)
        far=lots[i%len(lots)]; distance=distances[i%len(distances)]; e=select_minimum_safe_new_far(BEST,b,far,distance,2 if i>=80 else 1)
        trace=monotonicity_trace(BEST,b,far,range(0,501),2 if i>=80 else 1)
        monotonic=all(y>=x+BEST.minimum_improvement-1e-9 for x,y in zip(trace,trace[1:]))
        for move in (10,20,50,100,200,500):
            harvest=max(0,(e.core_lot+e.trend_lot-e.small_lot)*move*b.point_value-e.transition_costs)
            reserve=e.candidate.reserve_share*harvest; farloss=far*move*b.point_value
            coverage=reserve; deficit=farloss-coverage
            rows.append(dict(Scenario=i+1,Move=move,FarLot=far,FarLoss=round(farloss,6),HarvestNet=round(harvest,6),Reserve=round(reserve,6),Coverage=round(coverage,6),Deficit=round(deficit,6),RecoveryPL=round(trace[move],6),ReserveCatchUpRatio=round(e.catchup_ratio,6),Law1="PASS" if e.catchup_ratio>=BEST.safety_factor else "FAIL",Law2="PASS" if monotonic else "FAIL",LotStep=b.lot_step,CostMultiplier=2 if i>=80 else 1))
    return rows

def small_rows():
    rows=[]; lots=[.01,.05,.1,.5,1,2,5,10]; steps=[.001,.01,.1]
    for i in range(100):
        b=Broker(lot_step=steps[i%3],min_lot=steps[i%3],spread_points=20*(1+(i//20)%2),commission_per_lot=2*(1+(i//10)%2),slippage_points=(i%6)*10)
        old=lots[i%len(lots)]; e=select_minimum_safe_new_far(BEST,b,old,200,2 if i>=80 else 1)
        oldrisk=old*200*b.point_value; newrisk=e.new_far_lot*200*b.point_value
        oldgross=old+e.core_lot+e.trend_lot+e.small_lot
        nextgross=e.new_far_lot*(1+BEST.core_ratio+BEST.trend_ratio+BEST.small_ratio)
        rows.append(dict(Number=i+1,OldFar=old,TargetNewFar=round(old*BEST.target_far_ratio,6),ActualNewFar=e.new_far_lot,CompressionPercent=round((1-e.new_far_ratio)*100,4),OldRisk=oldrisk,NewRisk=newrisk,NextBigGross=round(e.new_big_gross_ratio*old,6),NextBigToOldFar=round(e.new_big_gross_ratio,6),OldCycleGross=oldgross,NextCycleGross=nextgross,Cycles=reverse_count(old,e.new_far_ratio,b),Completed="PASS" if e.accepted else "FAIL",Law3="PASS" if e.accepted and newrisk<oldrisk and nextgross<oldgross else "FAIL",RejectReason=e.reject_reason,LotStep=b.lot_step,CostMultiplier=2 if i>=80 else 1))
    return rows

def main():
    reports=ROOT/"Reports"; big=big_rows(); small=small_rows(); write(reports/"HYBRID_BIG_100_SCENARIOS.csv",big);write(reports/"HYBRID_SMALL_100_REVERSALS.csv",small)
    stress=[]
    for spread in (1,2,3,5):
      for commission in (1,2,3):
       for slip in (0,10,20,30,50):
        b=Broker(spread_points=20*spread,commission_per_lot=2*commission,slippage_points=slip);e=evaluate(BEST,b,1,200,commission)
        stress.append(dict(SpreadMultiplier=spread,CommissionMultiplier=commission,SlippagePoints=slip,Accepted=e.accepted,Law1=e.catchup_ratio>=BEST.safety_factor,Law2=e.recovery_slope>=BEST.minimum_improvement,Law3=e.accepted and e.new_far_ratio<1,TransitionNet=round(e.transition_net,6),Reason=e.reject_reason))
    write(reports/"HYBRID_STRESS_TEST.csv",stress)
    counter=[]
    for name,c in [("weak_catchup",Candidate("core_target",1.2,.1,.2,.5,.6)),("big_too_large",Candidate("core_target",2,.9,.2,.9,.7)),("transition_loss",Candidate("core_target",1.3,.1,.2,.9,.3))]:
        e=evaluate(c);counter.append(dict(Name=name,Accepted=e.accepted,RejectReason=e.reject_reason,RecoverySlope=e.recovery_slope,CatchUp=e.catchup_ratio,NewFarRatio=e.new_far_ratio,NewBigGross=e.new_big_gross_ratio,TransitionNet=e.transition_net))
    write(reports/"HYBRID_COUNTEREXAMPLES.csv",counter)
    candidates=[BEST,Candidate("dynamic",2.36,.99,.2,.93,.2),Candidate("two_stage",2.49,.64,.13,.99,.22),Candidate("trend_funded",2.33,.97,.21,.93,.24),Candidate("core_budget",2.1,.7,.18,.9,.25),Candidate("core_target",1.8,.75,.16,.92,.35)]
    compare=[]
    for c in candidates:
        e=evaluate(c);compare.append(dict(Architecture=c.architecture,Core=c.core_ratio,Trend=c.trend_ratio,Small=c.small_ratio,ReserveShare=c.reserve_share,NewFarRatio=e.new_far_ratio,NewBigRatio=e.new_big_gross_ratio,RecoverySlope=e.recovery_slope,CatchUp=e.catchup_ratio,TransitionNet=e.transition_net,Margin=e.margin_percent,ReverseBound=e.reverse_bound,Accepted=e.accepted,Reason=e.reject_reason))
    write(reports/"HYBRID_PARETO_COMPARISON.csv",compare)
    print(f"big_rows={len(big)} small_rows={len(small)} stress_rows={len(stress)}")
if __name__=="__main__":main()
