#property strict
#property description "ALE static runtime validation EA mirror"

#include "ALECore.mqh"
#include "ALEGeometry.mqh"
#include "ALEStateMachine.mqh"

int OnInit(){ return(INIT_SUCCEEDED); }
void OnDeinit(const int reason){ (void)reason; }
void OnTick(){}
