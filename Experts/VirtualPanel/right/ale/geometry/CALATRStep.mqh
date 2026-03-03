#ifndef __CALATRSTEP_MQH__
#define __CALATRSTEP_MQH__

#include "CALGeometryBase.mqh"

class CALATRStep : public CALGeometryBase
{
private:
   double m_atr;
public:
   CALATRStep(){ m_atr=0.0; m_step=100*_Point; }
   void SetATR(const double atr){ m_atr=atr; m_step=(atr>0.0?atr:100*_Point); }
   virtual void BuildGrid(const int direction,const double center,const int levels,CALGrid &out_grid)
   {
      const double step=(m_atr>0.0?m_atr:m_step);
      ArrayResize(out_grid.levels,levels);
      ArrayResize(out_grid.lots,levels);
      for(int i=0;i<levels;i++)
      {
         out_grid.levels[i]=center + direction*step*(i+1);
         out_grid.lots[i]=0.01*(1.0+0.5*i);
      }
   }
};

#endif
