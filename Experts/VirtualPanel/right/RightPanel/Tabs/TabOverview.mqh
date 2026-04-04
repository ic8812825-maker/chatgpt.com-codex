#ifndef __RIGHTPANEL_TABS_OVERVIEW_MQH__
#define __RIGHTPANEL_TABS_OVERVIEW_MQH__
#include "../UI/Label.mqh"
#include "ITab.mqh"

class CTabOverview : public IRightPanelTab
{
private:
   CUILabel m_lines[8];
public:
   bool Init(const string p,const int x,const int y,const int w,const int h)
   {
      m_lines[0].Create(p+"_ov_0",x+8,y+8,"System Status:");
      for(int i=1;i<8;i++) m_lines[i].Create(p+"_ov_"+(string)i,x+8,y+8+i*20,"-");
      return true;
   }
   void Update(const SPanelSnapshot &s)
   {
      m_lines[0].SetText("System Status: "+s.system_status);
      m_lines[1].SetText("E[dV]: "+DoubleToString(s.e_dv,4));
      m_lines[2].SetText("P(dV<=0): "+DoubleToString(s.p_non_pos*100.0,1)+"%");
      m_lines[3].SetText("max(V): "+DoubleToString(s.max_v,2));
      m_lines[4].SetText("Control Strength: "+DoubleToString(s.control_strength,2));
      m_lines[5].SetText("Current Action: "+s.current_action);
      m_lines[6].SetText("Latency: "+(string)s.latency_ticks+" ticks");
      m_lines[7].SetText("Panel: RIGHT ONLY");
   }
   void SetVisible(const bool v){ for(int i=0;i<8;i++) m_lines[i].SetVisible(v); }
};

#endif
