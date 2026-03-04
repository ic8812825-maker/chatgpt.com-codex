#ifndef __CALMARGINMODEL_MQH__
#define __CALMARGINMODEL_MQH__

class CALMarginModel
{
public:
   // I3
   double MarginFromLots(const double abs_lot,const double contract_size,const double margin_rate) const
   {
      return MathAbs(abs_lot)*contract_size*MathMax(0.0,margin_rate);
   }

   double MarginBuy(const double price,const double lots,const double leverage,const double contract_size) const
   {
      const double margin_rate=(leverage>0.0?1.0/leverage:1.0);
      return MarginFromLots(lots,contract_size,margin_rate);
   }

   double MarginSell(const double price,const double lots,const double leverage,const double contract_size) const
   {
      const double margin_rate=(leverage>0.0?1.0/leverage:1.0);
      return MarginFromLots(lots,contract_size,margin_rate);
   }
};

#endif
