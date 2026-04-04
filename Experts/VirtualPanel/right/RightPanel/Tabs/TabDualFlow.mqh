#ifndef __RIGHTPANEL_TABS_DUAL_MQH__
#define __RIGHTPANEL_TABS_DUAL_MQH__
#include "../UI/Label.mqh"
#include "ITab.mqh"

class CTabDualFlow : public IRightPanelTab
{
private: CUILabel m_l[6];
public:
   bool Init(const string p,const int x,const int y,const int w,const int h){ for(int i=0;i<6;i++) m_l[i].Create(p+"_dual_"+(string)i,x+8,y+8+i*20,"-"); return true; }
   void Update(const SPanelSnapshot &s){
      m_l[0].SetText("BUY Exposure: "+DoubleToString(s.buy_exposure,2));
      m_l[1].SetText("SELL Exposure: "+DoubleToString(s.sell_exposure,2));
      m_l[2].SetText("Asymmetry: "+DoubleToString(s.asymmetry,5));
      m_l[3].SetText("Cross-impact: "+DoubleToString(s.cross_impact,4));
      m_l[4].SetText("Total V: "+DoubleToString(s.total_v,2));
      m_l[5].SetText("Status: "+(s.total_v<1.2?"STABLE":"RISK"));
   }
   void SetVisible(const bool v){ for(int i=0;i<6;i++) m_l[i].SetVisible(v); }
};

#endif
