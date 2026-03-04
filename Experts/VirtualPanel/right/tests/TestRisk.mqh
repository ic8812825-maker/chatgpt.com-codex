#ifndef __TESTRISK_MQH__
#define __TESTRISK_MQH__

#include "..\\ale\\risk\\CALRiskEngine.mqh"
#include "..\\ale\\core\\CALContext.mqh"
#include "..\\ale\\positions\\CALPositionBook.mqh"
#include "..\\ale\\exposure\\CALExposureFlow.mqh"

bool TestRisk_WorstDDMargin()
{
   CALRiskEngine risk_buy;
   CALRiskEngine risk_sell;
   risk_buy.Init(ALE_FLOW_BUY);
   risk_sell.Init(ALE_FLOW_SELL);

   // monotonicity: bigger loss => bigger DD
   const double dd_small=risk_buy.CalculateDD(-50.0,1000.0);
   const double dd_big=risk_buy.CalculateDD(-150.0,1000.0);
   if(!(dd_big>=dd_small)) return false;

   CALStreamContext ctx;
   ctx.Reset();
   ctx.pnl=-100.0;

   CALPositionBook book;
   book.Init(ALE_FLOW_BUY);
   book.Add(1.1000,0.10);

   CALExposureFlow exposure;
   exposure.Init(ALE_FLOW_BUY);
   exposure.Recalculate(book,1.1000);

   // monotonicity: bigger lots => bigger margin
   const CALRiskReport r_small=risk_buy.Evaluate(ctx,exposure,1.1,0.1,100.0,100000.0,1000.0);
   const CALRiskReport r_big=risk_buy.Evaluate(ctx,exposure,1.1,0.5,100.0,100000.0,1000.0);
   if(!(r_big.margin>=r_small.margin)) return false;

   // SAFE consistency
   if(!risk_buy.SAFE(0.30,0.25)) return false;
   if(!risk_sell.SAFE(0.30,0.25)) return false;

   return true;
}

#endif
