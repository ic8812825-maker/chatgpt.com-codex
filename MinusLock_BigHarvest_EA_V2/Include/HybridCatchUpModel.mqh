#ifndef __BH_HYBRID_CATCHUP_MODEL_MQH__
#define __BH_HYBRID_CATCHUP_MODEL_MQH__
#include "HybridPartialFarPreview.mqh"

// Pure projected model: no orders, positions, global context, ledger or state-machine writes.
double HybridCatchUpMoneyRound(double value) { return NormalizeDouble(value,2); }
double HybridCatchUpClosePrice(Direction direction,double bid,double ask) { return direction==DIR_BUY?bid:ask; }

bool BuildProjectedReopenPrices(Direction bigDirection,double levelBid,double levelAsk,HybridReopenPrices &prices)
{
   ZeroMemory(prices);
   if(bigDirection==DIR_BUY) { prices.coreOpenPrice=levelAsk; prices.trendOpenPrice=levelAsk; prices.smallOpenPrice=levelBid; }
   else if(bigDirection==DIR_SELL) { prices.coreOpenPrice=levelBid; prices.trendOpenPrice=levelBid; prices.smallOpenPrice=levelAsk; }
   else return false;
   return levelBid>0 && levelAsk>=levelBid;
}

ulong HybridCatchUpFingerprint(const HybridCatchUpState &state,HybridCatchUpProfileKind profile)
{
   string value=StringFormat("%s|%I64d|%I64u|%I64u|%d|%d|%.8f|%.10f|%.8f|%.10f|%.8f|%.10f|%.8f|%.10f|%.10f|%.10f|%.2f|%.2f|%.2f|%.2f|%d",
      state.symbol,state.magic,state.cycleId,state.stateRevision,state.levelIndex,(int)state.farDirection,state.farLot,state.farOpenPrice,
      state.coreLot,state.coreOpenPrice,state.trendLot,state.trendOpenPrice,state.smallLot,state.smallOpenPrice,
      state.anchorBid,state.anchorAsk,state.realizedCyclePL,state.partialFarBudgetAvailable,state.finalReserveReal,state.carryAvailable,(int)profile);
   ulong hash=1469598103934665603;
   for(int i=0;i<StringLen(value);i++) { hash^=(ulong)StringGetCharacter(value,i); hash*=1099511628211; }
   return hash;
}

bool ValidateHybridCatchUpState(const HybridCatchUpState &s,string &reason)
{
   if(s.levelIndex<0 || s.symbol=="" || s.cycleId==0 || s.farDirection==DIR_NONE || s.bigDirection==DIR_NONE || s.smallDirection==DIR_NONE)
   { reason="CATCHUP_STATE_INVALID"; return false; }
   if(s.farLot<=0 || s.farOpenPrice<=0 || s.coreLot<=0 || s.coreOpenPrice<=0 || s.trendLot<=0 || s.trendOpenPrice<=0 || s.smallLot<=0 || s.smallOpenPrice<=0)
   { reason="CATCHUP_STATE_INVALID"; return false; }
   if(s.anchorBid<=0 || s.anchorAsk<s.anchorBid || s.partialFarBudgetAvailable<0 || s.finalReserveReal<0 || s.carryAvailable<0 || s.equity<=0 || s.currentMargin<0)
   { reason="CATCHUP_STATE_INVALID"; return false; }
   reason="PASS"; return true;
}

bool HybridCatchUpCurrentLegMoney(Direction direction,double lot,double openPrice,double bid,double ask,bool includeOpenCommission,BrokerMoneyResult &money)
{
   double closePrice=HybridCatchUpClosePrice(direction,bid,ask);
   return CalcProjectedPositionNetMoney(direction,lot,openPrice,closePrice,includeOpenCommission,true,money);
}

bool HybridCatchUpMarginMoney(Direction direction,double lot,double price,BrokerMoneyResult &money)
{
   return CalcProjectedMarginMoney(direction==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL,lot,price,money);
}

