#ifndef ALE_DO_UI_RIGHT_RIGHTTABS_MQH_INCLUDED
#define ALE_DO_UI_RIGHT_RIGHTTABS_MQH_INCLUDED

#include <Controls\TabControl.mqh>

#include "../../state/SystemState.mqh"
#include "../../state/DualState.mqh"

class CRightTabsControl
  {
private:
   CTabControl m_tabs;
   bool        m_initialized;

public:
            CRightTabsControl() : m_initialized(false) {}

   bool     Init(const int x1,const int y1,const int x2,const int y2)
     {
      if(m_initialized)
         return(true);

      if(!m_tabs.Create(0,"ALE_RightTabs",0,x1,y1,x2,y2))
         return(false);

      m_initialized=true;
      return(true);
     }

   void     UpdateLayout(const int x1,const int y1,const int x2,const int y2)
     {
      if(!m_initialized)
         return;
      m_tabs.Move(x1,y1,x2,y2);
     }

   void     OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
     {
      if(m_initialized)
         m_tabs.ChartEvent(id,lparam,dparam,sparam);
     }

   void     Shutdown(const int reason)
     {
      if(m_initialized)
         m_tabs.Destroy(reason);
      m_initialized=false;
     }
  };

CRightTabsControl g_right_tabs;

void RightTabs_Render(const SystemState &system_state,const DualState &dual_state,const int x1,const int y1,const int x2,const int y2)
  {
   if(!g_right_tabs.Init(x1,y1,x2,y2))
      return;
   g_right_tabs.UpdateLayout(x1,y1,x2,y2);
  }

void RightTabs_OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
  {
   g_right_tabs.OnChartEvent(id,lparam,dparam,sparam);
  }

void RightTabs_Destroy(const int reason)
  {
   g_right_tabs.Shutdown(reason);
  }

#endif // ALE_DO_UI_RIGHT_RIGHTTABS_MQH_INCLUDED
