#ifndef __TESTGEOMETRYPRESERVATION_MQH__
#define __TESTGEOMETRYPRESERVATION_MQH__

#include "..\\ale\\positions\\CALPositionBook.mqh"

bool TestGeometryPreservation_Run()
{
   CALPositionBook book;
   book.Init(ALE_FLOW_BUY);
   book.Add(1.0,0.01);
   book.Add(1.01,0.013);
   book.Add(1.02,0.017);
   book.Add(1.03,0.022);

   if(!book.ScaleLots(0.5)) return false;
   if(!book.RebuildGeometryLots(1.3,1e-12)) return false;
   if(!book.IsGeometryPreserved(1.3,1e-9)) return false;
   return true;
}

#endif
