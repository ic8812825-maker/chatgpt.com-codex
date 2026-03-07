#ifndef __CALRISKENGINE_MQH__
#define __CALRISKENGINE_MQH__

#include "..\\interfaces\\IALRiskModel.mqh"
#include "..\\core\\CALContext.mqh"
#include "..\\exposure\\CALExposureFlow.mqh"
#include "..\\math\\CALReturnProbability.mqh"
#include "CALWorstCase.mqh"
#include "CALMarginModel.mqh"
#include "CALDrawdownModel.mqh"
#include "CALSafeMode.mqh"
#include "..\\config\\CALRiskConfig.mqh"

struct CALRiskReport
{
   double worst_dd;
   double margin;
   double dd_probability;
   double stress_ratio;
   bool safe_triggered;

   void Reset()
   {
      worst_dd=0.0;
      margin=0.0;
      dd_probability=0.0;
      stress_ratio=0.0;
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
   CALReturnProbability m_prob;
   CALRiskConfig m_cfg;
public:
   void Init(const int direction){ m_direction=direction; m_cfg.SetDefaults(); m_safe.SetParams(m_cfg.SAFE_ALPHA,m_cfg.SAFE_BETA,m_cfg.SAFE_GAMMA,m_cfg.SAFE_K); }

   void SetConfig(const CALRiskConfig &cfg){ m_cfg=cfg; m_cfg.SyncAliases(); m_safe.SetParams(m_cfg.SAFE_ALPHA,m_cfg.SAFE_BETA,m_cfg.SAFE_GAMMA,m_cfg.SAFE_K); }
   CALRiskConfig Config() const { return m_cfg; }

   virtual double CalculateDD(const double pnl,const double peak) const
   {
      return m_dd.Drawdown(peak,peak+pnl);
   }

   virtual bool SAFE(const double drawdown,const double limit) const
   {
      return (m_direction==ALE_FLOW_BUY ? m_safe.TriggerBuy(drawdown,limit) : m_safe.TriggerSell(drawdown,limit));
   }

   CALRiskReport Evaluate(const CALStreamContext &ctx,const CALExposureFlow &exposure,const double price,const double lots,const double leverage,const double contract_size,const double equity)
   {
      CALRiskReport report;
      report.Reset();

      report.worst_dd=CalculateDD(ctx.pnl,equity);
      report.margin=(m_direction==ALE_FLOW_BUY ? m_margin.MarginBuy(price,lots,leverage,contract_size) : m_margin.MarginSell(price,lots,leverage,contract_size));

      const double p_min=price*0.90;
      const double p_max=price*1.10;
      const double pnl_min=ctx.pnl + exposure.DeltaSurface()*(p_min-price);
      const double pnl_max=ctx.pnl + exposure.DeltaSurface()*(p_max-price);
      const double dd_wc=(m_direction==ALE_FLOW_BUY ? m_worst.EvaluateBuy(pnl_min,pnl_max) : m_worst.EvaluateSell(pnl_min,pnl_max));
      report.worst_dd=MathMax(report.worst_dd,dd_wc/(MathAbs(equity)+1e-8));

      const double mu=0.0;
      const double sigma=0.2;
      report.dd_probability=m_prob.HitLevelGBM(price,p_min,mu,sigma);

      const double dd_max=(m_cfg.MAX_DRAWDOWN>0.0?m_cfg.MAX_DRAWDOWN:0.30);
      report.stress_ratio=report.worst_dd/(dd_max+1e-8);

      const bool phase_safe=m_safe.Evaluate(report.margin,report.worst_dd,ctx.net_delta,ctx.gamma);
      const double stress_limit=(m_cfg.STRESS_LIMIT>0.0?m_cfg.STRESS_LIMIT:1.0);
      report.safe_triggered=(report.stress_ratio>stress_limit) || (report.dd_probability>m_cfg.DD_PROB_LIMIT) || (report.worst_dd>dd_max) || phase_safe;
      return report;
   }

   CALRiskEngine(){ Init(ALE_FLOW_BUY); }
};

#endif
