#ifndef __IALEXPOSUREMODEL_MQH__
#define __IALEXPOSUREMODEL_MQH__

class IALExposureModel
{
public:
   virtual double DeltaSurface(const int direction,const double price,const double center) const=0;
   virtual double GammaProfile(const int direction,const double curvature) const=0;
};

#endif
