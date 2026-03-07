#ifndef __CALENGINE_MQH__
#define __CALENGINE_MQH__

#include "..\\interfaces\\IALEngine.mqh"
#include "..\\config\\CALRiskConfig.mqh"
#include "CBuyEngine.mqh"
#include "CSellEngine.mqh"
#include "CALEvent.mqh"
#include "CALDebug.mqh"

class CALEngine : public IALEngine
{
private:
   CBuyEngine m_buy_stream;
   CSellEngine m_sell_stream;
   CALContext m_context;
   CALEvent m_last_event;
   CALRiskConfig m_cfg;

   void SyncContext()
   {
      m_context.buy=m_buy_stream.Context();
      m_context.sell=m_sell_stream.Context();
   }

public:
   virtual void Init()
   {
      m_buy_stream.Init(ALE_FLOW_BUY);
      m_sell_stream.Init(ALE_FLOW_SELL);
      m_context.Reset();
      m_last_event.Reset();
      m_cfg.SetDefaults();
      m_buy_stream.SetRiskConfig(m_cfg);
      m_sell_stream.SetRiskConfig(m_cfg);
   }


   void SetRiskConfig(const CALRiskConfig &cfg)
   {
      m_cfg=cfg;
      m_cfg.SyncAliases();
      m_buy_stream.SetRiskConfig(m_cfg);
      m_sell_stream.SetRiskConfig(m_cfg);
   }

   CALRiskConfig RiskConfig() const { return m_cfg; }

   bool CheckGlobalSAFE() const
   {
      // Strict inequality (>) is intentional: threshold values themselves are still admissible.
      // SAFE activates only when aggregate stress exceeds configured risk budget.
      if(m_context.buy.safe_active || m_context.sell.safe_active) return true;
      if(m_context.buy.margin + m_context.sell.margin > m_cfg.GLOBAL_MARGIN_LIMIT) return true;
      if(m_context.buy.worst_dd + m_context.sell.worst_dd > m_cfg.GLOBAL_DD_SUM_LIMIT) return true;
      return false;
   }

   virtual void OnPriceUpdate(const double price)
   {
      const ENUM_ALE_STATE old_buy=m_buy_stream.State();
      const ENUM_ALE_STATE old_sell=m_sell_stream.State();

      m_buy_stream.Process(price);
      m_sell_stream.Process(price);
      SyncContext();

      if(CheckGlobalSAFE())
      {
         VP_DEBUG_LOG("Global SAFE triggered");
         m_buy_stream.ForceSAFE();
         m_sell_stream.ForceSAFE();
         SyncContext();
         m_last_event.OnSAFETriggeredGlobal();
      }

      const ENUM_ALE_STATE new_buy=m_buy_stream.State();
      const ENUM_ALE_STATE new_sell=m_sell_stream.State();
      if(old_buy!=new_buy) m_last_event.OnStateChangeBuy(old_buy,new_buy);
      if(old_sell!=new_sell) m_last_event.OnStateChangeSell(old_sell,new_sell);
      if(m_context.buy.safe_active || m_context.sell.safe_active) m_last_event.OnSAFETriggered();
      if(m_context.buy.worst_dd>m_cfg.MAX_DRAWDOWN || m_context.sell.worst_dd>m_cfg.MAX_DRAWDOWN) m_last_event.OnDrawdownExceeded();
   }

   bool BuildGrid(const int flow,const double center,const int levels,CALGrid &out_grid)
   {
      if(flow==ALE_FLOW_BUY) return m_buy_stream.BuildGrid(center,levels,out_grid);
      if(flow==ALE_FLOW_SELL) return m_sell_stream.BuildGrid(center,levels,out_grid);
      return false;
   }

   bool AddVirtual(const int flow,const double price,const double lot)
   {
      if(flow==ALE_FLOW_BUY) return m_buy_stream.AddVirtual(price,lot);
      if(flow==ALE_FLOW_SELL) return m_sell_stream.AddVirtual(price,lot);
      return false;
   }

   virtual double NetDeltaBuy() const { return m_context.buy.net_delta; }
   virtual double NetDeltaSell() const { return m_context.sell.net_delta; }
   virtual double PnLBuy() const { return m_context.buy.pnl; }
   virtual double PnLSell() const { return m_context.sell.pnl; }
   virtual ENUM_ALE_STATE StateBuy() const { return m_context.buy.state; }
   virtual ENUM_ALE_STATE StateSell() const { return m_context.sell.state; }
   virtual CALContext Context() const { return m_context; }

   CALEvent LastEvent() const { return m_last_event; }

   CALEngine(){ Init(); }
};

#endif
