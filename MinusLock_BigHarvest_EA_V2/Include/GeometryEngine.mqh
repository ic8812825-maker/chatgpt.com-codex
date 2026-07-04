#ifndef __BH_GEOMETRY_ENGINE_MQH__
#define __BH_GEOMETRY_ENGINE_MQH__

void SaveState();

int g_atrHandle = INVALID_HANDLE;
bool g_atrIndicatorAdded = false;
datetime g_lastATRWaitingLogTime = 0;

bool IsATRGeometryMode()
{
   return GeometryMode == GEOMETRY_ATR_SAFE || GeometryMode == GEOMETRY_ATR_BALANCED || GeometryMode == GEOMETRY_ATR_PROFIT || GeometryMode == GEOMETRY_ATR_CUSTOM;
}

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
   if(mode == GEOMETRY_MANUAL) return "GEOMETRY_MANUAL";
   if(mode == GEOMETRY_ATR_SAFE) return "GEOMETRY_ATR_SAFE";
   if(mode == GEOMETRY_ATR_BALANCED) return "GEOMETRY_ATR_BALANCED";
   if(mode == GEOMETRY_ATR_PROFIT) return "GEOMETRY_ATR_PROFIT";
   if(mode == GEOMETRY_ATR_CUSTOM) return "GEOMETRY_ATR_CUSTOM";
   return "GEOMETRY_UNKNOWN";
}

string ConfiguredGeometryModeToString()
{
   return GeometryModeToString((GeometryModeEnum)GeometryMode);
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
   GEOMETRY_SOURCE_ATR = 1,
   GEOMETRY_SOURCE_MANUAL_FALLBACK = 2,
   GEOMETRY_SOURCE_CLEARED = 3,
   GEOMETRY_SOURCE_NO_ACTIVE_CYCLE = 4
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
   if(source == GEOMETRY_SOURCE_ATR) return "ATR";
   if(source == GEOMETRY_SOURCE_MANUAL_FALLBACK) return "MANUAL_FALLBACK";
   if(source == GEOMETRY_SOURCE_CLEARED) return "CLEARED";
   if(source == GEOMETRY_SOURCE_NO_ACTIVE_CYCLE) return "NO_ACTIVE_CYCLE";
   return "MANUAL";
}

enum GeometryClearReasonEnum
{
   GEOMETRY_CLEAR_NONE = 0,
   GEOMETRY_CLEAR_RESET_CONTEXT = 1,
   GEOMETRY_CLEAR_CLOSED_PROFIT = 2,
   GEOMETRY_CLEAR_CLOSED_RECOVERY_LOSS = 3,
   GEOMETRY_CLEAR_STOP_MAX_LEVELS = 4,
   GEOMETRY_CLEAR_OPEN_INITIAL_LOCK = 5,
   GEOMETRY_CLEAR_MANUAL_RESET = 6
};

string GeometryClearReasonToString(int reasonCode)
{
   if(reasonCode == GEOMETRY_CLEAR_NONE) return "NONE";
   if(reasonCode == GEOMETRY_CLEAR_RESET_CONTEXT) return "RESET_CONTEXT";
   if(reasonCode == GEOMETRY_CLEAR_CLOSED_PROFIT) return "STATE_CLOSED_PROFIT";
   if(reasonCode == GEOMETRY_CLEAR_CLOSED_RECOVERY_LOSS) return "STATE_CLOSED_RECOVERY_LOSS";
   if(reasonCode == GEOMETRY_CLEAR_STOP_MAX_LEVELS) return "STATE_STOP_MAX_LEVELS";
   if(reasonCode == GEOMETRY_CLEAR_OPEN_INITIAL_LOCK) return "OPEN_INITIAL_LOCK";
   if(reasonCode == GEOMETRY_CLEAR_MANUAL_RESET) return "MANUAL_RESET";
   return "UNKNOWN";
}

bool GeometryActive()
{
   return Ctx.workInitialTriggerPoints > 0 && Ctx.workBigMoveStartPoints > 0 && Ctx.workBigMoveStepPoints > 0 && Ctx.workFarDistancePoints > 0;
}

