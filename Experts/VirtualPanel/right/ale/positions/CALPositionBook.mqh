#ifndef __CALPOSITIONBOOK_MQH__
#define __CALPOSITIONBOOK_MQH__

#include "CALVirtualPosition.mqh"
#include "..\\core\\CALContext.mqh"

// ALE-side runtime invariants for virtual books (P0 safety layer).
// Example:
//   CALPositionBook book;
//   book.Init(ALE_FLOW_BUY);
//   book.SetLimits(256,0.01);
//   book.SetStrictRuntimeChecks(true);
//   book.Add(1.1000,0.10);
//   book.Edit(0,1.1010,0.20);
class CALPositionBook
{
private:
   CALVirtualPosition m_positions[];
   int m_direction;
   int m_max_positions;
   double m_min_lot;
   bool m_strict_runtime_checks;

   bool IsDirectionValid(const int direction) const
   {
      return (direction==ALE_FLOW_BUY || direction==ALE_FLOW_SELL);
   }

   bool CheckInvariants(const string op_name) const
   {
      if(!m_strict_runtime_checks)
         return true;

      if(!IsDirectionValid(m_direction))
      {
         PrintFormat("[ALE][BOOK][INVARIANT] %s failed: invalid direction=%d",op_name,m_direction);
         return false;
      }

      const int n=ArraySize(m_positions);
      if(n<0 || n>m_max_positions)
      {
         PrintFormat("[ALE][BOOK][INVARIANT] %s failed: positions=%d max=%d",op_name,n,m_max_positions);
         return false;
      }

      for(int i=0;i<n;i++)
      {
         if(!MathIsValidNumber(m_positions[i].price) || m_positions[i].price<=0.0)
         {
            PrintFormat("[ALE][BOOK][INVARIANT] %s failed: bad price idx=%d value=%.10f",op_name,i,m_positions[i].price);
            return false;
         }

         if(!MathIsValidNumber(m_positions[i].lot) || m_positions[i].lot<m_min_lot)
         {
            PrintFormat("[ALE][BOOK][INVARIANT] %s failed: bad lot idx=%d value=%.10f min=%.10f",op_name,i,m_positions[i].lot,m_min_lot);
            return false;
         }

         if(!IsDirectionValid(m_positions[i].direction))
         {
            PrintFormat("[ALE][BOOK][INVARIANT] %s failed: bad position direction idx=%d dir=%d",op_name,i,m_positions[i].direction);
            return false;
         }
      }

      return true;
   }

public:
   void Init(const int direction)
   {
      m_direction=direction;
      m_max_positions=256;
      m_min_lot=0.01;
      m_strict_runtime_checks=true;
      ArrayResize(m_positions,0);
   }

   void SetLimits(const int max_positions,const double min_lot)
   {
      if(max_positions>0) m_max_positions=max_positions;
      if(min_lot>0.0) m_min_lot=min_lot;
   }

   void SetStrictRuntimeChecks(const bool enabled)
   {
      m_strict_runtime_checks=enabled;
   }

   bool Add(const double price,const double lot)
   {
      if(!MathIsValidNumber(price) || !MathIsValidNumber(lot) || price<=0.0 || lot<m_min_lot)
         return false;

      const int n=ArraySize(m_positions);
      if(n>=m_max_positions)
      {
         PrintFormat("[ALE][BOOK] Add rejected: positions=%d max=%d",n,m_max_positions);
         return false;
      }

      ArrayResize(m_positions,n+1);
      m_positions[n].Init(price,lot,m_direction);

      if(CheckInvariants("Add"))
         return true;

      // safe rollback
      ArrayResize(m_positions,n);
      return false;
   }

   bool Edit(const int index,const double price,const double lot)
   {
      const int n=ArraySize(m_positions);
      if(index<0 || index>=n) return false;
      if(!MathIsValidNumber(price) || !MathIsValidNumber(lot) || price<=0.0 || lot<m_min_lot)
         return false;

      const CALVirtualPosition backup=m_positions[index];
      m_positions[index].Init(price,lot,m_direction);
      if(CheckInvariants("Edit"))
         return true;

      // safe rollback
      m_positions[index]=backup;
      return false;
   }

   bool Remove(const int index)
   {
      const int n=ArraySize(m_positions);
      if(index<0 || index>=n) return false;

      CALVirtualPosition backup[];
      ArrayResize(backup,n);
      for(int i=0;i<n;i++) backup[i]=m_positions[i];

      for(int j=index;j<n-1;j++)
         m_positions[j]=m_positions[j+1];
      ArrayResize(m_positions,n-1);

      if(CheckInvariants("Remove"))
         return true;

      // safe rollback
      ArrayResize(m_positions,n);
      for(int k=0;k<n;k++) m_positions[k]=backup[k];
      return false;
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
      double d=0.0;
      for(int i=0;i<ArraySize(m_positions);i++) d+=m_positions[i].lot*m_positions[i].direction;
      return d;
   }
};

#endif
