#ifndef __TESTALE_MQH__
#define __TESTALE_MQH__

#include "..\\ale\\core\\CALEngine.mqh"
#include "..\\ale\\math\\CALCriticalMu.mqh"

bool IsFinite(const double v)
{
   return MathIsValidNumber(v) && v==v;
}

bool TestALE_DualFlowIntegration()
{
   CALEngine ale;
   ale.Init();

   ale.AddVirtual(ALE_FLOW_BUY,1.1000,0.10);
   ale.AddVirtual(ALE_FLOW_SELL,1.1010,0.12);

   // up-trend 1000 ticks
   double bid=1.1000;
   for(int i=0;i<1000;i++)
   {
      bid+=0.0001;
      ale.OnPriceUpdate(bid,bid+0.0002);
   }

   // down-trend 1000 ticks
   for(int j=0;j<1000;j++)
   {
      bid-=0.0001;
      ale.OnPriceUpdate(bid,bid+0.0002);
   }

   // oscillation
   for(int k=0;k<200;k++)
   {
      const double x=(k%2==0 ? 0.0004 : -0.0004);
      ale.OnPriceUpdate(bid+x,bid+x+0.0002);
   }

   // flash crash
   ale.OnPriceUpdate(0.9000,0.9002);

   const CALContext ctx=ale.Context();

   if(!IsFinite(ctx.buy.pnl) || !IsFinite(ctx.sell.pnl)) return false;
   if(!IsFinite(ctx.buy.exposure) || !IsFinite(ctx.sell.exposure)) return false;

   if(ale.StateBuy()==ALE_STATE_IDLE || ale.StateSell()==ALE_STATE_IDLE) return false;

   if(MathAbs((ctx.buy.exposure+ctx.sell.exposure)-ctx.NetExposureTotal())>1e-10) return false;
   if(MathAbs((ctx.buy.net_delta+ctx.sell.net_delta)-ctx.NetDeltaTotal())>1e-10) return false;

   CALCriticalMu mu;
   const double mu_crit=mu.Evaluate(0.2,1.0);
   if(mu_crit<=0.0) return false;

   return true;
}

#endif
