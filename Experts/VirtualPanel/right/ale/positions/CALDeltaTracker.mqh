#ifndef __CALDELTATRACKER_MQH__
#define __CALDELTATRACKER_MQH__

#include "CALPositionBook.mqh"

class CALDeltaTracker
{
public:
   double CalculateNetDelta(const CALPositionBook &book,const int direction) const
   {
      return (direction==ALE_FLOW_BUY ? book.TotalLot() : -book.TotalLot());
   }

   double CalculateTailSlope(const CALPositionBook &book) const
   {
      const int n=book.Size();
      if(n<=1) return 0.0;
      return book.TotalLot()/n;
   }
};

#endif
