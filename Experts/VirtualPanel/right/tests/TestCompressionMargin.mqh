#ifndef __TESTCOMPRESSIONMARGIN_MQH__
#define __TESTCOMPRESSIONMARGIN_MQH__

#include "..\\ale\\compression\\CALCompressionEngine.mqh"

bool TestCompressionMargin_Run()
{
   CALPositionBook book;
   book.Init(ALE_FLOW_SELL);
   for(int i=0;i<10;i++)
      book.Add(1.2+0.001*i,0.1);

   CALStreamContext ctx;
   ctx.Reset();
   ctx.margin=200.0;
   ctx.exposure=30.0;
   ctx.net_delta=book.Delta();

   CALCompressionEngine c;
   c.SetAlpha(0.5);
   c.SetTriggerLevels(8);

   if(!c.ProcessCompression(book,ctx,10000.0,false)) return false;
   if(!(ctx.margin<200.0)) return false;
   if(!(ctx.exposure<30.0)) return false;
   return true;
}

#endif
