#ifndef __BH_HYBRID_CATCHUP_MODEL_MQH__
#define __BH_HYBRID_CATCHUP_MODEL_MQH__
#include "HybridPartialFarPreview.mqh"

// Pure projected model: no orders, positions, ledgers or state-machine writes.
double HybridCatchUpMoneyRound(double value) { return NormalizeDouble(value,2); }
double HybridCatchUpClosePrice(Direction direction,double bid,double ask) { return direction==DIR_BUY?bid:ask; }
double HybridMarginControlPrice(Direction direction,double bid,double ask) { return direction==DIR_BUY?ask:bid; }

HybridCatchUpOutcomeClass ClassifyHybridCatchUpOutcome(HybridCatchUpOutcome outcome)
{
   if(outcome==HYBRID_CATCHUP_OUTCOME_CONTINUE) return HYBRID_CATCHUP_CLASS_CONTINUE;
   if(outcome==HYBRID_CATCHUP_OUTCOME_FINITE_PASS) return HYBRID_CATCHUP_CLASS_SUCCESS;
   if(outcome==HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED) return HYBRID_CATCHUP_CLASS_ROUTE;
   if(outcome==HYBRID_CATCHUP_OUTCOME_TERMINAL_MIN_VOLUME) return HYBRID_CATCHUP_CLASS_TERMINAL;
   if(outcome==HYBRID_CATCHUP_OUTCOME_NO_FINITE_LEVEL ||
      (outcome>=HYBRID_CATCHUP_OUTCOME_REJECT_CONFIG && outcome<=HYBRID_CATCHUP_OUTCOME_REJECT_WORST_NON_ADVERSE)) return HYBRID_CATCHUP_CLASS_REJECT;
   if(outcome>=HYBRID_CATCHUP_OUTCOME_ERROR_BROKER_MONEY) return HYBRID_CATCHUP_CLASS_ERROR;
   return HYBRID_CATCHUP_CLASS_NONE;
}

HybridCatchUpOutcome CombineHybridCatchUpOutcomes(HybridCatchUpOutcome baseOutcome,HybridCatchUpOutcome worstOutcome)
{
   HybridCatchUpOutcomeClass b=ClassifyHybridCatchUpOutcome(baseOutcome),w=ClassifyHybridCatchUpOutcome(worstOutcome);
   if(b==HYBRID_CATCHUP_CLASS_ERROR) return baseOutcome;
   if(w==HYBRID_CATCHUP_CLASS_ERROR) return worstOutcome;
   if(b==HYBRID_CATCHUP_CLASS_TERMINAL) return baseOutcome;
   if(w==HYBRID_CATCHUP_CLASS_TERMINAL) return worstOutcome;
   if(b==HYBRID_CATCHUP_CLASS_REJECT) return baseOutcome;
   if(w==HYBRID_CATCHUP_CLASS_REJECT) return worstOutcome;
   if(b==HYBRID_CATCHUP_CLASS_ROUTE || w==HYBRID_CATCHUP_CLASS_ROUTE)
   {
      if(b==HYBRID_CATCHUP_CLASS_ROUTE && w==HYBRID_CATCHUP_CLASS_ROUTE) return HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED;
      return HYBRID_CATCHUP_OUTCOME_REJECT_OUTCOME_DIVERGENCE;
   }
   if(b==HYBRID_CATCHUP_CLASS_SUCCESS && w==HYBRID_CATCHUP_CLASS_SUCCESS) return HYBRID_CATCHUP_OUTCOME_FINITE_PASS;
   return HYBRID_CATCHUP_OUTCOME_CONTINUE;
}

string HybridCatchUpReasonCode(HybridCatchUpOutcome outcome)
{
   switch(outcome)
   {
      case HYBRID_CATCHUP_OUTCOME_CONTINUE: return "CATCHUP_CONTINUE";
      case HYBRID_CATCHUP_OUTCOME_FINITE_PASS: return "CATCHUP_FINITE_PASS";
      case HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED: return "CATCHUP_FINAL_CLOSE_PREVIEW_REQUIRED";
      case HYBRID_CATCHUP_OUTCOME_TERMINAL_MIN_VOLUME: return "CATCHUP_TERMINAL_MIN_VOLUME";
      case HYBRID_CATCHUP_OUTCOME_NO_FINITE_LEVEL: return "CATCHUP_NO_FINITE_LEVEL";
      case HYBRID_CATCHUP_OUTCOME_REJECT_STATE: return "CATCHUP_REJECT_STATE";
      case HYBRID_CATCHUP_OUTCOME_REJECT_GEOMETRY: return "CATCHUP_REJECT_GEOMETRY";
      case HYBRID_CATCHUP_OUTCOME_REJECT_MARGIN: return "CATCHUP_REJECT_MARGIN";
      case HYBRID_CATCHUP_OUTCOME_REJECT_TEMPORAL_INVARIANT: return "CATCHUP_REJECT_TEMPORAL";
      case HYBRID_CATCHUP_OUTCOME_REJECT_OUTCOME_DIVERGENCE: return "CATCHUP_OUTCOME_DIVERGENCE";
      case HYBRID_CATCHUP_OUTCOME_REJECT_WORST_NON_ADVERSE: return "CATCHUP_WORST_NON_ADVERSE_RESULT";
      case HYBRID_CATCHUP_OUTCOME_ERROR_BROKER_MONEY: return "CATCHUP_ERROR_BROKER_MONEY";
      case HYBRID_CATCHUP_OUTCOME_ERROR_MARGIN_CALCULATION: return "CATCHUP_ERROR_MARGIN_CALCULATION";
      case HYBRID_CATCHUP_OUTCOME_ERROR_PARTIAL_SOLVER: return "CATCHUP_ERROR_PARTIAL_SOLVER";
      default: return "CATCHUP_ERROR_INTERNAL";
   }
}

HybridCatchUpOutcome SetHybridCatchUpRowOutcome(HybridHarvestLevelResult &row,HybridCatchUpOutcome outcome,string reason)
{
   row.outcome=outcome; row.outcomeClass=ClassifyHybridCatchUpOutcome(outcome);
   row.calculationValid=row.outcomeClass!=HYBRID_CATCHUP_CLASS_ERROR;
   row.continuationAllowed=row.outcomeClass==HYBRID_CATCHUP_CLASS_CONTINUE;
   row.finalClosePreviewRequired=row.outcomeClass==HYBRID_CATCHUP_CLASS_ROUTE;
   row.terminal=row.outcomeClass==HYBRID_CATCHUP_CLASS_TERMINAL;
   row.reject=row.outcomeClass==HYBRID_CATCHUP_CLASS_REJECT;
   row.error=row.outcomeClass==HYBRID_CATCHUP_CLASS_ERROR;
   row.pass=outcome==HYBRID_CATCHUP_OUTCOME_FINITE_PASS;
   row.reasonCode=HybridCatchUpReasonCode(outcome); row.reason=reason;
   return outcome;
}

bool BuildProjectedReopenPrices(Direction bigDirection,double levelBid,double levelAsk,HybridReopenPrices &prices)
{
   ZeroMemory(prices);
   if(bigDirection==DIR_BUY) { prices.coreOpenPrice=levelAsk; prices.trendOpenPrice=levelAsk; prices.smallOpenPrice=levelBid; }
   else if(bigDirection==DIR_SELL) { prices.coreOpenPrice=levelBid; prices.trendOpenPrice=levelBid; prices.smallOpenPrice=levelAsk; }
   else return false;
   return levelBid>0 && levelAsk>=levelBid;
}

