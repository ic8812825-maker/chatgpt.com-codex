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
};

#endif
