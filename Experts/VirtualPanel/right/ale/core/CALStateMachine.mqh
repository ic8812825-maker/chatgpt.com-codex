#ifndef __CALSTATEMACHINE_MQH__
#define __CALSTATEMACHINE_MQH__

#include "CALContext.mqh"

class CALStateMachine
{
private:
   ENUM_ALE_STATE m_state;
public:
   void Reset(){ m_state=ALE_STATE_IDLE; }
   ENUM_ALE_STATE State() const { return m_state; }
   ENUM_ALE_STATE Next(const double pnl,const double drawdown,const bool safe_trigger)
   {
      if(safe_trigger) { m_state=ALE_STATE_SAFE; return m_state; }
      if(drawdown>0.0 && drawdown>MathAbs(pnl)*0.5) { m_state=ALE_STATE_RESET; return m_state; }
      if(MathAbs(pnl)<0.0000001) m_state=ALE_STATE_BASE;
      else if(pnl<0.0) m_state=ALE_STATE_EXPANSION;
      else m_state=ALE_STATE_HARVEST;
      return m_state;
   }
   CALStateMachine(){ Reset(); }
};

#endif
