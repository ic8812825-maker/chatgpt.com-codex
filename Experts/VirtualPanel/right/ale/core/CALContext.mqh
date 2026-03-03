#ifndef __CALCONTEXT_MQH__
#define __CALCONTEXT_MQH__

enum ENUM_ALE_STATE
{
   ALE_STATE_IDLE=0,
   ALE_STATE_BASE=1,
   ALE_STATE_EXPANSION=2,
   ALE_STATE_HARVEST=3,
   ALE_STATE_RESET=4,
   ALE_STATE_SAFE=5
};

struct CALContext
{
   ENUM_ALE_STATE state_buy;
   ENUM_ALE_STATE state_sell;
   double net_delta_buy;
   double net_delta_sell;
   double pnl_buy;
   double pnl_sell;
   double exposure_buy;
   double exposure_sell;
   double worst_dd_buy;
   double worst_dd_sell;
   double margin_buy;
   double margin_sell;

   void Reset()
   {
      state_buy=ALE_STATE_IDLE;
      state_sell=ALE_STATE_IDLE;
      net_delta_buy=0.0; net_delta_sell=0.0;
      pnl_buy=0.0; pnl_sell=0.0;
      exposure_buy=0.0; exposure_sell=0.0;
      worst_dd_buy=0.0; worst_dd_sell=0.0;
      margin_buy=0.0; margin_sell=0.0;
   }
};

#endif
