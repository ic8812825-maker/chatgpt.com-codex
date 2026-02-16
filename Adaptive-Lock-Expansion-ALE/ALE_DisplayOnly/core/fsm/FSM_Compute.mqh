#ifndef __ALE_DisplayOnly_CORE_FSM_FSM_COMPUTE_MQH__
#define __ALE_DisplayOnly_CORE_FSM_FSM_COMPUTE_MQH__

#include "FSM_State.mqh"
#include "FSM_SafeRules.mqh"
#include "../../state/SystemState.mqh"
#include "../flow/common/FlowSnapshot.mqh"

FSM_DTO FSM_ComputeState(const SystemState &system_state,const FlowSnapshot &snapshot)
  {
   FSM_DTO dto;
   dto.current=system_state.fsm_state;
   dto.next=system_state.fsm_state;

   if(FSM_ShouldEnterSafeMode(snapshot))
      dto.next=FSM_STATE_SAFE;
   else if(system_state.book.items_total>0)
      dto.next=FSM_STATE_ACTIVE;
   else
      dto.next=FSM_STATE_IDLE;

   if(!FSM_IsSafeTransition(dto.current,dto.next))
      dto.next=dto.current;

   return(dto);
  }

#endif // __ALE_DisplayOnly_CORE_FSM_FSM_COMPUTE_MQH__
