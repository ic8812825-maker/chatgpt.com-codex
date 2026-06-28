#ifndef __BH_RECOVERYMATH_MQH__
#define __BH_RECOVERYMATH_MQH__

double PointValuePerLot()
{
   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   double point     = SymbolInfoDouble(_Symbol, SYMBOL_POINT);

   if(tickSize <= 0.0 || point <= 0.0)
      return 0.0;

   return tickValue * point / tickSize;
}

// Manual compatibility formula remains: BigMoveStartPoints + (level - 1) * BigMoveStepPoints.
// Runtime uses WorkBigMoveStartPoints() + (level - 1) * WorkBigMoveStepPoints().
int GetBigMovePoints(const int level)
{
   if(level <= 0)
      return 0;

   return WorkBigMoveStartPoints() + (level - 1) * WorkBigMoveStepPoints();
}

double CalcBigLot(double farLot)
{
   return NormalizeLotNearest(farLot * BigRatio);
}

double CalcSmallLot(double bigLot)
{
   return NormalizeLotUp(bigLot * WorkSmallRatio);
}

double CalcProfit(double lot, int points)
{
   return lot * points * PointValuePerLot();
}

double CalcCloseFarBudget(double netProfit)
{
   if(netProfit <= 0.0)
      return 0.0;

   return netProfit * WorkCloseFarShare;
}

double CalcReserveAdd(double netProfit)
{
   if(netProfit <= 0.0)
      return 0.0;

   return netProfit * WorkReserveShare;
}

double CalcCloseFarLotRaw(double closeFarBudget, double farDistancePoints)
{
   double lossPerLot = farDistancePoints * PointValuePerLot();

   if(lossPerLot <= 0.0)
      return 0.0;

   return closeFarBudget / lossPerLot;
}

double CalcCloseFarLotRounded(double rawLot, double farLot)
{
   double rounded = NormalizeLotDown(rawLot);

   if(rounded > farLot)
      rounded = farLot;

   return NormalizeLotDown(rounded);
}

double CalcFarRemainLoss(double farRemainLot, double farDistancePoints)
{
   return farRemainLot * farDistancePoints * PointValuePerLot();
}


double CalcSignedPositionPL(Direction dir, double lot, double openPrice, double closePrice)
{
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   double pointValue = PointValuePerLot();

   if(point <= 0.0 || pointValue <= 0.0 || lot <= 0.0 || openPrice <= 0.0 || closePrice <= 0.0)
      return 0.0;

   if(dir == DIR_BUY)
      return lot * ((closePrice - openPrice) / point) * pointValue;

   if(dir == DIR_SELL)
      return lot * ((openPrice - closePrice) / point) * pointValue;

   return 0.0;
}

double CalcMovePointsBetween(double fromPrice, double toPrice)
{
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   if(point <= 0.0 || fromPrice <= 0.0 || toPrice <= 0.0)
      return 0.0;

   return MathAbs(toPrice - fromPrice) / point;
}

string ReverseStrengthStatus(double reverseStrength)
{
   if(reverseStrength >= StrongReverseStrength)
      return "STRONG";
   if(reverseStrength >= WarningReverseStrength)
      return "OK";
   if(reverseStrength >= MinReverseStrength)
      return "WARNING";
   return "INVALID";
}

bool ValidateReverseGeometry(
   double oldFarLot,
   double newFarLot,
   double newBigLot,
   double newSmallLot,
   double &reverseStrength,
   string &reason
)
{
   reverseStrength = 0.0;
   reason = "OK";

   if(oldFarLot <= 0.0 || newFarLot <= 0.0)
   {
      reason = "OldFarLot or NewFarLot <= 0";
      return false;
   }

   if(newFarLot >= oldFarLot)
   {
      reason = "NewFarLot >= OldFarLot";
      return false;
   }

   if(newBigLot >= oldFarLot)
   {
      reason = "Risk Compression failed: NewBig >= OldFar; BigRatio^2 * RemainBigOnSmall must be < 1";
      return false;
   }

   if(newSmallLot >= newBigLot)
   {
      reason = "NewSmallLot >= NewBigLot";
      return false;
   }

   reverseStrength = (newBigLot - newFarLot) / newFarLot;
   if(reverseStrength < MinReverseStrength)
   {
      reason = "ReverseStrength below minimum";
      return false;
   }

   return true;
}

