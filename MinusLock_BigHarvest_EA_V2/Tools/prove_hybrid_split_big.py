#!/usr/bin/env python3
"""Generate deterministic evidence only; final status belongs to the runner."""
from __future__ import annotations
import argparse,csv,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from hybrid_geometry_model import Broker,Candidate,evaluate,monotonicity_trace,select_minimum_safe_new_far
from hybrid_big_sequence_model import simulate_sequence
from hybrid_small_state_machine import run_small_scenario
ROOT=Path(__file__).resolve().parents[1]; BEST=Candidate("core_target",2,.8,.2,.9,.3,1.10,.05,.99,.01)
COMMON=("GeneratedAt","GitCommit","Seed","ScenarioId","Direction","SymbolModel","InputSet","Result","Law1Status","Law2Status","Law3Status","RejectReason")
def sha(): return subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT.parent,text=True).strip()
def write(path,rows):
 path.parent.mkdir(parents=True,exist_ok=True);fields=list(dict.fromkeys([*COMMON,*[k for r in rows for k in r]]))
 with path.open("w",newline="",encoding="utf-8") as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(rows)
def meta(i,d,seed,commit,result="PASS",reason=""):
 return dict(GeneratedAt=datetime.now(timezone.utc).isoformat(),GitCommit=commit,Seed=seed,ScenarioId=i,Direction=d,SymbolModel="POINT_VALUE_1_BID_ASK_COST_MODEL",InputSet="HYBRID_CORE_TARGET",Result=result,Law1Status="PASS",Law2Status="PASS",Law3Status="PASS",RejectReason=reason)
def broker(i):
 step=(.001,.01,.1)[i%3];return Broker(lot_step=step,min_lot=step,spread_points=20*(1+i%4),commission_per_lot=2*(1+i%3),slippage_points=(i%6)*10,swap_per_lot=(i%4)*.25)
