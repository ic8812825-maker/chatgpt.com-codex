#ifndef __CALRETURNPROBABILITY_MQH__
#define __CALRETURNPROBABILITY_MQH__

class CALReturnProbability
{
public:
   double ToCenter(const double distance,const double sigma) const
   {
      if(sigma<=0.0) return 0.0;
      const double z=MathAbs(distance)/(sigma+1e-8);
      return MathExp(-0.5*z*z);
   }

   double HitLevelGBM(const double p,const double l,const double mu,const double sigma) const
   {
      if(p<=0.0 || l<=0.0 || sigma<=0.0 || l>=p) return 0.0;
      if(MathAbs(mu)<1e-12) return l/p;

      const double x=-(2.0*mu/(sigma*sigma))*MathLog(p/l);
      const double clipped=MathMax(-60.0,MathMin(20.0,x));
      return MathMin(1.0,MathMax(0.0,MathExp(clipped)));
   }
};

#endif
