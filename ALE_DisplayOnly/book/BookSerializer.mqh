#ifndef ALE_DO_BOOK_BOOKSERIALIZER_MQH_INCLUDED
#define ALE_DO_BOOK_BOOKSERIALIZER_MQH_INCLUDED

#include "VirtualBook.mqh"

class CBookSerializer
  {
public:
   static string ToString(const VirtualBook &book)
     {
      return("{}");
     }
  };

#endif // ALE_DO_BOOK_BOOKSERIALIZER_MQH_INCLUDED
