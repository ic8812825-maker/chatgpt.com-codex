#ifndef __CALLOTOPTIMIZER_MQH__
#define __CALLOTOPTIMIZER_MQH__

#include "..\\math\\CALPhaseDiagram.mqh"

class CALLotOptimizer
{
private:
   CALPhaseDiagram m_phase;

public:
   double OptimizeBuy(const double base_lot,const double risk_factor,const double k=0.5,const double g=0.8,const double sigma=0.2) const
   {
      const double raw=base_lot*MathMax(0.1,1.0-risk_factor);
      return (m_phase.IsStable(k,g,sigma) ? raw : MathMin(raw,base_lot));
   }

   double OptimizeSell(const double base_lot,const double risk_factor,const double k=0.5,const double g=0.8,const double sigma=0.2) const
   {
      const double raw=base_lot*MathMax(0.1,1.0-risk_factor);
      return (m_phase.IsStable(k,g,sigma) ? raw : MathMin(raw,base_lot));
   }
};

#endif
