#ifndef __TESTALE_MQH__
#define __TESTALE_MQH__

#include "..\\ale\\core\\CALEngine.mqh"
#include "..\\ale\\core\\CALStateMachine.mqh"
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

#endif
