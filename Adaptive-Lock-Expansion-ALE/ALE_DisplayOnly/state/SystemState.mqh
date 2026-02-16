#ifndef ALE_DO_STATE_SYSTEMSTATE_MQH_INCLUDED
#define ALE_DO_STATE_SYSTEMSTATE_MQH_INCLUDED

#include "../book/VirtualBook.mqh"
#include "../core/ALE_Params.mqh"
#include "../core/fsm/FSM_State.mqh"
#include "AnchorState.mqh"

class SystemState
  {
public:
   VirtualBook  book;
   AnchorState  anchor;
   ALE_Params   params;
   FSM_StateId  fsm_state;

               SystemState() : fsm_state(FSM_STATE_IDLE) {}
  };

#endif // ALE_DO_STATE_SYSTEMSTATE_MQH_INCLUDED
