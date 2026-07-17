#ifndef __BH_BROKERMONEYMODEL_MQH__
#define __BH_BROKERMONEYMODEL_MQH__

struct BrokerMoneyResult
{
   bool calculationValid;
   bool ok; // compatibility alias
   double grossProfit;
   double openCommission;
   double closeCommission;
   double fee;
   double swap;
   double accruedSwap;
   double projectedFutureSwap;
   double worstCaseSwapBuffer;
   double swapBuffer; // compatibility alias
   double baseSpreadCost;
   double spreadExpansionCost;
   double spreadCost; // compatibility alias: expansion only
   double slippageCost;
   double perOrderBuffer;
   double perPositionBuffer;
   double basketBuffer;
   double cycleBuffer;
   double safetyBuffer; // compatibility aggregate
   double netMoney;
   double requiredMargin;
   double marginMoney; // compatibility alias
   bool baseSpreadIncludedInPrices;
   string reason;
};

struct SignedSwapResult
{
   bool calculationValid;
   double expectedSignedSwap;
   double worstCaseSwapCost;
   double additionalSwapBuffer;
   int chargedDays;
   int rolloverMultipliers;
   string dailyBreakdown;
   string reason;
};
struct CommissionBaseResult { double notionalOpen; double notionalClose; double openTurnover; double closeTurnover; double totalTurnover; double openCommission; double closeCommission; bool valid; string reason; };

struct BigRecoveryEvaluation { bool calculationValid; double netBigExposure; double projectedRecoveryDelta; double costs; bool geometryPass; bool recoveryPass; string reason; };
struct BigReserveCatchUpEvaluation { double reserveBefore; double reserveAfter; double carryBefore; double carryAfter; double farLotBefore; double farLotAfter; double farLossBefore; double farLossAfter; double partialFarActualCost; double coverageBefore; double coverageAfter; bool pass; string reason; };
struct SmallTransitionEvaluation { bool calculationValid; double bigTrendCloseNet; double smallBaseCloseNet; double reverseSmallCloseNet; double oldFarCloseNet; double bigCorePartialCloseNet; double commission; double swap; double spreadExpansion; double slippage; double buffers; double transitionNet; double oldFarLot; double targetNewFarLot; double projectedNewFarLot; double compressionRatio; double netSmallExposure; double projectedMarginLevel; bool moneyPass; bool exposurePass; bool compressionPass; bool marginPass; bool transitionAllowed; string reason; };
enum SmallTransitionLegRole { SMALL_LEG_BIG_TREND_CLOSE=0, SMALL_LEG_SMALL_BASE_CLOSE, SMALL_LEG_REVERSE_SMALL, SMALL_LEG_OLD_FAR_CLOSE, SMALL_LEG_BIG_CORE_PARTIAL };
struct SmallTransitionLeg { SmallTransitionLegRole role; BrokerMoneyResult money; double requestedLot; double residualLot; bool fullClose; bool includesOpenAndClose; };
struct ReverseCyclesEvaluation { int requiredCycles; double finalFarLot; double finalFarLoss; double projectedReserve; double projectedCarry; double projectedRecoveryPL; double finalCoverage; bool pass; string reason; };
struct BigBasketGate { double totalMargin; double projectedMarginLevel; bool volumePass; bool marginPass; bool positionsPass; bool pass; string reason; };
enum FalseReverseAction { FALSE_REVERSE_CONTINUE_WAIT=0, FALSE_REVERSE_CLOSE_REVERSE, FALSE_REVERSE_CLOSE_BASE, FALSE_REVERSE_CLOSE_TAILS, FALSE_REVERSE_CLOSE_BASKET, FALSE_REVERSE_KEEP_LOCK, FALSE_REVERSE_MANUAL };
struct FalseReverseOption { FalseReverseAction action; double projectedNet; double projectedRecoveryPL; double reserveImpact; double projectedMarginLevel; double remainingExposure; bool safe; };
struct FalseReverseEvaluation { FalseReverseOption options[6]; FalseReverseAction selected; bool automaticAllowed; string reason; };

