#property strict
#property script_show_inputs
#include "../../Include/Core/HSBI_Version.mqh"
#include "../../Include/Core/HSBI_Context.mqh"
#include "../../Include/Core/HSBI_StateMachine.mqh"
#include "../../Include/Core/HSBI_StateValidator.mqh"
#include "../../Include/Core/HSBI_Invariants.mqh"
#include "../../Include/Planning/HSBI_CandidatePlan.mqh"
#include "../../Include/Execution/HSBI_ActionTypes.mqh"
#include "../../Include/Execution/HSBI_EventTypes.mqh"
#include "../../Include/Execution/HSBI_TransactionTypes.mqh"
#include "../../Include/Execution/HSBI_NoTradeExecution.mqh"
#include "../../Include/Execution/HSBI_OwnershipGuardTypes.mqh"
#include "../../Include/Persistence/HSBI_SnapshotTypes.mqh"
#include "../../Include/Persistence/HSBI_JournalTypes.mqh"
#include "../../Include/Money/HSBI_BrokerMoneyTypes.mqh"
#include "../../Include/Money/HSBI_BrokerMoneyModel.mqh"
#include "../../Include/Money/HSBI_BrokerMarginModel.mqh"
#include "../../Include/Money/HSBI_CostModel.mqh"
#include "../../Include/Money/HSBI_CatchUpModel.mqh"
#include "../../Include/Planning/HSBI_BrokerGrid.mqh"
#include "../../Include/Planning/HSBI_GeometrySolver.mqh"
#include "../../Include/Risk/HSBI_CalculationGateTypes.mqh"

int g_pass=0,g_fail=0;
void Check(const string id,const string req,const bool expected,const bool actual,const string reason)
{
   bool ok=(expected==actual);
   Print("TEST_ID=",id,"|Requirement=",req,"|Expected=",expected,"|Actual=",actual,"|Result=",ok?"PASS":"FAIL","|ReasonCode=",reason);
   if(ok)g_pass++;else g_fail++;
}
HSBI_Identity Identity(){HSBI_Identity x;x.accountLogin=1;x.symbol="EURUSD";x.magic=7;x.cycleId=11;x.positionIdentifier=101;x.role=HSBI_ROLE_FAR;return x;}
HSBI_RecoveryContext ValidContext(){HSBI_RecoveryContext c;HSBI_InitializeContext(c,HSBI_RUNTIME_UNIT_TEST);c.accountLogin=1;c.symbol="EURUSD";c.magic=7;c.cycleId=11;return c;}
HSBI_PositionDescriptor Position(const HSBI_Role role,const ulong identifier,const ulong ticket,const double volume){HSBI_PositionDescriptor p;ZeroMemory(p);p.identity=Identity();p.identity.role=role;p.identity.positionIdentifier=identifier;p.identifier=identifier;p.ticket=ticket;p.role=role;p.actualVolume=volume;p.requestedVolume=volume;return p;}
HSBI_OwnershipGuardInput Ownership(const HSBI_Identity &expected,const HSBI_Identity &actual){HSBI_OwnershipGuardInput x;ZeroMemory(x);x.expectedIdentity=expected;x.actualIdentity=actual;x.expectedTicket=100;x.actualTicket=100;x.expectedRole=expected.role;x.actualRole=actual.role;x.expectedDirection=HSBI_DIRECTION_BUY;x.actualDirection=HSBI_DIRECTION_BUY;x.expectedVolume=0.5;x.actualVolume=0.5;x.expectedStateRevision=4;x.actualStateRevision=4;x.planId=1;x.actionId=1;return x;}
HSBI_TransactionBarrierInput Barrier(const HSBI_TransactionOutcome outcome){HSBI_TransactionBarrierInput x;ZeroMemory(x);x.transaction.actionId=50;x.transaction.eventId=61;x.transaction.outcome=outcome;x.transaction.accumulatedVolume=0.5;x.transaction.expectedVolume=0.5;x.transaction.actualPositionRead=true;x.expectedActionId=50;x.lastAppliedEventId=60;x.expectedStateRevision=4;x.actualStateRevision=4;x.actualDealRead=true;x.ownershipConfirmed=true;return x;}
HSBI_BrokerProperties Broker(){HSBI_BrokerProperties p;ZeroMemory(p);p.symbol="TEST";p.point=0.00001;p.tickSize=0.00001;p.digits=5;p.volumeMin=0.01;p.volumeMax=100.0;p.volumeStep=0.01;p.tickValueProfit=1.0;p.tickValueLoss=1.0;p.valid=true;p.fresh=true;p.snapshotId=1;p.timestamp=TimeCurrent();return p;}
HSBI_CostSnapshot ProjectedCosts(){HSBI_CostSnapshot c;ZeroMemory(c);c.commission=-1.0;c.swap=-0.5;c.fee=-0.2;c.slippageBuffer=0.3;c.spreadCost=0.4;c.valid=true;c.actual=false;c.timestamp=TimeCurrent();c.snapshotId=1;return c;}
HSBI_ControlPrice Control(const HSBI_Direction direction){HSBI_ControlPrice p;ZeroMemory(p);p.symbol="TEST";p.bid=1.10000;p.ask=1.10002;p.mid=1.10001;p.direction=direction;p.side=(direction==HSBI_DIRECTION_BUY?HSBI_PRICE_SIDE_BID:HSBI_PRICE_SIDE_ASK);p.selectedPrice=(direction==HSBI_DIRECTION_BUY?p.bid:p.ask);p.point=0.00001;p.tickSize=0.00001;p.digits=5;p.timestamp=TimeCurrent();p.snapshotId=1;p.fresh=true;p.normalized=true;p.valid=true;return p;}
HSBI_CatchUpInput CatchUp(){HSBI_CatchUpInput x;ZeroMemory(x);x.reserveShare=0.6;x.netBigVolume=2.0;x.farVolume=1.0;x.reserveGainMoney=20.0;x.farLossIncreaseMoney=10.0;x.executionSafetyBuffer=2.0;x.farDirection=HSBI_DIRECTION_SELL;x.moneyAvailable=true;x.snapshotFresh=true;return x;}

