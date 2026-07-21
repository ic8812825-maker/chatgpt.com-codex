#ifndef __BH_HYBRID_GEOMETRY_SOLVER_MQH__
#define __BH_HYBRID_GEOMETRY_SOLVER_MQH__

// A deterministic pre-open gate.  It does not create orders and therefore
// cannot bypass the existing atomic basket/pending/reconciliation contracts.
struct HybridGeometryDecision
{
   bool valid; string reason;
   double bigCoreLot, bigTrendLot, smallBaseLot, targetNewFarLot;
   double netBigExposureLot, recoverySlopeMoneyPerPoint;
   double reserveSlopeMoneyPerPoint, farLossSlopeMoneyPerPoint, reserveCatchUpRatio;
   double expectedNewBigGrossLot, expectedNewBigDirectionalLot;
};

struct HybridRecoveryProjection
{
   double farNet, coreNet, trendNet, smallNet, basketNet, recoveryPL;
   double costs;
};

bool EvaluateHybridProjectedRecoveryAtPrice(Direction farDirection,double farLot,double farOpen,
                                             Direction coreDirection,double coreLot,double coreOpen,
                                             Direction trendDirection,double trendLot,double trendOpen,
                                             Direction smallDirection,double smallLot,double smallOpen,
                                             double closeMid,HybridRecoveryProjection &p)
{
   BrokerMoneyResult far,core,trend,small;
   bool ok=CalcProjectedCloseNetMoney(farDirection,farLot,farOpen,BrokerClosePriceAtMid(farDirection,closeMid),far)&&
           CalcProjectedPositionNetMoney(coreDirection,coreLot,coreOpen,BrokerClosePriceAtMid(coreDirection,closeMid),true,true,core)&&
           CalcProjectedPositionNetMoney(trendDirection,trendLot,trendOpen,BrokerClosePriceAtMid(trendDirection,closeMid),true,true,trend)&&
           CalcProjectedPositionNetMoney(smallDirection,smallLot,smallOpen,BrokerClosePriceAtMid(smallDirection,closeMid),true,true,small);
   if(!ok) return false;
   p.farNet=far.netMoney;p.coreNet=core.netMoney;p.trendNet=trend.netMoney;p.smallNet=small.netMoney;
   p.basketNet=p.farNet+p.coreNet+p.trendNet+p.smallNet;
   p.costs=far.openCommission+far.closeCommission+core.openCommission+core.closeCommission+trend.openCommission+trend.closeCommission+small.openCommission+small.closeCommission+far.spreadExpansionCost+core.spreadExpansionCost+trend.spreadExpansionCost+small.spreadExpansionCost+far.slippageCost+core.slippageCost+trend.slippageCost+small.slippageCost;
   p.recoveryPL=p.basketNet; return true;
}

bool ValidateHybridRecoveryMonotonicity(Direction farDirection,double farLot,double farOpen,
                                        Direction coreDirection,double coreLot,double coreOpen,
                                        Direction trendDirection,double trendLot,double trendOpen,
                                        Direction smallDirection,double smallLot,double smallOpen,
                                        int targetPoints,string &reason)
{
   // Check every point through the target and 500 continuation points. This
   // catches local reversals hidden between coarse diagnostic checkpoints.
   int maximumStep=MathMax(targetPoints+500,targetPoints+FarDistancePoints);
   double point=SymbolInfoDouble(_Symbol,SYMBOL_POINT),mid=(MarketAsk()+MarketBid())*.5,previous=0;
   for(int step=0;step<=maximumStep;step++)
   {
      double closeMid=mid+(coreDirection==DIR_BUY?1.0:-1.0)*step*point; HybridRecoveryProjection p;
      if(!EvaluateHybridProjectedRecoveryAtPrice(farDirection,farLot,farOpen,coreDirection,coreLot,coreOpen,trendDirection,trendLot,trendOpen,smallDirection,smallLot,smallOpen,closeMid,p)){reason="HYBRID_RECOVERY_MONEY";return false;}
      if(step>0&&p.recoveryPL<previous+MinimumRecoverySlopeMoneyPerPoint){reason=StringFormat("HYBRID_RECOVERY_NON_MONOTONIC Step=%d Previous=%.5f Current=%.5f",step,previous,p.recoveryPL);return false;}
      previous=p.recoveryPL;
   }
   reason="PASS";return true;
}