bool HybridCatchUpMarginTransition(const HybridCatchUpState &before,const HybridCatchUpState &after,double partialLot,HybridHarvestLevelResult &row,const HybridCatchUpProfile &profile)
{
   BrokerMoneyResult oldCore,oldTrend,oldSmall,partial,remain,nextCore,nextTrend,nextSmall;
   if(!HybridCatchUpMarginMoney(before.bigDirection,before.coreLot,before.coreOpenPrice,oldCore)
      || !HybridCatchUpMarginMoney(before.bigDirection,before.trendLot,before.trendOpenPrice,oldTrend)
      || !HybridCatchUpMarginMoney(before.smallDirection,before.smallLot,before.smallOpenPrice,oldSmall)) return false;
   double released=oldCore.requiredMargin+oldTrend.requiredMargin+oldSmall.requiredMargin;
   if(partialLot>0)
   { if(!HybridCatchUpMarginMoney(before.farDirection,partialLot,before.farOpenPrice,partial)) return false; released+=partial.requiredMargin; }
   if(!HybridCatchUpMarginMoney(after.farDirection,after.farLot,after.farOpenPrice,remain)
      || !HybridCatchUpMarginMoney(after.bigDirection,after.coreLot,after.coreOpenPrice,nextCore)
      || !HybridCatchUpMarginMoney(after.bigDirection,after.trendLot,after.trendOpenPrice,nextTrend)
      || !HybridCatchUpMarginMoney(after.smallDirection,after.smallLot,after.smallOpenPrice,nextSmall)) return false;
   row.marginBefore=before.currentMargin;
   row.marginReleased=MathMin(before.currentMargin,released);
   row.marginAfter=remain.requiredMargin+nextCore.requiredMargin+nextTrend.requiredMargin+nextSmall.requiredMargin;
   row.overlapUpper=before.currentMargin+nextCore.requiredMargin+nextTrend.requiredMargin+nextSmall.requiredMargin;
   row.peakMargin=HybridCatchUpAssumeMarginOverlap?row.overlapUpper:MathMax(before.currentMargin,row.marginAfter);
   double worstMargin=row.marginAfter*(1.0+profile.marginSafetyPercent/100.0);
   double level=worstMargin>0?before.equity/worstMargin*100.0:DBL_MAX;
   double usage=worstMargin/before.equity*100.0;
   return before.equity-worstMargin>0 && level+MoneyCalculationTolerance>=MinimumSafeMarginLevel && usage<=MaxMarginPercent+MoneyCalculationTolerance;
}

bool BuildInitialHybridCatchUpState(const HybridCycleSnapshot &snapshot,const HybridCandidatePlan &plan,const HybridCatchUpProfile &profile,HybridCatchUpState &state)
{
   ZeroMemory(state);
   state.levelIndex=0; state.symbol=snapshot.symbol; state.magic=(long)snapshot.magic; state.cycleId=snapshot.cycleId;
   state.stateRevision=snapshot.stateRevision; state.snapshotTime=snapshot.snapshotTime;
   state.farDirection=snapshot.farDirection; state.farLot=snapshot.farLot; state.farOpenPrice=snapshot.farOpenPrice;
   state.bigDirection=plan.bigDirection; state.coreLot=plan.coreLot; state.trendLot=plan.trendLot;
   state.smallDirection=plan.smallDirection; state.smallLot=plan.smallLot;
   state.anchorBid=snapshot.bid; state.anchorAsk=snapshot.ask; state.spread=snapshot.ask-snapshot.bid;
   HybridReopenPrices prices; if(!BuildProjectedReopenPrices(plan.bigDirection,snapshot.bid,snapshot.ask,prices)) return false;
   state.coreOpenPrice=prices.coreOpenPrice; state.trendOpenPrice=prices.trendOpenPrice; state.smallOpenPrice=prices.smallOpenPrice;
   state.realizedCyclePL=snapshot.realizedCyclePL; state.partialFarBudgetAvailable=snapshot.partialFarAvailable;
   state.finalReserveReal=snapshot.finalReserveReal; state.carryAvailable=0;
   state.equity=snapshot.equity; state.currentMargin=snapshot.margin; state.freeMargin=snapshot.freeMargin;
   state.lastCoverageDeficit=DBL_MAX; state.lastRecoveryPL=-DBL_MAX;
   state.openCommissionAlreadyRealized=false; state.projectedOpenCommissionIncluded=false; state.projectedCloseCommissionIncluded=false;
   state.fingerprint=HybridCatchUpFingerprint(state,profile.kind);
   string reason; return ValidateHybridCatchUpState(state,reason);
}

