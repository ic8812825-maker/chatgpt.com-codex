#ifndef __CALSAFEMODE_MQH__
#define __CALSAFEMODE_MQH__

class CALSafeMode
{
public:
   bool TriggerBuy(const double dd,const double limit) const { return dd>=limit; }
   bool TriggerSell(const double dd,const double limit) const { return dd>=limit; }
};

#endif
