#property strict
#property script_show_inputs
#include "../../Include/Config.mqh"
#include "../../Include/Types.mqh"
#include "../../Include/LotUtils.mqh"
#include "../../Include/BrokerMoneyModel.mqh"
#define BIG_SMALL_TEST_MAGIC 9900260717
int passed=0,total=0;
void Check(string name,bool value){ total++; if(value) passed++; PrintFormat("BIG_SMALL_TEST %s=%s",name,value?"PASS":"FAIL"); }
BrokerMoneyResult Money(double net)
{
 BrokerMoneyResult r; ResetBrokerMoneyResult(r); r.calculationValid=true; r.ok=true; r.grossProfit=net; r.netMoney=net; return r;
}
void OnStart()
{
 if(MagicNumber!=BIG_SMALL_TEST_MAGIC||AllowRealTrading||!UseInternalSimulation){Print("BIG_SMALL_TEST_CONFIGURATION_REFUSED");return;}
 BrokerMoneyResult p=Money(4),n=Money(-4),z=Money(0),legs[4]; legs[0]=p;legs[1]=p;legs[2]=n;legs[3]=p;
 BigRecoveryEvaluation big;
 Check("BIG_GATE_PASS",EvaluateBigGeometryAndRecovery(1,1.6,.25,.6,p,p,p,p,big)&&big.projectedRecoveryDelta==16);
 Check("BIG_GATE_NEGATIVE",!EvaluateBigGeometryAndRecovery(1,1.6,.25,.6,n,n,n,n,big)&&big.projectedRecoveryDelta<0);
 Check("BIG_GATE_ZERO_REJECTED",!EvaluateBigGeometryAndRecovery(1,1.6,.25,.6,z,z,z,z,big)&&!big.recoveryPass);
 BigReserveCatchUpEvaluation c;
 Check("COVERAGE_IMPROVES",EvaluateBigReserveCatchUp(5,11,1,2,1,.8,10,10,0,c)&&c.coverageAfter>c.coverageBefore);
 Check("COVERAGE_WORSENS",!EvaluateBigReserveCatchUp(5,5,2,1,1,1,10,12,2,c)&&c.coverageAfter<c.coverageBefore);
 double target=CalcTargetNewFarLot(1.0);
 Check("NEW_FAR_COMPRESSES",target>0&&target<1.0&&target/1.0<=MaximumNewFarRatio);
 SmallTransitionEvaluation s;
 Check("SMALL_TRANSITION_PASS",EvaluateSmallTransition(legs,4,1,target,.1,MinimumSafeMarginLevel,s)&&s.transitionNet==8);
 Check("SMALL_COMPRESSION_FAIL",!EvaluateSmallTransition(legs,4,1,1,.1,MinimumSafeMarginLevel,s)&&!s.compressionPass);
 Check("SMALL_MARGIN_FAIL",!EvaluateSmallTransition(legs,4,1,target,.1,MinimumSafeMarginLevel-1,s)&&!s.marginPass);
 Check("REVERSE_LIMIT",EvaluateRequiredReverseCycles(1,.01,.999)>MaxReverseCycles);
 Check("REVERSE_REACHABLE",EvaluateRequiredReverseCycles(.02,.01,.5)==1);
 BrokerMoneyResult basket; Check("BASKET_COMPONENTS",CalcProjectedBasketNetMoney(legs,4,basket)&&basket.netMoney<=8&&basket.grossProfit==8);
 Check("COMMISSION_CONFLICT",CommissionPerLotPerSide==0||CommissionPerLotRoundTurn==0);
 Check("GEOMETRY_MODE_EXCLUSIVE",UseSplitBigGeometry!=UseLegacySingleBigGeometry);
 Check("REAL_TRADING_DISABLED",!AllowRealTrading);
 PrintFormat("BIG_SMALL_SCENARIO_TEST %s Passed=%d Total=%d",passed==total?"PASS":"FAIL",passed,total);
}
