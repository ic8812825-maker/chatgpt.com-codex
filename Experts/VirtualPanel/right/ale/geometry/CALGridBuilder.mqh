#ifndef __CALGRIDBUILDER_MQH__
#define __CALGRIDBUILDER_MQH__

#include "CALFixedStep.mqh"

class CALGridBuilder
{
private:
   IALGeometry *m_geometry;
public:
   CALGridBuilder(){ m_geometry=NULL; }
   void SetGeometry(IALGeometry &geometry){ m_geometry=&geometry; }
   bool BuildGrid(const int direction,const double center,const int levels,CALGrid &out_grid)
   {
      if(m_geometry==NULL || levels<=0) return false;
      m_geometry.BuildGrid(direction,center,levels,out_grid);
      return true;
   }
};

#endif
