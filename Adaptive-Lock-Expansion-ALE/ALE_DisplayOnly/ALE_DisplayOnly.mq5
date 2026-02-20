#property strict

#include "core/ALE_Core.mqh"
#include "state/SystemState.mqh"
#include "state/DualState.mqh"
#include "book/VirtualBook.mqh"
#include "errors/ErrorDispatcher.mqh"
#include "success/SuccessDispatcher.mqh"
#include "ui/left/LeftPanel.mqh"
#include "ui/right/RightPanel.mqh"

bool g_timer_started=false;

void RenderPanels()
  {
   SystemState system_state;
   DualState dual_state;
   FlowSnapshot input_snapshot;

   input_snapshot.metric=0.0;
   input_snapshot.version=0;

   CALECore::Recalculate(system_state,dual_state,input_snapshot);
   LeftPanel_Render(system_state,dual_state);
   RightPanel_Render(system_state,dual_state);
   ChartRedraw(0);
  }

int OnInit()
  {
   ResetLastError();
   EventSetMillisecondTimer(250);
   g_timer_started=(GetLastError()==0);
   if(!g_timer_started)
     {
      ResetLastError();
      EventSetTimer(1);
      g_timer_started=(GetLastError()==0);
     }

   if(!g_timer_started)
      PrintFormat("ALE_DisplayOnly: timer setup failed, err=%d",GetLastError());

   RenderPanels();
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
   EventKillTimer();
   g_timer_started=false;
   LeftPanel_Destroy(reason);
   RightPanel_Destroy(reason);
  }

void OnTick()
  {
   RenderPanels();
  }

void OnTimer()
  {
   RenderPanels();
  }

void OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
  {
   LeftPanel_OnChartEvent(id,lparam,dparam,sparam);
   RightPanel_OnChartEvent(id,lparam,dparam,sparam);

   if(id==CHARTEVENT_CHART_CHANGE ||
      id==CHARTEVENT_CLICK ||
      id==CHARTEVENT_OBJECT_CLICK ||
      id==CHARTEVENT_KEYDOWN)
      RenderPanels();
  }