void ResetBrokerMoneyResult(BrokerMoneyResult &r)
{
   r.calculationValid=false; r.ok=false; r.grossProfit=0; r.openCommission=0; r.closeCommission=0; r.fee=0;
   r.swap=0; r.accruedSwap=0; r.projectedFutureSwap=0; r.worstCaseSwapBuffer=0; r.swapBuffer=0; r.baseSpreadCost=0; r.spreadExpansionCost=0; r.spreadCost=0; r.slippageCost=0;
   r.perOrderBuffer=0; r.perPositionBuffer=0; r.basketBuffer=0; r.cycleBuffer=0; r.safetyBuffer=0;
   r.netMoney=0; r.requiredMargin=0; r.marginMoney=0; r.baseSpreadIncludedInPrices=true; r.reason="";
}

double BrokerPointsCostMoney(double lot,double points)
{
   double tick=SymbolInfoDouble(_Symbol,SYMBOL_TRADE_TICK_VALUE_LOSS), size=SymbolInfoDouble(_Symbol,SYMBOL_TRADE_TICK_SIZE), point=SymbolInfoDouble(_Symbol,SYMBOL_POINT);
   if(lot<=0||points<0||tick<=0||size<=0||point<=0) return -1;
   return lot*points*point/size*tick;
}
double BrokerSpreadCostMoney(double lot,double points) { return BrokerPointsCostMoney(lot,points); }
double BrokerExecutionOpenPrice(Direction d) { return SymbolInfoDouble(_Symbol,d==DIR_BUY?SYMBOL_ASK:SYMBOL_BID); }
double BrokerClosePriceAtMid(Direction d,double mid)
{
   double spread=SymbolInfoDouble(_Symbol,SYMBOL_ASK)-SymbolInfoDouble(_Symbol,SYMBOL_BID);
   return d==DIR_BUY?mid-spread*.5:mid+spread*.5;
}

bool ValidateCommissionModel(string &reason)
{
   if(CommissionPerLotPerSide<0||CommissionPerLotRoundTurn<0||CommissionFixedPerDeal<0||CommissionPercent<0) { reason="COMMISSION_NEGATIVE"; return false; }
   int models=(CommissionPerLotPerSide>0?1:0)+(CommissionPerLotRoundTurn>0?1:0)+(CommissionFixedPerDeal>0?1:0)+(CommissionPercent>0?1:0);
   if(models>1) { reason="COMMISSION_MODE_CONFLICT"; return false; }
   return true;
}

bool CalcCommissionBases(double lot,double contractSize,double openPrice,double closePrice,double percent,CommissionPercentBase mode,bool chargeNotionalOnOpen,CommissionBaseResult &r);

bool CalcPercentCommissionSide(double lot,double price,double otherPrice,double margin,bool opening,double &value,string &reason)
{
   value=0; double contract=SymbolInfoDouble(_Symbol,SYMBOL_TRADE_CONTRACT_SIZE);
   if(contract<=0||price<=0) { reason="COMMISSION_CONVERSION_FAILED"; return false; }
   if(CommissionPercentCalculationBase==COMMISSION_PERCENT_NOTIONAL||CommissionPercentCalculationBase==COMMISSION_PERCENT_TURNOVER)
   { CommissionBaseResult base; double openPrice=opening?price:otherPrice,closePrice=opening?otherPrice:price; if(!CalcCommissionBases(lot,contract,openPrice,closePrice,CommissionPercent,CommissionPercentCalculationBase,CommissionNotionalChargeOnOpen,base)) { reason=base.reason; return false; } value=opening?base.openCommission:base.closeCommission; }
   else if(CommissionPercentCalculationBase==COMMISSION_PERCENT_MARGIN)
   {
      if(margin<=0) { reason="COMMISSION_MARGIN_BASE_UNAVAILABLE"; return false; }
      value=margin*CommissionPercent/100.0;
   }
   else { reason="COMMISSION_PERCENT_BASE_DISABLED"; return false; }
   return MathIsValidNumber(value)&&value>=0;
}

bool CalcCommissionBases(double lot,double contractSize,double openPrice,double closePrice,double percent,CommissionPercentBase mode,bool chargeNotionalOnOpen,CommissionBaseResult &r)
{
   r.valid=false; r.reason=""; r.notionalOpen=lot*contractSize*openPrice; r.notionalClose=lot*contractSize*closePrice; r.openTurnover=r.notionalOpen; r.closeTurnover=r.notionalClose; r.totalTurnover=r.openTurnover+r.closeTurnover; r.openCommission=0; r.closeCommission=0;
   if(lot<=0||contractSize<=0||openPrice<=0||closePrice<=0||percent<0) { r.reason="COMMISSION_BASE_INVALID"; return false; }
   if(mode==COMMISSION_PERCENT_NOTIONAL) { if(chargeNotionalOnOpen) r.openCommission=r.notionalOpen*percent/100.0; else r.closeCommission=r.notionalClose*percent/100.0; }
   else if(mode==COMMISSION_PERCENT_TURNOVER) { r.openCommission=r.openTurnover*percent/100.0; r.closeCommission=r.closeTurnover*percent/100.0; }
   else { r.reason="COMMISSION_BASE_UNSUPPORTED"; return false; }
   r.valid=true; return true;
}

