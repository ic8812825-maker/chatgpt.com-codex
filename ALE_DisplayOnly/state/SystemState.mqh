#pragma once

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
