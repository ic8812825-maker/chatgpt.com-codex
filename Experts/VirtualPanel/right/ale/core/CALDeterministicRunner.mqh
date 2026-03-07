#ifndef __CALDETERMINISTICRUNNER_MQH__
#define __CALDETERMINISTICRUNNER_MQH__

#include "CALEngine.mqh"

enum ENUM_ALE_REPLAY_SCENARIO
{
   ALE_REPLAY_UPTREND=0,
   ALE_REPLAY_DOWNTREND=1,
   ALE_REPLAY_OSCILLATION=2,
   ALE_REPLAY_CRASH=3
};

struct CALReplayResult
{
   bool ok;
   int steps;
   ENUM_ALE_STATE state_buy;
   ENUM_ALE_STATE state_sell;
   double pnl_buy;
   double pnl_sell;
   double worst_dd_buy;
   double worst_dd_sell;

   void Reset()
   {
      ok=false;
      steps=0;
      state_buy=ALE_STATE_IDLE;
      state_sell=ALE_STATE_IDLE;
      pnl_buy=0.0;
      pnl_sell=0.0;
      worst_dd_buy=0.0;
      worst_dd_sell=0.0;
   }
};

class CALDeterministicRunner
{
private:
   CALEngine m_engine;

   bool IsFinite(const double v) const
   {
      return MathIsValidNumber(v) && v==v;
   }

public:
   void Init(const CALRiskConfig &cfg)
   {
      m_engine.Init();
      m_engine.SetRiskConfig(cfg);
   }

   bool AttachVirtuals(const double buy_price,const double buy_lot,const double sell_price,const double sell_lot)
   {
      const bool ok_buy=m_engine.AddVirtual(ALE_FLOW_BUY,buy_price,buy_lot);
      const bool ok_sell=m_engine.AddVirtual(ALE_FLOW_SELL,sell_price,sell_lot);
      return ok_buy && ok_sell;
   }

   void BuildScenario(const ENUM_ALE_REPLAY_SCENARIO scenario,const double start,const double step,const int count,double &out_prices[]) const
   {
      ArrayResize(out_prices,count);
      if(count<=0)
         return;

      if(scenario==ALE_REPLAY_UPTREND)
      {
         for(int i=0;i<count;i++) out_prices[i]=start+step*i;
         return;
      }

      if(scenario==ALE_REPLAY_DOWNTREND)
      {
         for(int j=0;j<count;j++) out_prices[j]=start-step*j;
         return;
      }

      if(scenario==ALE_REPLAY_OSCILLATION)
      {
         for(int k=0;k<count;k++) out_prices[k]=start+((k%2==0)?step:-step);
         return;
      }

      // ALE_REPLAY_CRASH
      for(int c=0;c<count;c++)
      {
         if(c<count-2) out_prices[c]=start;
         else if(c==count-2) out_prices[c]=start-step;
         else out_prices[c]=start-(4.0*step);
      }
   }

   bool ReplayScenario(const ENUM_ALE_REPLAY_SCENARIO scenario,const double start,const double step,const int count,CALReplayResult &out_result)
   {
      double prices[];
      BuildScenario(scenario,start,step,count,prices);
      return Replay(prices,out_result);
   }

   bool Replay(const double &prices[],CALReplayResult &out_result)
   {
      out_result.Reset();
      const int n=ArraySize(prices);
      if(n<=0)
         return false;

      for(int i=0;i<n;i++)
      {
         m_engine.OnPriceUpdate(prices[i]);
         const CALContext ctx=m_engine.Context();

         if(!IsFinite(ctx.buy.pnl) || !IsFinite(ctx.sell.pnl))
            return false;
         if(!IsFinite(ctx.buy.net_delta) || !IsFinite(ctx.sell.net_delta))
            return false;
         if(!IsFinite(ctx.buy.worst_dd) || !IsFinite(ctx.sell.worst_dd))
            return false;
      }

      const CALContext final_ctx=m_engine.Context();
      out_result.ok=true;
      out_result.steps=n;
      out_result.state_buy=final_ctx.buy.state;
      out_result.state_sell=final_ctx.sell.state;
      out_result.pnl_buy=final_ctx.buy.pnl;
      out_result.pnl_sell=final_ctx.sell.pnl;
      out_result.worst_dd_buy=final_ctx.buy.worst_dd;
      out_result.worst_dd_sell=final_ctx.sell.worst_dd;
      return true;
   }

   CALEngine Engine() const { return m_engine; }
};

#endif
