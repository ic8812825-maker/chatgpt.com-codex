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

   void Update(CALContext &ctx,const bool safe_trigger)
   {
      if(safe_trigger)
      {
         m_state=ALE_STATE_SAFE;
         ctx.state=m_state;
         return;
      }

      if(ctx.drawdown>0.25)
      {
         m_state=ALE_STATE_RESET;
      }
      else if(MathAbs(ctx.pnl)<0.0000001)
      {
         m_state=ALE_STATE_BASE;
      }
      else if(ctx.pnl<0.0)
      {
         m_state=ALE_STATE_EXPANSION;
      }
      else
      {
         m_state=ALE_STATE_HARVEST;
      }

      ctx.state=m_state;
   }

   CALStateMachine(){ Reset(); }
};

#endif
