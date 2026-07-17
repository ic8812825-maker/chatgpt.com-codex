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
 BrokerMoneyResult p=Money(4),n=Money(-4),z=Money(0); SmallTransitionLeg legs[5]; for(int i=0;i<5;i++){legs[i].role=(SmallTransitionLegRole)i; legs[i].money=p;} double contractTarget=CalcTargetNewFarLot(1.0); legs[0].actualPositionLot=.25;legs[0].requestedLot=.25;legs[0].fullClose=true;legs[1].actualPositionLot=.60;legs[1].requestedLot=.60;legs[1].fullClose=true;legs[2].actualPositionLot=.20;legs[2].openLot=.20;legs[2].closeLot=.20;legs[2].includesOpenAndClose=true;legs[3].actualPositionLot=1;legs[3].requestedLot=1;legs[3].fullClose=true;legs[4].actualPositionLot=1.2;legs[4].requestedLot=1.2-contractTarget;legs[4].residualLot=contractTarget;
 BigRecoveryEvaluation big;
 Check("BIG_GATE_PASS",EvaluateBigGeometryAndRecovery(1,1.6,.25,.6,p,p,p,p,big)&&big.projectedRecoveryDelta==16);
 Check("BIG_GATE_NEGATIVE",!EvaluateBigGeometryAndRecovery(1,1.6,.25,.6,n,n,n,n,big)&&big.projectedRecoveryDelta<0);
 Check("BIG_GATE_ZERO_REJECTED",!EvaluateBigGeometryAndRecovery(1,1.6,.25,.6,z,z,z,z,big)&&!big.recoveryPass);
 BigReserveCatchUpEvaluation c;
 Check("COVERAGE_IMPROVES",EvaluateBigReserveCatchUp(5,11,1,2,1,.8,10,10,0,c)&&c.coverageAfter>c.coverageBefore);
 Check("COVERAGE_WORSENS",!EvaluateBigReserveCatchUp(5,5,2,1,1,1,10,12,2,c)&&c.coverageAfter<c.coverageBefore);
 double target=contractTarget;
 Check("NEW_FAR_COMPRESSES",target>0&&target<1.0&&target/1.0<=MaximumNewFarRatio);
 SmallTransitionEvaluation s;
 Check("SMALL_TRANSITION_PASS",EvaluateSmallTransition(legs,1,target,.1,MinimumSafeMarginLevel,s)&&s.transitionNet==20);
 Check("SMALL_COMPRESSION_FAIL",!EvaluateSmallTransition(legs,1,1,.1,MinimumSafeMarginLevel,s)&&!s.compressionPass);
 Check("SMALL_MARGIN_FAIL",!EvaluateSmallTransition(legs,1,target,.1,MinimumSafeMarginLevel-1,s)&&!s.marginPass);
 SmallTransitionLeg shuffled[5]; for(int k=0;k<5;k++) shuffled[k]=legs[k]; SmallTransitionLeg temp=shuffled[0]; shuffled[0]=shuffled[4]; shuffled[4]=temp; Check("SMALL_SHUFFLED_ROLES",EvaluateSmallTransition(shuffled,1,target,.1,MinimumSafeMarginLevel,s));
 shuffled[0].role=shuffled[1].role; Check("SMALL_DUPLICATE_ROLE_REJECTED",!EvaluateSmallTransition(shuffled,1,target,.1,MinimumSafeMarginLevel,s));
 ReverseCycleProjection rc; rc.farLotBefore=.02;rc.farLotAfter=.01;rc.transitionNet=10;rc.signedSwap=-1;rc.commission=1;rc.spread=1;rc.slippage=1;rc.reserveAdd=30;rc.carryAdd=0;rc.requiredMargin=10;rc.availableMargin=100; ReverseCyclesEvaluation re;
 Check("REVERSE_REACHABLE",EvaluateReverseCyclesWithCosts(.02,.02,1,0,1,.01,rc,re)&&re.requiredCycles<=MaxReverseCycles);
 rc.reserveAdd=0;rc.transitionNet=0; Check("REVERSE_MONEY_FAIL",!EvaluateReverseCyclesWithCosts(1,100,0,0,0,.01,rc,re)&&!re.pass);
 BrokerMoneyResult raw[5]; for(int j=0;j<5;j++) raw[j]=legs[j].money; BrokerMoneyResult basket; Check("BASKET_COMPONENTS",CalcProjectedBasketNetMoney(raw,5,basket)&&basket.grossProfit==20);
 Check("COMMISSION_CONFLICT",CommissionPerLotPerSide==0||CommissionPerLotRoundTurn==0);
 Check("GEOMETRY_MODE_EXCLUSIVE",UseSplitBigGeometry!=UseLegacySingleBigGeometry);
 SignedSwapResult swap; datetime monday=D'2026.07.13 00:00';
 CalcSignedSwapCalendar(2.0,monday,monday+86400,3,1.0,swap); Check("BUY_POSITIVE_SWAP",swap.expectedSignedSwap==2.0&&swap.additionalSwapBuffer==1.0);
 CalcSignedSwapCalendar(-2.0,monday,monday+86400,3,1.0,swap); Check("BUY_NEGATIVE_SWAP",swap.expectedSignedSwap==-2.0&&swap.worstCaseSwapCost==3.0);
 CalcSignedSwapCalendar(2.0,monday,monday+3*86400,3,0,swap); Check("TRIPLE_SWAP",swap.rolloverMultipliers==5&&swap.expectedSignedSwap==10.0);
 CalcSignedSwapCalendar(-2.0,monday,monday,3,0,swap); Check("CLOSE_NOW_NO_FUTURE_SWAP",swap.expectedSignedSwap==0);
 CommissionBaseResult cb; CalcCommissionBases(1,100000,1.10,1.20,0.01,COMMISSION_PERCENT_TURNOVER,true,cb); Check("TURNOVER_OPEN_CLOSE",cb.openCommission==11&&cb.closeCommission==12&&cb.totalTurnover==230000);
 CalcCommissionBases(1,100000,1.10,1.20,0.01,COMMISSION_PERCENT_NOTIONAL,true,cb); Check("NOTIONAL_ONE_SIDE",cb.openCommission==11&&cb.closeCommission==0);
 FalseReverseOption options[6]; for(int q=0;q<6;q++){options[q].action=(FalseReverseAction)q;options[q].projectedNet=-q;options[q].realizedRecoveryPL=0;options[q].projectedClosedNet=-q;options[q].projectedFloatingNetRemaining=0;options[q].reserveImpact=q;options[q].projectedMarginLevel=MinimumSafeMarginLevel+q;options[q].remainingExposure=1;options[q].secondTailRisk=false;} options[2].realizedRecoveryPL=2;options[2].projectedClosedNet=1;options[2].projectedNet=1;options[2].reserveImpact=0;FalseReverseEvaluation falseReverse; Check("FALSE_REVERSE_SAFE_OPTION",EvaluateFalseReverseMoney(options,MinimumRecoveryProfitMoney,10,falseReverse)&&falseReverse.selected==FALSE_REVERSE_CLOSE_BASE);
 for(int u=0;u<6;u++) options[u].realizedRecoveryPL=-10; Check("FALSE_REVERSE_MANUAL_FALLBACK",!EvaluateFalseReverseMoney(options,MinimumRecoveryProfitMoney,10,falseReverse)&&falseReverse.selected==FALSE_REVERSE_MANUAL);
 Check("REAL_TRADING_DISABLED",!AllowRealTrading);
 PrintFormat("BIG_SMALL_SCENARIO_TEST %s Passed=%d Total=%d",passed==total?"PASS":"FAIL",passed,total);
}
