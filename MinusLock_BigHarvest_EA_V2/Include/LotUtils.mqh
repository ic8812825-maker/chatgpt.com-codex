#ifndef __BH_LOTUTILS_MQH__
#define __BH_LOTUTILS_MQH__

double BrokerLotStep()
{
   double brokerStep = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   if(brokerStep <= 0.0)
      return LotStep;

   return brokerStep;
}

double GetEffectiveLotStep()
{
   if(LotStep > 0.0)
      return LotStep;

   return BrokerLotStep();
}

double GetMinLot()
{
   double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   if(minLot <= 0.0)
      return GetEffectiveLotStep();

   return minLot;
}

double GetMaxLot()
{
   double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   if(maxLot <= 0.0)
      return 100.0;

   return maxLot;
}

int VolumeDigits()
{
   double step = GetEffectiveLotStep();
   int digits = 0;

   while(step < 1.0 && digits < 8)
   {
      step *= 10.0;
      digits++;
   }

   return digits;
}

double NormalizeVolumeToStep(double volume)
{
   double step = GetEffectiveLotStep();
   double minLot = GetMinLot();
   double maxLot = GetMaxLot();

   if(step <= 0.0 || volume <= 0.0)
      return 0.0;

   double result = MathRound(volume / step) * step;

   if(result < minLot)
      return 0.0;

   if(result > maxLot)
      result = maxLot;

   return NormalizeDouble(result, VolumeDigits());
}

double NormalizeLotDown(double lot)
{
   double step = GetEffectiveLotStep();
   double minLot = GetMinLot();
   double maxLot = GetMaxLot();

   if(step <= 0.0 || lot <= 0.0)
      return 0.0;

   double result = MathFloor((lot + 0.000000001) / step) * step;

   if(result < minLot)
      return 0.0;

   if(result > maxLot)
      result = maxLot;

   return NormalizeDouble(result, VolumeDigits());
}

double NormalizeLotNearest(double lot)
{
   double step = GetEffectiveLotStep();
   double minLot = GetMinLot();
   double maxLot = GetMaxLot();

   if(step <= 0.0 || lot <= 0.0)
      return 0.0;

   double result = MathRound(lot / step) * step;

   if(result < minLot)
      return 0.0;

   if(result > maxLot)
      result = maxLot;

   return NormalizeDouble(result, VolumeDigits());
}

#endif // __BH_LOTUTILS_MQH__
