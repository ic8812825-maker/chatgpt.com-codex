#property strict
#property version   "1.00"
#property description "MinusLock Big-Harvest EA. Works strictly from manual/big_harvest_system_manual_ru.md."

#include "Include/Config.mqh"
#include "Include/Types.mqh"
#include "Include/LotUtils.mqh"
#include "Include/SimulationEngine.mqh"
#include "Include/PositionUtils.mqh"
#include "Include/GeometryEngine.mqh"
#include "Include/Logger.mqh"
#include "Include/TradeEngine.mqh"
#include "Include/RecoveryMath.mqh"
#include "Include/RiskManager.mqh"
#include "Include/StateMachine.mqh"
#include "Include/PendingContractEngine.mqh"
#include "Include/PositionResolutionEngine.mqh"
#include "Include/StateIntegrityEngine.mqh"
#include "Include/ReconciliationEngine.mqh"

bool ValidateInputs()
{
   double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   double lotStep = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);

   if(StartLot < minLot || StartLot > maxLot)
   {
      Print("ERROR: StartLot outside SYMBOL_VOLUME_MIN/MAX");
      return false;
   }

   if(lotStep <= 0.0 || MathAbs(NormalizeLotDown(StartLot) - StartLot) > lotStep * 0.5)
   {
      Print("ERROR: StartLot does not match SYMBOL_VOLUME_STEP");
      return false;
   }

   if(InitialTriggerPoints <= 0) { Print("ERROR: InitialTriggerPoints must be > 0"); return false; }
   if(BigMoveStartPoints <= 0) { Print("ERROR: BigMoveStartPoints must be > 0"); return false; }
   if(BigMoveStepPoints <= 0) { Print("ERROR: BigMoveStepPoints must be > 0"); return false; }
   if(FarDistancePoints <= 0) { Print("ERROR: FarDistancePoints must be > 0"); return false; }
   if(MaxHarvestLevels <= 0) { Print("ERROR: MaxHarvestLevels must be > 0"); return false; }
   if(CloseFarShare < 0.0 || ReserveShare < 0.0 || MathAbs((CloseFarShare + ReserveShare) - 1.0) > 0.000001)
   {
      Print("ERROR: ReserveShare + CloseFarShare must be exactly 1.0");
      return false;
   }
   if(MaxReverseCycles <= 0) { Print("ERROR: MaxReverseCycles must be > 0"); return false; }
   if(MaxSpreadPoints <= 0.0) { Print("ERROR: MaxSpreadPoints must be > 0"); return false; }
   if(MaxMarginPercent <= 0.0) { Print("ERROR: MaxMarginPercent must be > 0"); return false; }
   if(MaxAccountMarginPercent <= 0.0) { Print("ERROR: MaxAccountMarginPercent must be > 0"); return false; }
   if(MaxActiveSymbols <= 0) { Print("ERROR: MaxActiveSymbols must be > 0"); return false; }
   if(MaxCloseRetryAttempts <= 0) { Print("ERROR: MaxCloseRetryAttempts must be > 0"); return false; }
   if(RetryLogIntervalSeconds <= 0) { Print("ERROR: RetryLogIntervalSeconds must be > 0"); return false; }
   if(RiskGateLogIntervalSeconds <= 0) { Print("ERROR: RiskGateLogIntervalSeconds must be > 0"); return false; }
   if(TerminalStateLogIntervalSeconds <= 0) { Print("ERROR: TerminalStateLogIntervalSeconds must be > 0"); return false; }
   if(VolumeMismatchToleranceLots <= 0.0) { Print("ERROR: VolumeMismatchToleranceLots must be > 0"); return false; }
   if(ATRPeriod <= 0) { Print("ERROR: ATRPeriod must be > 0"); return false; }
   if(GeometryRoundStep <= 0) { Print("ERROR: GeometryRoundStep must be > 0"); return false; }
   if(InitialRoundStep < 1) { Print("ERROR: InitialRoundStep must be >= 1"); return false; }
   if(BigStartRoundStep < 1) { Print("ERROR: BigStartRoundStep must be >= 1"); return false; }
   if(BigStepRoundStep < 1) { Print("ERROR: BigStepRoundStep must be >= 1"); return false; }
   if(FarDistanceRoundStep < 1) { Print("ERROR: FarDistanceRoundStep must be >= 1"); return false; }
   if(MinInitialTriggerPoints <= 0 || MaxInitialTriggerPoints < MinInitialTriggerPoints) { Print("ERROR: invalid InitialTrigger adaptive bounds"); return false; }
   if(MinBigMoveStartPoints <= 0 || MaxBigMoveStartPoints < MinBigMoveStartPoints) { Print("ERROR: invalid BigMoveStart adaptive bounds"); return false; }
   if(MinBigMoveStepPoints <= 0 || MaxBigMoveStepPoints < MinBigMoveStepPoints) { Print("ERROR: invalid BigMoveStep adaptive bounds"); return false; }
   if(MinFarDistancePoints <= 0 || MaxFarDistancePoints < MinFarDistancePoints) { Print("ERROR: invalid FarDistance adaptive bounds"); return false; }

   int lastLevelPoints = BigMoveStartPoints + (MaxHarvestLevels - 1) * BigMoveStepPoints;
   if(lastLevelPoints <= 0) { Print("ERROR: Invalid BigMove levels calculation"); return false; }

   if(UseInternalSimulation && AllowRealTrading)
   {
      Print("ERROR: UseInternalSimulation=true cannot be mixed with AllowRealTrading=true");
      return false;
   }

   return true;
}

