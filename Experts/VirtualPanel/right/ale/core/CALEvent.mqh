#ifndef __CALEVENT_MQH__
#define __CALEVENT_MQH__

#include "CALContext.mqh"

enum ENUM_ALE_EVENT_TYPE
{
   ALE_EVENT_NONE=0,
   ALE_EVENT_STATE_CHANGE_BUY=1,
   ALE_EVENT_STATE_CHANGE_SELL=2,
   ALE_EVENT_DRAWDOWN_EXCEEDED=3,
   ALE_EVENT_SAFE_TRIGGERED=4
};

class CALEvent
{
private:
   ENUM_ALE_EVENT_TYPE m_type;
   ENUM_ALE_STATE m_from_state;
   ENUM_ALE_STATE m_to_state;
   string m_message;
public:
   void Reset(){ m_type=ALE_EVENT_NONE; m_from_state=ALE_STATE_IDLE; m_to_state=ALE_STATE_IDLE; m_message=""; }
   void OnStateChangeBuy(const ENUM_ALE_STATE from_state,const ENUM_ALE_STATE to_state){ m_type=ALE_EVENT_STATE_CHANGE_BUY; m_from_state=from_state; m_to_state=to_state; m_message="BUY state changed"; }
   void OnStateChangeSell(const ENUM_ALE_STATE from_state,const ENUM_ALE_STATE to_state){ m_type=ALE_EVENT_STATE_CHANGE_SELL; m_from_state=from_state; m_to_state=to_state; m_message="SELL state changed"; }
   void OnDrawdownExceeded(){ m_type=ALE_EVENT_DRAWDOWN_EXCEEDED; m_message="Drawdown exceeded"; }
   void OnSAFETriggered(){ m_type=ALE_EVENT_SAFE_TRIGGERED; m_message="SAFE triggered"; }
   ENUM_ALE_EVENT_TYPE Type() const { return m_type; }
   ENUM_ALE_STATE FromState() const { return m_from_state; }
   ENUM_ALE_STATE ToState() const { return m_to_state; }
   string Message() const { return m_message; }
   CALEvent(){ Reset(); }
};

#endif
