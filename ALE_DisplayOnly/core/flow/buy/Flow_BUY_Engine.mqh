#ifndef ALE_DO_CORE_FLOW_BUY_FLOW_BUY_ENGINE_MQH_INCLUDED
#define ALE_DO_CORE_FLOW_BUY_FLOW_BUY_ENGINE_MQH_INCLUDED

#include "../common/FlowSnapshot.mqh"
#include "../common/FlowContext.mqh"
#include "../common/FlowMath.mqh"
#include "../../geometry/Geometry_Volume.mqh"
#include "../../geometry/Geometry_Distance.mqh"
#include "../../margin/Margin_Calc.mqh"
#include "Flow_BUY_Rules.mqh"

class CFlowBuyEngine
  {
public:
   static FlowSnapshot Compute(const FlowContext &ctx,const FlowSnapshot &previous_snapshot)
     {
      FlowSnapshot next_snapshot=previous_snapshot;
      const double distance=CGeometryDistance::Compute(ctx.geometry.market_price,ctx.geometry.anchor_price);
      const double volume=CGeometryVolume::Compute(ctx.signal_strength);
      const double margin=CMarginCalc::Required(volume);

      next_snapshot.metric=CFlowMath::Normalize(distance+margin);
      next_snapshot.version=previous_snapshot.version+1;
      return(next_snapshot);
     }
  };

#endif // ALE_DO_CORE_FLOW_BUY_FLOW_BUY_ENGINE_MQH_INCLUDED
