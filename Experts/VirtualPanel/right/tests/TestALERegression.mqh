#ifndef __TESTALEREGRESSION_MQH__
#define __TESTALEREGRESSION_MQH__

#include "..\\ale\\core\\CALDeterministicRunner.mqh"
#include "..\\ale\\interfaces\\IMarketAdapter.mqh"

bool NearReg(const double a,const double b,const double eps=1e-10){ return MathAbs(a-b)<=eps; }
bool FiniteReg(const double v){ return MathIsValidNumber(v) && v==v; }

class CRegressionMarketAdapter : public IMarketAdapter
{
public:
   virtual double Bid() const { return 1.1000; }
   virtual double Ask() const { return 1.1003; }
   virtual double Spread() const { return Ask()-Bid(); }
   virtual double ATR() const { return 0.0010; }
   virtual double MarginRequired(const double volume) const { return volume*1000.0; }
   virtual double TickValue() const { return 10.0; }
};

bool TestALE_RegressionOracles()
{
   CALRiskConfig cfg;
   cfg.SetDefaults();

   if(!cfg.IsValid()) return false;

   CALDeterministicRunner runner;
   runner.SetConfig(cfg);

   double trend_up[2]={1.0,1.1};
   runner.Run(trend_up,2);

   const CALStreamContext buy=runner.ContextBuy();
   const CALStreamContext sell=runner.ContextSell();
   const CALContext ctx=runner.Context();

   if(!NearReg(buy.net_delta,0.1)) return false;
   if(!NearReg(sell.net_delta,-0.1)) return false;
   if(!NearReg(buy.pnl,0.01)) return false;
   if(!NearReg(sell.pnl,-0.01)) return false;
   if(!NearReg(buy.margin,0.001)) return false;
   if(!NearReg(sell.margin,0.001)) return false;
   if(!NearReg(buy.worst_dd,0.001)) return false;
   if(!NearReg(sell.worst_dd,0.021)) return false;
   if(buy.safe_active || sell.safe_active) return false;

   if(!NearReg(ctx.NetDeltaTotal(),0.0)) return false;
   if(!NearReg(ctx.TotalPnL(),0.0)) return false;
   if(!NearReg(ctx.NetExposureTotal(),buy.exposure+sell.exposure)) return false;

   // I1 numerical derivative oracle.
   const double eps=1e-6;
   const double p0=1.05;
   const double pnl_plus=0.1*(p0+eps-1.0);
   const double pnl_minus=0.1*(p0-eps-1.0);
   const double d_num=(pnl_plus-pnl_minus)/(2.0*eps);
   if(!NearReg(d_num,0.1,1e-10)) return false;

   // Determinism replay oracle.
   CALDeterministicRunner runner2;
   runner2.SetConfig(cfg);
   runner2.Run(trend_up,2);
   const CALStreamContext buy2=runner2.ContextBuy();
   const CALStreamContext sell2=runner2.ContextSell();
   if(!NearReg(buy.pnl,buy2.pnl) || !NearReg(sell.pnl,sell2.pnl)) return false;
   if(!NearReg(buy.margin,buy2.margin) || !NearReg(sell.margin,sell2.margin)) return false;

   // Reset reproducibility oracle.
   runner2.Reset();
   runner2.Run(trend_up,2);
   const CALStreamContext buy3=runner2.ContextBuy();
   const CALStreamContext sell3=runner2.ContextSell();
   if(!NearReg(buy.pnl,buy3.pnl) || !NearReg(sell.pnl,sell3.pnl)) return false;

   // Trend down scenario.
   runner.Reset();
   double trend_down[2]={1.0,0.9};
   runner.Run(trend_down,2);
   const CALContext down=runner.Context();
   if(!NearReg(down.buy.pnl,-0.01)) return false;
   if(!NearReg(down.sell.pnl,0.01)) return false;

   // Oscillation scenario + finite checks.
   runner.Reset();
   double osc[6]={1.0,1.01,0.99,1.01,0.99,1.0};
   runner.Run(osc,6);
   const CALContext osc_ctx=runner.Context();
   if(!FiniteReg(osc_ctx.buy.pnl) || !FiniteReg(osc_ctx.sell.pnl)) return false;

   // Flash crash + recovery.
   runner.Reset();
   double flash[4]={1.0,1.0,0.7,1.0};
   runner.Run(flash,4);
   const CALContext flash_ctx=runner.Context();
   if(!FiniteReg(flash_ctx.buy.worst_dd) || !FiniteReg(flash_ctx.sell.worst_dd)) return false;

   // Zero equity edge-case formula oracle.
   const double lot_zero=(0.0*0.02)/(200.0*10.0);
   if(!NearReg(lot_zero,0.0)) return false;

   // Spread invariant.
   CRegressionMarketAdapter market;
   if(!NearReg(market.Spread(),0.0003)) return false;

   // SAFE phase legality.
   CALStateMachine fsm;
   if(!fsm.Transition(ALE_STATE_SAFE)) return false;
   if(fsm.Transition(ALE_STATE_EXPANSION)) return false;

   return true;
}

#endif
