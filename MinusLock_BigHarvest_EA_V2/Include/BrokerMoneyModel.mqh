#ifndef __BH_BROKERMONEYMODEL_MQH__
#define __BH_BROKERMONEYMODEL_MQH__

struct BrokerMoneyResult
{
   bool ok;
   double grossProfit;
   double openCommission;
   double closeCommission;
   double swapBuffer;
   double spreadCost;
   double slippageCost;
   double safetyBuffer;
   double netMoney;
   double marginMoney;
   string reason;
};

double BrokerSpreadCostMoney(double lot, double spreadPoints)
{
   double tickValueLoss = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE_LOSS);
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   if(tickValueLoss <= 0.0 || tickSize <= 0.0 || point <= 0.0 || lot <= 0.0 || spreadPoints < 0.0)
      return -1.0;
   return lot * spreadPoints * point / tickSize * tickValueLoss;
}

bool CalcProjectedPositionNetMoney(Direction direction,
                                   double lot,
                                   double openPrice,
                                   double closePrice,
                                   bool includeOpenCommission,
                                   bool includeCloseCommission,
                                   BrokerMoneyResult &result)
{
   result.ok = false;
   result.grossProfit = 0.0;
   result.openCommission = 0.0;
   result.closeCommission = 0.0;
   result.swapBuffer = 0.0;
   result.spreadCost = 0.0;
   result.slippageCost = 0.0;
   result.safetyBuffer = ExecutionSafetyBufferMoney;
   result.netMoney = 0.0;
   result.marginMoney = 0.0;
   result.reason = "";

   if(direction == DIR_NONE || lot <= 0.0 || openPrice <= 0.0 || closePrice <= 0.0)
   {
      result.reason = "BROKER_MONEY_INVALID_INPUT";
      return false;
   }

   ENUM_ORDER_TYPE orderType = (direction == DIR_BUY ? ORDER_TYPE_BUY : ORDER_TYPE_SELL);
   double profit = 0.0;
   if(!OrderCalcProfit(orderType, _Symbol, lot, openPrice, closePrice, profit))
   {
      result.reason = "BROKER_MONEY_ORDERCALCPROFIT_FAILED";
      return false;
   }

   double spreadPoints = ((SymbolInfoDouble(_Symbol, SYMBOL_ASK) - SymbolInfoDouble(_Symbol, SYMBOL_BID)) / SymbolInfoDouble(_Symbol, SYMBOL_POINT)) + SpreadExpansionBufferPoints;
   double spreadCost = BrokerSpreadCostMoney(lot, spreadPoints);
   double slippageCost = BrokerSpreadCostMoney(lot, MaxSlippagePoints * SlippageSafetyMultiplier);
   if(spreadCost < 0.0 || slippageCost < 0.0)
   {
      result.reason = "BROKER_MONEY_TICK_VALUE_FAILED";
      return false;
   }

   result.grossProfit = profit;
   result.openCommission = includeOpenCommission ? lot * EstimatedOpenCommissionPerLot : 0.0;
   result.closeCommission = includeCloseCommission ? lot * EstimatedCloseCommissionPerLot : 0.0;
   result.swapBuffer = EstimatedSwapBufferMoney;
   result.spreadCost = spreadCost;
   result.slippageCost = slippageCost;
   result.netMoney = profit - result.openCommission - result.closeCommission - result.swapBuffer - result.spreadCost - result.slippageCost - result.safetyBuffer;
   result.ok = true;
   return true;
}

bool CalcProjectedCloseNetMoney(Direction direction, double lot, double openPrice, double closePrice, BrokerMoneyResult &result)
{
   return CalcProjectedPositionNetMoney(direction, lot, openPrice, closePrice, false, true, result);
}

bool CalcProjectedOpenAndCloseCosts(double lot, BrokerMoneyResult &result)
{
   result.ok = false;
   result.grossProfit = 0.0;
   result.openCommission = lot * EstimatedOpenCommissionPerLot;
   result.closeCommission = lot * EstimatedCloseCommissionPerLot;
   result.swapBuffer = EstimatedSwapBufferMoney;
   result.spreadCost = BrokerSpreadCostMoney(lot, SpreadExpansionBufferPoints);
   result.slippageCost = BrokerSpreadCostMoney(lot, MaxSlippagePoints * SlippageSafetyMultiplier);
   result.safetyBuffer = ExecutionSafetyBufferMoney;
   if(result.spreadCost < 0.0 || result.slippageCost < 0.0)
   {
      result.reason = "BROKER_MONEY_COST_MODEL_FAILED";
      return false;
   }
   result.netMoney = -(result.openCommission + result.closeCommission + result.swapBuffer + result.spreadCost + result.slippageCost + result.safetyBuffer);
   result.ok = true;
   result.reason = "";
   return true;
}

bool CalcProjectedMarginMoney(ENUM_ORDER_TYPE orderType, double lot, double price, BrokerMoneyResult &result)
{
   result.ok = false;
   result.marginMoney = 0.0;
   if(lot <= 0.0 || price <= 0.0)
   {
      result.reason = "BROKER_MARGIN_INVALID_INPUT";
      return false;
   }
   double margin = 0.0;
   if(!OrderCalcMargin(orderType, _Symbol, lot, price, margin))
   {
      result.reason = "BROKER_MARGIN_ORDERCALCMARGIN_FAILED";
      return false;
   }
   result.marginMoney = margin;
   result.ok = true;
   result.reason = "";
   return true;
}

bool CalcProjectedBasketNetMoney(BrokerMoneyResult &items[], int count, BrokerMoneyResult &result)
{
   result.ok = false;
   result.netMoney = 0.0;
   for(int i = 0; i < count; i++)
   {
      if(!items[i].ok)
      {
         result.reason = "BROKER_BASKET_ITEM_INVALID";
         return false;
      }
      result.netMoney += items[i].netMoney;
   }
   result.ok = true;
   result.reason = "";
   return true;
}

bool CalcFarCloseLossWorstCaseMoney(Direction farDirection, double farLot, double farOpenPrice, double closePrice, double &lossMoney)
{
   BrokerMoneyResult result;
   if(!CalcProjectedCloseNetMoney(farDirection, farLot, farOpenPrice, closePrice, result))
      return false;
   lossMoney = MathMax(0.0, -result.netMoney);
   return true;
}

bool CalcMoveRecoveryDeltaMoney(Direction direction, double lot, double openPrice, double closePrice, double &deltaMoney)
{
   BrokerMoneyResult result;
   if(!CalcProjectedPositionNetMoney(direction, lot, openPrice, closePrice, true, true, result))
      return false;
   deltaMoney = result.netMoney;
   return true;
}

#endif