bool CalcProjectedOpenCommission(double lot,double openPrice,double closePrice,double margin,double &value,string &reason)
{
   if(CommissionPerLotPerSide>0) { value=lot*CommissionPerLotPerSide; return true; }
   if(CommissionPerLotRoundTurn>0) { value=lot*CommissionPerLotRoundTurn*.5; return true; }
   if(CommissionFixedPerDeal>0) { value=CommissionFixedPerDeal; return true; }
   if(CommissionPercent>0) return CalcPercentCommissionSide(lot,openPrice,closePrice,margin,true,value,reason);
   value=lot*EstimatedOpenCommissionPerLot; return true;
}
bool CalcProjectedCloseCommission(double lot,double openPrice,double closePrice,double margin,double &value,string &reason)
{
   if(CommissionPerLotPerSide>0) { value=lot*CommissionPerLotPerSide; return true; }
   if(CommissionPerLotRoundTurn>0) { value=lot*CommissionPerLotRoundTurn*.5; return true; }
   if(CommissionFixedPerDeal>0) { value=CommissionFixedPerDeal; return true; }
   if(CommissionPercent>0) return CalcPercentCommissionSide(lot,closePrice,openPrice,margin,false,value,reason);
   value=lot*EstimatedCloseCommissionPerLot; return true;
}

bool CalcSignedBrokerSwap(Direction direction,double lot,datetime openTime,datetime projectedCloseTime,SignedSwapResult &result)
{
   result.calculationValid=false; result.expectedSignedSwap=0; result.worstCaseSwapCost=0; result.additionalSwapBuffer=MathMax(0.0,AdditionalSwapSafetyMoney); result.chargedDays=0; result.rolloverMultipliers=0; result.dailyBreakdown=""; result.reason="";
   if(lot<=0||projectedCloseTime<=openTime) { result.calculationValid=true; return true; }
   if(!UseBrokerSwapProperties) { result.expectedSignedSwap=-MathMax(0.0,EstimatedSwapBufferMoney)*lot; result.worstCaseSwapCost=MathMax(0.0,-result.expectedSignedSwap); result.calculationValid=true; return true; }
   double rate=SymbolInfoDouble(_Symbol,direction==DIR_BUY?SYMBOL_SWAP_LONG:SYMBOL_SWAP_SHORT);
   long mode=SymbolInfoInteger(_Symbol,SYMBOL_SWAP_MODE);
   if(!MathIsValidNumber(rate)) { result.reason="SWAP_PROPERTY_INVALID"; return false; }
   if(mode==SYMBOL_SWAP_MODE_DISABLED) { result.calculationValid=true; return true; }
   int rollover=(int)SymbolInfoInteger(_Symbol,SYMBOL_SWAP_ROLLOVER3DAYS);
   double signedDaily=0;
   if(mode==SYMBOL_SWAP_MODE_POINTS)
   {
      double onePoint=BrokerPointsCostMoney(lot,1.0); if(onePoint<0) { result.reason="SWAP_CONVERSION_FAILED"; return false; }
      signedDaily=onePoint*rate;
   }
   else { if(EstimatedSwapBufferMoney<=0) { result.reason="SWAP_MODE_REQUIRES_FALLBACK"; return false; } signedDaily=(rate>=0?1:-1)*EstimatedSwapBufferMoney*lot; }
   datetime cursor=openTime;
   while(cursor<projectedCloseTime)
   {
      cursor+=86400; if(cursor>projectedCloseTime) break;
      MqlDateTime dt; TimeToStruct(cursor,dt); if(dt.day_of_week==0||dt.day_of_week==6) continue;
      int multiplier=(dt.day_of_week==rollover?3:1); result.expectedSignedSwap+=signedDaily*multiplier; result.chargedDays++; result.rolloverMultipliers+=multiplier;
      result.dailyBreakdown+=StringFormat("%04d-%02d-%02d:x%d;",dt.year,dt.mon,dt.day,multiplier);
   }
   result.worstCaseSwapCost=MathMax(0.0,-result.expectedSignedSwap); result.calculationValid=true; return true;
}

