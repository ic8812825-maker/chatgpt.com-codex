#ifndef __CALDETERMINISTICRUNNER_MQH__
#define __CALDETERMINISTICRUNNER_MQH__

#include "CALEngine.mqh"

class CALDeterministicRunner
{
private:
   CALEngine m_engine;
   CALRiskConfig m_cfg;
   bool m_seeded;

   mutable CALStreamContext m_buy_cache;
   mutable CALStreamContext m_sell_cache;

   void SyncCaches() const
   {
      const CALContext ctx=m_engine.Context();
      m_buy_cache=ctx.buy;
      m_sell_cache=ctx.sell;
   }

public:
   void SetConfig(const CALRiskConfig &cfg)
   {
      m_cfg=cfg;
      m_engine.SetRiskConfig(m_cfg);
      m_engine.Init();
      m_seeded=false;
      SyncCaches();
   }

   void Reset()
   {
      m_engine.SetRiskConfig(m_cfg);
      m_engine.Init();
      m_seeded=false;
      SyncCaches();
   }

   void Run(const double prices[],const int n)
   {
      if(n<=0) return;

      if(!m_seeded)
      {
         const double p0=prices[0];
         m_engine.AddVirtual(ALE_FLOW_BUY,p0,0.1);
         m_engine.AddVirtual(ALE_FLOW_SELL,p0,0.1);
         m_seeded=true;
      }

      for(int i=0;i<n;i++)
         m_engine.OnPriceUpdate(prices[i]);

      SyncCaches();
   }

   const CALStreamContext& ContextBuy() const
   {
      SyncCaches();
      return m_buy_cache;
   }

   const CALStreamContext& ContextSell() const
   {
      SyncCaches();
      return m_sell_cache;
   }

   CALContext Context() const { return m_engine.Context(); }

   CALDeterministicRunner()
   {
      m_cfg.SetDefaults();
      m_engine.SetRiskConfig(m_cfg);
      m_engine.Init();
      m_seeded=false;
      SyncCaches();
   }
};

#endif
