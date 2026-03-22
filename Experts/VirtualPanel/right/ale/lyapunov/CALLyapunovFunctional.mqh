#ifndef __CALLYAPUNOVFUNCTIONAL_MQH__
#define __CALLYAPUNOVFUNCTIONAL_MQH__

#include "CALLyapunovTypes.mqh"
#include "CALLyapunovMetrics.mqh"

class CALLyapunovFunctional
{
private:
   CALLyapunovWeights m_w;

public:
   CALLyapunovFunctional(){ m_w.SetDefault(); }
   void SetWeights(const CALLyapunovWeights &w){ m_w=w; }

   double V(const CALLyapunovState &s) const
   {
      const double nd=CALLyapunovMetrics::Normalize(s.drawdown,1.0);
      const double ne=CALLyapunovMetrics::Normalize(s.exposure,10.0);
      const double nm=CALLyapunovMetrics::Normalize(s.margin_usage,1.5);
      const double nx=CALLyapunovMetrics::Normalize(s.depth,60.0);
      const double nb=CALLyapunovMetrics::Normalize(s.distance_to_be,5000.0);
      const double nl=CALLyapunovMetrics::Normalize(s.unrealized_loss,50000.0);
      const double nt=CALLyapunovMetrics::Normalize(s.tail_effect,1.0);
      const double np=CALLyapunovMetrics::Normalize(s.pnl_contribution,0.2);

      return m_w.w_drawdown*nd + m_w.w_exposure*ne + m_w.w_margin*nm + m_w.w_depth*nx
           + m_w.w_distance*nb + m_w.w_loss*nl + m_w.w_tail*(1.0-nt) + m_w.w_pnl*(1.0-np);
   }

   double DeltaV(const CALLyapunovState &st,const CALLyapunovState &st1) const
   {
      return V(st1)-V(st);
   }

   bool Exists(const CALLyapunovState &probe) const
   {
      const double v=V(probe);
      return MathIsValidNumber(v) && v==v;
   }
};

#endif