bool ValidateSmallGeometry(
   double smallPL,
   double oldFarPL,
   double closedBigPL,
   double &smallReverseNet,
   string &reason
)
{
   smallReverseNet = smallPL + oldFarPL + closedBigPL;
   reason = "OK";

   if(smallReverseNet <= 0.0)
   {
      reason = "SmallReverseNet <= 0";
      return AllowNegativeSmallReverseNet;
   }

   return true;
}

bool ValidateReverseRisk(
   double totalReserve,
   double expectedNextReserve,
   double expectedNextFarLoss,
   double &projectedReserveCoverage,
   string &reason
)
{
   reason = "OK";
   if(expectedNextFarLoss <= 0.0)
   {
      projectedReserveCoverage = 0.0;
      reason = "ExpectedNextFarLoss <= 0";
      return false;
   }

   projectedReserveCoverage = (totalReserve + expectedNextReserve) / expectedNextFarLoss;
   if(projectedReserveCoverage < MinProjectedReserveCoverage)
   {
      reason = "ProjectedReserveCoverage below minimum";
      return false;
   }

   return true;
}

double CalcExpectedNextReserve(double newBigLot, double newSmallLot, int nextLevel)
{
   double expectedNetProfit = (newBigLot - newSmallLot) * GetBigMovePoints(nextLevel) * PointValuePerLot();
   return CalcReserveAdd(expectedNetProfit);
}

string FarDistanceModeToString(FarDistanceModeEnum mode)
{
   if(mode == FIXED_200)
      return "FIXED_200";
   if(mode == INITIAL_PLUS_CURRENT)
      return "INITIAL_PLUS_CURRENT";
   if(mode == INITIAL_PLUS_CUMULATIVE)
      return "INITIAL_PLUS_CUMULATIVE";
   if(mode == REAL_PRICE_DISTANCE)
      return "REAL_PRICE_DISTANCE";
   return "UNKNOWN";
}

double CalcRealPriceFarDistancePoints(double currentClosePrice, double farOpenPrice)
{
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   if(point <= 0.0 || currentClosePrice <= 0.0 || farOpenPrice <= 0.0)
      return 0.0;
   return MathAbs(currentClosePrice - farOpenPrice) / point;
}

double CalcEffectiveFarDistancePoints(
   double initialFarDistancePoints,
   double currentBigMovePoints,
   double cumulativeBigMovePoints,
   double currentClosePrice,
   double farOpenPrice
)
{
   if(WorkFarDistanceMode == FIXED_200)
      return WorkFarDistancePoints();
   if(WorkFarDistanceMode == INITIAL_PLUS_CURRENT)
      return initialFarDistancePoints + currentBigMovePoints;
   if(WorkFarDistanceMode == INITIAL_PLUS_CUMULATIVE)
      return initialFarDistancePoints + cumulativeBigMovePoints;
   if(WorkFarDistanceMode == REAL_PRICE_DISTANCE)
      return CalcRealPriceFarDistancePoints(currentClosePrice, farOpenPrice);
   return WorkFarDistancePoints();
}

bool CalcFinalCloseAllowed(double totalReserve, double farRemainLot, double farDistancePoints)
{
   double farRemainLoss = CalcFarRemainLoss(farRemainLot, farDistancePoints);
   return totalReserve >= farRemainLoss;
}

double CalcCloseBigLotOnSmall(double bigLot)
{
   return NormalizeVolumeToStep(bigLot * WorkCloseBigOnSmall);
}

double CalcRemainBigLotOnSmall(double bigLot)
{
   return NormalizeLotDown(bigLot * WorkRemainBigOnSmall);
}


bool ValidateRiskCompression(double bigRatio, double remainBigOnSmall, string &reason)
{
   double compression = bigRatio * bigRatio * remainBigOnSmall;
   if(compression >= 1.0)
   {
      reason = StringFormat("Risk Compression Reverse invalid: BigRatio^2 * RemainBigOnSmall = %.6f >= 1. New Big after Small reverse will not be smaller than Old Far.", compression);
      return false;
   }

   reason = "OK";
   return true;
}

double CalcSmallReserveAdd(double smallScenarioRealNet)
{
   if(smallScenarioRealNet <= 0.0)
      return 0.0;
   return smallScenarioRealNet * WorkSmallReserveShare;
}

double CalcRealFarLossMoney(Direction dir, double lot, double openPrice, double closePrice)
{
   return MathAbs(CalcSignedPositionPL(dir, lot, openPrice, closePrice));
}

#endif // __BH_RECOVERYMATH_MQH__
