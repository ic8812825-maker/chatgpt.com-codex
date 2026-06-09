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
   if(!IsTradingAllowedSafe())
      return;

   RunStateMachine();
}
