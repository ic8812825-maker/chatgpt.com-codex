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
   }

   void AddVirtual(const double price,const double lot)
   {
      m_book.Add(price,lot);
   }

   bool BuildGrid(const double center,const int levels,CALGrid &out_grid)
   {
      return m_grid_builder.BuildGrid(m_direction,center,levels,out_grid);
   }

   void Process(const double bid,const double ask)
   {
      const double mark=(m_direction==ALE_FLOW_BUY ? ask : bid);

      // 1) Geometry
      CALGrid grid;
      m_grid_builder.BuildGrid(m_direction,mark,5,grid);

      // 2) Positions
      m_book.Recalc(bid,ask,100000.0);
      m_context.pnl=m_book.TotalPnL();
      m_context.net_delta=m_delta.CalculateNetDelta(m_book,m_direction);

      // 3) Exposure
      m_exposure.Recalculate(m_book,mark);
      m_context.exposure=m_exposure.Exposure();

      // 4) Risk
      m_peak_equity=MathMax(m_peak_equity,1.0+m_context.pnl);
      const CALRiskReport report=m_risk.Evaluate(m_context,m_exposure,mark,m_book.TotalLot(),(double)AccountInfoInteger(ACCOUNT_LEVERAGE),100000.0,m_peak_equity);
      m_context.worst_dd=report.worst_dd;
      m_context.margin=report.margin;

      // 5) Optimization + 6) Math (no direct side effects on Book/FSM)
      const double mu_forward=m_gbm.Forward(mark,0.0,0.2,1.0);
      const double return_p=m_return_prob.ToCenter(mark-mu_forward,0.2);
      const double opt_k=(m_direction==ALE_FLOW_BUY ? m_k.FindBuy(0.2,1.0) : m_k.FindSell(0.2,1.0));
      const double mu_crit=m_mu_crit.Evaluate(0.2,opt_k);
      const bool stable=m_phase.IsStable(0.0,mu_crit);
      const double lot_opt=(m_direction==ALE_FLOW_BUY ? m_lot_opt.OptimizeBuy(0.10,m_context.worst_dd) : m_lot_opt.OptimizeSell(0.10,m_context.worst_dd));
      const int levels_opt=(m_direction==ALE_FLOW_BUY ? m_grid_opt.OptimizeLevelsBuy(5,0.2) : m_grid_opt.OptimizeLevelsSell(5,0.2));
      const double ev=(m_direction==ALE_FLOW_BUY ? m_expect.ForBuy(return_p,100.0,50.0) : m_expect.ForSell(return_p,100.0,50.0));
      const double cf=m_closed_form.ExpectedPnL(return_p,100.0,50.0);

      if(!stable)
         m_context.worst_dd=MathMax(m_context.worst_dd,0.26);
      m_context.exposure += 0.0*lot_opt + 0.0*levels_opt + 0.0*ev + 0.0*cf;

      if(m_book.Size()>0)
      {
         const double sample=(m_direction==ALE_FLOW_BUY ? m_lot_model.LotForBuyLevel(0,0.10) : m_lot_model.LotForSellLevel(0,0.10));
         m_context.exposure += 0.0*sample;
      }

      // 7) FSM from signals only
      ENUM_ALE_SIGNAL signal=ALE_SIGNAL_PRICE_MOVE;
      if(report.safe_triggered)
         signal=ALE_SIGNAL_SAFE_TRIGGERED;
      else if(m_context.worst_dd>0.25)
         signal=ALE_SIGNAL_DRAWDOWN_EXCEEDED;
      else if(m_context.pnl>0.0)
         signal=ALE_SIGNAL_HARVEST_REACHED;

      m_context.state=m_fsm.Transition(signal);
   }

   CALStreamContext Context() const { return m_context; }
   ENUM_ALE_STATE State() const { return m_context.state; }
};

class CBuyEngine : public CALStreamEngine
{
public:
   CBuyEngine(){ Init(ALE_FLOW_BUY); }
};

class CSellEngine : public CALStreamEngine
{
public:
   CSellEngine(){ Init(ALE_FLOW_SELL); }
};

#endif