bool InvalidIdentityContexts(){HSBI_RecoveryContext c=ValidContext();c.accountLogin=0;if(HSBI_ValidateContext(c))return false;c=ValidContext();c.symbol="";if(HSBI_ValidateContext(c))return false;c=ValidContext();c.magic=0;if(HSBI_ValidateContext(c))return false;c=ValidContext();c.cycleId=0;return !HSBI_ValidateContext(c);}
bool InvalidStateContexts(){HSBI_RecoveryContext c=ValidContext();c.currentState=(HSBI_State)999;if(HSBI_ValidateContext(c))return false;c=ValidContext();c.currentState=HSBI_STATE_FAR_ACTIVE;if(HSBI_ValidateContext(c))return false;c=ValidContext();c.reconciliationStatus=6;return !HSBI_ValidateContext(c);}
bool InvalidRoleVolumeContexts(){HSBI_RecoveryContext c=ValidContext();c.far=Position(HSBI_ROLE_FAR,101,100,0.5);c.bigCore=Position(HSBI_ROLE_FAR,102,101,0.4);if(HSBI_ValidateContext(c))return false;c=ValidContext();c.far=Position(HSBI_ROLE_FAR,101,100,-0.1);if(HSBI_ValidateContext(c))return false;c=ValidContext();c.bigCore=Position(HSBI_ROLE_FAR,101,100,0.5);if(HSBI_ValidateContext(c))return false;c=ValidContext();c.currentState=HSBI_STATE_CYCLE_CLOSED;c.stateRevision=1;c.pendingActionId=1;return !HSBI_ValidateContext(c);}

