#ifndef ALE_DO_STATE_SYSTEMSTATE_MQH_INCLUDED
#define ALE_DO_STATE_SYSTEMSTATE_MQH_INCLUDED

#include "../book/VirtualBook.mqh"
#include "../core/ALE_Params.mqh"
#include "../core/fsm/FSM_State.mqh"
#include "AnchorState.mqh"

struct SystemState
  {
   VirtualBook book;
   AnchorState anchor;
   ALE_Params params;
   FSM_StateId fsm_state;
  };

#endif // ALE_DO_STATE_SYSTEMSTATE_MQH_INCLUDED
