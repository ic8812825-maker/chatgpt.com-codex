#ifndef __BH_HYBRID_TRANSITION_PLANNER_MQH__
#define __BH_HYBRID_TRANSITION_PLANNER_MQH__
#include "HybridRoundingModel.mqh"

// Plan-before-close contract.  This uses the EA broker money functions rather
// than a synthetic P/L approximation and never credits Final Reserve.
bool PreviewNextSplitGeometry(double oldFarLot,double targetFar,HybridReversePlan &p)
{
   p.nextBigCoreLot=NormalizeLotDown(targetFar*BigCoreRatio);
   p.nextBigTrendLot=NormalizeLotDown(targetFar*BigTrendRatio);
   p.nextSmallBaseLot=NormalizeHybridSmallLot(targetFar*SmallBaseToFarRatio);
   if(targetFar<=0||targetFar>=oldFarLot||p.nextBigCoreLot<=0||p.nextBigTrendLot<=0||p.nextSmallBaseLot<=0){p.validationReason="NEXT_VOLUME";return false;}
   p.nextBigGrossLot=p.nextBigCoreLot+p.nextBigTrendLot;
   double net=p.nextBigCoreLot+p.nextBigTrendLot-p.nextSmallBaseLot-targetFar;
   p.nextRecoverySlope=net*PointValuePerLot();
   double farSlope=targetFar*PointValuePerLot();
   p.nextReserveCatchUpRatio=farSlope>0?HybridFinalReserveShare*(p.nextBigCoreLot+p.nextBigTrendLot-p.nextSmallBaseLot)*PointValuePerLot()/farSlope:0;
   p.nextMarginLevel=AccountInfoDouble(ACCOUNT_MARGIN_LEVEL);
   if(net<MinimumNetBigExposureLots||p.nextRecoverySlope<MinimumRecoverySlopeMoneyPerPoint){p.validationReason="NEXT_RECOVERY";return false;}
   if(p.nextReserveCatchUpRatio<MinimumReserveCatchUpRatio){p.validationReason="NEXT_CATCHUP";return false;}
   if(RequireNewBigBelowOldFar&&p.nextBigGrossLot>=oldFarLot*MaximumNewBigToOldFarRatio){p.validationReason="NEXT_BIG_GROSS";return false;}
   p.validationReason="PASS";return true;
}

bool EvaluateHybridReverseCandidate(double targetFar,HybridReversePlan &p)
{
   p.targetNewFarLot=targetFar;p.requiredBigCoreCloseLot=NormalizeLotDown(Ctx.bigCoreLot-p.targetNewFarLot);
   if(p.targetNewFarLot<=0||p.targetNewFarLot>=p.oldFarLot||p.requiredBigCoreCloseLot<=0){p.validationReason="TARGET";return false;}
   BrokerMoneyResult s,f,t,c;
   bool money=CalcProjectedCloseNetMoney(Ctx.smallBaseDirection,Ctx.smallBaseLot,Ctx.smallBaseOpenPrice,CurrentPriceForDirectionClose(Ctx.smallBaseDirection),s)&&CalcProjectedCloseNetMoney(Ctx.farDirection,Ctx.farLot,Ctx.farOpenPrice,CurrentPriceForDirectionClose(Ctx.farDirection),f)&&CalcProjectedCloseNetMoney(Ctx.bigTrendDirection,Ctx.bigTrendLot,Ctx.bigTrendOpenPrice,CurrentPriceForDirectionClose(Ctx.bigTrendDirection),t)&&CalcProjectedCloseNetMoney(Ctx.bigCoreDirection,p.requiredBigCoreCloseLot,Ctx.bigCoreOpenPrice,CurrentPriceForDirectionClose(Ctx.bigCoreDirection),c);
   if(!money){p.validationReason="MONEY";return false;}
   p.projectedSmallNet=s.netMoney;p.projectedOldFarNet=f.netMoney;p.projectedBigTrendNet=t.netMoney;p.projectedBigCoreCloseNet=c.netMoney;
   p.projectedTransitionNet=s.netMoney+f.netMoney+t.netMoney+c.netMoney;p.projectedReserveAfter=p.reserveBefore; // Final Reserve is not transition funding.
   if(p.projectedTransitionNet<MaximumTransitionLossMoney||p.projectedReserveAfter<MinimumReserveAfterTransition){p.validationReason="TRANSITION_MONEY";return false;}
   if(!PreviewNextSplitGeometry(p.oldFarLot,p.targetNewFarLot,p))return false;
   p.valid=true;p.validationReason="PASS";return true;
}

bool BuildHybridReversePlan(HybridReversePlan &p)
{
   p.valid=false;p.selectedArchitecture="TARGET_NEW_FAR_MINIMUM_SAFE";p.validationReason="PLAN_NOT_BUILT";
   p.oldFarIdentifier=Ctx.farIdentifier;p.bigCoreIdentifier=Ctx.bigCoreIdentifier;p.bigTrendIdentifier=Ctx.bigTrendIdentifier;p.smallBaseIdentifier=Ctx.smallBaseIdentifier;
   p.oldFarLot=Ctx.farLot;p.reserveBefore=Ctx.totalReserve;
   if(!UseHybridSplitBigGeometry){p.validationReason="HYBRID_DISABLED";return false;}
   if(p.oldFarIdentifier==0||p.bigCoreIdentifier==0||p.bigTrendIdentifier==0||p.smallBaseIdentifier==0){p.validationReason="IDENTIFIER";return false;}
   double minLot=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MIN),step=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_STEP);
   double upper=NormalizeLotDown(MathMin(Ctx.bigCoreLot-step,Ctx.farLot*TargetNewFarRatio));
   if(step<=0||upper<minLot){p.validationReason="NO_COMPRESSIBLE_BROKER_VOLUME";return false;}
   // Ascending scan is intentional: the first PASS is mathematically the
   // minimum broker-valid NewFar, not merely the configured target.
   HybridReversePlan candidate;
   for(double target=minLot;target<=upper+step*.25;target=NormalizeLotDown(target+step))
   {
      candidate=p;
      if(EvaluateHybridReverseCandidate(target,candidate)) { p=candidate; return true; }
      if(target+step<=target) break;
   }
   p.valid=false;p.validationReason="NO_SAFE_NEW_FAR";return false;
}
#endif
