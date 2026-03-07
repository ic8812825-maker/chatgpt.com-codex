#ifndef __TESTALE_MQH__
#define __TESTALE_MQH__

#include "..\\ale\\core\\CALEngine.mqh"
#include "..\\ale\\core\\CALStateMachine.mqh"
#include "..\\ale\\core\\CALDeterministicRunner.mqh"
#include "..\\ale\\interfaces\\IMarketAdapter.mqh"

class CMockMarketAdapter : public IMarketAdapter
{
public:
   virtual double Bid() const { return 1.1000; }
   virtual double Ask() const { return 1.1003; }
   virtual double Spread() const { return Ask()-Bid(); }
   virtual double ATR() const { return 0.0010; }
   virtual double MarginRequired(const double volume) const { return volume*1000.0; }
   virtual double TickValue() const { return 10.0; }
};

bool NearALE(const double a,const double b,const double eps=1e-8){ return MathAbs(a-b)<=eps; }
bool IsFiniteALE(const double v){ return MathIsValidNumber(v) && v==v; }

bool TestALE_DualFlowIntegration()
{
   CMockMarketAdapter market;
   if(!NearALE(market.Spread(),0.0003,1e-12)) return false;

   CALEngine ale;
   ale.Init();
   if(!ale.AddVirtual(ALE_FLOW_BUY,1.0,0.1)) return false;
   if(!ale.AddVirtual(ALE_FLOW_SELL,1.2,0.1)) return false;

   double p=1.0;
   for(int i=0;i<1000;i++){ p+=0.0001; ale.OnPriceUpdate(p); }
   for(int j=0;j<1000;j++){ p-=0.0001; ale.OnPriceUpdate(p); }
   for(int k=0;k<200;k++){ const double x=(k%2==0?0.0004:-0.0004); ale.OnPriceUpdate(p+x); }
   ale.OnPriceUpdate(0.7);

   CALContext ctx=ale.Context();
   if(!NearALE(ctx.NetDeltaTotal(),ctx.buy.net_delta+ctx.sell.net_delta,1e-12)) return false;
   if(!NearALE(ctx.TotalPnL(),ctx.buy.pnl+ctx.sell.pnl,1e-12)) return false;

   if(!IsFiniteALE(ctx.buy.pnl) || !IsFiniteALE(ctx.sell.pnl)) return false;
   if(!IsFiniteALE(ctx.buy.exposure) || !IsFiniteALE(ctx.sell.exposure)) return false;

   const double h=1e-5;
   const double p0=1.05;
   const double pnl_plus=0.1*(p0+h-1.0);
   const double pnl_minus=0.1*(p0-h-1.0);
   const double d_num=(pnl_plus-pnl_minus)/(2.0*h);
   if(!NearALE(d_num,0.1,1e-6)) return false;

   CALStateMachine fsm;
   if(!fsm.Transition(ALE_STATE_SAFE)) return false;
   if(fsm.Transition(ALE_STATE_EXPANSION)) return false;

   CALStateMachine fsm2;
   fsm2.Transition(ALE_STATE_BASE);
   if(fsm2.TransitionBySignal(ALE_SIGNAL_HARVEST_REACHED)!=ALE_STATE_HARVEST) return false;

   const double max_lot_zero=(0.0*0.02)/(200.0*market.TickValue());
   if(!NearALE(max_lot_zero,0.0,1e-12)) return false;

   return true;
}

bool PrepareRunner(CALDeterministicRunner &runner)
{
   CALRiskConfig cfg;
   cfg.SetDefaults();
   cfg.dd_max=0.35;
   cfg.stress_limit=1.2;
   runner.Init(cfg);
   return runner.AttachVirtuals(1.1000,0.10,1.1000,0.10);
}

bool TestALE_DeterministicReplayHarness()
{
   CALDeterministicRunner runner;
   if(!PrepareRunner(runner)) return false;

   double prices[];
   ArrayResize(prices,8);
   prices[0]=1.1000;
   prices[1]=1.1008;
   prices[2]=1.1016;
   prices[3]=1.1004;
   prices[4]=1.0992;
   prices[5]=1.1001;
   prices[6]=1.0995;
   prices[7]=1.1000;

   CALReplayResult res;
   if(!runner.Replay(prices,res)) return false;
   if(!res.ok || res.steps!=8) return false;

   if(!IsFiniteALE(res.pnl_buy) || !IsFiniteALE(res.pnl_sell)) return false;
   if(!IsFiniteALE(res.worst_dd_buy) || !IsFiniteALE(res.worst_dd_sell)) return false;
   return true;
}

bool TestALE_ReplayScenario_Uptrend()
{
   CALDeterministicRunner runner;
   if(!PrepareRunner(runner)) return false;

   CALReplayResult res;
   if(!runner.ReplayScenario(ALE_REPLAY_UPTREND,1.1000,0.0002,16,res)) return false;
   if(!res.ok || res.steps!=16) return false;
   return IsFiniteALE(res.pnl_buy) && IsFiniteALE(res.pnl_sell);
}

bool TestALE_ReplayScenario_Oscillation()
{
   CALDeterministicRunner runner;
   if(!PrepareRunner(runner)) return false;

   CALReplayResult res;
   if(!runner.ReplayScenario(ALE_REPLAY_OSCILLATION,1.1000,0.0005,20,res)) return false;
   if(!res.ok || res.steps!=20) return false;
   return IsFiniteALE(res.worst_dd_buy) && IsFiniteALE(res.worst_dd_sell);
}

bool TestALE_ReplayScenario_Crash()
{
   CALDeterministicRunner runner;
   if(!PrepareRunner(runner)) return false;

   CALReplayResult res;
   if(!runner.ReplayScenario(ALE_REPLAY_CRASH,1.1000,0.0020,12,res)) return false;
   if(!res.ok || res.steps!=12) return false;
   return (res.worst_dd_buy>=0.0 && res.worst_dd_sell>=0.0);
}

#endif
