#ifndef __IMARKETADAPTER_MQH__
#define __IMARKETADAPTER_MQH__

class IMarketAdapter
{
public:
   virtual double Bid() const=0;
   virtual double Ask() const=0;
   virtual double Spread() const=0;
   virtual double ATR() const=0;
   virtual double MarginRequired(const double volume) const=0;
   virtual double TickValue() const=0;
};

#endif
