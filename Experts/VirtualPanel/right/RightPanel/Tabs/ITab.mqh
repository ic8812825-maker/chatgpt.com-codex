#ifndef __RIGHTPANEL_TABS_ITAB_MQH__
#define __RIGHTPANEL_TABS_ITAB_MQH__

struct SPanelSnapshot
{
   string system_status;
   double e_dv;
   double p_non_pos;
   double max_v;
   double control_strength;
   string current_action;
   int    latency_ticks;

   double predicted_dv;
   double real_dv;
   bool   argmin_match;
   int    horizon;
   double objective_value;

   double v_now;
   double dv_now;
   double cvar;
   string risk_trend;

   double buy_exposure;
   double sell_exposure;
   double asymmetry;
   double cross_impact;
   double total_v;

   int    delay;
   double slippage;
   string execution_mode;
   bool   emergency;
   int    critical_delay;

   string logs[6];
};

class IRightPanelTab
{
public:
   virtual bool Init(const string prefix,const int x,const int y,const int w,const int h)=0;
   virtual void Update(const SPanelSnapshot &s)=0;
   virtual void SetVisible(const bool visible)=0;
};

#endif
