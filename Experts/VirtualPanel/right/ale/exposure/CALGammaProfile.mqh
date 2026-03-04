#ifndef __CALGAMMAPROFILE_MQH__
#define __CALGAMMAPROFILE_MQH__

class CALGammaProfile
{
public:
   double FromDeltaSurface(const double delta_surface) const
   {
      return MathMax(0.0,MathAbs(delta_surface));
   }
};

#endif
