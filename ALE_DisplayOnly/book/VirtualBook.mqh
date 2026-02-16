#ifndef ALE_DO_BOOK_VIRTUALBOOK_MQH_INCLUDED
#define ALE_DO_BOOK_VIRTUALBOOK_MQH_INCLUDED

#include "VirtualPosition.mqh"

class VirtualBook
  {
public:
   VirtualPosition items[];
   int             items_total;

                     VirtualBook() : items_total(0) {}
  };

#endif // ALE_DO_BOOK_VIRTUALBOOK_MQH_INCLUDED
