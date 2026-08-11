#property strict
#property script_show_inputs
#include "../../Include/Core/HSBI_Version.mqh"
#include "../../Include/Core/HSBI_Enums.mqh"
#include "../../Include/Core/HSBI_Types.mqh"
#include "../../Include/Core/HSBI_ReasonCodes.mqh"
#include "../../Include/Core/HSBI_Identifiers.mqh"
#include "../../Include/Core/HSBI_Roles.mqh"
#include "../../Include/Core/HSBI_RuntimeMode.mqh"
#include "../../Include/Core/HSBI_Context.mqh"
#include "../../Include/Core/HSBI_StateMachine.mqh"
#include "../../Include/Core/HSBI_StateValidator.mqh"
#include "../../Include/Core/HSBI_Invariants.mqh"
#include "../../Include/Execution/HSBI_TransactionTypes.mqh"
#include "../../Include/Execution/HSBI_NoTradeExecution.mqh"
#include "../../Include/Execution/HSBI_OwnershipGuardTypes.mqh"

int g_pass=0,g_fail=0;
void Check(const string id,const string req,const bool expected,const bool actual,const string reason)
{
   bool ok=(expected==actual);
   Print("TEST_ID=",id,"|Requirement=",req,"|Expected=",expected,"|Actual=",actual,"|Result=",ok?"PASS":"FAIL","|ReasonCode=",reason);
   if(ok)g_pass++;else g_fail++;
}

HSBI_OwnershipGuardInput OwnershipInput(const HSBI_Identity &expected,const HSBI_Identity &actual)
{
   HSBI_OwnershipGuardInput x;ZeroMemory(x);x.expectedIdentity=expected;x.actualIdentity=actual;x.expectedRole=expected.role;x.actualRole=actual.role;x.expectedDirection=HSBI_DIRECTION_BUY;x.actualDirection=HSBI_DIRECTION_BUY;x.expectedVolume=0.5;x.actualVolume=0.5;x.expectedStateRevision=4;x.actualStateRevision=4;x.planId=1;x.actionId=1;return x;
}

