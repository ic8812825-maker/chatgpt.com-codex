#ifndef __CALSAFEMODE_MQH__
#define __CALSAFEMODE_MQH__

class CALSafeMode
{
private:
   double m_alpha;
   double m_beta;
   double m_gamma;
   double m_k;
public:
   CALSafeMode(){ m_alpha=1.0; m_beta=1.0; m_gamma=1.0; m_k=1.0; }

   void SetParams(const double alpha,const double beta,const double gamma,const double k)
   {
      m_alpha=alpha;
      m_beta=beta;
      m_gamma=gamma;
      m_k=k;
   }

   bool EvaluatePhase(const double margin,const double dd,const double delta,const double gamma_value) const
   {
      const double f=m_alpha*margin + m_beta*dd + m_gamma*MathAbs(delta) + MathMax(0.0,-gamma_value) - m_k;
      return (f>0.0);
   }

   bool EvaluateTriggers(const double margin_level,const double min_margin,
                         const double drawdown,const double max_dd,
                         const double atr,const double atr_limit,
                         const double spread,const double spread_limit,
                         const double p_return,const double p_safe) const
   {
      if(margin_level<min_margin) return true;
      if(drawdown>max_dd) return true;
      if(atr>atr_limit) return true;
      if(spread>spread_limit) return true;
      if(p_return<p_safe) return true;
      return false;
   }

   bool TriggerBuy(const double dd,const double limit) const { return dd>=limit; }
   bool TriggerSell(const double dd,const double limit) const { return dd>=limit; }
};

#endif
