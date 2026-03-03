#ifndef __TESTRISK_MQH__
#define __TESTRISK_MQH__

#include "..\ale\risk\CALRiskEngine.mqh"

bool TestRisk_WorstDDMargin()
{
   CALRiskEngine risk;
   const double dd=risk.CalculateDD(-100.0,1000.0);
   const double m_buy=risk.MarginBuy(1.1000,0.5,100.0,100000.0);
   const double m_sell=risk.MarginSell(1.1000,0.5,100.0,100000.0);
   if(dd<=0.0) return false;
   if(m_buy<=0.0 || m_sell<=0.0) return false;
   if(!risk.SAFE(0.30,0.25)) return false;
   return true;
}

#endif
