#ifndef __BH_SIMULATIONENGINE_MQH__
#define __BH_SIMULATIONENGINE_MQH__

PositionSnapshot SimPositions[];
ulong SimNextTicket = 900000001;

double SimEntryPrice(Direction dir)
{
   if(dir == DIR_BUY)
      return SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   if(dir == DIR_SELL)
      return SymbolInfoDouble(_Symbol, SYMBOL_BID);

   return 0.0;
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
   if(dir == DIR_NONE || lot <= 0.0)
      return false;

   int index = ArraySize(SimPositions);
   ArrayResize(SimPositions, index + 1);

   SimPositions[index].exists = true;
   SimPositions[index].ticket = SimNextTicket++;
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
   int index = SimFindIndexByTicket(ticket);
   if(index < 0 || lot <= 0.0)
      return false;

   double closeLot = lot;
   if(closeLot > SimPositions[index].lot)
      closeLot = SimPositions[index].lot;

   PrintFormat(
      "[BigHarvest][SIMULATION] CLOSE ticket=%I64u comment=%s direction=%s requestedLot=%.2f closedLot=%.2f lotBefore=%.2f",
      ticket,
      SimPositions[index].comment,
      DirectionToString(SimPositions[index].direction),
      lot,
      closeLot,
      SimPositions[index].lot
   );

   if(closeLot >= SimPositions[index].lot - 0.000000001)
   {
      int last = ArraySize(SimPositions) - 1;
      if(index != last)
         SimPositions[index] = SimPositions[last];
      ArrayResize(SimPositions, last);
      return true;
   }

   SimPositions[index].lot = SimPositions[index].lot - closeLot;
   return true;
}

#endif // __BH_SIMULATIONENGINE_MQH__
