#ifndef __CALDELTATRACKER_MQH__
#define __CALDELTATRACKER_MQH__

class CALDeltaTracker
{
private:
   double m_net_delta;
   double m_tail_slope;
public:
   void Reset(){ m_net_delta=0.0; m_tail_slope=0.0; }
   void Update(const double delta,const double slope){ m_net_delta=delta; m_tail_slope=slope; }
   double NetDelta() const { return m_net_delta; }
   double TailSlope() const { return m_tail_slope; }
   CALDeltaTracker(){ Reset(); }
};

#endif
