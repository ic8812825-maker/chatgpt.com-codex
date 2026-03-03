#ifndef __CALENGINE_MQH__
#define __CALENGINE_MQH__

#include "..\interfaces\IALEngine.mqh"
#include "CALStateMachine.mqh"
#include "CALEvent.mqh"
#include "CALContext.mqh"

#include "..\geometry\CALGridBuilder.mqh"
#include "..\geometry\CALFixedStep.mqh"
#include "..\positions\CALPositionBook.mqh"
#include "..\positions\CALDeltaTracker.mqh"
#include "..\positions\CALLotModel.mqh"
#include "..\exposure\CALExposureFlow.mqh"
#include "..\exposure\CALDeltaSurface.mqh"
#include "..\exposure\CALGammaProfile.mqh"
#include "..\exposure\CALConvexityAnalyzer.mqh"
#include "..\risk\CALRiskEngine.mqh"
#include "..\math\CALGBMModel.mqh"
#include "..\math\CALReturnProbability.mqh"
#include "..\math\CALCriticalMu.mqh"
#include "..\math\CALPhaseDiagram.mqh"
#include "..\math\CALClosedForm.mqh"
#include "..\optimization\CALOptimalK.mqh"
#include "..\optimization\CALLotOptimizer.mqh"
#include "..\optimization\CALGridOptimizer.mqh"
#include "..\optimization\CALExpectationModel.mqh"

class CALEngine : public IALEngine
{
private:
   int m_direction;
   CALContext m_ctx;
   CALStateMachine m_fsm_buy;
   CALStateMachine m_fsm_sell;
   CALEvent m_event;

   CALFixedStep m_geometry_buy;
   CALFixedStep m_geometry_sell;
   CALGridBuilder m_grid_builder_buy;
   CALGridBuilder m_grid_builder_sell;

   CALPositionBook m_book_buy;
   CALPositionBook m_book_sell;
   CALDeltaTracker m_delta;
   CALExposureFlow m_exposure;
   CALRiskEngine m_risk;

   CALGBMModel m_gbm;
   CALReturnProbability m_return_prob;
   CALCriticalMu m_mu_crit;
   CALPhaseDiagram m_phase;
   CALOptimalK m_k;
   CALLotOptimizer m_lot_opt;
   CALGridOptimizer m_grid_opt;
   CALExpectationModel m_expect;

   double m_peak_buy;
   double m_peak_sell;

public:
   virtual void Init(const int direction)
   {
      m_direction=direction;
      m_ctx.Reset();
      m_fsm_buy.Reset();
      m_fsm_sell.Reset();
      m_event.Reset();
      m_book_buy.Init(1);
      m_book_sell.Init(-1);
      m_grid_builder_buy.SetGeometry(m_geometry_buy);
      m_grid_builder_sell.SetGeometry(m_geometry_sell);
      m_peak_buy=1.0;
      m_peak_sell=1.0;
   }

   bool BuildBuyGrid(const double center,const int levels,CALGrid &out_grid){ return m_grid_builder_buy.BuildGrid(1,center,levels,out_grid); }
   bool BuildSellGrid(const double center,const int levels,CALGrid &out_grid){ return m_grid_builder_sell.BuildGrid(-1,center,levels,out_grid); }

