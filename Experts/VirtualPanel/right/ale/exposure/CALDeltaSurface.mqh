#ifndef __CALDELTASURFACE_MQH__
#define __CALDELTASURFACE_MQH__

class CALDeltaSurface
{
public:
   double DeltaForBuy(const double price,const double center) const { return (price-center); }
   double DeltaForSell(const double price,const double center) const { return (center-price); }
};

#endif
