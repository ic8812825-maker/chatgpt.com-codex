#ifndef ALE_DO_CORE_ALE_CORE_MQH_INCLUDED
#define ALE_DO_CORE_ALE_CORE_MQH_INCLUDED

#include "ALE_DualCycleEngine.mqh"
#include "ALE_Params.mqh"
#include "ALE_Types.mqh"
#include "../state/SystemState.mqh"
#include "../state/DualState.mqh"
#include "../errors/ErrorDispatcher.mqh"
#include "../success/SuccessDispatcher.mqh"

void ALE_Recalculate(SystemState &system_state,DualState &dual_state,const FlowSnapshot &input_snapshot)
  {
   FlowContext buy_ctx;
   buy_ctx.geometry.anchor_price=system_state.anchor.anchor_price;
   buy_ctx.geometry.market_price=system_state.anchor.anchor_price;
   buy_ctx.signal_strength=1.0;

   FlowContext sell_ctx=buy_ctx;

   ALE_RunDualCycle(buy_ctx,sell_ctx,input_snapshot,dual_state.buy_snapshot,dual_state.sell_snapshot);

   const FSM_DTO fsm=FSM_ComputeState(system_state,input_snapshot);
   system_state.fsm_state=fsm.next;
  }

#endif // ALE_DO_CORE_ALE_CORE_MQH_INCLUDED
