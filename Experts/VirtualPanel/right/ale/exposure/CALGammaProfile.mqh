#ifndef __CALGAMMAPROFILE_MQH__
#define __CALGAMMAPROFILE_MQH__

class CALGammaProfile
{
public:
   // I2 piecewise-constant gamma from delta jumps
   double FromDeltaSurface(const double delta_left,const double delta_right,const double dp) const
   {
      if(MathAbs(dp)<1e-12) return 0.0;
      return MathAbs((delta_right-delta_left)/dp);
   }
};

#endif
