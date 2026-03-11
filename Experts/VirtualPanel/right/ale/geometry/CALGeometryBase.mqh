#ifndef __CALGEOMETRYBASE_MQH__
#define __CALGEOMETRYBASE_MQH__

#include "..\interfaces\IALGeometry.mqh"

class CALGeometryBase : public IALGeometry
{
protected:
   double m_step;
public:
   CALGeometryBase(){ m_step=0.0; }
   void SetStep(const double step){ m_step=step; }
   virtual double LevelPrice(const int index,const CALGrid &grid) const
   {
      if(index<0 || index>=ArraySize(grid.levels)) return 0.0;
      return grid.levels[index];
   }
   virtual double Lot(const int index,const CALGrid &grid) const
   {
      if(index<0 || index>=ArraySize(grid.lots)) return 0.0;
      return grid.lots[index];
   }
};

#endif
