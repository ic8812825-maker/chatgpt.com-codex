#property strict
#property script_show_inputs
#include "../../../Include/Config.mqh"
#include "../../../Include/Types.mqh"
#include "../../../Include/LotUtils.mqh"
#include "../../../Include/BrokerMoneyModel.mqh"
#include "../../../Include/HybridRoundingModel.mqh"
#include "../../../Include/HybridCatchUpModel.mqh"

int failures=0;
void Stage12Assert(string id,bool condition,string expected,string actual)
{
   if(condition) Print("STAGE12_TEST|ID=",id,"|PASS");
   else { failures++; Print("STAGE12_TEST|ID=",id,"|FAIL|Expected=",expected,"|Actual=",actual); }
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
   Print("STAGE12_TEST|SUMMARY|Failures=",failures);
}
