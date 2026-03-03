#ifndef __CALWORSTCASE_MQH__
#define __CALWORSTCASE_MQH__

class CALWorstCase
{
public:
   double EvaluateBuy(const double pnl,const double shock) const { return pnl - MathAbs(shock); }
   double EvaluateSell(const double pnl,const double shock) const { return pnl - MathAbs(shock); }
};

#endif
