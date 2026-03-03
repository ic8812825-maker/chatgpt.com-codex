#ifndef __CALGRIDOPTIMIZER_MQH__
#define __CALGRIDOPTIMIZER_MQH__

class CALGridOptimizer
{
public:
   int OptimizeLevelsBuy(const int base_levels,const double volatility) const { return MathMax(1,base_levels+(int)MathRound(volatility)); }
   int OptimizeLevelsSell(const int base_levels,const double volatility) const { return MathMax(1,base_levels+(int)MathRound(volatility)); }
};

#endif
