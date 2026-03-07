#ifndef __CALENGINEBUY_MQH__
#define __CALENGINEBUY_MQH__

#include "CBuyEngine.mqh"
#include "..\\config\\CALRiskConfig.mqh"

// Independent BUY brain.
// Owns BUY-only FSM/risk/exposure path and does not read SELL context.
class CALEngineBuy
{
private:
   CBuyEngine m_stream;
   CALRiskConfig m_cfg;

public:
   void Init()
   {
      m_stream.Init(ALE_FLOW_BUY);
      m_cfg.SetDefaults();
      m_stream.SetRiskConfig(m_cfg);
   }

   void SetRiskConfig(const CALRiskConfig &cfg)
   {
      m_cfg=cfg;
      m_cfg.SyncAliases();
      m_stream.SetRiskConfig(m_cfg);
   }

   void OnPriceUpdate(const double price)
   {
      m_stream.Process(price);
   }

   bool AddVirtual(const double price,const double lot)
   {
      return m_stream.AddVirtual(price,lot);
   }

   bool BuildGrid(const double center,const int levels,CALGrid &out_grid)
   {
      return m_stream.BuildGrid(center,levels,out_grid);
   }

   void ForceSAFE(){ m_stream.ForceSAFE(); }

   ENUM_ALE_STATE State() const { return m_stream.State(); }
   CALStreamContext Context() const { return m_stream.Context(); }

   CALEngineBuy(){ Init(); }
};

#endif
