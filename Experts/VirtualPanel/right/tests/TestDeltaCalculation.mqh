#ifndef __TESTDELTACALCULATION_MQH__
#define __TESTDELTACALCULATION_MQH__

#include "..\\ale\\positions\\CALPositionBook.mqh"

bool TestDeltaCalculation_Run()
{
   CALPositionBook buy;
   buy.Init(ALE_FLOW_BUY);
   buy.Add(1.0,0.3);
   buy.Add(1.1,0.2);

   CALPositionBook sell;
   sell.Init(ALE_FLOW_SELL);
   sell.Add(1.2,0.1);

   const double delta=buy.EffectiveDelta()+sell.EffectiveDelta();
   if(MathAbs(delta-0.4)>1e-12) return false;
   return true;
}

#endif
