#ifndef __CALFIXEDSTEP_MQH__
#define __CALFIXEDSTEP_MQH__

#include "CALGeometryBase.mqh"

class CALFixedStep : public CALGeometryBase
{
public:
   CALFixedStep(const double step=100*_Point){ m_step=step; }
   virtual void BuildGrid(const int direction,const double center,const int levels,CALGrid &out_grid)
   {
      ArrayResize(out_grid.levels,levels);
      ArrayResize(out_grid.lots,levels);
      for(int i=0;i<levels;i++)
      {
         out_grid.levels[i]=center + direction*m_step*(i+1);
         out_grid.lots[i]=0.01*(i+1);
      }
   }
};

#endif
