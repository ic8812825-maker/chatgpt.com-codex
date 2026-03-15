#ifndef __TESTCOMPRESSIONTRIGGER_MQH__
#define __TESTCOMPRESSIONTRIGGER_MQH__

#include "..\\ale\\compression\\CALCompressionEngine.mqh"

bool TestCompressionTrigger_Run()
{
   CALCompressionEngine c;
   CALPositionBook book;
   book.Init(ALE_FLOW_BUY);

   for(int i=0;i<9;i++)
      book.Add(1.0+0.001*i,0.1);

   if(!c.ShouldTrigger(book,10.0,10000.0,false)) return false;
   if(!c.ShouldTrigger(book,1000.0,1000.0,true)) return false; // SAFE rescue path

   CALPositionBook small;
   small.Init(ALE_FLOW_BUY);
   small.Add(1.0,0.1);
   if(c.ShouldTrigger(small,10.0,10000.0,false)) return false;
   return true;
}

#endif
