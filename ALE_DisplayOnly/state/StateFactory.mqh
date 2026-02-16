#ifndef ALE_DO_STATE_STATEFACTORY_MQH_INCLUDED
#define ALE_DO_STATE_STATEFACTORY_MQH_INCLUDED

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

#endif // ALE_DO_STATE_STATEFACTORY_MQH_INCLUDED