bool CalcSignedSwapCalendar(double signedDailyMoney,datetime openTime,datetime closeTime,int rolloverDay,double additionalBuffer,SignedSwapResult &result)
{
   result.calculationValid=false; result.expectedSignedSwap=0; result.worstCaseSwapCost=0; result.additionalSwapBuffer=MathMax(0.0,additionalBuffer); result.chargedDays=0; result.rolloverMultipliers=0; result.dailyBreakdown=""; result.reason="";
   if(closeTime<=openTime) { result.calculationValid=true; return true; }
   datetime cursor=openTime; while(cursor<closeTime) { cursor+=86400; if(cursor>closeTime) break; MqlDateTime dt; TimeToStruct(cursor,dt); if(dt.day_of_week==0||dt.day_of_week==6) continue; int multiplier=(dt.day_of_week==rolloverDay?3:1); result.expectedSignedSwap+=signedDailyMoney*multiplier; result.chargedDays++; result.rolloverMultipliers+=multiplier; result.dailyBreakdown+=StringFormat("%04d-%02d-%02d:x%d;",dt.year,dt.mon,dt.day,multiplier); }
   result.worstCaseSwapCost=MathMax(0.0,-result.expectedSignedSwap)+result.additionalSwapBuffer; result.calculationValid=true; return true;
}

bool CalcProjectedPositionNetMoneyForHolding(Direction direction,double lot,double openPrice,double closePrice,bool includeOpenCommission,bool includeCloseCommission,int holdingDays,double accruedSwap,BrokerMoneyResult &r)
{
   ResetBrokerMoneyResult(r);
   if(direction==DIR_NONE||lot<=0||openPrice<=0||closePrice<=0) { r.reason="BROKER_MONEY_INVALID_INPUT"; return false; }
   if(!ValidateCommissionModel(r.reason)) return false;
   double gross=0; ENUM_ORDER_TYPE type=direction==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL;
   if(!OrderCalcProfit(type,_Symbol,lot,openPrice,closePrice,gross)) { r.reason="BROKER_MONEY_ORDERCALCPROFIT_FAILED"; return false; }
   r.grossProfit=gross; r.baseSpreadIncludedInPrices=true; r.baseSpreadCost=0; // execution Bid/Ask already contains base spread
   r.spreadExpansionCost=BrokerPointsCostMoney(lot,SpreadExpansionBufferPoints);
   r.slippageCost=BrokerPointsCostMoney(lot,MaxSlippagePoints*SlippageSafetyMultiplier);
   if(r.spreadExpansionCost<0||r.slippageCost<0) { r.reason="BROKER_MONEY_TICK_VALUE_FAILED"; return false; }
   double margin=0; OrderCalcMargin(type,_Symbol,lot,openPrice,margin);
   if(includeOpenCommission&&!CalcProjectedOpenCommission(lot,openPrice,closePrice,margin,r.openCommission,r.reason)) return false;
   if(includeCloseCommission&&!CalcProjectedCloseCommission(lot,openPrice,closePrice,margin,r.closeCommission,r.reason)) return false;
   r.accruedSwap=accruedSwap;
   SignedSwapResult signedSwap; if(!CalcSignedBrokerSwap(direction,lot,TimeCurrent(),TimeCurrent()+holdingDays*86400,signedSwap)) { r.reason=signedSwap.reason; return false; }
   r.projectedFutureSwap=signedSwap.expectedSignedSwap; r.worstCaseSwapBuffer=signedSwap.additionalSwapBuffer; r.swap=r.accruedSwap+r.projectedFutureSwap; r.swapBuffer=r.worstCaseSwapBuffer; r.spreadCost=r.spreadExpansionCost;
   r.perOrderBuffer=ExecutionBufferPerOrderMoney; r.perPositionBuffer=ExecutionBufferPerPositionMoney;
   r.safetyBuffer=r.perOrderBuffer+r.perPositionBuffer;
   r.netMoney=r.grossProfit+r.accruedSwap+r.projectedFutureSwap-r.openCommission-r.closeCommission-r.fee-r.worstCaseSwapBuffer-r.spreadExpansionCost-r.slippageCost-r.safetyBuffer;
   r.calculationValid=true; r.ok=true; return true;
}

