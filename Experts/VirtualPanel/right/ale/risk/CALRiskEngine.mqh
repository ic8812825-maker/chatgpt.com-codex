#ifndef __CALRISKENGINE_MQH__
#define __CALRISKENGINE_MQH__

#include "..\\interfaces\\IALRiskModel.mqh"
#include "..\\core\\CALContext.mqh"
#include "..\\exposure\\CALExposureFlow.mqh"
#include "CALWorstCase.mqh"
#include "CALMarginModel.mqh"
#include "CALDrawdownModel.mqh"
#include "CALSafeMode.mqh"

struct CALRiskReport
{
   double worst_dd;
   double margin;
   bool safe_triggered;

   void Reset()
   {
      worst_dd=0.0;
      margin=0.0;
      safe_triggered=false;
   }
};

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

   CALRiskReport Evaluate(const CALStreamContext &ctx,const CALExposureFlow &exposure,const double price,const double lots,const double leverage,const double contract_size,const double peak_equity)
   {
      CALRiskReport report;
      report.Reset();

      report.worst_dd=CalculateDD(ctx.pnl,peak_equity);
      report.margin=(m_direction==ALE_FLOW_BUY ? m_margin.MarginBuy(price,lots,leverage,contract_size) : m_margin.MarginSell(price,lots,leverage,contract_size));

      const double worst=(m_direction==ALE_FLOW_BUY ? m_worst.EvaluateBuy(ctx.pnl,MathAbs(exposure.Convexity())) : m_worst.EvaluateSell(ctx.pnl,MathAbs(exposure.Convexity())));
      if(worst<ctx.pnl)
         report.worst_dd=MathMax(report.worst_dd,MathAbs(worst)/(MathAbs(peak_equity)+1e-8));

      if(exposure.Convexity()<0.0)
         report.worst_dd=MathMax(report.worst_dd,0.30);

      report.safe_triggered=SAFE(report.worst_dd,0.25) || report.margin<=0.0 || exposure.Convexity()<0.0;
      return report;
   }

   CALRiskEngine(){ Init(ALE_FLOW_BUY); }
};

#endif