bool ValidateWorkingParameters()
{
   if(WorkSmallRatio <= 0.0 || WorkSmallRatio >= 1.0) { Print("ERROR: WorkSmallRatio must be > 0 and < 1"); return false; }
   if(WorkCloseBigOnSmall <= 0.0 || WorkCloseBigOnSmall >= 1.0) { Print("ERROR: WorkCloseBigOnSmall must be > 0 and < 1"); return false; }
   if(WorkRemainBigOnSmall <= 0.0 || WorkRemainBigOnSmall >= 1.0) { Print("ERROR: WorkRemainBigOnSmall must be > 0 and < 1"); return false; }
   if(MathAbs((WorkCloseBigOnSmall + WorkRemainBigOnSmall) - 1.0) > 0.000001) { Print("ERROR: WorkCloseBigOnSmall + WorkRemainBigOnSmall must equal 1.0"); return false; }
   if(WorkCloseFarShare < 0.0 || WorkReserveShare < 0.0 || MathAbs((WorkCloseFarShare + WorkReserveShare) - 1.0) > 0.000001) { Print("ERROR: WorkCloseFarShare + WorkReserveShare must equal 1.0 and both be >= 0"); return false; }
   if(WorkSmallReserveShare < 0.0 || WorkSmallReserveShare > 1.0) { Print("ERROR: WorkSmallReserveShare must be between 0 and 1"); return false; }
   if(WorkMaxHarvestLevels <= 0) { Print("ERROR: WorkMaxHarvestLevels must be > 0"); return false; }
   if(WorkMaxReverseCycles <= 0) { Print("ERROR: WorkMaxReverseCycles must be > 0"); return false; }

   string compressionReason = "OK";
   if(!ValidateRiskCompression(BigRatio, WorkRemainBigOnSmall, compressionReason))
   {
      Print("ERROR: ", compressionReason);
      return false;
   }

   Print("ValidateWorkingParameters PASS | UseRecommended5050Preset=", UseRecommended5050Preset);
   return true;
}

