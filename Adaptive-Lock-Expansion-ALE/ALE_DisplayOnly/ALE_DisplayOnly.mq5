#property strict

#include "core/ALE_Core.mqh"
#include "state/SystemState.mqh"
#include "state/DualState.mqh"
#include "book/VirtualBook.mqh"
#include "errors/ErrorDispatcher.mqh"
#include "success/SuccessDispatcher.mqh"
#include "ui/left/LeftPanel.mqh"
#include "ui/right/RightPanel.mqh"

bool g_is_rendering=false;
SystemState g_system_state;
DualState   g_dual_state;
int         g_snapshot_version=0;

void RenderPanels()
  {
   if(g_is_rendering)
      return;

   g_is_rendering=true;

   FlowSnapshot input_snapshot;
   MqlTick tick;

   if(SymbolInfoTick(_Symbol,tick))
      input_snapshot.metric=tick.bid;
   else
      input_snapshot.metric=0.0;
   input_snapshot.version=g_snapshot_version++;

   if(input_snapshot.metric>0.0)
      CALECore::Recalculate(g_system_state,g_dual_state,input_snapshot);

   LeftPanel_Render(g_system_state,g_dual_state);
   RightPanel_Render(g_system_state,g_dual_state);

   g_is_rendering=false;
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
