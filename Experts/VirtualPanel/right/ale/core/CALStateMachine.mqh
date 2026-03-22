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
   ALE_SIGNAL_RESET_REQUESTED=5,
   ALE_SIGNAL_COMPRESSION=6,
   ALE_SIGNAL_LYAPUNOV_GUARD=7,
   ALE_SIGNAL_LYAPUNOV_CRITICAL=8
};

class CALStateMachine : public IFSM
{
private:
   ENUM_ALE_STATE m_state;

   bool IsAllowed(const ENUM_ALE_STATE from_state,const ENUM_ALE_STATE to_state) const
   {
      bool allowed[7][7];
      for(int i=0;i<7;i++) for(int j=0;j<7;j++) allowed[i][j]=false;

      allowed[ALE_STATE_IDLE][ALE_STATE_BASE]=true;
      allowed[ALE_STATE_BASE][ALE_STATE_EXPANSION]=true;
      allowed[ALE_STATE_BASE][ALE_STATE_HARVEST]=true;
      allowed[ALE_STATE_BASE][ALE_STATE_COMPRESSION]=true;
      allowed[ALE_STATE_EXPANSION][ALE_STATE_HARVEST]=true;
      allowed[ALE_STATE_EXPANSION][ALE_STATE_COMPRESSION]=true;
      allowed[ALE_STATE_EXPANSION][ALE_STATE_RESET]=true;
      allowed[ALE_STATE_HARVEST][ALE_STATE_RESET]=true;
      allowed[ALE_STATE_HARVEST][ALE_STATE_COMPRESSION]=true;
      allowed[ALE_STATE_COMPRESSION][ALE_STATE_EXPANSION]=true;
      allowed[ALE_STATE_COMPRESSION][ALE_STATE_HARVEST]=true;
      allowed[ALE_STATE_COMPRESSION][ALE_STATE_RESET]=true;
      allowed[ALE_STATE_RESET][ALE_STATE_BASE]=true;

      for(int s=0;s<7;s++) allowed[s][ALE_STATE_SAFE]=true;
      return allowed[from_state][to_state];
   }

public:
   void Reset(){ m_state=ALE_STATE_IDLE; }
   virtual ENUM_ALE_STATE Current() const { return m_state; }

   virtual bool Transition(const ENUM_ALE_STATE next_state)
   {
      if(m_state==ALE_STATE_SAFE && next_state!=ALE_STATE_RESET)
         return false;

      if(!IsAllowed(m_state,next_state))
      {
         m_state=ALE_STATE_SAFE;
         return false;
      }

      m_state=next_state;
      return true;
   }

   ENUM_ALE_STATE TransitionBySignal(const ENUM_ALE_SIGNAL signal)
   {
      if(signal==ALE_SIGNAL_SAFE_TRIGGERED || signal==ALE_SIGNAL_LYAPUNOV_CRITICAL) { Transition(ALE_STATE_SAFE); return m_state; }
      if(signal==ALE_SIGNAL_DRAWDOWN_EXCEEDED || signal==ALE_SIGNAL_RESET_REQUESTED) { Transition(ALE_STATE_RESET); return m_state; }
      if(signal==ALE_SIGNAL_HARVEST_REACHED) { Transition(ALE_STATE_HARVEST); return m_state; }
      if(signal==ALE_SIGNAL_COMPRESSION || signal==ALE_SIGNAL_LYAPUNOV_GUARD) { Transition(ALE_STATE_COMPRESSION); return m_state; }

      if(signal==ALE_SIGNAL_PRICE_MOVE)
      {
         if(m_state==ALE_STATE_SAFE) return m_state;
         if(m_state==ALE_STATE_IDLE) Transition(ALE_STATE_BASE);
         else if(m_state==ALE_STATE_BASE || m_state==ALE_STATE_COMPRESSION) Transition(ALE_STATE_EXPANSION);
      }
      return m_state;
   }

   CALStateMachine(){ Reset(); }
};

#endif
