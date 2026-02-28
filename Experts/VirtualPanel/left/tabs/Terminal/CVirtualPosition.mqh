#ifndef __CVIRTUALPOSITION_MQH__
#define __CVIRTUALPOSITION_MQH__

#include "..\\..\\..\\constants\\PanelConstants.mqh"

class CVirtualPosition
{
public:
   int id;
   int dir;
   int direction;
   double price;
   double lot;
   string comment;

   // virtual-engine metrics
   double floating_pnl;
   double used_margin;
   datetime opened_at;
   string symbol;

   void Init(const int _id,const int _direction,const double _price,const double _lot,const string _comment="")
   {
      id=_id;
      dir=_direction;
      direction=_direction;
      price=_price;
      lot=_lot;
      comment=_comment;

      floating_pnl=0.0;
      used_margin=0.0;
      opened_at=TimeCurrent();
      symbol=_Symbol;
   }

   void UpdateVirtualMetrics(const double bid,const double ask,const double contract_size,const double leverage)
   {
      const double mark=(dir==DIR_BUY ? bid : ask);
      const double d=(dir==DIR_BUY ? (mark-price) : (price-mark));
      floating_pnl=d*lot*contract_size;

      const double margin_price=(dir==DIR_BUY ? ask : bid);
      const double lvg=(leverage>0.0?leverage:1.0);
      used_margin=(margin_price*lot*contract_size)/lvg;
   }
};

#endif // __CVIRTUALPOSITION_MQH__