bool CalcProjectedPositionNetMoney(Direction d,double lot,double open,double close,bool openCommission,bool closeCommission,BrokerMoneyResult &r) { return CalcProjectedPositionNetMoneyForHolding(d,lot,open,close,openCommission,closeCommission,ExpectedHoldingDays,0,r); }
bool CalcProjectedCloseNetMoneyWithAccrued(Direction d,double lot,double open,double close,double accruedSwap,BrokerMoneyResult &r) { return CalcProjectedPositionNetMoneyForHolding(d,lot,open,close,false,true,0,accruedSwap,r); }
bool CalcProjectedCloseNetMoney(Direction d,double lot,double open,double close,BrokerMoneyResult &r) { return CalcProjectedCloseNetMoneyWithAccrued(d,lot,open,close,0,r); }
bool CalcProjectedOpenAndCloseCosts(double lot,BrokerMoneyResult &r)
{
   ResetBrokerMoneyResult(r); if(!ValidateCommissionModel(r.reason)||lot<=0) return false;
   double price=BrokerExecutionOpenPrice(DIR_BUY),margin=0; if(!CalcProjectedOpenCommission(lot,price,price,margin,r.openCommission,r.reason)||!CalcProjectedCloseCommission(lot,price,price,margin,r.closeCommission,r.reason)) return false; double commission=r.openCommission+r.closeCommission;
   r.spreadExpansionCost=BrokerPointsCostMoney(lot,SpreadExpansionBufferPoints); r.slippageCost=BrokerPointsCostMoney(lot,MaxSlippagePoints*SlippageSafetyMultiplier);
   r.perOrderBuffer=ExecutionBufferPerOrderMoney*2; r.perPositionBuffer=ExecutionBufferPerPositionMoney; r.safetyBuffer=r.perOrderBuffer+r.perPositionBuffer;
   if(r.spreadExpansionCost<0||r.slippageCost<0) return false; r.spreadCost=r.spreadExpansionCost;
   r.netMoney=-(commission+r.spreadExpansionCost+r.slippageCost+r.safetyBuffer); r.calculationValid=true; r.ok=true; return true;
}
bool CalcProjectedMarginMoney(ENUM_ORDER_TYPE type,double lot,double price,BrokerMoneyResult &r)
{
   ResetBrokerMoneyResult(r); double margin=0; if(lot<=0||price<=0||!OrderCalcMargin(type,_Symbol,lot,price,margin)) { r.reason="BROKER_MARGIN_FAILED"; return false; }
   r.requiredMargin=margin; r.marginMoney=margin; r.calculationValid=true; r.ok=true; return true;
}
bool CalcProjectedBasketNetMoney(BrokerMoneyResult &items[],int count,BrokerMoneyResult &r)
{
   ResetBrokerMoneyResult(r); if(count<0) return false;
   for(int i=0;i<count;i++) { if(!items[i].calculationValid&&!items[i].ok) { r.reason="BROKER_BASKET_ITEM_INVALID"; return false; }
      r.grossProfit+=items[i].grossProfit; r.openCommission+=items[i].openCommission; r.closeCommission+=items[i].closeCommission; r.fee+=items[i].fee; r.swap+=items[i].swap; r.accruedSwap+=items[i].accruedSwap; r.projectedFutureSwap+=items[i].projectedFutureSwap; r.worstCaseSwapBuffer+=items[i].worstCaseSwapBuffer;
      r.baseSpreadCost+=items[i].baseSpreadCost; r.spreadExpansionCost+=items[i].spreadExpansionCost; r.slippageCost+=items[i].slippageCost; r.perOrderBuffer+=items[i].perOrderBuffer; r.perPositionBuffer+=items[i].perPositionBuffer; r.requiredMargin+=items[i].requiredMargin; }
   r.basketBuffer=ExecutionBufferPerBasketMoney; r.netMoney=r.grossProfit+r.accruedSwap+r.projectedFutureSwap-r.openCommission-r.closeCommission-r.fee-r.worstCaseSwapBuffer-r.spreadExpansionCost-r.slippageCost-r.perOrderBuffer-r.perPositionBuffer-r.basketBuffer;
   r.swapBuffer=r.swap; r.spreadCost=r.spreadExpansionCost; r.marginMoney=r.requiredMargin; r.safetyBuffer=r.perOrderBuffer+r.perPositionBuffer+r.basketBuffer; r.calculationValid=true; r.ok=true; return true;
}
bool CalcFarCloseLossWorstCaseMoney(Direction d,double lot,double open,double close,double &loss) { BrokerMoneyResult r; if(!CalcProjectedCloseNetMoney(d,lot,open,close,r)) return false; loss=MathMax(0,-r.netMoney); return true; }
bool CalcMoveRecoveryDeltaMoney(Direction d,double lot,double open,double close,double &delta) { BrokerMoneyResult r; if(!CalcProjectedPositionNetMoney(d,lot,open,close,true,true,r)) return false; delta=r.netMoney; return true; }
bool CalcProjectedTransitionNetMoney(BrokerMoneyResult &legs[],int count,BrokerMoneyResult &r) { return CalcProjectedBasketNetMoney(legs,count,r); }

