#ifndef ALE_DO_STATE_DUALSTATE_MQH_INCLUDED
#define ALE_DO_STATE_DUALSTATE_MQH_INCLUDED

#include "../core/flow/common/FlowSnapshot.mqh"
#include "../core/ALE_Types.mqh"

struct DualState
  {
   FlowSnapshot buy_snapshot;
   FlowSnapshot sell_snapshot;
   ALE_Side active_side;
  };

#endif // ALE_DO_STATE_DUALSTATE_MQH_INCLUDED
