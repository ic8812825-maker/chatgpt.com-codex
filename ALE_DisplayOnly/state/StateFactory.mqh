#ifndef __ALE_DisplayOnly_STATE_STATEFACTORY_MQH__
#define __ALE_DisplayOnly_STATE_STATEFACTORY_MQH__

#include "SystemState.mqh"
#include "DualState.mqh"

SystemState StateFactory_CreateSystemState()
  {
   SystemState state;
   return(state);
  }

DualState StateFactory_CreateDualState()
  {
   DualState state;
   return(state);
  }

#endif // __ALE_DisplayOnly_STATE_STATEFACTORY_MQH__
