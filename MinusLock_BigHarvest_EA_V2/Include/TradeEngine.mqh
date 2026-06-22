#ifndef __BH_TRADEENGINE_MQH__
#define __BH_TRADEENGINE_MQH__

#include <Trade/Trade.mqh>

CTrade BigHarvestTrade;

ENUM_ORDER_TYPE_FILLING ResolveSymbolFillingMode(string symbol)
{
   int filling = (int)SymbolInfoInteger(symbol, SYMBOL_FILLING_MODE);
   if((filling & SYMBOL_FILLING_FOK) == SYMBOL_FILLING_FOK)
      return ORDER_FILLING_FOK;
   if((filling & SYMBOL_FILLING_IOC) == SYMBOL_FILLING_IOC)
      return ORDER_FILLING_IOC;
   return ORDER_FILLING_RETURN;
}

bool PrepareTradeEngine()
{
   BigHarvestTrade.SetExpertMagicNumber(MagicNumber);
   BigHarvestTrade.SetDeviationInPoints(MaxSlippagePoints);
   BigHarvestTrade.SetTypeFillingBySymbol(_Symbol);

   if(!UseMarketOrders)
   {
      LogError("UseMarketOrders=false is not supported in this implementation; market orders are required by the specification");
      return false;
   }

   return true;
}

bool OpenPosition(Direction dir, double lot, string comment)
{
   if(lot <= 0.0)
   {
      LogError(StringFormat("OpenPosition rejected: comment=%s lot=%.2f", comment, lot));
      return false;
   }

   if(!PrepareTradeEngine())
      return false;

   ResetLastError();

   if(IsInternalSimulationMode())
   {
      if(dir == DIR_BUY)
         Print("SIM OPEN BUY");
      if(dir == DIR_SELL)
         Print("SIM OPEN SELL");
      bool simOpened = SimOpenPosition(dir, lot, comment);
      if(!simOpened)
         Print("TRADE ERROR=", GetLastError());
      return simOpened;
   }

   bool opened = false;
   if(dir == DIR_BUY)
   {
      Print("TRADE OPEN BUY");
      opened = BigHarvestTrade.Buy(lot, _Symbol, 0.0, 0.0, 0.0, comment);
   }
   else if(dir == DIR_SELL)
   {
      Print("TRADE OPEN SELL");
      opened = BigHarvestTrade.Sell(lot, _Symbol, 0.0, 0.0, 0.0, comment);
   }

   PrintFormat("TRADE_RESULT operation=OPEN symbol=%s magic=%I64u comment=%s lot=%.2f direction=%s expectedPrice=%.5f spread=%.1f state=%s retcode=%u retcodeDescription=%s order=%I64u deal=%I64u volume=%.2f actualPrice=%.5f lastError=%d",
      _Symbol, MagicNumber, comment, lot, DirectionToString(dir), EntryPriceForDirection(dir),
      (SymbolInfoDouble(_Symbol, SYMBOL_ASK) - SymbolInfoDouble(_Symbol, SYMBOL_BID)) / SymbolInfoDouble(_Symbol, SYMBOL_POINT),
      StateToString(State), BigHarvestTrade.ResultRetcode(), BigHarvestTrade.ResultRetcodeDescription(),
      BigHarvestTrade.ResultOrder(), BigHarvestTrade.ResultDeal(), BigHarvestTrade.ResultVolume(), BigHarvestTrade.ResultPrice(), GetLastError());

   if(!opened)
      Print("TRADE ERROR=", GetLastError());

   return opened;
}

