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

class CALFlowEngine
{
private:
   int m_direction;
   CALContext m_context;
   CALStateMachine m_fsm;

   CALFixedStep m_geometry;
   CALGridBuilder m_grid_builder;
   CALPositionBook m_positions;
   CALDeltaTracker m_delta;
   CALLotModel m_lot_model;
   CALExposureFlow m_exposure;
   CALRiskEngine m_risk;

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
      m_positions.Init(direction);
      m_exposure.Init(direction);
      m_risk.Init(direction);
      m_peak_equity=1.0;
   }

   void AddVirtual(const double price,const double lot)
   {
      m_positions.Add(price,lot);
   }

   bool BuildGrid(const double center,const int levels,CALGrid &out_grid)
   {
      return m_grid_builder.BuildGrid(m_direction,center,levels,out_grid);
   }

   void Process(const double bid,const double ask)
   {
      const double mark=(m_direction==ALE_FLOW_BUY ? ask : bid);

      CALGrid grid;
      m_grid_builder.BuildGrid(m_direction,mark,5,grid);

      m_positions.Recalc(bid,ask,100000.0);
      m_context.pnl=m_positions.TotalPnL();
      m_context.net_delta=(m_direction==ALE_FLOW_BUY ? m_positions.TotalLot() : -m_positions.TotalLot());

      m_exposure.Recalculate(m_positions,mark);
      m_context.exposure=m_exposure.Exposure();

      m_peak_equity=MathMax(m_peak_equity,1.0+m_context.pnl);
      m_risk.Evaluate(m_context,m_exposure,mark,m_positions.TotalLot(),(double)AccountInfoInteger(ACCOUNT_LEVERAGE),100000.0,m_peak_equity);

      const bool safe_trigger=m_risk.SAFE(m_context.drawdown,0.25) || m_context.margin<=0.0 || m_exposure.Convexity()<0.0;
      m_fsm.Update(m_context,safe_trigger);

      const double mu_forward=m_gbm.Forward(mark,0.0,0.2,1.0);
      const double return_p=m_return_prob.ToCenter(mark-mu_forward,0.2);
      const double opt_k=(m_direction==ALE_FLOW_BUY ? m_k.FindBuy(0.2,1.0) : m_k.FindSell(0.2,1.0));
      const double mu_crit=m_mu_crit.Evaluate(0.2,opt_k);
      const bool stable=m_phase.IsStable(0.0,mu_crit);
      if(!stable)
         m_context.drawdown=MathMax(m_context.drawdown,0.26);

      const double lot_opt=(m_direction==ALE_FLOW_BUY ? m_lot_opt.OptimizeBuy(0.10,m_context.drawdown) : m_lot_opt.OptimizeSell(0.10,m_context.drawdown));
      const int levels_opt=(m_direction==ALE_FLOW_BUY ? m_grid_opt.OptimizeLevelsBuy(5,0.2) : m_grid_opt.OptimizeLevelsSell(5,0.2));
      const double ev=(m_direction==ALE_FLOW_BUY ? m_expect.ForBuy(return_p,100.0,50.0) : m_expect.ForSell(return_p,100.0,50.0));
      const double cf=m_closed_form.ExpectedPnL(return_p,100.0,50.0);

      m_context.exposure += 0.0*lot_opt + 0.0*levels_opt + 0.0*ev + 0.0*cf;
      m_delta.Update(m_context.net_delta,m_context.net_delta*0.1);

      // keep lot model available for future per-level sizing integration
      if(m_positions.Size()>0)
      {
         double sample=(m_direction==ALE_FLOW_BUY ? m_lot_model.LotForBuyLevel(0,0.10) : m_lot_model.LotForSellLevel(0,0.10));
         m_context.exposure += 0.0*sample;
      }
   }

   CALContext Context() const { return m_context; }
   ENUM_ALE_STATE State() const { return m_context.state; }
};

class CBuyEngine : public CALFlowEngine
{
public:
   CBuyEngine(){ Init(ALE_FLOW_BUY); }
};

class CSellEngine : public CALFlowEngine
{
public:
   CSellEngine(){ Init(ALE_FLOW_SELL); }
};

#endif
