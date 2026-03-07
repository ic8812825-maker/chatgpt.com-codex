#ifndef __IALENGINE_MQH__
#define __IALENGINE_MQH__

#include "..\\core\\CALContext.mqh"

class IALEngine
{
public:
   virtual void Init()=0;
   virtual void OnPriceUpdate(const double price)=0;

   virtual double NetDeltaBuy() const=0;
   virtual double NetDeltaSell() const=0;
   virtual double NetDeltaCommon() const=0;

   virtual double PnLBuy() const=0;
   virtual double PnLSell() const=0;
   virtual double PnLCommon() const=0;

   virtual double ExposureCommon() const=0;
   virtual double MarginCommon() const=0;
   virtual double WorstDDCommon() const=0;
   virtual bool SAFECommon() const=0;

   virtual ENUM_ALE_STATE StateBuy() const=0;
   virtual ENUM_ALE_STATE StateSell() const=0;
   virtual ENUM_ALE_STATE StateCommon() const=0;
   virtual CALContext Context() const=0;
};

#endif