bool BuildCatchUpBaseTrigger(const HybridCatchUpState &state,double distancePoints,double &bid,double &ask)
{
   double point=SymbolInfoDouble(state.symbol,SYMBOL_POINT); if(point<=0 || state.baselineSpread<0) return false;
   double distance=distancePoints*point;
   if(state.bigDirection==DIR_BUY) { bid=state.anchorBid+distance; ask=bid+state.baselineSpread; }
   else if(state.bigDirection==DIR_SELL) { ask=state.anchorAsk-distance; bid=ask-state.baselineSpread; }
   else return false;
   return bid>0 && ask>=bid;
}

bool ApplyCatchUpExecutionProfile(double baseBid,double baseAsk,const HybridCatchUpProfile &profile,double point,double &bid,double &ask)
{
   bid=baseBid-profile.bidAdversePoints*point; ask=baseAsk+profile.askAdversePoints*point;
   return point>0 && bid>0 && ask>=bid;
}

ulong HybridCatchUpFingerprint(const HybridCatchUpState &s,HybridCatchUpProfileKind profile)
{
   string value=StringFormat("%s|%I64d|%I64u|%I64u|%d|%d|%.8f|%.10f|%.8f|%.10f|%.8f|%.10f|%.8f|%.10f|%.10f|%.10f|%.10f|%.10f|%.10f|%.2f|%.2f|%.2f|%.2f|%d",
      s.symbol,s.magic,s.cycleId,s.stateRevision,s.levelIndex,(int)s.farDirection,s.farLot,s.farOpenPrice,s.coreLot,s.coreOpenPrice,
      s.trendLot,s.trendOpenPrice,s.smallLot,s.smallOpenPrice,s.anchorMid,s.anchorBid,s.anchorAsk,s.baselineSpread,s.lastExecutionBid,
      s.realizedCyclePL,s.partialFarBudgetAvailable,s.finalReserveReal,s.carryAvailable,(int)profile);
   ulong hash=1469598103934665603;
   for(int i=0;i<StringLen(value);i++) { hash^=(ulong)StringGetCharacter(value,i); hash*=1099511628211; }
   return hash;
}

bool ValidateHybridCatchUpState(const HybridCatchUpState &s,string &reason)
{
   if(s.levelIndex<0 || s.symbol=="" || s.cycleId==0 || s.farDirection==DIR_NONE || s.bigDirection==DIR_NONE || s.smallDirection==DIR_NONE ||
      s.farLot<=0 || s.farOpenPrice<=0 || s.coreLot<=0 || s.coreOpenPrice<=0 || s.trendLot<=0 || s.trendOpenPrice<=0 || s.smallLot<=0 || s.smallOpenPrice<=0 ||
      s.anchorBid<=0 || s.anchorAsk<s.anchorBid || s.baselineSpread<0 || s.partialFarBudgetAvailable<0 || s.finalReserveReal<0 || s.carryAvailable<0 || s.equity<=0 || s.currentMargin<0)
   { reason="CATCHUP_REJECT_STATE"; return false; }
   reason="PASS"; return true;
}

bool HybridCatchUpCurrentLegMoney(Direction direction,double lot,double openPrice,double bid,double ask,bool includeOpenCommission,BrokerMoneyResult &money)
{ return CalcProjectedPositionNetMoney(direction,lot,openPrice,HybridCatchUpClosePrice(direction,bid,ask),includeOpenCommission,true,money); }
bool HybridCatchUpMarginMoney(Direction direction,double lot,double price,BrokerMoneyResult &money)
{ return CalcProjectedMarginMoney(direction==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL,lot,price,money); }

bool HybridCatchUpMarginTransition(const HybridCatchUpState &before,const HybridCatchUpState &after,double partialLot,double executionBid,double executionAsk,double reopenBid,double reopenAsk,HybridHarvestLevelResult &row,const HybridCatchUpProfile &profile)
{
   BrokerMoneyResult oldCore,oldTrend,oldSmall,partial,remain,nextCore,nextTrend,nextSmall;
   double oldBigPrice=HybridMarginControlPrice(before.bigDirection,executionBid,executionAsk);
   double oldSmallPrice=HybridMarginControlPrice(before.smallDirection,executionBid,executionAsk);
   if(!HybridCatchUpMarginMoney(before.bigDirection,before.coreLot,oldBigPrice,oldCore) ||
      !HybridCatchUpMarginMoney(before.bigDirection,before.trendLot,oldBigPrice,oldTrend) ||
      !HybridCatchUpMarginMoney(before.smallDirection,before.smallLot,oldSmallPrice,oldSmall)) return false;
   ResetBrokerMoneyResult(partial);
   if(partialLot>0 && !HybridCatchUpMarginMoney(before.farDirection,partialLot,HybridMarginControlPrice(before.farDirection,executionBid,executionAsk),partial)) return false;
   if(!HybridCatchUpMarginMoney(after.farDirection,after.farLot,HybridMarginControlPrice(after.farDirection,executionBid,executionAsk),remain) ||
      !HybridCatchUpMarginMoney(after.bigDirection,after.coreLot,HybridMarginControlPrice(after.bigDirection,reopenBid,reopenAsk),nextCore) ||
      !HybridCatchUpMarginMoney(after.bigDirection,after.trendLot,HybridMarginControlPrice(after.bigDirection,reopenBid,reopenAsk),nextTrend) ||
      !HybridCatchUpMarginMoney(after.smallDirection,after.smallLot,HybridMarginControlPrice(after.smallDirection,reopenBid,reopenAsk),nextSmall)) return false;
   row.marginBeforeSnapshot=before.currentMargin;
   row.estimatedOldCoreMargin=oldCore.requiredMargin; row.estimatedOldTrendMargin=oldTrend.requiredMargin; row.estimatedOldSmallMargin=oldSmall.requiredMargin;
   row.estimatedPartialFarMarginRelease=partial.requiredMargin;
   row.estimatedReleasedMarginUpper=oldCore.requiredMargin+oldTrend.requiredMargin+oldSmall.requiredMargin+partial.requiredMargin;
   row.remainingFarMargin=remain.requiredMargin; row.nextCoreMargin=nextCore.requiredMargin; row.nextTrendMargin=nextTrend.requiredMargin; row.nextSmallMargin=nextSmall.requiredMargin;
   row.steadyStateMarginUpper=row.remainingFarMargin+row.nextCoreMargin+row.nextTrendMargin+row.nextSmallMargin;
   row.overlapMarginUpper=before.currentMargin+row.nextCoreMargin+row.nextTrendMargin+row.nextSmallMargin;
   row.peakExecutionMarginUpper=HybridCatchUpAssumeMarginOverlap?row.overlapMarginUpper:MathMax(before.currentMargin,row.steadyStateMarginUpper);
   double gatedMargin=row.steadyStateMarginUpper*(1.0+profile.marginSafetyPercent/100.0);
   row.projectedFreeMarginAfter=before.equity-gatedMargin;
   row.marginLevelAfter=gatedMargin>0?before.equity/gatedMargin*100.0:DBL_MAX;
   row.marginUsageAfter=gatedMargin/before.equity*100.0;
   return HybridMoneyGreater(row.projectedFreeMarginAfter,0.0) && HybridPercentGreaterOrEqual(row.marginLevelAfter,MinimumSafeMarginLevel) && HybridPercentLessOrEqual(row.marginUsageAfter,MaxMarginPercent);
}

