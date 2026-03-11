#ifndef __CALCONVEXITYANALYZER_MQH__
#define __CALCONVEXITYANALYZER_MQH__

class CALConvexityAnalyzer
{
public:
   double ConvexityBuy(const double gamma,const double delta) const { return gamma*MathAbs(delta); }
   double ConvexitySell(const double gamma,const double delta) const { return gamma*MathAbs(delta); }
};

#endif
