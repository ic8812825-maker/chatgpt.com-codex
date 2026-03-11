#ifndef __CALOPTIMALK_MQH__
#define __CALOPTIMALK_MQH__

#include "..\\math\\CALPhaseDiagram.mqh"

class CALOptimalK
{
private:
   CALPhaseDiagram m_phase;

   double StabilizeK(const double candidate,const double alpha,const double sigma) const
   {
      if(alpha<0.5 || alpha>0.85) return 0.5;
      if(m_phase.IsStable(candidate,alpha,sigma)) return candidate;
      const double limit=m_phase.StabilityLimit(sigma);
      return MathMax(0.05,(limit*0.99)/MathMax(1e-12,alpha));
   }

public:
   double FindBuy(const double sigma,const double target,const double alpha=0.8) const
   {
      const double candidate=MathMax(0.1,target/(sigma+1e-6));
      return StabilizeK(candidate,alpha,sigma);
   }

   double FindSell(const double sigma,const double target,const double alpha=0.8) const
   {
      const double candidate=MathMax(0.1,target/(sigma+1e-6));
      return StabilizeK(candidate,alpha,sigma);
   }

   double HedgeLot(const double l0,const double k,const double max_safe_volume) const
   {
      if(l0<=0.0 || k<=0.0 || max_safe_volume<=0.0) return 0.0;
      return MathMin(l0*k,max_safe_volume);
   }
};

#endif