bool BuildInitialHybridCatchUpState(const HybridCycleSnapshot &snapshot,const HybridCandidatePlan &plan,const HybridCatchUpProfile &profile,HybridCatchUpState &state)
{
   ZeroMemory(state); state.levelIndex=0; state.symbol=snapshot.symbol; state.magic=(long)snapshot.magic; state.cycleId=snapshot.cycleId;
   state.stateRevision=snapshot.stateRevision; state.snapshotTime=snapshot.snapshotTime; state.farDirection=snapshot.farDirection;
   state.farLot=snapshot.farLot; state.farOpenPrice=snapshot.farOpenPrice; state.bigDirection=plan.bigDirection;
   state.coreLot=plan.coreLot; state.trendLot=plan.trendLot; state.smallDirection=plan.smallDirection; state.smallLot=plan.smallLot;
   state.anchorBid=snapshot.bid; state.anchorAsk=snapshot.ask; state.anchorMid=(snapshot.bid+snapshot.ask)/2.0;
   state.baselineSpread=snapshot.ask-snapshot.bid; state.lastExecutionBid=snapshot.bid; state.lastExecutionAsk=snapshot.ask;
   HybridReopenPrices prices; if(!BuildProjectedReopenPrices(plan.bigDirection,snapshot.bid,snapshot.ask,prices)) return false;
   state.coreOpenPrice=prices.coreOpenPrice; state.trendOpenPrice=prices.trendOpenPrice; state.smallOpenPrice=prices.smallOpenPrice;
   state.realizedCyclePL=snapshot.realizedCyclePL; state.partialFarBudgetAvailable=snapshot.partialFarAvailable;
   state.finalReserveReal=snapshot.finalReserveReal; state.equity=snapshot.equity; state.currentMargin=snapshot.margin; state.freeMargin=snapshot.freeMargin;
   state.lastCoverageDeficit=DBL_MAX; state.lastRecoveryPL=-DBL_MAX; state.fingerprint=HybridCatchUpFingerprint(state,profile.kind);
   string reason; return ValidateHybridCatchUpState(state,reason);
}

string HybridFinalCloseRouteFingerprintPayload(const HybridFinalCloseRouteState &s)
{
   BrokerMoneyResult m=s.fullFarCloseMoney;
   return StringFormat("%s|%I64d|%I64u|%I64u|%I64u|%d|%d|%d|%d|%.8f|%.10f|%.10f|%.10f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%.2f|%I64u",
      s.symbol,s.magic,s.cycleId,s.sourceStateRevision,s.routeStateRevision,s.level,(int)s.profileKind,(int)s.farDirection,(int)s.routeCandidate,
      s.farLot,s.farOpenPrice,s.executionBid,s.executionAsk,HybridCatchUpMoneyRound(m.grossProfit),HybridCatchUpMoneyRound(m.openCommission),
      HybridCatchUpMoneyRound(m.closeCommission),HybridCatchUpMoneyRound(m.swap),HybridCatchUpMoneyRound(m.fee),HybridCatchUpMoneyRound(m.slippageCost),
      HybridCatchUpMoneyRound(m.spreadExpansionCost),HybridCatchUpMoneyRound(m.safetyBuffer),HybridCatchUpMoneyRound(m.netMoney),
      HybridCatchUpMoneyRound(s.fullFarLoss),HybridCatchUpMoneyRound(s.harvestNet),HybridCatchUpMoneyRound(s.realizedPLBefore),
      HybridCatchUpMoneyRound(s.realizedPLAfterHarvest),HybridCatchUpMoneyRound(s.partialBudgetBefore),HybridCatchUpMoneyRound(s.partialAdd),
      HybridCatchUpMoneyRound(s.partialBudgetGross),HybridCatchUpMoneyRound(s.reserveBefore),HybridCatchUpMoneyRound(s.reserveAdd),
      HybridCatchUpMoneyRound(s.reserveAfter),HybridCatchUpMoneyRound(s.carryBefore),HybridCatchUpMoneyRound(s.carryAdd),
      HybridCatchUpMoneyRound(s.carryAfter),s.sourceStateFingerprint);
}

ulong HybridFinalCloseRouteFingerprint(const HybridFinalCloseRouteState &s)
{
   string value=HybridFinalCloseRouteFingerprintPayload(s); ulong hash=1469598103934665603;
   for(int i=0;i<StringLen(value);i++) { hash^=(ulong)StringGetCharacter(value,i); hash*=1099511628211; }
   return hash;
}

bool HybridMoneyEqual(double a,double b) { return MathAbs(HybridCatchUpMoneyRound(a)-HybridCatchUpMoneyRound(b))<=MoneyCalculationTolerance; }
bool HybridMoneyGreater(double a,double b) { return a>b+MoneyCalculationTolerance; }
bool HybridMoneyLessOrEqual(double a,double b) { return a<=b+MoneyCalculationTolerance; }
bool HybridMoneyGreaterOrEqual(double a,double b) { return a>=b-MoneyCalculationTolerance; }
double HybridLotTolerance(const string symbol)
{
   double step=SymbolInfoDouble(symbol,SYMBOL_VOLUME_STEP);
   if(step<=0) step=1e-5;
   return MathMax(1e-9,MathMin(VolumeMismatchToleranceLots,step*1e-4));
}
bool HybridLotEqual(const string symbol,double a,double b) { return MathAbs(a-b)<=HybridLotTolerance(symbol); }
bool HybridLotLess(const string symbol,double a,double b) { return a<b-HybridLotTolerance(symbol); }
bool HybridLotLessOrEqual(const string symbol,double a,double b) { return a<=b+HybridLotTolerance(symbol); }
bool HybridLotGreater(const string symbol,double a,double b) { return a>b+HybridLotTolerance(symbol); }
bool HybridLotGreaterOrEqual(const string symbol,double a,double b) { return a>=b-HybridLotTolerance(symbol); }
double HybridPriceTolerance(const string symbol)
{
   double point=SymbolInfoDouble(symbol,SYMBOL_POINT); int digits=(int)SymbolInfoInteger(symbol,SYMBOL_DIGITS);
   if(point<=0 || digits<=0) return 1e-10;
   return MathMax(point*1e-3,MathPow(10.0,-(digits+2)));
}
bool HybridPriceEqual(const string symbol,double a,double b) { return MathAbs(a-b)<=HybridPriceTolerance(symbol); }
double HybridRatioTolerance() { return MathMax(CoverageImprovementTolerance,1e-9); }
bool HybridRatioLess(double a,double b) { return a<b-HybridRatioTolerance(); }
bool HybridRatioGreaterOrEqual(double a,double b) { return a>=b-HybridRatioTolerance(); }
double HybridPercentTolerance() { return 1e-6; }
bool HybridPercentLessOrEqual(double a,double b) { return a<=b+HybridPercentTolerance(); }
bool HybridPercentGreaterOrEqual(double a,double b) { return a>=b-HybridPercentTolerance(); }
bool HybridRouteBrokerMoneyEqual(const BrokerMoneyResult &a,const BrokerMoneyResult &b)
{
   return a.calculationValid==b.calculationValid && HybridMoneyEqual(a.grossProfit,b.grossProfit) &&
      HybridMoneyEqual(a.openCommission,b.openCommission) && HybridMoneyEqual(a.closeCommission,b.closeCommission) &&
      HybridMoneyEqual(a.swap,b.swap) && HybridMoneyEqual(a.fee,b.fee) && HybridMoneyEqual(a.slippageCost,b.slippageCost) &&
      HybridMoneyEqual(a.spreadExpansionCost,b.spreadExpansionCost) && HybridMoneyEqual(a.safetyBuffer,b.safetyBuffer) && HybridMoneyEqual(a.netMoney,b.netMoney);
}

