#ifndef __CALLYAPUNOVMETRICS_MQH__
#define __CALLYAPUNOVMETRICS_MQH__

class CALLyapunovMetrics
{
public:
   static double Clamp01(const double v)
   {
      if(v<0.0) return 0.0;
      if(v>1.0) return 1.0;
      return v;
   }

   static double SafeDiv(const double a,const double b,const double fallback=0.0)
   {
      if(MathAbs(b)<=1e-12) return fallback;
      return a/b;
   }

   static double Normalize(const double value,const double scale)
   {
      return Clamp01(MathAbs(SafeDiv(value,MathMax(1e-12,scale),0.0)));
   }

   static double DepthScore(const int levels,const int max_levels)
   {
      return Clamp01(SafeDiv((double)levels,(double)MathMax(1,max_levels),0.0));
   }

   static double ExposureScore(const double abs_lot,const double lot_limit)
   {
      return Normalize(abs_lot,MathMax(1e-6,lot_limit));
   }

   static double TailEffect(const double risk_before,const double risk_after)
   {
      // >0 => risk reduction, <0 => risk increase
      return Clamp01((risk_before-risk_after)+0.5)-0.5;
   }

   static double PnLContribution(const double pnl_before,const double pnl_after,const double equity0)
   {
      return SafeDiv(pnl_after-pnl_before,MathMax(1.0,equity0),0.0);
   }
};

#endif
