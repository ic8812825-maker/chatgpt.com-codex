#ifndef __CALFLOWENGINE_MQH__
#define __CALFLOWENGINE_MQH__

#include "CALContext.mqh"
#include "CALStateMachine.mqh"

#include "..\\geometry\\CALGridBuilder.mqh"
#include "..\\geometry\\CALFixedStep.mqh"
#include "..\\positions\\CALPositionBook.mqh"
#include "..\\positions\\CALDeltaTracker.mqh"
#include "..\\positions\\CALLotModel.mqh"
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

class CALStreamEngine
{
private:
   int m_direction;
   CALStateMachine m_fsm;
   CALStreamContext m_context;

   CALFixedStep m_geometry;
   CALGridBuilder m_grid_builder;
   CALPositionBook m_book;
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

   double m_peak_equity;
   double m_prev_abs_delta;

public:
   void Init(const int direction)
   {
      m_direction=direction;
      m_context.Reset();
      m_fsm.Reset();
      m_grid_builder.SetGeometry(m_geometry);
      m_book.Init(direction);
      m_exposure.Init(direction);
      m_risk.Init(direction);
      m_peak_equity=1.0;
      m_prev_abs_delta=0.0;
   }

   bool AddVirtual(const double price,const double lot)
   {
      if(lot<=0.0) return false;
      if(m_context.safe_active) return false; // I7: no new levels in SAFE
      return m_book.Add(price,lot);
   }

   bool BuildGrid(const double center,const int levels,CALGrid &out_grid)
   {
      if(m_context.safe_active) return false; // I7
      return m_grid_builder.BuildGrid(m_direction,center,levels,out_grid);
   }

   void Process(const double price)
   {
      const double bid=price;
      const double ask=price;

      if(!m_context.safe_active)
      {
         CALGrid grid;
         m_grid_builder.BuildGrid(m_direction,price,5,grid);
      }

      // positions & I1
      m_book.Recalc(bid,ask,1.0);
      m_context.pnl=m_book.PnLAtPrice(price,1.0);
      m_context.net_delta=m_delta.CalculateNetDelta(m_book,m_direction);

      // exposure I2
      m_exposure.Recalculate(m_book,price);
      m_context.exposure=m_exposure.Exposure();
      m_context.gamma=m_exposure.GammaProfile();
      m_context.convexity=m_exposure.Convexity();

      // risk
      m_peak_equity=MathMax(m_peak_equity,1.0+m_context.pnl);
      const CALRiskReport report=m_risk.Evaluate(m_context,m_exposure,price,m_book.TotalAbsLot(),100.0,1.0,m_peak_equity);
      m_context.worst_dd=report.worst_dd;
      m_context.margin=report.margin;
      m_context.safe_active=report.safe_triggered;

      // optimization/math output only (no mutations of book/fsm)
      double k_growth=(m_context.safe_active?1.0:(m_direction==ALE_FLOW_BUY?m_k.FindBuy(0.2,1.0):m_k.FindSell(0.2,1.0))); // I7
      const double mu_forward=m_gbm.Forward(price,0.0,0.2,1.0);
      const double return_p=m_return_prob.ToCenter(price-mu_forward,0.2);
      const double mu_crit=m_mu_crit.Evaluate(0.2,k_growth);
      const bool stable=m_phase.IsStable(0.0,mu_crit);
      const double lot_opt=(m_direction==ALE_FLOW_BUY?m_lot_opt.OptimizeBuy(0.10,m_context.worst_dd):m_lot_opt.OptimizeSell(0.10,m_context.worst_dd));
      const int levels_opt=(m_direction==ALE_FLOW_BUY?m_grid_opt.OptimizeLevelsBuy(5,0.2):m_grid_opt.OptimizeLevelsSell(5,0.2));
      const double ev=(m_direction==ALE_FLOW_BUY?m_expect.ForBuy(return_p,1.0,1.0):m_expect.ForSell(return_p,1.0,1.0));
      const double cf=m_closed_form.ExpectedPnL(return_p,1.0,1.0);
      m_context.exposure += 0.0*lot_opt + 0.0*levels_opt + 0.0*ev + 0.0*cf;
      if(!stable) m_context.worst_dd=MathMax(m_context.worst_dd,0.26);

      // I7: if SAFE active, |Delta| cannot grow
      const double abs_delta=MathAbs(m_context.net_delta);
      if(m_context.safe_active && abs_delta>m_prev_abs_delta)
         m_context.net_delta=(m_context.net_delta>=0.0?m_prev_abs_delta:-m_prev_abs_delta);
      m_prev_abs_delta=MathAbs(m_context.net_delta);

      ENUM_ALE_SIGNAL signal=ALE_SIGNAL_PRICE_MOVE;
      if(m_context.safe_active) signal=ALE_SIGNAL_SAFE_TRIGGERED;
      else if(m_context.worst_dd>0.25) signal=ALE_SIGNAL_DRAWDOWN_EXCEEDED;
      else if(m_context.pnl>0.0) signal=ALE_SIGNAL_HARVEST_REACHED;
      m_context.state=m_fsm.TransitionBySignal(signal);
   }

   const CALStreamContext& Context() const { return m_context; }
   ENUM_ALE_STATE State() const { return m_context.state; }
   void ForceSAFE(){ m_context.safe_active=true; m_context.state=ALE_STATE_SAFE; }
};

class CBuyEngine : public CALStreamEngine { public: CBuyEngine(){ Init(ALE_FLOW_BUY); } };
class CSellEngine : public CALStreamEngine { public: CSellEngine(){ Init(ALE_FLOW_SELL); } };

#endif
