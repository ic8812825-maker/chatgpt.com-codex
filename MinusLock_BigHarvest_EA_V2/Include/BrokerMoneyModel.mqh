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

void ResetBrokerMoneyResult(BrokerMoneyResult &r)
{
   r.calculationValid=false; r.ok=false; r.grossProfit=0; r.openCommission=0; r.closeCommission=0; r.fee=0;
   r.swap=0; r.swapBuffer=0; r.baseSpreadCost=0; r.spreadExpansionCost=0; r.spreadCost=0; r.slippageCost=0;
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

bool ValidateCommissionModel(string &reason)
{
   if(CommissionPerLotPerSide<0||CommissionPerLotRoundTurn<0||CommissionFixedPerDeal<0||CommissionPercent<0) { reason="COMMISSION_NEGATIVE"; return false; }
   int models=(CommissionPerLotPerSide>0?1:0)+(CommissionPerLotRoundTurn>0?1:0)+(CommissionFixedPerDeal>0?1:0)+(CommissionPercent>0?1:0);
   if(models>1) { reason="COMMISSION_MODE_CONFLICT"; return false; }
   return true;
}

double ProjectedCommission(double lot,double grossAbs,bool oneSide)
{
   if(CommissionPerLotPerSide>0) return lot*CommissionPerLotPerSide*(oneSide?1:2);
   if(CommissionPerLotRoundTurn>0) return lot*CommissionPerLotRoundTurn*(oneSide?0.5:1.0);
   if(CommissionFixedPerDeal>0) return CommissionFixedPerDeal*(oneSide?1:2);
   if(CommissionPercent>0) return grossAbs*CommissionPercent/100.0;
   return lot*((oneSide?EstimatedCloseCommissionPerLot:(EstimatedOpenCommissionPerLot+EstimatedCloseCommissionPerLot)));
}

bool ProjectedSwapMoney(Direction direction,double lot,int days,double &cost,string &reason)
{
   cost=AdditionalSwapSafetyMoney;
   if(days<=0) return true;
   if(!UseBrokerSwapProperties) { cost+=MathMax(0.0,EstimatedSwapBufferMoney)*lot*days; return true; }
   double rate=SymbolInfoDouble(_Symbol,direction==DIR_BUY?SYMBOL_SWAP_LONG:SYMBOL_SWAP_SHORT);
   long mode=SymbolInfoInteger(_Symbol,SYMBOL_SWAP_MODE);
   if(!MathIsValidNumber(rate)) { reason="SWAP_PROPERTY_INVALID"; return false; }
   if(mode==SYMBOL_SWAP_MODE_DISABLED) return true;
   if(mode==SYMBOL_SWAP_MODE_POINTS)
   {
      double daily=BrokerPointsCostMoney(lot,MathAbs(rate)); if(daily<0) { reason="SWAP_CONVERSION_FAILED"; return false; }
      cost+=daily*days; return true;
   }
   // Non-point broker modes are already account-currency dependent; require an explicit conservative fallback.
   if(EstimatedSwapBufferMoney<=0) { reason="SWAP_MODE_REQUIRES_FALLBACK"; return false; }
   cost+=EstimatedSwapBufferMoney*lot*days; return true;
}

bool CalcProjectedPositionNetMoney(Direction direction,double lot,double openPrice,double closePrice,bool includeOpenCommission,bool includeCloseCommission,BrokerMoneyResult &r)
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
   double totalCommission=ProjectedCommission(lot,MathAbs(gross),!(includeOpenCommission&&includeCloseCommission));
   r.openCommission=includeOpenCommission?(includeCloseCommission?totalCommission*0.5:totalCommission):0;
   r.closeCommission=includeCloseCommission?(includeOpenCommission?totalCommission*0.5:totalCommission):0;
   if(!ProjectedSwapMoney(direction,lot,MaximumHoldingDays,r.swap,r.reason)) return false;
   r.swapBuffer=r.swap; r.spreadCost=r.spreadExpansionCost;
   r.perOrderBuffer=ExecutionBufferPerOrderMoney; r.perPositionBuffer=ExecutionBufferPerPositionMoney;
   r.safetyBuffer=r.perOrderBuffer+r.perPositionBuffer;
   r.netMoney=r.grossProfit-r.openCommission-r.closeCommission-r.fee-r.swap-r.spreadExpansionCost-r.slippageCost-r.safetyBuffer;
   r.calculationValid=true; r.ok=true; return true;
}

bool CalcProjectedCloseNetMoney(Direction d,double lot,double open,double close,BrokerMoneyResult &r) { return CalcProjectedPositionNetMoney(d,lot,open,close,false,true,r); }
bool CalcProjectedOpenAndCloseCosts(double lot,BrokerMoneyResult &r)
{
   ResetBrokerMoneyResult(r); if(!ValidateCommissionModel(r.reason)||lot<=0) return false;
   double commission=ProjectedCommission(lot,0,false); r.openCommission=commission*.5; r.closeCommission=commission*.5;
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
      r.grossProfit+=items[i].grossProfit; r.openCommission+=items[i].openCommission; r.closeCommission+=items[i].closeCommission; r.fee+=items[i].fee; r.swap+=items[i].swap;
      r.baseSpreadCost+=items[i].baseSpreadCost; r.spreadExpansionCost+=items[i].spreadExpansionCost; r.slippageCost+=items[i].slippageCost; r.perOrderBuffer+=items[i].perOrderBuffer; r.perPositionBuffer+=items[i].perPositionBuffer; r.requiredMargin+=items[i].requiredMargin; }
   r.basketBuffer=ExecutionBufferPerBasketMoney; r.netMoney=r.grossProfit-r.openCommission-r.closeCommission-r.fee-r.swap-r.spreadExpansionCost-r.slippageCost-r.perOrderBuffer-r.perPositionBuffer-r.basketBuffer;
   r.swapBuffer=r.swap; r.spreadCost=r.spreadExpansionCost; r.marginMoney=r.requiredMargin; r.safetyBuffer=r.perOrderBuffer+r.perPositionBuffer+r.basketBuffer; r.calculationValid=true; r.ok=true; return true;
}
bool CalcFarCloseLossWorstCaseMoney(Direction d,double lot,double open,double close,double &loss) { BrokerMoneyResult r; if(!CalcProjectedCloseNetMoney(d,lot,open,close,r)) return false; loss=MathMax(0,-r.netMoney); return true; }
bool CalcMoveRecoveryDeltaMoney(Direction d,double lot,double open,double close,double &delta) { BrokerMoneyResult r; if(!CalcProjectedPositionNetMoney(d,lot,open,close,true,true,r)) return false; delta=r.netMoney; return true; }
bool CalcProjectedTransitionNetMoney(BrokerMoneyResult &legs[],int count,BrokerMoneyResult &r) { return CalcProjectedBasketNetMoney(legs,count,r); }

#endif
