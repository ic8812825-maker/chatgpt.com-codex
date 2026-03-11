#ifndef __CALLOTMODEL_MQH__
#define __CALLOTMODEL_MQH__

class CALLotModel
{
private:
   bool IsAlphaSafe(const double alpha) const
   {
      return (alpha>=0.5 && alpha<=0.85);
   }

public:
   double LotAtLevel(const int level,const double base_lot,const double alpha) const
   {
      if(level<0 || base_lot<=0.0 || !IsAlphaSafe(alpha)) return -1.0;
      return base_lot*MathPow(alpha,level);
   }

   double CumulativeMaxVolume(const double base_lot,const double alpha) const
   {
      if(base_lot<=0.0 || !IsAlphaSafe(alpha)) return -1.0;
      return base_lot/(1.0-alpha);
   }

   bool CanAddLevel(const double current_cum,const int next_level,const double base_lot,const double alpha) const
   {
      const double next_lot=LotAtLevel(next_level,base_lot,alpha);
      const double vmax=CumulativeMaxVolume(base_lot,alpha);
      if(next_lot<=0.0 || vmax<=0.0) return false;
      return (current_cum + next_lot)<=vmax;
   }

   double HedgeLot(const double l0,const double k,const double max_safe_volume) const
   {
      if(l0<=0.0 || k<=0.0 || max_safe_volume<=0.0) return 0.0;
      return MathMin(l0*k,max_safe_volume);
   }

   double LotForBuyLevel(const int level,const double base_lot,const double alpha=0.8) const
   {
      return LotAtLevel(level,base_lot,alpha);
   }

   double LotForSellLevel(const int level,const double base_lot,const double alpha=0.8) const
   {
      return LotAtLevel(level,base_lot,alpha);
   }
};

#endif
