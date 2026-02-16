#ifndef ALE_DO_CORE_ALE_DUALCYCLEENGINE_MQH_INCLUDED
#define ALE_DO_CORE_ALE_DUALCYCLEENGINE_MQH_INCLUDED

#include "flow/buy/Flow_BUY_Engine.mqh"
#include "flow/sell/Flow_SELL_Engine.mqh"
#include "fsm/FSM_Compute.mqh"
#include "invariants/Invariant_Validator.mqh"

void ALE_RunDualCycle(const FlowContext &buy_ctx,
                      const FlowContext &sell_ctx,
                      const FlowSnapshot &input_snapshot,
                      FlowSnapshot &buy_out,
                      FlowSnapshot &sell_out)
  {
   buy_out=Flow_BUY_Compute(buy_ctx,input_snapshot);
   sell_out=Flow_SELL_Compute(sell_ctx,input_snapshot);
  }

#endif // ALE_DO_CORE_ALE_DUALCYCLEENGINE_MQH_INCLUDED