string RuntimeGeometryModeToString()
{
   if(GeometryActive())
      return GeometryModeToString((GeometryModeEnum)Ctx.geometryModeUsed);
   if(Ctx.geometryCleared > 0)
      return "NO_ACTIVE_CYCLE";
   if(IsATRGeometryMode() && Ctx.geometryReady == 0 && Ctx.geometryFallback == 0)
      return "WAITING_ATR";
   if(GeometryMode == GEOMETRY_MANUAL)
      return "GEOMETRY_MANUAL";
   return "NO_ACTIVE_CYCLE";
}

string GeometrySourceForDiagnostics()
{
   if(Ctx.geometryCleared > 0 && !GeometryActive())
      return "CLEARED";
   if(Ctx.geometryFallback > 0)
      return "MANUAL_FALLBACK";
   if(IsATRGeometryMode() && Ctx.geometryReady == 0 && Ctx.geometryFallback == 0 && Ctx.geometryCleared == 0)
      return "ATR_NOT_READY";
   if(!GeometryActive() && GeometryMode != GEOMETRY_MANUAL)
      return "NO_ACTIVE_CYCLE";
   return GeometrySourceToString(Ctx.geometrySource);
}

int DisplayWorkInitialTriggerPoints() { return GeometryActive() ? Ctx.workInitialTriggerPoints : InitialTriggerPoints; }
int DisplayWorkBigMoveStartPoints() { return GeometryActive() ? Ctx.workBigMoveStartPoints : BigMoveStartPoints; }
int DisplayWorkBigMoveStepPoints() { return GeometryActive() ? Ctx.workBigMoveStepPoints : BigMoveStepPoints; }
int DisplayWorkFarDistancePoints() { return GeometryActive() ? Ctx.workFarDistancePoints : FarDistancePoints; }

bool GeometryReady()
{
   if(GeometryMode == GEOMETRY_MANUAL)
      return true;
   return IsATRGeometryMode() && GeometryActive() && Ctx.geometryReady > 0 && Ctx.geometrySource == GEOMETRY_SOURCE_ATR && Ctx.cycleATRRaw > 0.0 && Ctx.cycleATRPoints > 0.0;
}

bool TradingAllowedByATRManualFallback()
{
   return IsATRGeometryMode() && AllowATRManualFallback && Ctx.geometryFallback > 0 && GeometryActive();
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
   Ctx.geometrySource = (reason != "") ? (int)GEOMETRY_SOURCE_MANUAL_FALLBACK : (int)GEOMETRY_SOURCE_MANUAL;
   Ctx.geometryFallback = (reason != "") ? 1 : 0;
   Ctx.geometryFallbackReasonCode = (reason != "") ? reasonCode : GEOMETRY_FALLBACK_NONE;
   Ctx.geometryCleared = 0;
   Ctx.geometryClearReasonCode = GEOMETRY_CLEAR_NONE;
   Ctx.geometryReady = (reason == "" && GeometryMode == GEOMETRY_MANUAL) ? 1 : 0;
   Ctx.tradingAllowedByFallback = (reason != "" && IsATRGeometryMode() && AllowATRManualFallback) ? 1 : 0;
   Ctx.geometryCalculatedTime = TimeCurrent();
   if(reason != "")
   {
      Print("ATR CALCULATION FAILED reason=", reason, " fallback=MANUAL");
      Print("ADAPTIVE_GEOMETRY_FALLBACK ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
            " RuntimeGeometryMode=", RuntimeGeometryModeToString(),
            " GeometrySource=MANUAL_FALLBACK FallbackReason=", GeometryFallbackReasonToString(Ctx.geometryFallbackReasonCode),
            " ManualInitial=", InitialTriggerPoints,
            " ManualBigStart=", BigMoveStartPoints,
            " ManualBigStep=", BigMoveStepPoints,
            " ManualFar=", FarDistancePoints,
            " TradingAllowedByFallback=", Ctx.tradingAllowedByFallback > 0 ? "YES" : "NO");
      Print("WARNING: Adaptive geometry failed. Manual geometry fallback used.");
   }
}

