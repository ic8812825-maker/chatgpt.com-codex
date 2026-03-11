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
   virtual double PnLBuy() const=0;
   virtual double PnLSell() const=0;
   virtual ENUM_ALE_STATE StateBuy() const=0;
   virtual ENUM_ALE_STATE StateSell() const=0;
   virtual CALContext Context() const=0;
};

#endif