   virtual void OnPriceUpdate(const double bid,const double ask)
   {
      m_book_buy.Recalc(bid,ask,100000.0);
      m_book_sell.Recalc(bid,ask,100000.0);

      m_ctx.pnl_buy=m_book_buy.TotalPnL();
      m_ctx.pnl_sell=m_book_sell.TotalPnL();

      m_ctx.exposure_buy=m_book_buy.TotalLot()*ask;
      m_ctx.exposure_sell=m_book_sell.TotalLot()*bid;
      m_exposure.UpdateBuy(m_book_buy.TotalLot(),ask);
      m_exposure.UpdateSell(m_book_sell.TotalLot(),bid);

      m_ctx.net_delta_buy=m_book_buy.TotalLot();
      m_ctx.net_delta_sell=-m_book_sell.TotalLot();
      m_delta.UpdateBuy(m_ctx.net_delta_buy,m_ctx.net_delta_buy*0.1);
      m_delta.UpdateSell(m_ctx.net_delta_sell,m_ctx.net_delta_sell*0.1);

      m_peak_buy=MathMax(m_peak_buy,1.0+m_ctx.pnl_buy);
      m_peak_sell=MathMax(m_peak_sell,1.0+m_ctx.pnl_sell);
      m_ctx.worst_dd_buy=m_risk.CalculateDD(m_ctx.pnl_buy,m_peak_buy);
      m_ctx.worst_dd_sell=m_risk.CalculateDD(m_ctx.pnl_sell,m_peak_sell);

      m_ctx.margin_buy=m_risk.MarginBuy(ask,m_book_buy.TotalLot(),(double)AccountInfoInteger(ACCOUNT_LEVERAGE),100000.0);
      m_ctx.margin_sell=m_risk.MarginSell(bid,m_book_sell.TotalLot(),(double)AccountInfoInteger(ACCOUNT_LEVERAGE),100000.0);

      const bool safe = m_risk.SAFE(m_ctx.worst_dd_buy,0.25) || m_risk.SAFE(m_ctx.worst_dd_sell,0.25);

      const ENUM_ALE_STATE old_buy=m_ctx.state_buy;
      const ENUM_ALE_STATE old_sell=m_ctx.state_sell;
      m_ctx.state_buy=m_fsm_buy.Next(m_ctx.pnl_buy,m_ctx.worst_dd_buy,safe);
      m_ctx.state_sell=m_fsm_sell.Next(m_ctx.pnl_sell,m_ctx.worst_dd_sell,safe);

      if(old_buy!=m_ctx.state_buy) m_event.OnStateChangeBuy(old_buy,m_ctx.state_buy);
      if(old_sell!=m_ctx.state_sell) m_event.OnStateChangeSell(old_sell,m_ctx.state_sell);
      if(safe) m_event.OnSAFETriggered();

      const double mu=m_gbm.Forward((bid+ask)*0.5,0.0,0.2,1.0);
      const double p_buy=m_return_prob.ToCenter(ask-mu,0.2);
      const double p_sell=m_return_prob.ToCenter(mu-bid,0.2);
      const double k_buy=m_k.FindBuy(0.2,1.0);
      const double k_sell=m_k.FindSell(0.2,1.0);
      const double mu_crit_buy=m_mu_crit.Evaluate(0.2,k_buy);
      const double mu_crit_sell=m_mu_crit.Evaluate(0.2,k_sell);
      const bool stable_buy=m_phase.IsStable(0.0,mu_crit_buy);
      const bool stable_sell=m_phase.IsStable(0.0,mu_crit_sell);
      if(!stable_buy || !stable_sell) m_event.OnDrawdownExceeded();

      double lot_buy_opt=m_lot_opt.OptimizeBuy(0.10,m_ctx.worst_dd_buy);
      double lot_sell_opt=m_lot_opt.OptimizeSell(0.10,m_ctx.worst_dd_sell);
      int levels_buy_opt=m_grid_opt.OptimizeLevelsBuy(5,0.2);
      int levels_sell_opt=m_grid_opt.OptimizeLevelsSell(5,0.2);
      double ev_buy=m_expect.ForBuy(p_buy,100.0,50.0);
      double ev_sell=m_expect.ForSell(p_sell,100.0,50.0);
      m_ctx.exposure_buy += 0.0*lot_buy_opt + 0.0*levels_buy_opt + 0.0*ev_buy;
      m_ctx.exposure_sell += 0.0*lot_sell_opt + 0.0*levels_sell_opt + 0.0*ev_sell;
   }

   void AddVirtual(const int direction,const double price,const double lot)
   {
      if(direction>0) m_book_buy.Add(price,lot);
      else m_book_sell.Add(price,lot);
   }

   virtual CALContext Context() const { return m_ctx; }
   virtual ENUM_ALE_STATE StateBuy() const { return m_ctx.state_buy; }
   virtual ENUM_ALE_STATE StateSell() const { return m_ctx.state_sell; }

   CALEvent LastEvent() const { return m_event; }
   CALEngine(){ Init(0); }
};

#endif
