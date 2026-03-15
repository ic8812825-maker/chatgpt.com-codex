#ifndef __TESTALCSTABILITY_MQH__
#define __TESTALCSTABILITY_MQH__

#include "..\\ale\\compression\\CALCompressionEngine.mqh"

bool TestALCStability_Run()
{
   CALPositionBook book;
   book.Init(ALE_FLOW_BUY);
   for(int i=0;i<12;i++)
      book.Add(1.0+0.001*i,0.1);

   CALStreamContext ctx;
   ctx.Reset();
   ctx.margin=50.0;
   ctx.exposure=book.TotalAbsLot()*1.0;
   ctx.net_delta=book.Delta();

   CALCompressionEngine c;
   c.SetTriggerLevels(8);

   if(!c.ShouldTrigger(book,ctx.margin,10000.0,false)) return false;
   if(!c.ProcessCompression(book,ctx,10000.0,false)) return false;
   if(ctx.exposure<=0.0) return false;
   if(c.LastEvent().levels_after>c.LastEvent().levels_before) return false;
   return true;
}

#endif
