#ifndef __IALENGINE_MQH__
#define __IALENGINE_MQH__

#include "..\\core\\CALContext.mqh"

class IALEngine
{
public:
   virtual void Init()=0;
   virtual void OnPriceUpdate(const double bid,const double ask)=0;
   virtual CALContext Context(const int flow) const=0;
   virtual ENUM_ALE_STATE State(const int flow) const=0;
};

#endif