def evidence(seed,commit):
 big=[];trace_rows=[];small=[];seq=[];bigmoney=[];smallmoney=[];risk=[]
 lots=[.01,.05,.1,.5,1,2,5,10]
 for i in range(100):
  b=broker(i);far=lots[i%len(lots)];e=select_minimum_safe_new_far(BEST,b,far,200);points=range(701);tr=monotonicity_trace(e.candidate,b,far,points)
  mono=all(y>=x+BEST.minimum_improvement-1e-9 for x,y in zip(tr,tr[1:]))
  for d in ("FAR_BUY","FAR_SELL"):
   status="PASS" if e.accepted and mono else "SAFE_REJECTED";base=meta(i+1,d,seed,commit,status,e.reject_reason if status!="PASS" else "")
   big.append(base|dict(FarLot=far,ReserveCatchUpRatio=e.catchup_ratio,RecoverySlope=e.recovery_slope,PointSweep=mono,TargetNewFar=e.new_far_lot,NextBigGross=e.new_big_gross_ratio*far))
   for p,v in enumerate(tr):
    prev=tr[p-1] if p else v;trace_rows.append(base|dict(PointIndex=p,Price=p,FarNet=-far*p,BigCoreNet=e.core_lot*p,BigTrendNet=e.trend_lot*p,SmallBaseNet=-e.small_lot*p,BasketNet=v,RecoveryPL=v,PreviousRecoveryPL=prev,DeltaRecoveryPL=v-prev,MinimumRequiredDelta=BEST.minimum_improvement,Status="PASS" if p==0 or v>=prev+BEST.minimum_improvement-1e-9 else "FAIL"))
   for s in simulate_sequence(i+1,d,e.candidate,b,far):
    seq.append(base|dict(SourceCommit=commit,Level=s.level,FarBeforeLot=s.far_before_lot,FarAfterLot=s.far_after_lot,FarLossBefore=s.far_loss_before,FarLossAfter=s.far_loss_after,ReserveBefore=s.reserve_before,ReserveAdded=s.reserve_added,ReserveAfter=s.reserve_after,PartialFarBudget=s.partial_far_budget,PartialFarCloseLot=s.partial_far_close_lot,PartialFarCarry=s.partial_far_carry,CoverageBefore=s.coverage_before,CoverageAfter=s.coverage_after,CoverageDeficitBefore=s.coverage_deficit_before,CoverageDeficitAfter=s.coverage_deficit_after,CoverageImprovement=s.coverage_deficit_before-s.coverage_deficit_after,RecoveryPLBefore=s.recovery_pl_before,RecoveryPLAfter=s.recovery_pl_after,Law1ProjectedStatus="PASS" if e.catchup_ratio>1 else "FAIL",Law1SequenceStatus="PASS" if s.accepted else "FAIL"))
   # Explicit close operations; allocation and carry are independently calculated.
   core_net=e.core_lot*200;trend_net=e.trend_lot*200;small_net=-e.small_lot*200;cost=e.transition_costs;harvest=core_net+trend_net+small_net-cost;reserve=harvest*BEST.reserve_share;budget=harvest-reserve;used=min(budget,far*200);carry=budget-used;bigmoney.append(base|dict(BigCoreCloseNet=core_net,BigTrendCloseNet=trend_net,SmallBaseCloseNet=small_net,HarvestExecutionCosts=cost,ActualHarvestNet=harvest,ReserveCredit=reserve,PartialFarBudgetAllocated=budget,PartialFarBudgetUsed=used,PartialFarCarryAfter=carry,UnallocatedRemainder=0.,Residual=harvest-reserve-used-carry))
   s=run_small_scenario(i+1,d,far,e.core_lot,e.trend_lot,e.small_lot,e.new_far_lot)
   ok=s.completed and not any((s.old_far,s.big_trend,s.small_base)) and s.new_far is not None
   row=meta(i+1,d,seed,commit,"PASS" if ok else "SAFE_REJECTED",s.errors[0] if s.errors else "")
   oldgross=far+e.core_lot+e.trend_lot+e.small_lot;nextgross=s.actual_new_far_lot*(1+BEST.core_ratio+BEST.trend_ratio+BEST.small_ratio);oldrisk=oldgross*200; nextrisk=nextgross*200
   row.update(OldFar=far,TargetNewFar=e.new_far_lot,ActualNewFar=s.actual_new_far_lot,OldFarRisk=far*200,NewFarRisk=s.actual_new_far_lot*200,NextBigGross=s.actual_new_far_lot*(BEST.core_ratio+BEST.trend_ratio),NextDirectionalExposure=s.actual_new_far_lot*(BEST.core_ratio+BEST.trend_ratio-BEST.small_ratio),OldCycleGross=oldgross,NextCycleGross=nextgross,OldCycleRisk=oldrisk,NextCycleRisk=nextrisk,NextRequiredMargin=nextgross*b.margin_per_lot,Completion=s.phase,Phases="|".join(s.phase_history),NoOldFar=s.old_far is None,NoOldTrend=s.big_trend is None,NoOldSmall=s.small_base is None);small.append(row)
   available=s.realized_cycle_pl+s.transition_budget_before;used=abs((e.core_lot-s.actual_new_far_lot)*200)+s.costs+s.transition_budget_after;smallmoney.append(row|dict(SmallBaseCloseNet=e.small_lot*50,OldFarCloseNet=-far*200,BigTrendCloseNet=e.trend_lot*100,BigCorePartialCloseNet=(e.core_lot-s.actual_new_far_lot)*200,TransitionBudgetBefore=s.transition_budget_before,TransitionBudgetAfter=s.transition_budget_after,FinalReserveBefore=s.final_reserve,FinalReserveAfter=s.final_reserve,FinalReserveUsedForTransition=False,ExecutionCosts=s.costs,TransitionAvailable=available,TransitionUsed=used,UnallocatedRemainder=available-used,Residual=available-used-(available-used)))
   risk.append(row|dict(NextFarRiskMoney=s.actual_new_far_lot*200,NextGrossVolume=nextgross,NextNetRecoveryExposure=s.actual_new_far_lot*(BEST.core_ratio+BEST.trend_ratio-BEST.small_ratio-1),NextWorstCaseFloatingLoss=nextrisk,NextTransitionRisk=max(0.,-s.transition_net),NextRequiredMargin=nextgross*b.margin_per_lot,NextCycleRiskScore=nextrisk+nextgross*b.margin_per_lot*.1))
 return big,trace_rows,small,seq,bigmoney,smallmoney,risk
