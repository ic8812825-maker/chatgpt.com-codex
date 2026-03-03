#ifndef __CALLOTOPTIMIZER_MQH__
#define __CALLOTOPTIMIZER_MQH__

class CALLotOptimizer
{
public:
   double OptimizeBuy(const double base_lot,const double risk_factor) const { return base_lot*MathMax(0.1,1.0-risk_factor); }
   double OptimizeSell(const double base_lot,const double risk_factor) const { return base_lot*MathMax(0.1,1.0-risk_factor); }
};

#endif