bool ValidateHybridFinalCloseRouteState(const HybridCatchUpState &before,const HybridHarvestLevelResult &row,const HybridPartialFarPreviewResult &partial,const HybridFinalCloseRouteState &route,string &reasonCode,string &reason)
{
   reasonCode="CATCHUP_ROUTE_STATE_VALID"; reason="PASS";
   if(route.symbol=="" || route.symbol!=before.symbol || route.magic!=before.magic || route.cycleId==0 || route.cycleId!=before.cycleId ||
      (route.profileKind!=HYBRID_CATCHUP_BASE && route.profileKind!=HYBRID_CATCHUP_WORST) || route.level!=before.levelIndex+1)
   { reasonCode="CATCHUP_ROUTE_IDENTITY_INVALID"; reason="Route identity mismatch"; return false; }
   if(route.farDirection==DIR_NONE || route.farDirection!=before.farDirection || route.farLot<=0 || !HybridLotEqual(before.symbol,route.farLot,before.farLot) ||
      route.farOpenPrice<=0 || !HybridPriceEqual(before.symbol,route.farOpenPrice,before.farOpenPrice))
   { reasonCode="CATCHUP_ROUTE_FAR_INVALID"; reason="Route Far mismatch"; return false; }
   if(route.executionBid<=0 || route.executionAsk<route.executionBid || !HybridPriceEqual(before.symbol,route.executionBid,row.triggerBid) || !HybridPriceEqual(before.symbol,route.executionAsk,row.triggerAsk))
   { reasonCode="CATCHUP_ROUTE_EXECUTION_PRICE_INVALID"; reason="Execution price mismatch"; return false; }
   if(!partial.fullFarCloseMoney.calculationValid || !HybridRouteBrokerMoneyEqual(route.fullFarCloseMoney,partial.fullFarCloseMoney) ||
      !HybridMoneyEqual(route.fullFarLoss,MathMax(-route.fullFarCloseMoney.netMoney,0.0)))
   { reasonCode="CATCHUP_ROUTE_FULL_FAR_MONEY_INVALID"; reason="Full Far money mismatch"; return false; }
   if(!partial.calculationValid || !partial.finalClosePreviewRouteCandidate || !partial.partialBudgetCanCoverFullFarLoss || partial.partialCloseAvailable ||
      !HybridLotEqual(before.symbol,partial.rawCloseLot,0.0) || !HybridLotEqual(before.symbol,partial.normalizedCloseLot,0.0) ||
      !HybridLotEqual(before.symbol,partial.farLotBefore,before.farLot) || !HybridLotEqual(before.symbol,partial.farLotAfter,before.farLot) ||
      !HybridMoneyEqual(partial.budgetConsumed,0.0) || !HybridMoneyEqual(partial.budgetAfter,partial.budgetGross) ||
      !HybridMoneyEqual(partial.partialCloseMoney.netMoney,0.0) || !partial.remainderVolumeValid || !partial.budgetConservationPass)
   { reasonCode="CATCHUP_ROUTE_PARTIAL_POLICY_VIOLATION"; reason="Partial policy changed route state"; return false; }
   if(!HybridMoneyEqual(route.realizedPLBefore,before.realizedCyclePL) || !HybridMoneyEqual(route.harvestNet,row.harvestNet) ||
      !HybridMoneyEqual(route.realizedPLAfterHarvest,HybridCatchUpMoneyRound(before.realizedCyclePL+row.harvestNet)))
   { reasonCode="CATCHUP_ROUTE_REALIZED_PL_INVALID"; reason="Realized PL mismatch"; return false; }
   if(!HybridMoneyEqual(route.partialBudgetBefore,before.partialFarBudgetAvailable) || !HybridMoneyEqual(route.partialAdd,row.partialAdd) ||
      !HybridMoneyEqual(route.partialBudgetGross,HybridCatchUpMoneyRound(before.partialFarBudgetAvailable+row.partialAdd)) ||
      !HybridMoneyEqual(route.partialBudgetGross,partial.budgetGross) || !HybridMoneyEqual(route.partialBudgetGross,partial.budgetAfter))
   { reasonCode="CATCHUP_ROUTE_PARTIAL_BUDGET_INVALID"; reason="Partial budget mismatch"; return false; }
   if(!HybridMoneyEqual(route.reserveBefore,before.finalReserveReal) || !HybridMoneyEqual(route.reserveAdd,row.reserveAdd) ||
      !HybridMoneyEqual(route.reserveAfter,HybridCatchUpMoneyRound(before.finalReserveReal+row.reserveAdd)))
   { reasonCode="CATCHUP_ROUTE_RESERVE_INVALID"; reason="Reserve mismatch"; return false; }
   if(!HybridMoneyEqual(route.carryBefore,before.carryAvailable) || !HybridMoneyEqual(route.carryAdd,row.carryAdd) ||
      !HybridMoneyEqual(route.carryAfter,HybridCatchUpMoneyRound(before.carryAvailable+row.carryAdd)))
   { reasonCode="CATCHUP_ROUTE_CARRY_INVALID"; reason="Carry mismatch"; return false; }
   if(!row.currentLegMoneyEvaluated || !row.harvestAllocationEvaluated || !row.fullFarAffordabilityEvaluated || row.partialFarEvaluated ||
      row.nextBasketEvaluated || row.nextBasketGeometryEvaluated || row.nextBasketMarginEvaluated || row.recoveryAfterReopenEvaluated ||
      !HybridLotEqual(before.symbol,row.farLotClosed,0.0) || !HybridLotEqual(before.symbol,row.farLotAfter,before.farLot) ||
      !HybridMoneyEqual(row.partialConsumed,0.0) || !HybridMoneyEqual(row.realizedPLAfterPartial,row.realizedPLAfterHarvest))
   { reasonCode="CATCHUP_ROUTE_STAGE_FLAGS_INVALID"; reason="Route stage flags invalid"; return false; }
   if(!route.routeCandidate || route.routeCandidate!=partial.finalClosePreviewRouteCandidate)
   { reasonCode="CATCHUP_ROUTE_CANDIDATE_INVALID"; reason="Route candidate mismatch"; return false; }
   if(route.sourceStateRevision!=before.stateRevision || route.routeStateRevision!=before.stateRevision+1)
   { reasonCode="CATCHUP_ROUTE_REVISION_INVALID"; reason="Route revision mismatch"; return false; }
   if(route.sourceStateFingerprint!=before.fingerprint || route.routeStateFingerprint==0 || route.routeStateFingerprint!=HybridFinalCloseRouteFingerprint(route))
   { reasonCode="CATCHUP_ROUTE_FINGERPRINT_INVALID"; reason="Route fingerprint mismatch"; return false; }
   return true;
}

bool BuildHybridFinalCloseRouteState(const HybridCatchUpState &before,const HybridHarvestLevelResult &row,const HybridPartialFarPreviewResult &partial,const HybridCatchUpProfile &profile,HybridFinalCloseRouteState &route)
{
   ZeroMemory(route); route.routeCandidate=partial.finalClosePreviewRouteCandidate; route.symbol=before.symbol; route.magic=before.magic;
   route.cycleId=before.cycleId; route.sourceStateRevision=before.stateRevision; route.routeStateRevision=before.stateRevision+1; route.level=row.level; route.profileKind=profile.kind;
   route.farDirection=before.farDirection; route.farLot=before.farLot; route.farOpenPrice=before.farOpenPrice;
   route.executionBid=row.triggerBid; route.executionAsk=row.triggerAsk; route.fullFarCloseMoney=partial.fullFarCloseMoney;
   route.fullFarLoss=partial.fullFarLoss; route.harvestNet=row.harvestNet; route.realizedPLBefore=before.realizedCyclePL;
   route.realizedPLAfterHarvest=row.realizedPLAfterHarvest; route.partialBudgetBefore=before.partialFarBudgetAvailable;
   route.partialAdd=row.partialAdd; route.partialBudgetGross=partial.budgetGross; route.reserveBefore=before.finalReserveReal;
   route.reserveAdd=row.reserveAdd; route.reserveAfter=HybridCatchUpMoneyRound(before.finalReserveReal+row.reserveAdd);
   route.carryBefore=before.carryAvailable; route.carryAdd=row.carryAdd; route.carryAfter=HybridCatchUpMoneyRound(before.carryAvailable+row.carryAdd);
   route.sourceStateFingerprint=before.fingerprint; route.routeStateFingerprint=HybridFinalCloseRouteFingerprint(route);
   string code,reason; route.validationPass=ValidateHybridFinalCloseRouteState(before,row,partial,route,code,reason);
   route.calculationValid=route.validationPass; route.validationCode=code; route.reasonCode=code; route.reason=reason;
   return route.validationPass;
}

