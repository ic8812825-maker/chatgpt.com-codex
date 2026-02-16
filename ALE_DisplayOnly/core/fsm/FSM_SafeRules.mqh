#ifndef ALE_DO_CORE_FSM_FSM_SAFERULES_MQH_INCLUDED
#define ALE_DO_CORE_FSM_FSM_SAFERULES_MQH_INCLUDED

#include "FSM_State.mqh"
#include "../flow/common/FlowSnapshot.mqh"

class CFSMSafeRules
  {
public:
   static bool IsSafeTransition(const FSM_StateId from_state,const FSM_StateId to_state)
     {
      if(from_state==FSM_STATE_SAFE && to_state==FSM_STATE_ACTIVE)
         return(false);
      return(true);
     }

   static bool ShouldEnterSafeMode(const FlowSnapshot &snapshot)
     {
      return(snapshot.metric<0.0);
     }
  };

#endif // ALE_DO_CORE_FSM_FSM_SAFERULES_MQH_INCLUDED
