#ifndef __IALEXPOSUREMODEL_MQH__
#define __IALEXPOSUREMODEL_MQH__

#include "..\\positions\\CALPositionBook.mqh"

class IALExposureModel
{
public:
   virtual void Recalculate(const CALPositionBook &book,const double price)=0;
   virtual double Exposure() const=0;
   virtual double DeltaSurface() const=0;
   virtual double GammaProfile() const=0;
};

#endif
