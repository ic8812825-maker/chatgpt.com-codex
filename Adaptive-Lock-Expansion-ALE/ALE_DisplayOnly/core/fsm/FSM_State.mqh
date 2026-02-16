#ifndef ALE_DO_CORE_FSM_FSM_STATE_MQH_INCLUDED
#define ALE_DO_CORE_FSM_FSM_STATE_MQH_INCLUDED

enum FSM_StateId
  {
   FSM_STATE_IDLE = 0,
   FSM_STATE_ACTIVE = 1,
   FSM_STATE_SAFE = 2
  };

struct FSM_DTO
  {
   FSM_StateId current;
   FSM_StateId next;
  };

struct FSM_Transition
  {
   FSM_StateId from;
   FSM_StateId to;
  };

#endif // ALE_DO_CORE_FSM_FSM_STATE_MQH_INCLUDED
