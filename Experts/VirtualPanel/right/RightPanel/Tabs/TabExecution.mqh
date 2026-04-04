#ifndef __RIGHTPANEL_TABS_EXEC_MQH__
#define __RIGHTPANEL_TABS_EXEC_MQH__
#include "../UI/Label.mqh"
#include "ITab.mqh"

class CTabExecution : public IRightPanelTab
{
private: CUILabel m_l[5];
public:
   bool Init(const string p,const int x,const int y,const int w,const int h){ for(int i=0;i<5;i++) m_l[i].Create(p+"_exe_"+(string)i,x+8,y+8+i*20,"-"); return true; }
   void Update(const SPanelSnapshot &s){
      m_l[0].SetText("Delay: "+(string)s.delay);
      m_l[1].SetText("Slippage: "+DoubleToString(s.slippage,2));
      m_l[2].SetText("Execution Mode: "+s.execution_mode);
      m_l[3].SetText("Emergency: "+(s.emergency?"ON":"OFF"));
      m_l[4].SetText("Critical Delay: "+(string)s.critical_delay);
   }
   void SetVisible(const bool v){ for(int i=0;i<5;i++) m_l[i].SetVisible(v); }
};

#endif
