#ifndef __CALLYAPUNOVTAILEFFECT_MQH__
#define __CALLYAPUNOVTAILEFFECT_MQH__

#include "CALLyapunovMetrics.mqh"

class CALLyapunovTailEffect
{
public:
   static double EstimateRiskProxy(const double margin_usage,const double depth,const double exposure)
   {
      return 0.45*CALLyapunovMetrics::Normalize(margin_usage,1.5)
           + 0.30*CALLyapunovMetrics::Normalize(depth,60.0)
           + 0.25*CALLyapunovMetrics::Normalize(exposure,10.0);
   }

   static double Score(const double risk_before,const double risk_after)
   {
      return CALLyapunovMetrics::TailEffect(risk_before,risk_after);
   }
};

#endif
