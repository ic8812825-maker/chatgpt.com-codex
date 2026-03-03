#ifndef __CALCRITICALMU_MQH__
#define __CALCRITICALMU_MQH__

class CALCriticalMu
{
public:
   double Evaluate(const double sigma,const double k) const { return 0.5*sigma*sigma + k; }
};

#endif
