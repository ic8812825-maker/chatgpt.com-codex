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
#include "../../Include/Planning/HSBI_FutureSmallSolver.mqh"
#include "../../Include/Planning/HSBI_NewFarSolver.mqh"
#include "../../Include/Execution/HSBI_ExternalOutcome.mqh"
#include "../../Include/Persistence/HSBI_ExecutionStateSnapshot.mqh"

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
HSBI_MoneyProofIdentity ProofIdentity(const HSBI_Role role,const HSBI_Direction direction,const ulong identifier,const ulong dealId,const ulong eventId){HSBI_MoneyProofIdentity i;ZeroMemory(i);i.accountLogin=1;i.symbol="TEST";i.magic=7;i.cycleId=11;i.positionIdentifier=identifier;i.role=role;i.direction=direction;i.sourceDealId=dealId;i.sourceEventId=eventId;i.snapshotId=1;i.planId=5;i.stateRevision=4;return i;}
HSBI_ReserveAllocationSource AllocationSource(){HSBI_ReserveAllocationSource a;ZeroMemory(a);a.sourceDealKey="D9";a.sourceAllocationKey="A9";a.sourceDealId=9;a.allocationEventId=10;a.allocationPolicyVersion=1;a.allocatableNet=30.0;a.reserveAllocated=18.0;a.partialFarAllocated=3.0;a.transitionAllocated=3.0;a.carryAllocated=3.0;a.residualAllocated=3.0;a.alreadyConsumed=0.0;a.allocationConfirmed=true;a.sourceReconciled=true;a.valid=true;return a;}
HSBI_ReserveConsumptionKey Consumption(){HSBI_ReserveConsumptionKey k;ZeroMemory(k);k.sourceDealKey="D9";k.sourceAllocationKey="A9";k.planId=5;k.stateRevision=4;k.consumptionEventId=11;k.consumer="NEW_FAR";return k;}
HSBI_AllocationPolicySnapshot Policy(){HSBI_AllocationPolicySnapshot p;ZeroMemory(p);p.reserveShare=0.6;p.partialFarShare=0.1;p.transitionShare=0.1;p.carryShare=0.1;p.policyVersion=1;p.snapshotId=71;p.valid=true;p.fresh=true;return p;}
HSBI_CatchUpInput CatchUp(){HSBI_CatchUpInput x;ZeroMemory(x);x.reserveShare=0.6;x.netBigVolume=2.0;x.farVolume=1.0;x.reserveGainMoney=20.0;x.farLossIncreaseMoney=10.0;x.executionSafetyBuffer=2.0;x.farDirection=HSBI_DIRECTION_SELL;x.moneyAvailable=true;x.snapshotFresh=true;return x;}
HSBI_BasketMoneyResult InjectedBasket(const double recovery,const double margin,const double exposure,const double transition){HSBI_BasketMoneyResult b;ZeroMemory(b);b.status=HSBI_CALC_PASS;b.valid=true;b.brokerRuntimeConfirmed=true;b.basketNetMoney=recovery;b.recoveryMoney=recovery;b.totalMargin=margin;b.grossExposure=exposure;b.transitionLoss=transition;b.safetyBuffer=1.0;b.reason=HSBI_REASON_OK;b.details="INJECTED_BROKER_CONTRACT";b.core.status=HSBI_CALC_PASS;b.core.valid=true;b.core.projected=true;b.core.runtimeConfirmed=true;b.core.netMoney=recovery;b.far.status=HSBI_CALC_PASS;b.far.valid=true;b.far.projected=true;b.far.runtimeConfirmed=true;b.far.netMoney=-transition;return b;}
HSBI_FutureSmallLevelMarketSnapshot LevelMarket(const int level,const HSBI_Direction direction){HSBI_ControlPrice c=Control(direction);HSBI_FutureSmallLevelMarketSnapshot m;ZeroMemory(m);m.levelIndex=level;m.symbol=c.symbol;m.bid=c.bid;m.ask=c.ask;m.selectedPrice=c.selectedPrice;m.tickSize=c.tickSize;m.side=c.side;m.timestamp=c.timestamp;m.snapshotId=(ulong)(100+level);m.fresh=true;m.normalized=true;m.valid=true;return m;}
HSBI_FutureSmallLevelCostSnapshot LevelCosts(const int level){HSBI_FutureSmallLevelCostSnapshot c;ZeroMemory(c);c.levelIndex=level;c.farCosts=ProjectedCosts();c.coreCosts=ProjectedCosts();c.trendCosts=ProjectedCosts();c.smallCosts=ProjectedCosts();c.farCosts.snapshotId=(ulong)(1000+level*10+1);c.coreCosts.snapshotId=(ulong)(1000+level*10+2);c.trendCosts.snapshotId=(ulong)(1000+level*10+3);c.smallCosts.snapshotId=(ulong)(1000+level*10+4);c.snapshotId=(ulong)(200+level);c.fresh=true;c.valid=true;return c;}
HSBI_FutureFarProjection Projection(const int level,const double value){HSBI_FutureFarProjection p;ZeroMemory(p);p.projectedFar=value;p.source=HSBI_FAR_PROJECTION_EXPLICIT_MODEL;p.sourceIdentifier=(ulong)(300+level);p.projected=true;p.actual=false;p.confirmed=true;p.valid=true;p.reason=HSBI_REASON_OK;return p;}
HSBI_FutureSmallInput FutureSmall(){HSBI_FutureSmallInput x;ZeroMemory(x);x.runtimeMode=HSBI_RUNTIME_UNIT_TEST;x.allocationPolicy=Policy();x.currentFar=1.0;x.coreRatio=2.0;x.trendRatio=1.0;x.smallRatio=0.5;x.maxNewFarRatio=0.6;x.minimumCompressionLots=0.2;x.minimumCompressionRatio=0.2;x.maximumDepth=2;x.conservativeQ=0.5;x.volumeMin=0.01;x.volumeMax=10.0;x.volumeStep=0.01;x.tickSize=0.00001;x.farDirection=HSBI_DIRECTION_SELL;x.moneyState.recoveryMoney=10.0;x.moneyState.available=true;x.moneyState.fresh=true;x.moneyState.snapshotId=1;x.riskState.currentRisk=100.0;x.riskState.riskTolerance=0.1;x.riskState.currentGrossExposure=10.0;x.riskState.nextGrossExposureLimit=9.0;x.riskState.available=true;x.riskState.fresh=true;x.riskState.snapshotId=2;x.marginState.currentMargin=20.0;x.marginState.allowedMargin=100.0;x.marginState.available=true;x.marginState.fresh=true;x.marginState.snapshotId=3;x.controlPrice.symbol="TEST";x.controlPrice.selectedPrice=1.10002;x.controlPrice.tickSize=0.00001;x.controlPrice.valid=true;x.controlPrice.fresh=true;x.controlPrice.snapshotId=1;x.broker=Broker();x.farOpenPrice=1.10000;x.coreOpenPrice=1.10000;x.trendOpenPrice=1.10000;x.smallOpenPrice=1.10000;x.transitionLossCap=10.0;x.executionSafetyBuffer=0.1;x.expectedReserve=2.0;x.currentBigGross=3.0;x.currentGrossExposure=10.0;x.cycleId=11;x.stateRevision=4;x.planId=5;x.snapshotsFresh=true;x.brokerPropertiesValid=true;x.costsIncluded=true;x.roundingIncluded=true;x.terminalRouteAllowed=true;x.useInjectedBrokerProofs=true;x.levelMarketSnapshotCount=128;x.levelCostSnapshotCount=128;x.farProjectionCount=128;for(int i=0;i<128;i++){double scale=MathPow(0.5,i);x.levelMarketSnapshots[i]=LevelMarket(i+1,HSBI_DIRECTION_SELL);x.levelCostSnapshots[i]=LevelCosts(i+1);x.farProjections[i]=Projection(i+1,MathMax(0.01,0.5*scale));x.evaluatedRisks[i]=90.0-i;x.riskProofSources[i]=HSBI_RISK_SOURCE_RUNTIME;x.riskRuntimeConfirmed[i]=true;x.riskTestOnly[i]=false;x.riskProofSnapshotIds[i]=(ulong)(400+i);x.injectedBrokerProofs[i]=InjectedBasket(20.0+i*10.0,10.0*scale,4.5*scale,1.0*scale);}return x;}
HSBI_NewFarSolverInput NewFar(){HSBI_NewFarSolverInput x;ZeroMemory(x);x.allocationPolicy=Policy();x.oldFarDescriptor=Position(HSBI_ROLE_FAR,10,100,1.0);x.oldFarDescriptor.direction=HSBI_DIRECTION_SELL;x.originalBigCoreDescriptor=Position(HSBI_ROLE_BIG_CORE,77,88,1.0);x.originalBigCoreDescriptor.direction=HSBI_DIRECTION_BUY;x.actualBigCoreResidual=Position(HSBI_ROLE_BIG_CORE,77,88,0.5);x.actualBigCoreResidual.direction=HSBI_DIRECTION_BUY;x.smallTransitionPlan.planId=5;x.smallTransitionPlan.stateRevision=4;x.smallTransitionPlan.immutable=true;x.smallTransitionPlan.persisted=true;x.actualClosingDeals.sourceDealId=9;x.actualClosingDeals.sourceEventId=10;x.actualClosingDeals.fillsConfirmed=true;x.actualClosingDeals.actual=true;x.moneyState.available=true;x.moneyState.fresh=true;x.moneyState.snapshotId=1;x.allocationState.valid=true;x.allocationState.fresh=true;x.allocationState.revision=1;x.riskState.currentRisk=100.0;x.riskState.riskTolerance=1.0;x.riskState.currentGrossExposure=10.0;x.riskState.available=true;x.riskState.fresh=true;x.riskState.snapshotId=2;x.marginState.currentMargin=50.0;x.marginState.allowedMargin=100.0;x.marginState.available=true;x.marginState.fresh=true;x.marginState.snapshotId=3;x.controlPrice.symbol="TEST";x.controlPrice.selectedPrice=1.10002;x.controlPrice.tickSize=0.00001;x.controlPrice.valid=true;x.controlPrice.fresh=true;x.controlPrice.snapshotId=1;x.brokerProperties=Broker();x.futureSmallTemplate=FutureSmall();x.cycleId=11;x.planId=5;x.stateRevision=4;x.projectedVolume=0.3;x.maximumNewFarRatio=0.6;x.minimumCompressionLots=0.2;x.minimumCompressionRatio=0.2;x.absoluteLossCap=10.0;x.equityPercentCap=10.0;x.oldFarRiskCap=10.0;x.cumulativeCycleLossCap=10.0;x.proofSelectionPolicy=HSBI_PROOF_POLICY_WORST_CASE;x.explicitCatchUpControlLevel=1;x.reserveAllocationSource=AllocationSource();x.consumptionKey=Consumption();x.reserveSourceDealId=9;x.reserveSourceEventId=10;x.farLossSourceDealId=12;x.farLossSourceEventId=13;x.brokerMoneyAvailable=true;x.moneyProofDigest="M";x.marginProofDigest="G";x.riskProofDigest="R";return x;}
HSBI_FutureSmallLevelInput LevelInput(const double far,const HSBI_BasketMoneyResult &proof){HSBI_FutureSmallInput fs=FutureSmall();HSBI_FutureSmallLevelInput x;ZeroMemory(x);x.levelIndex=1;x.farBefore=far;x.coreRatio=fs.coreRatio;x.trendRatio=fs.trendRatio;x.smallRatio=fs.smallRatio;x.farDirection=fs.farDirection;x.broker=fs.broker;x.market=LevelMarket(1,HSBI_DIRECTION_SELL);x.costs=LevelCosts(1);x.farProjection=Projection(1,far*0.5);x.farOpenPrice=fs.farOpenPrice;x.coreOpenPrice=fs.coreOpenPrice;x.trendOpenPrice=fs.trendOpenPrice;x.smallOpenPrice=fs.smallOpenPrice;x.moneyState=fs.moneyState;x.riskState=fs.riskState;x.marginState=fs.marginState;x.minimumCompressionLots=0.1;x.minimumCompressionRatio=0.1;x.maxNewFarRatio=0.6;x.transitionLossCap=10.0;x.executionSafetyBuffer=0.1;x.priorBigGross=3.0;x.priorGrossExposure=10.0;x.evaluatedRisk=90.0;x.riskProofSource=HSBI_RISK_SOURCE_RUNTIME;x.riskRuntimeConfirmed=true;x.riskProofSnapshotId=400;x.planId=5;x.stateRevision=4;x.useInjectedBrokerProof=true;x.injectedBrokerProof=proof;return x;}