bool EvaluateBigGeometryAndRecovery(double farLot,double coreLot,double trendLot,double smallLot,
                                    BrokerMoneyResult &core,BrokerMoneyResult &trend,BrokerMoneyResult &small,BrokerMoneyResult &far,
                                    BigRecoveryEvaluation &e)
{
   e.calculationValid=core.ok&&trend.ok&&small.ok&&far.ok; e.netBigExposure=coreLot+trendLot-smallLot-farLot;
   e.costs=(core.grossProfit-core.netMoney)+(trend.grossProfit-trend.netMoney)+(small.grossProfit-small.netMoney)+(far.grossProfit-far.netMoney);
   e.projectedRecoveryDelta=core.netMoney+trend.netMoney+small.netMoney+far.netMoney;
   e.geometryPass=e.netBigExposure>=MinimumNetBigExposureLots; e.recoveryPass=e.projectedRecoveryDelta>MinimumBigRecoveryImprovementMoney+MoneyCalculationTolerance;
   e.reason=!e.calculationValid?"BIG_RECOVERY_CALCULATION_FAILED":(!e.geometryPass?"BIG_NET_EXPOSURE_TOO_SMALL":(!e.recoveryPass?"BIG_RECOVERY_DELTA_TOO_SMALL":"OK"));
   return e.calculationValid&&e.geometryPass&&e.recoveryPass;
}

bool EvaluateBigReserveCatchUp(double reserveBefore,double reserveAfter,double carryBefore,double carryAfter,double farLotBefore,double farLotAfter,double farLossBefore,double farLossAfter,double partialCost,BigReserveCatchUpEvaluation &e)
{
   e.reserveBefore=reserveBefore; e.reserveAfter=reserveAfter; e.carryBefore=carryBefore; e.carryAfter=carryAfter; e.farLotBefore=farLotBefore; e.farLotAfter=farLotAfter; e.farLossBefore=farLossBefore; e.farLossAfter=farLossAfter; e.partialFarActualCost=partialCost;
   e.coverageBefore=farLossBefore>0?(reserveBefore+carryBefore)/farLossBefore:1.0;
   e.coverageAfter=farLossAfter>0?(reserveAfter+carryAfter)/farLossAfter:1.0;
   e.pass=e.coverageAfter>e.coverageBefore+CoverageImprovementTolerance; e.reason=e.pass?"OK":"BIG_RESERVE_COVERAGE_NOT_IMPROVED"; return e.pass;
}

double CalcTargetNewFarLot(double oldFarLot)
{
   if(oldFarLot<=0) return 0; return NormalizeLotDown(oldFarLot*MaximumNewFarRatio);
}

