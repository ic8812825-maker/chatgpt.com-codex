#ifndef __TESTRISK_MQH__
#define __TESTRISK_MQH__

#include "..\\ale\\risk\\CALRiskEngine.mqh"

bool TestRisk_WorstDDMargin()
{
   CALRiskEngine risk_buy;
   CALRiskEngine risk_sell;
   risk_buy.Init(ALE_FLOW_BUY);
   risk_sell.Init(ALE_FLOW_SELL);

   const double dd_buy=risk_buy.CalculateDD(-100.0,1000.0);
   const double dd_sell=risk_sell.CalculateDD(-120.0,1000.0);
   const double m_buy=risk_buy.MarginBuy(1.1000,0.5,100.0,100000.0);
   const double m_sell=risk_sell.MarginSell(1.1000,0.5,100.0,100000.0);
   if(dd_buy<=0.0 || dd_sell<=0.0) return false;
   if(m_buy<=0.0 || m_sell<=0.0) return false;
   if(!risk_buy.SAFE(0.30,0.25)) return false;
   if(!risk_sell.SAFE(0.30,0.25)) return false;
   return true;
}

#endif
