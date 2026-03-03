#ifndef __CALDELTATRACKER_MQH__
#define __CALDELTATRACKER_MQH__

class CALDeltaTracker
{
private:
   double m_net_delta_buy;
   double m_net_delta_sell;
   double m_tail_slope_buy;
   double m_tail_slope_sell;
public:
   void Reset(){ m_net_delta_buy=0.0; m_net_delta_sell=0.0; m_tail_slope_buy=0.0; m_tail_slope_sell=0.0; }
   void UpdateBuy(const double delta,const double slope){ m_net_delta_buy=delta; m_tail_slope_buy=slope; }
   void UpdateSell(const double delta,const double slope){ m_net_delta_sell=delta; m_tail_slope_sell=slope; }
   double NetDeltaBuy() const { return m_net_delta_buy; }
   double NetDeltaSell() const { return m_net_delta_sell; }
   CALDeltaTracker(){ Reset(); }
};

#endif