bool MarkATRGeometryWaiting(string reason, int reasonCode, int bars = -1, int barsCalculated = -1, long synchronized = -1)
{
   Ctx.cycleATRRaw = 0.0;
   Ctx.cycleATRPoints = 0.0;
   Ctx.workInitialTriggerPoints = 0;
   Ctx.workBigMoveStartPoints = 0;
   Ctx.workBigMoveStepPoints = 0;
   Ctx.workFarDistancePoints = 0;
   Ctx.geometryModeUsed = (int)GeometryMode;
   Ctx.geometrySource = (int)GEOMETRY_SOURCE_NO_ACTIVE_CYCLE;
   Ctx.geometryFallback = 0;
   Ctx.geometryFallbackReasonCode = reasonCode;
   Ctx.geometryCleared = 0;
   Ctx.geometryClearReasonCode = GEOMETRY_CLEAR_NONE;
   Ctx.geometryReady = 0;
   Ctx.tradingAllowedByFallback = 0;
   datetime now = TimeCurrent();
   if(g_lastATRWaitingLogTime == 0 || now - g_lastATRWaitingLogTime >= RiskGateLogIntervalSeconds)
   {
      Print("ATR_GEOMETRY_WAITING Reason=", GeometryFallbackReasonToString(reasonCode),
            " Details=", reason,
            " Bars=", bars,
            " BarsCalculated=", barsCalculated,
            " ATRPeriod=", ATRPeriod,
            " ATRTimeframe=", EnumToString(ATRTimeframe),
            " ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
            " RuntimeGeometryMode=WAITING_ATR GeometrySource=ATR_NOT_READY TradingBlocked=YES");
      g_lastATRWaitingLogTime = now;
   }
   return false;
}

bool FailAdaptiveGeometry(string reason, int reasonCode, int bars = -1, int barsCalculated = -1, long synchronized = -1)
{
   Print("ATR_CALC_FAIL reason=", reason, " ConfiguredGeometryMode=", ConfiguredGeometryModeToString());
   if(IsATRGeometryMode() && !AllowATRManualFallback)
      return MarkATRGeometryWaiting(reason, reasonCode, bars, barsCalculated, synchronized);

   UseManualGeometryFallback(reason, reasonCode);
   return false;
}

bool EnsureATRHandle()
{
   if(!IsATRGeometryMode())
      return true;
   if(g_atrHandle != INVALID_HANDLE)
      return true;

   Print("ATR_HANDLE_CREATE_START Symbol=", _Symbol, " Timeframe=", EnumToString(ATRTimeframe), " Period=", ATRPeriod);
   ResetLastError();
   g_atrHandle = iATR(_Symbol, ATRTimeframe, ATRPeriod);
   int err = GetLastError();
   if(g_atrHandle == INVALID_HANDLE)
   {
      Print("ATR_HANDLE_CREATE_FAIL Error=", err, " Symbol=", _Symbol, " Timeframe=", EnumToString(ATRTimeframe), " Period=", ATRPeriod);
      return false;
   }

   Print("ATR_HANDLE_CREATE_OK Symbol=", _Symbol, " Timeframe=", EnumToString(ATRTimeframe), " Period=", ATRPeriod, " Handle=", g_atrHandle);
   return true;
}

void ReleaseATRHandle()
{
   if(g_atrHandle != INVALID_HANDLE)
   {
      IndicatorRelease(g_atrHandle);
      Print("ATR_HANDLE_RELEASE Handle=", g_atrHandle);
      g_atrHandle = INVALID_HANDLE;
   }
   g_atrIndicatorAdded = false;
}

