#ifndef __CALWORSTCASE_MQH__
#define __CALWORSTCASE_MQH__

class CALWorstCase
{
public:
   // I4 closed-form over linear segment endpoint values.
   double DrawdownFromEndpoints(const double pnl_min,const double pnl_max) const
   {
      return MathMax(-pnl_min,-pnl_max);
   }

   double EvaluateBuy(const double pnl_at_min,const double pnl_at_max) const
   {
      return DrawdownFromEndpoints(pnl_at_min,pnl_at_max);
   }

   double EvaluateSell(const double pnl_at_min,const double pnl_at_max) const
   {
      return DrawdownFromEndpoints(pnl_at_min,pnl_at_max);
   }
};

#endif
