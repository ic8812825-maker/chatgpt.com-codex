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
   Print("HSBI_TEST_SUMMARY|TOTAL=",g_pass+g_fail,"|PASS=",g_pass,"|FAIL=",g_fail);
}
