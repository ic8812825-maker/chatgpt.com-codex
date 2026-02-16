#ifndef ALE_DO_BOOK_VIRTUALBOOK_MQH_INCLUDED
#define ALE_DO_BOOK_VIRTUALBOOK_MQH_INCLUDED

#include "VirtualPosition.mqh"

struct VirtualBook
  {
   VirtualPosition items[];
   int items_total;
  };

#endif // ALE_DO_BOOK_VIRTUALBOOK_MQH_INCLUDED
