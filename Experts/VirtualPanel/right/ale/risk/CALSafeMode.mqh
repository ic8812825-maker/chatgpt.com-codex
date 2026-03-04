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
      m_alpha=alpha; m_beta=beta; m_gamma=gamma; m_k=k;
   }

   bool Evaluate(const double margin,const double dd,const double delta,const double gamma_value) const
   {
      const double phase=m_alpha*margin + m_beta*dd + m_gamma*MathAbs(delta) + MathMax(0.0,-gamma_value) - m_k;
      return phase>0.0;
   }

   bool TriggerBuy(const double dd,const double limit) const { return dd>=limit; }
   bool TriggerSell(const double dd,const double limit) const { return dd>=limit; }
};

#endif
