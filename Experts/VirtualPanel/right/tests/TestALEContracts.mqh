#ifndef __TESTALECONTRACTS_MQH__
#define __TESTALECONTRACTS_MQH__

#include "..\\ale\\core\\CALEngine.mqh"
#include "..\\ale\\math\\CALPhaseDiagram.mqh"

bool NearContract(const double a,const double b,const double eps=1e-10){ return MathAbs(a-b)<=eps; }

bool TestPhaseDiagramGuard()
{
   CALRiskConfig cfg;
   cfg.SetDefaults();
   cfg.k=0.8;
   cfg.growth_g=1.3; // theta = 1.04 (explosive)
   if(cfg.IsValid()) return false;

   CALPhaseDiagram phase;
   if(phase.DetectPhase(cfg.k,cfg.growth_g)!=PHASE_EXPLOSIVE) return false;
   if(phase.IsStable(cfg.k,cfg.growth_g,cfg.sigma)) return false;

   CALLotModel lot_model;
   if(lot_model.LotAtLevel(1,0.1,0.9)>0.0) return false;
   if(lot_model.LotAtLevel(1,0.1,0.8)<=0.0) return false;
   return true;
}

bool TestSAFEBypassContract()
{
   CALEngine ale;
   CALRiskConfig cfg;
   cfg.SetDefaults();
   cfg.k=0.8;
   cfg.growth_g=1.3; // invalid/explosive -> SAFE activation path
   ale.SetRiskConfig(cfg);
   ale.Init();

   if(!ale.AddVirtual(ALE_FLOW_BUY,1.0,0.1)) return false;
   if(!ale.AddVirtual(ALE_FLOW_SELL,1.0,0.1)) return false;

   ale.OnPriceUpdate(1.0);
   if(ale.StateBuy()!=ALE_STATE_SAFE || ale.StateSell()!=ALE_STATE_SAFE) return false;

   CALGrid g;
   if(ale.AddVirtual(ALE_FLOW_BUY,1.0,0.1)) return false;
   if(ale.BuildGrid(ALE_FLOW_BUY,1.0,3,g)) return false;
   return true;
}

bool TestAdditivityContract()
{
   CALEngine ale;
   ale.Init();
   ale.AddVirtual(ALE_FLOW_BUY,1.0,0.1);
   ale.AddVirtual(ALE_FLOW_SELL,1.0,0.1);
   ale.OnPriceUpdate(1.1);

   const CALContext c=ale.Context();
   if(!NearContract(c.TotalPnL(),c.buy.pnl+c.sell.pnl)) return false;
   if(!NearContract(c.NetDeltaTotal(),c.buy.net_delta+c.sell.net_delta)) return false;
   if(!NearContract(c.NetExposureTotal(),c.buy.exposure+c.sell.exposure)) return false;
   return true;
}

#endif
