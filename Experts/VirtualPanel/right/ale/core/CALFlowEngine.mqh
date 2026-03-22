#ifndef __CALFLOWENGINE_MQH__
#define __CALFLOWENGINE_MQH__

#include "CALContext.mqh"
#include "CALStateMachine.mqh"
#include "..\\config\\CALRiskConfig.mqh"

#include "..\\geometry\\CALGridBuilder.mqh"
#include "..\\geometry\\CALFixedStep.mqh"
#include "..\\positions\\CALPositionBook.mqh"
#include "..\\positions\\CALDeltaTracker.mqh"
#include "..\\positions\\CALLotModel.mqh"
#include "..\\compression\\CALCompressionEngine.mqh"
#include "..\\exposure\\CALExposureFlow.mqh"
#include "..\\risk\\CALRiskEngine.mqh"
#include "..\\math\\CALGBMModel.mqh"
#include "..\\math\\CALReturnProbability.mqh"
#include "..\\math\\CALCriticalMu.mqh"
#include "..\\math\\CALPhaseDiagram.mqh"
#include "..\\math\\CALClosedForm.mqh"
#include "..\\optimization\\CALOptimalK.mqh"
#include "..\\optimization\\CALLotOptimizer.mqh"
#include "..\\optimization\\CALGridOptimizer.mqh"
#include "..\\optimization\\CALExpectationModel.mqh"
#include "..\\lyapunov\\CALLyapunovToolkit.mqh"

class CALStreamEngine
{
private:
   int m_direction;
   CALRiskConfig m_cfg;
   CALStateMachine m_fsm;
   CALStreamContext m_context;

   CALFixedStep m_geometry;
   CALGridBuilder m_grid_builder;
   CALPositionBook m_book;
   CALCompressionEngine m_compression;
   CALExposureFlow m_exposure;
   CALRiskEngine m_risk;

   CALDeltaTracker m_delta;
   CALLotModel m_lot_model;
   CALGBMModel m_gbm;
   CALReturnProbability m_return_prob;
   CALCriticalMu m_mu_crit;
   CALPhaseDiagram m_phase;
   CALClosedForm m_closed_form;

   CALOptimalK m_k;
   CALLotOptimizer m_lot_opt;
   CALGridOptimizer m_grid_opt;
   CALExpectationModel m_expect;

   CALLyapunovFunctional m_lyap;
   CALLyapunovState m_prev_lyap_state;
   bool m_has_lyap_prev;

   double m_equity;
   double m_prev_abs_delta;
   double m_cum_volume;

private:
   CALLyapunovState BuildLyapunovState(const double price) const
   {
      CALLyapunovState s;
      const double dd_ratio=MathMax(0.0,-m_context.pnl)/MathMax(1.0,m_equity);
      const double margin_usage=m_context.margin/MathMax(1.0,m_equity);
      const double depth=(double)m_book.Size();

      s.drawdown=dd_ratio;
      s.exposure=m_book.TotalAbsLot();
      s.margin_usage=margin_usage;
      s.depth=depth;
      s.distance_to_be=MathAbs(m_context.net_delta)*MathMax(1.0,price)*1000.0;
      s.unrealized_loss=MathMax(0.0,-m_context.pnl);
      s.tail_effect=CALLyapunovTailEffect::EstimateRiskProxy(margin_usage,depth,s.exposure);
      s.pnl_contribution=CALLyapunovMetrics::PnLContribution(m_context.pnl,0.0,m_equity);
      return s;
   }

   void UpdateLyapunovTelemetry(const double price)
   {
      const CALLyapunovState s=BuildLyapunovState(price);
      const double v=m_lyap.V(s);
      const double dv=(m_has_lyap_prev ? m_lyap.DeltaV(m_prev_lyap_state,s) : 0.0);
      m_context.lyapunov_prev_v=m_context.lyapunov_v;
      m_context.lyapunov_v=v;
      m_context.lyapunov_delta=dv;

      if(v>0.85 || dv>0.03) m_context.lyapunov_risk_level=3;
      else if(v>0.70 || dv>0.015) m_context.lyapunov_risk_level=2;
      else if(v>0.55 || dv>0.005) m_context.lyapunov_risk_level=1;
      else m_context.lyapunov_risk_level=0;

      m_prev_lyap_state=s;
      m_has_lyap_prev=true;
   }

