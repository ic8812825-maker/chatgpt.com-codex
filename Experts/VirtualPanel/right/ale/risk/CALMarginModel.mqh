#ifndef __CALMARGINMODEL_MQH__
#define __CALMARGINMODEL_MQH__

class CALMarginModel
{
public:
   double MarginBuy(const double price,const double lots,const double leverage,const double contract_size) const
   { const double l=(leverage>0.0?leverage:1.0); return (price*lots*contract_size)/l; }
   double MarginSell(const double price,const double lots,const double leverage,const double contract_size) const
   { const double l=(leverage>0.0?leverage:1.0); return (price*lots*contract_size)/l; }
};

#endif
