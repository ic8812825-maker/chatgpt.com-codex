#ifndef __CALENGINESELL_MQH__
#define __CALENGINESELL_MQH__

#include "CSellEngine.mqh"
#include "..\\config\\CALRiskConfig.mqh"

// Independent SELL brain.
// Owns SELL-only FSM/risk/exposure path and does not read BUY context.
class CALEngineSell
{
private:
   CSellEngine m_stream;
   CALRiskConfig m_cfg;

public:
   void Init()
   {
      m_stream.Init(ALE_FLOW_SELL);
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

   CALEngineSell(){ Init(); }
};

#endif
