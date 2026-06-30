#ifndef __BH_GEOMETRY_ENGINE_MQH__
#define __BH_GEOMETRY_ENGINE_MQH__

int RoundToStep(double value, int step)
{
   if(step <= 0)
      return (int)MathRound(value);
   return (int)(MathRound(value / step) * step);
}

int ClampInt(int value, int minValue, int maxValue)
{
   if(value < minValue) return minValue;
   if(value > maxValue) return maxValue;
   return value;
}

string GeometryModeToString(GeometryModeEnum mode)
{
   if(mode == GEOMETRY_MANUAL) return "MANUAL";
   if(mode == GEOMETRY_ATR_SAFE) return "SAFE";
   if(mode == GEOMETRY_ATR_BALANCED) return "BALANCED";
   if(mode == GEOMETRY_ATR_PROFIT) return "PROFIT";
   if(mode == GEOMETRY_ATR_CUSTOM) return "CUSTOM";
   return "UNKNOWN";
}

void ApplyGeometryPresetMultipliers(double &initialMult, double &bigStartMult, double &stepMult, double &farMult)
{
   initialMult = ATRInitialMultiplier;
   bigStartMult = ATRBigStartMultiplier;
   stepMult = ATRStepMultiplier;
   farMult = ATRFarMultiplier;

   if(GeometryMode == GEOMETRY_ATR_SAFE)
   {
      initialMult = 1.00; bigStartMult = 1.00; stepMult = 0.40; farMult = 1.30;
   }
   else if(GeometryMode == GEOMETRY_ATR_BALANCED)
   {
      initialMult = 1.00; bigStartMult = 1.15; stepMult = 0.40; farMult = 1.50;
   }
   else if(GeometryMode == GEOMETRY_ATR_PROFIT)
   {
      initialMult = 1.05; bigStartMult = 1.20; stepMult = 0.45; farMult = 1.60;
   }
}

enum GeometrySourceEnum
{
   GEOMETRY_SOURCE_MANUAL = 0,
   GEOMETRY_SOURCE_ATR = 1
};

enum GeometryFallbackReasonEnum
{
   GEOMETRY_FALLBACK_NONE = 0,
   GEOMETRY_FALLBACK_MANUAL_MODE = 1,
   GEOMETRY_FALLBACK_HISTORY_NOT_SYNCHRONIZED = 2,
   GEOMETRY_FALLBACK_NOT_ENOUGH_BARS = 3,
   GEOMETRY_FALLBACK_INVALID_HANDLE = 4,
   GEOMETRY_FALLBACK_BARS_CALCULATED = 5,
   GEOMETRY_FALLBACK_COPYBUFFER_FAILED = 6,
   GEOMETRY_FALLBACK_ATR_NAN = 7,
   GEOMETRY_FALLBACK_ATR_NON_POSITIVE = 8,
   GEOMETRY_FALLBACK_POINT_NON_POSITIVE = 9
};

string GeometrySourceToString(int source)
{
   if(source == GEOMETRY_SOURCE_ATR)
      return "ATR";
   return "MANUAL";
}

string GeometryFallbackReasonToString(int reasonCode)
{
   if(reasonCode == GEOMETRY_FALLBACK_NONE) return "NONE";
   if(reasonCode == GEOMETRY_FALLBACK_MANUAL_MODE) return "MANUAL_MODE";
   if(reasonCode == GEOMETRY_FALLBACK_HISTORY_NOT_SYNCHRONIZED) return "History not synchronized";
   if(reasonCode == GEOMETRY_FALLBACK_NOT_ENOUGH_BARS) return "Not enough bars";
   if(reasonCode == GEOMETRY_FALLBACK_INVALID_HANDLE) return "INVALID_HANDLE";
   if(reasonCode == GEOMETRY_FALLBACK_BARS_CALCULATED) return "BarsCalculated=0";
   if(reasonCode == GEOMETRY_FALLBACK_COPYBUFFER_FAILED) return "CopyBuffer failed";
   if(reasonCode == GEOMETRY_FALLBACK_ATR_NAN) return "ATR=NaN";
   if(reasonCode == GEOMETRY_FALLBACK_ATR_NON_POSITIVE) return "ATR<=0";
   if(reasonCode == GEOMETRY_FALLBACK_POINT_NON_POSITIVE) return "Point<=0";
   return "UNKNOWN";
}