void OnStart()
{
   Check("T01","HSBI-GEN-030",true,HSBI_IsRuntimeModeAllowedAtStage1(HSBI_RUNTIME_UNIT_TEST),"OK");
   Check("T02","HSBI-GEN-030",false,HSBI_IsRuntimeModeAllowedAtStage1(HSBI_RUNTIME_REAL_LIMITED),"REAL_TRADING_FORBIDDEN");
   Check("T03","HSBI-ID-010",true,HSBI_UlongToString((ulong)4294967296)=="4294967296","OK");

   HSBI_Identity a;a.accountLogin=1;a.symbol="EURUSD";a.magic=7;a.cycleId=1;a.positionIdentifier=10;a.role=HSBI_ROLE_FAR;
   Check("T04","HSBI-ID-010",true,HSBI_IsValidIdentity(a),"OK");
   HSBI_Identity b=a;b.symbol="GBPUSD";Check("T05","HSBI-ID-010",false,HSBI_EvaluateOwnership(OwnershipInput(a,b)).allowed,"INVALID_IDENTITY_SYMBOL");
   b=a;b.magic=8;Check("T06","HSBI-ID-010",false,HSBI_EvaluateOwnership(OwnershipInput(a,b)).allowed,"INVALID_IDENTITY_MAGIC");
   b=a;b.accountLogin=2;Check("T07","HSBI-ID-010",false,HSBI_EvaluateOwnership(OwnershipInput(a,b)).allowed,"INVALID_IDENTITY_ACCOUNT");
   b=a;b.cycleId=2;Check("T08","HSBI-ID-010",false,HSBI_EvaluateOwnership(OwnershipInput(a,b)).allowed,"INVALID_IDENTITY_CYCLE");
   b=a;b.positionIdentifier=11;Check("T09","HSBI-ID-010",false,HSBI_EvaluateOwnership(OwnershipInput(a,b)).allowed,"INVALID_POSITION_IDENTIFIER");
   b=a;b.role=HSBI_ROLE_BIG_CORE;Check("T10","HSBI-ID-010",false,HSBI_EvaluateOwnership(OwnershipInput(a,b)).allowed,"INVALID_ROLE");

   HSBI_PositionDescriptor p1,p2;ZeroMemory(p1);ZeroMemory(p2);p1.identity=a;p2.identity=a;p1.identifier=10;p2.identifier=10;p1.role=HSBI_ROLE_FAR;p2.role=HSBI_ROLE_FAR;p1.ticket=100;p2.ticket=999;
   Check("T11","HSBI-ID-010",true,HSBI_TicketDoesNotDefineOwnership(p1,p2),"STALE_REUSED_TICKET_IGNORED");
   HSBI_OwnershipGuardInput ox=OwnershipInput(a,a);ox.actualVolume=0.4;Check("T12","HSBI-ID-010",false,HSBI_EvaluateOwnership(ox).allowed,"CHANGED_VOLUME");
   ox=OwnershipInput(a,a);ox.actualRole=HSBI_ROLE_BIG_CORE;Check("T13","HSBI-ID-010",false,HSBI_EvaluateOwnership(ox).allowed,"CHANGED_ROLE");

   HSBI_RecoveryContext c;HSBI_InitializeContext(c,HSBI_RUNTIME_UNIT_TEST);c.far.role=HSBI_ROLE_FAR;c.bigCore.role=HSBI_ROLE_FAR;
   Check("T14","HSBI-ID-010",false,HSBI_ExactlyOneFarOrZero(c).passed,"DUPLICATE_FAR");
   HSBI_PositionDescriptor residual;ZeroMemory(residual);residual.identity=a;residual.identity.positionIdentifier=77;residual.identifier=77;residual.role=HSBI_ROLE_BIG_CORE;residual.actualVolume=0.25;
   Check("T15","HSBI-NF-001",true,HSBI_IsActualBigCoreResidual(residual,77)&&!HSBI_ValidateRoleTransition(HSBI_ROLE_SMALL_BASE,HSBI_ROLE_FAR),"ACTUAL_RESIDUAL_ONLY");

   Check("T16","HSBI-FSM-002",true,HSBI_IsTransitionAllowed(HSBI_STATE_DISABLED,HSBI_STATE_IDLE),"OK");
   Check("T17","HSBI-FSM-002",false,HSBI_IsTransitionAllowed(HSBI_STATE_IDLE,HSBI_STATE_CYCLE_CLOSED),"INVALID_STATE_TRANSITION");
   HSBI_TransactionMetadata tx;ZeroMemory(tx);tx.actionId=50;tx.eventId=60;tx.actualPositionRead=true;tx.outcome=HSBI_TX_PLACED;
   Check("T18","HSBI-TX-006",false,HSBI_TransactionPermitsStateTransition(tx,50),"PLACED_BARRIER");
   tx.outcome=HSBI_TX_PARTIAL;Check("T19","HSBI-TX-006",false,HSBI_TransactionPermitsStateTransition(tx,50),"PARTIAL_FILL_PENDING");
   tx.outcome=HSBI_TX_TIMEOUT;Check("T20","HSBI-TX-006",false,HSBI_TransactionPermitsStateTransition(tx,50),"TIMEOUT_BARRIER");
   tx.outcome=HSBI_TX_COMPLETED;Check("T21","HSBI-TX-006",true,HSBI_TransactionPermitsStateTransition(tx,50),"COMPLETED_FILL");
   Check("T22","HSBI-TX-006",false,HSBI_IsFreshEvent(60,59)||HSBI_IsFreshEvent(60,60),"DELAYED_OR_DUPLICATE_EVENT");
   Check("T23","HSBI-TX-006",true,HSBI_IsRetryOfSameAction(50,50)&&!HSBI_IsRetryOfSameAction(50,51),"SAME_ACTION_ID");
   Check("T24","HSBI-RECON-002",true,HSBI_ConflictTargetState()==HSBI_STATE_RECONCILING,"RECONCILIATION_REQUIRED");
   Check("T25","HSBI-FSM-002",true,HSBI_CriticalErrorTargetState(false)==HSBI_STATE_EMERGENCY&&HSBI_CriticalErrorTargetState(true)==HSBI_STATE_TERMINAL_SAFE,"CRITICAL_ERROR_ROUTE");
   HSBI_RecoveryContext closed;HSBI_InitializeContext(closed,HSBI_RUNTIME_UNIT_TEST);closed.currentState=HSBI_STATE_CYCLE_CLOSED;closed.pendingActionId=1;closed.stateRevision=7;
   Check("T26","HSBI-FSM-002",false,HSBI_ValidateStateTopology(closed).passed||closed.stateRevision!=7,"CLOSED_PENDING_ACTION");
   Print("HSBI_TEST_SUMMARY|TOTAL=",g_pass+g_fail,"|PASS=",g_pass,"|FAIL=",g_fail);
}
