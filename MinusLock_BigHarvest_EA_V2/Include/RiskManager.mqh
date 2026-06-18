#ifndef __BH_RISKMANAGER_MQH__
#define __BH_RISKMANAGER_MQH__

datetime LastRiskGateLogTime = 0;
bool LastRiskGateOk = true;

bool ShouldLogRiskGateNow()
{
   datetime now = TimeCurrent();
   if(RiskGateLogIntervalSeconds <= 0 || LastRiskGateLogTime == 0 || now - LastRiskGateLogTime >= RiskGateLogIntervalSeconds)
   {
      LastRiskGateLogTime = now;
      return true;
   }
   return false;
}

void LogRiskGateBlocked(string reason)
{
   if(ShouldLogRiskGateNow())
      LogInfo(StringFormat("RiskGate blocked: %s", reason));
}

bool SpreadOk()
{
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);

   double spreadPoints = 0.0;
   if(point > 0.0 && ask > 0.0 && bid > 0.0)
      spreadPoints = (ask - bid) / point;

   if(VerboseTickLogs)
      Print("RiskGate Spread=", spreadPoints);

   if(point <= 0.0 || ask <= 0.0 || bid <= 0.0)
   {
      Print("RISK GATE BLOCKED: invalid symbol price for spread check");
      return false;
   }

   if(spreadPoints > MaxSpreadPoints)
   {
      if(ShouldLogRiskGateNow())
      {
         Print("RISK GATE BLOCKED: spread exceeds MaxSpreadPoints");
         LogInfo(StringFormat("Spread blocked: spreadPoints=%.1f MaxSpreadPoints=%.1f", spreadPoints, MaxSpreadPoints));
      }
      return false;
   }

   return true;
}

bool MarginOk()
{
   double equity = AccountInfoDouble(ACCOUNT_EQUITY);
   double margin = AccountInfoDouble(ACCOUNT_MARGIN);
   double freeMargin = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
   double balance = AccountInfoDouble(ACCOUNT_BALANCE);
   double marginPercent = 0.0;
   double drawdownPercent = 0.0;

   if(equity > 0.0)
      marginPercent = margin / equity * 100.0;
   if(balance > 0.0 && equity < balance)
      drawdownPercent = (balance - equity) / balance * 100.0;

   if(VerboseTickLogs)
      Print("RiskGate Margin=", marginPercent, " FreeMargin=", freeMargin, " Drawdown=", drawdownPercent);

   if(equity <= 0.0)
   {
      Print("RISK GATE BLOCKED: Account equity <= 0");
      return false;
   }

   if(marginPercent > MaxMarginPercent)
   {
      Print("RISK GATE BLOCKED: margin exceeds MaxMarginPercent");
      LogInfo(StringFormat("Margin blocked: marginPercent=%.2f MaxMarginPercent=%.2f", marginPercent, MaxMarginPercent));
      return false;
   }

   if(drawdownPercent > MaxDrawdownPercent)
   {
      Print("RISK GATE BLOCKED: drawdown exceeds MaxDrawdownPercent");
      LogInfo(StringFormat("Drawdown blocked: drawdownPercent=%.2f MaxDrawdownPercent=%.2f", drawdownPercent, MaxDrawdownPercent));
      return false;
   }

   if(freeMargin <= 0.0)
   {
      Print("RISK GATE BLOCKED: free margin <= 0");
      return false;
   }

   return true;
}

bool SymbolRiskOk()
{
   if((int)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_MODE) == SYMBOL_TRADE_MODE_DISABLED)
   {
      Print("RISK GATE BLOCKED: symbol trading disabled");
      return false;
   }

   if(CountManagedOpenPositions() > MaxManagedPositions)
   {
      Print("RISK GATE BLOCKED: managed positions exceed MaxManagedPositions");
      return false;
   }

   return true;
}

bool IsTradingAllowedSafe()
{
   bool spreadOk = SpreadOk();
   bool marginOk = MarginOk();
   bool symbolOk = SymbolRiskOk();

   if(IsInternalSimulationMode())
   {
      if(!spreadOk || !marginOk || !symbolOk)
         Print("SIMULATION mode: RiskGate warning logged but simulation is not blocked");
      return true;
   }

   bool ok = spreadOk && marginOk && symbolOk;
   if(ok != LastRiskGateOk)
   {
      LogInfo(ok ? "RiskGate became OK" : "RiskGate became BLOCKED");
      LastRiskGateOk = ok;
   }

   return ok;
}

#endif // __BH_RISKMANAGER_MQH__