void UseManualGeometryFallback(string reason, int reasonCode = GEOMETRY_FALLBACK_MANUAL_MODE)
{
   Ctx.cycleATRRaw = 0.0;
   Ctx.cycleATRPoints = 0.0;
   Ctx.workInitialTriggerPoints = InitialTriggerPoints;
   Ctx.workBigMoveStartPoints = BigMoveStartPoints;
   Ctx.workBigMoveStepPoints = BigMoveStepPoints;
   Ctx.workFarDistancePoints = FarDistancePoints;
   Ctx.geometryModeUsed = (int)GEOMETRY_MANUAL;
   Ctx.geometrySource = (int)GEOMETRY_SOURCE_MANUAL;
   Ctx.geometryFallback = (reason != "") ? 1 : 0;
   Ctx.geometryFallbackReasonCode = (reason != "") ? reasonCode : GEOMETRY_FALLBACK_NONE;
   Ctx.geometryCalculatedTime = TimeCurrent();
   if(reason != "")
   {
      Print("ATR CALCULATION FAILED reason=", reason, " fallback=MANUAL");
      Print("ADAPTIVE_GEOMETRY_ERROR reason=", reason, " fallback=MANUAL_PARAMETERS");
      Print("WARNING: Adaptive geometry failed. Manual geometry fallback used.");
   }
}

bool FailAdaptiveGeometry(string reason, int reasonCode, int atrHandle = INVALID_HANDLE)
{
   if(atrHandle != INVALID_HANDLE)
      IndicatorRelease(atrHandle);
   UseManualGeometryFallback(reason, reasonCode);
   return false;
}

bool ReadClosedBarATR(double &atrRaw, string &failureReason, int &failureReasonCode)
{
   atrRaw = 0.0;
   failureReason = "";
   failureReasonCode = GEOMETRY_FALLBACK_NONE;

   long synchronized = 0;
   if(!SeriesInfoInteger(_Symbol, ATRTimeframe, SERIES_SYNCHRONIZED, synchronized) || synchronized == 0)
   {
      failureReason = StringFormat("History not synchronized Symbol=%s Timeframe=%s", _Symbol, EnumToString(ATRTimeframe));
      failureReasonCode = GEOMETRY_FALLBACK_HISTORY_NOT_SYNCHRONIZED;
      return false;
   }

   int bars = Bars(_Symbol, ATRTimeframe);
   if(bars <= ATRPeriod + 1)
   {
      failureReason = StringFormat("Not enough bars Bars=%d ATRPeriod=%d Required>%d", bars, ATRPeriod, ATRPeriod + 1);
      failureReasonCode = GEOMETRY_FALLBACK_NOT_ENOUGH_BARS;
      return false;
   }

   int atrHandle = iATR(_Symbol, ATRTimeframe, ATRPeriod);
   if(atrHandle == INVALID_HANDLE)
   {
      failureReason = StringFormat("INVALID_HANDLE error=%d", GetLastError());
      failureReasonCode = GEOMETRY_FALLBACK_INVALID_HANDLE;
      return false;
   }

   int calculated = BarsCalculated(atrHandle);
   if(calculated <= 1)
   {
      failureReason = StringFormat("BarsCalculated=%d", calculated);
      failureReasonCode = GEOMETRY_FALLBACK_BARS_CALCULATED;
      IndicatorRelease(atrHandle);
      return false;
   }

   double atrBuffer[];
   ArraySetAsSeries(atrBuffer, true);
   ResetLastError();
   int copied = CopyBuffer(atrHandle, 0, 1, 1, atrBuffer);
   int copyError = GetLastError();
   IndicatorRelease(atrHandle);
   if(copied != 1)
   {
      failureReason = StringFormat("CopyBuffer failed copied=%d error=%d", copied, copyError);
      failureReasonCode = GEOMETRY_FALLBACK_COPYBUFFER_FAILED;
      return false;
   }

   atrRaw = atrBuffer[0];
   if(!MathIsValidNumber(atrRaw))
   {
      failureReason = "ATR=NaN";
      failureReasonCode = GEOMETRY_FALLBACK_ATR_NAN;
      return false;
   }
   if(atrRaw <= 0.0)
   {
      failureReason = StringFormat("ATR<=0 ATRRaw=%.10f", atrRaw);
      failureReasonCode = GEOMETRY_FALLBACK_ATR_NON_POSITIVE;
      return false;
   }

   return true;
}