bool EvaluateSmallTransition(SmallTransitionLeg &legs[],double oldFarLot,double projectedNewFarLot,double netSmallExposure,double marginLevel,SmallTransitionEvaluation &e)
{
   if(ArraySize(legs)!=5) { e.calculationValid=false; e.transitionAllowed=false; e.reason="SMALL_REQUIRES_EXACTLY_FIVE_LEGS"; return false; }
   BrokerMoneyResult money[5]; bool seen[5]={false,false,false,false,false}; int oldFarIndex=-1,coreIndex=-1,reverseIndex=-1;
   for(int i=0;i<5;i++) { int role=(int)legs[i].role; if(role<0||role>=5||seen[role]||!legs[i].money.calculationValid) { e.calculationValid=false; e.transitionAllowed=false; e.reason="SMALL_LEG_CONTRACT_INVALID"; return false; } seen[role]=true; money[i]=legs[i].money; if(role==SMALL_LEG_OLD_FAR_CLOSE) oldFarIndex=i; if(role==SMALL_LEG_BIG_CORE_PARTIAL) coreIndex=i; if(role==SMALL_LEG_REVERSE_SMALL) reverseIndex=i; }
   if(oldFarIndex<0||coreIndex<0||reverseIndex<0||!legs[oldFarIndex].fullClose||legs[coreIndex].residualLot<=0||!legs[reverseIndex].includesOpenAndClose) { e.calculationValid=false; e.transitionAllowed=false; e.reason="SMALL_LEG_SEMANTICS_INVALID"; return false; }
   BrokerMoneyResult basket; ResetBrokerMoneyResult(basket); e.calculationValid=CalcProjectedTransitionNetMoney(money,5,basket);
   e.transitionNet=basket.netMoney; e.commission=basket.openCommission+basket.closeCommission; e.swap=basket.swap; e.spreadExpansion=basket.spreadExpansionCost; e.slippage=basket.slippageCost; e.buffers=basket.safetyBuffer;
   e.oldFarLot=oldFarLot; e.targetNewFarLot=CalcTargetNewFarLot(oldFarLot); e.projectedNewFarLot=projectedNewFarLot; e.compressionRatio=oldFarLot>0?projectedNewFarLot/oldFarLot:1; e.netSmallExposure=netSmallExposure; e.projectedMarginLevel=marginLevel;
   e.moneyPass=e.calculationValid&&e.transitionNet>=MinimumTransitionProfitMoney; e.exposurePass=netSmallExposure>VolumeMismatchToleranceLots;
   e.compressionPass=projectedNewFarLot<oldFarLot&&(oldFarLot-projectedNewFarLot)>=MinimumFarCompressionLots&&e.compressionRatio<=MaximumNewFarRatio;
   e.marginPass=marginLevel>=MinimumSafeMarginLevel; e.transitionAllowed=e.moneyPass&&e.exposurePass&&e.compressionPass&&e.marginPass;
   e.reason=e.transitionAllowed?"OK":(!e.moneyPass?"SMALL_TRANSITION_MONEY_FAIL":(!e.compressionPass?"SMALL_COMPRESSION_FAIL":(!e.marginPass?"SMALL_MARGIN_FAIL":"SMALL_EXPOSURE_FAIL"))); return e.transitionAllowed;
}

bool EvaluateBigBasketGate(Direction directions[],double lots[],int managedPositions,BigBasketGate &g)
{
   g.totalMargin=0; g.projectedMarginLevel=0; g.volumePass=true; g.marginPass=false; g.positionsPass=(managedPositions+3<=MaxManagedPositions); g.reason="";
   if(ArraySize(directions)!=3||ArraySize(lots)!=3) { g.reason="BIG_BASKET_REQUIRES_THREE_LEGS"; return false; }
   double minLot=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MIN),maxLot=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MAX),step=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_STEP),limit=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_LIMIT);
   double plannedBuy=0,plannedSell=0,existingBuy=0,existingSell=0;
   for(int j=0;j<3;j++) { if(directions[j]==DIR_BUY) plannedBuy+=lots[j]; else if(directions[j]==DIR_SELL) plannedSell+=lots[j]; else g.volumePass=false; }
   for(int p=0;p<PositionsTotal();p++) { ulong ticket=PositionGetTicket(p); if(ticket==0||!PositionSelectByTicket(ticket)||PositionGetString(POSITION_SYMBOL)!=_Symbol) continue; if(PositionGetInteger(POSITION_TYPE)==POSITION_TYPE_BUY) existingBuy+=PositionGetDouble(POSITION_VOLUME); else existingSell+=PositionGetDouble(POSITION_VOLUME); }
   if(limit>0&&(existingBuy+plannedBuy>limit+VolumeMismatchToleranceLots||existingSell+plannedSell>limit+VolumeMismatchToleranceLots)) g.volumePass=false;
   for(int i=0;i<3;i++)
   {
      if(lots[i]<minLot||lots[i]>maxLot||step<=0||MathAbs(lots[i]/step-MathRound(lots[i]/step))>VolumeMismatchToleranceLots) g.volumePass=false;
      BrokerMoneyResult m; if(!CalcProjectedMarginMoney(directions[i]==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL,lots[i],BrokerExecutionOpenPrice(directions[i]),m)) { g.reason="BIG_BASKET_MARGIN_CALC_FAILED"; return false; } g.totalMargin+=m.requiredMargin;
   }
   double equity=AccountInfoDouble(ACCOUNT_EQUITY),currentMargin=AccountInfoDouble(ACCOUNT_MARGIN); g.projectedMarginLevel=(currentMargin+g.totalMargin)>0?equity/(currentMargin+g.totalMargin)*100.0:999999;
   g.marginPass=g.projectedMarginLevel>=MinimumSafeMarginLevel&&(equity>0?g.totalMargin/equity*100.0:999999)<=MaxAccountMarginPercent;
   g.pass=g.volumePass&&g.marginPass&&g.positionsPass; if(!g.pass&&g.reason=="") g.reason=!g.volumePass?"BIG_BASKET_VOLUME_FAIL":(!g.marginPass?"BIG_BASKET_MARGIN_FAIL":"BIG_BASKET_POSITION_LIMIT"); return g.pass;
}

