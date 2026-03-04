#ifndef __CALDELTASURFACE_MQH__
#define __CALDELTASURFACE_MQH__

#include "..\\positions\\CALPositionBook.mqh"

class CALDeltaSurface
{
public:
   // I2 piecewise-linear (constant slope segments for linear position model)
   double DeltaFromBook(const CALPositionBook &book) const { return book.Delta(); }

   double DeltaForBuy(const double price,const double center) const
   {
      return (price>=center ? 1.0 : -1.0);
   }

   double DeltaForSell(const double price,const double center) const
   {
      return -DeltaForBuy(price,center);
   }
};

#endif
