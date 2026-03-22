#ifndef __TESTLYAPUNOV_MQH__
#define __TESTLYAPUNOV_MQH__

#include "..\\ale\\lyapunov\\CALLyapunovToolkit.mqh"

bool NearLyap(const double a,const double b,const double eps=1e-9){ return MathAbs(a-b)<=eps; }

CALLyapunovState MakeState(const double dd,const double ex,const double mu,const double depth,const double dist,const double loss,const double tail,const double pnl)
{
   CALLyapunovState s;
   s.drawdown=dd;
   s.exposure=ex;
   s.margin_usage=mu;
   s.depth=depth;
   s.distance_to_be=dist;
   s.unrealized_loss=loss;
   s.tail_effect=tail;
   s.pnl_contribution=pnl;
   return s;
}

bool TestLyapunov_Exists()
{
   CALLyapunovFunctional L;
   CALLyapunovState s=MakeState(0.02,0.5,0.08,3,250,100,0.1,0.02);
   if(!L.Exists(s)) return false;
   return (L.V(s)>=0.0);
}

bool TestLyapunov_DeltaV_Random()
{
   CALLyapunovFunctional L;
   CALLyapunovState s0=MakeState(0.01,0.4,0.06,2,120,40,0.05,0.01);
   CALLyapunovState s1=MakeState(0.013,0.45,0.07,3,160,55,0.03,0.005);
   const double dv=L.DeltaV(s0,s1);
   return MathIsValidNumber(dv);
}

bool TestLyapunov_DeltaV_Trend()
{
   CALLyapunovFunctional L;
   CALLyapunovState s0=MakeState(0.04,1.0,0.20,8,740,600,0.00,-0.04);
   CALLyapunovState s1=MakeState(0.06,1.4,0.28,11,1100,900,-0.02,-0.06);
   const double dv=L.DeltaV(s0,s1);
   return (dv>0.0); // adverse trend should increase instability score
}

bool TestLyapunov_DeltaV_Adversarial()
{
   CALLyapunovFunctional L;
   CALLyapunovState mono=MakeState(0.10,2.8,0.38,16,1700,2100,-0.08,-0.10);
   CALLyapunovState jump=MakeState(0.14,3.5,0.48,20,2600,3200,-0.12,-0.14);
   CALLyapunovState gap =MakeState(0.18,4.2,0.58,24,3400,4500,-0.20,-0.18);
   return (L.DeltaV(mono,jump)>0.0 && L.DeltaV(jump,gap)>0.0);
}

bool TestLyapunov_TailEffect()
{
   const double before=CALLyapunovTailEffect::EstimateRiskProxy(0.45,15,3.2);
   const double after =CALLyapunovTailEffect::EstimateRiskProxy(0.38,13,2.8);
   const double tail=CALLyapunovTailEffect::Score(before,after);
   return (tail>0.0);
}

bool TestLyapunov_ControlLatency()
{
   CALLyapunovFunctional L;
   CALLyapunovState fast=MakeState(0.05,1.1,0.18,7,650,500,0.03,0.00);
   CALLyapunovState slow=MakeState(0.07,1.5,0.26,10,980,850,-0.03,-0.03);
   return (L.DeltaV(fast,slow)>0.0);
}

#endif
