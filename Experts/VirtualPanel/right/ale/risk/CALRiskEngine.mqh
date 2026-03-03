#ifndef __CALRISKENGINE_MQH__
#define __CALRISKENGINE_MQH__

#include "..\interfaces\IALRiskModel.mqh"
#include "CALWorstCase.mqh"
#include "CALMarginModel.mqh"
#include "CALDrawdownModel.mqh"
#include "CALSafeMode.mqh"

class CALRiskEngine : public IALRiskModel
{
private:
   CALWorstCase m_worst;
   CALMarginModel m_margin;
   CALDrawdownModel m_dd;
   CALSafeMode m_safe;
public:
   virtual double CalculateDD(const double pnl,const double peak) const { return m_dd.Drawdown(peak,peak+pnl); }
   virtual bool SAFE(const double drawdown,const double limit) const { return m_safe.TriggerBuy(drawdown,limit) || m_safe.TriggerSell(drawdown,limit); }
   double MarginBuy(const double price,const double lots,const double leverage,const double contract_size) const { return m_margin.MarginBuy(price,lots,leverage,contract_size); }
   double MarginSell(const double price,const double lots,const double leverage,const double contract_size) const { return m_margin.MarginSell(price,lots,leverage,contract_size); }
   double WorstBuy(const double pnl,const double shock) const { return m_worst.EvaluateBuy(pnl,shock); }
   double WorstSell(const double pnl,const double shock) const { return m_worst.EvaluateSell(pnl,shock); }
};

#endif
