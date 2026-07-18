#ifndef __BH_SIMULATIONENGINE_MQH__
#define __BH_SIMULATIONENGINE_MQH__

PositionSnapshot SimPositions[];
SimDealSnapshot SimDeals[];
ulong SimNextPositionTicket = 900000001;
ulong SimNextDealTicket = 990000001;
double SimRealizedPL = 0.0;
double SimClosedProfit = 0.0;
double SimClosedLoss = 0.0;

void SimResetHistory()
{
   ArrayResize(SimPositions, 0);
   ArrayResize(SimDeals, 0);
   SimNextPositionTicket = 900000001;
   SimNextDealTicket = 990000001;
   SimRealizedPL = 0.0;
   SimClosedProfit = 0.0;
   SimClosedLoss = 0.0;
   TestMarketEventActive=false;
}

double SimEntryPrice(Direction dir)
{
   if(dir == DIR_BUY)
      return MarketAsk();
   if(dir == DIR_SELL)
      return MarketBid();

   return 0.0;
}

double SimExitPrice(Direction dir)
{
   if(dir == DIR_BUY)
      return MarketBid();
   if(dir == DIR_SELL)
      return MarketAsk();

   return 0.0;
}

double SimPointValuePerLot()
{
   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   double point     = SymbolInfoDouble(_Symbol, SYMBOL_POINT);

   if(tickSize <= 0.0 || point <= 0.0)
      return 0.0;

   return tickValue * point / tickSize;
}

double SimSignedPositionPL(Direction dir, double lot, double openPrice, double closePrice)
{
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   double pointValue = SimPointValuePerLot();

   if(point <= 0.0 || pointValue <= 0.0 || lot <= 0.0 || openPrice <= 0.0 || closePrice <= 0.0)
      return 0.0;

   if(dir == DIR_BUY)
      return lot * ((closePrice - openPrice) / point) * pointValue;

   if(dir == DIR_SELL)
      return lot * ((openPrice - closePrice) / point) * pointValue;

   return 0.0;
}

void SimRecordClosedDeal(ulong ticket, ulong identifier, Direction dir, double lot, double openPrice, double closePrice, double profitMoney, double commission, double swap, double fee, string comment)
{
   int index = ArraySize(SimDeals);
   ArrayResize(SimDeals, index + 1);

   SimDeals[index].ticket = SimNextDealTicket++;
   SimDeals[index].positionTicket = ticket;
   SimDeals[index].positionIdentifier = identifier;
   SimDeals[index].entry = DEAL_ENTRY_OUT;
   SimDeals[index].dealTime = TestMarketEventActive && ActiveTestMarketEvent.time > 0 ? ActiveTestMarketEvent.time : TimeCurrent();
   SimDeals[index].direction = dir;
   SimDeals[index].lot = lot;
   SimDeals[index].openPrice = openPrice;
   SimDeals[index].closePrice = closePrice;
   SimDeals[index].profitMoney = profitMoney;
   SimDeals[index].commission = commission;
   SimDeals[index].swap = swap;
   SimDeals[index].fee = fee;
   SimDeals[index].netMoney = profitMoney + commission + swap + fee;
   SimDeals[index].comment = comment;

   SimRealizedPL += SimDeals[index].netMoney;
   if(SimDeals[index].netMoney >= 0.0)
      SimClosedProfit += SimDeals[index].netMoney;
   else
      SimClosedLoss += SimDeals[index].netMoney;
}

int SimFindIndexByTicket(ulong ticket)
{
   for(int i = 0; i < ArraySize(SimPositions); i++)
   {
      if(SimPositions[i].exists && SimPositions[i].ticket == ticket)
         return i;
   }

   return -1;
}

int SimFindIndexByComment(string comment)
{
   for(int i = 0; i < ArraySize(SimPositions); i++)
   {
      if(SimPositions[i].exists && SimPositions[i].comment == comment)
         return i;
   }

   return -1;
}

bool SimGetPositionByTicket(ulong ticket, PositionSnapshot &snapshot)
{
   snapshot.exists = false;

   int index = SimFindIndexByTicket(ticket);
   if(index < 0)
      return false;

   snapshot = SimPositions[index];
   return true;
}

bool SimGetPositionByComment(string comment, PositionSnapshot &snapshot)
{
   snapshot.exists = false;

   int index = SimFindIndexByComment(comment);
   if(index < 0)
      return false;

   snapshot = SimPositions[index];
   return true;
}

