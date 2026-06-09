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

int GetBigMovePoints(int level)
{
   if(level <= 1)
      return BigMoveLevel1;
   if(level == 2)
      return BigMoveLevel2;

   return BigMoveLevel3;
}

double CalcBigLot(double farLot)
{
   return NormalizeLotNearest(farLot * BigRatio);
}

double CalcSmallLot(double bigLot)
{
   return NormalizeLotNearest(bigLot * SmallRatio);
}

double CalcProfit(double lot, int points)
{
   return lot * points * PointValuePerLot();
}

double CalcCloseFarBudget(double netProfit)
{
   if(netProfit <= 0.0)
      return 0.0;

   return netProfit * CloseFarShare;
}

double CalcReserveAdd(double netProfit)
{
   if(netProfit <= 0.0)
      return 0.0;

   return netProfit * ReserveShare;
}

double CalcCloseFarLotRaw(double closeFarBudget, int farDistancePoints)
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

double CalcFarRemainLoss(double farRemainLot, int farDistancePoints)
{
   return farRemainLot * farDistancePoints * PointValuePerLot();
}

bool CalcFinalCloseAllowed(double totalReserve, double farRemainLot, int farDistancePoints)
{
   double farRemainLoss = CalcFarRemainLoss(farRemainLot, farDistancePoints);
   return totalReserve >= farRemainLoss;
}

double CalcCloseBigLotOnSmall(double bigLot)
{
   return NormalizeLotDown(bigLot * CloseBigOnSmall);
}

double CalcRemainBigLotOnSmall(double bigLot)
{
   return NormalizeLotDown(bigLot * RemainBigOnSmall);
}

#endif // __BH_RECOVERYMATH_MQH__
