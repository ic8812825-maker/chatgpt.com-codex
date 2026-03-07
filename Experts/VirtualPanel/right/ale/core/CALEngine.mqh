#ifndef __CALENGINE_MQH__
#define __CALENGINE_MQH__

#include "..\\interfaces\\IALEngine.mqh"
#include "..\\config\\CALRiskConfig.mqh"
#include "CALEngineBuy.mqh"
#include "CALEngineSell.mqh"
#include "CALEngineCommon.mqh"
#include "CALEvent.mqh"
#include "CALDebug.mqh"

class CALEngine : public IALEngine
{
private:
   CALEngineBuy m_buy_brain;
   CALEngineSell m_sell_brain;
   CALEngineCommon m_common_brain;

   CALContext m_context;
   CALEvent m_last_event;
   CALRiskConfig m_cfg;

   void SyncContext()
   {
      m_context.buy=m_buy_brain.Context();
      m_context.sell=m_sell_brain.Context();
      m_context.common=m_common_brain.Context();
   }

public:
   virtual void Init()
   {
      m_buy_brain.Init();
      m_sell_brain.Init();
      m_common_brain.Init();
      m_context.Reset();
      m_last_event.Reset();
      m_cfg.SetDefaults();
      m_buy_brain.SetRiskConfig(m_cfg);
      m_sell_brain.SetRiskConfig(m_cfg);
      m_common_brain.SetRiskConfig(m_cfg);
   }

   void SetRiskConfig(const CALRiskConfig &cfg)
   {
      m_cfg=cfg;
      m_cfg.SyncAliases();
      m_buy_brain.SetRiskConfig(m_cfg);
      m_sell_brain.SetRiskConfig(m_cfg);
      m_common_brain.SetRiskConfig(m_cfg);
   }

   CALRiskConfig RiskConfig() const { return m_cfg; }

   bool CheckGlobalSAFE() const
   {
      // Strict inequality (>) is intentional: threshold values themselves are still admissible.
      // SAFE activates only when aggregate stress exceeds configured risk budget.
      if(m_context.buy.safe_active || m_context.sell.safe_active) return true;
      if(m_context.common.margin > m_cfg.GLOBAL_MARGIN_LIMIT) return true;
      if(m_context.common.worst_dd > m_cfg.GLOBAL_DD_SUM_LIMIT) return true;
      return false;
   }

   virtual void OnPriceUpdate(const double price)
   {
      const ENUM_ALE_STATE old_buy=m_buy_brain.State();
      const ENUM_ALE_STATE old_sell=m_sell_brain.State();
      const ENUM_ALE_STATE old_common=m_common_brain.State();

      // Independent brains update first.
      m_buy_brain.OnPriceUpdate(price);
      m_sell_brain.OnPriceUpdate(price);

      // Common brain sees only read-only contexts from BUY/SELL.
      m_common_brain.Aggregate(m_buy_brain.Context(),m_sell_brain.Context());
      SyncContext();

      if(CheckGlobalSAFE())
      {
         VP_DEBUG_LOG("Global SAFE triggered");
         m_buy_brain.ForceSAFE();
         m_sell_brain.ForceSAFE();
         m_common_brain.Aggregate(m_buy_brain.Context(),m_sell_brain.Context());
         SyncContext();
         m_last_event.OnSAFETriggeredGlobal();
      }

      const ENUM_ALE_STATE new_buy=m_buy_brain.State();
      const ENUM_ALE_STATE new_sell=m_sell_brain.State();
      const ENUM_ALE_STATE new_common=m_common_brain.State();

      if(old_buy!=new_buy) m_last_event.OnStateChangeBuy(old_buy,new_buy);
      if(old_sell!=new_sell) m_last_event.OnStateChangeSell(old_sell,new_sell);
      if(old_common!=new_common) m_last_event.OnStateChangeCommon(old_common,new_common);

      if(m_context.buy.safe_active || m_context.sell.safe_active || m_context.common.safe_active)
         m_last_event.OnSAFETriggered();
      if(m_context.buy.worst_dd>m_cfg.MAX_DRAWDOWN || m_context.sell.worst_dd>m_cfg.MAX_DRAWDOWN || m_context.common.worst_dd>m_cfg.GLOBAL_DD_SUM_LIMIT)
         m_last_event.OnDrawdownExceeded();
   }

   bool BuildGrid(const int flow,const double center,const int levels,CALGrid &out_grid)
   {
      if(flow==ALE_FLOW_BUY) return m_buy_brain.BuildGrid(center,levels,out_grid);
      if(flow==ALE_FLOW_SELL) return m_sell_brain.BuildGrid(center,levels,out_grid);
      return false;
   }

   bool AddVirtual(const int flow,const double price,const double lot)
   {
      if(flow==ALE_FLOW_BUY) return m_buy_brain.AddVirtual(price,lot);
      if(flow==ALE_FLOW_SELL) return m_sell_brain.AddVirtual(price,lot);
      return false;
   }

   virtual double NetDeltaBuy() const { return m_context.buy.net_delta; }
   virtual double NetDeltaSell() const { return m_context.sell.net_delta; }
   virtual double NetDeltaCommon() const { return m_context.common.net_delta; }

   virtual double PnLBuy() const { return m_context.buy.pnl; }
   virtual double PnLSell() const { return m_context.sell.pnl; }
   virtual double PnLCommon() const { return m_context.common.pnl; }

   virtual double ExposureCommon() const { return m_context.common.exposure; }
   virtual double MarginCommon() const { return m_context.common.margin; }
   virtual double WorstDDCommon() const { return m_context.common.worst_dd; }
   virtual bool SAFECommon() const { return m_context.common.safe_active; }

   virtual ENUM_ALE_STATE StateBuy() const { return m_context.buy.state; }
   virtual ENUM_ALE_STATE StateSell() const { return m_context.sell.state; }
   virtual ENUM_ALE_STATE StateCommon() const { return m_context.common.state; }
   virtual CALContext Context() const { return m_context; }

   CALEvent LastEvent() const { return m_last_event; }

   CALEngine(){ Init(); }
};

#endif
