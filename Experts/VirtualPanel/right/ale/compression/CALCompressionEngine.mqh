#ifndef __CALCOMPRESSIONENGINE_MQH__
#define __CALCOMPRESSIONENGINE_MQH__

#include "CALLockCompression.mqh"
#include "CALCompressionHistory.mqh"
#include "CALCompressionScheduler.mqh"
#include "CALGreedyDeltaMatching.mqh"
#include "..\\core\\CALContext.mqh"
#include "..\\positions\\CALPositionBook.mqh"

class CALCompressionEngine
{
private:
   CALLockCompression m_lock;
   CALCompressionHistory m_history;
   CALCompressionScheduler m_scheduler;
   CALGreedyDeltaMatching m_match;
   double m_alpha;
   int m_trigger_levels;
   int m_max_levels;
   double m_k;

public:
   CALCompressionEngine() : m_alpha(0.5), m_trigger_levels(8), m_max_levels(30), m_k(1.3) {}

   void SetAlpha(const double alpha){ m_alpha=(alpha>0.0 && alpha<=1.0 ? alpha : 0.5); }
   void SetTriggerLevels(const int levels){ m_trigger_levels=(levels>0?levels:8); }
   void SetMaxLevels(const int levels){ m_max_levels=(levels>0?levels:30); }
   void SetGeometryK(const double k){ m_k=(k>0.0?k:1.3); }

   int MaxLevels() const { return m_max_levels; }
   int HistorySize() const { return m_history.Size(); }
   CALCompressionEvent LastEvent() const { return m_history.Last(); }
   void SetScheduleEveryTicks(const int n){ m_scheduler.SetEveryTicks(n); }
   void ResetHistory(){ m_history.Reset(); }

   bool ShouldTrigger(const CALPositionBook &book,const double margin,const double equity,const bool safe_active) const
   {
      const int n=book.Size();
      if(n>m_trigger_levels) return true;
      if(n>=m_max_levels) return true;

      if(margin>1e-12)
      {
         const double margin_level=(equity/margin)*100.0;
         if(margin_level<200.0) return true;
      }

      if(safe_active) return true;
      return false;
   }

   bool ProcessCompression(CALPositionBook &book,CALStreamContext &ctx,const double equity,const bool safe_rescue)
   {
      if(!m_scheduler.ShouldRun()) return false;
      if(!ShouldTrigger(book,ctx.margin,equity,safe_rescue)) return false;

      const int levels_before=book.Size();
      const double delta_before=book.EffectiveDelta();
      const double margin_before=ctx.margin;
      if(levels_before<=0) return false;

      if(levels_before>m_max_levels)
         book.TrimTail(levels_before-m_max_levels);

      // TYPE-C lock compression + geometry rebuild.
      if(!m_lock.Compress(book,m_alpha)) return false;
      if(!book.RebuildGeometryLots(m_k,1e-12)) return false;

      const int levels_after=book.Size();
      const double delta_after=book.EffectiveDelta();
      const double margin_after=margin_before*m_alpha;

      ctx.net_delta=delta_after;
      ctx.exposure*=m_alpha;
      ctx.margin=margin_after;

      CALCompressionEvent ev;
      ev.timestamp=(long)TimeCurrent();
      ev.levels_before=levels_before;
      ev.levels_after=levels_after;
      ev.delta_before=delta_before;
      ev.delta_after=delta_after;
      ev.margin_before=margin_before;
      ev.margin_after=margin_after;
      m_history.Add(ev);
      return true;
   }

   bool ValidateGreedyMatching(const double &buy_lots[],const double &sell_lots[],double &delta_before,double &delta_after) const
   {
      CLockPair pairs[];
      return m_match.Match(buy_lots,sell_lots,pairs,delta_before,delta_after);
   }
};

#endif
