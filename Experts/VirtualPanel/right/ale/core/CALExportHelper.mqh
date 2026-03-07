#ifndef __CALEXPORTHELPER_MQH__
#define __CALEXPORTHELPER_MQH__

#include "CALContext.mqh"

// Helper for machine-readable exports from deterministic ALE runs.
// Usage example:
//   CALExportHelper helper;
//   helper.BeginReplayContextCSV("ale_replay_context.csv");
//   helper.AppendReplayStepCSV(1,ctx);
//   helper.EndReplayContextCSV();
class CALExportHelper
{
private:
   int m_ctx_handle;

public:
   void BeginReplayContextCSV(const string file_name)
   {
      m_ctx_handle=FileOpen(file_name,FILE_WRITE|FILE_CSV|FILE_ANSI,';');
      if(m_ctx_handle==INVALID_HANDLE)
      {
         PrintFormat("[ALE][EXPORT] cannot open CSV: %s",file_name);
         return;
      }

      FileWrite(m_ctx_handle,
                "step",
                "state_buy","state_sell",
                "pnl_buy","pnl_sell",
                "net_delta_buy","net_delta_sell",
                "worst_dd_buy","worst_dd_sell",
                "margin_buy","margin_sell",
                "safe_buy","safe_sell");
   }

   void AppendReplayStepCSV(const int step,const CALContext &ctx)
   {
      if(m_ctx_handle==INVALID_HANDLE)
         return;

      FileWrite(m_ctx_handle,
                step,
                (int)ctx.buy.state,(int)ctx.sell.state,
                ctx.buy.pnl,ctx.sell.pnl,
                ctx.buy.net_delta,ctx.sell.net_delta,
                ctx.buy.worst_dd,ctx.sell.worst_dd,
                ctx.buy.margin,ctx.sell.margin,
                (ctx.buy.safe_active?1:0),(ctx.sell.safe_active?1:0));
   }

   void EndReplayContextCSV()
   {
      if(m_ctx_handle!=INVALID_HANDLE)
         FileClose(m_ctx_handle);
      m_ctx_handle=INVALID_HANDLE;
   }

   bool ExportPositionsCSV(const string file_name,
                           const double &buy_prices[],const double &buy_lots[],
                           const double &sell_prices[],const double &sell_lots[])
   {
      const int h=FileOpen(file_name,FILE_WRITE|FILE_CSV|FILE_ANSI,';');
      if(h==INVALID_HANDLE)
      {
         PrintFormat("[ALE][EXPORT] cannot open positions CSV: %s",file_name);
         return false;
      }

      FileWrite(h,"flow","price","lot");

      for(int i=0;i<ArraySize(buy_prices) && i<ArraySize(buy_lots);i++)
         FileWrite(h,"BUY",buy_prices[i],buy_lots[i]);

      for(int j=0;j<ArraySize(sell_prices) && j<ArraySize(sell_lots);j++)
         FileWrite(h,"SELL",sell_prices[j],sell_lots[j]);

      FileClose(h);
      return true;
   }

   bool ExportJUnitXML(const string file_name,const int total,const int failed)
   {
      const int h=FileOpen(file_name,FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(h==INVALID_HANDLE)
      {
         PrintFormat("[ALE][EXPORT] cannot open junit xml: %s",file_name);
         return false;
      }

      const string head=StringFormat("<testsuite name=\"ALE\" tests=\"%d\" failures=\"%d\">",total,failed);
      FileWriteString(h,"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
      FileWriteString(h,head+"\n");
      if(failed>0)
         FileWriteString(h,"  <testcase name=\"ALERunner\"><failure message=\"One or more tests failed\"/></testcase>\n");
      else
         FileWriteString(h,"  <testcase name=\"ALERunner\"/>\n");
      FileWriteString(h,"</testsuite>\n");
      FileClose(h);
      return true;
   }

   CALExportHelper(){ m_ctx_handle=INVALID_HANDLE; }
};

#endif