int SimCountOpenPositions()
{
   int count = 0;

   for(int i = 0; i < ArraySize(SimPositions); i++)
   {
      if(SimPositions[i].exists && SimPositions[i].lot > 0.0)
         count++;
   }

   return count;
}

int SimCountFarLikePositions(Direction expectedFarDirection)
{
   int count = 0;

   for(int i = 0; i < ArraySize(SimPositions); i++)
   {
      if(SimPositions[i].exists && SimPositions[i].direction == expectedFarDirection && SimPositions[i].lot > 0.0)
         count++;
   }

   return count;
}

bool SimOpenPosition(Direction dir, double lot, string comment)
{
   if(TestMarketEventActive&&ActiveTestMarketEvent.rejectOpen) return false;
   if(dir == DIR_NONE || lot <= 0.0)
      return false;

   int index = ArraySize(SimPositions);
   ArrayResize(SimPositions, index + 1);

   SimPositions[index].exists = true;
   SimPositions[index].ticket = SimNextPositionTicket++;
   SimPositions[index].identifier = SimPositions[index].ticket;
   SimPositions[index].direction = dir;
   SimPositions[index].lot = lot;
   SimPositions[index].openPrice = SimEntryPrice(dir);
   SimPositions[index].profitMoney = 0.0;
   SimPositions[index].comment = comment;

   PrintFormat(
      "[BigHarvest][SIMULATION] OPEN comment=%s ticket=%I64u direction=%s lot=%.2f openPrice=%.5f",
      comment,
      SimPositions[index].ticket,
      DirectionToString(dir),
      lot,
      SimPositions[index].openPrice
   );

   return true;
}

bool SimClosePositionByTicket(ulong ticket, double lot)
{
   if(TestMarketEventActive&&ActiveTestMarketEvent.rejectClose) return false;
   int index = SimFindIndexByTicket(ticket);
   if(index < 0 || lot <= 0.0)
      return false;

   double closeLot = lot;
   if(TestMarketEventActive&&ActiveTestMarketEvent.partialFillRatio>0&&ActiveTestMarketEvent.partialFillRatio<1) closeLot*=ActiveTestMarketEvent.partialFillRatio;
   if(closeLot > SimPositions[index].lot)
      closeLot = SimPositions[index].lot;

   double closePrice = SimExitPrice(SimPositions[index].direction);
   double realizedPL = SimSignedPositionPL(
      SimPositions[index].direction,
      closeLot,
      SimPositions[index].openPrice,
      closePrice
   );

   PrintFormat(
      "[BigHarvest][SIMULATION] CLOSE ticket=%I64u comment=%s direction=%s requestedLot=%.2f closedLot=%.2f lotBefore=%.2f closePrice=%.5f realizedPL=%.2f",
      ticket,
      SimPositions[index].comment,
      DirectionToString(SimPositions[index].direction),
      lot,
      closeLot,
      SimPositions[index].lot,
      closePrice,
      realizedPL
   );

   SimRecordClosedDeal(
      ticket,
      SimPositions[index].identifier,
      SimPositions[index].direction,
      closeLot,
      SimPositions[index].openPrice,
      closePrice,
      realizedPL,
      TestMarketEventActive ? ActiveTestMarketEvent.closeCommissionMoney : 0.0,
      TestMarketEventActive ? ActiveTestMarketEvent.swapMoney : 0.0,
      TestMarketEventActive ? ActiveTestMarketEvent.feeMoney : 0.0,
      SimPositions[index].comment
   );

   if(closeLot >= SimPositions[index].lot - 0.000000001)
   {
      int last = ArraySize(SimPositions) - 1;
      if(index != last)
         SimPositions[index] = SimPositions[last];
      ArrayResize(SimPositions, last);
      return true;
   }

   SimPositions[index].lot = NormalizeLotDown(SimPositions[index].lot - closeLot);
   return true;
}

bool SimRecalculateClosedStats(double &realCyclePL, double &closedProfit, double &closedLoss)
{
   realCyclePL = SimRealizedPL;
   closedProfit = SimClosedProfit;
   closedLoss = SimClosedLoss;
   return ArraySize(SimDeals) > 0;
}

#endif // __BH_SIMULATIONENGINE_MQH__
