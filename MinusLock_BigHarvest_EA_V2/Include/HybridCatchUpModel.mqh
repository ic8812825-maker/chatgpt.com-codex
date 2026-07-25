#ifndef __BH_HYBRID_CATCHUP_MODEL_MQH__
#define __BH_HYBRID_CATCHUP_MODEL_MQH__

// Pure level-by-level preview. It performs no trade, state or ledger mutation.
double HybridCatchUpClosePrice(Direction direction,double bid,double ask)
{
   return direction==DIR_BUY?bid:ask;
}

double HybridCatchUpMoneyRound(double value)
{
   return NormalizeDouble(value,2);
}

bool HybridCatchUpLeg(Direction direction,double lot,double openPrice,double bid,double ask,BrokerMoneyResult &money)
{
   if(direction==DIR_NONE || lot<=0 || openPrice<=0 || bid<=0 || ask<bid)
   {
      ResetBrokerMoneyResult(money);
      money.reason="CATCHUP_LEG_INVALID";
      return false;
   }
   return CalcProjectedPositionNetMoney(direction,lot,openPrice,HybridCatchUpClosePrice(direction,bid,ask),true,true,money);
}

bool HybridCatchUpMarginAtLevel(const HybridCycleSnapshot &snapshot,const HybridCandidatePlan &plan,double bid,double ask,double &baseMargin,double &worstMargin)
{
   BrokerMoneyResult coreMargin,trendMargin,smallMargin;
   ENUM_ORDER_TYPE bigType=plan.bigDirection==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL;
   ENUM_ORDER_TYPE smallType=plan.smallDirection==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL;
   double bigPrice=plan.bigDirection==DIR_BUY?ask:bid;
   double smallPrice=plan.smallDirection==DIR_BUY?ask:bid;
   if(!CalcProjectedMarginMoney(bigType,plan.coreLot,bigPrice,coreMargin)
      || !CalcProjectedMarginMoney(bigType,plan.trendLot,bigPrice,trendMargin)
      || !CalcProjectedMarginMoney(smallType,plan.smallLot,smallPrice,smallMargin))
      return false;
   baseMargin=snapshot.margin+coreMargin.requiredMargin+trendMargin.requiredMargin+smallMargin.requiredMargin;
   worstMargin=baseMargin*(1.0+HybridCatchUpMarginSafetyPercent/100.0);
   return MathIsValidNumber(baseMargin) && MathIsValidNumber(worstMargin) && baseMargin>=0 && worstMargin>=baseMargin;
}

bool HybridCatchUpMarginPass(const HybridCycleSnapshot &snapshot,double margin)
{
   if(snapshot.equity<=0 || margin<0) return false;
   double level=margin>0?snapshot.equity/margin*100.0:DBL_MAX;
   double usage=margin/snapshot.equity*100.0;
   return level+MoneyCalculationTolerance>=MinimumSafeMarginLevel
      && usage<=MaxMarginPercent+MoneyCalculationTolerance
      && snapshot.equity-margin>0;
}

