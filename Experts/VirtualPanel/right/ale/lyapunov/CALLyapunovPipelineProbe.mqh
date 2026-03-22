#ifndef __CALLYAPUNOVPIPELINEPROBE_MQH__
#define __CALLYAPUNOVPIPELINEPROBE_MQH__

#include "..\\core\\CALFlowEngine.mqh"
#include "..\\positions\\CALPositionBook.mqh"
#include "..\\core\\CALStateMachine.mqh"
#include "..\\risk\\CALRiskEngine.mqh"
#include "CALLyapunovTypes.mqh"
#include "CALLyapunovMetrics.mqh"
#include "CALLyapunovTailEffect.mqh"

class CALLyapunovPipelineProbe
{
public:
   static CALLyapunovState Snapshot(const CALStreamContext &ctx,
                                    const CALPositionBook &book,
                                    const double equity0,
                                    const double distance_to_be,
                                    const double pnl_before,
                                    const double pnl_after,
                                    const double risk_before,
                                    const double risk_after)
   {
      CALLyapunovState s;
      s.drawdown=CALLyapunovMetrics::Clamp01(CALLyapunovMetrics::SafeDiv(MathMax(0.0,-ctx.pnl),MathMax(1.0,equity0),0.0));
      s.exposure=book.TotalAbsLot();
      s.margin_usage=CALLyapunovMetrics::SafeDiv(ctx.margin,MathMax(1.0,equity0),0.0);
      s.depth=(double)book.Size();
      s.distance_to_be=MathMax(0.0,distance_to_be);
      s.unrealized_loss=MathMax(0.0,-ctx.pnl);
      s.tail_effect=CALLyapunovTailEffect::Score(risk_before,risk_after);
      s.pnl_contribution=CALLyapunovMetrics::PnLContribution(pnl_before,pnl_after,equity0);
      return s;
   }
};

#endif
