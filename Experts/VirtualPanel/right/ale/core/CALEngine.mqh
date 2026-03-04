#ifndef __CALENGINE_MQH__
#define __CALENGINE_MQH__

#include "..\\interfaces\\IALEngine.mqh"
#include "CBuyEngine.mqh"
#include "CSellEngine.mqh"
#include "CALEvent.mqh"

class CALEngine : public IALEngine
{
private:
   CBuyEngine m_buy_stream;
   CSellEngine m_sell_stream;
   CALEvent m_last_event;

   double m_global_margin_limit;
   double m_global_drawdown_limit;

   CALContext BuildContextSnapshot() const
   {
      CALContext ctx;
      ctx.Reset();
      ctx.buy=m_buy_stream.Context();
      ctx.sell=m_sell_stream.Context();
      return ctx;
   }

public:
   virtual void Init()
   {
      m_buy_stream.Init(ALE_FLOW_BUY);
      m_sell_stream.Init(ALE_FLOW_SELL);
      m_last_event.Reset();
      m_global_margin_limit=100000.0;
      m_global_drawdown_limit=0.50;
   }

   bool CheckGlobalSAFE() const
   {
      const CALContext ctx=BuildContextSnapshot();
      if(ctx.buy.margin + ctx.sell.margin > m_global_margin_limit)
         return true;
      if(ctx.buy.worst_dd + ctx.sell.worst_dd > m_global_drawdown_limit)
         return true;
      return false;
   }

   virtual void OnPriceUpdate(const double bid,const double ask)
   {
      const ENUM_ALE_STATE old_buy=m_buy_stream.State();
      const ENUM_ALE_STATE old_sell=m_sell_stream.State();

      m_buy_stream.Process(bid,ask);
      m_sell_stream.Process(bid,ask);

      const ENUM_ALE_STATE new_buy=m_buy_stream.State();
      const ENUM_ALE_STATE new_sell=m_sell_stream.State();

      if(old_buy!=new_buy)
         m_last_event.OnStateChangeBuy(old_buy,new_buy);
      if(old_sell!=new_sell)
         m_last_event.OnStateChangeSell(old_sell,new_sell);

      const CALContext ctx=BuildContextSnapshot();
      if(ctx.buy.state==ALE_STATE_SAFE || ctx.sell.state==ALE_STATE_SAFE)
         m_last_event.OnSAFETriggered();
      if(CheckGlobalSAFE())
         m_last_event.OnSAFETriggeredGlobal();
      if(ctx.buy.worst_dd>0.25 || ctx.sell.worst_dd>0.25)
         m_last_event.OnDrawdownExceeded();
   }

   bool BuildGrid(const int flow,const double center,const int levels,CALGrid &out_grid)
   {
      if(flow==ALE_FLOW_BUY) return m_buy_stream.BuildGrid(center,levels,out_grid);
      if(flow==ALE_FLOW_SELL) return m_sell_stream.BuildGrid(center,levels,out_grid);
      return false;
   }

   void AddVirtual(const int flow,const double price,const double lot)
   {
      if(flow==ALE_FLOW_BUY) m_buy_stream.AddVirtual(price,lot);
      if(flow==ALE_FLOW_SELL) m_sell_stream.AddVirtual(price,lot);
   }

   virtual double NetDeltaBuy() const { return m_buy_stream.Context().net_delta; }
   virtual double NetDeltaSell() const { return m_sell_stream.Context().net_delta; }
   virtual ENUM_ALE_STATE StateBuy() const { return m_buy_stream.State(); }
   virtual ENUM_ALE_STATE StateSell() const { return m_sell_stream.State(); }
   virtual CALContext Context() const { return BuildContextSnapshot(); }

   CALEvent LastEvent() const { return m_last_event; }

   CALEngine(){ Init(); }
};

#endif
