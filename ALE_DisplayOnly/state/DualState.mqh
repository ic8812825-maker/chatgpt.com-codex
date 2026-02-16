#ifndef __ALE_DisplayOnly_STATE_DUALSTATE_MQH__
#define __ALE_DisplayOnly_STATE_DUALSTATE_MQH__

#include "../core/flow/common/FlowSnapshot.mqh"
#include "../core/ALE_Types.mqh"

struct DualState
  {
   FlowSnapshot buy_snapshot;
   FlowSnapshot sell_snapshot;
   ALE_Side active_side;
  };

#endif // __ALE_DisplayOnly_STATE_DUALSTATE_MQH__
