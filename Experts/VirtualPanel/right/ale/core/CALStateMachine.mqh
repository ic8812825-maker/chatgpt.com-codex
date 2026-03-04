#ifndef __CALSTATEMACHINE_MQH__
#define __CALSTATEMACHINE_MQH__

#include "CALContext.mqh"
#include "..\\interfaces\\IFSM.mqh"

enum ENUM_ALE_SIGNAL
{
   ALE_SIGNAL_NONE=0,
   ALE_SIGNAL_PRICE_MOVE=1,
   ALE_SIGNAL_DRAWDOWN_EXCEEDED=2,
   ALE_SIGNAL_HARVEST_REACHED=3,
   ALE_SIGNAL_SAFE_TRIGGERED=4,
   ALE_SIGNAL_RESET_REQUESTED=5
};

class CALStateMachine : public IFSM
{
private:
   ENUM_ALE_STATE m_state;
public:
   void Reset(){ m_state=ALE_STATE_IDLE; }
   virtual ENUM_ALE_STATE Current() const { return m_state; }

   virtual bool Transition(const ENUM_ALE_STATE next_state)
   {
      if(m_state==ALE_STATE_SAFE && next_state==ALE_STATE_EXPANSION)
         return false;

      if(m_state==ALE_STATE_IDLE && next_state==ALE_STATE_BASE) { m_state=next_state; return true; }
      if(m_state==ALE_STATE_BASE && (next_state==ALE_STATE_EXPANSION || next_state==ALE_STATE_HARVEST || next_state==ALE_STATE_SAFE)) { m_state=next_state; return true; }
      if(m_state==ALE_STATE_EXPANSION && (next_state==ALE_STATE_HARVEST || next_state==ALE_STATE_RESET || next_state==ALE_STATE_SAFE)) { m_state=next_state; return true; }
      if(m_state==ALE_STATE_HARVEST && (next_state==ALE_STATE_RESET || next_state==ALE_STATE_SAFE)) { m_state=next_state; return true; }
      if(m_state==ALE_STATE_RESET && (next_state==ALE_STATE_IDLE || next_state==ALE_STATE_SAFE)) { m_state=next_state; return true; }
      if(next_state==ALE_STATE_SAFE) { m_state=next_state; return true; }
      return false;
   }

   ENUM_ALE_STATE TransitionBySignal(const ENUM_ALE_SIGNAL signal)
   {
      if(signal==ALE_SIGNAL_SAFE_TRIGGERED) { Transition(ALE_STATE_SAFE); return m_state; }
      if(signal==ALE_SIGNAL_DRAWDOWN_EXCEEDED || signal==ALE_SIGNAL_RESET_REQUESTED) { Transition(ALE_STATE_RESET); return m_state; }
      if(signal==ALE_SIGNAL_HARVEST_REACHED) { Transition(ALE_STATE_HARVEST); return m_state; }
      if(signal==ALE_SIGNAL_PRICE_MOVE)
      {
         if(m_state==ALE_STATE_IDLE) Transition(ALE_STATE_BASE);
         else if(m_state==ALE_STATE_BASE) Transition(ALE_STATE_EXPANSION);
      }
      return m_state;
   }

   CALStateMachine(){ Reset(); }
};

#endif