bool CalculateAdaptiveGeometry()
{
   if(GeometryMode == GEOMETRY_MANUAL)
   {
      UseManualGeometryFallback("", GEOMETRY_FALLBACK_NONE);
      return true;
   }

   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   if(point <= 0.0)
      return FailAdaptiveGeometry("Point<=0", GEOMETRY_FALLBACK_POINT_NON_POSITIVE);

   double atrRaw = 0.0;
   string failureReason = "";
   int failureReasonCode = GEOMETRY_FALLBACK_NONE;
   if(!ReadClosedBarATR(atrRaw, failureReason, failureReasonCode))
      return FailAdaptiveGeometry(failureReason, failureReasonCode);

   double atrPoints = atrRaw / point;
   if(!MathIsValidNumber(atrPoints))
      return FailAdaptiveGeometry("ATRPoints=NaN", GEOMETRY_FALLBACK_ATR_NAN);
   if(atrPoints <= 0.0)
      return FailAdaptiveGeometry(StringFormat("ATRPoints<=0 ATRRaw=%.10f Point=%.10f", atrRaw, point), GEOMETRY_FALLBACK_ATR_NON_POSITIVE);

   double initialMult, bigStartMult, stepMult, farMult;
   ApplyGeometryPresetMultipliers(initialMult, bigStartMult, stepMult, farMult);

   double initialBeforeRound = atrPoints * initialMult;
   double bigStartBeforeRound = atrPoints * bigStartMult;
   double bigStepBeforeRound = atrPoints * stepMult;
   double farBeforeRound = atrPoints * farMult;

   int initialAfterRound = RoundToStep(initialBeforeRound, InitialRoundStep);
   int bigStartAfterRound = RoundToStep(bigStartBeforeRound, BigStartRoundStep);
   int bigStepAfterRound = RoundToStep(bigStepBeforeRound, BigStepRoundStep);
   int farAfterRound = RoundToStep(farBeforeRound, FarDistanceRoundStep);

   Ctx.cycleATRRaw = atrRaw;
   Ctx.cycleATRPoints = atrPoints;
   Ctx.workInitialTriggerPoints = ClampInt(initialAfterRound, MinInitialTriggerPoints, MaxInitialTriggerPoints);
   Ctx.workBigMoveStartPoints = ClampInt(bigStartAfterRound, MinBigMoveStartPoints, MaxBigMoveStartPoints);
   Ctx.workBigMoveStepPoints = ClampInt(bigStepAfterRound, MinBigMoveStepPoints, MaxBigMoveStepPoints);
   Ctx.workFarDistancePoints = ClampInt(farAfterRound, MinFarDistancePoints, MaxFarDistancePoints);
   Ctx.geometryModeUsed = (int)GeometryMode;
   Ctx.geometrySource = (int)GEOMETRY_SOURCE_ATR;
   Ctx.geometryFallback = 0;
   Ctx.geometryFallbackReasonCode = GEOMETRY_FALLBACK_NONE;
   Ctx.geometryCalculatedTime = TimeCurrent();

   if(PrintAdaptiveGeometryLog)
   {
      Print("========== ADAPTIVE GEOMETRY ==========");
      Print("Mode = ", GeometryModeToString((GeometryModeEnum)GeometryMode));
      Print("ATR timeframe = ", EnumToString(ATRTimeframe));
      Print("ATR period = ", ATRPeriod);
      Print("ATR raw = ", DoubleToString(atrRaw, 10));
      Print("Point = ", DoubleToString(point, 10));
      Print("Digits = ", (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS));
      Print("ATRPoints = ", DoubleToString(atrPoints, 1));
      Print("Multiplier Initial = ", DoubleToString(initialMult, 2));
      Print("Multiplier BigStart = ", DoubleToString(bigStartMult, 2));
      Print("Multiplier BigStep = ", DoubleToString(stepMult, 2));
      Print("Multiplier Far = ", DoubleToString(farMult, 2));
      Print("Initial before round = ", DoubleToString(initialBeforeRound, 2), " after round = ", initialAfterRound, " work = ", Ctx.workInitialTriggerPoints);
      Print("BigStart before round = ", DoubleToString(bigStartBeforeRound, 2), " after round = ", bigStartAfterRound, " work = ", Ctx.workBigMoveStartPoints);
      Print("BigStep before round = ", DoubleToString(bigStepBeforeRound, 2), " after round = ", bigStepAfterRound, " work = ", Ctx.workBigMoveStepPoints);
      Print("Far before round = ", DoubleToString(farBeforeRound, 2), " after round = ", farAfterRound, " work = ", Ctx.workFarDistancePoints);
      Print("Geometry READY");
      Print("=======================================");
   }

   return true;
}

