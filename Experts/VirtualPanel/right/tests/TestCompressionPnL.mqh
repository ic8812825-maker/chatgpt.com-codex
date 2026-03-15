#ifndef __TESTCOMPRESSIONPNL_MQH__
#define __TESTCOMPRESSIONPNL_MQH__

#include "..\\ale\\compression\\CALCompressionEngine.mqh"

bool TestCompressionPnL_Run()
{
   CALPositionBook book;
   book.Init(ALE_FLOW_BUY);
   book.Add(1.0,0.5);
   const double before=book.PnLAtPrice(1.1,1.0);

   CALStreamContext ctx;
   ctx.Reset();
   ctx.margin=120.0;
   ctx.exposure=10.0;
   ctx.net_delta=book.Delta();

   CALCompressionEngine c;
   c.SetAlpha(0.5);
   c.SetTriggerLevels(1);
   if(!c.ProcessCompression(book,ctx,10000.0,false)) return false;

   const double after=book.PnLAtPrice(1.1,1.0);
   // PnL is not fixed externally; it is redistributed proportionally in structure.
   if(MathAbs(after-before*0.5)>1e-12) return false;
   return true;
}

#endif
