#ifndef __TESTRISK_MQH__
#define __TESTRISK_MQH__

#include "..\\ale\\risk\\CALRiskEngine.mqh"
#include "..\\ale\\risk\\CALMarginModel.mqh"
#include "..\\ale\\risk\\CALWorstCase.mqh"
#include "..\\ale\\core\\CALContext.mqh"
#include "..\\ale\\exposure\\CALExposureFlow.mqh"
#include "..\\ale\\positions\\CALPositionBook.mqh"

bool NearRisk(const double a,const double b,const double eps=1e-9){ return MathAbs(a-b)<=eps; }

bool TestRisk_WorstDDMargin()
{
   CALRiskEngine risk;
   risk.Init(ALE_FLOW_BUY);

   const double lot_risk=(10000.0*0.02)/(200.0*10.0);
   if(!NearRisk(lot_risk,0.1,1e-12)) return false;

   CALMarginModel margin_model;
   const double m1=margin_model.MarginFromLots(1.0,100000.0,0.01);
   const double m2=margin_model.MarginFromLots(2.0,100000.0,0.01);
   const double m3=margin_model.MarginFromLots(3.0,100000.0,0.01);
   if(!(m1<m2 && m2<m3)) return false;

   CALWorstCase wc;
   const double dd=wc.DrawdownFromEndpoints(-120.0,40.0);
   if(!NearRisk(dd,120.0,1e-12)) return false;

   CALStreamContext ctx;
   ctx.Reset();
   ctx.pnl=-50.0;
   ctx.net_delta=0.2;
   ctx.gamma=-1.0;

   CALPositionBook book;
   book.Init(ALE_FLOW_BUY);
   book.Add(1.1000,0.1);
   CALExposureFlow exp;
   exp.Init(ALE_FLOW_BUY);
   exp.Recalculate(book,1.0);

   const CALRiskReport rep=risk.Evaluate(ctx,exp,1.0,0.1,100.0,1.0,10000.0);
   if(rep.margin<=0.0) return false;
   if(rep.stress_ratio<0.0) return false;

   return true;
}

bool TestRisk_ConfigThresholdsAffectSAFE()
{
   CALRiskEngine risk;
   risk.Init(ALE_FLOW_SELL);

   CALRiskConfig cfg;
   cfg.SetDefaults();
   cfg.MAX_DRAWDOWN=0.05;
   cfg.STRESS_LIMIT=0.7;
   cfg.DD_PROB_LIMIT=0.50;
   cfg.SyncAliases();
   risk.SetConfig(cfg);

   CALStreamContext ctx;
   ctx.Reset();
   ctx.pnl=-1000.0;
   ctx.net_delta=0.0;
   ctx.gamma=0.0;

   CALPositionBook book;
   book.Init(ALE_FLOW_SELL);
   book.Add(1.1000,0.2);

   CALExposureFlow exp;
   exp.Init(ALE_FLOW_SELL);
   exp.Recalculate(book,1.1000);

   const CALRiskReport strict_rep=risk.Evaluate(ctx,exp,1.1000,0.2,100.0,100000.0,10000.0);
   if(!strict_rep.safe_triggered) return false;

   cfg.MAX_DRAWDOWN=1.00;
   cfg.STRESS_LIMIT=2.0;
   cfg.DD_PROB_LIMIT=1.00;
   cfg.SAFE_ALPHA=0.0;
   cfg.SAFE_BETA=0.0;
   cfg.SAFE_GAMMA=0.0;
   cfg.SAFE_K=10.0;
   cfg.SyncAliases();
   risk.SetConfig(cfg);

   const CALRiskReport loose_rep=risk.Evaluate(ctx,exp,1.1000,0.2,100.0,100000.0,10000.0);
   if(loose_rep.stress_ratio>=strict_rep.stress_ratio) return false;

   return true;
}

bool TestRisk_ZeroEquityFinite()
{
   CALRiskEngine risk;
   risk.Init(ALE_FLOW_BUY);

   CALRiskConfig cfg;
   cfg.SetDefaults();
   cfg.SyncAliases();
   risk.SetConfig(cfg);

   CALStreamContext ctx;
   ctx.Reset();
   ctx.pnl=-10.0;
   ctx.net_delta=0.1;
   ctx.gamma=0.0;

   CALPositionBook book;
   book.Init(ALE_FLOW_BUY);
   book.Add(1.1000,0.1);

   CALExposureFlow exp;
   exp.Init(ALE_FLOW_BUY);
   exp.Recalculate(book,1.1000);

   const CALRiskReport rep=risk.Evaluate(ctx,exp,1.1000,0.1,100.0,100000.0,0.0);
   if(!MathIsValidNumber(rep.worst_dd) || !MathIsValidNumber(rep.stress_ratio)) return false;
   if(rep.worst_dd<0.0 || rep.stress_ratio<0.0) return false;
   return true;
}


bool TestRisk_GlobalSafeThresholdBoundaries()
{
   CALEngine ale;
   ale.Init();

   CALRiskConfig cfg;
   cfg.SetDefaults();
   cfg.MAX_DRAWDOWN=1.00;
   cfg.STRESS_LIMIT=10.0;
   cfg.DD_PROB_LIMIT=1.00;
   cfg.GLOBAL_MARGIN_LIMIT=100.0;
   cfg.GLOBAL_DD_SUM_LIMIT=1.00;
   cfg.SyncAliases();
   ale.SetRiskConfig(cfg);

   if(!ale.AddVirtual(ALE_FLOW_BUY,1.1000,0.10)) return false;
   if(!ale.AddVirtual(ALE_FLOW_SELL,1.1000,0.10)) return false;

   ale.OnPriceUpdate(1.1000);
   CALContext ctx=ale.Context();

   // Boundary (==) should not trigger global SAFE by design (strict inequality).
   cfg.GLOBAL_MARGIN_LIMIT=ctx.buy.margin+ctx.sell.margin;
   cfg.GLOBAL_DD_SUM_LIMIT=ctx.buy.worst_dd+ctx.sell.worst_dd;
   cfg.SyncAliases();
   ale.SetRiskConfig(cfg);
   if(ale.CheckGlobalSAFE()) return false;

   // Tiny exceedance must trigger global SAFE.
   cfg.GLOBAL_MARGIN_LIMIT=(ctx.buy.margin+ctx.sell.margin)-1e-8;
   cfg.GLOBAL_DD_SUM_LIMIT=(ctx.buy.worst_dd+ctx.sell.worst_dd)-1e-8;
   cfg.SyncAliases();
   ale.SetRiskConfig(cfg);

   if(!ale.CheckGlobalSAFE()) return false;
   return true;
}

#endif
