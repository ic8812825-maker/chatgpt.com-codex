#ifndef __BH_HYBRID_FUTURE_SMALL_SOLVER_MQH__
#define __BH_HYBRID_FUTURE_SMALL_SOLVER_MQH__
#include "HybridRoundingModel.mqh"

bool EvaluateHybridFutureSmallDepth1(const HybridCycleSnapshot &snapshot,const HybridCandidatePlan &currentPlan,HybridFutureSmallResult &result)
{
   result.pass=false; result.depthProven=0; result.triggerPrice=0; result.transitionNet=0; result.nextNewFar=0; result.nextBigGross=0; result.nextMarginLevel=0; result.reason="NOT_EVALUATED";
   double point=SymbolInfoDouble(_Symbol,SYMBOL_POINT);
   if(point<=0){ result.reason="POINT_INVALID"; return false; }
   result.triggerPrice = snapshot.farDirection==DIR_BUY ? snapshot.farOpenPrice - FarDistancePoints*point : snapshot.farOpenPrice + FarDistancePoints*point;
   double closePrice = snapshot.farDirection==DIR_BUY ? result.triggerPrice : result.triggerPrice;
   BrokerMoneyResult far,small,trend,core;
   if(!CalcProjectedCloseNetMoney(snapshot.farDirection,snapshot.farLot,snapshot.farOpenPrice,closePrice,far)){ result.reason=far.reason; return false; }
   if(!CalcProjectedCloseNetMoney(currentPlan.smallDirection,currentPlan.smallLot,snapshot.smallOpenPrice,closePrice,small)){ result.reason=small.reason; return false; }
   if(!CalcProjectedCloseNetMoney(currentPlan.bigDirection,currentPlan.trendLot,snapshot.trendOpenPrice,closePrice,trend)){ result.reason=trend.reason; return false; }
   if(!CalcProjectedCloseNetMoney(currentPlan.bigDirection,currentPlan.closeCoreLot,snapshot.coreOpenPrice,closePrice,core)){ result.reason=core.reason; return false; }
   result.transitionNet=far.netMoney+small.netMoney+trend.netMoney+core.netMoney;
   if(result.transitionNet < -MaximumTransitionLossMoney-MoneyCalculationTolerance){ result.reason="TRANSITION_LOSS"; return false; }
   result.nextNewFar=NormalizeHybridNewFarLot(currentPlan.newFarLot*TargetNewFarRatio);
   if(result.nextNewFar<=0 || result.nextNewFar>=currentPlan.newFarLot){ result.reason="NO_VALID_NEXT_NEW_FAR"; return false; }
   double nextCore=NormalizeHybridCoreLot(currentPlan.newFarLot*BigCoreRatio);
   double nextTrend=NormalizeHybridTrendLot(currentPlan.newFarLot*BigTrendRatio);
   double nextSmall=NormalizeHybridSmallLot(currentPlan.newFarLot*SmallBaseToFarRatio);
   result.nextBigGross=nextCore+nextTrend;
   double kr=HybridFinalReserveShare*(nextCore+nextTrend-nextSmall)/currentPlan.newFarLot;
   double slope=nextCore+nextTrend-nextSmall-currentPlan.newFarLot;
   if(kr+MoneyCalculationTolerance<MinimumReserveCatchUpRatio){ result.reason="NEXT_LAW1"; return false; }
   if(slope<=0){ result.reason="NEXT_LAW2"; return false; }
   if(result.nextBigGross>=currentPlan.newFarLot*MaximumNewBigToOldFarRatio){ result.reason="NEXT_BIG"; return false; }
   result.nextMarginLevel=0;
   result.pass=true; result.depthProven=1; result.reason="PASS"; return true;
}

#endif // __BH_HYBRID_FUTURE_SMALL_SOLVER_MQH__