bool EvaluateRequiredReverseCyclesMoney(double farLot,double farLoss,double reserve,double carry,double recovery,double compression,double transitionNet,double reserveAdd,double carryAdd,double cycleCosts,double targetLot,ReverseCyclesEvaluation &e)
{
   e.requiredCycles=0; e.finalFarLot=farLot; e.finalFarLoss=farLoss; e.projectedReserve=reserve; e.projectedCarry=carry; e.projectedRecoveryPL=recovery; e.finalCoverage=farLoss>0?(reserve+carry)/farLoss:1; e.pass=false; e.reason="REVERSE_LIMIT";
   for(int n=0;n<=MaxReverseCycles;n++) { e.requiredCycles=n; e.finalCoverage=e.finalFarLoss>0?(e.projectedReserve+e.projectedCarry)/e.finalFarLoss:1; if(e.finalFarLot<=targetLot&&e.finalCoverage>=1&&e.projectedRecoveryPL>=MinimumRecoveryProfitMoney) { e.pass=true; e.reason="OK"; return true; } if(n==MaxReverseCycles) break; e.finalFarLot=NormalizeLotDown(e.finalFarLot*compression); e.finalFarLoss*=compression; e.projectedReserve+=reserveAdd; e.projectedCarry+=carryAdd; e.projectedRecoveryPL+=transitionNet-cycleCosts; }
   return false;
}

bool EvaluateSmallPreTradeGate(SmallTransitionLeg &legs[],double oldFar,double newFar,double exposure,double marginLevel,ReverseCyclesEvaluation &cycles,SmallTransitionEvaluation &transition)
{
   if(!cycles.pass||cycles.requiredCycles>MaxReverseCycles) { transition.reason="SMALL_REVERSE_COUNT_FAIL"; return false; }
   return EvaluateSmallTransition(legs,oldFar,newFar,exposure,marginLevel,transition)&&transition.transitionNet>=MinimumTransitionProfitMoney&&newFar<oldFar&&marginLevel>=MinimumSafeMarginLevel;
}

bool EvaluateFalseReverseMoney(FalseReverseOption &candidates[],double minimumRecovery,FalseReverseEvaluation &evaluation)
{
   evaluation.selected=FALSE_REVERSE_MANUAL; evaluation.automaticAllowed=false; evaluation.reason="NO_SAFE_FALSE_REVERSE_OPTION";
   if(ArraySize(candidates)!=6) return false;
   double best=-DBL_MAX;
   for(int i=0;i<6;i++) { evaluation.options[i]=candidates[i]; evaluation.options[i].safe=candidates[i].projectedRecoveryPL>=minimumRecovery&&candidates[i].projectedMarginLevel>=MinimumSafeMarginLevel&&candidates[i].reserveImpact<=0; if(evaluation.options[i].safe&&evaluation.options[i].projectedNet>best) { best=evaluation.options[i].projectedNet; evaluation.selected=evaluation.options[i].action; evaluation.automaticAllowed=true; } }
   if(evaluation.automaticAllowed) evaluation.reason="SAFE_FALSE_REVERSE_OPTION_SELECTED"; return evaluation.automaticAllowed;
}

int EvaluateRequiredReverseCycles(double currentFar,double targetLot,double compressionRatio)
{
   if(currentFar<=targetLot) return 0; if(compressionRatio<=0||compressionRatio>=1) return MaxReverseCycles+1;
   double lot=currentFar; for(int n=1;n<=MaxReverseCycles;n++) { lot=NormalizeLotDown(lot*compressionRatio); if(lot<=targetLot) return n; }
   return MaxReverseCycles+1;
}

#endif
