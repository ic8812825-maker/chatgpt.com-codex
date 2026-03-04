#ifndef __TESTGEOMETRY_MQH__
#define __TESTGEOMETRY_MQH__

#include "..\\ale\\core\\CALEngine.mqh"
#include "..\\ale\\geometry\\CALLogGeometry.mqh"

bool NearEq(const double a,const double b,const double eps=1e-9){ return MathAbs(a-b)<=eps; }

bool TestGeometry_BuySellGrids()
{
   CALEngine ale;
   CALGrid buy_grid;
   CALGrid sell_grid;

   if(!ale.BuildGrid(ALE_FLOW_BUY,1.1000,4,buy_grid)) return false;
   if(!ale.BuildGrid(ALE_FLOW_SELL,1.1000,4,sell_grid)) return false;

   if(ArraySize(buy_grid.levels)!=4 || ArraySize(sell_grid.levels)!=4) return false;

   // I5 symmetry around center for fixed-step mirror geometry.
   const double center=1.1000;
   for(int i=0;i<4;i++)
   {
      const double d_buy=buy_grid.levels[i]-center;
      const double d_sell=sell_grid.levels[i]-center;
      if(!NearEq(d_buy,-d_sell,1e-8)) return false;
   }

   // step-R check
   if(!NearEq(buy_grid.levels[1]-buy_grid.levels[0],buy_grid.levels[2]-buy_grid.levels[1],1e-12)) return false;

   // log-geometry check
   CALLogGeometry log_geo;
   CALGrid log_grid;
   log_geo.SetBase(1.5);
   log_geo.BuildGrid(ALE_FLOW_BUY,center,3,log_grid);
   if(!(log_grid.levels[2]-center > log_grid.levels[1]-center)) return false;

   return true;
}

#endif