bool EvaluateHybridCatchUpLevel(const HybridCatchUpState &before,const HybridCatchUpProfile &profile,HybridHarvestLevelResult &row,HybridCatchUpState &after)
{
   ZeroMemory(row); ZeroMemory(after); row.level=before.levelIndex+1; row.reason="NOT_EVALUATED";
   string validation; if(!ValidateHybridCatchUpState(before,validation)) { row.reason=validation; return false; }
   row.stateBeforeFingerprint=before.fingerprint; row.farLotBefore=before.farLot; row.farOpenPrice=before.farOpenPrice;
   row.coreLot=before.coreLot; row.coreOpenPrice=before.coreOpenPrice;
   row.trendLot=before.trendLot; row.trendOpenPrice=before.trendOpenPrice;
   row.smallLot=before.smallLot; row.smallOpenPrice=before.smallOpenPrice;
   row.partialBudgetBefore=before.partialFarBudgetAvailable; row.reserveBefore=before.finalReserveReal;
   row.carryBefore=before.carryAvailable; row.realizedPLBefore=before.realizedCyclePL; row.marginBefore=before.currentMargin;
   row.coverageBefore=before.lastCoverageDeficit; row.recoveryBefore=before.lastRecoveryPL;

   double point=SymbolInfoDouble(before.symbol,SYMBOL_POINT); if(point<=0) { row.reason="CATCHUP_TRIGGER_INVALID"; return false; }
   double distance=(before.levelIndex==0?BigMoveStartPoints:BigMoveStepPoints)*point;
   double baseBid,baseAsk;
   if(before.bigDirection==DIR_BUY) { baseBid=before.anchorBid+distance; baseAsk=baseBid+before.spread; }
   else { baseAsk=before.anchorAsk-distance; baseBid=baseAsk-before.spread; }
   // A shared pair is used only because bid-down is adverse for every BUY close
   // and ask-up is adverse for every SELL close; the property is explicit here.
   row.triggerBid=baseBid-profile.adversePoints*point;
   row.triggerAsk=baseAsk+profile.adversePoints*point;
   if(row.triggerBid<=0 || row.triggerAsk<row.triggerBid) { row.reason="CATCHUP_TRIGGER_INVALID"; return false; }

   bool includeOpen=!before.openCommissionAlreadyRealized;
   if(!HybridCatchUpCurrentLegMoney(before.bigDirection,before.coreLot,before.coreOpenPrice,row.triggerBid,row.triggerAsk,includeOpen,row.coreClose)
      || !HybridCatchUpCurrentLegMoney(before.bigDirection,before.trendLot,before.trendOpenPrice,row.triggerBid,row.triggerAsk,includeOpen,row.trendClose)
      || !HybridCatchUpCurrentLegMoney(before.smallDirection,before.smallLot,before.smallOpenPrice,row.triggerBid,row.triggerAsk,includeOpen,row.smallClose))
   { row.reason="CATCHUP_CURRENT_MONEY_FAILED"; return false; }
   row.harvestNet=HybridCatchUpMoneyRound(row.coreClose.netMoney+row.trendClose.netMoney+row.smallClose.netMoney);
   row.eligibleHarvest=MathMax(row.harvestNet,0.0);
   row.partialAdd=HybridCatchUpMoneyRound(HybridPartialFarShare*row.eligibleHarvest);
   row.reserveAdd=HybridCatchUpMoneyRound(HybridFinalReserveShare*row.eligibleHarvest);
   double carryBase=HybridCatchUpMoneyRound(HybridCarryShare*row.eligibleHarvest);
   row.carryAdd=HybridCatchUpMoneyRound(carryBase+HybridCatchUpMoneyRound(row.eligibleHarvest-row.partialAdd-row.reserveAdd-carryBase));
   row.allocationPass=MathAbs(row.partialAdd+row.reserveAdd+row.carryAdd-row.eligibleHarvest)<=MoneyCalculationTolerance;
   if(!row.allocationPass) { row.reason="CATCHUP_ALLOCATION_FAILED"; return false; }

   double budgetGross=HybridCatchUpMoneyRound(before.partialFarBudgetAvailable+row.partialAdd);
   HybridPartialFarPreviewResult partial;
   if(!SolveHybridPartialFarPreview(before,budgetGross,row.triggerBid,row.triggerAsk,partial)) { row.reason=partial.reason; return false; }
   row.requiresFinalCloseCheck=partial.requiresFinalClosePreview;
   row.farLotClosed=partial.normalizedCloseLot; row.farLotAfter=partial.farLotAfter;
   row.partialFarClose=partial.partialCloseMoney; row.partialConsumed=partial.budgetConsumed; row.partialBudgetAfter=partial.budgetAfter;
   row.partialBudgetPass=partial.budgetConservationPass; row.realizedPLAfterHarvest=HybridCatchUpMoneyRound(before.realizedCyclePL+row.harvestNet);
   double partialNet=partial.partialCloseAvailable?partial.partialCloseMoney.netMoney:0.0;
   row.realizedPLAfterPartial=HybridCatchUpMoneyRound(row.realizedPLAfterHarvest+partialNet);
   if(!row.partialBudgetPass) { row.reason="CATCHUP_PARTIAL_BUDGET_FAILED"; return false; }
   if(!partial.remainderVolumeValid) { row.reason="CATCHUP_INVALID_FAR_REMAINDER"; return false; }
   if(partial.requiresFinalClosePreview) { row.reason="CATCHUP_REQUIRES_FINAL_CLOSE_PREVIEW"; return false; }

   after=before; after.levelIndex=before.levelIndex+1; after.stateRevision=before.stateRevision+1;
   after.snapshotTime=before.snapshotTime; after.farLot=row.farLotAfter;
   after.realizedCyclePL=row.realizedPLAfterPartial; after.partialFarBudgetAvailable=row.partialBudgetAfter;
   after.finalReserveReal=HybridCatchUpMoneyRound(before.finalReserveReal+row.reserveAdd);
   after.carryAvailable=HybridCatchUpMoneyRound(before.carryAvailable+row.carryAdd);
   after.cumulativeHarvestNet=HybridCatchUpMoneyRound(before.cumulativeHarvestNet+row.harvestNet);
   after.cumulativePartialFarNet=HybridCatchUpMoneyRound(before.cumulativePartialFarNet+partialNet);
   after.anchorBid=row.triggerBid; after.anchorAsk=row.triggerAsk; after.spread=row.triggerAsk-row.triggerBid;
   row.reserveAfter=after.finalReserveReal; row.carryAfter=after.carryAvailable;
   row.reserveAfter=after.finalReserveReal; row.carryAfter=after.carryAvailable;

   double minLot=SymbolInfoDouble(before.symbol,SYMBOL_VOLUME_MIN);
   if(after.farLot<minLot-MoneyCalculationTolerance) { row.reason="CATCHUP_TERMINAL_MIN_VOLUME"; return false; }
   after.coreLot=NormalizeHybridCoreLot(after.farLot*BigCoreRatio);
   after.trendLot=NormalizeHybridTrendLot(after.farLot*BigTrendRatio);
   after.smallLot=NormalizeHybridSmallLot(after.farLot*SmallBaseToFarRatio);
   row.nextCoreLot=after.coreLot; row.nextTrendLot=after.trendLot; row.nextSmallLot=after.smallLot;
   row.nextStatePass=after.coreLot>=minLot && after.trendLot>=minLot && after.smallLot>=minLot;
   if(!row.nextStatePass) { row.reason="CATCHUP_TERMINAL_MIN_VOLUME"; return false; }
   double kr=HybridFinalReserveShare*(after.coreLot+after.trendLot-after.smallLot)/after.farLot;
   double slope=after.coreLot+after.trendLot-after.smallLot-after.farLot;
   if(kr+MoneyCalculationTolerance<MinimumReserveCatchUpRatio || slope<=0 || after.coreLot+after.trendLot>=before.farLot*MaximumNewBigToOldFarRatio)
   { row.reason="CATCHUP_NEXT_BASKET_GEOMETRY_FAILED"; return false; }
   HybridReopenPrices reopen; if(!BuildProjectedReopenPrices(after.bigDirection,row.triggerBid,row.triggerAsk,reopen)) { row.reason="CATCHUP_NEXT_BASKET_VOLUME_FAILED"; return false; }
   after.coreOpenPrice=reopen.coreOpenPrice; after.trendOpenPrice=reopen.trendOpenPrice; after.smallOpenPrice=reopen.smallOpenPrice;
   row.nextAnchorBid=row.triggerBid; row.nextAnchorAsk=row.triggerAsk;

   if(!HybridPartialFarCloseMoney(after,after.farLot,row.triggerBid,row.triggerAsk,row.remainingFar)) { row.reason="CATCHUP_REMAINING_FAR_MONEY_FAILED"; return false; }
   row.remainingFarCloseCost=HybridCatchUpMoneyRound(MathMax(-row.remainingFar.netMoney,0.0)+HybridCoverageSafetyBufferMoney);
   row.coverageDeficit=HybridCatchUpMoneyRound(row.remainingFarCloseCost-after.finalReserveReal); row.coverageAfter=row.coverageDeficit;
   row.coveragePass=row.coverageDeficit<=MoneyCalculationTolerance;
   row.recoveryAfterPartial=HybridCatchUpMoneyRound(after.realizedCyclePL+row.remainingFar.netMoney);
   BrokerMoneyResult nextCore,nextTrend,nextSmall;
   if(!HybridCatchUpCurrentLegMoney(after.bigDirection,after.coreLot,after.coreOpenPrice,row.triggerBid,row.triggerAsk,true,nextCore)
      || !HybridCatchUpCurrentLegMoney(after.bigDirection,after.trendLot,after.trendOpenPrice,row.triggerBid,row.triggerAsk,true,nextTrend)
      || !HybridCatchUpCurrentLegMoney(after.smallDirection,after.smallLot,after.smallOpenPrice,row.triggerBid,row.triggerAsk,true,nextSmall))
   { row.reason="CATCHUP_CURRENT_MONEY_FAILED"; return false; }
   row.recoveryAfterReopen=HybridCatchUpMoneyRound(after.realizedCyclePL+row.remainingFar.netMoney+nextCore.netMoney+nextTrend.netMoney+nextSmall.netMoney);
   row.recoveryPass=row.recoveryAfterReopen+MoneyCalculationTolerance>=MinimumRecoveryProfitMoney;

   row.marginPass=HybridCatchUpMarginTransition(before,after,row.farLotClosed,row,profile);
   if(!row.marginPass) { row.reason="CATCHUP_MARGIN_FAILED"; return false; }
   after.currentMargin=row.marginAfter; after.freeMargin=after.equity-after.currentMargin;
   row.temporalPass=after.finalReserveReal+MoneyCalculationTolerance>=before.finalReserveReal
      && after.farLot<=before.farLot+MoneyCalculationTolerance
      && (row.farLotClosed<=MoneyCalculationTolerance || after.farLot<before.farLot-MoneyCalculationTolerance)
      && (before.levelIndex==0 || row.coverageDeficit<=before.lastCoverageDeficit-HybridMinimumCoverageGainMoney+MoneyCalculationTolerance)
      && (before.levelIndex==0 || row.recoveryAfterReopen+HybridAllowedMarketCostDeteriorationMoney+MoneyCalculationTolerance>=before.lastRecoveryPL);
   if(!row.temporalPass) { row.reason="CATCHUP_TEMPORAL_INVARIANT_FAILED"; return false; }
   after.lastCoverageDeficit=row.coverageDeficit; after.lastRecoveryPL=row.recoveryAfterReopen;
   after.openCommissionAlreadyRealized=false; after.projectedOpenCommissionIncluded=true; after.projectedCloseCommissionIncluded=false;
   after.cumulativeOpeningCosts=HybridCatchUpMoneyRound(before.cumulativeOpeningCosts+nextCore.openCommission+nextTrend.openCommission+nextSmall.openCommission);
   after.fingerprint=HybridCatchUpFingerprint(after,profile.kind); row.stateAfterFingerprint=after.fingerprint; row.stateAfter=after;
   row.pass=row.coveragePass && row.recoveryPass && row.marginPass && row.allocationPass && row.partialBudgetPass && row.temporalPass && row.nextStatePass;
   row.reason=row.pass?"PASS":(!row.coveragePass?"CATCHUP_REMAINING_FAR_NOT_COVERED":"CATCHUP_RECOVERY_FAILED");
   return true;
}

