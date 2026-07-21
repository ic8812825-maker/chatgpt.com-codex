#ifndef __BH_CONFIG_MQH__
#define __BH_CONFIG_MQH__

enum CommissionPercentBase
{
   COMMISSION_PERCENT_NOTIONAL = 0,
   COMMISSION_PERCENT_TURNOVER,
   COMMISSION_PERCENT_MARGIN,
   COMMISSION_PERCENT_DISABLED
};

enum FarDistanceModeEnum
{
   FIXED_200 = 0,
   INITIAL_PLUS_CURRENT,
   INITIAL_PLUS_CUMULATIVE,
   REAL_PRICE_DISTANCE
};

enum GeometryModeEnum
{
   GEOMETRY_MANUAL = 0,
   GEOMETRY_ATR_SAFE = 1,
   GEOMETRY_ATR_BALANCED = 2,
   GEOMETRY_ATR_PROFIT = 3,
   GEOMETRY_ATR_CUSTOM = 4
};

input double StartLot              = 0.10;
input double BigRatio              = 1.15;
input double SmallRatio            = 0.25;
input double CloseBigOnSmall       = 0.40;
input double RemainBigOnSmall      = 0.60;
input double CloseFarShare         = 0.10;
input double ReserveShare          = 0.90;
input double SmallReserveShare     = 0.05;
input bool   UseRecommended5050Preset = false;
input bool   UseSplitBigGeometry = false;
input bool   UseLegacySingleBigGeometry = true;
input bool   AllowCycleWithoutBigTrend = false;

input double BigCoreRatio = 1.60;
input double BigTrendRatio = 0.25;
input double SmallBaseToFarRatio = 0.60;
input double CloseBigCoreOnSmall = 0.40;
input double RemainBigCoreOnSmall = 0.60;

input bool   UseDynamicReverseSmall = false;
// Hybrid mode is opt-in: legacy Split behaviour remains unchanged until this
// independent solver has also passed terminal validation.
enum HybridGeometryMode { HYBRID_FIXED=0, HYBRID_TARGET_NEW_FAR, HYBRID_TARGET_NEW_BIG, HYBRID_MONEY_OPTIMIZED, HYBRID_DYNAMIC };
input HybridGeometryMode HybridMode = HYBRID_FIXED;
input bool UseHybridSplitBigGeometry = false;
input bool UseHybridGeometrySolver = false;
input double TargetNewFarRatio = 0.60;
input double MaximumNewBigToOldFarRatio = 0.99;
input double MinimumReserveCatchUpRatio = 1.10;
input double MinimumRecoverySlopeMoneyPerPoint = 0.01;
input bool RequireNewBigBelowOldFar = true;
input bool RejectNonMonotonicRecovery = true;
input bool RejectReserveCatchUpBelowMinimum = true;
input bool PrintHybridOptimizationDiagnostics = true;
input double MaximumTransitionLossMoney = 0.0;
input double MinimumReserveAfterTransition = 0.0;
input double ReverseDirectionBufferRatio = 0.03;
input double ReverseSmallSafetyMoney = 3.00;
input int    ReverseConfirmationRetracePoints = 50;
input int    BigTrendEmergencyExitOffsetPoints = 0;
input bool   CloseBigTrendAtBigEntryReturn = true;
input bool   BigTrendNeverBecomesFar = true;
input double MaxBigTrendReverseLossMoney = 0.0;
input int    MaxBigTrendReverseLossPoints = 0;
input double MinimumFarCompressionLots = 0.01;
input double MinimumFarCompressionRatio = 0.01;
input double MaximumNewFarRatio = 0.97;

input int    InitialTriggerPoints  = 100;
input int    BigMoveStartPoints    = 100;
input int    BigMoveStepPoints     = 50;

input int    FarDistancePoints     = 200;
input FarDistanceModeEnum FarDistanceMode = REAL_PRICE_DISTANCE;

