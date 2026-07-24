#ifndef __BH_HYBRID_MARGIN_MODEL_MQH__
#define __BH_HYBRID_MARGIN_MODEL_MQH__

bool EvaluateHybridCandidateMargin(const HybridCycleSnapshot &snapshot,const HybridCandidatePlan &plan,HybridMarginPreview &preview)
{
   preview.pass=false; preview.coreMargin=0; preview.trendMargin=0; preview.smallMargin=0; preview.totalNewMargin=0; preview.conservativeUpper=0; preview.projectedMarginLevel=0; preview.projectedMarginPercent=0; preview.projectedFreeMargin=0; preview.reason="NOT_EVALUATED";
   BrokerMoneyResult m;
   if(!CalcProjectedMarginMoney(plan.bigDirection==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL,plan.coreLot,plan.bigDirection==DIR_BUY?snapshot.ask:snapshot.bid,m)){ preview.reason=m.reason; return false; }
   preview.coreMargin=m.requiredMargin;
   if(!CalcProjectedMarginMoney(plan.bigDirection==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL,plan.trendLot,plan.bigDirection==DIR_BUY?snapshot.ask:snapshot.bid,m)){ preview.reason=m.reason; return false; }
   preview.trendMargin=m.requiredMargin;
   if(!CalcProjectedMarginMoney(plan.smallDirection==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL,plan.smallLot,plan.smallDirection==DIR_BUY?snapshot.ask:snapshot.bid,m)){ preview.reason=m.reason; return false; }
   preview.smallMargin=m.requiredMargin;
   preview.totalNewMargin=preview.coreMargin+preview.trendMargin+preview.smallMargin;
   preview.conservativeUpper=snapshot.margin+preview.totalNewMargin;
   preview.projectedFreeMargin=snapshot.freeMargin-preview.totalNewMargin;
   if(snapshot.equity<=0 || preview.conservativeUpper<=0){ preview.reason="MARGIN_INPUT_INVALID"; return false; }
   preview.projectedMarginLevel=snapshot.equity/preview.conservativeUpper*100.0;
   preview.projectedMarginPercent=preview.conservativeUpper/snapshot.equity*100.0;
   preview.pass=preview.projectedFreeMargin>0 && preview.projectedMarginLevel+MoneyCalculationTolerance>=MinimumSafeMarginLevel && preview.projectedMarginPercent<=MaxMarginPercent+MoneyCalculationTolerance;
   preview.reason=preview.pass?"PASS":"MARGIN_LIMIT";
   return preview.pass;
}

#endif // __BH_HYBRID_MARGIN_MODEL_MQH__