bool ValidateTradingEnvironment()
{
   Print("TRADING_ENVIRONMENT | TerminalTradeAllowed=", (int)TerminalInfoInteger(TERMINAL_TRADE_ALLOWED),
         " MqlTradeAllowed=", (int)MQLInfoInteger(MQL_TRADE_ALLOWED),
         " MarginMode=", (int)AccountInfoInteger(ACCOUNT_MARGIN_MODE),
         " SymbolTradeMode=", (int)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_MODE),
         " SymbolExecution=", (int)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_EXEMODE),
         " SymbolFilling=", (int)SymbolInfoInteger(_Symbol, SYMBOL_FILLING_MODE),
         " MinLot=", SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN),
         " MaxLot=", SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX),
         " LotStep=", SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP));

   if(IsInternalSimulationMode())
      return true;

   if(!TerminalInfoInteger(TERMINAL_TRADE_ALLOWED) || !MQLInfoInteger(MQL_TRADE_ALLOWED))
   {
      Print("ERROR: terminal or MQL trading is not allowed");
      return false;
   }

   if((ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE) != ACCOUNT_MARGIN_MODE_RETAIL_HEDGING)
   {
      Print("ERROR: MinusLock BigHarvest requires ACCOUNT_MARGIN_MODE_RETAIL_HEDGING");
      return false;
   }

   if((int)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_MODE) == SYMBOL_TRADE_MODE_DISABLED)
   {
      Print("ERROR: symbol trade mode is disabled");
      return false;
   }

   return true;
}

void LogBigMoveLevels()
{
   Print("BIG_MOVE_LEVELS:");
   if(IsATRGeometryMode() && !GeometryReady() && !TradingAllowedByATRManualFallback())
   {
      Print("BIG_MOVE_LEVELS_WAITING_ATR ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
            " RuntimeGeometryMode=", RuntimeGeometryModeToString(),
            " GeometrySource=", GeometrySourceForDiagnostics(),
            " Reason=", GeometryFallbackReasonToString(Ctx.geometryFallbackReasonCode));
      return;
   }
   for(int level = 1; level <= MaxHarvestLevels; level++)
      Print("L", level, " = ", GetBigMovePoints(level), " points");
}


int OnInit()
{
   ConfigureWorkingParameters();

   if(!ValidateInputs())
      return INIT_PARAMETERS_INCORRECT;

   if(!ValidateWorkingParameters())
      return INIT_PARAMETERS_INCORRECT;

   if(!ValidateFSMIntegrity())
      return INIT_FAILED;

   if(GeometryMode == GEOMETRY_MANUAL)
      UseManualGeometryFallback("");
   else
   {
      EnsureATRIndicatorOnChart();
      CalculateAdaptiveGeometry();
   }
   PrintGeometryDiagnostics();

   LogBigMoveLevels();

   if(!UseMarketOrders)
   {
      Print("INIT FAILED: UseMarketOrders=false is not supported; market orders are required");
      return INIT_PARAMETERS_INCORRECT;
   }

   if(!ValidateTradingEnvironment())
      return INIT_FAILED;

   if(!RecoverState())
   {
      ResetRecoveryContext();
      State = STATE_IDLE;
   }
   else if(!ValidateNoOrphanManagedPositions())
      return INIT_FAILED;
   else if(!ValidateStatePositionConsistency())
      return INIT_FAILED;
   else if(!ValidateCurrentStateIntegrity())
      return INIT_FAILED;
   else if(!RunReconciliation())
      return INIT_FAILED;

   Print("EA INIT START");
   Print("AllowRealTrading=", AllowRealTrading);
   Print("UseInternalSimulation=", UseInternalSimulation);
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

   ReleaseATRHandle();
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
   Ctx.riskGateOk = riskOk;

   RunPeriodicReconciliation();
   if(State == STATE_RECOVERY_MISMATCH || State == STATE_INTEGRITY_ERROR || State == STATE_POSITION_RESOLUTION_ERROR)
      return;

   UpdateGeometryPanel();

   if(State == STATE_IDLE && managedPositions == 0)
   {
      Print("EMERGENCY_START: STATE_IDLE with zero managed positions; forcing OpenInitialLock");
      OpenInitialLock();
      return;
   }

   RunStateMachine();
}
