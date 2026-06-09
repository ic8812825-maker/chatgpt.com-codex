#ifndef __BH_RISKMANAGER_MQH__
#define __BH_RISKMANAGER_MQH__

bool SpreadOk()
{
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);

   if(point <= 0.0 || ask <= 0.0 || bid <= 0.0)
      return false;

   double spreadPoints = (ask - bid) / point;

   if(spreadPoints > MaxSpreadPoints)
   {
      LogInfo(StringFormat("Spread blocked: spreadPoints=%.1f MaxSpreadPoints=%.1f", spreadPoints, MaxSpreadPoints));
      return false;
   }

   return true;
}

bool MarginOk()
{
   double equity = AccountInfoDouble(ACCOUNT_EQUITY);
   double margin = AccountInfoDouble(ACCOUNT_MARGIN);

   if(equity <= 0.0)
      return false;

   double marginPercent = margin / equity * 100.0;

   if(marginPercent > MaxMarginPercent)
   {
      LogInfo(StringFormat("Margin blocked: marginPercent=%.2f MaxMarginPercent=%.2f", marginPercent, MaxMarginPercent));
      return false;
   }

   return true;
}

bool IsTradingAllowedSafe()
{
   if(!SpreadOk())
      return false;

   if(!MarginOk())
      return false;

   return true;
}

#endif // __BH_RISKMANAGER_MQH__
