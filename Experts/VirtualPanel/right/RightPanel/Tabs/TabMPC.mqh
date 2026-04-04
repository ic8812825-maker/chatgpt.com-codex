#ifndef __RIGHTPANEL_TABS_MPC_MQH__
#define __RIGHTPANEL_TABS_MPC_MQH__
#include "../UI/Label.mqh"
#include "ITab.mqh"

class CTabMPC : public IRightPanelTab
{
private: CUILabel m_l[6];
public:
   bool Init(const string p,const int x,const int y,const int w,const int h){ for(int i=0;i<6;i++) m_l[i].Create(p+"_mpc_"+(string)i,x+8,y+8+i*20,"-"); return true; }
   void Update(const SPanelSnapshot &s){
      m_l[0].SetText("Selected Action: "+s.current_action);
      m_l[1].SetText("Predicted dV: "+DoubleToString(s.predicted_dv,4));
      m_l[2].SetText("Real dV: "+DoubleToString(s.real_dv,4));
      m_l[3].SetText("Argmin Match: "+(s.argmin_match?"YES":"NO"));
      m_l[4].SetText("Horizon: "+(string)s.horizon);
      m_l[5].SetText("Objective: "+DoubleToString(s.objective_value,4));
   }
   void SetVisible(const bool v){ for(int i=0;i<6;i++) m_l[i].SetVisible(v); }
};

#endif
