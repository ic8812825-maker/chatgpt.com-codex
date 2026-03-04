#ifndef __CALSTATEMACHINE_MQH__
#define __CALSTATEMACHINE_MQH__

#include "CALContext.mqh"

enum ENUM_ALE_SIGNAL
{
   ALE_SIGNAL_NONE=0,
   ALE_SIGNAL_PRICE_MOVE=1,
   ALE_SIGNAL_DRAWDOWN_EXCEEDED=2,
   ALE_SIGNAL_HARVEST_REACHED=3,
   ALE_SIGNAL_SAFE_TRIGGERED=4
};

class CALStateMachine
{
private:
   ENUM_ALE_STATE m_state;
public:
   void Reset(){ m_state=ALE_STATE_IDLE; }
   ENUM_ALE_STATE State() const { return m_state; }

   ENUM_ALE_STATE Transition(const ENUM_ALE_SIGNAL signal)
   {
      if(signal==ALE_SIGNAL_SAFE_TRIGGERED)
      {
         m_state=ALE_STATE_SAFE;
         return m_state;
      }

      if(signal==ALE_SIGNAL_DRAWDOWN_EXCEEDED)
      {
         m_state=ALE_STATE_RESET;
         return m_state;
      }

      if(signal==ALE_SIGNAL_HARVEST_REACHED)
      {
         m_state=ALE_STATE_HARVEST;
         return m_state;
      }

      if(signal==ALE_SIGNAL_PRICE_MOVE)
      {
         if(m_state==ALE_STATE_IDLE)
            m_state=ALE_STATE_BASE;
         else if(m_state==ALE_STATE_BASE)
            m_state=ALE_STATE_EXPANSION;
      }

      return m_state;
   }

   CALStateMachine(){ Reset(); }
};

#endif
