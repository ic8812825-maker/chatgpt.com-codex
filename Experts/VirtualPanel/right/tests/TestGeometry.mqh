#ifndef __TESTGEOMETRY_MQH__
#define __TESTGEOMETRY_MQH__

#include "..\\ale\\core\\CALEngine.mqh"
#include "..\\ale\\geometry\\CALATRStep.mqh"

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

   const double buy_step=buy_grid.levels[1]-buy_grid.levels[0];
   const double sell_step=sell_grid.levels[0]-sell_grid.levels[1];
   if(MathAbs(buy_step-sell_step)>1e-10) return false;

   CALATRStep atr_geo;
   CALGrid atr_grid;
   atr_geo.SetATR(0.0015);
   atr_geo.BuildGrid(ALE_FLOW_BUY,1.1000,3,atr_grid);
   if(ArraySize(atr_grid.levels)!=3) return false;
   if(!(atr_grid.levels[0]>1.1000)) return false;

   return true;
}

#endif
