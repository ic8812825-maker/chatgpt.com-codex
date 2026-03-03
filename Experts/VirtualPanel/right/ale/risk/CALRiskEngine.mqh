#ifndef __CALRISKENGINE_MQH__
#define __CALRISKENGINE_MQH__

#include "..\\interfaces\\IALRiskModel.mqh"
#include "..\\core\\CALContext.mqh"
#include "..\\exposure\\CALExposureFlow.mqh"
#include "CALWorstCase.mqh"
#include "CALMarginModel.mqh"
#include "CALDrawdownModel.mqh"
#include "CALSafeMode.mqh"

class CALRiskEngine : public IALRiskModel
{
private:
   int m_direction;
   CALWorstCase m_worst;
   CALMarginModel m_margin;
   CALDrawdownModel m_dd;
   CALSafeMode m_safe;
public:
   void Init(const int direction){ m_direction=direction; }

   virtual double CalculateDD(const double pnl,const double peak) const
   {
      return m_dd.Drawdown(peak,peak+pnl);
   }

   virtual bool SAFE(const double drawdown,const double limit) const
   {
      return (m_direction==ALE_FLOW_BUY ? m_safe.TriggerBuy(drawdown,limit) : m_safe.TriggerSell(drawdown,limit));
   }


   double MarginBuy(const double price,const double lots,const double leverage,const double contract_size) const
   {
      return m_margin.MarginBuy(price,lots,leverage,contract_size);
   }

   double MarginSell(const double price,const double lots,const double leverage,const double contract_size) const
   {
      return m_margin.MarginSell(price,lots,leverage,contract_size);
   }

   double WorstBuy(const double pnl,const double shock) const { return m_worst.EvaluateBuy(pnl,shock); }
   double WorstSell(const double pnl,const double shock) const { return m_worst.EvaluateSell(pnl,shock); }

   void Evaluate(CALContext &ctx,const CALExposureFlow &exposure,const double price,const double lots,const double leverage,const double contract_size,const double peak_equity)
   {
      ctx.drawdown=CalculateDD(ctx.pnl,peak_equity);
      ctx.margin=(m_direction==ALE_FLOW_BUY ? m_margin.MarginBuy(price,lots,leverage,contract_size) : m_margin.MarginSell(price,lots,leverage,contract_size));

      const double worst=(m_direction==ALE_FLOW_BUY ? m_worst.EvaluateBuy(ctx.pnl,MathAbs(exposure.Convexity())) : m_worst.EvaluateSell(ctx.pnl,MathAbs(exposure.Convexity())));
      if(worst<ctx.pnl) ctx.drawdown=MathMax(ctx.drawdown,MathAbs(worst)/(MathAbs(peak_equity)+1e-8));

      if(exposure.Convexity()<0.0) ctx.drawdown=MathMax(ctx.drawdown,0.30);
   }

   CALRiskEngine(){ Init(ALE_FLOW_BUY); }
};

#endif
