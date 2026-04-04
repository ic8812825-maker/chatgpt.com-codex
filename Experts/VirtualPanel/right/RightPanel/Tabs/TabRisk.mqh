#ifndef __RIGHTPANEL_TABS_RISK_MQH__
#define __RIGHTPANEL_TABS_RISK_MQH__
#include "../UI/Label.mqh"
#include "ITab.mqh"

class CTabRisk : public IRightPanelTab
{
private: CUILabel m_l[5];
public:
   bool Init(const string p,const int x,const int y,const int w,const int h){ for(int i=0;i<5;i++) m_l[i].Create(p+"_risk_"+(string)i,x+8,y+8+i*20,"-"); return true; }
   void Update(const SPanelSnapshot &s){
      m_l[0].SetText("V(t): "+DoubleToString(s.v_now,2));
      m_l[1].SetText("dV: "+DoubleToString(s.dv_now,3));
      m_l[2].SetText("CVaR: "+DoubleToString(s.cvar,3));
      m_l[3].SetText("Max V: "+DoubleToString(s.max_v,2));
      m_l[4].SetText("Risk Trend: "+s.risk_trend);
      color c=(s.v_now<0.9)?(color)0x5BC28C:((s.v_now<1.2)?(color)0xE1C45A:(color)0xE0695F);
      m_l[0].SetColor(c); m_l[1].SetColor(c);
   }
   void SetVisible(const bool v){ for(int i=0;i<5;i++) m_l[i].SetVisible(v); }
};

#endif
