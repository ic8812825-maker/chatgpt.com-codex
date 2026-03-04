#ifndef __CALPHASEDIAGRAM_MQH__
#define __CALPHASEDIAGRAM_MQH__

class CALPhaseDiagram
{
public:
   double CriticalDD(const double k,const double lambda,const double delta_abs) const
   {
      return k - lambda*delta_abs;
   }

   bool IsSafeRegion(const double dd,const double k,const double lambda,const double delta_abs) const
   {
      return dd > CriticalDD(k,lambda,delta_abs);
   }

   bool IsStable(const double mu,const double mu_crit) const
   {
      return mu<mu_crit;
   }
};

#endif