bool EnsureATRIndicatorOnChart()
{
   if(!IsATRGeometryMode() || !ShowATRIndicatorOnChart)
      return true;
   if(g_atrIndicatorAdded)
      return true;
   if(!EnsureATRHandle())
      return false;

   ResetLastError();
   bool added = ChartIndicatorAdd(0, 1, g_atrHandle);
   int err = GetLastError();
   if(added)
   {
      g_atrIndicatorAdded = true;
      Print("ATR_INDICATOR_ADD_OK Symbol=", _Symbol, " Timeframe=", EnumToString(ATRTimeframe), " Period=", ATRPeriod, " Handle=", g_atrHandle);
      return true;
   }

   Print("ATR_INDICATOR_ADD_FAIL Error=", err, " Handle=", g_atrHandle, " Symbol=", _Symbol, " Timeframe=", EnumToString(ATRTimeframe));
   return false;
}

bool ReadClosedBarATR(double &atrRaw, string &failureReason, int &failureReasonCode, int &bars, int &calculated, long &synchronized)
{
   atrRaw = 0.0;
   failureReason = "";
   failureReasonCode = GEOMETRY_FALLBACK_NONE;

   synchronized = 0;
   SymbolSelect(_Symbol, true);
   if(!SeriesInfoInteger(_Symbol, ATRTimeframe, SERIES_SYNCHRONIZED, synchronized) || synchronized == 0)
   {
      failureReason = StringFormat("History not synchronized Symbol=%s Timeframe=%s", _Symbol, EnumToString(ATRTimeframe));
      failureReasonCode = GEOMETRY_FALLBACK_HISTORY_NOT_SYNCHRONIZED;
      bars = Bars(_Symbol, ATRTimeframe);
      calculated = (g_atrHandle != INVALID_HANDLE) ? BarsCalculated(g_atrHandle) : -1;
      return false;
   }

   bars = Bars(_Symbol, ATRTimeframe);
   Print("ATR_HISTORY_CHECK Symbol=", _Symbol, " Timeframe=", EnumToString(ATRTimeframe), " Period=", ATRPeriod, " Bars=", bars, " SeriesSynchronized=", synchronized > 0 ? "YES" : "NO");
   Print("ATR_CALC_START Symbol=", _Symbol, " Timeframe=", EnumToString(ATRTimeframe), " Period=", ATRPeriod, " Bars=", bars, " SeriesSynchronized=", synchronized > 0 ? "YES" : "NO");
   if(bars <= ATRPeriod + 1)
   {
      failureReason = StringFormat("Not enough bars Bars=%d ATRPeriod=%d Required>%d", bars, ATRPeriod, ATRPeriod + 1);
      failureReasonCode = GEOMETRY_FALLBACK_NOT_ENOUGH_BARS;
      calculated = (g_atrHandle != INVALID_HANDLE) ? BarsCalculated(g_atrHandle) : -1;
      return false;
   }

   if(!EnsureATRHandle())
   {
      failureReason = StringFormat("INVALID_HANDLE error=%d", GetLastError());
      failureReasonCode = GEOMETRY_FALLBACK_INVALID_HANDLE;
      calculated = -1;
      return false;
   }

   calculated = BarsCalculated(g_atrHandle);
   Print("ATR_CALC_STATUS Symbol=", _Symbol, " BarsCalculated=", calculated);
   if(calculated < ATRPeriod + 1)
   {
      failureReason = StringFormat("BarsCalculated=%d Required>=%d", calculated, ATRPeriod + 1);
      failureReasonCode = GEOMETRY_FALLBACK_BARS_CALCULATED;
      return false;
   }

   double atrBuffer[];
   ArraySetAsSeries(atrBuffer, true);
   ResetLastError();
   int copied = CopyBuffer(g_atrHandle, 0, 1, 1, atrBuffer);
   int copyError = GetLastError();
   if(copied != 1)
   {
      failureReason = StringFormat("CopyBuffer failed copied=%d error=%d", copied, copyError);
      failureReasonCode = GEOMETRY_FALLBACK_COPYBUFFER_FAILED;
      return false;
   }

   atrRaw = atrBuffer[0];
   Print("ATR_CALC_OK ATRRaw=", DoubleToString(atrRaw, 10), " Point=", DoubleToString(SymbolInfoDouble(_Symbol, SYMBOL_POINT), 10), " ATRPoints=", DoubleToString(atrRaw / MathMax(SymbolInfoDouble(_Symbol, SYMBOL_POINT), 0.0000000001), 1));
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
   int bars = -1;
   int barsCalculated = -1;
   long synchronized = -1;
   if(!ReadClosedBarATR(atrRaw, failureReason, failureReasonCode, bars, barsCalculated, synchronized))
      return FailAdaptiveGeometry(failureReason, failureReasonCode, bars, barsCalculated, synchronized);

   double atrPoints = atrRaw / point;
   if(!MathIsValidNumber(atrPoints))
      return FailAdaptiveGeometry("ATRPoints=NaN", GEOMETRY_FALLBACK_ATR_NAN, bars, barsCalculated, synchronized);
   if(atrPoints <= 0.0)
      return FailAdaptiveGeometry(StringFormat("ATRPoints<=0 ATRRaw=%.10f Point=%.10f", atrRaw, point), GEOMETRY_FALLBACK_ATR_NON_POSITIVE, bars, barsCalculated, synchronized);

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
   Ctx.geometryCleared = 0;
   Ctx.geometryClearReasonCode = GEOMETRY_CLEAR_NONE;
   Ctx.geometryReady = 1;
   Ctx.tradingAllowedByFallback = 0;
   Ctx.geometryCalculatedTime = TimeCurrent();

   if(PrintAdaptiveGeometryLog)
   {
      Print("========== ADAPTIVE GEOMETRY ==========");
      Print("ConfiguredGeometryMode = ", ConfiguredGeometryModeToString());
      Print("RuntimeGeometryMode = ", RuntimeGeometryModeToString());
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

   Print("ADAPTIVE_GEOMETRY_CALCULATED ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
         " RuntimeGeometryMode=", RuntimeGeometryModeToString(),
         " GeometrySource=ATR",
         " ATRRaw=", DoubleToString(atrRaw, 10),
         " ATRPoints=", DoubleToString(atrPoints, 1),
         " ManualInitial=", InitialTriggerPoints,
         " ManualBigStart=", BigMoveStartPoints,
         " ManualBigStep=", BigMoveStepPoints,
         " ManualFar=", FarDistancePoints,
         " CalculatedInitial=", Ctx.workInitialTriggerPoints,
         " CalculatedBigStart=", Ctx.workBigMoveStartPoints,
         " CalculatedBigStep=", Ctx.workBigMoveStepPoints,
         " CalculatedFar=", Ctx.workFarDistancePoints);
   if(Ctx.workInitialTriggerPoints == InitialTriggerPoints && Ctx.workBigMoveStartPoints == BigMoveStartPoints &&
      Ctx.workBigMoveStepPoints == BigMoveStepPoints && Ctx.workFarDistancePoints == FarDistancePoints)
      Print("ATR_VALUES_EQUAL_MANUAL Reason=rounding_or_same_ATR ConfiguredGeometryMode=", ConfiguredGeometryModeToString());

   return true;
}

bool HasCycleGeometry()
{
   return GeometryActive();
}

void ResetCycleGeometryFields(string reason)
{
   Ctx.cycleATRRaw = 0.0;
   Ctx.cycleATRPoints = 0.0;
   Ctx.geometrySource = (int)GEOMETRY_SOURCE_NO_ACTIVE_CYCLE;
   Ctx.geometryFallback = 0;
   Ctx.geometryFallbackReasonCode = GEOMETRY_FALLBACK_NONE;
   Ctx.geometryCleared = 0;
   Ctx.geometryClearReasonCode = GEOMETRY_CLEAR_NONE;
   Ctx.geometryReady = 0;
   Ctx.tradingAllowedByFallback = 0;
   Ctx.workInitialTriggerPoints = 0;
   Ctx.workBigMoveStartPoints = 0;
   Ctx.workBigMoveStepPoints = 0;
   Ctx.workFarDistancePoints = 0;
   Ctx.geometryModeUsed = (int)GEOMETRY_MANUAL;
   Ctx.geometryCalculatedTime = 0;
   if(reason != "")
      Print("RESET_CYCLE_GEOMETRY_FIELDS reason=", reason);
}

bool InitializeCycleGeometry()
{
   Print("ADAPTIVE_GEOMETRY_REQUEST ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
         " State=", StateToString(State),
         " HaveActiveCycle=", HasCycleGeometry() ? "YES" : "NO",
         " FreezeGeometryPerCycle=", FreezeGeometryPerCycle ? "true" : "false",
         " ExistingGeometryCalculated=", Ctx.geometryCalculatedTime > 0 ? "YES" : "NO");
   if(FreezeGeometryPerCycle && HasCycleGeometry() && Ctx.geometryCalculatedTime > 0)
   {
      Print("ADAPTIVE_GEOMETRY_FREEZE_KEEP ExistingGeometry=YES Mode=", GeometryModeToString((GeometryModeEnum)Ctx.geometryModeUsed),
            " ATRPoints=", DoubleToString(Ctx.cycleATRPoints, 1),
            " WorkInitialTriggerPoints=", Ctx.workInitialTriggerPoints,
            " WorkBigMoveStartPoints=", Ctx.workBigMoveStartPoints,
            " WorkBigMoveStepPoints=", Ctx.workBigMoveStepPoints,
            " WorkFarDistancePoints=", Ctx.workFarDistancePoints);
      return true;
   }

   if(GeometryMode == GEOMETRY_MANUAL)
   {
      UseManualGeometryFallback("");
      return true;
   }

   EnsureATRIndicatorOnChart();
   bool ok = CalculateAdaptiveGeometry();
   if(!ok)
      return false;
   return true;
}

bool EnsureCycleGeometry(string reason)
{
   if(HasCycleGeometry())
      return true;

   Print("ADAPTIVE_GEOMETRY_MISSING reason=", reason, " ConfiguredGeometryMode=", ConfiguredGeometryModeToString(), " RuntimeGeometryMode=", RuntimeGeometryModeToString(), " GeometrySource=", GeometrySourceForDiagnostics(), " action=InitializeCycleGeometry");
   bool ok = InitializeCycleGeometry();
   if(!ok || !HasCycleGeometry())
   {
      Print("ADAPTIVE_GEOMETRY_UNAVAILABLE reason=", reason, " fallback=", Ctx.geometryFallback > 0 ? "YES" : "NO", " fallbackReason=", GeometryFallbackReasonToString(Ctx.geometryFallbackReasonCode));
      return false;
   }
   PrintGeometryDiagnostics();
   return true;
}

int WorkInitialTriggerPoints()
{
   if(!HasCycleGeometry())
      EnsureCycleGeometry("WorkInitialTriggerPoints");
   return Ctx.workInitialTriggerPoints > 0 ? Ctx.workInitialTriggerPoints : InitialTriggerPoints;
}

int WorkBigMoveStartPoints()
{
   if(!HasCycleGeometry())
      EnsureCycleGeometry("WorkBigMoveStartPoints");
   return Ctx.workBigMoveStartPoints > 0 ? Ctx.workBigMoveStartPoints : BigMoveStartPoints;
}

int WorkBigMoveStepPoints()
{
   if(!HasCycleGeometry())
      EnsureCycleGeometry("WorkBigMoveStepPoints");
   return Ctx.workBigMoveStepPoints > 0 ? Ctx.workBigMoveStepPoints : BigMoveStepPoints;
}

int WorkFarDistancePoints()
{
   if(!HasCycleGeometry())
      EnsureCycleGeometry("WorkFarDistancePoints");
   return Ctx.workFarDistancePoints > 0 ? Ctx.workFarDistancePoints : FarDistancePoints;
}

void PrintGeometryDiagnostics()
{
   if(!PrintAdaptiveGeometryLog)
      return;

   double initialMult, bigStartMult, stepMult, farMult;
   ApplyGeometryPresetMultipliers(initialMult, bigStartMult, stepMult, farMult);

   if(GeometryMode == GEOMETRY_MANUAL)
   {
      Print("GEOMETRY_MODE=MANUAL ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
            " RuntimeGeometryMode=", RuntimeGeometryModeToString(),
            " Manual InitialTriggerPoints=", InitialTriggerPoints,
            " Manual BigMoveStartPoints=", BigMoveStartPoints,
            " Manual BigMoveStepPoints=", BigMoveStepPoints,
            " Manual FarDistancePoints=", FarDistancePoints,
            " GeometrySource=MANUAL Fallback=NO FallbackReason=NONE");
      return;
   }

   if(IsATRGeometryMode() && !GeometryReady() && !TradingAllowedByATRManualFallback())
   {
      Print("ADAPTIVE_GEOMETRY_NOT_READY Symbol=", _Symbol,
            " ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
            " RuntimeGeometryMode=", RuntimeGeometryModeToString(),
            " GeometrySource=", GeometrySourceForDiagnostics(),
            " ATRRaw=", DoubleToString(Ctx.cycleATRRaw, 10),
            " ATRPoints=", DoubleToString(Ctx.cycleATRPoints, 1),
            " FallbackReason=", GeometryFallbackReasonToString(Ctx.geometryFallbackReasonCode),
            " TradingBlocked=YES");
      return;
   }

   Print("ADAPTIVE_GEOMETRY_CALCULATED Symbol=", _Symbol,
         " ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
         " RuntimeGeometryMode=", RuntimeGeometryModeToString(),
         " Timeframe=", EnumToString(ATRTimeframe),
         " ATRPeriod=", ATRPeriod,
         " ATRRaw=", DoubleToString(Ctx.cycleATRRaw, 10),
         " ATRPoints=", DoubleToString(Ctx.cycleATRPoints, 1),
         " GeometrySource=", GeometrySourceForDiagnostics(),
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
         " WorkInitialTriggerPoints=", DisplayWorkInitialTriggerPoints(),
         " WorkBigMoveStartPoints=", DisplayWorkBigMoveStartPoints(),
         " WorkBigMoveStepPoints=", DisplayWorkBigMoveStepPoints(),
         " WorkFarDistancePoints=", DisplayWorkFarDistancePoints(),
         " FreezeGeometryPerCycle=", FreezeGeometryPerCycle ? "true" : "false");
}

void UpdateGeometryPanel()
{
   Comment("Configured: ", ConfiguredGeometryModeToString(), "\n",
           "Runtime: ", RuntimeGeometryModeToString(), "\n",
           "Source: ", GeometrySourceForDiagnostics(), "\n",
           "ATRTimeframe=", EnumToString(ATRTimeframe), "\n",
           "ATRPeriod=", ATRPeriod, "\n",
           "ATRRaw=", DoubleToString(Ctx.cycleATRRaw, 10), "\n",
           "ATRPoints=", DoubleToString(Ctx.cycleATRPoints, 1), "\n",
           "WorkInitial=", DisplayWorkInitialTriggerPoints(), "\n",
           "WorkBigStart=", DisplayWorkBigMoveStartPoints(), "\n",
           "WorkBigStep=", DisplayWorkBigMoveStepPoints(), "\n",
           "WorkFar=", DisplayWorkFarDistancePoints(), "\n",
           "GeometryActive=", GeometryActive() ? "YES" : "NO", "\n",
           "GeometryReady=", GeometryReady() ? "YES" : "NO", "\n",
           "TradingBlocked=", (IsATRGeometryMode() && !GeometryReady() && !TradingAllowedByATRManualFallback()) ? "YES" : "NO", "\n",
           "ATRIndicator=", (IsATRGeometryMode() && ShowATRIndicatorOnChart && g_atrIndicatorAdded) ? "VISIBLE" : "NOT_VISIBLE", "\n",
           "GeometryCleared=", Ctx.geometryCleared > 0 ? "YES" : "NO", "\n",
           "FallbackReason=", GeometryFallbackReasonToString(Ctx.geometryFallbackReasonCode), "\n",
           "ClearReason=", GeometryClearReasonToString(Ctx.geometryClearReasonCode), "\n",
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

void ClearCycleGeometry(bool persist = false, int clearReasonCode = GEOMETRY_CLEAR_RESET_CONTEXT)
{
   if(Ctx.geometryCleared > 0 && Ctx.geometryClearReasonCode == clearReasonCode)
      return;

   if(!CanClearCycleGeometry())
   {
      Print("CLEAR_CYCLE_GEOMETRY_SKIPPED reason=ACTIVE_CONTEXT_OR_POSITIONS ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
            " RuntimeGeometryMode=", RuntimeGeometryModeToString());
      return;
   }

   string previousRuntimeMode = RuntimeGeometryModeToString();
   double previousATRPoints = Ctx.cycleATRPoints;
   int previousWorkInitial = Ctx.workInitialTriggerPoints;
   int previousWorkBigStart = Ctx.workBigMoveStartPoints;
   int previousWorkBigStep = Ctx.workBigMoveStepPoints;
   int previousWorkFar = Ctx.workFarDistancePoints;

   ResetCycleGeometryFields("");
   Ctx.geometrySource = (int)GEOMETRY_SOURCE_CLEARED;
   Ctx.geometryCleared = 1;
   Ctx.geometryClearReasonCode = clearReasonCode;
   if(persist)
      SaveState();
   Print("CLEAR_CYCLE_GEOMETRY_DONE PreviousRuntimeGeometryMode=", previousRuntimeMode,
         " PreviousATRPoints=", DoubleToString(previousATRPoints, 1),
         " PreviousWorkInitial=", previousWorkInitial,
         " PreviousWorkBigStart=", previousWorkBigStart,
         " PreviousWorkBigStep=", previousWorkBigStep,
         " PreviousWorkFar=", previousWorkFar,
         " ClearReason=", GeometryClearReasonToString(clearReasonCode),
         " ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
         " RuntimeGeometryMode=", RuntimeGeometryModeToString(),
         " GeometrySource=", GeometrySourceForDiagnostics(),
         " persist=", persist ? "YES" : "NO");
}

bool EnsureGeometryReadyForInitialLock()
{
   if(GeometryMode == GEOMETRY_MANUAL)
      return true;

   if(GeometryReady())
   {
      Print("INITIAL_LOCK_ALLOWED_ATR_READY ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
            " RuntimeGeometryMode=", RuntimeGeometryModeToString(),
            " GeometrySource=ATR ATRRaw=", DoubleToString(Ctx.cycleATRRaw, 10),
            " ATRPoints=", DoubleToString(Ctx.cycleATRPoints, 1));
      return true;
   }

   if(!HasCycleGeometry())
      InitializeCycleGeometry();

   if(GeometryReady())
   {
      Print("INITIAL_LOCK_ALLOWED_ATR_READY ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
            " RuntimeGeometryMode=", RuntimeGeometryModeToString(),
            " GeometrySource=ATR ATRRaw=", DoubleToString(Ctx.cycleATRRaw, 10),
            " ATRPoints=", DoubleToString(Ctx.cycleATRPoints, 1));
      return true;
   }

   if(TradingAllowedByATRManualFallback())
   {
      Print("INITIAL_LOCK_ALLOWED_ATR_MANUAL_FALLBACK ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
            " RuntimeGeometryMode=", RuntimeGeometryModeToString(),
            " GeometrySource=MANUAL_FALLBACK FallbackReason=", GeometryFallbackReasonToString(Ctx.geometryFallbackReasonCode),
            " TradingAllowedByFallback=YES");
      return true;
   }

   Print("INITIAL_LOCK_BLOCKED_ATR_NOT_READY ConfiguredGeometryMode=", ConfiguredGeometryModeToString(),
         " RuntimeGeometryMode=WAITING_ATR GeometrySource=ATR_NOT_READY ATRRaw=", DoubleToString(Ctx.cycleATRRaw, 10),
         " ATRPoints=", DoubleToString(Ctx.cycleATRPoints, 1),
         " Reason=", GeometryFallbackReasonToString(Ctx.geometryFallbackReasonCode));
   return false;
}

#endif // __BH_GEOMETRY_ENGINE_MQH__
