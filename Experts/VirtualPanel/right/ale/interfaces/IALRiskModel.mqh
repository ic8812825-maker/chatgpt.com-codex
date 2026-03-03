#ifndef __IALRISKMODEL_MQH__
#define __IALRISKMODEL_MQH__

class IALRiskModel
{
public:
   virtual double CalculateDD(const double pnl,const double peak) const=0;
   virtual bool SAFE(const double drawdown,const double limit) const=0;
};

#endif
