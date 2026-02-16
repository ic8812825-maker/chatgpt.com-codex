#pragma once

#include "../common/FlowSnapshot.mqh"
#include "../common/FlowContext.mqh"
#include "../common/FlowMath.mqh"
#include "../../geometry/Geometry_Volume.mqh"
#include "../../geometry/Geometry_Distance.mqh"
#include "../../margin/Margin_Calc.mqh"
#include "Flow_SELL_Rules.mqh"

FlowSnapshot Flow_SELL_Compute(const FlowContext &ctx,const FlowSnapshot &previous_snapshot)
  {
   FlowSnapshot next_snapshot=previous_snapshot;
   const double distance=Geometry_ComputeDistance(ctx.geometry.anchor_price,ctx.geometry.market_price);
   const double volume=Geometry_ComputeVolume(ctx.signal_strength);
   const double margin=Margin_CalcRequired(volume);

   next_snapshot.metric=FlowMath_Normalize(distance-margin);
   next_snapshot.version=previous_snapshot.version+1;
   return(next_snapshot);
  }