   bool LyapunovAllowsExpansion() const
   {
      if(m_context.lyapunov_risk_level>=3) return false;
      if(m_context.lyapunov_risk_level>=2 && m_context.lyapunov_delta>0.0) return false;
      return true;
   }

   void ApplyLyapunovControl(const double price)
   {
      m_context.lyapunov_action_code=0;

      if(m_context.lyapunov_risk_level>=3)
      {
         RequestCompression(price,true);
         m_context.safe_active=true;
         m_context.state=m_fsm.TransitionBySignal(ALE_SIGNAL_LYAPUNOV_CRITICAL);
         m_context.lyapunov_action_code=3;
         return;
      }

      if(m_context.lyapunov_risk_level>=2)
      {
         RequestCompression(price,false);
         m_context.state=m_fsm.TransitionBySignal(ALE_SIGNAL_LYAPUNOV_GUARD);
         m_context.lyapunov_action_code=2;
         return;
      }

      if(m_context.lyapunov_risk_level==1)
      {
         m_context.lyapunov_action_code=1;
      }
   }

public:
   void Init(const int direction,const CALRiskConfig &cfg)
   {
      m_direction=direction;
      m_cfg=cfg;
      m_context.Reset();
      m_fsm.Reset();
      m_grid_builder.SetGeometry(m_geometry);
      m_book.Init(direction);
      m_compression.SetAlpha(0.5);
      m_compression.SetTriggerLevels(8);
      m_compression.SetMaxLevels(30);
      m_exposure.Init(direction);
      m_risk.Init(direction,m_cfg);
      m_equity=m_cfg.initial_equity;
      m_prev_abs_delta=0.0;
      m_cum_volume=0.0;
      m_has_lyap_prev=false;
   }

   bool AddVirtual(const double price,const double lot)
   {
      if(lot<=0.0 || m_context.safe_active) return false;
      if(!LyapunovAllowsExpansion()) return false;
      if(m_book.Size()>=m_compression.MaxLevels())
      {
         RequestCompression(price,false);
         return false;
      }
      if(!m_lot_model.CanAddLevel(m_cum_volume,m_book.Size(),MathMax(1e-6,lot),m_cfg.growth_g)) return false;
      const bool ok=m_book.Add(price,lot);
      if(ok) m_cum_volume += MathAbs(lot);
      return ok;
   }

   bool BuildGrid(const double center,const int levels,CALGrid &out_grid)
   {
      if(m_context.safe_active) return false;
      return m_grid_builder.BuildGrid(m_direction,center,levels,out_grid);
   }

   bool RequestCompression(const double price,const bool rescue)
   {
      m_context.pnl=m_book.PnLAtPrice(price,1.0);
      m_context.net_delta=m_delta.CalculateNetDelta(m_book,m_direction);
      m_exposure.Recalculate(m_book,price);
      m_context.exposure=m_exposure.Exposure();

      const bool compressed=m_compression.ProcessCompression(m_book,m_context,m_equity,rescue);
      if(compressed)
      {
         m_context.state=m_fsm.TransitionBySignal(ALE_SIGNAL_COMPRESSION);
         m_context.net_delta=m_delta.CalculateNetDelta(m_book,m_direction);
      }
      return compressed;
   }

   bool PartialHarvest(const double price)
   {
      return RequestCompression(price,false);
   }

