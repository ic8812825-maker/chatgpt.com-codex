#ifndef __CALLOCKCOMPRESSION_MQH__
#define __CALLOCKCOMPRESSION_MQH__

#include "..\\positions\\CALPositionBook.mqh"

class CALLockCompression
{
public:
   bool Compress(CALPositionBook &book,const double alpha) const
   {
      if(alpha<=0.0 || alpha>1.0)
         return false;
      if(book.Size()<=0)
         return false;

      // TYPE C — LOCK COMPRESSION (effective exposure scaling).
      // In single-stream book this is implemented as proportional lot reduction
      // while preserving relative geometry of existing levels.
      return book.ScaleLots(alpha);
   }
};

#endif
