#ifndef __CALCOMPRESSIONSCHEDULER_MQH__
#define __CALCOMPRESSIONSCHEDULER_MQH__

class CALCompressionScheduler
{
private:
   int m_every_ticks;
   int m_counter;

public:
   CALCompressionScheduler() : m_every_ticks(1), m_counter(0) {}

   void SetEveryTicks(const int value)
   {
      m_every_ticks=(value>0?value:1);
   }

   bool ShouldRun()
   {
      m_counter++;
      if(m_counter>=m_every_ticks)
      {
         m_counter=0;
         return true;
      }
      return false;
   }

   void Reset(){ m_counter=0; }
};

#endif
