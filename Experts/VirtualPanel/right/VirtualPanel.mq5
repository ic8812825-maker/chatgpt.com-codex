#property strict
#property description "ALE static runtime validation EA stub"

#include "ALECore.mqh"
#include "ALEGeometry.mqh"
#include "ALEStateMachine.mqh"

#define VP_PANEL_MAIN     "VP_PANEL_MAIN"
#define VP_BTN_BUY        "VP_BTN_BUY"
#define VP_BTN_SELL       "VP_BTN_SELL"
#define VP_LABEL_STATUS   "VP_LABEL_STATUS"

int OnInit()
{
   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
   (void)reason;
}

void OnTick()
{
}