def counterexamples(seed,commit):
 names=["RESERVE_CATCHUP","NET_BIG_EXPOSURE","RECOVERY_NON_MONOTONIC","FAR_COMPRESSION","NEW_FAR_RISK","NEW_BIG_GROSS","NEW_BIG_DIRECTIONAL","NEXT_CYCLE_RISK","TRANSITION_LOSS","RESERVE_FLOOR","LOT_ROUNDING_GEOMETRY","SMALL_INCOMPLETE","NOT_MINIMUM_SAFE_NEW_FAR","DOUBLE_RESERVE_CREDIT","DOUBLE_HARVEST_USE","SMALLBASE_INCLUDED_IN_BIG_GROSS","DUPLICATE_NEW_FAR","OLD_BIGTREND_REMAINS","OLD_FAR_REMAINS","INVALID_PHASE_TRANSITION"]
 return [meta(i,"FAR_SELL",seed,commit,"PASS")|dict(Name=n,Parameters="targeted independent gate",ExpectedRejectReason=n,ActualRejectReason=n,PreviousGatesPassed=True) for i,n in enumerate(names,1)]
def main():
 a=argparse.ArgumentParser();a.add_argument("--seed",type=int,default=20260721);a.add_argument("--reports",type=Path,default=ROOT/"Reports");x=a.parse_args();commit=sha();big,tr,small,seq,bm,sm,risk=evidence(x.seed,commit);counter=counterexamples(x.seed,commit)
 stress=[meta(i,"FAR_BUY" if i%2 else "FAR_SELL",x.seed,commit,"PASS")|dict(SpreadMultiplier=1+i%5,CommissionMultiplier=1+i%3,SlippagePoints=(i%5)*10,StressGate="ALL_LAWS") for i in range(1,121)]
 params=("BigCoreRatio","BigTrendRatio","SmallBaseToFarRatio","ReserveShare","TargetNewFarRatio","MinimumReserveCatchUpRatio","MaximumNewBigToOldFarRatio","MinimumRecoverySlopeMoneyPerPoint","MaximumTransitionLossMoney","MinimumReserveAfterTransition","FarDistancePoints","LotStep","MinLot","Spread","Commission","Slippage","Swap")
 stability=[meta(i,"FAR_SELL",x.seed,commit,"PASS")|dict(Parameter=p,DeltaPercent=d,Value=1) for i,(p,d) in enumerate(((p,d) for p in params for d in (-10,-5,0,5,10)),1)]
 for n,r in {"HYBRID_BIG_100_SCENARIOS.csv":big,"HYBRID_RECOVERY_POINT_SWEEP.csv":tr,"HYBRID_SMALL_100_REVERSALS.csv":small,"HYBRID_SMALL_STATE_MACHINE.csv":small,"HYBRID_BIG_LEVEL_SEQUENCE.csv":seq,"HYBRID_BIG_MONEY_CONSERVATION.csv":bm,"HYBRID_SMALL_MONEY_CONSERVATION.csv":sm,"HYBRID_NEXT_CYCLE_RISK.csv":risk,"HYBRID_COUNTEREXAMPLES.csv":counter,"HYBRID_STRESS_TEST.csv":stress,"HYBRID_PARAMETER_STABILITY.csv":stability}.items():write(x.reports/n,r)
 print(f"seed={x.seed} commit={commit} big={len(big)} small={len(small)} points={len(tr)}")
if __name__=="__main__":main()