HybridCatchUpOutcome EvaluateHybridCatchUpLevel(const HybridCatchUpState &before,const HybridCatchUpProfile &profile,HybridHarvestLevelResult &row,HybridCatchUpState &after)
{
   ZeroMemory(row); ZeroMemory(after); row.level=before.levelIndex+1;
   string validation; if(!ValidateHybridCatchUpState(before,validation)) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_REJECT_STATE,validation);
   row.stateBeforeFingerprint=before.fingerprint; row.farLotBefore=before.farLot; row.farOpenPrice=before.farOpenPrice;
   row.coreLot=before.coreLot; row.coreOpenPrice=before.coreOpenPrice; row.trendLot=before.trendLot; row.trendOpenPrice=before.trendOpenPrice;
   row.smallLot=before.smallLot; row.smallOpenPrice=before.smallOpenPrice; row.partialBudgetBefore=before.partialFarBudgetAvailable;
   row.reserveBefore=before.finalReserveReal; row.carryBefore=before.carryAvailable; row.realizedPLBefore=before.realizedCyclePL;
   row.baselineSpread=before.baselineSpread; row.cumulativeSpreadStress=profile.cumulativeSpreadStress;
   double distance=before.levelIndex==0?BigMoveStartPoints:BigMoveStepPoints;
   if(!BuildCatchUpBaseTrigger(before,distance,row.baseTriggerBid,row.baseTriggerAsk)) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_ERROR_INTERNAL,"Trigger geometry failed");
   double point=SymbolInfoDouble(before.symbol,SYMBOL_POINT);
   if(!ApplyCatchUpExecutionProfile(row.baseTriggerBid,row.baseTriggerAsk,profile,point,row.triggerBid,row.triggerAsk)) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_ERROR_INTERNAL,"Execution profile failed");
   row.executionSpread=row.triggerAsk-row.triggerBid;
   bool includeOpen=!before.openCommissionAlreadyRealized;
   if(!HybridCatchUpCurrentLegMoney(before.bigDirection,before.coreLot,before.coreOpenPrice,row.triggerBid,row.triggerAsk,includeOpen,row.coreClose) ||
      !HybridCatchUpCurrentLegMoney(before.bigDirection,before.trendLot,before.trendOpenPrice,row.triggerBid,row.triggerAsk,includeOpen,row.trendClose) ||
      !HybridCatchUpCurrentLegMoney(before.smallDirection,before.smallLot,before.smallOpenPrice,row.triggerBid,row.triggerAsk,includeOpen,row.smallClose))
      return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_ERROR_BROKER_MONEY,"Current leg money failed");
   row.currentLegMoneyEvaluated=true;
   row.harvestNet=HybridCatchUpMoneyRound(row.coreClose.netMoney+row.trendClose.netMoney+row.smallClose.netMoney); row.eligibleHarvest=MathMax(row.harvestNet,0.0);
   row.partialAdd=HybridCatchUpMoneyRound(HybridPartialFarShare*row.eligibleHarvest); row.reserveAdd=HybridCatchUpMoneyRound(HybridFinalReserveShare*row.eligibleHarvest);
   double carryBase=HybridCatchUpMoneyRound(HybridCarryShare*row.eligibleHarvest);
   row.carryAdd=HybridCatchUpMoneyRound(carryBase+HybridCatchUpMoneyRound(row.eligibleHarvest-row.partialAdd-row.reserveAdd-carryBase));
   row.allocationPass=MathAbs(row.partialAdd+row.reserveAdd+row.carryAdd-row.eligibleHarvest)<=MoneyCalculationTolerance;
   if(!row.allocationPass) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_ERROR_INTERNAL,"Allocation conservation failed");
   row.harvestAllocationEvaluated=true;
   double budgetGross=HybridCatchUpMoneyRound(before.partialFarBudgetAvailable+row.partialAdd); HybridPartialFarPreviewResult partial;
   if(!SolveHybridPartialFarPreview(before,budgetGross,row.triggerBid,row.triggerAsk,partial)) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_ERROR_PARTIAL_SOLVER,partial.reason);
   row.fullFarAffordabilityEvaluated=true; row.partialBudgetCanCoverFullFarLoss=partial.partialBudgetCanCoverFullFarLoss;
   row.finalClosePreviewRouteCandidate=partial.finalClosePreviewRouteCandidate; row.fullFarNet=partial.fullFarCloseMoney.netMoney;
   row.fullFarLoss=partial.fullFarLoss; row.partialBudgetGross=partial.budgetGross;
   row.realizedPLAfterHarvest=HybridCatchUpMoneyRound(before.realizedCyclePL+row.harvestNet);
   if(partial.finalClosePreviewRouteCandidate)
   {
      row.farLotClosed=0; row.farLotAfter=before.farLot; row.partialConsumed=0; row.partialBudgetAfter=partial.budgetAfter;
      row.partialBudgetPass=partial.budgetConservationPass; row.realizedPLAfterPartial=row.realizedPLAfterHarvest;
      row.realizedPLForFinalClosePreview=row.realizedPLAfterHarvest;
      row.reserveAfter=HybridCatchUpMoneyRound(before.finalReserveReal+row.reserveAdd);
      row.carryAfter=HybridCatchUpMoneyRound(before.carryAvailable+row.carryAdd);
      if(!BuildHybridFinalCloseRouteState(before,row,partial,profile,row.finalCloseRouteState))
         return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_ERROR_INTERNAL,"CATCHUP_ROUTE_STATE_BUILD_FAILED");
      return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED,"Full Far loss affordable; route state preserved before Partial Far");
   }
   row.partialFarEvaluated=true; row.farLotClosed=partial.normalizedCloseLot; row.farLotAfter=partial.farLotAfter;
   row.partialFarClose=partial.partialCloseMoney; row.partialConsumed=partial.budgetConsumed; row.partialBudgetAfter=partial.budgetAfter; row.partialBudgetPass=partial.budgetConservationPass;
   double partialNet=partial.partialCloseAvailable?partial.partialCloseMoney.netMoney:0.0;
   row.realizedPLAfterPartial=HybridCatchUpMoneyRound(row.realizedPLAfterHarvest+partialNet);
   if(!row.partialBudgetPass) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_ERROR_PARTIAL_SOLVER,"Partial budget conservation failed");
   if(!partial.remainderVolumeValid) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_TERMINAL_MIN_VOLUME,"Invalid Far remainder");
   after=before; after.levelIndex=before.levelIndex+1; after.stateRevision=before.stateRevision+1; after.farLot=row.farLotAfter;
   after.realizedCyclePL=row.realizedPLAfterPartial; after.partialFarBudgetAvailable=row.partialBudgetAfter;
   after.finalReserveReal=HybridCatchUpMoneyRound(before.finalReserveReal+row.reserveAdd); after.carryAvailable=HybridCatchUpMoneyRound(before.carryAvailable+row.carryAdd);
   after.cumulativeHarvestNet=HybridCatchUpMoneyRound(before.cumulativeHarvestNet+row.harvestNet); after.cumulativePartialFarNet=HybridCatchUpMoneyRound(before.cumulativePartialFarNet+partialNet);
   after.anchorBid=row.baseTriggerBid; after.anchorAsk=row.baseTriggerAsk; after.anchorMid=(row.baseTriggerBid+row.baseTriggerAsk)/2.0;
   after.baselineSpread=before.baselineSpread; after.lastExecutionBid=row.triggerBid; after.lastExecutionAsk=row.triggerAsk;
   row.reserveAfter=after.finalReserveReal; row.carryAfter=after.carryAvailable;
   double minLot=SymbolInfoDouble(before.symbol,SYMBOL_VOLUME_MIN);
   if(HybridLotLess(before.symbol,after.farLot,minLot)) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_TERMINAL_MIN_VOLUME,"Far below minimum");
   after.coreLot=NormalizeHybridCoreLot(after.farLot*BigCoreRatio); after.trendLot=NormalizeHybridTrendLot(after.farLot*BigTrendRatio); after.smallLot=NormalizeHybridSmallLot(after.farLot*SmallBaseToFarRatio);
   row.nextBasketEvaluated=true;
   row.nextCoreLot=after.coreLot; row.nextTrendLot=after.trendLot; row.nextSmallLot=after.smallLot;
   row.nextStatePass=HybridLotGreaterOrEqual(before.symbol,after.coreLot,minLot) && HybridLotGreaterOrEqual(before.symbol,after.trendLot,minLot) && HybridLotGreaterOrEqual(before.symbol,after.smallLot,minLot);
   if(!row.nextStatePass) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_TERMINAL_MIN_VOLUME,"Next basket below minimum");
   double kr=HybridFinalReserveShare*(after.coreLot+after.trendLot-after.smallLot)/after.farLot, slope=after.coreLot+after.trendLot-after.smallLot-after.farLot;
   double maximumAllowedNewBigLot=before.farLot*MaximumNewBigToOldFarRatio;
   if(HybridRatioLess(kr,MinimumReserveCatchUpRatio) || !HybridLotGreater(before.symbol,slope,0.0) || HybridLotGreaterOrEqual(before.symbol,after.coreLot+after.trendLot,maximumAllowedNewBigLot))
      return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_REJECT_GEOMETRY,"Next basket geometry failed");
   row.nextBasketGeometryEvaluated=true;
   HybridReopenPrices reopen; if(!BuildProjectedReopenPrices(after.bigDirection,row.baseTriggerBid,row.baseTriggerAsk,reopen)) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_REJECT_GEOMETRY,"Reopen prices failed");
   after.coreOpenPrice=reopen.coreOpenPrice; after.trendOpenPrice=reopen.trendOpenPrice; after.smallOpenPrice=reopen.smallOpenPrice;
   row.nextAnchorBid=row.baseTriggerBid; row.nextAnchorAsk=row.baseTriggerAsk;
   if(!HybridPartialFarCloseMoney(after,after.farLot,row.triggerBid,row.triggerAsk,row.remainingFar)) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_ERROR_BROKER_MONEY,"Remaining Far money failed");
   row.remainingFarCloseCost=HybridCatchUpMoneyRound(MathMax(-row.remainingFar.netMoney,0.0)+HybridCoverageSafetyBufferMoney);
   row.coverageDeficit=HybridCatchUpMoneyRound(row.remainingFarCloseCost-after.finalReserveReal); row.coveragePass=row.coverageDeficit<=MoneyCalculationTolerance;
   row.recoveryAfterPartial=HybridCatchUpMoneyRound(after.realizedCyclePL+row.remainingFar.netMoney); BrokerMoneyResult nextCore,nextTrend,nextSmall;
   if(!HybridCatchUpCurrentLegMoney(after.bigDirection,after.coreLot,after.coreOpenPrice,row.baseTriggerBid,row.baseTriggerAsk,true,nextCore) ||
      !HybridCatchUpCurrentLegMoney(after.bigDirection,after.trendLot,after.trendOpenPrice,row.baseTriggerBid,row.baseTriggerAsk,true,nextTrend) ||
      !HybridCatchUpCurrentLegMoney(after.smallDirection,after.smallLot,after.smallOpenPrice,row.baseTriggerBid,row.baseTriggerAsk,true,nextSmall))
      return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_ERROR_BROKER_MONEY,"Reopen money failed");
   row.recoveryAfterReopen=HybridCatchUpMoneyRound(after.realizedCyclePL+row.remainingFar.netMoney+nextCore.netMoney+nextTrend.netMoney+nextSmall.netMoney);
   row.recoveryAfterReopenEvaluated=true;
   row.recoveryPass=row.recoveryAfterReopen+MoneyCalculationTolerance>=MinimumRecoveryProfitMoney;
   row.marginPass=HybridCatchUpMarginTransition(before,after,row.farLotClosed,row.triggerBid,row.triggerAsk,row.baseTriggerBid,row.baseTriggerAsk,row,profile);
   row.nextBasketMarginEvaluated=true;
   if(!row.marginPass) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_REJECT_MARGIN,"Conservative margin gate failed");
   after.currentMargin=row.steadyStateMarginUpper; after.freeMargin=after.equity-after.currentMargin;
   bool farDidNotIncrease=HybridLotLessOrEqual(before.symbol,after.farLot,before.farLot);
   bool noPartialClose=HybridLotEqual(before.symbol,row.farLotClosed,0.0);
   bool farStrictlyCompressed=HybridLotLess(before.symbol,after.farLot,before.farLot);
   row.temporalPass=after.finalReserveReal+MoneyCalculationTolerance>=before.finalReserveReal && farDidNotIncrease &&
      (noPartialClose || farStrictlyCompressed) &&
      (before.levelIndex==0 || row.coverageDeficit<=before.lastCoverageDeficit-HybridMinimumCoverageGainMoney+MoneyCalculationTolerance) &&
      (before.levelIndex==0 || HybridMoneyGreaterOrEqual(row.recoveryAfterReopen+HybridAllowedMarketCostDeteriorationMoney,before.lastRecoveryPL));
   if(!row.temporalPass) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_REJECT_TEMPORAL_INVARIANT,"Temporal invariant failed");
   after.lastCoverageDeficit=row.coverageDeficit; after.lastRecoveryPL=row.recoveryAfterReopen; after.projectedOpenCommissionIncluded=true;
   after.cumulativeOpeningCosts=HybridCatchUpMoneyRound(before.cumulativeOpeningCosts+nextCore.openCommission+nextTrend.openCommission+nextSmall.openCommission);
   after.fingerprint=HybridCatchUpFingerprint(after,profile.kind); row.stateAfterFingerprint=after.fingerprint; row.stateAfter=after;
   row.continuationStateValid=true;
   if(row.coveragePass && row.recoveryPass) return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_FINITE_PASS,"Finite Catch-Up gates passed");
   return SetHybridCatchUpRowOutcome(row,HYBRID_CATCHUP_OUTCOME_CONTINUE,!row.coveragePass?"Remaining Far not covered":"Recovery threshold not reached");
}

