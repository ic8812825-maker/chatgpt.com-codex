#ifndef __CALGBMMODEL_MQH__
#define __CALGBMMODEL_MQH__

class CALGBMModel
{
private:
   double LCG(const int seed) const
   {
      const long a=1103515245;
      const long c=12345;
      const long m=2147483647;
      long x=(long)MathAbs(seed+1);
      x=(a*x + c) % m;
      return ((double)x)/((double)m);
   }

public:
   double Forward(const double s0,const double mu,const double sigma,const double t) const
   {
      return s0*MathExp((mu-0.5*sigma*sigma)*t);
   }

   double MonteCarloReturnProb(const double s0,const double mu,const double sigma,const double dt,const int steps,const int simulations,const double target) const
   {
      if(s0<=0.0 || sigma<=0.0 || dt<=0.0 || steps<=0 || simulations<=0) return 0.0;

      int success=0;
      const int n=MathMin(simulations,100000);
      for(int i=0;i<n;i++)
      {
         double s=s0;
         for(int t=0;t<steps;t++)
         {
            const double u=LCG(i*steps + t + 17);
            const double z=(u-0.5)*2.0;
            s = s*MathExp((mu-0.5*sigma*sigma)*dt + sigma*MathSqrt(dt)*z);
         }
         if(s>=target) success++;
      }

      return ((double)success)/((double)n);
   }
};

#endif
