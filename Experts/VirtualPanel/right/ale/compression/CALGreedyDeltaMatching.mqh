#ifndef __CALGREEDYDELTAMATCHING_MQH__
#define __CALGREEDYDELTAMATCHING_MQH__

struct CLockPair
{
   int buy_index;
   int sell_index;
   double lot;
};

class CALGreedyDeltaMatching
{
private:
   void SortDesc(double &lots[],int &idx[]) const
   {
      const int n=ArraySize(lots);
      for(int i=0;i<n;i++) idx[i]=i;
      for(int i=0;i<n;i++)
         for(int j=i+1;j<n;j++)
            if(lots[j]>lots[i])
            {
               const double t=lots[i]; lots[i]=lots[j]; lots[j]=t;
               const int ti=idx[i]; idx[i]=idx[j]; idx[j]=ti;
            }
   }

public:
   double CalculateEffectiveDelta(const double &buy_lots[],const double &sell_lots[]) const
   {
      double b=0.0,s=0.0;
      for(int i=0;i<ArraySize(buy_lots);i++) b+=MathAbs(buy_lots[i]);
      for(int j=0;j<ArraySize(sell_lots);j++) s+=MathAbs(sell_lots[j]);
      return b-s;
   }

   bool Match(const double &buy_in[],const double &sell_in[],CLockPair &pairs[],double &delta_before,double &delta_after) const
   {
      double buy[]; double sell[];
      const int nb=ArraySize(buy_in), ns=ArraySize(sell_in);
      ArrayResize(buy,nb); ArrayResize(sell,ns);
      int bi[]; int si[];
      ArrayResize(bi,nb); ArrayResize(si,ns);

      for(int i=0;i<nb;i++) buy[i]=MathAbs(buy_in[i]);
      for(int j=0;j<ns;j++) sell[j]=MathAbs(sell_in[j]);

      delta_before=CalculateEffectiveDelta(buy,sell);
      SortDesc(buy,bi);
      SortDesc(sell,si);

      ArrayResize(pairs,0);
      int i=0,j=0;
      while(i<nb && j<ns)
      {
         if(buy[i]<=1e-12){ i++; continue; }
         if(sell[j]<=1e-12){ j++; continue; }

         const double L=MathMin(buy[i],sell[j]);
         const int n=ArraySize(pairs);
         ArrayResize(pairs,n+1);
         pairs[n].buy_index=bi[i];
         pairs[n].sell_index=si[j];
         pairs[n].lot=L;

         buy[i]-=L;
         sell[j]-=L;

         if(buy[i]<=1e-12) i++;
         if(sell[j]<=1e-12) j++;
      }

      delta_after=CalculateEffectiveDelta(buy,sell);
      return(true);
   }
};

#endif
