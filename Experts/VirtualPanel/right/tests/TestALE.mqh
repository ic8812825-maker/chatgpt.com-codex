#ifndef __TESTALE_MQH__
#define __TESTALE_MQH__

#include "..\\ale\\core\\CALEngine.mqh"
#include "..\\ale\\math\\CALCriticalMu.mqh"

bool TestALE_DualFlowIntegration()
{
   CALEngine ale;
   ale.Init();

   // isolated books per flow
   ale.AddVirtual(ALE_FLOW_BUY,1.1000,0.10);
   ale.AddVirtual(ALE_FLOW_SELL,1.1010,0.12);

   // run full cycle for both independent engines
   ale.OnPriceUpdate(1.0700,1.0702);

   CALContext buy_ctx=ale.Context(ALE_FLOW_BUY);
   CALContext sell_ctx=ale.Context(ALE_FLOW_SELL);

   // delta consistency
   if(buy_ctx.net_delta<0.0) return false;
   if(sell_ctx.net_delta>0.0) return false;

   // context updated and FSM progressed
   if(buy_ctx.state==ALE_STATE_IDLE || sell_ctx.state==ALE_STATE_IDLE) return false;

   // SAFE trigger check under stressed move
   const bool safe_triggered=(buy_ctx.state==ALE_STATE_SAFE || sell_ctx.state==ALE_STATE_SAFE || buy_ctx.drawdown>0.25 || sell_ctx.drawdown>0.25);
   if(!safe_triggered) return false;

   // mu_crit sanity check
   CALCriticalMu mu;
   const double mu_crit=mu.Evaluate(0.2,1.0);
   if(mu_crit<=0.0) return false;

   return true;
}

#endif