   void Process(const double price)
   {
      // STRICT PIPELINE: MarketTick -> Geometry -> Positions -> ALC Compression -> Exposure -> Risk -> Optimization -> Lyapunov feedback
      if(m_context.safe_active)
      {
         RequestCompression(price,true);
         m_context.state=m_fsm.TransitionBySignal(ALE_SIGNAL_SAFE_TRIGGERED);
         return;
      }

      CALGrid grid;
      m_grid_builder.BuildGrid(m_direction,price,5,grid);

      m_context.pnl=m_book.PnLAtPrice(price,1.0);
      m_context.net_delta=m_delta.CalculateNetDelta(m_book,m_direction);

      const bool compressed=RequestCompression(price,false);

      m_exposure.Recalculate(m_book,price);
      m_context.exposure=m_exposure.Exposure();
      m_context.gamma=m_exposure.GammaProfile();
      m_context.convexity=m_exposure.Convexity();

      const CALRiskReport report=m_risk.Evaluate(m_context,m_exposure,price,m_book.TotalAbsLot(),100.0,1.0,m_equity);
      m_context.worst_dd=report.worst_dd;
      m_context.margin=report.margin;
      m_context.safe_active=report.safe_triggered;

      UpdateLyapunovTelemetry(price);
      ApplyLyapunovControl(price);

      if(m_context.safe_active)
      {
         RequestCompression(price,true);
         m_context.state=m_fsm.TransitionBySignal(ALE_SIGNAL_SAFE_TRIGGERED);
         return;
      }

      const double k_growth=(m_direction==ALE_FLOW_BUY?m_k.FindBuy(m_cfg.sigma,1.0,m_cfg.growth_g):m_k.FindSell(m_cfg.sigma,1.0,m_cfg.growth_g));
      const double max_safe_vol=m_risk.SafeL0(m_equity);
      const double hedge_lot=m_k.HedgeLot(0.1,k_growth,max_safe_vol);

      const double mu_forward=m_gbm.Forward(price,0.0,m_cfg.sigma,m_cfg.dt);
      const double p_ret=m_return_prob.ToCenter(price-mu_forward,m_cfg.sigma);
      const double mu_crit=m_mu_crit.Evaluate(m_cfg.sigma,MathMax(1.0,k_growth));
      const bool stable=m_phase.IsStable(k_growth,m_cfg.growth_g,m_cfg.sigma);

      const double lot_opt=(m_direction==ALE_FLOW_BUY?m_lot_opt.OptimizeBuy(0.10,m_context.worst_dd,k_growth,m_cfg.growth_g,m_cfg.sigma):m_lot_opt.OptimizeSell(0.10,m_context.worst_dd,k_growth,m_cfg.growth_g,m_cfg.sigma));
      const int levels_opt=(m_direction==ALE_FLOW_BUY?m_grid_opt.OptimizeLevelsBuy(5,m_cfg.sigma,k_growth,m_cfg.growth_g):m_grid_opt.OptimizeLevelsSell(5,m_cfg.sigma,k_growth,m_cfg.growth_g));
      const double ev=(m_direction==ALE_FLOW_BUY?m_expect.ForBuy(p_ret,1.0,1.0):m_expect.ForSell(p_ret,1.0,1.0));
      const double cf=m_closed_form.ExpectedPnL(p_ret,1.0,1.0);

      // Lyapunov guard can damp optimization aggressiveness
      const double lyap_guard=(m_context.lyapunov_risk_level>=1 ? 0.5 : 1.0);
      m_context.exposure += 0.0*(lot_opt*lyap_guard + hedge_lot) + 0.0*levels_opt + 0.0*ev + 0.0*cf + 0.0*mu_crit;
      if(!stable) m_context.worst_dd=MathMax(m_context.worst_dd,m_cfg.dd_max);

      const double abs_delta=MathAbs(m_context.net_delta);
      if(abs_delta>m_prev_abs_delta)
         m_prev_abs_delta=abs_delta;

      ENUM_ALE_SIGNAL signal=ALE_SIGNAL_PRICE_MOVE;
      if(m_context.lyapunov_risk_level>=3)
         signal=ALE_SIGNAL_LYAPUNOV_CRITICAL;
      else if(m_context.lyapunov_risk_level>=2)
         signal=ALE_SIGNAL_LYAPUNOV_GUARD;
      else if(compressed)
         signal=ALE_SIGNAL_COMPRESSION;
      else if(m_context.pnl>=m_cfg.harvest_target)
         signal=ALE_SIGNAL_HARVEST_REACHED;
      else if(m_context.worst_dd>m_cfg.dd_max*m_equity)
         signal=ALE_SIGNAL_DRAWDOWN_EXCEEDED;
      m_context.state=m_fsm.TransitionBySignal(signal);
   }

   CALStreamContext Context() const { return m_context; }
   ENUM_ALE_STATE State() const { return m_context.state; }
   int Levels() const { return m_book.Size(); }
   int CompressionCount() const { return m_compression.HistorySize(); }
   void ForceSAFE(){ m_context.safe_active=true; m_context.state=ALE_STATE_SAFE; }
};

class CBuyEngine : public CALStreamEngine { public: CBuyEngine(){ CALRiskConfig cfg; Init(ALE_FLOW_BUY,cfg); } };
class CSellEngine : public CALStreamEngine { public: CSellEngine(){ CALRiskConfig cfg; Init(ALE_FLOW_SELL,cfg); } };

#endif