bool HybridWorstCurrentLegsAreAdverse(const string symbol,const HybridHarvestLevelResult &base,const HybridHarvestLevelResult &worst)
{
   double priceTolerance=HybridPriceTolerance(symbol);
   return worst.triggerBid<=base.triggerBid+priceTolerance && worst.triggerAsk+priceTolerance>=base.triggerAsk &&
      worst.coreClose.netMoney<=base.coreClose.netMoney+MoneyCalculationTolerance && worst.trendClose.netMoney<=base.trendClose.netMoney+MoneyCalculationTolerance && worst.smallClose.netMoney<=base.smallClose.netMoney+MoneyCalculationTolerance;
}
bool HybridWorstFullFarIsAdverse(const string symbol,const HybridHarvestLevelResult &base,const HybridHarvestLevelResult &worst)
{
   if(!base.fullFarAffordabilityEvaluated || !worst.fullFarAffordabilityEvaluated) return true;
   double pt=HybridPriceTolerance(symbol);
   bool lossAdverse=HybridMoneyGreaterOrEqual(worst.fullFarLoss,base.fullFarLoss);
   bool executionAdverse=worst.triggerBid<=base.triggerBid+pt && worst.triggerAsk+pt>=base.triggerAsk;
   return lossAdverse && executionAdverse &&
      HybridLotEqual(symbol,base.farLotBefore,worst.farLotBefore) && HybridPriceEqual(symbol,base.farOpenPrice,worst.farOpenPrice);
}
bool HybridWorstRowIsAdverse(const string symbol,const HybridHarvestLevelResult &base,const HybridHarvestLevelResult &worst)
{ return HybridWorstCurrentLegsAreAdverse(symbol,base,worst) && HybridWorstFullFarIsAdverse(symbol,base,worst); }