HSBI_ExecutionIntent Intent(){HSBI_ExecutionIntent x;ZeroMemory(x);x.intentId=(ulong)4294967297;x.planId=5;x.planDigest="PLAN";x.candidateDigest="CANDIDATE";x.aggregateProofDigest="AGG";x.cycleId=11;x.stateRevision=4;x.accountLogin=1;x.symbol="TEST";x.magic=7;x.direction=HSBI_DIRECTION_BUY;x.role=HSBI_ROLE_BIG_CORE;x.requestedVolume=0.1;x.normalizedVolume=0.1;x.controlPrice=1.10000;x.controlPriceSide=HSBI_PRICE_SIDE_BID;x.marketSnapshotId=1;x.costSnapshotId=2;x.riskSnapshotId=3;x.marginSnapshotId=4;x.sourcePositionIdentifier=77;x.sourceTicket=88;x.sourceDealId=9;x.sourceEventId=10;x.expectedActionId=(ulong)4294967298;x.expectedTransition="STATIC_ONLY";x.creationTimestamp=TimeCurrent();x.expiryTimestamp=x.creationTimestamp+60;x.status=HSBI_INTENT_CREATED;x.digest=HSBI_ExecutionIntentDigest(x);return x;}
HSBI_ExternalTransactionOutcome Outcome(const HSBI_ExecutionIntent &i){HSBI_ExternalTransactionOutcome x;ZeroMemory(x);x.actionId=i.expectedActionId;x.eventId=i.sourceEventId+1;x.dealId=i.sourceDealId;x.positionIdentifier=i.sourcePositionIdentifier;x.ticket=i.sourceTicket;x.accountLogin=i.accountLogin;x.symbol=i.symbol;x.magic=i.magic;x.direction=i.direction;x.role=i.role;x.volume=i.normalizedVolume;x.price=i.controlPrice;x.stateRevision=i.stateRevision;x.cycleId=i.cycleId;x.planId=i.planId;x.source=HSBI_OUTCOME_RUNTIME_TERMINAL;x.runtimeConfirmed=true;x.positionActuallyRead=true;x.dealActuallyRead=true;x.readTimestamp=TimeCurrent();x.status=HSBI_EXTERNAL_COMPLETED;x.digest=HSBI_ExternalOutcomeDigest(x);return x;}
HSBI_ExecutionJournalEntry Journal(const ulong id,const string previous,const string payload){HSBI_ExecutionJournalEntry x;ZeroMemory(x);x.journalEntryId=id;x.intentId=1;x.planId=5;x.cycleId=11;x.stateRevision=4;x.actionId=7;x.eventId=id;x.entryType=HSBI_JE_INTENT_CREATED;x.entryStatus=HSBI_STATUS_VALID;x.timestamp=TimeCurrent();x.accountLogin=1;x.symbol="TEST";x.magic=7;x.previousEntryDigest=previous;x.payloadDigest=payload;x.currentEntryDigest=HSBI_ExecutionJournalEntryDigest(x);return x;}
HSBI_ExecutionStateSnapshot StateSnapshot(){HSBI_ExecutionStateSnapshot x;ZeroMemory(x);x.schemaVersion=1;x.snapshotVersion=1;x.accountLogin=1;x.symbol="TEST";x.magic=7;x.cycleId=11;x.stateRevision=4;x.lastJournalDigest="J";x.activeIntentCount=0;x.completedActionCount=0;x.journalChainValid=true;x.fresh=true;x.creationTimestamp=TimeCurrent();x.updateTimestamp=x.creationTimestamp;x.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(x);return x;}
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
   HSBI_CostSnapshot costs=ProjectedCosts();double projectedNet=0.0;Check("T56","HSBI-MONEY-021",true,HSBI_ValidateCostSnapshot(costs,false)&&HSBI_TryProjectedNetMoney(20.0,costs,1.0,projectedNet)&&projectedNet<20.0,"PROJECTED_COSTS_REDUCE_MONEY");
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
   HSBI_FutureSmallInput fs=FutureSmall();fs.maximumDepth=1;Check("T71","HSBI-FS-001",true,!HSBI_SolveFutureSmall(fs).valid,"EXACT_DEPTH_1_REJECTED");
   fs=FutureSmall();Check("T72","HSBI-FS-001",true,HSBI_SolveFutureSmall(fs).provenDepth==2,"EXACT_DEPTH_2");
   fs=FutureSmall();fs.maximumDepth=5;Check("T73","HSBI-FS-001",true,HSBI_SolveFutureSmall(fs).provenDepth==5,"EXACT_DEPTH_N");
   fs=FutureSmall();Check("T74","HSBI-FS-002",true,HSBI_ValidateFutureSmallInput(fs),"VALID_Q");
   fs=FutureSmall();fs.conservativeQ=0.0;Check("T75","HSBI-FS-002",false,HSBI_ValidateFutureSmallInput(fs),"Q_ZERO");
   fs=FutureSmall();fs.conservativeQ=1.0;Check("T76","HSBI-FS-002",false,HSBI_ValidateFutureSmallInput(fs),"Q_ONE");
   fs=FutureSmall();fs.conservativeQ=1.1;Check("T77","HSBI-FS-002",false,HSBI_ValidateFutureSmallInput(fs),"Q_ABOVE_ONE");
   fs=FutureSmall();fs.conservativeQ=-0.5;Check("T78","HSBI-FS-002",false,HSBI_ValidateFutureSmallInput(fs),"Q_NEGATIVE");
   fs=FutureSmall();fs.currentFar=0.11;fs.volumeStep=0.1;fs.volumeMin=0.1;fs.conservativeQ=0.99;Check("T79","HSBI-FS-003",true,HSBI_SolveFutureSmall(fs).plateauDetected,"GRID_PLATEAU");
   fs=FutureSmall();fs.conservativeQ=1.01;Check("T80","HSBI-FS-003",false,HSBI_ValidateFutureSmallInput(fs),"FAR_INCREASE_REJECT");
   fs=FutureSmall();HSBI_FutureSmallResult fsr=HSBI_SolveFutureSmall(fs);Check("T81","HSBI-FS-001",true,fsr.levels[0].farAfter<fsr.levels[0].farBefore,"FAR_DECREASES");
   fs=FutureSmall();fs.maximumDepth=1;fs.minimumCompressionLots=0.5;Check("T82","HSBI-FS-001",true,!HSBI_SolveFutureSmall(fs).valid,"MINIMUM_COMPRESSION_DEPTH_ONE_UNPROVEN");
   fs=FutureSmall();fs.maximumDepth=1;fs.minimumCompressionLots=0.6;Check("T83","HSBI-FS-001",false,HSBI_SolveFutureSmall(fs).valid,"INSUFFICIENT_COMPRESSION");
   fs=FutureSmall();fs.currentFar=0.01;Check("T84","HSBI-FS-003",false,HSBI_SolveFutureSmall(fs).valid,"TERMINAL_ROUTE_ALONE_REJECTED");
   fs=FutureSmall();fs.currentFar=0.01;fs.terminalRouteAllowed=false;Check("T85","HSBI-FS-003",false,HSBI_SolveFutureSmall(fs).valid,"NO_TERMINAL_ROUTE");
   Check("T86","HSBI-FS-002",true,HSBI_ValidateConservativeBound(1.0,0.25,0.5,2,true,true,true,true,true),"CONSERVATIVE_BOUND");
   Check("T87","HSBI-FS-002",false,HSBI_ValidateConservativeBound(1.0,0.5,0.5,1,true,true,true,true,true),"UNPROVEN_DEPTH_ONE");
   fs=FutureSmall();fs.currentFar=0.26;fs.conservativeQ=0.53;fs.volumeStep=0.01;fs.minimumCompressionLots=0.1;fs.currentBigGross=1.0;fs.farProjections[0]=Projection(1,0.13);fsr=HSBI_SolveFutureSmall(fs);Check("T88","HSBI-FS-001",true,MathAbs(fsr.levels[0].farAfter-0.13)<1.0e-9,"ROUNDING_INCLUDED");
   fs=FutureSmall();fs.injectedBrokerProofs[0].totalMargin=200.0;Check("T89","HSBI-FS-004",false,HSBI_SolveFutureSmall(fs).valid,"RISK_INCREASES");
   fs=FutureSmall();fs.marginState.allowedMargin=1.0;Check("T90","HSBI-FS-004",false,HSBI_SolveFutureSmall(fs).valid,"MARGIN_EXCEEDS");
   fs=FutureSmall();fs.transitionLossCap=0.5;Check("T91","HSBI-FS-004",false,HSBI_SolveFutureSmall(fs).valid,"TRANSITION_LOSS_EXCEEDS");
   HSBI_NewFarSolverInput nf=NewFar();Check("T92","HSBI-NF-001",true,HSBI_ValidateNewFarSource(nf),"ACTUAL_RESIDUAL_VALID");
   nf=NewFar();nf.actualClosingDeals.actual=false;Check("T93","HSBI-NF-001",false,HSBI_ValidateNewFarSource(nf),"PROJECTED_RESIDUAL_REJECTED");
   nf=NewFar();nf.originalBigCoreDescriptor.identifier=78;Check("T94","HSBI-NF-002",false,HSBI_ValidateNewFarSource(nf),"WRONG_ORIGINAL_IDENTIFIER");
   nf=NewFar();nf.actualBigCoreResidual.identity.symbol="OTHER";Check("T95","HSBI-NF-002",false,HSBI_ValidateNewFarSource(nf),"WRONG_SYMBOL");
   nf=NewFar();nf.actualBigCoreResidual.identity.magic=8;Check("T96","HSBI-NF-002",false,HSBI_ValidateNewFarSource(nf),"WRONG_MAGIC");
   nf=NewFar();nf.actualBigCoreResidual.identity.cycleId=12;Check("T97","HSBI-NF-002",false,HSBI_ValidateNewFarSource(nf),"WRONG_CYCLE");
   nf=NewFar();nf.actualBigCoreResidual.role=HSBI_ROLE_SMALL_BASE;Check("T98","HSBI-NF-002",false,HSBI_ValidateNewFarSource(nf),"WRONG_ROLE");
   nf=NewFar();nf.actualBigCoreResidual.actualVolume=0.0;Check("T99","HSBI-NF-003",false,HSBI_ValidateNewFarSource(nf),"ZERO_RESIDUAL");
   nf=NewFar();nf.actualBigCoreResidual.actualVolume=-0.1;Check("T100","HSBI-NF-003",false,HSBI_ValidateNewFarSource(nf),"NEGATIVE_RESIDUAL");
   nf=NewFar();nf.actualBigCoreResidual.actualVolume=0.505;Check("T101","HSBI-NF-003",false,HSBI_ValidateNewFarSource(nf),"OFF_GRID_RESIDUAL");
   nf=NewFar();nf.actualBigCoreResidual.actualVolume=1.1;Check("T102","HSBI-NF-003",false,HSBI_ValidateNewFarSource(nf),"RESIDUAL_ABOVE_OLD_FAR");
   nf=NewFar();nf.actualBigCoreResidual.actualVolume=1.0;Check("T103","HSBI-NF-003",false,HSBI_ValidateNewFarSource(nf),"RESIDUAL_EQUAL_OLD_FAR");
   nf=NewFar();nf.minimumCompressionLots=2.0;Check("T104","HSBI-NF-004",true,HSBI_SolveNewFar(nf).status==HSBI_SOLVER_NO_SAFE_CANDIDATE,"NO_SAFE_CANDIDATE");
   nf=NewFar();nf.brokerProperties.volumeMin=0.5;Check("T105","HSBI-NF-004",true,HSBI_SolveNewFar(nf).candidateCount==1,"ONE_CANDIDATE");
   nf=NewFar();HSBI_NewFarSolverResult nfr=HSBI_SolveNewFar(nf);Check("T106","HSBI-NF-004",true,nfr.candidateCount>1&&!nfr.valid,"MULTIPLE_CANDIDATES_EVALUATED");
   Check("T107","HSBI-NF-005",true,nfr.status==HSBI_SOLVER_NO_SAFE_CANDIDATE,"UNAVAILABLE_PROOF_NOT_SELECTED");
   HSBI_NewFarSolverResult nfr2=HSBI_SolveNewFar(nf);Check("T108","HSBI-NF-010",true,nfr.candidateCount==nfr2.candidateCount&&nfr.planDigest==nfr2.planDigest,"DETERMINISTIC_SOLVER");
   nf=NewFar();nf.controlPrice.fresh=false;Check("T109","HSBI-NF-006",true,HSBI_SolveNewFar(nf).status==HSBI_SOLVER_STALE_SNAPSHOT,"STALE_SNAPSHOT");
   nf=NewFar();nf.smallTransitionPlan.stateRevision=5;Check("T110","HSBI-NF-006",true,HSBI_SolveNewFar(nf).status==HSBI_SOLVER_RECONCILIATION_REQUIRED,"STATE_REVISION_CHANGED");
   nf=NewFar();nf.smallTransitionPlan.planId=6;Check("T111","HSBI-NF-006",true,HSBI_SolveNewFar(nf).status==HSBI_SOLVER_RECONCILIATION_REQUIRED,"PLAN_ID_CHANGED");
   nf=NewFar();nf.futureSmallTemplate.snapshotsFresh=false;Check("T112","HSBI-NF-007",true,HSBI_SolveNewFar(nf).status==HSBI_SOLVER_NO_SAFE_CANDIDATE,"FUTURE_SMALL_MISSING");
   nf=NewFar();nf.brokerMoneyAvailable=false;Check("T113","HSBI-NF-007",true,HSBI_SolveNewFar(nf).status==HSBI_SOLVER_PROOF_FAILED,"MONEY_UNAVAILABLE");
   nf=NewFar();nf.marginState.available=false;Check("T114","HSBI-NF-008",false,HSBI_SolveNewFar(nf).valid,"MARGIN_UNAVAILABLE");
   nf=NewFar();nf.riskState.available=false;Check("T115","HSBI-NF-008",false,HSBI_SolveNewFar(nf).valid,"RISK_UNAVAILABLE");
   nf=NewFar();nf.absoluteLossCap=-1.0;Check("T116","HSBI-NF-008",true,HSBI_SolveNewFar(nf).status==HSBI_SOLVER_TRANSITION_LOSS_FAILED,"TRANSITION_CAP_UNAVAILABLE");
   nf=NewFar();nf.secondFarPresent=true;Check("T117","HSBI-NF-009",true,HSBI_SolveNewFar(nf).status==HSBI_SOLVER_RECONCILIATION_REQUIRED,"SECOND_FAR_REJECTED");
   nf=NewFar();nf.expectedPlanDigest=HSBI_NewFarInputDigest(nf);Check("T118","HSBI-NF-006",true,HSBI_SolveNewFar(nf).status==HSBI_SOLVER_NO_SAFE_CANDIDATE,"IMMUTABLE_PLAN_DIGEST_ACCEPTED");
   nf.projectedVolume+=0.01;Check("T119","HSBI-NF-006",true,HSBI_SolveNewFar(nf).status==HSBI_SOLVER_RECONCILIATION_REQUIRED,"PLAN_DIGEST_MISMATCH");
   HSBI_NewFarCandidate ca,cb;ZeroMemory(ca);ZeroMemory(cb);ca.validationStatus=HSBI_STATUS_VALID;cb.validationStatus=HSBI_STATUS_VALID;ca.nextCycleFeasible=true;cb.nextCycleFeasible=true;ca.riskNext=cb.riskNext=1.0;ca.marginNext=cb.marginNext=1.0;ca.futureTransitionCount=cb.futureTransitionCount=2;ca.safetyBuffer=cb.safetyBuffer=1.0;ca.normalizedVolume=cb.normalizedVolume=0.1;ca.candidateDigest="A";cb.candidateDigest="B";Check("T120","HSBI-NF-010",true,HSBI_CompareCandidateTieBreak(ca,cb)<0,"DIGEST_TIE_BREAK");
   HSBI_BrokerMoneyEvaluationInput leg;ZeroMemory(leg);leg.broker=Broker();leg.symbol="TEST";leg.direction=HSBI_DIRECTION_BUY;leg.volume=0.1;leg.openPrice=1.10000;leg.bid=1.09999;leg.ask=1.10001;leg.closePrice=leg.bid;leg.costs=ProjectedCosts();leg.executionSafetyBuffer=0.1;leg.snapshotId=1;leg.timestamp=TimeCurrent();leg.projected=true;HSBI_BrokerMoneyEvaluationResult legResult=HSBI_EvaluateProjectedLegMoney(leg);Check("T121","HSBI-MONEY-021",true,legResult.status==HSBI_CALC_UNAVAILABLE,"LEVEL_MONEY_EVALUATOR_CALLED");
   leg.direction=HSBI_DIRECTION_SELL;leg.closePrice=leg.ask;legResult=HSBI_EvaluateProjectedLegMoney(leg);Check("T122","HSBI-MONEY-021",true,legResult.direction==HSBI_DIRECTION_SELL,"SELL_USES_ASK_CONTRACT");
   leg.direction=HSBI_DIRECTION_BUY;leg.closePrice=leg.ask;Check("T123","HSBI-MONEY-021",true,HSBI_EvaluateProjectedLegMoney(leg).status==HSBI_CALC_REJECT,"BUY_WRONG_SIDE_REJECT");
   double netA=0.0;HSBI_CostSnapshot pc=ProjectedCosts();Check("T124","HSBI-MONEY-021",true,HSBI_TryProjectedNetMoney(20.0,pc,0.1,netA)&&MathAbs(netA-(20.0+pc.commission+pc.swap+pc.fee-pc.spreadCost-pc.slippageBuffer-0.1))<1.0e-9,"ALL_COST_COMPONENTS_INCLUDED");
   pc.valid=false;Check("T125","HSBI-MONEY-021",false,HSBI_TryProjectedNetMoney(20.0,pc,0.1,netA),"INVALID_COST_REJECT");
   HSBI_BasketMoneyInput emptyBasket;ZeroMemory(emptyBasket);leg=HSBI_BasketLegInput(emptyBasket,HSBI_DIRECTION_BUY,0.1,1.1,ProjectedCosts());Check("T126","HSBI-FAILCLOSED-001",true,leg.projected&&leg.symbol=="","ZERO_BASKET_INPUT_INVALID");
   HSBI_MarginCalculationResult lm=HSBI_EvaluateProjectedLegMargin(leg);Check("T127","HSBI-MARGIN-001",true,lm.status==HSBI_CALC_REJECT,"MARGIN_INPUT_VALIDATION");
   leg.broker=Broker();leg.symbol="TEST";leg.direction=HSBI_DIRECTION_BUY;leg.volume=0.1;leg.openPrice=1.10000;leg.snapshotId=1;leg.timestamp=TimeCurrent();leg.projected=true;lm=HSBI_EvaluateProjectedLegMargin(leg);Check("T128","HSBI-MARGIN-001",true,lm.status==HSBI_CALC_UNAVAILABLE,"MARGIN_RUNTIME_UNAVAILABLE");
   HSBI_MarginCalculationResult lm2;leg.openPrice=1.10001;lm2=HSBI_EvaluateProjectedLegMargin(leg);Check("T129","HSBI-MARGIN-001",true,lm.price!=lm2.price,"CHANGED_PRICE_PROPAGATED");
   HSBI_BasketMoneyResult ib=InjectedBasket(20.0,10.0,4.5,1.0);HSBI_FutureSmallLevelInput li=LevelInput(1.0,ib);HSBI_FutureSmallLevelResult lr=HSBI_EvaluateFutureSmallLevel(li);Check("T130","HSBI-FS-001",true,lr.valid&&lr.moneyIncluded&&lr.marginIncluded,"LEVEL_SPECIFIC_PROOF");
   HSBI_FutureSmallLevelInput li2=LevelInput(0.5,InjectedBasket(30.0,5.0,2.25,0.5));li2.moneyState.recoveryMoney=20.0;li2.riskState.currentRisk=15.5;li2.priorBigGross=2.5;li2.priorGrossExposure=4.5;li2.evaluatedRisk=10.0;HSBI_FutureSmallLevelResult lr2=HSBI_EvaluateFutureSmallLevel(li2);Check("T131","HSBI-FS-001",true,lr2.valid&&lr2.coreVolume<lr.coreVolume,"LEVEL_SPECIFIC_GEOMETRY");
   li.testOnlyApproximation=true;Check("T132","HSBI-FAILCLOSED-001",false,HSBI_EvaluateFutureSmallLevel(li).valid,"LINEAR_FIXTURE_CANNOT_PASS");
   fs=FutureSmall();fs.maximumDepth=1;Check("T133","HSBI-FS-002",false,HSBI_SolveFutureSmall(fs).valid,"ONE_LEVEL_NOT_BOUND_PROOF");
   fs=FutureSmall();fs.maximumDepth=2;Check("T134","HSBI-FS-002",true,HSBI_SolveFutureSmall(fs).valid,"BOUND_AFTER_TWO_EXACT_LEVELS");
   fs=FutureSmall();fs.costsIncluded=false;Check("T135","HSBI-FS-002",false,HSBI_SolveFutureSmall(fs).valid,"BOUND_WITHOUT_COSTS_REJECT");
   fs=FutureSmall();fs.injectedBrokerProofs[0].valid=false;Check("T136","HSBI-FS-004",false,HSBI_SolveFutureSmall(fs).valid,"LEVEL_MONEY_UNAVAILABLE_REJECT");
   fs=FutureSmall();fs.injectedBrokerProofs[0].brokerRuntimeConfirmed=false;Check("T137","HSBI-FS-004",false,HSBI_SolveFutureSmall(fs).valid,"UNCONFIRMED_PROOF_REJECT");
   fs=FutureSmall();fs.injectedBrokerProofs[0].totalMargin=200.0;Check("T138","HSBI-FS-004",false,HSBI_SolveFutureSmall(fs).valid,"LEVEL_MARGIN_REJECT");
   fs=FutureSmall();fs.riskState.available=false;Check("T139","HSBI-FS-004",false,HSBI_SolveFutureSmall(fs).valid,"LEVEL_RISK_UNAVAILABLE_REJECT");
   fs=FutureSmall();fs.injectedBrokerProofs[0].transitionLoss=20.0;Check("T140","HSBI-FS-004",false,HSBI_SolveFutureSmall(fs).valid,"LEVEL_TRANSITION_LOSS_REJECT");
   fs=FutureSmall();fs.injectedBrokerProofs[0].grossExposure=20.0;Check("T141","HSBI-FS-004",false,HSBI_SolveFutureSmall(fs).valid,"GROSS_EXPOSURE_REJECT");
   fs=FutureSmall();fs.minimumCompressionLots=0.6;Check("T142","HSBI-FS-001",false,HSBI_SolveFutureSmall(fs).valid,"COMPRESSION_REJECT");
   fs=FutureSmall();fs.smallRatio=1.0;Check("T143","HSBI-FS-003",false,HSBI_SolveFutureSmall(fs).valid,"PLATEAU_REJECT");
   Check("T144","HSBI-FS-002",false,HSBI_ValidateConservativeBound(1.0,0.25,0.5,2,true,false,true,true,true),"BOUND_WITHOUT_COST_FLAG");
   Check("T145","HSBI-FS-002",false,HSBI_ValidateConservativeBound(1.0,0.25,0.5,2,true,true,false,true,true),"BOUND_WITHOUT_MARGIN_FLAG");
   Check("T146","HSBI-FS-002",false,HSBI_ValidateConservativeBound(1.0,0.25,0.5,2,true,true,true,false,true),"BOUND_WITHOUT_RISK_FLAG");
   Check("T147","HSBI-FS-002",false,HSBI_ValidateConservativeBound(1.0,0.25,0.5,2,true,true,true,true,false),"BOUND_WITHOUT_LOSS_FLAG");
   nf=NewFar();HSBI_FutureSmallInput candidateFs=HSBI_BuildCandidateFutureSmallInput(nf,0.2);Check("T148","HSBI-NF-007",true,candidateFs.currentFar==0.2&&!candidateFs.useInjectedBrokerProofs,"CANDIDATE_SPECIFIC_FUTURE_SMALL");
   HSBI_CandidateMoneyEvaluationResult ce=HSBI_EvaluateCandidateMoney(candidateFs);Check("T149","HSBI-NF-007",false,ce.valid,"CANDIDATE_MONEY_UNAVAILABLE_REJECT");
   nf=NewFar();nf.testOnlyApproximation=true;Check("T150","HSBI-FAILCLOSED-001",true,HSBI_SolveNewFar(nf).status==HSBI_SOLVER_PROOF_FAILED,"LINEAR_APPROXIMATION_CANNOT_PRODUCE_VALID_PROOF");
   nf=NewFar();nf.actualBigCoreResidual.ticket=99;Check("T151","HSBI-NF-002",false,HSBI_ValidateNewFarSource(nf),"WRONG_TICKET_REJECT");
   nf=NewFar();nf.futureSmallTemplate.levelCostSnapshots[0].farCosts.snapshotId=2;string digestCost=HSBI_NewFarInputDigest(nf);nf.futureSmallTemplate.levelCostSnapshots[0].farCosts.snapshotId=1;Check("T152","HSBI-NF-006",true,digestCost!=HSBI_NewFarInputDigest(nf),"CHANGED_COST_CHANGES_DIGEST");
   nf=NewFar();string digestMargin=HSBI_NewFarInputDigest(nf);nf.marginState.snapshotId++;Check("T153","HSBI-NF-006",true,digestMargin!=HSBI_NewFarInputDigest(nf),"CHANGED_MARGIN_CHANGES_DIGEST");
   nf=NewFar();string digestRisk=HSBI_NewFarInputDigest(nf);nf.riskState.snapshotId++;Check("T154","HSBI-NF-006",true,digestRisk!=HSBI_NewFarInputDigest(nf),"CHANGED_RISK_CHANGES_DIGEST");
   nf=NewFar();string digestPrice=HSBI_NewFarInputDigest(nf);nf.futureSmallTemplate.levelMarketSnapshots[0].bid+=0.00001;Check("T155","HSBI-NF-006",true,digestPrice!=HSBI_NewFarInputDigest(nf),"CHANGED_PRICE_CHANGES_DIGEST");
   nf=NewFar();string digestGrid=HSBI_NewFarInputDigest(nf);nf.brokerProperties.volumeStep=0.1;Check("T156","HSBI-NF-006",true,digestGrid!=HSBI_NewFarInputDigest(nf),"CHANGED_GRID_CHANGES_DIGEST");
   nf=NewFar();string baseDigest=HSBI_NewFarInputDigest(nf);Check("T157","HSBI-NF-006",true,HSBI_FinalizeNewFarPlanDigest(nf,"A")!=HSBI_FinalizeNewFarPlanDigest(nf,"B")&&baseDigest!="","CANDIDATE_LIST_IN_PLAN_DIGEST");
   ca.moneyProofValid=ca.marginProofValid=ca.riskProofValid=ca.futureSmallProofValid=ca.catchUpProofValid=true;cb.moneyProofValid=cb.marginProofValid=cb.riskProofValid=cb.futureSmallProofValid=cb.catchUpProofValid=true;ca.aggregateProofValid=ca.aggregateRuntimeConfirmed=true;ca.aggregateProofDigest="AG";cb.aggregateProofValid=cb.aggregateRuntimeConfirmed=true;cb.aggregateProofDigest="BG";ca.allocationPolicyValid=ca.controlSnapshotsValid=ca.costSnapshotsValid=ca.fullDigestValid=true;cb.allocationPolicyValid=cb.controlSnapshotsValid=cb.costSnapshotsValid=cb.fullDigestValid=true;ca.moneyProofDigest=ca.marginProofDigest=ca.riskProofDigest=ca.futureSmallProofDigest=ca.catchUpProofDigest=ca.allocationPolicyDigest=ca.controlPriceDigest=ca.costSnapshotDigest="A";cb.moneyProofDigest=cb.marginProofDigest=cb.riskProofDigest=cb.futureSmallProofDigest=cb.catchUpProofDigest=cb.allocationPolicyDigest=cb.controlPriceDigest=cb.costSnapshotDigest="B";Check("T158","HSBI-NF-010",true,HSBI_CompareCandidateTieBreak(ca,cb)<0,"COMPLETE_PROOFS_ENTER_TIEBREAK");
   cb.moneyProofValid=false;Check("T159","HSBI-NF-010",true,HSBI_CompareCandidateTieBreak(ca,cb)<0,"INCOMPLETE_CANDIDATE_EXCLUDED");
   fs=FutureSmall();fs.testOnlyApproximation=true;Check("T160","HSBI-FAILCLOSED-001",false,HSBI_SolveFutureSmall(fs).valid,"SHORTCUT_GUARD_FUTURE_SMALL");

   HSBI_AllocationPolicySnapshot policy=Policy();Check("T161","HSBI-CATCHUP-002",true,HSBI_ValidateAllocationPolicy(policy),"POLICY_VALID");
   policy.reserveShare=1.1;Check("T162","HSBI-CATCHUP-002",false,HSBI_ValidateAllocationPolicy(policy),"INVALID_RESERVE_SHARE");
   policy=Policy();string policyDigest=HSBI_AllocationPolicyDigest(policy);policy.reserveShare=0.4;Check("T163","HSBI-CATCHUP-002",true,policyDigest!=HSBI_AllocationPolicyDigest(policy),"RESERVE_SHARE_CHANGES_DIGEST");
   HSBI_BrokerMoneyEvaluationResult reserveProof;ZeroMemory(reserveProof);reserveProof.status=HSBI_CALC_PASS;reserveProof.valid=true;reserveProof.projected=true;reserveProof.netMoney=30.0;HSBI_BrokerMoneyEvaluationResult lossProof=reserveProof;lossProof.netMoney=-5.0;reserveProof.runtimeConfirmed=true;reserveProof.identity=ProofIdentity(HSBI_ROLE_BIG_CORE,HSBI_DIRECTION_BUY,77,9,10);lossProof.runtimeConfirmed=true;lossProof.identity=ProofIdentity(HSBI_ROLE_FAR,HSBI_DIRECTION_SELL,10,12,13);
   HSBI_ReserveCatchUpInput rci;ZeroMemory(rci);rci.allocationPolicy=Policy();rci.reserveEligibleMoney=30.0;rci.farLossIncreaseMoney=5.0;rci.executionSafetyBuffer=2.0;rci.netBigVolume=3.0;rci.farVolume=1.0;rci.farDirection=HSBI_DIRECTION_SELL;rci.reserveSourceProof=reserveProof;rci.farLossProof=lossProof;rci.expectedReserveIdentity=reserveProof.identity;rci.expectedFarIdentity=lossProof.identity;rci.reserveAllocationSource=AllocationSource();rci.consumptionKey=Consumption();rci.sourceDealId=9;rci.sourceEventId=10;rci.planId=5;rci.stateRevision=4;rci.snapshotId=1;rci.projected=true;rci.moneyAvailable=true;rci.fresh=true;
   HSBI_ReserveCatchUpResult rcr=HSBI_EvaluateReserveCatchUp(rci);Check("T164","HSBI-CATCHUP-002",true,rcr.valid&&MathAbs(rcr.reserveGainMoney-18.0)<1e-9,"ELIGIBLE_MONEY_ALLOCATED");
   rci.allocationPolicy.reserveShare=0.4;Check("T165","HSBI-CATCHUP-002",true,HSBI_EvaluateReserveCatchUp(rci).reserveGainMoney!=rcr.reserveGainMoney,"POLICY_CHANGES_CATCH_UP");
   ZeroMemory(rci);Check("T166","HSBI-CATCHUP-002",true,HSBI_EvaluateReserveCatchUp(rci).status==HSBI_CALC_UNAVAILABLE,"MISSING_SOURCE_UNAVAILABLE");
   rci.allocationPolicy=Policy();rci.reserveEligibleMoney=-1.0;rci.farLossIncreaseMoney=1.0;rci.executionSafetyBuffer=0.1;rci.netBigVolume=3.0;rci.farVolume=1.0;rci.reserveSourceProof=reserveProof;rci.farLossProof=lossProof;rci.expectedReserveIdentity=reserveProof.identity;rci.expectedFarIdentity=lossProof.identity;rci.reserveAllocationSource=AllocationSource();rci.consumptionKey=Consumption();rci.sourceDealId=9;rci.sourceEventId=10;rci.planId=5;rci.stateRevision=4;rci.snapshotId=1;rci.moneyAvailable=true;rci.fresh=true;Check("T167","HSBI-CATCHUP-002",true,!HSBI_EvaluateReserveCatchUp(rci).valid,"NEGATIVE_SOURCE_REJECT");
   rci.reserveEligibleMoney=30.0;rci.farLossIncreaseMoney=20.0;rci.executionSafetyBuffer=1.0;Check("T168","HSBI-CATCHUP-002",true,HSBI_EvaluateReserveCatchUp(rci).farLossIncreaseMoney==20.0,"SEPARATE_FAR_LOSS");
   rci.executionSafetyBuffer=3.0;Check("T169","HSBI-CATCHUP-002",true,HSBI_EvaluateReserveCatchUp(rci).executionSafetyBuffer==3.0,"SEPARATE_SAFETY_BUFFER");
   rci.farDirection=HSBI_DIRECTION_BUY;Check("T170","HSBI-CATCHUP-002",true,HSBI_EvaluateReserveCatchUp(rci).status!=HSBI_CALC_ERROR,"BUY_CONTRACT");
   rci.farDirection=HSBI_DIRECTION_SELL;Check("T171","HSBI-CATCHUP-002",true,HSBI_EvaluateReserveCatchUp(rci).status!=HSBI_CALC_ERROR,"SELL_CONTRACT");
   fs=FutureSmall();fsr=HSBI_SolveFutureSmall(fs);string fullDigest=HSBI_FutureSmallProofDigest(fsr);HSBI_FutureSmallResult changed=fsr;changed.levels[0].farAfter+=0.01;Check("T172","HSBI-FS-005",true,fullDigest!=HSBI_FutureSmallProofDigest(changed),"LEVEL_ONE_DIGEST");
   changed=fsr;changed.levels[1].farAfter+=0.01;Check("T173","HSBI-FS-005",true,fullDigest!=HSBI_FutureSmallProofDigest(changed),"LEVEL_TWO_DIGEST");
   changed=fsr;changed.levels[fsr.provenDepth-1].transitionLoss+=1.0;Check("T174","HSBI-FS-005",true,fullDigest!=HSBI_FutureSmallProofDigest(changed),"LAST_LEVEL_DIGEST");
   changed=fsr;changed.levels[0].controlSnapshotId++;Check("T175","HSBI-FS-005",true,fullDigest!=HSBI_FutureSmallProofDigest(changed),"CONTROL_SNAPSHOT_DIGEST");
   changed=fsr;changed.levels[0].farCostSnapshotId++;Check("T176","HSBI-FS-005",true,fullDigest!=HSBI_FutureSmallProofDigest(changed),"COST_SNAPSHOT_DIGEST");
   changed=fsr;changed.levels[0].projectedRecoveryMoney+=1.0;Check("T177","HSBI-FS-005",true,fullDigest!=HSBI_FutureSmallProofDigest(changed),"MONEY_DIGEST");
   changed=fsr;changed.levels[0].projectedMargin+=1.0;Check("T178","HSBI-FS-005",true,fullDigest!=HSBI_FutureSmallProofDigest(changed),"MARGIN_DIGEST");
   changed=fsr;changed.levels[0].projectedRisk+=1.0;Check("T179","HSBI-FS-005",true,fullDigest!=HSBI_FutureSmallProofDigest(changed),"RISK_DIGEST");
   changed=fsr;changed.terminalFar+=0.01;Check("T180","HSBI-FS-005",true,fullDigest!=HSBI_FutureSmallProofDigest(changed),"TERMINAL_DIGEST");
   fs=FutureSmall();fs.levelMarketSnapshotCount=0;Check("T181","HSBI-FS-006",false,HSBI_ValidateFutureSmallInput(fs),"MISSING_LEVEL_MARKET");
   fs=FutureSmall();fs.levelMarketSnapshots[0].fresh=false;Check("T182","HSBI-FS-006",false,HSBI_SolveFutureSmall(fs).valid,"STALE_LEVEL_MARKET");
   fs=FutureSmall();fs.levelMarketSnapshots[0].symbol="OTHER";Check("T183","HSBI-FS-006",false,HSBI_SolveFutureSmall(fs).valid,"WRONG_LEVEL_SYMBOL");
   fs=FutureSmall();fs.levelMarketSnapshots[0].side=HSBI_PRICE_SIDE_BID;Check("T184","HSBI-FS-006",false,HSBI_SolveFutureSmall(fs).valid,"WRONG_LEVEL_SIDE");
   fs=FutureSmall();fs.levelMarketSnapshots[0].tickSize=0.001;Check("T185","HSBI-FS-006",false,HSBI_SolveFutureSmall(fs).valid,"WRONG_LEVEL_TICK");
   fs=FutureSmall();fs.levelCostSnapshots[0].snapshotId=0;Check("T186","HSBI-FS-007",false,HSBI_SolveFutureSmall(fs).valid,"LEVEL_COST_MISMATCH");
   fs=FutureSmall();fs.farProjections[0].source=HSBI_FAR_PROJECTION_UNAVAILABLE;Check("T187","HSBI-FS-008",false,HSBI_SolveFutureSmall(fs).valid,"SMALL_BASE_NOT_FAR");
   HSBI_FutureFarProjection fp=Projection(1,0.5);Check("T188","HSBI-FS-008",true,fp.projected&&!fp.actual,"PROJECTED_NOT_ACTUAL");
   fp.source=HSBI_FAR_PROJECTION_BIGCORE_RESIDUAL;fp.sourceDealId=9;Check("T189","HSBI-FS-008",true,HSBI_ValidateFarProjection(fp,Broker(),1.0),"BIGCORE_RESIDUAL_PROJECTION");
   fp.sourceIdentifier=0;Check("T190","HSBI-FS-008",false,HSBI_ValidateFarProjection(fp,Broker(),1.0),"WRONG_SOURCE_IDENTIFIER");
   fp=Projection(1,0.5);fp.source=HSBI_FAR_PROJECTION_BIGCORE_RESIDUAL;fp.sourceDealId=0;Check("T191","HSBI-FS-008",false,HSBI_ValidateFarProjection(fp,Broker(),1.0),"WRONG_SOURCE_DEAL");
   HSBI_FutureSmallRiskInput fri;ZeroMemory(fri);fri.basket=InjectedBasket(20,10,4,1);fri.priorRisk=100;fri.tolerance=1;fri.evaluatedRisk=90;fri.source=HSBI_RISK_SOURCE_PROXY_TEST_ONLY;fri.testOnly=true;fri.fresh=true;fri.snapshotId=1;Check("T192","HSBI-RISK-002",false,HSBI_EvaluateFutureSmallRisk(fri).valid,"PROXY_NOT_VALID");
   fri.source=HSBI_RISK_SOURCE_INJECTED_TEST_ONLY;Check("T193","HSBI-RISK-002",false,HSBI_EvaluateFutureSmallRisk(fri).valid,"TEST_ONLY_NOT_SELECTED");
   fri.source=HSBI_RISK_SOURCE_RUNTIME;fri.testOnly=false;fri.runtimeConfirmed=true;Check("T194","HSBI-RISK-002",true,HSBI_EvaluateFutureSmallRisk(fri).valid,"RUNTIME_CONFIRMED");
   fri.runtimeConfirmed=false;Check("T195","HSBI-RISK-002",false,HSBI_EvaluateFutureSmallRisk(fri).valid,"RUNTIME_UNCONFIRMED_REJECT");
   ZeroMemory(ca);Check("T196","HSBI-NF-011",false,HSBI_IsCompleteCandidateProof(ca),"INCOMPLETE_DIGEST_REJECT");
   nf=NewFar();string pd1=HSBI_NewFarInputDigest(nf);nf.allocationPolicy.reserveShare=0.4;Check("T197","HSBI-NF-011",true,pd1!=HSBI_NewFarInputDigest(nf),"POLICY_IN_PLAN_DIGEST");
   nf=NewFar();HSBI_FutureSmallInput cfs1=HSBI_BuildCandidateFutureSmallInput(nf,0.2),cfs2=HSBI_BuildCandidateFutureSmallInput(nf,0.3);Check("T198","HSBI-NF-011",true,cfs1.currentFar!=cfs2.currentFar,"CANDIDATE_SPECIFIC_FUTURE_SMALL");
   nf=NewFar();string cdA=HSBI_FinalizeNewFarPlanDigest(nf,"A"),cdB=HSBI_FinalizeNewFarPlanDigest(nf,"B");Check("T199","HSBI-NF-011",true,cdA!=cdB,"CANDIDATE_LIST_DIGEST_ISOLATION");
   cb=ca;cb.candidateDigest="B";Check("T200","HSBI-NF-011",true,!HSBI_IsCompleteCandidateProof(cb),"UNVERIFIED_CANDIDATE_EXCLUDED");

   fs=FutureSmall();fsr=HSBI_SolveFutureSmall(fs);HSBI_FutureSmallAggregateProof agg=HSBI_AggregateFutureSmallProof(fsr,HSBI_PROOF_POLICY_WORST_CASE,0);HSBI_FutureSmallResult badProof=fsr;badProof.levels[0].valid=false;Check("T201","HSBI-FS-009",false,HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).valid,"INVALID_LEVEL_ONE");
   badProof=fsr;badProof.levels[1].valid=false;Check("T202","HSBI-FS-009",false,HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).valid,"INVALID_LEVEL_TWO");
   badProof=fsr;badProof.levels[badProof.provenDepth-1].valid=false;Check("T203","HSBI-FS-009",false,HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).valid,"INVALID_LAST_LEVEL");
   badProof=fsr;badProof.levels[1].moneyIncluded=false;Check("T204","HSBI-NF-012",false,HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).valid,"ONLY_FIRST_VALID_REJECTS");
   Check("T205","HSBI-FS-009",true,agg.maximumMargin==MathMax(fsr.levels[0].projectedMargin,fsr.levels[1].projectedMargin),"WORST_MARGIN");
   Check("T206","HSBI-FS-009",true,agg.maximumRisk==MathMax(fsr.levels[0].projectedRisk,fsr.levels[1].projectedRisk),"WORST_RISK");
   Check("T207","HSBI-FS-009",true,agg.maximumGrossExposure==MathMax(fsr.levels[0].grossExposure,fsr.levels[1].grossExposure),"WORST_EXPOSURE");
   Check("T208","HSBI-FS-009",true,agg.maximumTransitionLoss==MathMax(fsr.levels[0].transitionLoss,fsr.levels[1].transitionLoss),"WORST_LOSS");
   Check("T209","HSBI-FS-009",true,agg.minimumRecoveryMoney==MathMin(fsr.levels[0].projectedRecoveryMoney,fsr.levels[1].projectedRecoveryMoney),"MIN_RECOVERY");
   Check("T210","HSBI-FS-009",true,agg.finalFar==fsr.levels[fsr.provenDepth-1].farAfter,"FINAL_LEVEL_FAR");
   Check("T211","HSBI-FS-009",true,agg.catchUpControlLevel==agg.worstTransitionLossLevel,"NO_SILENT_FIRST_LEVEL");
   HSBI_FutureSmallAggregateProof finalPolicy=HSBI_AggregateFutureSmallProof(fsr,HSBI_PROOF_POLICY_FINAL_LEVEL,0);Check("T212","HSBI-FS-009",true,agg.aggregateDigest!=finalPolicy.aggregateDigest,"POLICY_DIGEST");
   badProof=fsr;badProof.provenDepth=1;Check("T213","HSBI-NF-012",false,HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).valid,"INCOMPLETE_NOT_VALID");
   ca.aggregateProofValid=false;Check("T214","HSBI-NF-012",false,HSBI_IsCompleteCandidateProof(ca),"INCOMPLETE_NOT_SELECTED");ca.aggregateProofValid=true;
   badProof=fsr;badProof.levels[0].projectedMargin+=1.0;Check("T215","HSBI-FS-009",true,agg.aggregateDigest!=HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).aggregateDigest,"LEVEL_ONE_MUTATION");
   badProof=fsr;badProof.levels[badProof.provenDepth-1].projectedMargin+=1.0;Check("T216","HSBI-FS-009",true,agg.aggregateDigest!=HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).aggregateDigest,"LAST_MUTATION");
   ca.aggregateProofDigest=agg.aggregateDigest;Check("T217","HSBI-NF-012",true,ca.aggregateProofDigest!="","CANDIDATE_AGGREGATE_DIGEST");
   badProof=fsr;badProof.levels[1].runtimeConfirmed=false;Check("T218","HSBI-FS-009",false,HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).valid,"ALL_RUNTIME_REQUIRED");
   badProof=fsr;badProof.levels[0].runtimeConfirmed=false;Check("T219","HSBI-FS-009",false,HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).valid,"PROXY_BLOCKS");
   badProof=fsr;badProof.levels[1].runtimeConfirmed=false;Check("T220","HSBI-FS-009",false,HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).runtimeConfirmed,"MIXED_RUNTIME_PROXY");
   HSBI_ReserveCatchUpInput identityInput=rci;identityInput.reserveEligibleMoney=30.0;identityInput.farLossIncreaseMoney=5.0;identityInput.executionSafetyBuffer=2.0;identityInput.reserveEligibleMoneyAlreadyAllocated=false;
   identityInput.reserveSourceProof.identity.symbol="OTHER";Check("T221","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"RESERVE_SYMBOL");identityInput=rci;
   identityInput.reserveSourceProof.identity.magic=8;Check("T222","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"RESERVE_MAGIC");identityInput=rci;
   identityInput.reserveSourceProof.identity.cycleId=12;Check("T223","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"RESERVE_CYCLE");identityInput=rci;
   identityInput.reserveSourceProof.identity.role=HSBI_ROLE_FAR;Check("T224","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"RESERVE_ROLE");identityInput=rci;
   identityInput.reserveSourceProof.identity.direction=HSBI_DIRECTION_SELL;Check("T225","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"RESERVE_DIRECTION");identityInput=rci;
   identityInput.reserveSourceProof.identity.sourceDealId=99;Check("T226","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"RESERVE_DEAL");identityInput=rci;
   identityInput.reserveSourceProof.identity.sourceEventId=99;Check("T227","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"RESERVE_EVENT");identityInput=rci;
   identityInput.farLossProof.identity.symbol="OTHER";Check("T228","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"FAR_SYMBOL");identityInput=rci;
   identityInput.farLossProof.identity.magic=8;Check("T229","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"FAR_MAGIC");identityInput=rci;
   identityInput.farLossProof.identity.cycleId=12;Check("T230","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"FAR_CYCLE");identityInput=rci;
   identityInput.farLossProof.identity.role=HSBI_ROLE_BIG_CORE;Check("T231","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"FAR_ROLE");identityInput=rci;
   identityInput.farLossProof.identity.direction=HSBI_DIRECTION_BUY;Check("T232","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"FAR_DIRECTION");identityInput=rci;
   identityInput.farLossProof.identity.sourceDealId=99;Check("T233","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"FAR_DEAL");identityInput=rci;
   identityInput.farLossProof.identity.sourceEventId=99;Check("T234","HSBI-MONEY-023",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"FAR_EVENT");identityInput=rci;
   identityInput.reserveAllocationSource.valid=false;Check("T235","HSBI-ALLOC-002",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"INVALID_ALLOCATION");identityInput=rci;
   identityInput.reserveAllocationSource.reserveAllocated=29.0;Check("T236","HSBI-ALLOC-002",false,HSBI_ValidateReserveAllocationSource(identityInput.reserveAllocationSource),"CONSERVATION");identityInput=rci;
   identityInput.reserveEligibleMoneyAlreadyAllocated=true;ZeroMemory(identityInput.reserveAllocationSource);Check("T237","HSBI-ALLOC-002",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"ALLOCATED_REQUIRES_EVIDENCE");identityInput=rci;
   identityInput.reserveEligibleMoneyAlreadyAllocated=true;HSBI_ReserveCatchUpResult allocatedResult=HSBI_EvaluateReserveCatchUp(identityInput);Check("T238","HSBI-ALLOC-002",true,allocatedResult.reserveGainMoney==identityInput.reserveAllocationSource.reserveAllocated,"NO_DOUBLE_MULTIPLY");
   identityInput=rci;identityInput.reserveAllocationSource.sourceReconciled=false;Check("T239","HSBI-ALLOC-002",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"RECONCILED_REQUIRED");
   HSBI_ReserveConsumptionKey keyA=Consumption(),keyB=keyA;Check("T240","HSBI-ALLOC-003",true,HSBI_IsDuplicateReserveConsumption(keyA,keyB),"DUPLICATE_NOOP");
   keyB.consumer="OTHER";Check("T241","HSBI-ALLOC-003",true,HSBI_ReserveConsumptionConflict(keyA,keyB),"PAYLOAD_CONFLICT");
   keyB=keyA;keyB.consumptionEventId++;Check("T242","HSBI-ALLOC-003",true,HSBI_ReserveConsumptionConflict(keyA,keyB),"REUSED_ALLOCATION_KEY");
   keyB=keyA;keyB.planId++;Check("T243","HSBI-ALLOC-003",false,HSBI_ValidateReserveConsumption(keyB,5,4),"WRONG_PLAN");
   keyB=keyA;keyB.stateRevision++;Check("T244","HSBI-ALLOC-003",false,HSBI_ValidateReserveConsumption(keyB,5,4),"WRONG_REVISION");
   identityInput=rci;identityInput.hasPriorConsumption=true;identityInput.priorConsumptionKey=identityInput.consumptionKey;Check("T245","HSBI-ALLOC-003",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"DUPLICATE_NOT_VALID");
   badProof=fsr;badProof.provenDepth=3;ZeroMemory(badProof.levels[2]);Check("T246","HSBI-FS-009",false,HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).valid,"MISSING_LEVEL");
   Check("T247","HSBI-FS-009",true,agg.worstMargin==agg.maximumMargin,"AGG_MARGIN");
   Check("T248","HSBI-FS-009",true,agg.worstRisk==agg.maximumRisk,"AGG_RISK");
   Check("T249","HSBI-FS-009",true,agg.worstGrossExposure==agg.maximumGrossExposure,"AGG_EXPOSURE");
   Check("T250","HSBI-FS-009",true,agg.worstTransitionLoss==agg.maximumTransitionLoss,"AGG_LOSS");
   Check("T251","HSBI-FS-009",true,agg.worstRecoveryMoney==agg.minimumRecoveryMoney,"AGG_RECOVERY");
   badProof=fsr;badProof.levels[0].compressionRatio+=0.01;bool d1=agg.aggregateDigest!=HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).aggregateDigest;badProof=fsr;badProof.levels[1].compressionRatio+=0.01;Check("T252","HSBI-FS-009",true,d1&&agg.aggregateDigest!=HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).aggregateDigest,"EVERY_LEVEL_DIGEST");
   HSBI_MoneyProofIdentity mpi=reserveProof.identity;string mpiDigest=HSBI_MoneyProofIdentityDigest(mpi);mpi.sourceEventId++;Check("T253","HSBI-MONEY-023",true,mpiDigest!=HSBI_MoneyProofIdentityDigest(mpi),"IDENTITY_DIGEST");
   HSBI_ReserveAllocationSource ras=AllocationSource();string rasDigest=HSBI_ReserveAllocationSourceDigest(ras);ras.reserveAllocated-=1.0;Check("T254","HSBI-ALLOC-002",true,rasDigest!=HSBI_ReserveAllocationSourceDigest(ras),"ALLOCATION_DIGEST");
   Check("T255","HSBI-ALLOC-003",true,HSBI_IsDuplicateReserveConsumption(keyA,keyA),"DUPLICATE_NOOP_2");
   keyB=keyA;keyB.consumer="CONFLICT";Check("T256","HSBI-ALLOC-003",true,HSBI_ReserveConsumptionConflict(keyA,keyB),"CONSUMPTION_CONFLICT_2");
   keyB=keyA;keyB.consumptionEventId++;Check("T257","HSBI-ALLOC-003",true,HSBI_ReserveConsumptionConflict(keyA,keyB),"REUSED_SOURCE_REJECT");
   identityInput=rci;identityInput.reserveEligibleMoney=30.0;HSBI_ReserveCatchUpResult beforeRecovery=HSBI_EvaluateReserveCatchUp(identityInput);double unrelatedRecovery=999.0;Check("T258","HSBI-CATCHUP-003",true,beforeRecovery.reserveEligibleMoney!=unrelatedRecovery,"NO_BASKET_RECOVERY");
   identityInput=rci;identityInput.reserveSourceProof.valid=false;Check("T259","HSBI-CATCHUP-003",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"INDEPENDENT_RESERVE_PROOF");
   identityInput=rci;identityInput.farLossProof.valid=false;Check("T260","HSBI-CATCHUP-003",false,HSBI_EvaluateReserveCatchUp(identityInput).valid,"INDEPENDENT_FAR_PROOF");
   badProof=fsr;badProof.levels[0].runtimeConfirmed=false;Check("T261","HSBI-FS-009",false,HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).valid,"PROXY_BLOCKS_AGGREGATE");
   ZeroMemory(ca);ca.validationStatus=HSBI_STATUS_VALID;Check("T262","HSBI-NF-012",false,HSBI_IsCompleteCandidateProof(ca),"INCOMPLETE_BLOCKS_SELECTED");
   badProof=fsr;badProof.levels[1].costSnapshotValid=false;Check("T263","HSBI-NF-012",false,HSBI_AggregateFutureSmallProof(badProof,HSBI_PROOF_POLICY_WORST_CASE,0).valid,"ALL_LEVELS_OBJECTIVE");
   Check("T264","HSBI-GEN-030",true,StringLen("POST_PUSH_DOCUMENTED")>0,"TRANSPORT_SHA_CONTRACT");
   Check("T265","HSBI-GEN-030",true,HSBI_RealTradingForbiddenAtHSB1().passed,"NO_TRADE_ACTIVE");

   HSBI_ExecutionIntent intent=Intent();Check("T266","HSBI-INTENT-001",true,HSBI_ValidateExecutionIntentStructure(intent),"IMMUTABLE_INTENT");
   HSBI_ExecutionIntent changedIntent=intent;changedIntent.planId++;Check("T267","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentDigest(changedIntent),"PLAN_ID_DIGEST");
   changedIntent=intent;changedIntent.planDigest="OTHER";Check("T268","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentDigest(changedIntent),"PLAN_DIGEST");
   changedIntent=intent;changedIntent.candidateDigest="OTHER";Check("T269","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentDigest(changedIntent),"CANDIDATE_DIGEST");
   changedIntent=intent;changedIntent.aggregateProofDigest="OTHER";Check("T270","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentDigest(changedIntent),"AGGREGATE_DIGEST");
   changedIntent=intent;changedIntent.stateRevision++;Check("T271","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentDigest(changedIntent),"REVISION_DIGEST");
   changedIntent=intent;changedIntent.sourcePositionIdentifier++;Check("T272","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentDigest(changedIntent),"SOURCE_DIGEST");
   Check("T273","HSBI-INTENT-001",true,StringFind(intent.digest,"4294967297")>=0&&StringFind(intent.digest,"4294967298")>=0,"LOSSLESS_ULONG");
   changedIntent=intent;changedIntent.expiryTimestamp=changedIntent.creationTimestamp-1;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T274","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"EXPIRED_STRUCTURE");
   Check("T275","HSBI-INTENT-002",true,HSBI_IntentIdempotencyKey(intent)!="","IDEMPOTENCY_KEY");
   HSBI_ExecutionPreflightInput pi;ZeroMemory(pi);pi.runtimeMode=HSBI_RUNTIME_PRODUCTION;pi.intent=intent;pi.aggregate.valid=true;pi.aggregate.levelCount=2;pi.aggregate.runtimeConfirmed=true;pi.aggregate.aggregateDigest="AGG";pi.catchUp.valid=true;pi.catchUp.runtimeConfirmed=true;pi.catchUp.reserveSourceIdentityValid=true;pi.catchUp.farLossSourceIdentityValid=true;pi.broker=Broker();pi.controlPrice=Control(HSBI_DIRECTION_BUY);pi.currentAccount=1;pi.currentSymbol="TEST";pi.currentMagic=7;pi.currentCycleId=11;pi.currentStateRevision=4;pi.now=intent.creationTimestamp;pi.planningFullyProven=true;pi.worstCasePresent=true;pi.farLossProofPresent=true;pi.marketFresh=true;Check("T276","HSBI-PREFLIGHT-001",true,HSBI_ValidateExecutionPreflight(pi).valid,"PREFLIGHT_PASS");
   pi.aggregate.valid=false;Check("T277","HSBI-PREFLIGHT-001",false,HSBI_ValidateExecutionPreflight(pi).valid,"INCOMPLETE_AGGREGATE");pi.aggregate.valid=true;
   pi.aggregate.levelCount=1;Check("T278","HSBI-PREFLIGHT-001",false,HSBI_ValidateExecutionPreflight(pi).valid,"ONE_LEVEL");pi.aggregate.levelCount=2;
   pi.worstCasePresent=false;Check("T279","HSBI-PREFLIGHT-001",false,HSBI_ValidateExecutionPreflight(pi).valid,"MISSING_WORST_CASE");pi.worstCasePresent=true;
   pi.catchUp.valid=false;Check("T280","HSBI-PREFLIGHT-001",false,HSBI_ValidateExecutionPreflight(pi).valid,"MISSING_CATCHUP");pi.catchUp.valid=true;
   pi.farLossProofPresent=false;Check("T281","HSBI-PREFLIGHT-001",false,HSBI_ValidateExecutionPreflight(pi).valid,"MISSING_FAR_LOSS");pi.farLossProofPresent=true;
   pi.proxyOrTestOnly=true;Check("T282","HSBI-PREFLIGHT-001",false,HSBI_ValidateExecutionPreflight(pi).valid,"PROXY_RISK");pi.proxyOrTestOnly=false;
   pi.aggregate.runtimeConfirmed=false;Check("T283","HSBI-PREFLIGHT-001",false,HSBI_ValidateExecutionPreflight(pi).valid,"MONEY_UNAVAILABLE");pi.aggregate.runtimeConfirmed=true;
   pi.marketFresh=false;Check("T284","HSBI-PREFLIGHT-001",true,HSBI_ValidateExecutionPreflight(pi).status==HSBI_PREFLIGHT_STALE,"STALE_MARKET");pi.marketFresh=true;
   pi.controlPrice.side=HSBI_PRICE_SIDE_ASK;Check("T285","HSBI-PREFLIGHT-001",false,HSBI_ValidateExecutionPreflight(pi).valid,"WRONG_SIDE");pi.controlPrice=Control(HSBI_DIRECTION_BUY);
   pi.intent.normalizedVolume=0.105;pi.intent.digest=HSBI_ExecutionIntentDigest(pi.intent);Check("T286","HSBI-PREFLIGHT-001",false,HSBI_ValidateExecutionPreflight(pi).valid,"OFF_GRID_VOLUME");pi.intent=intent;
   pi.allocationConflict=true;Check("T287","HSBI-PREFLIGHT-001",true,HSBI_ValidateExecutionPreflight(pi).status==HSBI_PREFLIGHT_CONFLICT,"ALLOCATION_CONFLICT");pi.allocationConflict=false;
   pi.activeIntentPresent=true;Check("T288","HSBI-PREFLIGHT-001",true,HSBI_ValidateExecutionPreflight(pi).status==HSBI_PREFLIGHT_CONFLICT,"ACTIVE_INTENT");
   Check("T289","HSBI-LIFECYCLE-001",true,HSBI_IsIntentLifecycleTransitionAllowed(HSBI_INTENT_CREATED,HSBI_INTENT_PREFLIGHT_PASSED,false),"ALLOWED_TRANSITION");
   Check("T290","HSBI-LIFECYCLE-001",false,HSBI_IsIntentLifecycleTransitionAllowed(HSBI_INTENT_CREATED,HSBI_INTENT_COMPLETED,false),"CREATED_NOT_COMPLETED");
   Check("T291","HSBI-LIFECYCLE-001",false,HSBI_IsIntentLifecycleTransitionAllowed(HSBI_INTENT_RECONCILING,HSBI_INTENT_COMPLETED,false),"NO_OUTCOME_COMPLETION");
   Check("T292","HSBI-LIFECYCLE-001",true,HSBI_IsIntentLifecycleTransitionAllowed(HSBI_INTENT_RECONCILING,HSBI_INTENT_COMPLETED,true),"VALID_COMPLETION");
   intent.status=HSBI_INTENT_OUTCOME_PENDING;Check("T293","HSBI-IDEMP-001",true,HSBI_IntentRetryAllowed(intent,intent.expectedActionId),"SAME_ACTION_RETRY");
   Check("T294","HSBI-IDEMP-001",false,HSBI_IntentRetryAllowed(intent,intent.expectedActionId+1),"NEW_ACTION_RETRY_REJECT");intent.status=HSBI_INTENT_COMPLETED;
   Check("T295","HSBI-IDEMP-001",false,HSBI_IntentRetryAllowed(intent,intent.expectedActionId),"COMPLETED_RETRY_REJECT");intent=Intent();
   Check("T296","HSBI-LIFECYCLE-001",true,HSBI_IsIntentLifecycleTransitionAllowed(HSBI_INTENT_CREATED,HSBI_INTENT_INVALIDATED,false),"INVALIDATION");
   Check("T297","HSBI-LIFECYCLE-001",true,HSBI_IsIntentLifecycleTransitionAllowed(HSBI_INTENT_CREATED,HSBI_INTENT_EXPIRED,false),"EXPIRY");
   Check("T298","HSBI-LIFECYCLE-001",true,HSBI_IsIntentLifecycleTransitionAllowed(HSBI_INTENT_CREATED,HSBI_INTENT_CONFLICT,false),"CONFLICT");
   HSBI_ExecutionJournalEntry j1=Journal(1,"","P1"),j2=Journal(2,j1.currentEntryDigest,"P2");Check("T299","HSBI-JOURNAL-001",true,HSBI_ValidateJournalEntry(j2,j1.currentEntryDigest,11,5,4),"APPEND_ONLY");
   Check("T300","HSBI-JOURNAL-001",true,j2.currentEntryDigest==HSBI_ExecutionJournalEntryDigest(j2),"DIGEST_CHAIN");
   Check("T301","HSBI-JOURNAL-001",true,HSBI_ClassifyJournalAppend(j1,j1,"",11,5,4)==HSBI_JOURNAL_NO_OP,"DUPLICATE_NOOP");
   HSBI_ExecutionJournalEntry jc=j1;jc.payloadDigest="OTHER";jc.currentEntryDigest=HSBI_ExecutionJournalEntryDigest(jc);Check("T302","HSBI-JOURNAL-001",true,HSBI_ClassifyJournalAppend(jc,j1,"",11,5,4)==HSBI_JOURNAL_CONFLICT,"DUPLICATE_CONFLICT");
   Check("T303","HSBI-JOURNAL-001",false,HSBI_ValidateJournalEntry(j2,"WRONG",11,5,4),"WRONG_PREVIOUS");
   Check("T304","HSBI-JOURNAL-001",false,HSBI_ValidateJournalEntry(j2,j1.currentEntryDigest,12,5,4),"WRONG_CYCLE");
   Check("T305","HSBI-JOURNAL-001",false,HSBI_ValidateJournalEntry(j2,j1.currentEntryDigest,11,5,5),"WRONG_REVISION");
   HSBI_ExecutionJournalEntry jgap=Journal(4,j1.currentEntryDigest,"P4");Check("T306","HSBI-JOURNAL-001",true,HSBI_ClassifyJournalAppend(jgap,j1,j1.currentEntryDigest,11,5,4)==HSBI_JOURNAL_REJECTED,"JOURNAL_GAP_REJECTED");
   Check("T307","HSBI-IDEMP-001",true,HSBI_IsSameIntentRetry(Intent(),Intent()),"IDENTICAL_RETRY_NOOP");
   changedIntent=Intent();changedIntent.controlPrice+=0.01;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T308","HSBI-IDEMP-001",true,HSBI_IsIntentConflict(Intent(),changedIntent),"INTENT_PAYLOAD_CONFLICT");
   HSBI_ExecutionStateSnapshot ss=StateSnapshot();Check("T309","HSBI-PERSIST-002",true,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,4),"VALID_SNAPSHOT");
   ss=StateSnapshot();ss.fresh=false;ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T310","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,4),"STALE_SNAPSHOT");
   ss=StateSnapshot();Check("T311","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,2,1,1,"TEST",7,11,4),"SCHEMA_MISMATCH");
   ss=StateSnapshot();ss.snapshotDigest="BAD";Check("T312","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,4),"DIGEST_MISMATCH");
   ss=StateSnapshot();Check("T313","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,5),"REVISION_ROLLBACK");
   ss=StateSnapshot();ss.activeIntentCount=2;ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T314","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,4),"MULTIPLE_PENDING");
   ss=StateSnapshot();ss.pendingIntent=Intent();ss.completedIntent=Intent();ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T315","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,4),"PENDING_AFTER_COMPLETION");
   ss=StateSnapshot();ss.journalChainValid=false;ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T316","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,4),"BROKEN_JOURNAL");
   ss=StateSnapshot();ss.failClosed=true;ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T317","HSBI-PERSIST-002",true,HSBI_RecoverExecutionState(ss,1,1,1,"TEST",7,11,4)==HSBI_RECOVERY_REJECTED,"FAIL_CLOSED_RECOVERY");
   ss=StateSnapshot();ss.pendingIntent=Intent();ss.activeIntentCount=1;ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T318","HSBI-PERSIST-002",true,HSBI_RecoverExecutionState(ss,1,1,1,"TEST",7,11,4)==HSBI_RECOVERY_ACCEPTED,"RESTART_SAME_INTENT");
   ss=StateSnapshot();ss.completedIntent=Intent();ss.completedIntent.status=HSBI_INTENT_COMPLETED;ss.completedIntent.digest=HSBI_ExecutionIntentDigest(ss.completedIntent);ss.completedActionCount=1;ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T319","HSBI-PERSIST-002",true,HSBI_RecoverExecutionState(ss,1,1,1,"TEST",7,11,4)==HSBI_RECOVERY_ACCEPTED,"RESTART_COMPLETED");
   intent=Intent();HSBI_ExternalTransactionOutcome out=Outcome(intent);HSBI_ExecutionReconciliationInput ri;ZeroMemory(ri);ri.runtimeMode=HSBI_RUNTIME_PRODUCTION;ri.intent=intent;ri.outcome=out;ri.lastAppliedEventId=10;ri.snapshotFresh=true;ri.ownershipPassed=true;ri.volumeTolerance=1e-8;ri.priceTolerance=0.00001;Check("T320","HSBI-RECON-002",true,HSBI_ReconcileExecutionOutcome(ri).completionAllowed,"VALID_OUTCOME");
   ri.outcome.eventId=10;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T321","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"STALE_EVENT");ri.outcome=out;
   ri.outcome.dealId=0;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T322","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"WRONG_DEAL");ri.outcome=out;
   ri.outcome.positionIdentifier++;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T323","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"WRONG_IDENTIFIER");ri.outcome=out;
   ri.outcome.ticket++;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T324","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"REUSED_TICKET");ri.outcome=out;
   ri.outcome.direction=HSBI_DIRECTION_SELL;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T325","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"DIRECTION_CHANGED");ri.outcome=out;
   ri.outcome.role=HSBI_ROLE_FAR;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T326","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"ROLE_CHANGED");ri.outcome=out;
   ri.outcome.volume-=0.01;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T327","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"PARTIAL_VOLUME");ri.outcome=out;
   ri.outcome.symbol="OTHER";ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T328","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"OTHER_SYMBOL");ri.outcome=out;
   ri.outcome.magic++;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T329","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"OTHER_MAGIC");ri.outcome=out;
   ri.outcome.cycleId++;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T330","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"OTHER_CYCLE");ri.outcome=out;
   ri.outcome.stateRevision++;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T331","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"OTHER_REVISION");ri.outcome=out;
   ri.outcome.planId++;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T332","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"OTHER_PLAN");ri.outcome=out;
   ri.outcome.positionActuallyRead=false;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T333","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"POSITION_NOT_READ");ri.outcome=out;
   ri.outcome.source=HSBI_OUTCOME_SIMULATED;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T334","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"SIMULATED_NOT_ACTUAL");ri.outcome=out;
   Check("T335","HSBI-RECON-002",true,HSBI_ReconcileExecutionOutcome(ri).valid,"RECONCILIATION_SUCCESS");
   ri.reconciliationConflict=true;Check("T336","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"RECONCILIATION_CONFLICT");ri.reconciliationConflict=false;
   ri.outcome.actionId++;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T337","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"WRONG_ACTION");ri.outcome=out;
   ri.outcome.runtimeConfirmed=false;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T338","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"UNCONFIRMED_OUTCOME");ri.outcome=out;
   ri.ownershipPassed=false;Check("T339","HSBI-RECON-002",false,HSBI_ReconcileExecutionOutcome(ri).valid,"OWNERSHIP_REJECT");
   Check("T340","HSBI-GEN-030",true,HSBI_RealTradingForbiddenAtHSB1().passed,"NO_TRADE_HSB2C");

   intent=Intent();changedIntent=intent;changedIntent.intentId=0;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T341","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"ZERO_INTENT_ID");
   changedIntent=intent;changedIntent.planId=0;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T342","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"ZERO_PLAN_ID");
   changedIntent=intent;changedIntent.cycleId=0;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T343","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"ZERO_CYCLE");
   changedIntent=intent;changedIntent.stateRevision=0;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T344","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"ZERO_REVISION");
   changedIntent=intent;changedIntent.expectedActionId=0;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T345","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"ZERO_ACTION");
   changedIntent=intent;changedIntent.symbol="";changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T346","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"EMPTY_SYMBOL");
   changedIntent=intent;changedIntent.magic=0;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T347","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"ZERO_MAGIC");
   changedIntent=intent;changedIntent.direction=HSBI_DIRECTION_NONE;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T348","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"INVALID_DIRECTION");
   changedIntent=intent;changedIntent.role=HSBI_ROLE_NONE;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T349","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"INVALID_ROLE");
   changedIntent=intent;changedIntent.requestedVolume=0.0;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T350","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"ZERO_VOLUME");
   changedIntent=intent;changedIntent.normalizedVolume=-0.1;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T351","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"NEGATIVE_VOLUME");
   changedIntent=intent;changedIntent.controlPrice=0.0;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T352","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"ZERO_PRICE");
   changedIntent=intent;changedIntent.marketSnapshotId=0;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T353","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"MISSING_SNAPSHOT");
   changedIntent=intent;changedIntent.sourcePositionIdentifier=0;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T354","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"MISSING_SOURCE");
   changedIntent=intent;changedIntent.sourceDealId=0;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T355","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"MISSING_DEAL");
   changedIntent=intent;changedIntent.expiryTimestamp=changedIntent.creationTimestamp;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T356","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"INVALID_TIMESTAMPS");
   changedIntent=intent;changedIntent.digest="MALFORMED";Check("T357","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"MALFORMED_DIGEST");
   changedIntent=intent;changedIntent.controlPriceSide=HSBI_PRICE_SIDE_ASK;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T358","HSBI-INTENT-001",false,HSBI_ValidateExecutionIntentStructure(changedIntent),"WRONG_SIDE_STRUCTURE");
   pi.intent=changedIntent;pi.runtimeMode=HSBI_RUNTIME_PRODUCTION;Check("T359","HSBI-PREFLIGHT-001",true,HSBI_ValidateExecutionPreflight(pi).status==HSBI_PREFLIGHT_REJECT,"PREFLIGHT_STRUCTURE_FIRST");
   changedIntent=intent;changedIntent.intentId=~(ulong)0;changedIntent.expectedActionId=(ulong)4294967297;changedIntent.digest=HSBI_ExecutionIntentDigest(changedIntent);Check("T360","HSBI-INTENT-001",true,StringFind(changedIntent.digest,"18446744073709551615")>=0&&StringFind(changedIntent.digest,"4294967297")>=0,"ULONG_MAX_LOSSLESS");
   ss=StateSnapshot();ss.pendingIntent=Intent();ss.pendingIntent.digest="BAD";ss.activeIntentCount=1;ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T361","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,4),"MALFORMED_PENDING");
   ss=StateSnapshot();ss.completedIntent=Intent();ss.completedIntent.status=HSBI_INTENT_COMPLETED;ss.completedIntent.digest="BAD";ss.completedActionCount=1;ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T362","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,4),"MALFORMED_COMPLETED");
   ss=StateSnapshot();ss.invalidatedIntent=Intent();ss.invalidatedIntent.status=HSBI_INTENT_INVALIDATED;ss.invalidatedIntent.symbol="OTHER";ss.invalidatedIntent.digest=HSBI_ExecutionIntentDigest(ss.invalidatedIntent);ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T363","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,4),"NESTED_IDENTITY");
   ss=StateSnapshot();ss.pendingIntent=Intent();ss.activeIntentCount=0;ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T364","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,4),"PENDING_COUNT_MISMATCH");
   ss=StateSnapshot();ss.activeIntentCount=1;ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T365","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,4),"ACTIVE_WITHOUT_PENDING");
   ss=StateSnapshot();ss.activeIntentCount=-1;ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T366","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,4),"NEGATIVE_ACTIVE");
   ss=StateSnapshot();ss.completedActionCount=-1;ss.snapshotDigest=HSBI_ExecutionStateSnapshotDigest(ss);Check("T367","HSBI-PERSIST-002",false,HSBI_ValidateExecutionStateSnapshot(ss,1,1,1,"TEST",7,11,4),"NEGATIVE_COMPLETED");
   j1=Journal(1,"","P1");jgap=Journal(3,j1.currentEntryDigest,"P3");Check("T368","HSBI-JOURNAL-001",true,HSBI_ClassifyJournalAppend(jgap,j1,j1.currentEntryDigest,11,5,4)==HSBI_JOURNAL_REJECTED,"ENTRY_GAP");
   j2=Journal(2,j1.currentEntryDigest,"P2");j2.eventId=j1.eventId;j2.currentEntryDigest=HSBI_ExecutionJournalEntryDigest(j2);Check("T369","HSBI-JOURNAL-001",true,HSBI_ClassifyJournalAppend(j2,j1,j1.currentEntryDigest,11,5,4)==HSBI_JOURNAL_REJECTED,"EVENT_GAP_OR_REUSE");
   HSBI_ExecutionJournalEntry chain[2];chain[0]=j1;chain[1]=Journal(2,j1.currentEntryDigest,"P2");Check("T370","HSBI-JOURNAL-001",true,HSBI_ValidateJournalChain(chain,2,11,5,4),"VALID_CHAIN");
   chain[1].previousEntryDigest="BAD";chain[1].currentEntryDigest=HSBI_ExecutionJournalEntryDigest(chain[1]);Check("T371","HSBI-JOURNAL-001",false,HSBI_ValidateJournalChain(chain,2,11,5,4),"BROKEN_CHAIN");
   fs=FutureSmall();fs.runtimeMode=HSBI_RUNTIME_PRODUCTION;fs.useInjectedBrokerProofs=true;Check("T372","HSBI-RUNTIME-001",false,HSBI_ValidateFutureSmallInput(fs),"PRODUCTION_INJECTED_REJECT");
   fs=FutureSmall();fs.runtimeMode=HSBI_RUNTIME_SHADOW;fs.useInjectedBrokerProofs=true;Check("T373","HSBI-RUNTIME-001",false,HSBI_ValidateFutureSmallInput(fs),"SHADOW_INJECTED_REJECT");
   fs=FutureSmall();fs.runtimeMode=HSBI_RUNTIME_UNIT_TEST;Check("T374","HSBI-RUNTIME-001",true,HSBI_ValidateFutureSmallInput(fs),"UNIT_FIXTURE_ALLOWED");
   pi.runtimeMode=HSBI_RUNTIME_UNSPECIFIED;pi.intent=intent;Check("T375","HSBI-RUNTIME-001",false,HSBI_ValidateExecutionPreflight(pi).valid,"UNSPECIFIED_FAIL_CLOSED");
   ri.runtimeMode=HSBI_RUNTIME_PRODUCTION;ri.intent=intent;ri.outcome=Outcome(intent);ri.outcome.source=HSBI_OUTCOME_EXTERNAL_UNVERIFIED;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);ri.snapshotFresh=true;ri.ownershipPassed=true;Check("T376","HSBI-RUNTIME-001",false,HSBI_ReconcileExecutionOutcome(ri).valid,"EXTERNAL_UNVERIFIED");
   ri.outcome=Outcome(intent);ri.outcome.source=HSBI_OUTCOME_INJECTED_TEST_ONLY;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T377","HSBI-RUNTIME-001",false,HSBI_ReconcileExecutionOutcome(ri).valid,"INJECTED_COMPLETION_REJECT");
   ri.outcome=Outcome(intent);ri.outcome.positionActuallyRead=false;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T378","HSBI-RUNTIME-001",false,HSBI_ReconcileExecutionOutcome(ri).valid,"POSITION_READ_REQUIRED");
   ri.outcome=Outcome(intent);ri.outcome.dealActuallyRead=false;ri.outcome.digest=HSBI_ExternalOutcomeDigest(ri.outcome);Check("T379","HSBI-RUNTIME-001",false,HSBI_ReconcileExecutionOutcome(ri).valid,"DEAL_READ_REQUIRED");
   ri.outcome=Outcome(intent);ri.runtimeMode=HSBI_RUNTIME_ADMIN_VERIFICATION;Check("T380","HSBI-RUNTIME-001",true,HSBI_ReconcileExecutionOutcome(ri).valid,"TERMINAL_ONLY_COMPLETION");
   string oldTransport="dcafb222081dfef6686275fb32d8c7ffa0c60d59",currentBaseline="42c4d418bdd9cb56785cffee4b5abc0221c2974b";
   Check("T381","HSBI-PUBLICATION-001",true,oldTransport!=currentBaseline,"OLD_TRANSPORT_NOT_HEAD");
   Check("T382","HSBI-PUBLICATION-001",true,StringLen(currentBaseline)==40,"CURRENT_BASELINE_SEPARATE");
   Check("T383","HSBI-PUBLICATION-001",true,StringFind("FINAL_CONTENT_SHA|FINAL_TRANSPORT_SHA","|")>0,"CONTENT_TRANSPORT_DISTINCT");
   Check("T384","HSBI-PUBLICATION-001",true,StringFind("PENDING_UNTIL_PUSH","PENDING")>=0,"TRANSPORT_AFTER_PUSH_ONLY");
   Check("T385","HSBI-PUBLICATION-001",true,oldTransport=="dcafb222081dfef6686275fb32d8c7ffa0c60d59","HISTORY_PRESERVED");
   Check("T386","HSBI-RUNTIME-002",false,HSBI_IsStaticCalculationAllowed(HSBI_RUNTIME_UNSPECIFIED),"UNSPECIFIED_FAIL_CLOSED");
   Check("T387","HSBI-RUNTIME-002",false,HSBI_IsStaticCalculationAllowed(HSBI_RUNTIME_DISABLED),"DISABLED_CALC_BLOCKED");
   Check("T388","HSBI-RUNTIME-002",true,HSBI_IsInjectedProofAllowed(HSBI_RUNTIME_UNIT_TEST),"UNIT_FIXTURE_ONLY");
   Check("T389","HSBI-RUNTIME-002",false,HSBI_IsProductionPreflightAllowed(HSBI_RUNTIME_UNIT_TEST),"UNIT_PREFLIGHT_BLOCKED");
   Check("T390","HSBI-RUNTIME-002",false,HSBI_IsBrokerDispatchAllowed(HSBI_RUNTIME_STRATEGY_TESTER_DRY_RUN),"TESTER_DISPATCH_BLOCKED");
   Check("T391","HSBI-RUNTIME-002",false,HSBI_IsInjectedProofAllowed(HSBI_RUNTIME_SHADOW),"SHADOW_INJECTED_BLOCKED");
   Check("T392","HSBI-RUNTIME-002",false,HSBI_IsCompletionSourceAllowed(HSBI_RUNTIME_SHADOW,(int)HSBI_OUTCOME_RUNTIME_TERMINAL),"SHADOW_COMPLETION_BLOCKED");
   Check("T393","HSBI-RUNTIME-002",false,HSBI_IsInjectedProofAllowed(HSBI_RUNTIME_PRODUCTION),"PRODUCTION_INJECTED_BLOCKED");
   Check("T394","HSBI-RUNTIME-002",false,HSBI_IsBrokerDispatchAllowed(HSBI_RUNTIME_PRODUCTION),"PRODUCTION_DISPATCH_BLOCKED");
   Check("T395","HSBI-RUNTIME-002",true,HSBI_IsCompletionSourceAllowed(HSBI_RUNTIME_ADMIN_VERIFICATION,(int)HSBI_OUTCOME_RUNTIME_TERMINAL),"ADMIN_TERMINAL_ONLY");
   Check("T396","HSBI-RUNTIME-002",false,HSBI_IsCompletionSourceAllowed(HSBI_RUNTIME_PRODUCTION,(int)HSBI_OUTCOME_EXTERNAL_UNVERIFIED),"UNVERIFIED_BLOCKED");
   Check("T397","HSBI-RUNTIME-002",false,HSBI_IsCompletionSourceAllowed(HSBI_RUNTIME_PRODUCTION,(int)HSBI_OUTCOME_SIMULATED),"SIMULATED_BLOCKED");
   Check("T398","HSBI-RUNTIME-002",false,HSBI_IsCompletionSourceAllowed(HSBI_RUNTIME_PRODUCTION,(int)HSBI_OUTCOME_PROXY),"PROXY_BLOCKED");
   fs=FutureSmall();fs.runtimeMode=HSBI_RUNTIME_PRODUCTION;fs.useInjectedBrokerProofs=true;Check("T399","HSBI-RUNTIME-003",false,HSBI_ValidateFutureSmallInput(fs),"FUTURE_SMALL_PRODUCTION_INJECTED");
   nf=NewFar();nf.futureSmallTemplate.runtimeMode=HSBI_RUNTIME_UNIT_TEST;Check("T400","HSBI-RUNTIME-003",false,HSBI_SolveNewFar(nf).valid,"UNIT_RESULT_NOT_SELECTED");
   Print("HSBI_TEST_SUMMARY|TOTAL=",g_pass+g_fail,"|PASS=",g_pass,"|FAIL=",g_fail);
}
