#ifndef __CALOPTIMALK_MQH__
#define __CALOPTIMALK_MQH__

class CALOptimalK
{
public:
   double FindBuy(const double sigma,const double target) const { return MathMax(0.1,target/(sigma+1e-6)); }
   double FindSell(const double sigma,const double target) const { return MathMax(0.1,target/(sigma+1e-6)); }
};

#endif
