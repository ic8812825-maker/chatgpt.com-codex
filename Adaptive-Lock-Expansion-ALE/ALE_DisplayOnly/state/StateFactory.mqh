#ifndef ALE_DO_STATE_STATEFACTORY_MQH_INCLUDED
#define ALE_DO_STATE_STATEFACTORY_MQH_INCLUDED

#include "SystemState.mqh"
#include "DualState.mqh"

class CStateFactory
  {
public:
   static SystemState CreateSystemState()
     {
      SystemState state;
      return(state);
     }

   static DualState CreateDualState()
     {
      DualState state;
      return(state);
     }
  };

#endif // ALE_DO_STATE_STATEFACTORY_MQH_INCLUDED
