#property strict

#include "core/ALE_Core.mqh"
#include "state/SystemState.mqh"
#include "state/DualState.mqh"
#include "book/VirtualBook.mqh"
#include "errors/ErrorDispatcher.mqh"
#include "success/SuccessDispatcher.mqh"
#include "ui/left/LeftPanel.mqh"
#include "ui/right/RightPanel.mqh"

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
  }

int OnInit()
  {
   EventSetTimer(1);
   RenderPanels();
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
   EventKillTimer();
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

   if(id==CHARTEVENT_CHART_CHANGE)
      RenderPanels();
  }