bool EvaluateHybridFiniteCatchUpPreview(const HybridCycleSnapshot &snapshot,const HybridCandidatePlan &plan,HybridCatchUpResult &result)
{
   result.pass=false;
   result.finiteLevel=-1;
   result.finalCoverageDeficit=0;
   result.finalRecoveryPL=0;
   result.trace="";
   result.reason="NOT_EVALUATED";
   ArrayResize(result.levels,0);

   if(MaxHarvestLevels<=0 || BigMoveStartPoints<=0 || BigMoveStepPoints<0)
   {
      result.reason="CATCHUP_LEVEL_CONFIG_INVALID";
      return false;
   }
   if(snapshot.bid<=0 || snapshot.ask<snapshot.bid || snapshot.farLot<=0 || snapshot.farOpenPrice<=0
      || plan.coreLot<=0 || plan.trendLot<=0 || plan.smallLot<=0
      || plan.bigDirection==DIR_NONE || plan.smallDirection==DIR_NONE)
   {
      result.reason="CATCHUP_INPUT_INVALID";
      return false;
   }

   double point=SymbolInfoDouble(snapshot.symbol,SYMBOL_POINT);
   if(point<=0 || !MathIsValidNumber(point))
   {
      result.reason="CATCHUP_POINT_INVALID";
      return false;
   }
   double spread=snapshot.ask-snapshot.bid;
   double cumulativePartial=snapshot.partialFarAvailable;
   double cumulativeReserve=snapshot.finalReserveReal;
   double cumulativeCarry=0.0;
   double cumulativeHarvest=0.0;
   double cumulativeWorstHarvest=0.0;
   double cumulativeWorstReserve=snapshot.finalReserveReal;
   double previousDeficit=DBL_MAX;
   double previousReserve=cumulativeReserve;
   double previousRecovery=-DBL_MAX;

   for(int index=0; index<MaxHarvestLevels; index++)
   {
      int level=index+1;
      ArrayResize(result.levels,level);
      HybridHarvestLevelResult row;
      ZeroMemory(row);
      row.level=level;
      row.reason="NOT_EVALUATED";
      double distance=(double)BigMoveStartPoints+(double)index*BigMoveStepPoints;
      if(plan.bigDirection==DIR_BUY)
      {
         row.levelBid=snapshot.bid+distance*point;
         row.levelAsk=row.levelBid+spread;
      }
      else
      {
         row.levelAsk=snapshot.ask-distance*point;
         row.levelBid=row.levelAsk-spread;
      }
      if(row.levelBid<=0 || row.levelAsk<row.levelBid)
      {
         row.reason="LEVEL_PRICE_INVALID";
         result.levels[index]=row;
         result.reason=row.reason;
         return false;
      }

      // These are candidate legs, therefore their frozen entry prices are the
      // snapshot execution sides, never unrelated legacy/current role prices.
      double coreOpen=plan.bigDirection==DIR_BUY?snapshot.ask:snapshot.bid;
      double trendOpen=coreOpen;
      double smallOpen=plan.smallDirection==DIR_BUY?snapshot.ask:snapshot.bid;
      if(!HybridCatchUpLeg(snapshot.farDirection,snapshot.farLot,snapshot.farOpenPrice,row.levelBid,row.levelAsk,row.far)
         || !HybridCatchUpLeg(plan.bigDirection,plan.coreLot,coreOpen,row.levelBid,row.levelAsk,row.core)
         || !HybridCatchUpLeg(plan.bigDirection,plan.trendLot,trendOpen,row.levelBid,row.levelAsk,row.trend)
         || !HybridCatchUpLeg(plan.smallDirection,plan.smallLot,smallOpen,row.levelBid,row.levelAsk,row.small))
      {
         row.reason="LEVEL_BROKER_MONEY_FAILED";
         result.levels[index]=row;
         result.reason=row.reason;
         return false;
      }

      row.harvestNet=HybridCatchUpMoneyRound(row.core.netMoney+row.trend.netMoney+row.small.netMoney);
      row.eligibleHarvestNet=MathMax(0.0,row.harvestNet);
      row.partialAdd=HybridCatchUpMoneyRound(HybridPartialFarShare*row.eligibleHarvestNet);
      row.reserveAdd=HybridCatchUpMoneyRound(HybridFinalReserveShare*row.eligibleHarvestNet);
      double carryBase=HybridCatchUpMoneyRound(HybridCarryShare*row.eligibleHarvestNet);
      double residual=HybridCatchUpMoneyRound(row.eligibleHarvestNet-row.partialAdd-row.reserveAdd-carryBase);
      row.carryAdd=HybridCatchUpMoneyRound(carryBase+residual);
      if(MathAbs(row.partialAdd+row.reserveAdd+row.carryAdd-row.eligibleHarvestNet)>MoneyCalculationTolerance)
      {
         row.reason="ALLOCATION_CONSERVATION_FAILED";
         result.levels[index]=row;
         result.reason=row.reason;
         return false;
      }

      cumulativePartial=HybridCatchUpMoneyRound(cumulativePartial+row.partialAdd);
      cumulativeReserve=HybridCatchUpMoneyRound(cumulativeReserve+row.reserveAdd);
      cumulativeCarry=HybridCatchUpMoneyRound(cumulativeCarry+row.carryAdd);
      cumulativeHarvest=HybridCatchUpMoneyRound(cumulativeHarvest+row.harvestNet);
      row.partialBudgetAfter=cumulativePartial;
      row.reserveAfter=cumulativeReserve;
      row.carryAfter=cumulativeCarry;
      row.farCloseCost=HybridCatchUpMoneyRound(MathMax(-row.far.netMoney,0.0)+HybridCoverageSafetyBufferMoney);
      row.coverageDeficit=HybridCatchUpMoneyRound(row.farCloseCost-row.reserveAfter);
      row.projectedRealizedPL=HybridCatchUpMoneyRound(snapshot.realizedCyclePL+cumulativeHarvest);
      row.projectedFloatingPL=row.far.grossProfit;
      row.projectedExitCosts=HybridCatchUpMoneyRound(row.far.grossProfit-row.far.netMoney);
      row.projectedRecoveryPL=HybridCatchUpMoneyRound(row.projectedRealizedPL+row.projectedFloatingPL-row.projectedExitCosts);

      if(!HybridCatchUpMarginAtLevel(snapshot,plan,row.levelBid,row.levelAsk,row.marginBase,row.marginWorst))
      {
         row.reason="LEVEL_MARGIN_CALCULATION_FAILED";
         result.levels[index]=row;
         result.reason=row.reason;
         return false;
      }
      row.marginPass=HybridCatchUpMarginPass(snapshot,row.marginBase) && HybridCatchUpMarginPass(snapshot,row.marginWorst);
      double baseBasket=row.far.netMoney+row.core.netMoney+row.trend.netMoney+row.small.netMoney;
      row.riskBase=MathMax(-baseBasket,0.0);

      double worstBufferPoints=SpreadExpansionBufferPoints+MaxSlippagePoints*SlippageSafetyMultiplier+HybridGapBufferPoints;
      double worstBid=row.levelBid-worstBufferPoints*point;
      double worstAsk=row.levelAsk+worstBufferPoints*point;
      BrokerMoneyResult worstFar,worstCore,worstTrend,worstSmall;
      if(!HybridCatchUpLeg(snapshot.farDirection,snapshot.farLot,snapshot.farOpenPrice,worstBid,worstAsk,worstFar)
         || !HybridCatchUpLeg(plan.bigDirection,plan.coreLot,coreOpen,worstBid,worstAsk,worstCore)
         || !HybridCatchUpLeg(plan.bigDirection,plan.trendLot,trendOpen,worstBid,worstAsk,worstTrend)
         || !HybridCatchUpLeg(plan.smallDirection,plan.smallLot,smallOpen,worstBid,worstAsk,worstSmall))
      {
         row.reason="LEVEL_WORST_MONEY_FAILED";
         result.levels[index]=row;
         result.reason=row.reason;
         return false;
      }
      double worstBasket=worstFar.netMoney+worstCore.netMoney+worstTrend.netMoney+worstSmall.netMoney;
      row.riskWorst=MathMax(-worstBasket,0.0);
      double worstHarvest=HybridCatchUpMoneyRound(worstCore.netMoney+worstTrend.netMoney+worstSmall.netMoney);
      cumulativeWorstHarvest=HybridCatchUpMoneyRound(cumulativeWorstHarvest+worstHarvest);
      double worstEligible=MathMax(worstHarvest,0.0);
      cumulativeWorstReserve=HybridCatchUpMoneyRound(cumulativeWorstReserve+HybridCatchUpMoneyRound(HybridFinalReserveShare*worstEligible));
      double worstFarCost=HybridCatchUpMoneyRound(MathMax(-worstFar.netMoney,0.0)+HybridCoverageSafetyBufferMoney);
      double worstDeficit=HybridCatchUpMoneyRound(worstFarCost-cumulativeWorstReserve);
      double worstRecovery=HybridCatchUpMoneyRound(snapshot.realizedCyclePL+cumulativeWorstHarvest+worstFar.netMoney);
      row.coverageImproved=(index==0) || row.coverageDeficit<=previousDeficit-HybridMinimumCoverageGainMoney+MoneyCalculationTolerance;
      row.finalCoveragePass=row.coverageDeficit<=MoneyCalculationTolerance;
      row.recoveryPass=row.projectedRecoveryPL+MoneyCalculationTolerance>=MinimumRecoveryProfitMoney;
      row.basePass=row.finalCoveragePass && row.recoveryPass;
      row.worstPass=worstDeficit<=MoneyCalculationTolerance
         && worstRecovery+MoneyCalculationTolerance>=MinimumRecoveryProfitMoney
         && HybridCatchUpMarginPass(snapshot,row.marginWorst);

      bool reserveMonotonic=row.reserveAfter+MoneyCalculationTolerance>=previousReserve;
      bool recoveryMonotonic=(index==0) || row.projectedRecoveryPL+MoneyCalculationTolerance>=previousRecovery;
      if(!reserveMonotonic || !row.coverageImproved || !recoveryMonotonic)
      {
         row.reason=!reserveMonotonic?"RESERVE_NON_MONOTONIC":(!row.coverageImproved?"COVERAGE_DEFICIT_NON_MONOTONIC":"RECOVERY_NON_MONOTONIC");
         result.levels[index]=row;
         result.finalCoverageDeficit=row.coverageDeficit;
         result.finalRecoveryPL=row.projectedRecoveryPL;
         result.reason=row.reason;
         return false;
      }

      row.pass=row.finalCoveragePass && row.recoveryPass && row.marginPass && row.basePass && row.worstPass;
      row.reason=row.pass?"PASS":"CONTINUE";
      result.levels[index]=row;
      result.finalCoverageDeficit=row.coverageDeficit;
      result.finalRecoveryPL=row.projectedRecoveryPL;
      result.trace+=StringFormat("LEVEL=%d|BID=%.10f|ASK=%.10f|FarNet=%.2f|CoreNet=%.2f|TrendNet=%.2f|SmallNet=%.2f|HarvestNet=%.2f|Reserve=%.2f|Coverage=%.2f|RecoveryPL=%.2f|MarginBase=%.2f|MarginWorst=%.2f|Decision=%s;",level,row.levelBid,row.levelAsk,row.far.netMoney,row.core.netMoney,row.trend.netMoney,row.small.netMoney,row.harvestNet,row.reserveAfter,row.coverageDeficit,row.projectedRecoveryPL,row.marginBase,row.marginWorst,row.reason);
      previousDeficit=row.coverageDeficit;
      previousReserve=row.reserveAfter;
      previousRecovery=row.projectedRecoveryPL;
      if(row.pass)
      {
         result.pass=true;
         result.finiteLevel=level;
         result.reason="PASS";
         return true;
      }
   }
   result.reason="NO_FINITE_CATCHUP_LEVEL";
   return false;
}

#endif // __BH_HYBRID_CATCHUP_MODEL_MQH__
