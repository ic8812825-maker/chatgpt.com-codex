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

   // formula test
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

#endif
