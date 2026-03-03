#ifndef __CALEXPOSUREFLOW_MQH__
#define __CALEXPOSUREFLOW_MQH__

class CALExposureFlow
{
private:
   double m_buy_exposure;
   double m_sell_exposure;
public:
   void Reset(){ m_buy_exposure=0.0; m_sell_exposure=0.0; }
   void UpdateBuy(const double lots,const double price){ m_buy_exposure=lots*price; }
   void UpdateSell(const double lots,const double price){ m_sell_exposure=lots*price; }
   double BuyExposure() const { return m_buy_exposure; }
   double SellExposure() const { return m_sell_exposure; }
   CALExposureFlow(){ Reset(); }
};

#endif
