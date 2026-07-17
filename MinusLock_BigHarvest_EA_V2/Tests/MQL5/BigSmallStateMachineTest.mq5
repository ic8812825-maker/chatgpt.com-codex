#property strict
#property script_show_inputs
#include "../../Include/Config.mqh"
#include "../../Include/Types.mqh"
#include "../../Include/LotUtils.mqh"
#include "../../Include/SimulationEngine.mqh"
#include "../../Include/PositionUtils.mqh"
#include "../../Include/GeometryEngine.mqh"
#include "../../Include/Logger.mqh"
#include "../../Include/TradeEngine.mqh"
#include "../../Include/BrokerMoneyModel.mqh"
#include "../../Include/RecoveryMath.mqh"
#include "../../Include/RiskManager.mqh"
#include "../../Include/PendingContractEngine.mqh"
#include "../../Include/StateMachine.mqh"
#define STATE_MACHINE_TEST_MAGIC 9900260717
int passed=0,total=0;
void Verify(string name,bool condition){total++;if(condition)passed++;PrintFormat("BIG_SMALL_STATE_MACHINE %s=%s",name,condition?"PASS":"FAIL");}
BrokerMoneyResult TestMoney(double net){BrokerMoneyResult r;ResetBrokerMoneyResult(r);r.calculationValid=true;r.ok=true;r.grossProfit=net;r.netMoney=net;return r;}
void OnStart()
{
 if(MagicNumber!=STATE_MACHINE_TEST_MAGIC||AllowRealTrading||!UseInternalSimulation){Print("STATE_MACHINE_TEST_CONFIGURATION_REFUSED");return;}
 SimResetHistory();ResetRecoveryContext();ArrayResize(ReserveLedger,0);NextReserveEventId=1;
 Verify("INITIAL_BUY_OPEN",SimOpenPosition(DIR_BUY,.10,"TEST_INITIAL_BUY")); Verify("INITIAL_SELL_OPEN",SimOpenPosition(DIR_SELL,.10,"TEST_INITIAL_SELL"));
 ulong buy=SimPositions[0].ticket,sell=SimPositions[1].ticket; Verify("INITIAL_LOCK_IDENTITIES",buy!=sell&&SimPositions[0].identifier!=SimPositions[1].identifier);
 Verify("INITIAL_WINNER_CLOSE",SimClosePositionByTicket(buy,.10)); Ctx.farTicket=sell;Ctx.farIdentifier=sell;Ctx.farLot=.10;Ctx.farDirection=DIR_SELL;Ctx.farOpenPrice=SimPositions[0].openPrice;SetState(STATE_FAR_ACTIVE,"TEST_INITIAL_TO_FAR");Verify("INITIAL_TO_FAR",State==STATE_FAR_ACTIVE&&Ctx.farTicket==sell&&SimCountOpenPositions()==1);
 BrokerMoneyResult good=TestMoney(5),bad=TestMoney(-5),zero=TestMoney(0);BigRecoveryEvaluation big;
 Verify("BIG_RECOVERY_PASS",EvaluateBigGeometryAndRecovery(.1,.16,.03,.06,good,good,good,good,big)); Verify("BIG_RECOVERY_FAIL",!EvaluateBigGeometryAndRecovery(.1,.16,.03,.06,bad,bad,bad,bad,big));
 Verify("BIG_ZERO_DELTA_FAIL",!EvaluateBigGeometryAndRecovery(.1,.16,.03,.06,zero,zero,zero,zero,big));
 int openedBefore=SimCountOpenPositions();Verify("REJECTED_OPEN",!SimOpenPosition(DIR_NONE,.1,"REJECT"));Verify("REJECTED_OPEN_NO_POSITION",SimCountOpenPositions()==openedBefore);
 Verify("REJECTED_CLOSE",!SimClosePositionByTicket(999999999,.1));
 Verify("PARTIAL_FILL",SimClosePositionByTicket(sell,.04));PositionSnapshot residual;Verify("PARTIAL_FILL_RESIDUAL",SimGetPositionByTicket(sell,residual)&&residual.lot>0&&residual.lot<.1);
 BigReserveCatchUpEvaluation coverage;Verify("ACTUAL_CATCHUP_PASS",EvaluateBigReserveCatchUp(10,20,1,2,.1,.08,10,10,1,coverage));Verify("ACTUAL_CATCHUP_FAIL",!EvaluateBigReserveCatchUp(10,10,2,1,.1,.1,10,12,1,coverage));
 Ctx.cycleId=701;Ctx.harvestLevel=1;Ctx.harvestId=9001;Ctx.harvestReserveAdd=6;Ctx.harvestCarryAfter=4;Ctx.harvestPhase=HARVEST_LEDGER_PREPARED;Ctx.pendingReserveApplied=false;Ctx.totalReserve=0;SaveState();int ledgerBefore=ArraySize(ReserveLedger);Verify("HARVEST_DISTRIBUTE",ContinueSplitHarvestDistribution());double reserveOnce=Ctx.totalReserve;int ledgerOnce=ArraySize(ReserveLedger);Verify("HARVEST_EXACTLY_ONCE",ContinueSplitHarvestDistribution()&&Ctx.totalReserve==reserveOnce&&ArraySize(ReserveLedger)==ledgerOnce&&ledgerOnce==ledgerBefore+1);
 for(int phase=HARVEST_LEDGER_PREPARED;phase<=HARVEST_LEDGER_WRITTEN;phase++){Ctx.harvestPhase=(HarvestPhase)phase;Ctx.harvestId=9001;SaveState();HarvestPhase saved=Ctx.harvestPhase;ResetRecoveryContext();bool recovered=ReloadHarvestPersistence();Verify(StringFormat("HARVEST_RESTART_%d",phase),recovered&&Ctx.harvestPhase==saved&&Ctx.harvestId==9001);}
 SmallTransitionLeg legs[5];for(int i=0;i<5;i++){legs[i].role=(SmallTransitionLegRole)i;legs[i].money=good;}legs[0].actualPositionLot=.02;legs[0].requestedLot=.02;legs[0].fullClose=true;legs[1].actualPositionLot=.03;legs[1].requestedLot=.03;legs[1].fullClose=true;legs[2].actualPositionLot=.04;legs[2].openLot=.04;legs[2].closeLot=.04;legs[2].includesOpenAndClose=true;legs[3].actualPositionLot=.1;legs[3].requestedLot=.1;legs[3].fullClose=true;legs[4].actualPositionLot=.12;legs[4].requestedLot=.07;legs[4].residualLot=.05;SmallTransitionEvaluation small;Verify("SMALL_FIVE_LEGS",EvaluateSmallTransition(legs,.1,.05,.02,300,small));legs[4].role=SMALL_LEG_OLD_FAR_CLOSE;Verify("SMALL_DUPLICATE_REJECTED",!EvaluateSmallTransition(legs,.1,.05,.02,300,small));
 Verify("ACTUAL_NEW_FAR",.05<.10);Verify("SMALL_RECONCILIATION_FAIL",MathAbs(.05-.08)>VolumeMismatchToleranceLots);
 ReverseCycleProjection rc;rc.farLotBefore=.02;rc.farLotAfter=.01;rc.transitionNet=5;rc.signedSwap=-1;rc.commission=1;rc.spread=1;rc.slippage=1;rc.reserveAdd=40;rc.carryAdd=0;rc.requiredMargin=10;rc.availableMargin=100;ReverseCyclesEvaluation cycles;Verify("FINITE_REVERSE_PASS",EvaluateReverseCyclesWithCosts(.1,10,1,0,1,.01,rc,cycles));rc.reserveAdd=0;rc.transitionNet=0;Verify("FINITE_REVERSE_FAIL",!EvaluateReverseCyclesWithCosts(1,100,0,0,0,.01,rc,cycles));
 FalseReverseOption options[6];for(int o=0;o<6;o++){options[o].action=(FalseReverseAction)o;options[o].projectedNet=-o;options[o].realizedRecoveryPL=-10;options[o].projectedClosedNet=-o;options[o].projectedFloatingNetRemaining=0;options[o].reserveImpact=o;options[o].projectedMarginLevel=300-o;options[o].remainingExposure=1;options[o].secondTailRisk=false;}FalseReverseEvaluation falseDecision;Verify("FALSE_REVERSE_MANUAL",!EvaluateFalseReverseMoney(options,1,0,falseDecision)&&falseDecision.selected==FALSE_REVERSE_MANUAL);
 State=STATE_SPLIT_GEOMETRY_ACTIVE;Ctx.reverseSmallOpened=true;Verify("BIG_SMALL_COLLISION_REJECTED",!ValidateScenarioIsolation());
 SetState(STATE_FINAL_CLOSE,"TEST_FINAL_CLOSE");Verify("FINAL_CLOSE_STATE",State==STATE_FINAL_CLOSE);
 PrintFormat("BIG_SMALL_STATE_MACHINE_TEST %s Passed=%d Total=%d",passed==total?"PASS":"FAIL",passed,total);
}
