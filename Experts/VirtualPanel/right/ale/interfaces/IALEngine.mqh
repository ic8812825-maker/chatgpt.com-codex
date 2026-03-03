#ifndef __IALENGINE_MQH__
#define __IALENGINE_MQH__

#include "..\core\CALContext.mqh"

class IALEngine
{
public:
   virtual void Init(const int direction)=0;
   virtual void OnPriceUpdate(const double bid,const double ask)=0;
   virtual CALContext Context() const=0;
   virtual ENUM_ALE_STATE StateBuy() const=0;
   virtual ENUM_ALE_STATE StateSell() const=0;
};

#endif
