#ifndef __IALGEOMETRY_MQH__
#define __IALGEOMETRY_MQH__

struct CALGrid
{
   double levels[];
   double lots[];
};

class IALGeometry
{
public:
   virtual void BuildGrid(const int direction,const double center,const int levels,CALGrid &out_grid)=0;
   virtual double LevelPrice(const int index,const CALGrid &grid) const=0;
   virtual double Lot(const int index,const CALGrid &grid) const=0;
};

#endif
