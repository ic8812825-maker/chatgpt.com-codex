#ifndef __CALDRAWDOWNMODEL_MQH__
#define __CALDRAWDOWNMODEL_MQH__

class CALDrawdownModel
{
public:
   double Drawdown(const double peak,const double equity) const
   {
      if(peak<=0.0) return 0.0;
      const double dd=(peak-equity)/peak;
      return MathMax(0.0,dd);
   }
};

#endif
