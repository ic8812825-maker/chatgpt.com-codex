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
   ResetRecoveryContext();
   State = STATE_IDLE;

   Print("EA INIT START");
   Print("AllowRealTrading=", AllowRealTrading);
   Print("UseMarketOrders=", UseMarketOrders);
   Print("StartLot=", StartLot);
   Print("MagicNumber=", MagicNumber);
   Print("CurrentState=", StateToString(State));
   LogInfo("MinusLock BigHarvest EA initialized");
   LogInfo("Initial lock profit is ignored by design: InitialProfitIgnored must become true after the first plus close");
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   LogInfo(StringFormat("MinusLock BigHarvest EA stopped, reason=%d", reason));
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
