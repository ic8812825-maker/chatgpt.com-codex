#ifndef __CALLOGGEOMETRY_MQH__
#define __CALLOGGEOMETRY_MQH__

#include "CALGeometryBase.mqh"

class CALLogGeometry : public CALGeometryBase
{
private:
   double m_base;
public:
   CALLogGeometry(){ m_base=1.2; m_step=50*_Point; }
   void SetBase(const double base){ m_base=(base>1.0?base:1.2); }
   virtual void BuildGrid(const int direction,const double center,const int levels,CALGrid &out_grid)
   {
      ArrayResize(out_grid.levels,levels);
      ArrayResize(out_grid.lots,levels);
      for(int i=0;i<levels;i++)
      {
         const double dist=m_step*(MathPow(m_base,i+1)-1.0);
         out_grid.levels[i]=center + direction*dist;
         out_grid.lots[i]=0.01*MathPow(m_base,0.5*i);
      }
   }
};

#endif
