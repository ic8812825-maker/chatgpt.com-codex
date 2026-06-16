#ifndef __BH_TRADEENGINE_MQH__
#define __BH_TRADEENGINE_MQH__

#include <Trade/Trade.mqh>

CTrade BigHarvestTrade;

bool PrepareTradeEngine()
{
   BigHarvestTrade.SetExpertMagicNumber(MagicNumber);

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

   if(!AllowRealTrading)
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

   if(!opened)
      Print("TRADE ERROR=", GetLastError());

   return opened;
}

bool ClosePositionByTicket(ulong ticket, double lot)
{
   if(!PrepareTradeEngine())
      return false;

   if(!AllowRealTrading)
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

   if(closeLot >= currentLot)
      return BigHarvestTrade.PositionClose(ticket);

   return BigHarvestTrade.PositionClosePartial(ticket, closeLot);
}

bool ClosePositionByTicketWithComment(ulong ticket, double lot, string closeComment)
{
   if(!PrepareTradeEngine())
      return false;

   if(!AllowRealTrading)
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
   request.deviation = 30;
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

   Print("EA CLOSE COMMENT=", closeComment);
   return true;
}

#endif // __BH_TRADEENGINE_MQH__