bool HasCycleGeometry()
{
   return Ctx.workInitialTriggerPoints > 0 && Ctx.workBigMoveStartPoints > 0 && Ctx.workBigMoveStepPoints > 0 && Ctx.workFarDistancePoints > 0;
}

bool InitializeCycleGeometry()
{
   if(FreezeGeometryPerCycle && HasCycleGeometry() && Ctx.geometryCalculatedTime > 0)
      return true;

   if(GeometryMode == GEOMETRY_MANUAL)
   {
      UseManualGeometryFallback("");
      return true;
   }

   bool ok = CalculateAdaptiveGeometry();
   if(!ok)
      return false;
   return true;
}

int WorkInitialTriggerPoints()
{
   if(GeometryMode == GEOMETRY_MANUAL || Ctx.workInitialTriggerPoints <= 0) return InitialTriggerPoints;
   return Ctx.workInitialTriggerPoints;
}

int WorkBigMoveStartPoints()
{
   if(GeometryMode == GEOMETRY_MANUAL || Ctx.workBigMoveStartPoints <= 0) return BigMoveStartPoints;
   return Ctx.workBigMoveStartPoints;
}

int WorkBigMoveStepPoints()
{
   if(GeometryMode == GEOMETRY_MANUAL || Ctx.workBigMoveStepPoints <= 0) return BigMoveStepPoints;
   return Ctx.workBigMoveStepPoints;
}

int WorkFarDistancePoints()
{
   if(GeometryMode == GEOMETRY_MANUAL || Ctx.workFarDistancePoints <= 0) return FarDistancePoints;
   return Ctx.workFarDistancePoints;
}

void PrintGeometryDiagnostics()
{
   if(!PrintAdaptiveGeometryLog)
      return;

   double initialMult, bigStartMult, stepMult, farMult;
   ApplyGeometryPresetMultipliers(initialMult, bigStartMult, stepMult, farMult);

   if(GeometryMode == GEOMETRY_MANUAL)
   {
      Print("GEOMETRY_MODE=MANUAL Manual InitialTriggerPoints=", InitialTriggerPoints,
            " Manual BigMoveStartPoints=", BigMoveStartPoints,
            " Manual BigMoveStepPoints=", BigMoveStepPoints,
            " Manual FarDistancePoints=", FarDistancePoints,
            " GeometrySource=MANUAL Fallback=NO FallbackReason=NONE");
      return;
   }

   Print("ADAPTIVE_GEOMETRY_CALCULATED Symbol=", _Symbol,
         " Timeframe=", EnumToString(ATRTimeframe),
         " ATRPeriod=", ATRPeriod,
         " ATRRaw=", DoubleToString(Ctx.cycleATRRaw, 10),
         " ATRPoints=", DoubleToString(Ctx.cycleATRPoints, 1),
         " Mode=", GeometryModeToString((GeometryModeEnum)Ctx.geometryModeUsed),
         " GeometrySource=", GeometrySourceToString(Ctx.geometrySource),
         " Fallback=", Ctx.geometryFallback > 0 ? "YES" : "NO",
         " FallbackReason=", GeometryFallbackReasonToString(Ctx.geometryFallbackReasonCode),
         " InitialMultiplier=", DoubleToString(initialMult, 2),
         " BigStartMultiplier=", DoubleToString(bigStartMult, 2),
         " StepMultiplier=", DoubleToString(stepMult, 2),
         " FarMultiplier=", DoubleToString(farMult, 2),
         " InitialRoundStep=", InitialRoundStep,
         " BigStartRoundStep=", BigStartRoundStep,
         " BigStepRoundStep=", BigStepRoundStep,
         " FarDistanceRoundStep=", FarDistanceRoundStep,
         " WorkInitialTriggerPoints=", WorkInitialTriggerPoints(),
         " WorkBigMoveStartPoints=", WorkBigMoveStartPoints(),
         " WorkBigMoveStepPoints=", WorkBigMoveStepPoints(),
         " WorkFarDistancePoints=", WorkFarDistancePoints(),
         " FreezeGeometryPerCycle=", FreezeGeometryPerCycle ? "true" : "false");
}

