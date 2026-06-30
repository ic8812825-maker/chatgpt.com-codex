#ifndef __BH_POSITIONUTILS_MQH__
#define __BH_POSITIONUTILS_MQH__

Direction PositionTypeToDirection(long positionType)
{
   if(positionType == POSITION_TYPE_BUY)
      return DIR_BUY;
   if(positionType == POSITION_TYPE_SELL)
      return DIR_SELL;
   return DIR_NONE;
}

double ExitPriceForDirection(Direction dir)
{
   if(dir == DIR_BUY)
      return SymbolInfoDouble(_Symbol, SYMBOL_BID);
   if(dir == DIR_SELL)
      return SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   return 0.0;
}

double EntryPriceForDirection(Direction dir)
{
   if(dir == DIR_BUY)
      return SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   if(dir == DIR_SELL)
      return SymbolInfoDouble(_Symbol, SYMBOL_BID);

   return 0.0;
}

double ProfitPoints(Direction dir, double openPrice)
{
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   if(point <= 0.0 || openPrice <= 0.0)
      return 0.0;

   if(dir == DIR_BUY)
      return (SymbolInfoDouble(_Symbol, SYMBOL_BID) - openPrice) / point;

   if(dir == DIR_SELL)
      return (openPrice - SymbolInfoDouble(_Symbol, SYMBOL_ASK)) / point;

   return 0.0;
}

bool ReadSelectedPosition(PositionSnapshot &snapshot)
{
   snapshot.exists = false;

   if(PositionGetString(POSITION_SYMBOL) != _Symbol)
      return false;

   if((ulong)PositionGetInteger(POSITION_MAGIC) != MagicNumber)
      return false;

   snapshot.exists = true;
   snapshot.ticket = (ulong)PositionGetInteger(POSITION_TICKET);
   snapshot.identifier = (ulong)PositionGetInteger(POSITION_IDENTIFIER);
   snapshot.direction = PositionTypeToDirection(PositionGetInteger(POSITION_TYPE));
   snapshot.lot = PositionGetDouble(POSITION_VOLUME);
   snapshot.openPrice = PositionGetDouble(POSITION_PRICE_OPEN);
   snapshot.profitMoney = PositionGetDouble(POSITION_PROFIT);
   snapshot.comment = PositionGetString(POSITION_COMMENT);

   return true;
}

bool IsManagedPositionForCurrentSymbol()
{
   return PositionGetString(POSITION_SYMBOL) == _Symbol &&
          (ulong)PositionGetInteger(POSITION_MAGIC) == MagicNumber;
}

bool IsManagedPositionForMagic()
{
   return (ulong)PositionGetInteger(POSITION_MAGIC) == MagicNumber;
}

bool GetManagedPositionByTicket(ulong ticket, PositionSnapshot &snapshot)
{
   snapshot.exists = false;

   if(IsInternalSimulationMode())
      return SimGetPositionByTicket(ticket, snapshot);

   if(ticket == 0)
      return false;

   if(!PositionSelectByTicket(ticket))
      return false;

   return ReadSelectedPosition(snapshot);
}

bool GetManagedPositionByComment(string comment, PositionSnapshot &snapshot)
{
   snapshot.exists = false;

   if(IsInternalSimulationMode())
      return SimGetPositionByComment(comment, snapshot);

   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0)
         continue;

      if(!PositionSelectByTicket(ticket))
         continue;

      PositionSnapshot candidate;
      if(!ReadSelectedPosition(candidate))
         continue;

      if(candidate.comment == comment)
      {
         snapshot = candidate;
         return true;
      }
   }

   return false;
}

bool GetInitialBuy(PositionSnapshot &snapshot)
{
   return GetManagedPositionByComment("MinusLock_INITIAL_BUY", snapshot);
}

bool GetInitialSell(PositionSnapshot &snapshot)
{
   return GetManagedPositionByComment("MinusLock_INITIAL_SELL", snapshot);
}

string LevelComment(string prefix, int level)
{
   return StringFormat("MinusLock_%s_L%d", prefix, level);
}

int CountManagedOpenPositions()
{
   if(IsInternalSimulationMode())
      return SimCountOpenPositions();

   int count = 0;

   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0)
         continue;

      if(!PositionSelectByTicket(ticket))
         continue;

      PositionSnapshot snapshot;
      if(ReadSelectedPosition(snapshot))
         count++;
   }

   return count;
}

int CountActiveManagedSymbols()
{
   if(IsInternalSimulationMode())
      return SimCountOpenPositions() > 0 ? 1 : 0;

   string symbols[];
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0)
         continue;

      if(!PositionSelectByTicket(ticket))
         continue;

      if(!IsManagedPositionForMagic())
         continue;

      string symbol = PositionGetString(POSITION_SYMBOL);
      bool known = false;
      for(int j = 0; j < ArraySize(symbols); j++)
      {
         if(symbols[j] == symbol)
         {
            known = true;
            break;
         }
      }
      if(!known)
      {
         int index = ArraySize(symbols);
         ArrayResize(symbols, index + 1);
         symbols[index] = symbol;
      }
   }

   return ArraySize(symbols);
}

bool CurrentSymbolHasManagedPositions()
{
   return CountManagedOpenPositions() > 0;
}

int CountFarLikePositions(Direction expectedFarDirection)
{
   if(IsInternalSimulationMode())
      return SimCountFarLikePositions(expectedFarDirection);

   int count = 0;

   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0)
         continue;

      if(!PositionSelectByTicket(ticket))
         continue;

      PositionSnapshot snapshot;
      if(!ReadSelectedPosition(snapshot))
         continue;

      if(snapshot.direction == expectedFarDirection && snapshot.lot > 0.0)
         count++;
   }

   return count;
}

double GetActualPositionVolume(ulong ticket)
{
   if(ticket == 0)
      return 0.0;

   if(IsInternalSimulationMode())
   {
      PositionSnapshot snapshot;
      if(GetManagedPositionByTicket(ticket, snapshot))
         return NormalizeVolumeToStep(snapshot.lot);
      return 0.0;
   }

   if(!PositionSelectByTicket(ticket))
      return 0.0;

   if(PositionGetString(POSITION_SYMBOL) != _Symbol)
      return 0.0;
   if((ulong)PositionGetInteger(POSITION_MAGIC) != MagicNumber)
      return 0.0;

   return NormalizeVolumeToStep(PositionGetDouble(POSITION_VOLUME));
}

bool RefreshLegVolumeFromTerminal(ulong ticket, double &targetLot, string legName)
{
   double actualVolume = GetActualPositionVolume(ticket);
   double normalizedVolume = NormalizeVolumeToStep(actualVolume);
   LogInfo(StringFormat("REFRESH_LEG_VOLUME_FROM_TERMINAL Leg=%s Ticket=%I64u ActualVolume=%.2f NormalizedVolume=%.2f", legName, ticket, actualVolume, normalizedVolume));

   if(normalizedVolume <= 0.0)
   {
      targetLot = 0.0;
      return false;
   }

   targetLot = normalizedVolume;
   return true;
}

#endif // __BH_POSITIONUTILS_MQH__
