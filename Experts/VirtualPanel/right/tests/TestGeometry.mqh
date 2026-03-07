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

   // I5 symmetry
   const double center=1.1000;
   for(int i=0;i<4;i++)
   {
      const double d_buy=buy_grid.levels[i]-center;
      const double d_sell=sell_grid.levels[i]-center;
      if(!NearEq(d_buy,-d_sell,1e-8)) return false;
   }

   // step consistency
   if(!NearEq(buy_grid.levels[1]-buy_grid.levels[0],buy_grid.levels[2]-buy_grid.levels[1],1e-12)) return false;

   // log geometry growth
   CALLogGeometry log_geo;
   CALGrid log_grid;
   log_geo.SetBase(1.5);
   log_geo.BuildGrid(ALE_FLOW_BUY,center,3,log_grid);
   if(!(log_grid.levels[2]-center > log_grid.levels[1]-center)) return false;

   return true;
}

bool TestGeometry_LogGridMonotonicity()
{
   CALLogGeometry log_geo;
   log_geo.SetBase(1.3);

   CALGrid buy_grid;
   log_geo.BuildGrid(ALE_FLOW_BUY,1.2000,5,buy_grid);
   if(ArraySize(buy_grid.levels)!=5) return false;
   for(int i=1;i<ArraySize(buy_grid.levels);i++)
      if(!(buy_grid.levels[i]>buy_grid.levels[i-1])) return false;

   CALGrid sell_grid;
   log_geo.BuildGrid(ALE_FLOW_SELL,1.2000,5,sell_grid);
   if(ArraySize(sell_grid.levels)!=5) return false;
   for(int j=1;j<ArraySize(sell_grid.levels);j++)
      if(!(sell_grid.levels[j]<sell_grid.levels[j-1])) return false;

   return true;
}

#endif
