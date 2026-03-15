#ifndef __CALPOSITIONBOOK_MQH__
#define __CALPOSITIONBOOK_MQH__

#include "CALVirtualPosition.mqh"

class CALPositionBook
{
private:
   CALVirtualPosition m_positions[];
   int m_direction;
public:
   void Init(const int direction){ m_direction=direction; ArrayResize(m_positions,0); }

   bool Add(const double price,const double lot)
   {
      if(price<=0.0 || lot<=0.0 || !MathIsValidNumber(price) || !MathIsValidNumber(lot))
         return false;
      const int n=ArraySize(m_positions);
      ArrayResize(m_positions,n+1);
      m_positions[n].Init(price,lot,m_direction);
      return true;
   }

   void Recalc(const double bid,const double ask,const double contract_size)
   {
      for(int i=0;i<ArraySize(m_positions);i++)
         m_positions[i].UpdatePnL(bid,ask,contract_size);
   }

   int Size() const { return ArraySize(m_positions); }

   double TotalPnL() const
   {
      double s=0.0;
      for(int i=0;i<ArraySize(m_positions);i++) s+=m_positions[i].pnl;
      return s;
   }

   double TotalLot() const
   {
      double s=0.0;
      for(int i=0;i<ArraySize(m_positions);i++) s+=m_positions[i].lot;
      return s;
   }

   double TotalAbsLot() const
   {
      double s=0.0;
      for(int i=0;i<ArraySize(m_positions);i++) s+=MathAbs(m_positions[i].lot);
      return s;
   }

   bool ScaleLots(const double alpha)
   {
      if(alpha<=0.0 || alpha>1.0)
         return(false);
      const int n=ArraySize(m_positions);
      if(n<=0)
         return(false);

      for(int i=0;i<n;i++)
         m_positions[i].lot=MathMax(0.0,m_positions[i].lot*alpha);
      return(true);
   }

   bool TrimTail(const int count)
   {
      if(count<=0)
         return(false);
      const int n=ArraySize(m_positions);
      if(n<=0)
         return(false);

      const int keep=MathMax(0,n-count);
      ArrayResize(m_positions,keep);
      return(true);
   }

   bool RebuildGeometryLots(const double k,const double eps)
   {
      const int n=ArraySize(m_positions);
      if(n<=0 || k<=0.0)
         return(false);

      const double total=TotalAbsLot();
      if(total<=eps)
         return(false);

      double l0=0.0;
      if(MathAbs(k-1.0)<=eps)
         l0=total/(double)n;
      else
      {
         const double denom=(MathPow(k,n)-1.0)/(k-1.0);
         if(MathAbs(denom)<=eps)
            return(false);
         l0=total/denom;
      }

      for(int i=0;i<n;i++)
      {
         const double li=l0*MathPow(k,i);
         m_positions[i].lot=MathMax(0.0,li);
      }
      return(true);
   }

   bool IsGeometryPreserved(const double k,const double eps) const
   {
      const int n=ArraySize(m_positions);
      if(n<=1 || k<=0.0)
         return(true);

      const double l0=m_positions[0].lot;
      for(int i=0;i<n;i++)
      {
         const double expected=l0*MathPow(k,i);
         if(MathAbs(m_positions[i].lot-expected)>eps)
            return(false);
      }
      return(true);
   }

   double EffectiveDelta() const
   {
      double d=0.0;
      for(int i=0;i<ArraySize(m_positions);i++)
         d+=m_positions[i].lot*m_positions[i].direction;
      return(d);
   }

   void GetLots(double &out_lots[]) const
   {
      const int n=ArraySize(m_positions);
      ArrayResize(out_lots,n);
      for(int i=0;i<n;i++)
         out_lots[i]=m_positions[i].lot;
   }

   double PnLAtPrice(const double p,const double contract_size) const
   {
      double s=0.0;
      for(int i=0;i<ArraySize(m_positions);i++)
      {
         const CALVirtualPosition &v=m_positions[i];
         s += v.lot*v.direction*(p-v.price)*contract_size;
      }
      return s;
   }

   double Delta() const
   {
      return EffectiveDelta();
   }
};

#endif
