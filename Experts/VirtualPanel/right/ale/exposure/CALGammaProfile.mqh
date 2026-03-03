#ifndef __CALGAMMAPROFILE_MQH__
#define __CALGAMMAPROFILE_MQH__

class CALGammaProfile
{
public:
   double GammaForBuy(const double curvature) const { return MathMax(0.0,curvature); }
   double GammaForSell(const double curvature) const { return MathMax(0.0,curvature); }
};

#endif
