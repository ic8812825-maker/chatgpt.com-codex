#pragma once

#include "../core/flow/common/FlowSnapshot.mqh"
#include "../core/ALE_Types.mqh"

struct DualState
  {
   FlowSnapshot buy_snapshot;
   FlowSnapshot sell_snapshot;
   ALE_Side active_side;
  };