input GeometryModeEnum GeometryMode = GEOMETRY_MANUAL;
input ENUM_TIMEFRAMES ATRTimeframe = PERIOD_M30;
input int ATRPeriod = 14;
input double ATRInitialMultiplier = 1.00;
input double ATRBigStartMultiplier = 1.00;
input double ATRStepMultiplier = 0.40;
input double ATRFarMultiplier = 1.30;
input int MinInitialTriggerPoints = 100;
input int MaxInitialTriggerPoints = 250;
input int MinBigMoveStartPoints = 100;
input int MaxBigMoveStartPoints = 260;
input int MinBigMoveStepPoints = 50;
input int MaxBigMoveStepPoints = 125;
input int MinFarDistancePoints = 200;
input int MaxFarDistancePoints = 400;
input int GeometryRoundStep = 5; // legacy fallback; deprecated for adaptive ATR formulas
input int InitialRoundStep = 10;
input int BigStartRoundStep = 10;
input int BigStepRoundStep = 5;
input int FarDistanceRoundStep = 50;
input bool FreezeGeometryPerCycle = true;
input bool PrintAdaptiveGeometryLog = true;
input bool AllowATRManualFallback = false;
input bool ShowATRIndicatorOnChart = true;
input int    MaxHarvestLevels      = 7;
input int    SmallFarTouchOffsetPoints = 0;
input int    MaxReverseCycles              = 7;
input double MinReverseStrength            = 0.10;
input double WarningReverseStrength        = 0.15;
input double StrongReverseStrength         = 0.25;
input double MinProjectedReserveCoverage   = 1.00;
input double MinimumRecoveryProfitMoney = 1.00;
input double SafetyBufferMoney = 2.00;
input double EstimatedOpenCommissionPerLot = 0.00;
input double EstimatedCloseCommissionPerLot = 0.00;
input double EstimatedSwapBufferMoney = 0.00;
input double SpreadExpansionBufferPoints = 0.00;
input double SlippageSafetyMultiplier = 1.00;
input double ExecutionSafetyBufferMoney = 0.00;
input double CommissionPerLotPerSide = 0.00;
input double CommissionPerLotRoundTurn = 0.00;
input double CommissionFixedPerDeal = 0.00;
input double CommissionPercent = 0.00;
input CommissionPercentBase CommissionPercentCalculationBase = COMMISSION_PERCENT_DISABLED;
input bool CommissionNotionalChargeOnOpen = true;
input int ExpectedHoldingDays = 1;
input int MaximumHoldingDays = 3;
input bool UseBrokerSwapProperties = true;
input double AdditionalSwapSafetyMoney = 0.00;
input double ExecutionBufferPerOrderMoney = 0.00;
input double ExecutionBufferPerPositionMoney = 0.00;
input double ExecutionBufferPerBasketMoney = 0.00;
input double ExecutionBufferPerCycleMoney = 0.00;
input double MinimumBigRecoveryImprovementMoney = 1.00;
input double MoneyCalculationTolerance = 0.01;
input double CoverageImprovementTolerance = 0.000001;
input double MinimumNetBigExposureLots = 0.01;
input double MinimumTransitionProfitMoney = 0.00;
input double MinimumSafeMarginLevel = 200.0;
input bool   StopOnInvalidReverseGeometry  = true;
input bool   StopOnReverseLimit            = true;
input bool   AllowNegativeSmallReverseNet  = false;

input double LotStep               = 0.01;
input double MaxSpreadPoints       = 40.0;
input double MaxMarginPercent      = 60.0;
input double MaxDrawdownPercent    = 25.0;
input int    MaxManagedPositions   = 8;
input double MaxAccountMarginPercent = 60.0;
input int    MaxActiveSymbols       = 10;
input bool   StopOnRiskGateBlocked = true;
input int    RiskGateLogIntervalSeconds = 60;
input int    MaxCloseRetryAttempts = 20;
input int    RetryLogIntervalSeconds = 30;
input int    MaxSlippagePoints     = 30;
input bool   CloseAllOnInvalidGeometry = true;
input bool   CloseFarOnMaxLevels = true;
input double ReserveMismatchTolerance = 0.01;
input double VolumeMismatchToleranceLots = 0.001;
input int    ReconciliationIntervalSeconds = 300;
input int    TerminalStateLogIntervalSeconds = 300;
input int    PositionResolutionLookbackSeconds = 10;

input ulong  MagicNumber           = 20260609;
input bool   AllowRealTrading      = false;
input bool   UseInternalSimulation = false;
input bool   UseMarketOrders       = true;
input bool   EnableCycleMathCsv     = true;
input bool   VerboseTickLogs       = false;

double WorkSmallRatio;
double WorkCloseBigOnSmall;
double WorkRemainBigOnSmall;
double WorkCloseFarShare;
double WorkReserveShare;
double WorkSmallReserveShare;
int    WorkMaxHarvestLevels;
int    WorkMaxReverseCycles;
FarDistanceModeEnum WorkFarDistanceMode;

void ConfigureWorkingParameters()
{
   WorkSmallRatio = SmallRatio;
   WorkCloseBigOnSmall = CloseBigOnSmall;
   WorkRemainBigOnSmall = RemainBigOnSmall;
   WorkCloseFarShare = CloseFarShare;
   WorkReserveShare = ReserveShare;
   WorkSmallReserveShare = SmallReserveShare;
   WorkMaxHarvestLevels = MaxHarvestLevels;
   WorkMaxReverseCycles = MaxReverseCycles;
   WorkFarDistanceMode = FarDistanceMode;

   if(UseRecommended5050Preset)
   {
      Print("WARNING: 5050 preset is experimental and not the approved BigHarvest system.");
      WorkSmallRatio = 0.36;
      WorkCloseBigOnSmall = 0.35;
      WorkRemainBigOnSmall = 0.65;
      WorkCloseFarShare = 0.50;
      WorkReserveShare = 0.50;
      WorkSmallReserveShare = SmallReserveShare;
      WorkMaxHarvestLevels = 5;
      WorkMaxReverseCycles = 10;
      WorkFarDistanceMode = FarDistanceMode;
   }

   Print("WORKING_PARAMETERS | UseRecommended5050Preset=", UseRecommended5050Preset,
         " WorkSmallRatio=", DoubleToString(WorkSmallRatio, 2),
         " WorkCloseBigOnSmall=", DoubleToString(WorkCloseBigOnSmall, 2),
         " WorkRemainBigOnSmall=", DoubleToString(WorkRemainBigOnSmall, 2),
         " WorkCloseFarShare=", DoubleToString(WorkCloseFarShare, 2),
         " WorkReserveShare=", DoubleToString(WorkReserveShare, 2),
         " WorkSmallReserveShare=", DoubleToString(WorkSmallReserveShare, 2),
         " WorkMaxHarvestLevels=", WorkMaxHarvestLevels,
         " WorkMaxReverseCycles=", WorkMaxReverseCycles,
         " WorkFarDistanceMode=", EnumToString(WorkFarDistanceMode));
}

bool IsInternalSimulationMode()
{
   return UseInternalSimulation || !AllowRealTrading;
}

#endif // __BH_CONFIG_MQH__
