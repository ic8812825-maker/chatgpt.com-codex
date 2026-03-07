#ifndef __CALDETERMINISTICRUNNER_MQH__
#define __CALDETERMINISTICRUNNER_MQH__

#include "CALEngine.mqh"
#include "CALExportHelper.mqh"

enum ENUM_ALE_REPLAY_SCENARIO
{
   ALE_REPLAY_UPTREND=0,
   ALE_REPLAY_DOWNTREND=1,
   ALE_REPLAY_OSCILLATION=2,
   ALE_REPLAY_CRASH=3,
   ALE_REPLAY_VSHAPE=4
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

struct CALStateTraceExpectation
{
   ENUM_ALE_STATE buy_states[];
   ENUM_ALE_STATE sell_states[];

   void Reset()
   {
      ArrayResize(buy_states,0);
      ArrayResize(sell_states,0);
   }

   void Push(const ENUM_ALE_STATE buy_state,const ENUM_ALE_STATE sell_state)
   {
      const int n=ArraySize(buy_states);
      ArrayResize(buy_states,n+1);
      ArrayResize(sell_states,n+1);
      buy_states[n]=buy_state;
      sell_states[n]=sell_state;
   }
};

class CALDeterministicRunner
{
private:
   CALEngine m_engine;
   CALExportHelper m_export;

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

      if(scenario==ALE_REPLAY_VSHAPE)
      {
         const int pivot=(count/2);
         for(int v=0;v<count;v++)
         {
            if(v<=pivot) out_prices[v]=start-(step*v);
            else out_prices[v]=start-(step*pivot)+(step*(v-pivot));
         }
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

   bool ReplayWithExpectedTrace(const double &prices[],const CALStateTraceExpectation &expected,CALReplayResult &out_result)
   {
      out_result.Reset();
      const int n=ArraySize(prices);
      if(n<=0) return false;
      if(ArraySize(expected.buy_states)!=n || ArraySize(expected.sell_states)!=n) return false;

      for(int i=0;i<n;i++)
      {
         m_engine.OnPriceUpdate(prices[i]);
         const CALContext ctx=m_engine.Context();

         if(ctx.buy.state!=expected.buy_states[i]) return false;
         if(ctx.sell.state!=expected.sell_states[i]) return false;
         if(!IsFinite(ctx.buy.pnl) || !IsFinite(ctx.sell.pnl)) return false;
      }

      return Replay(prices,out_result);
   }

   bool Replay(const double &prices[],CALReplayResult &out_result)
   {
      out_result.Reset();
      const int n=ArraySize(prices);
      if(n<=0)
         return false;

      m_export.BeginReplayContextCSV("ale_replay_context.csv");
      for(int i=0;i<n;i++)
      {
         m_engine.OnPriceUpdate(prices[i]);
         const CALContext ctx=m_engine.Context();
         m_export.AppendReplayStepCSV(i,ctx);

         if(!IsFinite(ctx.buy.pnl) || !IsFinite(ctx.sell.pnl))
         {
            m_export.EndReplayContextCSV();
            return false;
         }
         if(!IsFinite(ctx.buy.net_delta) || !IsFinite(ctx.sell.net_delta))
         {
            m_export.EndReplayContextCSV();
            return false;
         }
         if(!IsFinite(ctx.buy.worst_dd) || !IsFinite(ctx.sell.worst_dd))
         {
            m_export.EndReplayContextCSV();
            return false;
         }
      }
      m_export.EndReplayContextCSV();

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

   bool ExportAttachedVirtuals(const string file_name,
                               const double &buy_prices[],const double &buy_lots[],
                               const double &sell_prices[],const double &sell_lots[])
   {
      return m_export.ExportPositionsCSV(file_name,buy_prices,buy_lots,sell_prices,sell_lots);
   }

   bool ExportJUnitSummary(const string file_name,const int total,const int failed)
   {
      return m_export.ExportJUnitXML(file_name,total,failed);
   }

   CALEngine Engine() const { return m_engine; }
};

#endif
