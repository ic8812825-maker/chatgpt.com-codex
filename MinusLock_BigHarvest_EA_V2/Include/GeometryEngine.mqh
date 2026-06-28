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

void UseManualGeometryFallback(string reason)
{
   Ctx.cycleATRPoints = 0.0;
   Ctx.workInitialTriggerPoints = InitialTriggerPoints;
   Ctx.workBigMoveStartPoints = BigMoveStartPoints;
   Ctx.workBigMoveStepPoints = BigMoveStepPoints;
   Ctx.workFarDistancePoints = FarDistancePoints;
   Ctx.geometryModeUsed = (int)GEOMETRY_MANUAL;
   Ctx.geometryCalculatedTime = TimeCurrent();
   if(reason != "")
   {
      Print("ADAPTIVE_GEOMETRY_ERROR reason=", reason, " fallback=MANUAL_PARAMETERS");
      Print("WARNING: Adaptive geometry failed. Manual geometry fallback used.");
   }
}

bool CalculateAdaptiveGeometry()
{
   if(GeometryMode == GEOMETRY_MANUAL)
   {
      UseManualGeometryFallback("");
      return true;
   }

   int atrHandle = iATR(_Symbol, ATRTimeframe, ATRPeriod);
   if(atrHandle == INVALID_HANDLE)
   {
      UseManualGeometryFallback("ATR_NOT_AVAILABLE");
      return false;
   }

   double atrBuffer[];
   ArraySetAsSeries(atrBuffer, true);
   int copied = CopyBuffer(atrHandle, 0, 1, 1, atrBuffer);
   IndicatorRelease(atrHandle);
   if(copied != 1 || atrBuffer[0] <= 0.0 || _Point <= 0.0)
   {
      UseManualGeometryFallback("ATR_NOT_AVAILABLE");
      return false;
   }

   double atrPoints = atrBuffer[0] / _Point;
   double initialMult, bigStartMult, stepMult, farMult;
   ApplyGeometryPresetMultipliers(initialMult, bigStartMult, stepMult, farMult);

   Ctx.cycleATRPoints = atrPoints;
   Ctx.workInitialTriggerPoints = ClampInt(RoundToStep(atrPoints * initialMult, GeometryRoundStep), MinInitialTriggerPoints, MaxInitialTriggerPoints);
   Ctx.workBigMoveStartPoints = ClampInt(RoundToStep(atrPoints * bigStartMult, GeometryRoundStep), MinBigMoveStartPoints, MaxBigMoveStartPoints);
   Ctx.workBigMoveStepPoints = ClampInt(RoundToStep(atrPoints * stepMult, GeometryRoundStep), MinBigMoveStepPoints, MaxBigMoveStepPoints);
   Ctx.workFarDistancePoints = ClampInt(RoundToStep(atrPoints * farMult, GeometryRoundStep), MinFarDistancePoints, MaxFarDistancePoints);
   Ctx.geometryModeUsed = (int)GeometryMode;
   Ctx.geometryCalculatedTime = TimeCurrent();
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

   if(GeometryMode == GEOMETRY_MANUAL)
   {
      Print("GEOMETRY_MODE=MANUAL Manual InitialTriggerPoints=", InitialTriggerPoints,
            " Manual BigMoveStartPoints=", BigMoveStartPoints,
            " Manual BigMoveStepPoints=", BigMoveStepPoints,
            " Manual FarDistancePoints=", FarDistancePoints);
      return;
   }

   double initialMult, bigStartMult, stepMult, farMult;
   ApplyGeometryPresetMultipliers(initialMult, bigStartMult, stepMult, farMult);
   Print("ADAPTIVE_GEOMETRY_CALCULATED Symbol=", _Symbol,
         " Timeframe=", EnumToString(ATRTimeframe),
         " ATRPeriod=", ATRPeriod,
         " ATRPoints=", DoubleToString(Ctx.cycleATRPoints, 1),
         " Mode=", GeometryModeToString((GeometryModeEnum)Ctx.geometryModeUsed),
         " InitialMultiplier=", DoubleToString(initialMult, 2),
         " BigStartMultiplier=", DoubleToString(bigStartMult, 2),
         " StepMultiplier=", DoubleToString(stepMult, 2),
         " FarMultiplier=", DoubleToString(farMult, 2),
         " WorkInitialTriggerPoints=", WorkInitialTriggerPoints(),
         " WorkBigMoveStartPoints=", WorkBigMoveStartPoints(),
         " WorkBigMoveStepPoints=", WorkBigMoveStepPoints(),
         " WorkFarDistancePoints=", WorkFarDistancePoints(),
         " FreezeGeometryPerCycle=", FreezeGeometryPerCycle ? "true" : "false");
}

void UpdateGeometryPanel()
{
   Comment("GeometryMode=", GeometryModeToString((GeometryModeEnum)(GeometryMode == GEOMETRY_MANUAL ? GEOMETRY_MANUAL : Ctx.geometryModeUsed)), "\n",
           "ATRPoints=", DoubleToString(Ctx.cycleATRPoints, 1), "\n",
           "WorkInitialTriggerPoints=", WorkInitialTriggerPoints(), "\n",
           "WorkBigMoveStartPoints=", WorkBigMoveStartPoints(), "\n",
           "WorkBigMoveStepPoints=", WorkBigMoveStepPoints(), "\n",
           "WorkFarDistancePoints=", WorkFarDistancePoints());
}

#endif // __BH_GEOMETRY_ENGINE_MQH__
