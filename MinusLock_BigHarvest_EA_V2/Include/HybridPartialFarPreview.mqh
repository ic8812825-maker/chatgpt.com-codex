#ifndef __BH_HYBRID_PARTIAL_FAR_PREVIEW_MQH__
#define __BH_HYBRID_PARTIAL_FAR_PREVIEW_MQH__

bool HybridPartialFarCloseMoney(const HybridCatchUpState &state,double lot,double bid,double ask,BrokerMoneyResult &money)
{
   double price=state.farDirection==DIR_BUY?bid:ask;
   return CalcProjectedCloseNetMoney(state.farDirection,lot,state.farOpenPrice,price,money);
}

bool SolveHybridPartialFarPreview(const HybridCatchUpState &state,double budgetAvailable,double closeBid,double closeAsk,HybridPartialFarPreviewResult &result)
{
   ZeroMemory(result); ResetBrokerMoneyResult(result.partialCloseMoney);
   result.reason="NOT_EVALUATED"; result.budgetBefore=state.partialFarBudgetAvailable;
   result.budgetGross=budgetAvailable; result.budgetAdded=budgetAvailable-state.partialFarBudgetAvailable;
   result.farLotBefore=state.farLot;
   if(state.farLot<=0 || state.farOpenPrice<=0 || budgetAvailable<-MoneyCalculationTolerance || closeBid<=0 || closeAsk<closeBid)
   { result.reason="CATCHUP_PARTIAL_SOLVER_FAILED"; return false; }
   double minLot=SymbolInfoDouble(state.symbol,SYMBOL_VOLUME_MIN),step=SymbolInfoDouble(state.symbol,SYMBOL_VOLUME_STEP);
   if(minLot<=0 || step<=0) { result.reason="CATCHUP_PARTIAL_SOLVER_FAILED"; return false; }

   BrokerMoneyResult fullMoney;
   if(!HybridPartialFarCloseMoney(state,state.farLot,closeBid,closeAsk,fullMoney))
   { result.reason="CATCHUP_PARTIAL_SOLVER_FAILED"; return false; }
   double fullCost=MathMax(-fullMoney.netMoney,0.0);
   result.fullFarCloseMoney=fullMoney; result.fullFarLoss=fullCost;
   result.partialBudgetCanCoverFullFarLoss=fullCost<=budgetAvailable+MoneyCalculationTolerance;
   result.finalClosePreviewRouteCandidate=result.partialBudgetCanCoverFullFarLoss;
   if(result.finalClosePreviewRouteCandidate)
   {
      result.calculationValid=true; result.partialCloseAvailable=false;
      result.rawCloseLot=0.0; result.normalizedCloseLot=0.0;
      result.farLotAfter=state.farLot; ResetBrokerMoneyResult(result.partialCloseMoney);
      result.budgetConsumed=0.0; result.budgetAfter=NormalizeDouble(MathMax(0.0,budgetAvailable),2);
      result.remainderVolumeValid=true;
      result.budgetConservationPass=MathAbs(result.budgetBefore+result.budgetAdded-result.budgetAfter)<=MoneyCalculationTolerance;
      result.reason="CATCHUP_FINAL_CLOSE_PREVIEW_REQUIRED";
      return result.budgetConservationPass;
   }

   // Full Far is never consumed by Partial policy. Descending scan selects the
   // maximum affordable lot leaving a broker-valid residual.
   double maximum=NormalizeLotDown(state.farLot-minLot);
   result.rawCloseLot=maximum;
   for(double raw=maximum; raw>=minLot-step*.5; raw-=step)
   {
      double candidate=NormalizeLotDown(raw);
      double remainder=NormalizeLotDown(state.farLot-candidate);
      if(candidate<minLot-step*.5 || candidate>=state.farLot-MoneyCalculationTolerance || remainder<minLot-step*.5) continue;
      BrokerMoneyResult money;
      if(!HybridPartialFarCloseMoney(state,candidate,closeBid,closeAsk,money))
      { result.reason="CATCHUP_PARTIAL_SOLVER_FAILED"; return false; }
      double cost=MathMax(-money.netMoney,0.0);
      if(cost>budgetAvailable+MoneyCalculationTolerance) continue;
      result.calculationValid=true; result.partialCloseAvailable=true;
      result.normalizedCloseLot=candidate; result.farLotAfter=remainder;
      result.partialCloseMoney=money; result.budgetConsumed=cost;
      result.budgetAfter=NormalizeDouble(MathMax(0.0,budgetAvailable-cost),2);
      result.remainderVolumeValid=true;
      result.budgetConservationPass=MathAbs(result.budgetBefore+result.budgetAdded-result.budgetConsumed-result.budgetAfter)<=MoneyCalculationTolerance;
      result.reason=result.budgetConservationPass?"PASS":"CATCHUP_PARTIAL_BUDGET_FAILED";
      return result.budgetConservationPass;
   }
   result.calculationValid=true; result.partialCloseAvailable=false;
   result.normalizedCloseLot=0; result.farLotAfter=state.farLot;
   result.budgetConsumed=0; result.budgetAfter=NormalizeDouble(MathMax(0.0,budgetAvailable),2);
   result.remainderVolumeValid=state.farLot+MoneyCalculationTolerance>=minLot;
   result.budgetConservationPass=MathAbs(result.budgetBefore+result.budgetAdded-result.budgetAfter)<=MoneyCalculationTolerance;
   result.reason=result.partialBudgetCanCoverFullFarLoss?"CATCHUP_REQUIRES_FINAL_CLOSE_PREVIEW":"NO_AFFORDABLE_PARTIAL_LOT";
   return result.budgetConservationPass && result.remainderVolumeValid;
}

#endif
