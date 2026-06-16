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
   if(BigMoveStartPoints <= 0)
   {
      Print("ERROR: BigMoveStartPoints must be > 0");
      return INIT_PARAMETERS_INCORRECT;
   }

   if(BigMoveStepPoints <= 0)
   {
      Print("ERROR: BigMoveStepPoints must be > 0");
      return INIT_PARAMETERS_INCORRECT;
   }

   if(MaxHarvestLevels <= 0)
   {
      Print("ERROR: MaxHarvestLevels must be > 0");
      return INIT_PARAMETERS_INCORRECT;
   }

   int lastLevelPoints = BigMoveStartPoints + (MaxHarvestLevels - 1) * BigMoveStepPoints;
   if(lastLevelPoints <= 0)
   {
      Print("ERROR: Invalid BigMove levels calculation");
      return INIT_PARAMETERS_INCORRECT;
   }

   Print("BIG_MOVE_LEVELS:");
   for(int level = 1; level <= MaxHarvestLevels; level++)
      Print("L", level, " = ", GetBigMovePoints(level), " points");

   ConfigureWorkingParameters();

   if(!UseMarketOrders)
   {
      Print("INIT FAILED: UseMarketOrders=false is not supported; market orders are required");
      return INIT_PARAMETERS_INCORRECT;
   }

   if((ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE) != ACCOUNT_MARGIN_MODE_RETAIL_HEDGING)
   {
      Print("INIT FAILED: MinusLock BigHarvest requires ACCOUNT_MARGIN_MODE_RETAIL_HEDGING");
      return INIT_FAILED;
   }

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
   RecalculateRealCycleStatsFromHistory();

   int managedPositions = CountManagedOpenPositions();
   bool passByRealPL = IsRealRecoveryPass();
   double testerValue = passByRealPL ? Ctx.realRecoveryPL : -1.0;

   LogRealCycleMath(State, testerValue);

   if(!passByRealPL)
   {
      Print("TEST RESULT FAIL: cycle not closed by real recovery profit");
      Print("OpenFarLot=", Ctx.farLot);
      Print("State=", StateToString(State));
      Print("ManagedPositions=", managedPositions);
      Print("RealRecoveryPL=", Ctx.realRecoveryPL);
      Print("TheoreticalCyclePL=", Ctx.theoreticalCyclePL);
      Print("LastSystemCloseComment=", Ctx.lastSystemCloseComment);
      return -1.0;
   }

   return testerValue;
}

void OnTick()
{
   int managedPositions = CountManagedOpenPositions();
   if(VerboseTickLogs)
   {
      Print("ON TICK");
      Print("State=", StateToString(State));
      Print("ManagedPositions=", managedPositions);
   }

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