void UpdateGeometryPanel()
{
   Comment("GeometryMode=", GeometryModeToString((GeometryModeEnum)(GeometryMode == GEOMETRY_MANUAL ? GEOMETRY_MANUAL : Ctx.geometryModeUsed)), "\n",
           "ATRTimeframe=", EnumToString(ATRTimeframe), "\n",
           "ATRPeriod=", ATRPeriod, "\n",
           "ATRRaw=", DoubleToString(Ctx.cycleATRRaw, 10), "\n",
           "ATRPoints=", DoubleToString(Ctx.cycleATRPoints, 1), "\n",
           "WorkInitialTriggerPoints=", WorkInitialTriggerPoints(), "\n",
           "WorkBigMoveStartPoints=", WorkBigMoveStartPoints(), "\n",
           "WorkBigMoveStepPoints=", WorkBigMoveStepPoints(), "\n",
           "WorkFarDistancePoints=", WorkFarDistancePoints(), "\n",
           "GeometrySource=", GeometrySourceToString(Ctx.geometrySource), "\n",
           "Fallback=", Ctx.geometryFallback > 0 ? "YES" : "NO", "\n",
           "Reason=", GeometryFallbackReasonToString(Ctx.geometryFallbackReasonCode), "\n",
           "InitialRoundStep=", InitialRoundStep, "\n",
           "BigStartRoundStep=", BigStartRoundStep, "\n",
           "BigStepRoundStep=", BigStepRoundStep, "\n",
           "FarDistanceRoundStep=", FarDistanceRoundStep);
}


bool CanClearCycleGeometry()
{
   return CountManagedOpenPositions() == 0
      && Ctx.farTicket == 0
      && Ctx.bigTicket == 0
      && Ctx.smallTicket == 0
      && Ctx.initialBuyTicket == 0
      && Ctx.initialSellTicket == 0
      && Ctx.pendingActionType == PENDING_NONE
      && Ctx.retryTicket == 0;
}

void ClearCycleGeometry()
{
   if(!CanClearCycleGeometry())
   {
      Print("CLEAR_CYCLE_GEOMETRY_SKIPPED reason=ACTIVE_CONTEXT_OR_POSITIONS");
      return;
   }

   Ctx.cycleATRRaw = 0.0;
   Ctx.cycleATRPoints = 0.0;
   Ctx.geometrySource = (int)GEOMETRY_SOURCE_MANUAL;
   Ctx.geometryFallback = 0;
   Ctx.geometryFallbackReasonCode = GEOMETRY_FALLBACK_NONE;
   Ctx.workInitialTriggerPoints = 0;
   Ctx.workBigMoveStartPoints = 0;
   Ctx.workBigMoveStepPoints = 0;
   Ctx.workFarDistancePoints = 0;
   Ctx.geometryModeUsed = (int)GEOMETRY_MANUAL;
   Ctx.geometryCalculatedTime = 0;
   Print("CLEAR_CYCLE_GEOMETRY_DONE");
}

#endif // __BH_GEOMETRY_ENGINE_MQH__
