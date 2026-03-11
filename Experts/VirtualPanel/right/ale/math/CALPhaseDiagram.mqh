#ifndef __CALPHASEDIAGRAM_MQH__
#define __CALPHASEDIAGRAM_MQH__

enum PhaseState
{
   PHASE_STABLE=0,
   PHASE_MARGINAL=1,
   PHASE_EXPLOSIVE=2
};

class CALPhaseDiagram
{
public:
   double StabilityIndex(const double k,const double g) const
   {
      return k*g;
   }

   PhaseState DetectPhase(const double k,const double g) const
   {
      const double theta=StabilityIndex(k,g);
      if(theta<0.9) return PHASE_STABLE;
      if(theta<1.0) return PHASE_MARGINAL;
      return PHASE_EXPLOSIVE;
   }

   PhaseState DeterminePhase(const double alpha,const double k,const double R,const double L0) const
   {
      const double theta=alpha*k;
      const double threshold1=0.9;
      const double threshold2=1.0;
      if(theta<threshold1) return PHASE_STABLE;
      if(theta<threshold2) return PHASE_MARGINAL;
      return PHASE_EXPLOSIVE;
   }

   double StabilityLimit(const double sigma) const
   {
      return MathExp(-(sigma*sigma)/2.0);
   }

   bool IsStable(const double k,const double g,const double sigma) const
   {
      return StabilityIndex(k,g)<StabilityLimit(sigma);
   }

   double CriticalDD(const double k,const double lambda,const double delta_abs) const
   {
      return k - lambda*delta_abs;
   }

   bool IsSafeRegion(const double dd,const double k,const double lambda,const double delta_abs) const
   {
      return dd > CriticalDD(k,lambda,delta_abs);
   }
};

#endif
