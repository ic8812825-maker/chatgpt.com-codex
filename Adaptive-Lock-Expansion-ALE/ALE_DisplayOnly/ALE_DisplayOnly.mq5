#property strict

#include "core/ALE_Core.mqh"
#include "state/SystemState.mqh"
#include "state/DualState.mqh"
#include "book/VirtualBook.mqh"
#include "errors/ErrorDispatcher.mqh"
#include "success/SuccessDispatcher.mqh"
#include "ui/left/LeftPanel.mqh"
#include "ui/right/RightPanel.mqh"

int OnInit()
  {
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
  }

void OnTick()
  {
   SystemState system_state;
   DualState dual_state;
   FlowSnapshot input_snapshot;

   input_snapshot.metric=0.0;
   input_snapshot.version=0;

   ALE_Recalculate(system_state,dual_state,input_snapshot);
   LeftPanel_Render(system_state,dual_state);
   RightPanel_Render(system_state,dual_state);
  }
