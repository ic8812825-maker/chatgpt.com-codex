#ifndef __BH_CONFIG_MQH__
#define __BH_CONFIG_MQH__

enum FarDistanceModeEnum
{
   FIXED_200 = 0,
   INITIAL_PLUS_CURRENT,
   INITIAL_PLUS_CUMULATIVE,
   REAL_PRICE_DISTANCE
};

input double StartLot              = 1.00;
input double BigRatio              = 1.30;
input double SmallRatio            = 0.37;
input double CloseBigOnSmall       = 0.30;
input double RemainBigOnSmall      = 0.70;
input double CloseFarShare         = 0.90;
input double ReserveShare          = 0.10;
input bool   UseRecommended5050Preset = false;

input int    InitialTriggerPoints  = 100;
input int    BigMoveLevel1         = 100;
input int    BigMoveLevel2         = 150;
input int    BigMoveLevel3         = 200;

input int    FarDistancePoints     = 200;
input FarDistanceModeEnum FarDistanceMode = REAL_PRICE_DISTANCE;
input int    MaxHarvestLevels      = 3;
input int    SmallFarTouchOffsetPoints = 0;
input int    MaxReverseCycles              = 3;
input double MinReverseStrength            = 0.10;
input double WarningReverseStrength        = 0.15;
input double StrongReverseStrength         = 0.25;
input double MinProjectedReserveCoverage   = 1.00;
input bool   StopOnInvalidReverseGeometry  = true;
input bool   StopOnReverseLimit            = true;
input bool   AllowNegativeSmallReverseNet  = false;

input double LotStep               = 0.01;
input double MaxSpreadPoints       = 30;
input double MaxMarginPercent      = 70.0;

input ulong  MagicNumber           = 20260609;
input bool   AllowRealTrading      = false;
input bool   UseMarketOrders       = true;
input bool   EnableCycleMathCsv     = true;
input bool   VerboseTickLogs       = false;

double WorkSmallRatio;
double WorkCloseBigOnSmall;
double WorkRemainBigOnSmall;
double WorkCloseFarShare;
double WorkReserveShare;
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
   WorkMaxHarvestLevels = MaxHarvestLevels;
   WorkMaxReverseCycles = MaxReverseCycles;
   WorkFarDistanceMode = FarDistanceMode;

   if(UseRecommended5050Preset)
   {
      WorkSmallRatio = 0.36;
      WorkCloseBigOnSmall = 0.35;
      WorkRemainBigOnSmall = 0.65;
      WorkCloseFarShare = 0.50;
      WorkReserveShare = 0.50;
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
         " WorkMaxHarvestLevels=", WorkMaxHarvestLevels,
         " WorkMaxReverseCycles=", WorkMaxReverseCycles,
         " WorkFarDistanceMode=", EnumToString(WorkFarDistanceMode));
}

#endif // __BH_CONFIG_MQH__
