#property strict
#property version   "1.00"
#property description "MinusLock Big-Harvest EA. Works strictly from manual/big_harvest_system_manual_ru.md."

#include "Include/Config.mqh"
#include "Include/Types.mqh"
#include "Include/Logger.mqh"
#include "Include/LotUtils.mqh"
#include "Include/SimulationEngine.mqh"
#include "Include/PositionUtils.mqh"
#include "Include/TradeEngine.mqh"
#include "Include/RecoveryMath.mqh"
#include "Include/RiskManager.mqh"
#include "Include/StateMachine.mqh"

int OnInit()
{
   ConfigureWorkingParameters();
   ResetRecoveryContext();
   State = STATE_IDLE;

   Print("EA INIT START");
   Print("AllowRealTrading=", AllowRealTrading);
   Print("UseMarketOrders=", UseMarketOrders);
   Print("StartLot=", StartLot);
   Print("MagicNumber=", MagicNumber);
   Print("UseRecommended5050Preset=", UseRecommended5050Preset);
   Print("CurrentState=", StateToString(State));
   LogInfo("MinusLock BigHarvest EA initialized");
   LogInfo("Initial lock profit is ignored by design: InitialProfitIgnored must become true after the first plus close");
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   int managedPositions = CountManagedOpenPositions();
   if(managedPositions > 0)
   {
      Print("CRITICAL: TEST ENDED WITH OPEN POSITIONS");
      Print("OpenFarLot=", Ctx.farLot);
      Print("State=", StateToString(State));
      Print("ManagedPositions=", managedPositions);
   }

   LogInfo(StringFormat("MinusLock BigHarvest EA stopped, reason=%d", reason));
}

double OnTester()
{
   int managedPositions = CountManagedOpenPositions();
   if(managedPositions > 0 || State == STATE_STOP_MAX_LEVELS || State == STATE_UNCLOSED_CYCLE || State == STATE_ERROR || State == STATE_STOP)
   {
      Print("TEST RESULT FAIL: cycle not closed by EA");
      Print("OpenFarLot=", Ctx.farLot);
      Print("State=", StateToString(State));
      Print("ManagedPositions=", managedPositions);
      return -1.0;
   }

   if(State == STATE_CLOSED_PROFIT)
      return Ctx.cycleFinalPL;

   return -1.0;
}

void OnTick()
{
   int managedPositions = CountManagedOpenPositions();
   Print("ON TICK");
   Print("State=", StateToString(State));
   Print("ManagedPositions=", managedPositions);

   bool riskOk = IsTradingAllowedSafe();
   if(!riskOk && AllowRealTrading)
      return;

   if(State == STATE_IDLE && managedPositions == 0)
   {
      Print("EMERGENCY_START: STATE_IDLE with zero managed positions; forcing OpenInitialLock");
      OpenInitialLock();
      return;
   }

   RunStateMachine();
}
