#ifndef __CALENGINECOMMON_MQH__
#define __CALENGINECOMMON_MQH__

#include "CALContext.mqh"
#include "CALStateMachine.mqh"
#include "..\\config\\CALRiskConfig.mqh"

// Common brain that aggregates BUY+SELL and computes global SAFE/FSM.
class CALEngineCommon
{
private:
   CALCommonContext m_common;
   CALStateMachine m_fsm;
   CALRiskConfig m_cfg;

public:
   void Init()
   {
      m_common.Reset();
      m_fsm.Reset();
      m_cfg.SetDefaults();
   }

   void SetRiskConfig(const CALRiskConfig &cfg)
   {
      m_cfg=cfg;
      m_cfg.SyncAliases();
   }

   void Aggregate(const CALStreamContext &buy,const CALStreamContext &sell)
   {
      m_common.net_delta=buy.net_delta+sell.net_delta;
      m_common.pnl=buy.pnl+sell.pnl;
      m_common.exposure=buy.exposure+sell.exposure;
      m_common.margin=buy.margin+sell.margin;
      m_common.worst_dd=buy.worst_dd+sell.worst_dd;

      const bool local_safe=(buy.safe_active || sell.safe_active);
      const bool margin_safe=(m_common.margin>m_cfg.GLOBAL_MARGIN_LIMIT);
      const bool dd_safe=(m_common.worst_dd>m_cfg.GLOBAL_DD_SUM_LIMIT);
      m_common.safe_active=(local_safe || margin_safe || dd_safe);

      ENUM_ALE_SIGNAL signal=ALE_SIGNAL_PRICE_MOVE;
      if(m_common.safe_active) signal=ALE_SIGNAL_SAFE_TRIGGERED;
      else if(m_common.worst_dd>m_cfg.MAX_DRAWDOWN) signal=ALE_SIGNAL_DRAWDOWN_EXCEEDED;
      else if(m_common.pnl>0.0) signal=ALE_SIGNAL_HARVEST_REACHED;

      m_common.state=m_fsm.TransitionBySignal(signal);
   }

   CALCommonContext Context() const { return m_common; }
   ENUM_ALE_STATE State() const { return m_common.state; }
   bool IsSAFE() const { return m_common.safe_active; }

   CALEngineCommon(){ Init(); }
};

#endif