bool ClosePositionByTicket(ulong ticket, double lot)
{
   if(!PrepareTradeEngine())
      return false;

   if(IsInternalSimulationMode())
      return SimClosePositionByTicket(ticket, lot);

   if(ticket == 0 || lot <= 0.0)
   {
      LogError(StringFormat("ClosePositionByTicket rejected: ticket=%I64u lot=%.2f", ticket, lot));
      return false;
   }

   if(!PositionSelectByTicket(ticket))
   {
      LogError(StringFormat("Position not found for close: ticket=%I64u", ticket));
      return false;
   }

   double currentLot = PositionGetDouble(POSITION_VOLUME);
   double closeLot = NormalizeLotDown(lot);

   if(closeLot <= 0.0)
      return false;

   bool closed = false;
   if(closeLot >= currentLot)
      closed = BigHarvestTrade.PositionClose(ticket);
   else
      closed = BigHarvestTrade.PositionClosePartial(ticket, closeLot);

   PrintFormat("TRADE_RESULT operation=CLOSE symbol=%s magic=%I64u ticket=%I64u lot=%.2f state=%s retcode=%u retcodeDescription=%s order=%I64u deal=%I64u volume=%.2f actualPrice=%.5f lastError=%d",
      _Symbol, MagicNumber, ticket, closeLot, StateToString(State), BigHarvestTrade.ResultRetcode(),
      BigHarvestTrade.ResultRetcodeDescription(), BigHarvestTrade.ResultOrder(), BigHarvestTrade.ResultDeal(),
      BigHarvestTrade.ResultVolume(), BigHarvestTrade.ResultPrice(), GetLastError());

   return closed;
}

bool ClosePositionByTicketWithComment(ulong ticket, double lot, string closeComment)
{
   if(!PrepareTradeEngine())
      return false;

   if(IsInternalSimulationMode())
   {
      Print("SIM CLOSE ", closeComment);
      return SimClosePositionByTicket(ticket, lot);
   }

   if(ticket == 0 || lot <= 0.0)
   {
      LogError(StringFormat("ClosePositionByTicketWithComment rejected: ticket=%I64u lot=%.2f comment=%s", ticket, lot, closeComment));
      return false;
   }

   if(!PositionSelectByTicket(ticket))
   {
      LogError(StringFormat("Position not found for close with comment: ticket=%I64u comment=%s", ticket, closeComment));
      return false;
   }

   string symbol = PositionGetString(POSITION_SYMBOL);
   long positionType = PositionGetInteger(POSITION_TYPE);
   double currentLot = PositionGetDouble(POSITION_VOLUME);
   double closeLot = NormalizeLotDown(lot);

   if(closeLot <= 0.0)
      return false;
   if(closeLot > currentLot)
      closeLot = currentLot;

   MqlTradeRequest request;
   MqlTradeResult result;
   ZeroMemory(request);
   ZeroMemory(result);

   request.action = TRADE_ACTION_DEAL;
   request.position = ticket;
   request.symbol = symbol;
   request.magic = MagicNumber;
   request.volume = closeLot;
   request.deviation = MaxSlippagePoints;
   request.type_filling = ResolveSymbolFillingMode(symbol);
   request.comment = closeComment;

   if(positionType == POSITION_TYPE_BUY)
   {
      request.type = ORDER_TYPE_SELL;
      request.price = SymbolInfoDouble(symbol, SYMBOL_BID);
   }
   else if(positionType == POSITION_TYPE_SELL)
   {
      request.type = ORDER_TYPE_BUY;
      request.price = SymbolInfoDouble(symbol, SYMBOL_ASK);
   }
   else
   {
      LogError(StringFormat("Unsupported position type for close: ticket=%I64u", ticket));
      return false;
   }

   ResetLastError();
   bool sent = OrderSend(request, result);
   if(!sent || (result.retcode != TRADE_RETCODE_DONE && result.retcode != TRADE_RETCODE_DONE_PARTIAL && result.retcode != TRADE_RETCODE_PLACED))
   {
      Print("TRADE ERROR=", GetLastError());
      LogError(StringFormat("ClosePositionByTicketWithComment failed: ticket=%I64u comment=%s retcode=%u", ticket, closeComment, result.retcode));
      return false;
   }

   PrintFormat("TRADE_RESULT operation=CLOSE_WITH_COMMENT symbol=%s magic=%I64u comment=%s ticket=%I64u lot=%.2f expectedPrice=%.5f state=%s retcode=%u order=%I64u deal=%I64u volume=%.2f actualPrice=%.5f lastError=%d",
      symbol, MagicNumber, closeComment, ticket, closeLot, request.price, StateToString(State), result.retcode, result.order, result.deal, result.volume, result.price, GetLastError());
   Print("EA CLOSE COMMENT=", closeComment);
   return true;
}

#endif // __BH_TRADEENGINE_MQH__
