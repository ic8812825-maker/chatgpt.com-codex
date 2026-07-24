#ifndef __BH_HYBRID_WORST_CASE_MODEL_MQH__
#define __BH_HYBRID_WORST_CASE_MODEL_MQH__

bool EvaluateHybridWorstCasePreview(const HybridCycleSnapshot &snapshot,const HybridCandidatePlan &plan,HybridWorstCasePreview &preview)
{
   preview.pass=false; preview.worstBid=0; preview.worstAsk=0; preview.worstNet=0; preview.reason="NOT_EVALUATED";
   double point=SymbolInfoDouble(_Symbol,SYMBOL_POINT);
   if(point<=0 || snapshot.bid<=0 || snapshot.ask<=0){ preview.reason="WORST_CASE_PRICE_INVALID"; return false; }
   double bufferPoints=SpreadExpansionBufferPoints + MaxSlippagePoints*SlippageSafetyMultiplier + HybridGapBufferPoints;
   preview.worstBid=snapshot.bid-point*bufferPoints;
   preview.worstAsk=snapshot.ask+point*bufferPoints;
   if(preview.worstBid<=0 || preview.worstAsk<preview.worstBid){ preview.reason="WORST_CASE_BUFFER_INVALID"; return false; }
   BrokerMoneyResult core,trend,small;
   bool ok=CalcProjectedPositionNetMoney(plan.bigDirection,plan.coreLot,plan.bigDirection==DIR_BUY?snapshot.ask:snapshot.bid,plan.bigDirection==DIR_BUY?preview.worstBid:preview.worstAsk,true,true,core)
         && CalcProjectedPositionNetMoney(plan.bigDirection,plan.trendLot,plan.bigDirection==DIR_BUY?snapshot.ask:snapshot.bid,plan.bigDirection==DIR_BUY?preview.worstBid:preview.worstAsk,true,true,trend)
         && CalcProjectedPositionNetMoney(plan.smallDirection,plan.smallLot,plan.smallDirection==DIR_BUY?snapshot.ask:snapshot.bid,plan.smallDirection==DIR_BUY?preview.worstBid:preview.worstAsk,true,true,small);
   if(!ok){ preview.reason="WORST_CASE_MONEY_FAILED"; return false; }
   preview.worstNet=core.netMoney+trend.netMoney+small.netMoney;
   preview.pass=preview.worstNet+MoneyCalculationTolerance>=-SafetyBufferMoney;
   preview.reason=preview.pass?"PASS":"WORST_CASE_NET";
   return preview.pass;
}

#endif // __BH_HYBRID_WORST_CASE_MODEL_MQH__
