#ifndef __TESTALE_MQH__
#define __TESTALE_MQH__

#include "..\ale\core\CALEngine.mqh"

bool TestALE_DualFlowIntegration()
{
   CALEngine ale;
   ale.Init(0);
   ale.AddVirtual(1,1.1000,0.10);
   ale.AddVirtual(-1,1.1010,0.10);
   ale.OnPriceUpdate(1.1005,1.1007);

   const CALContext &ctx=ale.Context();
   if(ctx.state_buy==ALE_STATE_IDLE || ctx.state_sell==ALE_STATE_IDLE) return false;
   if(ctx.net_delta_buy<0.0 || ctx.net_delta_sell>0.0) return false;
   return true;
}

#endif