void OnStart()
{
   Check("T01","HSBI-ID-010",true,HSBI_UlongToString(42)=="42","ULONG_NORMAL");
   Check("T02","HSBI-ID-010",true,HSBI_UlongToString((ulong)2147483648)=="2147483648","ULONG_ABOVE_INT_MAX");
   ulong huge=~(ulong)0;Check("T03","HSBI-ID-010",true,HSBI_UlongToString(huge)=="18446744073709551615","ULONG_MAX");
   HSBI_Identity high=Identity();high.cycleId=huge;high.positionIdentifier=(ulong)4294967296;string serialized=HSBI_SerializeIdentity(high);Check("T04","HSBI-ID-010",true,StringFind(serialized,"18446744073709551615")>=0&&StringFind(serialized,"4294967296")>=0,"IDENTITY_HIGH_BITS");
   HSBI_CandidatePlan plan,copy;ZeroMemory(plan);plan.planId=huge;plan.cycleId=(ulong)4294967296;plan.stateRevision=(ulong)4294967297;plan.marketSnapshotId=(ulong)4294967298;copy=plan;Check("T05","HSBI-ID-010",true,HSBI_CandidatePlanFingerprint(plan)==HSBI_CandidatePlanFingerprint(copy)&&StringFind(HSBI_CandidatePlanFingerprint(plan),"18446744073709551615")>=0,"FINGERPRINT_STABLE");

   HSBI_RecoveryContext c=ValidContext();c.runtimeMode=HSBI_RUNTIME_REAL_LIMITED;Check("T06","HSBI-GEN-030",true,!HSBI_IsRuntimeModeAllowedAtStage1(HSBI_RUNTIME_REAL_LIMITED)&&!HSBI_ValidateContext(c),"REAL_LIMITED_BLOCKED");
   c=ValidContext();c.schemaVersion++;bool schemaBlocked=!HSBI_ValidateContext(c);c=ValidContext();c.moneyStateVersion++;Check("T07","HSBI-PERSIST-001",true,schemaBlocked&&!HSBI_ValidateContext(c),"SCHEMA_VERSION_INVALID");
   Check("T08","HSBI-ID-010",true,InvalidIdentityContexts(),"IDENTITY_SCOPE_INVALID");
   Check("T09","HSBI-FSM-002",true,InvalidStateContexts(),"STATE_REVISION_RECON_INVALID");
   Check("T10","HSBI-ID-010",true,InvalidRoleVolumeContexts(),"ROLE_VOLUME_FAR_PENDING_INVALID");

   Check("T11","HSBI-TX-006",false,HSBI_TransactionBarrierPassed(Barrier(HSBI_TX_PLACED)),"PLACED_BARRIER");
   Check("T12","HSBI-TX-006",false,HSBI_TransactionBarrierPassed(Barrier(HSBI_TX_PARTIAL)),"PARTIAL_FILL_BARRIER");
   Check("T13","HSBI-TX-006",true,!HSBI_TransactionBarrierPassed(Barrier(HSBI_TX_TIMEOUT))&&HSBI_ConflictTargetState()==HSBI_STATE_RECONCILING,"TIMEOUT_RECONCILIATION");
   HSBI_TransactionBarrierInput tx=Barrier(HSBI_TX_COMPLETED);tx.transaction.actionId=51;Check("T14","HSBI-TX-006",false,HSBI_TransactionBarrierPassed(tx),"ACTION_ID_MISMATCH");
   tx=Barrier(HSBI_TX_COMPLETED);tx.transaction.eventId=60;Check("T15","HSBI-TX-006",false,HSBI_TransactionBarrierPassed(tx),"STALE_EVENT_ID");
   tx=Barrier(HSBI_TX_COMPLETED);tx.transaction.actionId=51;tx.transaction.eventId=62;Check("T16","HSBI-TX-006",false,HSBI_TransactionBarrierPassed(tx),"FRESH_EVENT_WRONG_ACTION");
   tx=Barrier(HSBI_TX_COMPLETED);tx.actualDealRead=false;bool missingActual=!HSBI_TransactionBarrierPassed(tx);tx=Barrier(HSBI_TX_COMPLETED);tx.transaction.accumulatedVolume=0.4;Check("T17","HSBI-TX-006",true,missingActual&&!HSBI_TransactionBarrierPassed(tx),"ACTUAL_VOLUME_REQUIRED");
   tx=Barrier(HSBI_TX_COMPLETED);bool completed=HSBI_TransactionBarrierPassed(tx);tx.ownershipConfirmed=false;bool ownerBlocked=!HSBI_TransactionBarrierPassed(tx);tx=Barrier(HSBI_TX_COMPLETED);tx.actualStateRevision=5;bool revisionBlocked=!HSBI_TransactionBarrierPassed(tx);tx=Barrier(HSBI_TX_COMPLETED);tx.reconciliationConflict=true;Check("T18","HSBI-TX-006",true,completed&&ownerBlocked&&revisionBlocked&&!HSBI_TransactionBarrierPassed(tx),"FULL_BARRIER_CONTRACT");
   Check("T19","HSBI-TX-006",true,HSBI_RetryAllowed(50,50,HSBI_TX_TIMEOUT,true)&&!HSBI_RetryAllowed(50,51,HSBI_TX_TIMEOUT,true)&&!HSBI_RetryAllowed(50,50,HSBI_TX_TIMEOUT,false),"SAME_ACTION_PENDING_ONLY");
   Check("T20","HSBI-TX-006",true,!HSBI_RetryAllowed(50,50,HSBI_TX_COMPLETED,true)&&HSBI_TransactionConflictTargetState()==HSBI_STATE_TERMINAL_SAFE,"COMPLETED_RETRY_FORBIDDEN");

   HSBI_Identity a=Identity(),b=a;b.accountLogin=2;bool account=!HSBI_EvaluateOwnership(Ownership(a,b)).allowed;b=a;b.symbol="GBPUSD";bool symbol=!HSBI_EvaluateOwnership(Ownership(a,b)).allowed;b=a;b.magic=8;Check("T21","HSBI-ID-010",true,account&&symbol&&!HSBI_EvaluateOwnership(Ownership(a,b)).allowed,"FOREIGN_ACCOUNT_SYMBOL_MAGIC");
   b=a;b.cycleId=12;bool cycle=!HSBI_EvaluateOwnership(Ownership(a,b)).allowed;b=a;b.positionIdentifier=102;bool identifier=!HSBI_EvaluateOwnership(Ownership(a,b)).allowed;b=a;b.role=HSBI_ROLE_BIG_CORE;Check("T22","HSBI-ID-010",true,cycle&&identifier&&!HSBI_EvaluateOwnership(Ownership(a,b)).allowed,"FOREIGN_CYCLE_IDENTIFIER_ROLE");
   HSBI_OwnershipGuardInput own=Ownership(a,a);own.actualTicket=99;bool stale=!HSBI_EvaluateOwnership(own).allowed;HSBI_PositionDescriptor ep=Position(HSBI_ROLE_FAR,101,100,0.5),ap=ep;ap.ticket=200;Check("T23","HSBI-ID-010",true,stale&&!HSBI_TicketMatchesObservation(ep,ap),"STALE_REUSED_TICKET");
   own=Ownership(a,a);own.actualVolume=0.4;bool volume=!HSBI_EvaluateOwnership(own).allowed;own=Ownership(a,a);own.actualDirection=HSBI_DIRECTION_SELL;Check("T24","HSBI-ID-010",true,volume&&!HSBI_EvaluateOwnership(own).allowed,"VOLUME_DIRECTION_CHANGED");
   c=ValidContext();c.far=Position(HSBI_ROLE_FAR,101,100,0.5);c.bigCore=Position(HSBI_ROLE_FAR,102,101,0.4);HSBI_PositionDescriptor residual=Position(HSBI_ROLE_BIG_CORE,77,88,0.25);Check("T25","HSBI-NF-001",true,!HSBI_ExactlyOneFarOrZero(c).passed&&HSBI_IsActualBigCoreResidual(residual,77)&&!HSBI_IsActualBigCoreResidual(residual,78),"SECOND_FAR_AND_ACTUAL_RESIDUAL");
   Check("T26","HSBI-GEN-030",true,HSBI_IsTransitionAllowed(HSBI_STATE_DISABLED,HSBI_STATE_IDLE)&&!HSBI_IsTransitionAllowed(HSBI_STATE_IDLE,HSBI_STATE_CYCLE_CLOSED)&&!HSBI_SubmitActionStub().success&&HSBI_RealTradingForbiddenAtHSB1().passed,"FSM_AND_NO_TRADE");
   HSBI_BrokerProperties bp=Broker();Check("T27","HSBI-MONEY-021",true,HSBI_ValidateBrokerProperties(bp)==HSBI_BROKER_PROPERTIES_VALID,"BROKER_PROPERTIES_VALID");
   bp=Broker();bp.symbol="";Check("T28","HSBI-MONEY-021",true,HSBI_ValidateBrokerProperties(bp)==HSBI_BROKER_PROPERTIES_INVALID,"INVALID_SYMBOL_PROPERTIES");
   bp=Broker();bp.tickSize=0.0;Check("T29","HSBI-MONEY-021",true,HSBI_ValidateBrokerProperties(bp)==HSBI_BROKER_PROPERTIES_INVALID,"INVALID_TICK_SIZE");
   bp=Broker();bp.volumeStep=-0.01;Check("T30","HSBI-GRID-002",true,HSBI_ValidateBrokerProperties(bp)==HSBI_BROKER_PROPERTIES_INVALID,"INVALID_VOLUME_STEP");
   bp=Broker();bp.volumeMin=2.0;bp.volumeMax=1.0;Check("T31","HSBI-MONEY-021",true,HSBI_ValidateBrokerProperties(bp)==HSBI_BROKER_PROPERTIES_INVALID,"MIN_ABOVE_MAX");
   bp=Broker();bp.point=MathArcsin(2.0);Check("T32","HSBI-FAILCLOSED-001",true,HSBI_ValidateBrokerProperties(bp)==HSBI_BROKER_PROPERTIES_INVALID,"NONFINITE_PROPERTY");
   bp=Broker();bp.fresh=false;Check("T33","HSBI-MONEY-021",true,HSBI_ValidateBrokerProperties(bp)==HSBI_BROKER_PROPERTIES_STALE,"STALE_SNAPSHOT");
   Check("T34","HSBI-GRID-001",true,HSBI_IsPriceOnTickGrid(1.10000,0.00001),"PRICE_ON_GRID");
   Check("T35","HSBI-GRID-001",false,HSBI_IsPriceOnTickGrid(1.100005,0.00001),"OFF_GRID_PRICE");
   Check("T36","HSBI-GRID-001",true,MathAbs(HSBI_NormalizePriceToTick(1.100006,0.00001,HSBI_GRID_NEAREST)-1.10001)<1.0e-9,"NEAREST_TICK");
   Check("T37","HSBI-GRID-001",true,HSBI_IsPriceOnTickGrid(1.234,0.001),"COARSE_TICK");
   Check("T38","HSBI-GRID-001",true,HSBI_NormalizePriceToTick(1.100006,0.00001,HSBI_GRID_FLOOR)<HSBI_NormalizePriceToTick(1.100006,0.00001,HSBI_GRID_CEIL),"FLOOR_CEIL_PRICE");
   Check("T39","HSBI-GRID-001",false,HSBI_IsPriceOnTickGrid(1.1,0.0),"INVALID_TICK_SIZE");
   Check("T40","HSBI-GRID-001",true,MathAbs(HSBI_PriceDistanceInTicks(1.10000,1.10010,0.00001)-10.0)<1.0e-7,"PRICE_DISTANCE_TICKS");
   bp=Broker();Check("T41","HSBI-GRID-002",true,HSBI_ValidateVolume(0.01,bp)&&HSBI_ValidateVolume(100.0,bp),"MIN_MAX_VOLUME");
   Check("T42","HSBI-GRID-002",true,MathAbs(HSBI_FloorVolumeToStep(0.256,0.01)-0.25)<1.0e-9,"FLOOR_STEP_001");
   Check("T43","HSBI-GRID-002",true,MathAbs(HSBI_CeilVolumeToStep(0.256,0.01)-0.26)<1.0e-9,"CEIL_STEP_001");
   Check("T44","HSBI-GRID-002",true,MathAbs(HSBI_FloorVolumeToStep(0.256,0.10)-0.20)<1.0e-9,"FLOOR_STEP_010");
   Check("T45","HSBI-GRID-002",true,MathAbs(HSBI_CeilVolumeToStep(0.256,0.10)-0.30)<1.0e-9,"CEIL_STEP_010");
   Check("T46","HSBI-GRID-002",false,HSBI_ValidateVolume(0.001,bp),"BELOW_MIN_VOLUME");
   Check("T47","HSBI-GRID-002",false,HSBI_ValidateVolume(100.01,bp),"ABOVE_MAX_VOLUME");
   Check("T48","HSBI-GRID-002",true,HSBI_FloorVolumeToStep(0.2,0.0)==0.0,"INVALID_STEP_REJECT");
   Check("T49","HSBI-GRID-002",true,HSBI_IsVolumeOnGrid(0.30000000001,0.01),"VOLUME_TOLERANCE");
   Check("T50","HSBI-GRID-002",true,MathAbs(HSBI_NormalizeVolume(0.256,0.01,HSBI_VOLUME_SMALL_BASE)-0.26)<1.0e-9&&MathAbs(HSBI_NormalizeVolume(0.256,0.01,HSBI_VOLUME_BIG_CORE)-0.25)<1.0e-9,"PURPOSE_ROUNDING");
   HSBI_ControlPrice cp=Control(HSBI_DIRECTION_BUY);Check("T51","HSBI-MONEY-022",true,HSBI_ValidateTypedControlPrice(cp,"TEST"),"BUY_USES_BID");
   cp=Control(HSBI_DIRECTION_SELL);Check("T52","HSBI-MONEY-022",true,HSBI_ValidateTypedControlPrice(cp,"TEST"),"SELL_USES_ASK");
   cp=Control(HSBI_DIRECTION_BUY);cp.side=HSBI_PRICE_SIDE_ASK;Check("T53","HSBI-MONEY-022",false,HSBI_ValidateTypedControlPrice(cp,"TEST"),"WRONG_CLOSE_SIDE");
   cp=Control(HSBI_DIRECTION_BUY);cp.ask=cp.bid-0.00001;Check("T54","HSBI-MONEY-022",false,HSBI_ValidateTypedControlPrice(cp,"TEST"),"INVALID_SPREAD");
   cp=Control(HSBI_DIRECTION_BUY);cp.fresh=false;Check("T55","HSBI-MONEY-022",false,HSBI_ValidateTypedControlPrice(cp,"TEST"),"STALE_CONTROL_PRICE");
   HSBI_CostSnapshot costs=ProjectedCosts();Check("T56","HSBI-MONEY-021",true,HSBI_ValidateCostSnapshot(costs,false)&&HSBI_ProjectedNetMoney(20.0,costs,1.0)<20.0,"PROJECTED_COSTS_REDUCE_MONEY");
   Check("T57","HSBI-FAILCLOSED-001",false,HSBI_CalculationResultFlagsValid(true,true,true,HSBI_CALC_PASS),"PROJECTED_ACTUAL_CONFLICT");
   costs=ProjectedCosts();costs.actual=true;Check("T58","HSBI-MONEY-021",false,HSBI_ValidateCostSnapshot(costs,false),"ACTUAL_PROJECTED_COST_SEPARATION");
   HSBI_MoneyCalculationResult mr=HSBI_CalculateProjectedProfit(Broker(),HSBI_DIRECTION_BUY,0.1,1.10000,1.09999,1.09999,1.10001,ProjectedCosts(),1.0);Check("T59","HSBI-MONEY-021",true,mr.projected&&!mr.actual&&(mr.status==HSBI_CALC_UNAVAILABLE||mr.status==HSBI_CALC_PASS),"PROJECTED_BUY_WRAPPER");
   mr=HSBI_CalculateProjectedProfit(Broker(),HSBI_DIRECTION_SELL,0.1,1.10000,1.10001,1.09999,1.10001,ProjectedCosts(),1.0);Check("T60","HSBI-MONEY-021",true,mr.projected&&!mr.actual&&(mr.status==HSBI_CALC_UNAVAILABLE||mr.status==HSBI_CALC_PASS),"PROJECTED_SELL_WRAPPER");
   bp=Broker();bp.symbol="__HSBI_UNAVAILABLE__";HSBI_MarginCalculationResult mm=HSBI_CalculateProjectedMargin(bp,HSBI_DIRECTION_BUY,0.1,1.10000);Check("T61","HSBI-MARGIN-001",true,mm.status==HSBI_CALC_UNAVAILABLE,"MARGIN_UNAVAILABLE");
   mm=HSBI_CalculateProjectedMargin(Broker(),HSBI_DIRECTION_BUY,0.001,1.10000);Check("T62","HSBI-MARGIN-001",true,mm.status==HSBI_CALC_REJECT,"MARGIN_INVALID_VOLUME");
   mm=HSBI_CalculateProjectedMargin(Broker(),HSBI_DIRECTION_SELL,0.1,0.0);Check("T63","HSBI-MARGIN-001",true,mm.status==HSBI_CALC_REJECT,"MARGIN_INVALID_PRICE");
   HSBI_GeometryResult gr=HSBI_SolveBigGeometry(1.0,2.0,1.0,0.5,Broker(),true,true);Check("T64","HSBI-GEO-001",true,gr.valid&&gr.netBigVolume>0.0&&gr.recoverySlopeLots>0.0,"VALID_BIG_GEOMETRY");
   double slope=0.0;Check("T65","HSBI-GEO-002",true,HSBI_ValidateRecoverySlope(2.0,1.0,0.5,1.0,true,slope)&&slope>0.0,"POSITIVE_SLOPE");
   Check("T66","HSBI-GEO-002",false,HSBI_ValidateRecoverySlope(1.0,0.5,0.5,1.0,true,slope),"ZERO_SLOPE_REJECT");
   Check("T67","HSBI-GEO-002",false,HSBI_ValidateRecoverySlope(0.5,0.2,0.5,1.0,true,slope),"NEGATIVE_SLOPE_REJECT");
   gr=HSBI_SolveBigGeometry(1.0,-1.0,1.0,0.5,Broker(),true,true);HSBI_RecoveryDirectionResult down=HSBI_EvaluateRecoveryMoneyDirection(HSBI_DIRECTION_BUY,10.0,11.0,true,true),up=HSBI_EvaluateRecoveryMoneyDirection(HSBI_DIRECTION_SELL,10.0,11.0,true,true);Check("T68","HSBI-GEO-003",true,gr.status==HSBI_CALC_REJECT&&down.directionCorrect&&up.directionCorrect,"INVALID_RATIO_AND_DIRECTION_CONTRACT");
   HSBI_CatchUpInput cu=CatchUp();bool sellCatch=HSBI_EvaluateCatchUp(cu).passed;cu.farDirection=HSBI_DIRECTION_BUY;Check("T69","HSBI-CATCHUP-001",true,sellCatch&&HSBI_EvaluateCatchUp(cu).passed,"CATCH_UP_BOTH_DIRECTIONS_PASS");
   cu=CatchUp();cu.moneyAvailable=false;bool unavailable=HSBI_EvaluateCatchUp(cu).status==HSBI_CALC_UNAVAILABLE;cu=CatchUp();cu.reserveShare=0.4;bool lotFail=!HSBI_EvaluateCatchUp(cu).passed;cu=CatchUp();cu.reserveGainMoney=11.0;Check("T70","HSBI-CATCHUP-001",true,unavailable&&lotFail&&!HSBI_EvaluateCatchUp(cu).passed,"CATCH_UP_FAIL_CLOSED");
   Print("HSBI_TEST_SUMMARY|TOTAL=",g_pass+g_fail,"|PASS=",g_pass,"|FAIL=",g_fail);
}