string HybridCatchUpTraceRow(const HybridHarvestLevelResult &r,string profile)
{
   string trace=StringFormat("HYBRID_CATCHUP_LEVEL|Profile=%s|Level=%d|Outcome=%d|OutcomeClass=%d|CalculationValid=%d|ContinuationAllowed=%d|FinalClosePreviewRequired=%d|Terminal=%d|Reject=%d|Error=%d|StateBeforeFingerprint=%I64u|StateAfterFingerprint=%I64u|BaseTriggerBid=%.10f|BaseTriggerAsk=%.10f|ExecutionBid=%.10f|ExecutionAsk=%.10f|BaselineSpread=%.10f|ExecutionSpread=%.10f|CumulativeSpreadStress=%d|FullFarAffordabilityEvaluated=%d|PartialBudgetCanCoverFullFarLoss=%d|FinalClosePreviewRouteCandidate=%d|FullFarNet=%.2f|FullFarLoss=%.2f|PartialFarEvaluated=%d|FarLotBefore=%.8f|FarCloseLot=%.8f|FarLotAfter=%.8f|FarLotForFinalClosePreview=%.8f|HarvestNet=%.2f|PartialBudgetBefore=%.2f|PartialAdd=%.2f|PartialBudgetGross=%.2f|PartialConsumed=%.2f|PartialBudgetAfter=%.2f|PartialBudgetForFinalClosePreview=%.2f|ReserveAfter=%.2f|ReserveForFinalClosePreview=%.2f|CarryAfter=%.2f|CarryForFinalClosePreview=%.2f|RealizedAfterHarvest=%.2f|RealizedForFinalClosePreview=%.2f|RealizedAfterPartial=%.2f|NextBasketEvaluated=%d|NextBasketGeometryEvaluated=%d|NextBasketMarginEvaluated=%d|RecoveryAfterReopenEvaluated=%d|RouteStateFingerprint=%I64u|RemainingFarCost=%.2f|CoverageDeficit=%.2f|RecoveryAfterReopen=%.2f|MarginBeforeSnapshot=%.2f|EstimatedReleasedMarginUpper=%.2f|RemainingFarMargin=%.2f|NextCoreMargin=%.2f|NextTrendMargin=%.2f|NextSmallMargin=%.2f|SteadyStateMarginUpper=%.2f|PeakExecutionMarginUpper=%.2f|OverlapMarginUpper=%.2f|MarginLevelAfter=%.2f|MarginUsageAfter=%.2f|ProjectedFreeMarginAfter=%.2f|ReasonCode=%s|Reason=%s;",
      profile,r.level,(int)r.outcome,(int)r.outcomeClass,(int)r.calculationValid,(int)r.continuationAllowed,(int)r.finalClosePreviewRequired,(int)r.terminal,(int)r.reject,(int)r.error,
      r.stateBeforeFingerprint,r.stateAfterFingerprint,r.baseTriggerBid,r.baseTriggerAsk,r.triggerBid,r.triggerAsk,r.baselineSpread,r.executionSpread,(int)r.cumulativeSpreadStress,
      (int)r.fullFarAffordabilityEvaluated,(int)r.partialBudgetCanCoverFullFarLoss,(int)r.finalClosePreviewRouteCandidate,r.fullFarNet,r.fullFarLoss,(int)r.partialFarEvaluated,
      r.farLotBefore,r.farLotClosed,r.farLotAfter,r.finalCloseRouteState.farLot,r.harvestNet,r.partialBudgetBefore,r.partialAdd,r.partialBudgetGross,r.partialConsumed,r.partialBudgetAfter,r.finalCloseRouteState.partialBudgetGross,r.reserveAfter,r.finalCloseRouteState.reserveAfter,r.carryAfter,r.finalCloseRouteState.carryAfter,
      r.realizedPLAfterHarvest,r.realizedPLForFinalClosePreview,r.realizedPLAfterPartial,(int)r.nextBasketEvaluated,(int)r.nextBasketGeometryEvaluated,(int)r.nextBasketMarginEvaluated,(int)r.recoveryAfterReopenEvaluated,r.finalCloseRouteState.routeStateFingerprint,
      r.remainingFarCloseCost,r.coverageDeficit,r.recoveryAfterReopen,r.marginBeforeSnapshot,r.estimatedReleasedMarginUpper,r.remainingFarMargin,
      r.nextCoreMargin,r.nextTrendMargin,r.nextSmallMargin,r.steadyStateMarginUpper,r.peakExecutionMarginUpper,r.overlapMarginUpper,r.marginLevelAfter,r.marginUsageAfter,r.projectedFreeMarginAfter,r.reasonCode,r.reason);
   BrokerMoneyResult m=r.finalCloseRouteState.fullFarCloseMoney;
   trace+=StringFormat("CurrentLegMoneyEvaluated=%d|HarvestAllocationEvaluated=%d|FullFarAdverseEvaluated=%d|FullFarAdversePass=%d|ContinuationStateValid=%d|RouteStateCalculationValid=%d|RouteStateValidationPass=%d|RouteStateValidationCode=%s|SourceStateRevision=%I64u|RouteStateRevision=%I64u|RouteFingerprintPayloadHash=%I64u|FullFarGrossProfit=%.2f|FullFarOpenCommission=%.2f|FullFarCloseCommission=%.2f|FullFarSwap=%.2f|FullFarFee=%.2f|FullFarSlippageCost=%.2f|FullFarNetMoney=%.2f;",(int)r.currentLegMoneyEvaluated,(int)r.harvestAllocationEvaluated,(int)r.fullFarAdverseEvaluated,(int)r.fullFarAdversePass,(int)r.continuationStateValid,(int)r.finalCloseRouteState.calculationValid,(int)r.finalCloseRouteState.validationPass,r.finalCloseRouteState.validationCode,r.finalCloseRouteState.sourceStateRevision,r.finalCloseRouteState.routeStateRevision,HybridFinalCloseRouteFingerprint(r.finalCloseRouteState),m.grossProfit,m.openCommission,m.closeCommission,m.swap,m.fee,m.slippageCost,m.netMoney);
   return trace;
}

