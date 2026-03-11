#ifndef __CALGRIDOPTIMIZER_MQH__
#define __CALGRIDOPTIMIZER_MQH__

#include "..\\math\\CALPhaseDiagram.mqh"

class CALGridOptimizer
{
private:
   CALPhaseDiagram m_phase;

public:
   int OptimizeLevelsBuy(const int base_levels,const double volatility,const double k=0.5,const double g=0.8) const
   {
      if(!m_phase.IsStable(k,g,volatility)) return MathMax(1,base_levels-1);
      return MathMax(1,base_levels+(int)MathRound(volatility));
   }

   int OptimizeLevelsSell(const int base_levels,const double volatility,const double k=0.5,const double g=0.8) const
   {
      if(!m_phase.IsStable(k,g,volatility)) return MathMax(1,base_levels-1);
      return MathMax(1,base_levels+(int)MathRound(volatility));
   }
};

#endif
