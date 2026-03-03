#ifndef __TESTGEOMETRY_MQH__
#define __TESTGEOMETRY_MQH__

#include "..\\ale\\core\\CALEngine.mqh"

bool TestGeometry_BuySellGrids()
{
   CALEngine ale;
   CALGrid buy_grid;
   CALGrid sell_grid;
   if(!ale.BuildGrid(ALE_FLOW_BUY,1.1000,4,buy_grid)) return false;
   if(!ale.BuildGrid(ALE_FLOW_SELL,1.1000,4,sell_grid)) return false;
   if(ArraySize(buy_grid.levels)!=4 || ArraySize(sell_grid.levels)!=4) return false;
   if(!(buy_grid.levels[0]>1.1000)) return false;
   if(!(sell_grid.levels[0]<1.1000)) return false;
   return true;
}

#endif