bool SolveHybridGeometry(double farLot, HybridGeometryDecision &d)
{
   d.valid=false; d.reason="HYBRID_NOT_EVALUATED";
   d.bigCoreLot=NormalizeLotDown(farLot*BigCoreRatio);
   d.bigTrendLot=NormalizeLotDown(farLot*BigTrendRatio);
   d.smallBaseLot=NormalizeLotDown(farLot*SmallBaseToFarRatio);
   d.targetNewFarLot=NormalizeLotDown(farLot*TargetNewFarRatio);
   if(!UseHybridSplitBigGeometry) { d.valid=true; d.reason="HYBRID_DISABLED"; return true; }
   if(farLot<=0 || d.bigCoreLot<=0 || d.bigTrendLot<=0 || d.smallBaseLot<=0) { d.reason="HYBRID_INVALID_VOLUME"; return false; }
   if(d.targetNewFarLot<=0 || d.targetNewFarLot>=farLot || d.targetNewFarLot>d.bigCoreLot) { d.reason="HYBRID_TARGET_NEW_FAR"; return false; }
   double pointValue=PointValuePerLot();
   d.netBigExposureLot=d.bigCoreLot+d.bigTrendLot-d.smallBaseLot-farLot;
   d.recoverySlopeMoneyPerPoint=d.netBigExposureLot*pointValue;
   d.reserveSlopeMoneyPerPoint=WorkReserveShare*(d.bigCoreLot+d.bigTrendLot-d.smallBaseLot)*pointValue;
   d.farLossSlopeMoneyPerPoint=farLot*pointValue;
   d.reserveCatchUpRatio=d.farLossSlopeMoneyPerPoint>0?d.reserveSlopeMoneyPerPoint/d.farLossSlopeMoneyPerPoint:0;
   // Gross Big is only BigCore + BigTrend; SmallBase is tracked separately
   // in directional/net exposure and must never inflate the NewBig metric.
   double nextGrossRatio=(d.bigCoreLot+d.bigTrendLot)/farLot;
   double nextNetRatio=(d.bigCoreLot+d.bigTrendLot-d.smallBaseLot-farLot)/farLot;
   d.expectedNewBigGrossLot=nextGrossRatio*d.targetNewFarLot;
   d.expectedNewBigDirectionalLot=nextNetRatio*d.targetNewFarLot;
   if(d.netBigExposureLot<MinimumNetBigExposureLots) d.reason="HYBRID_NET_BIG_EXPOSURE";
   else if(RejectNonMonotonicRecovery && d.recoverySlopeMoneyPerPoint<MinimumRecoverySlopeMoneyPerPoint) d.reason="HYBRID_RECOVERY_SLOPE";
   else if(RejectReserveCatchUpBelowMinimum && d.reserveCatchUpRatio<MinimumReserveCatchUpRatio) d.reason="HYBRID_RESERVE_CATCHUP";
   else if(d.expectedNewBigDirectionalLot>=farLot) d.reason="HYBRID_NEW_BIG_DIRECTIONAL";
   else if(RequireNewBigBelowOldFar && d.expectedNewBigGrossLot>=farLot*MaximumNewBigToOldFarRatio) d.reason="HYBRID_NEW_BIG_GROSS";
   else { d.valid=true; d.reason="PASS"; }
   if(PrintHybridOptimizationDiagnostics) Print(StringFormat("HYBRID_GEOMETRY_%s Far=%.2f Core=%.2f Trend=%.2f Small=%.2f TargetFar=%.2f RecoverySlope=%.5f CatchUp=%.5f NewBigGross=%.2f NewBigDirectional=%.2f Reason=%s",d.valid?"SELECTED":"REJECTED",farLot,d.bigCoreLot,d.bigTrendLot,d.smallBaseLot,d.targetNewFarLot,d.recoverySlopeMoneyPerPoint,d.reserveCatchUpRatio,d.expectedNewBigGrossLot,d.expectedNewBigDirectionalLot,d.reason));
   return d.valid;
}
#endif