HybridCatchUpOutcome SetHybridCatchUpResultOutcome(HybridCatchUpResult &result,HybridCatchUpOutcome outcome,string reason)
{
   result.outcome=outcome; result.outcomeClass=ClassifyHybridCatchUpOutcome(outcome); result.calculationValid=result.outcomeClass!=HYBRID_CATCHUP_CLASS_ERROR;
   result.finiteCatchUpPass=outcome==HYBRID_CATCHUP_OUTCOME_FINITE_PASS; result.pass=result.finiteCatchUpPass;
   result.finalClosePreviewRequired=result.outcomeClass==HYBRID_CATCHUP_CLASS_ROUTE; result.terminal=result.outcomeClass==HYBRID_CATCHUP_CLASS_TERMINAL;
   result.reject=result.outcomeClass==HYBRID_CATCHUP_CLASS_REJECT; result.error=result.outcomeClass==HYBRID_CATCHUP_CLASS_ERROR;
   result.reasonCode=HybridCatchUpReasonCode(outcome); result.reason=reason; return outcome;
}

HybridCatchUpOutcome EvaluateHybridFiniteCatchUpPreviewTyped(const HybridCycleSnapshot &snapshot,const HybridCandidatePlan &plan,HybridCatchUpResult &result)
{
   ZeroMemory(result); result.finiteLevel=-1; result.routedAtLevel=-1; result.terminalAtLevel=-1; result.rejectedAtLevel=-1; result.errorAtLevel=-1;
   ArrayResize(result.baseLevels,0); ArrayResize(result.worstLevels,0); HybridCatchUpProfile baseProfile,worstProfile; ZeroMemory(baseProfile); ZeroMemory(worstProfile);
   baseProfile.kind=HYBRID_CATCHUP_BASE; worstProfile.kind=HYBRID_CATCHUP_WORST;
   worstProfile.bidAdversePoints=SpreadExpansionBufferPoints+MaxSlippagePoints*SlippageSafetyMultiplier+HybridGapBufferPoints;
   worstProfile.askAdversePoints=worstProfile.bidAdversePoints; worstProfile.marginSafetyPercent=HybridCatchUpMarginSafetyPercent;
   baseProfile.cumulativeSpreadStress=false; worstProfile.cumulativeSpreadStress=false;
   HybridCatchUpState baseState,worstState;
   if(!BuildInitialHybridCatchUpState(snapshot,plan,baseProfile,baseState) || !BuildInitialHybridCatchUpState(snapshot,plan,worstProfile,worstState))
      return SetHybridCatchUpResultOutcome(result,HYBRID_CATCHUP_OUTCOME_REJECT_STATE,"Initial Catch-Up state invalid");
   for(int level=1;level<=MaxHarvestLevels;level++)
   {
      HybridHarvestLevelResult baseRow,worstRow; HybridCatchUpState nextBase,nextWorst;
      HybridCatchUpOutcome baseOutcome=EvaluateHybridCatchUpLevel(baseState,baseProfile,baseRow,nextBase);
      HybridCatchUpOutcome worstOutcome=EvaluateHybridCatchUpLevel(worstState,worstProfile,worstRow,nextWorst);
      baseRow.fullFarAdverseEvaluated=baseRow.fullFarAffordabilityEvaluated && worstRow.fullFarAffordabilityEvaluated;
      worstRow.fullFarAdverseEvaluated=baseRow.fullFarAdverseEvaluated;
      baseRow.fullFarAdversePass=baseRow.fullFarAdverseEvaluated && HybridWorstFullFarIsAdverse(snapshot.symbol,baseRow,worstRow);
      worstRow.fullFarAdversePass=baseRow.fullFarAdversePass;
      if(baseRow.currentLegMoneyEvaluated && worstRow.currentLegMoneyEvaluated && !HybridWorstRowIsAdverse(snapshot.symbol,baseRow,worstRow))
         worstOutcome=SetHybridCatchUpRowOutcome(worstRow,HYBRID_CATCHUP_OUTCOME_REJECT_WORST_NON_ADVERSE,"Worst execution improved a projected leg");
      ArrayResize(result.baseLevels,level); ArrayResize(result.worstLevels,level); result.baseLevels[level-1]=baseRow; result.worstLevels[level-1]=worstRow;
      result.evaluatedLevels=level; result.baseOutcome=baseOutcome; result.worstOutcome=worstOutcome;
      result.trace+=HybridCatchUpTraceRow(baseRow,"BASE")+HybridCatchUpTraceRow(worstRow,"WORST"); result.finalBaseState=nextBase; result.finalWorstState=nextWorst;
      result.finalBaseStateValid=baseRow.continuationStateValid; result.finalWorstStateValid=worstRow.continuationStateValid;
      result.finalCoverageDeficit=baseRow.coverageDeficit; result.finalRecoveryPL=baseRow.recoveryAfterReopen;
      HybridCatchUpOutcome aggregate=CombineHybridCatchUpOutcomes(baseOutcome,worstOutcome); HybridCatchUpOutcomeClass cls=ClassifyHybridCatchUpOutcome(aggregate);
      if(aggregate==HYBRID_CATCHUP_OUTCOME_FINITE_PASS) { result.finiteLevel=level; return SetHybridCatchUpResultOutcome(result,aggregate,"Base and Worst finite gates passed"); }
      if(aggregate==HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED)
      {
         result.routedAtLevel=level; result.finalCloseRouteBaseState=baseRow.finalCloseRouteState;
         result.finalCloseRouteWorstState=worstRow.finalCloseRouteState;
         result.finalBaseStateValid=false; result.finalWorstStateValid=false;
         result.finalCloseRouteStatesValid=baseRow.finalCloseRouteState.calculationValid && worstRow.finalCloseRouteState.calculationValid;
         if(!result.finalCloseRouteStatesValid) return SetHybridCatchUpResultOutcome(result,HYBRID_CATCHUP_OUTCOME_ERROR_INTERNAL,"CATCHUP_ROUTE_STATE_INVALID");
         return SetHybridCatchUpResultOutcome(result,aggregate,"Base and Worst route to Final Close preview");
      }
      if(cls==HYBRID_CATCHUP_CLASS_ERROR) { result.errorAtLevel=level; result.failedProfile=ClassifyHybridCatchUpOutcome(baseOutcome)==cls?"BASE":"WORST"; return SetHybridCatchUpResultOutcome(result,aggregate,"Catch-Up calculation error"); }
      if(cls==HYBRID_CATCHUP_CLASS_TERMINAL) { result.terminalAtLevel=level; return SetHybridCatchUpResultOutcome(result,aggregate,"Catch-Up terminal state"); }
      if(cls==HYBRID_CATCHUP_CLASS_REJECT) { result.rejectedAtLevel=level; return SetHybridCatchUpResultOutcome(result,aggregate,"Catch-Up rejected"); }
      baseState=nextBase; worstState=nextWorst;
   }
   result.rejectedAtLevel=result.evaluatedLevels; return SetHybridCatchUpResultOutcome(result,HYBRID_CATCHUP_OUTCOME_NO_FINITE_LEVEL,"Maximum Harvest levels exhausted");
}

// Compatibility API: legacy callers only consider a fully proven finite pass true.
bool EvaluateHybridFiniteCatchUpPreview(const HybridCycleSnapshot &snapshot,const HybridCandidatePlan &plan,HybridCatchUpResult &result)
{ return EvaluateHybridFiniteCatchUpPreviewTyped(snapshot,plan,result)==HYBRID_CATCHUP_OUTCOME_FINITE_PASS; }

#endif
