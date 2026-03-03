#ifndef __CALENGINE_MQH__
#define __CALENGINE_MQH__

#include "..\\interfaces\\IALEngine.mqh"
#include "CBuyEngine.mqh"
#include "CSellEngine.mqh"
#include "CALEvent.mqh"

class CALEngine : public IALEngine
{
private:
   CBuyEngine m_buy;
   CSellEngine m_sell;
   CALEvent m_last_event;

public:
   virtual void Init()
   {
      m_buy.Init(ALE_FLOW_BUY);
      m_sell.Init(ALE_FLOW_SELL);
      m_last_event.Reset();
   }

   virtual void OnPriceUpdate(const double bid,const double ask)
   {
      const ENUM_ALE_STATE old_buy=m_buy.State();
      const ENUM_ALE_STATE old_sell=m_sell.State();

      m_buy.Process(bid,ask);
      m_sell.Process(bid,ask);

      const ENUM_ALE_STATE new_buy=m_buy.State();
      const ENUM_ALE_STATE new_sell=m_sell.State();

      if(old_buy!=new_buy)
         m_last_event.OnStateChangeBuy(old_buy,new_buy);
      if(old_sell!=new_sell)
         m_last_event.OnStateChangeSell(old_sell,new_sell);

      const CALContext buy_ctx=m_buy.Context();
      const CALContext sell_ctx=m_sell.Context();
      if(buy_ctx.state==ALE_STATE_SAFE || sell_ctx.state==ALE_STATE_SAFE)
         m_last_event.OnSAFETriggered();
      if(buy_ctx.drawdown>0.25 || sell_ctx.drawdown>0.25)
         m_last_event.OnDrawdownExceeded();
   }

   bool BuildGrid(const int flow,const double center,const int levels,CALGrid &out_grid)
   {
      if(flow==ALE_FLOW_BUY) return m_buy.BuildGrid(center,levels,out_grid);
      if(flow==ALE_FLOW_SELL) return m_sell.BuildGrid(center,levels,out_grid);
      return false;
   }

   void AddVirtual(const int flow,const double price,const double lot)
   {
      if(flow==ALE_FLOW_BUY) m_buy.AddVirtual(price,lot);
      if(flow==ALE_FLOW_SELL) m_sell.AddVirtual(price,lot);
   }

   virtual CALContext Context(const int flow) const
   {
      if(flow==ALE_FLOW_BUY) return m_buy.Context();
      if(flow==ALE_FLOW_SELL) return m_sell.Context();

      CALContext empty_ctx;
      empty_ctx.Reset();
      return empty_ctx;
   }

   virtual ENUM_ALE_STATE State(const int flow) const
   {
      return Context(flow).state;
   }

   CALEvent LastEvent() const { return m_last_event; }

   CALEngine(){ Init(); }
};

#endif
