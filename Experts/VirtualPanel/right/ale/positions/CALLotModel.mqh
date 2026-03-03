#ifndef __CALLOTMODEL_MQH__
#define __CALLOTMODEL_MQH__

class CALLotModel
{
public:
   double LotForBuyLevel(const int level,const double base_lot) const { return base_lot*(1.0+0.2*level); }
   double LotForSellLevel(const int level,const double base_lot) const { return base_lot*(1.0+0.2*level); }
};

#endif
