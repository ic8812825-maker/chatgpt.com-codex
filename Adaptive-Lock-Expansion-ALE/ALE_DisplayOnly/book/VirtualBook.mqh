#ifndef __ALE_DisplayOnly_BOOK_VIRTUALBOOK_MQH__
#define __ALE_DisplayOnly_BOOK_VIRTUALBOOK_MQH__

#include "VirtualPosition.mqh"

struct VirtualBook
  {
   VirtualPosition items[];
   int items_total;
  };

#endif // __ALE_DisplayOnly_BOOK_VIRTUALBOOK_MQH__
