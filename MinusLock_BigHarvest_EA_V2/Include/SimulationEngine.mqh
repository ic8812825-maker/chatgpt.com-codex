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

bool SimRecordDeal(ulong positionTicket,ulong positionIdentifier,ENUM_DEAL_ENTRY entry,Direction direction,double requestedLot,double filledLot,double positionOpenPrice,double executionPrice,double profitMoney,double commissionMoney,double swapMoney,double feeMoney,double slippageMoney,string comment,ulong &createdDealTicket)
{
   createdDealTicket=0;
   string reason="";
   if(positionTicket==0) reason="SIM_DEAL_INVALID_POSITION_TICKET";
   else if(positionIdentifier==0) reason="SIM_DEAL_INVALID_IDENTIFIER";
   else if(direction==DIR_NONE) reason="SIM_DEAL_INVALID_DIRECTION";
   else if(requestedLot<=0) reason="SIM_DEAL_INVALID_REQUESTED_LOT";
   else if(filledLot<=0) reason="SIM_DEAL_INVALID_FILLED_LOT";
   else if(filledLot>requestedLot+VolumeMismatchToleranceLots) reason="SIM_DEAL_OVERFILL";
   else if(executionPrice<=0) reason="SIM_DEAL_INVALID_PRICE";
   else if(entry!=DEAL_ENTRY_IN&&entry!=DEAL_ENTRY_OUT&&entry!=DEAL_ENTRY_INOUT&&entry!=DEAL_ENTRY_OUT_BY) reason="SIM_DEAL_INVALID_ENTRY";
   if(reason!=""){Print("[BigHarvest][SIMULATION] "+reason);return false;}
   int oldSize=ArraySize(SimDeals); if(ArrayResize(SimDeals,oldSize+1)!=oldSize+1){Print("[BigHarvest][SIMULATION] SIM_DEAL_ARRAY_RESIZE_FAILED");return false;}
   SimDealSnapshot deal; ZeroMemory(deal); ulong candidate=SimNextDealTicket;
   deal.dealTicket=candidate; deal.positionTicket=positionTicket; deal.positionIdentifier=positionIdentifier; deal.entry=entry; deal.dealTime=TestMarketEventActive&&ActiveTestMarketEvent.time>0?ActiveTestMarketEvent.time:TimeCurrent(); deal.direction=direction; deal.requestedLot=requestedLot; deal.filledLot=filledLot; deal.positionOpenPrice=positionOpenPrice; deal.executionPrice=executionPrice; deal.profitMoney=profitMoney; deal.commissionMoney=commissionMoney; deal.swapMoney=swapMoney; deal.feeMoney=feeMoney; deal.slippageMoney=slippageMoney; deal.netMoney=profitMoney+commissionMoney+swapMoney+feeMoney+slippageMoney; deal.comment=comment;
   SimDeals[oldSize]=deal; SimNextDealTicket++; createdDealTicket=candidate; SimRealizedPL+=deal.netMoney; if(deal.netMoney>=0)SimClosedProfit+=deal.netMoney;else SimClosedLoss+=deal.netMoney; return true;
}

bool SimValidatePositionCandidate(const PositionSnapshot &position,string &reason)
{
 reason="";
 if(!position.exists){reason="SIM_POSITION_NOT_EXISTS";return false;} if(position.ticket==0){reason="SIM_POSITION_INVALID_TICKET";return false;} if(position.identifier==0){reason="SIM_POSITION_INVALID_IDENTIFIER";return false;} if(position.direction==DIR_NONE){reason="SIM_POSITION_INVALID_DIRECTION";return false;} if(position.initialLot<=0){reason="SIM_POSITION_INVALID_INITIAL_LOT";return false;} if(position.remainingLot<=0){reason="SIM_POSITION_INVALID_REMAINING_LOT";return false;} if(position.remainingLot>position.initialLot+VolumeMismatchToleranceLots){reason="SIM_POSITION_REMAINING_EXCEEDS_INITIAL";return false;} if(MathAbs(position.lot-position.remainingLot)>VolumeMismatchToleranceLots){reason="SIM_POSITION_LOT_ALIAS_MISMATCH";return false;} if(position.openPrice<=0){reason="SIM_POSITION_INVALID_OPEN_PRICE";return false;} if(position.openTime<=0){reason="SIM_POSITION_INVALID_OPEN_TIME";return false;} return true;
}
bool SimValidatePositionSnapshot(const PositionSnapshot &position,string &reason)
{
 if(!SimValidatePositionCandidate(position,reason))return false; if(position.entryDealTicket==0){reason="SIM_POSITION_ENTRY_DEAL_MISSING";return false;} return true;
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

bool SimOpenPosition(Direction dir,double lot,string comment)
{
 if(TestMarketEventActive&&ActiveTestMarketEvent.rejectOpen)return false; if(dir==DIR_NONE||lot<=0)return false;
 ulong candidatePositionTicket=SimNextPositionTicket; PositionSnapshot candidate; ZeroMemory(candidate); candidate.exists=true; candidate.ticket=candidatePositionTicket; candidate.identifier=candidatePositionTicket; candidate.direction=dir; candidate.initialLot=lot; candidate.remainingLot=lot; candidate.lot=lot; candidate.openPrice=SimEntryPrice(dir); candidate.openTime=TestMarketEventActive&&ActiveTestMarketEvent.time>0?ActiveTestMarketEvent.time:TimeCurrent(); candidate.comment=comment;
 string reason=""; if(!SimValidatePositionCandidate(candidate,reason)){Print("SIM_OPEN_CANDIDATE_INVALID "+reason);return false;} ulong entryDealTicket=0; if(!SimRecordDeal(candidate.ticket,candidate.identifier,DEAL_ENTRY_IN,dir,lot,lot,candidate.openPrice,candidate.openPrice,0,0,0,0,0,comment,entryDealTicket))return false; candidate.entryDealTicket=entryDealTicket; if(!SimValidatePositionSnapshot(candidate,reason))return false;
 int oldCount=ArraySize(SimPositions); if(ArrayResize(SimPositions,oldCount+1)!=oldCount+1){Print("SIM_POSITION_ARRAY_RESIZE_FAILED");return false;} SimPositions[oldCount]=candidate; if(!SimValidatePositionSnapshot(SimPositions[oldCount],reason)){ArrayResize(SimPositions,oldCount);return false;} SimNextPositionTicket++; return true;
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

   ulong exitDeal=0; if(!SimRecordDeal(ticket,SimPositions[index].identifier,DEAL_ENTRY_OUT,SimPositions[index].direction,lot,closeLot,SimPositions[index].openPrice,closePrice,realizedPL,TestMarketEventActive?ActiveTestMarketEvent.closeCommissionMoney:0,TestMarketEventActive?ActiveTestMarketEvent.swapMoney:0,TestMarketEventActive?ActiveTestMarketEvent.feeMoney:0,0,SimPositions[index].comment,exitDeal)) return false;

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
