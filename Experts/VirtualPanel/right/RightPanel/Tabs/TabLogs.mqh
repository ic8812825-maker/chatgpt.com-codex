#ifndef __RIGHTPANEL_TABS_LOGS_MQH__
#define __RIGHTPANEL_TABS_LOGS_MQH__
#include "../UI/Label.mqh"
#include "ITab.mqh"

class CTabLogs : public IRightPanelTab
{
private: CUILabel m_l[6];
public:
   bool Init(const string p,const int x,const int y,const int w,const int h){ for(int i=0;i<6;i++) m_l[i].Create(p+"_log_"+(string)i,x+8,y+8+i*20,"-"); return true; }
   void Update(const SPanelSnapshot &s){ for(int i=0;i<6;i++) m_l[i].SetText(s.logs[i]); }
   void SetVisible(const bool v){ for(int i=0;i<6;i++) m_l[i].SetVisible(v); }
};

#endif