string HybridCatchUpTraceRow(const HybridHarvestLevelResult &r,string profile)
{
   return StringFormat("HYBRID_CATCHUP_LEVEL|Profile=%s|Level=%d|StateBeforeFingerprint=%I64u|StateAfterFingerprint=%I64u|TriggerBid=%.10f|TriggerAsk=%.10f|FarLotBefore=%.8f|FarCloseLot=%.8f|FarLotAfter=%.8f|FarOpenPrice=%.10f|PartialFarNet=%.2f|CoreLot=%.8f|CoreOpenPrice=%.10f|CoreNet=%.2f|TrendLot=%.8f|TrendOpenPrice=%.10f|TrendNet=%.2f|SmallLot=%.8f|SmallOpenPrice=%.10f|SmallNet=%.2f|HarvestNet=%.2f|EligibleHarvest=%.2f|PartialBudgetBefore=%.2f|PartialAdd=%.2f|PartialConsumed=%.2f|PartialBudgetAfter=%.2f|ReserveBefore=%.2f|ReserveAdd=%.2f|ReserveAfter=%.2f|CarryBefore=%.2f|CarryAdd=%.2f|CarryAfter=%.2f|RealizedBefore=%.2f|RealizedAfterHarvest=%.2f|RealizedAfterPartial=%.2f|RemainingFarNet=%.2f|RemainingFarCost=%.2f|CoverageDeficit=%.2f|NextCoreLot=%.8f|NextTrendLot=%.8f|NextSmallLot=%.8f|NextAnchorBid=%.10f|NextAnchorAsk=%.10f|RecoveryAfterPartial=%.2f|RecoveryAfterReopen=%.2f|MarginBefore=%.2f|MarginReleased=%.2f|MarginAfter=%.2f|PeakMargin=%.2f|OverlapUpper=%.2f|TemporalPass=%d|AllocationPass=%d|PartialBudgetPass=%d|CoveragePass=%d|RecoveryPass=%d|MarginPass=%d|Decision=%s|Reason=%s;",
      profile,r.level,r.stateBeforeFingerprint,r.stateAfterFingerprint,r.triggerBid,r.triggerAsk,r.farLotBefore,r.farLotClosed,r.farLotAfter,r.farOpenPrice,r.partialFarClose.netMoney,
      r.coreLot,r.coreOpenPrice,r.coreClose.netMoney,r.trendLot,r.trendOpenPrice,r.trendClose.netMoney,r.smallLot,r.smallOpenPrice,r.smallClose.netMoney,
      r.harvestNet,r.eligibleHarvest,r.partialBudgetBefore,r.partialAdd,r.partialConsumed,r.partialBudgetAfter,r.reserveBefore,r.reserveAdd,r.reserveAfter,r.carryBefore,r.carryAdd,r.carryAfter,r.realizedPLBefore,r.realizedPLAfterHarvest,r.realizedPLAfterPartial,
      r.remainingFar.netMoney,r.remainingFarCloseCost,r.coverageDeficit,r.nextCoreLot,r.nextTrendLot,r.nextSmallLot,r.nextAnchorBid,r.nextAnchorAsk,r.recoveryAfterPartial,r.recoveryAfterReopen,r.marginBefore,r.marginReleased,r.marginAfter,r.peakMargin,r.overlapUpper,
      (int)r.temporalPass,(int)r.allocationPass,(int)r.partialBudgetPass,(int)r.coveragePass,(int)r.recoveryPass,(int)r.marginPass,r.pass?"PASS":"CONTINUE",r.reason);
}

