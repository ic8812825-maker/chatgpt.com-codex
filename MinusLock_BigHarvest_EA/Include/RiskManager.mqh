#ifndef __BH_RISKMANAGER_MQH__
#define __BH_RISKMANAGER_MQH__

double CurrentSpreadPoints()
{
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   if(point > 0.0 && ask > 0.0 && bid > 0.0)
      return (ask - bid) / point;
   return 0.0;
}

double CurrentMarginPercent()
{
   double equity = AccountInfoDouble(ACCOUNT_EQUITY);
   double margin = AccountInfoDouble(ACCOUNT_MARGIN);
   if(equity > 0.0)
      return margin / equity * 100.0;
   return 0.0;
}

bool SpreadOk()
{
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);

   double spreadPoints = CurrentSpreadPoints();

   Print("RiskGate Spread=", spreadPoints);

   if(point <= 0.0 || ask <= 0.0 || bid <= 0.0)
   {
      Ctx.riskGateStatus = "RISK GATE BLOCKED: invalid spread price";
      Print("RISK GATE BLOCKED: invalid symbol price for spread check");
      return false;
   }

   if(spreadPoints > MaxSpreadPoints)
   {
      Ctx.riskGateStatus = StringFormat("RISK GATE BLOCKED Spread=%.1f Max=%.1f", spreadPoints, MaxSpreadPoints);
      Print("RISK GATE BLOCKED: spread exceeds MaxSpreadPoints");
      LogInfo(StringFormat("Spread blocked: spreadPoints=%.1f MaxSpreadPoints=%.1f", spreadPoints, MaxSpreadPoints));
      return false;
   }

   Ctx.riskGateStatus = "OK";
   return true;
}

bool MarginOk()
{
   double equity = AccountInfoDouble(ACCOUNT_EQUITY);
   double margin = AccountInfoDouble(ACCOUNT_MARGIN);
   double marginPercent = CurrentMarginPercent();

   Print("RiskGate Margin=", marginPercent);

   if(equity <= 0.0)
   {
      Ctx.riskGateStatus = "RISK GATE BLOCKED: equity <= 0";
      Print("RISK GATE BLOCKED: Account equity <= 0");
      return false;
   }

   if(marginPercent > MaxMarginPercent)
   {
      Ctx.riskGateStatus = StringFormat("RISK GATE BLOCKED Margin=%.2f Max=%.2f", marginPercent, MaxMarginPercent);
      Print("RISK GATE BLOCKED: margin exceeds MaxMarginPercent");
      LogInfo(StringFormat("Margin blocked: marginPercent=%.2f MaxMarginPercent=%.2f", marginPercent, MaxMarginPercent));
      return false;
   }

   return true;
}

bool IsTradingAllowedSafe()
{
   bool spreadOk = SpreadOk();
   bool marginOk = MarginOk();

   if(!AllowRealTrading)
   {
      if(!spreadOk || !marginOk)
         Print("SIMULATION mode: RiskGate warning logged but initial simulation start is not blocked");
      return true;
   }

   if(!spreadOk || !marginOk)
      return false;

   return true;
}

#endif // __BH_RISKMANAGER_MQH__
