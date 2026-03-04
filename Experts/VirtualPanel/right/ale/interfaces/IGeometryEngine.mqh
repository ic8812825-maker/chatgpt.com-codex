#ifndef __IGEOMETRYENGINE_MQH__
#define __IGEOMETRYENGINE_MQH__

class IGeometryEngine
{
public:
   virtual double NextDistance(const double baseDistance,const int level,const double k) const=0;
   virtual double ExpansionVolume(const double baseLot,const int level) const=0;
};

#endif
