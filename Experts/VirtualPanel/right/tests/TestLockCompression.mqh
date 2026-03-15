#ifndef __TESTLOCKCOMPRESSION_MQH__
#define __TESTLOCKCOMPRESSION_MQH__

#include "..\\ale\\compression\\CALCompressionEngine.mqh"

bool TestLockCompression_Run()
{
   CALPositionBook book;
   book.Init(ALE_FLOW_BUY);
   book.Add(1.0,0.4);
   book.Add(1.1,0.2);

   CALStreamContext ctx;
   ctx.Reset();
   ctx.margin=100.0;
   ctx.exposure=10.0;
   ctx.net_delta=book.Delta();

   CALCompressionEngine c;
   c.SetAlpha(0.5);
   c.SetTriggerLevels(1);

   const bool ok=c.ProcessCompression(book,ctx,10000.0,false);
   if(!ok) return false;

   if(MathAbs(book.TotalAbsLot()-0.3)>1e-12) return false;
   if(!(MathAbs(ctx.net_delta) < 0.4+0.2)) return false;
   if(c.HistorySize()<=0) return false;
   return true;
}

#endif
