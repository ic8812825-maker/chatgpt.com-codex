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

enum ENUM_ALE_FLOW
{
   ALE_FLOW_BUY=1,
   ALE_FLOW_SELL=-1
};

struct CALContext
{
   double net_delta;
   double pnl;
   double exposure;
   double drawdown;
   double margin;
   ENUM_ALE_STATE state;

   void Reset()
   {
      net_delta=0.0;
      pnl=0.0;
      exposure=0.0;
      drawdown=0.0;
      margin=0.0;
      state=ALE_STATE_IDLE;
   }
};

#endif
