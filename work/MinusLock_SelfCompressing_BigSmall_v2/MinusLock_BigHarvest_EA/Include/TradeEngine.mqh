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

   if(!AllowRealTrading)
      return SimOpenPosition(dir, lot, comment);

   if(dir == DIR_BUY)
      return BigHarvestTrade.Buy(lot, _Symbol, 0.0, 0.0, 0.0, comment);

   if(dir == DIR_SELL)
      return BigHarvestTrade.Sell(lot, _Symbol, 0.0, 0.0, 0.0, comment);

   return false;
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

#endif // __BH_TRADEENGINE_MQH__