bool EvaluateHybridFiniteCatchUpPreview(const HybridCycleSnapshot &snapshot,const HybridCandidatePlan &plan,HybridCatchUpResult &result)
{
   ZeroMemory(result); result.finiteLevel=-1; result.reason="NOT_EVALUATED";
   ArrayResize(result.baseLevels,0); ArrayResize(result.worstLevels,0);
   HybridCatchUpProfile baseProfile,worstProfile;
   baseProfile.kind=HYBRID_CATCHUP_BASE; baseProfile.adversePoints=0; baseProfile.marginSafetyPercent=0;
   worstProfile.kind=HYBRID_CATCHUP_WORST; worstProfile.adversePoints=SpreadExpansionBufferPoints+MaxSlippagePoints*SlippageSafetyMultiplier+HybridGapBufferPoints; worstProfile.marginSafetyPercent=HybridCatchUpMarginSafetyPercent;
   HybridCatchUpState baseState,worstState;
   if(!BuildInitialHybridCatchUpState(snapshot,plan,baseProfile,baseState) || !BuildInitialHybridCatchUpState(snapshot,plan,worstProfile,worstState))
   { result.reason="CATCHUP_STATE_INVALID"; return false; }
   for(int level=1;level<=MaxHarvestLevels;level++)
   {
      HybridHarvestLevelResult baseRow,worstRow; HybridCatchUpState nextBase,nextWorst;
      if(!EvaluateHybridCatchUpLevel(baseState,baseProfile,baseRow,nextBase)) { result.reason=baseRow.reason; return false; }
      if(!EvaluateHybridCatchUpLevel(worstState,worstProfile,worstRow,nextWorst)) { result.reason="CATCHUP_WORST_FAILED|"+worstRow.reason; return false; }
      ArrayResize(result.baseLevels,level); ArrayResize(result.worstLevels,level);
      result.baseLevels[level-1]=baseRow; result.worstLevels[level-1]=worstRow; result.evaluatedLevels=level;
      result.trace+=HybridCatchUpTraceRow(baseRow,"BASE")+HybridCatchUpTraceRow(worstRow,"WORST");
      result.finalCoverageDeficit=baseRow.coverageDeficit; result.finalRecoveryPL=baseRow.recoveryAfterReopen;
      result.finalBaseState=nextBase; result.finalWorstState=nextWorst;
      if(baseRow.pass && worstRow.pass) { result.calculationValid=true; result.pass=true; result.finiteLevel=level; result.reason="PASS"; return true; }
      baseState=nextBase; worstState=nextWorst; // StateAfter[n] is the only StateBefore[n+1].
   }
   result.calculationValid=true; result.reason="NO_FINITE_CATCHUP_LEVEL"; return false;
}

#endif
