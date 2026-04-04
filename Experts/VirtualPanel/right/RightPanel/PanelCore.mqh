#ifndef __RIGHTPANEL_PANELCORE_MQH__
#define __RIGHTPANEL_PANELCORE_MQH__

#include "UI/Container.mqh"
#include "UI/TabSwitcher.mqh"
#include "Tabs/ITab.mqh"
#include "Tabs/TabOverview.mqh"
#include "Tabs/TabMPC.mqh"
#include "Tabs/TabRisk.mqh"
#include "Tabs/TabDualFlow.mqh"
#include "Tabs/TabExecution.mqh"
#include "Tabs/TabLogs.mqh"

enum ENUM_PANEL_TAB
{
   TAB_OVERVIEW=0,
   TAB_MPC,
   TAB_RISK,
   TAB_DUAL_FLOW,
   TAB_EXECUTION,
   TAB_LOGS
};

class CRightPanel
{
private:
   CUIContainer    m_root;
   CTabSwitcher    m_switch;
   CTabOverview    m_tab_overview;
   CTabMPC         m_tab_mpc;
   CTabRisk        m_tab_risk;
   CTabDualFlow    m_tab_dual;
   CTabExecution   m_tab_exec;
   CTabLogs        m_tab_logs;
   IRightPanelTab* m_tabs[6];
   int             m_current_tab;
   int             m_x;
   int             m_y;
   int             m_w;
   int             m_h;

public:
   CRightPanel(void): m_current_tab(TAB_OVERVIEW), m_x(0), m_y(0), m_w(300), m_h(0)
   {
      m_tabs[0]=&m_tab_overview;
      m_tabs[1]=&m_tab_mpc;
      m_tabs[2]=&m_tab_risk;
      m_tabs[3]=&m_tab_dual;
      m_tabs[4]=&m_tab_exec;
      m_tabs[5]=&m_tab_logs;
   }

   void Init(void)
   {
      int chart_w=(int)ChartGetInteger(0,CHART_WIDTH_IN_PIXELS);
      int chart_h=(int)ChartGetInteger(0,CHART_HEIGHT_IN_PIXELS);
      int panel_x_start=(int)(chart_w*0.6);

      m_w=300;
      m_h=chart_h;
      m_x=MathMax(panel_x_start,chart_w-m_w);
      m_y=0;

      m_root.Create("RP_ROOT",m_x,m_y,m_w,m_h,(color)0x1E1E1E);
      m_switch.Create(m_x+2,m_y+2,m_w-4);

      int content_y=m_y+28;
      int content_h=m_h-30;
      m_tab_overview.Init("RP",m_x,content_y,m_w,content_h);
      m_tab_mpc.Init("RP",m_x,content_y,m_w,content_h);
      m_tab_risk.Init("RP",m_x,content_y,m_w,content_h);
      m_tab_dual.Init("RP",m_x,content_y,m_w,content_h);
      m_tab_exec.Init("RP",m_x,content_y,m_w,content_h);
      m_tab_logs.Init("RP",m_x,content_y,m_w,content_h);

      SwitchTab(TAB_OVERVIEW);
   }

   void Render(void)
   {
      m_root.SetVisible(true);
      m_switch.SetVisible(true);
      SwitchTab(m_current_tab);
   }

   void Update(const SPanelSnapshot &snapshot)
   {
      m_tabs[m_current_tab].Update(snapshot);
   }

   void OnChartEvent(const int id,const string sparam)
   {
      if(id!=CHARTEVENT_OBJECT_CLICK) return;
      int tab=m_switch.HandleClick(sparam);
      if(tab>=0) SwitchTab(tab);
   }

   void SwitchTab(const int tab)
   {
      m_current_tab=tab;
      for(int i=0;i<6;i++) m_tabs[i].SetVisible(i==tab);
      m_switch.SetActive(tab);
   }
};

#endif
