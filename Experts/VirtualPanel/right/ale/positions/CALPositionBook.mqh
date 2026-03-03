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
      const int n=ArraySize(m_positions);
      ArrayResize(m_positions,n+1);
      m_positions[n].Init(price,lot,m_direction);
      return true;
   }
   void Recalc(const double bid,const double ask,const double contract_size)
   {
      for(int i=0;i<ArraySize(m_positions);i++) m_positions[i].UpdatePnL(bid,ask,contract_size);
   }
   int Size() const { return ArraySize(m_positions); }
   double TotalPnL() const { double s=0.0; for(int i=0;i<ArraySize(m_positions);i++) s+=m_positions[i].pnl; return s; }
   double TotalLot() const { double s=0.0; for(int i=0;i<ArraySize(m_positions);i++) s+=m_positions[i].lot; return s; }
};

#endif
