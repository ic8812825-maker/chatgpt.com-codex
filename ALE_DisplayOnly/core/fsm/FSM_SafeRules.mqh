#pragma once

#include "../flow/common/FlowSnapshot.mqh"

bool FSM_IsSafeTransition(const FSM_StateId from_state,const FSM_StateId to_state)
  {
   if(from_state==FSM_STATE_SAFE && to_state==FSM_STATE_ACTIVE)
      return(false);
   return(true);
  }

bool FSM_ShouldEnterSafeMode(const FlowSnapshot &snapshot)
  {
   return(snapshot.metric<0.0);
  }
