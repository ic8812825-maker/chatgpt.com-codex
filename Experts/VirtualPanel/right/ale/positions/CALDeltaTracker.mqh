#ifndef __CALDELTATRACKER_MQH__
#define __CALDELTATRACKER_MQH__

#include "CALPositionBook.mqh"

class CALDeltaTracker
{
public:
   double CalculateNetDelta(const CALPositionBook &book,const int direction) const
   {
      const double d=book.Delta();
      return (direction==ALE_FLOW_BUY ? MathAbs(d) : -MathAbs(d));
   }

   double CalculateTailSlope(const CALPositionBook &book,const double dp) const
   {
      if(MathAbs(dp)<1e-12) return 0.0;
      return book.Delta()/dp;
   }
};

#endif
