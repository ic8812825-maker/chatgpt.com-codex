#property strict
#property script_show_inputs
#include "../../../Include/Config.mqh"
#include "../../../Include/Types.mqh"
#include "../../../Include/LotUtils.mqh"
#include "../../../Include/BrokerMoneyModel.mqh"
#include "../../../Include/HybridRoundingModel.mqh"
#include "../../../Include/HybridCatchUpModel.mqh"
int routePassed=0,routeFailed=0;
void Check(string id,bool ok,string actual="") { if(ok){routePassed++;Print("ROUTE_HARDENING_TEST|ID=",id,"|PASS");}else{routeFailed++;Print("ROUTE_HARDENING_TEST|ID=",id,"|FAIL|Expected=PASS|Actual=",actual);} }
void OnStart()
{
 HybridCatchUpProfile profile; ZeroMemory(profile); profile.kind=HYBRID_CATCHUP_BASE;
 HybridCatchUpState s; ZeroMemory(s); s.levelIndex=0;s.symbol=_Symbol;s.magic=77;s.cycleId=9;s.stateRevision=4;s.farDirection=DIR_BUY;s.bigDirection=DIR_SELL;s.smallDirection=DIR_BUY;
 double minLot=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MIN),bid=SymbolInfoDouble(_Symbol,SYMBOL_BID),ask=SymbolInfoDouble(_Symbol,SYMBOL_ASK);
 s.farLot=MathMax(minLot,0.10);s.farOpenPrice=ask;s.coreLot=MathMax(minLot,0.16);s.trendLot=MathMax(minLot,0.03);s.smallLot=MathMax(minLot,0.06);
 s.coreOpenPrice=bid;s.trendOpenPrice=bid;s.smallOpenPrice=ask;s.anchorBid=bid;s.anchorAsk=ask;s.anchorMid=(bid+ask)/2;s.baselineSpread=ask-bid;s.equity=100000;s.currentMargin=100;s.freeMargin=99900;s.partialFarBudgetAvailable=1000000;s.finalReserveReal=10;s.carryAvailable=1;s.fingerprint=HybridCatchUpFingerprint(s,profile.kind);
 HybridPartialFarPreviewResult p; bool solved=SolveHybridPartialFarPreview(s,s.partialFarBudgetAvailable,bid,ask,p);
 HybridHarvestLevelResult row; ZeroMemory(row);row.level=1;row.triggerBid=bid;row.triggerAsk=ask;row.currentLegMoneyEvaluated=true;row.harvestAllocationEvaluated=true;row.fullFarAffordabilityEvaluated=true;row.farLotAfter=s.farLot;row.realizedPLAfterHarvest=s.realizedCyclePL;row.realizedPLAfterPartial=row.realizedPLAfterHarvest;row.partialBudgetGross=p.budgetGross;
 HybridFinalCloseRouteState route; bool built=BuildHybridFinalCloseRouteState(s,row,p,profile,route);string code,reason;
 Check("MQL-RV-01",solved&&built&&ValidateHybridFinalCloseRouteState(s,row,p,route,code,reason),code);
 HybridFinalCloseRouteState bad=route;bad.farLot-=minLot;Check("MQL-RV-02",!ValidateHybridFinalCloseRouteState(s,row,p,bad,code,reason),code);
 HybridPartialFarPreviewResult badP=p;badP.budgetConsumed=1;Check("MQL-RV-03",!ValidateHybridFinalCloseRouteState(s,row,badP,route,code,reason),code);
 HybridHarvestLevelResult badRow=row;badRow.nextBasketEvaluated=true;Check("MQL-RV-04",!ValidateHybridFinalCloseRouteState(s,badRow,p,route,code,reason),code);
 bad=route;bad.carryAfter+=1;Check("MQL-RV-05",!ValidateHybridFinalCloseRouteState(s,row,p,bad,code,reason),code);
 double volumeStep=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_STEP),point=SymbolInfoDouble(_Symbol,SYMBOL_POINT);
 bad=route;bad.farLot=route.farLot-volumeStep;Check("MQL-TOL-01",!ValidateHybridFinalCloseRouteState(s,row,p,bad,code,reason),code);
 bad=route;bad.farLot=route.farLot+volumeStep;Check("MQL-TOL-02",!ValidateHybridFinalCloseRouteState(s,row,p,bad,code,reason),code);
 bad=route;bad.farOpenPrice=route.farOpenPrice+point;Check("MQL-TOL-03",!ValidateHybridFinalCloseRouteState(s,row,p,bad,code,reason),code);
 bad=route;bad.farLot=route.farLot+HybridLotTolerance(_Symbol)*0.1;bad.routeStateFingerprint=HybridFinalCloseRouteFingerprint(bad);Check("MQL-TOL-04",ValidateHybridFinalCloseRouteState(s,row,p,bad,code,reason),code);
 bad=route;bad.routeCandidate=false;bad.routeStateFingerprint=HybridFinalCloseRouteFingerprint(bad);Check("MQL-TOL-05",!ValidateHybridFinalCloseRouteState(s,row,p,bad,code,reason),code);
 bad=route;bad.routeCandidate=false;Check("MQL-TOL-06",HybridFinalCloseRouteFingerprint(bad)!=HybridFinalCloseRouteFingerprint(route));
 Check("MQL-TOL-07",HybridMoneyEqual(10.0,10.009)&&!HybridMoneyEqual(10.0,10.02));
 bad=route;bad.carryAfter+=1;Check("MQL-FP-01",HybridFinalCloseRouteFingerprint(bad)!=HybridFinalCloseRouteFingerprint(route));bad=route;bad.fullFarCloseMoney.closeCommission+=1;Check("MQL-FP-02",HybridFinalCloseRouteFingerprint(bad)!=HybridFinalCloseRouteFingerprint(route));bad=route;bad.routeStateRevision++;Check("MQL-FP-03",HybridFinalCloseRouteFingerprint(bad)!=HybridFinalCloseRouteFingerprint(route));
 HybridHarvestLevelResult levelRow;HybridCatchUpState after;HybridCatchUpOutcome out=EvaluateHybridCatchUpLevel(s,profile,levelRow,after);
 Check("MQL-LVL-01",out==HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED);Check("MQL-LVL-02",!levelRow.partialFarEvaluated);Check("MQL-LVL-03",!levelRow.nextBasketEvaluated);Check("MQL-LVL-04",!levelRow.nextBasketGeometryEvaluated);Check("MQL-LVL-05",!levelRow.nextBasketMarginEvaluated);Check("MQL-LVL-06",!levelRow.recoveryAfterReopenEvaluated);Check("MQL-LVL-07",!levelRow.continuationStateValid);Check("MQL-LVL-08",levelRow.finalCloseRouteState.validationPass);string afterReason;Check("MQL-LVL-09",!ValidateHybridCatchUpState(after,afterReason));
 Check("MQL-COMBINE",CombineHybridCatchUpOutcomes(HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED,HYBRID_CATCHUP_OUTCOME_CONTINUE)==HYBRID_CATCHUP_OUTCOME_REJECT_OUTCOME_DIVERGENCE);
 Print("ROUTE_HARDENING_TEST|SUMMARY|Passed=",routePassed,"|Failed=",routeFailed);
}
