#ifndef __CALCOMPRESSIONHISTORY_MQH__
#define __CALCOMPRESSIONHISTORY_MQH__

struct CALCompressionEvent
{
   long timestamp;
   int levels_before;
   int levels_after;
   double delta_before;
   double delta_after;
   double margin_before;
   double margin_after;
};

class CALCompressionHistory
{
private:
   CALCompressionEvent m_events[];

public:
   void Add(const CALCompressionEvent &ev)
   {
      const int n=ArraySize(m_events);
      ArrayResize(m_events,n+1);
      m_events[n]=ev;
   }

   int Size() const { return ArraySize(m_events); }

   CALCompressionEvent Last() const
   {
      CALCompressionEvent ev;
      ev.timestamp=0;
      ev.levels_before=0;
      ev.levels_after=0;
      ev.delta_before=0.0;
      ev.delta_after=0.0;
      ev.margin_before=0.0;
      ev.margin_after=0.0;

      const int n=ArraySize(m_events);
      if(n>0)
         ev=m_events[n-1];
      return ev;
   }

   void Reset()
   {
      ArrayResize(m_events,0);
   }
};

#endif
