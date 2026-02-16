#ifndef ALE_DO_STATE_DUALSTATE_MQH_INCLUDED
#define ALE_DO_STATE_DUALSTATE_MQH_INCLUDED

#include "../core/flow/common/FlowSnapshot.mqh"
#include "../core/ALE_Types.mqh"

class DualState
  {
public:
   FlowSnapshot buy_snapshot;
   FlowSnapshot sell_snapshot;
   ALE_Side     active_side;

                DualState() : active_side(ALE_SIDE_BUY) {}
  };

#endif // ALE_DO_STATE_DUALSTATE_MQH_INCLUDED
