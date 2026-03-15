#ifndef __CALRISKENGINE_MQH__
#define __CALRISKENGINE_MQH__

#include "..\\interfaces\\IALRiskModel.mqh"
#include "..\\core\\CALContext.mqh"
#include "..\\config\\CALRiskConfig.mqh"
#include "..\\exposure\\CALExposureFlow.mqh"
#include "..\\math\\CALReturnProbability.mqh"
#include "..\\math\\CALPhaseDiagram.mqh"
#include "CALWorstCase.mqh"
#include "CALMarginModel.mqh"
#include "CALDrawdownModel.mqh"
#include "CALSafeMode.mqh"

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
   CALRiskConfig m_cfg;
   CALWorstCase m_worst;
   CALMarginModel m_margin;
   CALDrawdownModel m_dd;
   CALSafeMode m_safe;
   CALReturnProbability m_prob;
   CALPhaseDiagram m_phase;

public:
   void Init(const int direction,const CALRiskConfig &cfg)
   {
      m_direction=direction;
      m_cfg=cfg;
      m_safe.SetParams(m_cfg.alpha,m_cfg.beta,m_cfg.gamma,m_cfg.k);
   }

   void SetConfig(const CALRiskConfig &cfg)
   {
      m_cfg=cfg;
      m_safe.SetParams(m_cfg.alpha,m_cfg.beta,m_cfg.gamma,m_cfg.k);
   }

   virtual double CalculateDD(const double pnl,const double peak) const
   {
      return MathMax(0.0,-pnl);
   }

   virtual bool SAFE(const double drawdown,const double limit) const
   {
      return (m_direction==ALE_FLOW_BUY ? m_safe.TriggerBuy(drawdown,limit) : m_safe.TriggerSell(drawdown,limit));
   }

   double SafeL0(const double equity) const
   {
      const double alpha=MathMin(0.85,MathMax(0.5,m_cfg.growth_g));
      const double k=MathMax(1e-6,m_cfg.k);
      const double R=MathMax(1e-6,m_cfg.grid_step_R);
      const double denom=R*(k + alpha/MathPow(1.0-alpha,2));
      if(denom<=0.0) return 0.0;
      return equity*MathMax(0.01,MathMin(0.05,m_cfg.risk_fraction))/denom;
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
      report.worst_dd=MathMax(report.worst_dd,dd_wc);

      report.dd_probability=m_prob.HitLevelGBM(price,p_min,0.0,m_cfg.sigma);

      const double denom=MathMax(1e-12,equity*m_cfg.dd_max);
      report.stress_ratio=report.worst_dd/denom;

      const double margin_level=(report.margin>1e-12 ? (equity/report.margin)*100.0 : 1e9);
      const double atr=MathAbs(price-p_min)/MathMax(1e-12,price);
      const double spread=MathAbs(price-pnl_min)-MathAbs(price-pnl_max);
      const double p_return=1.0-report.dd_probability;

      const bool trigger_safe=m_safe.EvaluateTriggers(margin_level,m_cfg.min_margin_level,
                                                      report.worst_dd/MathMax(1e-12,equity),m_cfg.dd_max,
                                                      atr,m_cfg.atr_limit,
                                                      MathAbs(spread),m_cfg.spread_limit,
                                                      p_return,m_cfg.p_safe);

      const bool phase_safe=m_safe.EvaluatePhase(report.margin,report.worst_dd,ctx.net_delta,ctx.gamma);
      const PhaseState phase_state=m_phase.DeterminePhase(m_cfg.growth_g,m_cfg.k,m_cfg.grid_step_R,SafeL0(equity));
      const bool explosive=(phase_state==PHASE_EXPLOSIVE) || (!m_phase.IsStable(m_cfg.k,m_cfg.growth_g,m_cfg.sigma));

      report.safe_triggered=(report.stress_ratio>m_cfg.stress_limit)
                         || (report.dd_probability>m_cfg.dd_prob_limit)
                         || (report.worst_dd>equity*m_cfg.dd_max)
                         || phase_safe
                         || trigger_safe
                         || explosive;
      return report;
   }

   CALRiskEngine(){ m_cfg.SetDefaults(); Init(ALE_FLOW_BUY,m_cfg); }
};

#endif
