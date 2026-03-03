#ifndef __CALVIRTUALPOSITION_MQH__
#define __CALVIRTUALPOSITION_MQH__

class CALVirtualPosition
{
public:
   double price;
   double lot;
   int direction;
   double pnl;

   void Init(const double p,const double l,const int d){ price=p; lot=l; direction=d; pnl=0.0; }
   void UpdatePnL(const double bid,const double ask,const double contract_size)
   {
      const double mark=(direction>0?bid:ask);
      pnl=(direction>0?(mark-price):(price-mark))*lot*contract_size;
   }
};

#endif
