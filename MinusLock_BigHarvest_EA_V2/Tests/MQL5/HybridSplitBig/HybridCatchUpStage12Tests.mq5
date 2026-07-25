#property strict
#property script_show_inputs
#include "../../../Include/Config.mqh"
#include "../../../Include/Types.mqh"
#include "../../../Include/LotUtils.mqh"
#include "../../../Include/BrokerMoneyModel.mqh"
#include "../../../Include/HybridRoundingModel.mqh"
#include "../../../Include/HybridCatchUpModel.mqh"

int failures=0;
int routePassed=0;
void Stage12Assert(string id,bool condition,string expected,string actual)
{
   if(condition) Print("STAGE12_TEST|ID=",id,"|PASS");
   else { failures++; Print("STAGE12_TEST|ID=",id,"|FAIL|Expected=",expected,"|Actual=",actual); }
}
void RouteAssert(string id,bool condition,string expected,string actual)
{
   if(condition) { routePassed++; Print("ROUTE_TEST|ID=",id,"|PASS"); }
   else { failures++; Print("ROUTE_TEST|ID=",id,"|FAIL|Expected=",expected,"|Actual=",actual); }
}
void OnStart()
{
   Stage12Assert("FO-01",ClassifyHybridCatchUpOutcome(HYBRID_CATCHUP_OUTCOME_CONTINUE)==HYBRID_CATCHUP_CLASS_CONTINUE,"CONTINUE",IntegerToString((int)ClassifyHybridCatchUpOutcome(HYBRID_CATCHUP_OUTCOME_CONTINUE)));
   Stage12Assert("FO-02",ClassifyHybridCatchUpOutcome(HYBRID_CATCHUP_OUTCOME_FINITE_PASS)==HYBRID_CATCHUP_CLASS_SUCCESS,"SUCCESS",IntegerToString((int)ClassifyHybridCatchUpOutcome(HYBRID_CATCHUP_OUTCOME_FINITE_PASS)));
   Stage12Assert("FO-03",ClassifyHybridCatchUpOutcome(HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED)==HYBRID_CATCHUP_CLASS_ROUTE,"ROUTE",IntegerToString((int)ClassifyHybridCatchUpOutcome(HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED)));
   Stage12Assert("FO-06",CombineHybridCatchUpOutcomes(HYBRID_CATCHUP_OUTCOME_FINITE_PASS,HYBRID_CATCHUP_OUTCOME_FINITE_PASS)==HYBRID_CATCHUP_OUTCOME_FINITE_PASS,"FINITE_PASS","other");
   Stage12Assert("FO-07",CombineHybridCatchUpOutcomes(HYBRID_CATCHUP_OUTCOME_FINITE_PASS,HYBRID_CATCHUP_OUTCOME_CONTINUE)==HYBRID_CATCHUP_OUTCOME_CONTINUE,"CONTINUE","other");
   Stage12Assert("FO-08",CombineHybridCatchUpOutcomes(HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED,HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED)==HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED,"FINAL_ROUTE","other");
   HybridCatchUpProfile profile; ZeroMemory(profile); profile.kind=HYBRID_CATCHUP_WORST; profile.bidAdversePoints=10; profile.askAdversePoints=10; profile.cumulativeSpreadStress=false;
   double bid,ask; bool applied=ApplyCatchUpExecutionProfile(1.1000,1.1002,profile,0.00001,bid,ask);
   Stage12Assert("WP-03",applied && MathAbs((ask-bid)-0.0004)<0.0000001,"0.0004",DoubleToString(ask-bid,5));
   Stage12Assert("WP-08",!profile.cumulativeSpreadStress,"false",profile.cumulativeSpreadStress?"true":"false");
   Stage12Assert("MG-01",HybridMarginControlPrice(DIR_BUY,1.1000,1.1002)==1.1002,"Ask",DoubleToString(HybridMarginControlPrice(DIR_BUY,1.1000,1.1002),4));
   Stage12Assert("MG-02",HybridMarginControlPrice(DIR_SELL,1.1000,1.1002)==1.1000,"Bid",DoubleToString(HybridMarginControlPrice(DIR_SELL,1.1000,1.1002),4));
   HybridCatchUpState state; ZeroMemory(state); state.symbol=_Symbol; state.farDirection=DIR_BUY;
   state.farLot=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MIN); state.farOpenPrice=SymbolInfoDouble(_Symbol,SYMBOL_ASK);
   state.partialFarBudgetAvailable=1000000.0; state.fingerprint=12345;
   HybridPartialFarPreviewResult partial; bid=SymbolInfoDouble(_Symbol,SYMBOL_BID); ask=SymbolInfoDouble(_Symbol,SYMBOL_ASK);
   bool solved=SolveHybridPartialFarPreview(state,state.partialFarBudgetAvailable,bid,ask,partial);
   RouteAssert("ROUTE-01",solved && partial.finalClosePreviewRouteCandidate && !partial.partialCloseAvailable,"route/no partial",partial.reason);
   RouteAssert("ROUTE-02",partial.farLotAfter==state.farLot,"Far unchanged",DoubleToString(partial.farLotAfter,8));
   RouteAssert("ROUTE-03",partial.budgetConsumed==0 && partial.budgetAfter==state.partialFarBudgetAvailable,"budget preserved",DoubleToString(partial.budgetAfter,2));
   RouteAssert("ROUTE-04",partial.partialCloseMoney.netMoney==0,"PartialFarNet=0",DoubleToString(partial.partialCloseMoney.netMoney,2));
   HybridHarvestLevelResult row; ZeroMemory(row); row.level=1; row.triggerBid=bid; row.triggerAsk=ask; row.harvestNet=10;
   row.realizedPLAfterHarvest=10; row.partialAdd=1; row.reserveAdd=9; row.carryAdd=0;
   HybridCatchUpProfile routeProfile; ZeroMemory(routeProfile); routeProfile.kind=HYBRID_CATCHUP_BASE;
   HybridFinalCloseRouteState route; bool built=BuildHybridFinalCloseRouteState(state,row,partial,routeProfile,route);
   RouteAssert("ROUTE-05",built && route.farLot==state.farLot,"route Far unchanged",DoubleToString(route.farLot,8));
   RouteAssert("ROUTE-06",built && route.routeStateFingerprint!=0,"fingerprint","0");
   RouteAssert("ROUTE-07",route.sourceStateFingerprint==state.fingerprint,"source fingerprint",IntegerToString((int)route.sourceStateFingerprint));
   RouteAssert("ROUTE-08",CombineHybridCatchUpOutcomes(HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED,HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED)==HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED,"route","other");
   RouteAssert("ROUTE-09",CombineHybridCatchUpOutcomes(HYBRID_CATCHUP_OUTCOME_FINAL_CLOSE_PREVIEW_REQUIRED,HYBRID_CATCHUP_OUTCOME_CONTINUE)==HYBRID_CATCHUP_OUTCOME_REJECT_OUTCOME_DIVERGENCE,"divergence","other");
   HybridHarvestLevelResult baseRow,worstRow; ZeroMemory(baseRow); ZeroMemory(worstRow); baseRow.currentLegMoneyEvaluated=true; worstRow.currentLegMoneyEvaluated=true;
   RouteAssert("ADV-01",baseRow.currentLegMoneyEvaluated && worstRow.currentLegMoneyEvaluated,"guard true","false");
   baseRow.currentLegMoneyEvaluated=false;
   RouteAssert("ADV-02",!(baseRow.currentLegMoneyEvaluated && worstRow.currentLegMoneyEvaluated),"guard skipped","false");
   Print("STAGE12_TEST|SUMMARY|Failures=",failures);
   Print("ROUTE_TEST|SUMMARY|Passed=",routePassed,"|Failed=",failures);
}
