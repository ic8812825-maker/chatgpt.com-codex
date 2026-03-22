#ifndef __CALCONTEXT_MQH__
#define __CALCONTEXT_MQH__

enum ENUM_ALE_STATE
{
   ALE_STATE_IDLE=0,
   ALE_STATE_BASE=1,
   ALE_STATE_EXPANSION=2,
   ALE_STATE_HARVEST=3,
   ALE_STATE_COMPRESSION=4,
   ALE_STATE_RESET=5,
   ALE_STATE_SAFE=6
};

enum ENUM_ALE_FLOW
{
   ALE_FLOW_BUY=1,
   ALE_FLOW_SELL=-1
};

struct CALStreamContext
{
   ENUM_ALE_STATE state;
   double net_delta;
   double pnl;
   double exposure;
   double worst_dd;
   double margin;
   double gamma;
   double convexity;
   bool safe_active;

   // Lyapunov telemetry (runtime control loop)
   double lyapunov_v;
   double lyapunov_delta;
   double lyapunov_prev_v;
   int lyapunov_risk_level;   // 0=low 1=guard 2=high 3=critical
   int lyapunov_action_code;  // 0=none 1=limit_expansion 2=compress 3=safe 4=partial_close
   double lyapunov_control_strength;

   void Reset()
   {
      state=ALE_STATE_IDLE;
      net_delta=0.0;
      pnl=0.0;
      exposure=0.0;
      worst_dd=0.0;
      margin=0.0;
      gamma=0.0;
      convexity=0.0;
      safe_active=false;
      lyapunov_v=0.0;
      lyapunov_delta=0.0;
      lyapunov_prev_v=0.0;
      lyapunov_risk_level=0;
      lyapunov_action_code=0;
      lyapunov_control_strength=0.0;
   }
};

struct CALContext
{
   CALStreamContext buy;
   CALStreamContext sell;

   void Reset()
   {
      buy.Reset();
      sell.Reset();
   }

   double NetDeltaTotal() const { return buy.net_delta+sell.net_delta; }
   double NetExposureTotal() const { return buy.exposure+sell.exposure; }
   double TotalPnL() const { return buy.pnl+sell.pnl; }
};

#endif
