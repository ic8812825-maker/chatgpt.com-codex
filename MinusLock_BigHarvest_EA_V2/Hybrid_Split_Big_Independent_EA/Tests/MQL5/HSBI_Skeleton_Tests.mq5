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
#include "../../Include/Planning/HSBI_NewFarCandidate.mqh"
#include "../../Include/Money/HSBI_AllocationLedgerTypes.mqh"
#include "../../Include/Execution/HSBI_TransactionTypes.mqh"
#include "../../Include/Execution/HSBI_NoTradeExecution.mqh"
#include "../../Include/Execution/HSBI_OwnershipGuardTypes.mqh"
#include "../../Include/Persistence/HSBI_SnapshotTypes.mqh"
#include "../../Include/Persistence/HSBI_ReconciliationTypes.mqh"

int g_pass=0,g_fail=0;
void Check(const string id,const string req,const bool expected,const bool actual){bool ok=(expected==actual);Print("TEST_ID=",id,"|Requirement=",req,"|Expected=",expected,"|Actual=",actual,"|",ok?"PASS":"FAIL");if(ok)g_pass++;else g_fail++;}

void OnStart(){
 Check("T01","HSBI-GEN-030",true,HSBI_RUNTIME_DISABLED!=HSBI_RUNTIME_UNIT_TEST);
 Check("T02","HSBI-GEN-030",true,HSBI_IsRuntimeModeAllowedAtStage1(HSBI_RUNTIME_UNIT_TEST));
 Check("T03","HSBI-GEN-030",false,HSBI_IsRuntimeModeAllowedAtStage1(HSBI_RUNTIME_REAL_LIMITED));
 HSBI_Identity a;a.accountLogin=1;a.symbol="EURUSD";a.magic=7;a.cycleId=1;a.positionIdentifier=10;a.role=HSBI_ROLE_FAR;
 HSBI_Identity b=a;Check("T04","HSBI-ID-010",true,HSBI_IsValidIdentity(a));Check("T05","HSBI-ID-010",true,HSBI_SameCycle(a,b));b.positionIdentifier=11;Check("T06","HSBI-ID-010",false,HSBI_SamePositionOwner(a,b));
 HSBI_RecoveryContext c;HSBI_InitializeContext(c,HSBI_RUNTIME_UNIT_TEST);c.far.role=HSBI_ROLE_FAR;Check("T07","HSBI-ID-010",true,HSBI_ExactlyOneFarOrZero(c).passed);c.bigCore.role=HSBI_ROLE_FAR;Check("T08","HSBI-ID-010",false,HSBI_ExactlyOneFarOrZero(c).passed);
 HSBI_PositionDescriptor p;ZeroMemory(p);p.role=HSBI_ROLE_BIG_CORE;p.identifier=77;p.ticket=88;p.actualVolume=0.5;Check("T09","HSBI-NF-001",true,HSBI_CanPromoteToFar(p,77));p.role=HSBI_ROLE_BIG_TREND;Check("T10","HSBI-NF-001",false,HSBI_CanPromoteToFar(p,77));p.role=HSBI_ROLE_SMALL_BASE;Check("T11","HSBI-NF-001",false,HSBI_CanPromoteToFar(p,77));p.role=HSBI_ROLE_BIG_CORE;Check("T12","HSBI-NF-001",true,HSBI_CanPromoteToFar(p,77));
 Check("T13","HSBI-FSM-002",true,HSBI_IsTransitionAllowed(HSBI_STATE_DISABLED,HSBI_STATE_IDLE));Check("T14","HSBI-FSM-002",false,HSBI_IsTransitionAllowed(HSBI_STATE_IDLE,HSBI_STATE_CYCLE_CLOSED));
 Check("T15","HSBI-TX-006",false,HSBI_IsCompletedOutcome(HSBI_TX_PLACED));Check("T16","HSBI-TX-006",false,HSBI_IsCompletedOutcome(HSBI_TX_PARTIAL));Check("T17","HSBI-TX-006",false,HSBI_IsCompletedOutcome(HSBI_TX_TIMEOUT));
 HSBI_AllocationLedgerRecord ar;ZeroMemory(ar);ar.valid=true;ar.sourceDealKey="d";ar.sourceDealNet=100;ar.finalReserveAllocated=60;ar.partialFarAllocated=20;ar.transitionAllocated=10;ar.carryAllocated=5;ar.residual=5;ar.available=100;Check("T18","HSBI-MONEY-014",true,HSBI_ValidateAllocationConservation(ar));ar.sourceDealNet=-1;Check("T19","HSBI-MONEY-014",false,HSBI_ValidateAllocationConservation(ar));Check("T20","HSBI-PF-001",false,HSBI_CanConsumeBucket(HSBI_BUCKET_FINAL_RESERVE,true));
 HSBI_NewFarCandidate n1,n2;ZeroMemory(n1);ZeroMemory(n2);n1.normalizedVolume=0.2;n2.normalizedVolume=0.3;Check("T21","HSBI-NF-010",true,HSBI_CompareCandidateTieBreak(n1,n2)<0);
 HSBI_SnapshotRecord s;ZeroMemory(s);s.schemaVersion=HSBI_SNAPSHOT_SCHEMA_VERSION;s.moneyStateVersion=HSBI_MONEY_STATE_VERSION;s.stateRevision=1;s.timestamp=TimeCurrent();Check("T22","HSBI-PERSIST-001",true,HSBI_ValidateSnapshotSchema(s));Check("T23","HSBI-FSM-002",true,HSBI_StateRevisionMonotonic(1,2).passed);
 HSBI_ReconciliationInput ri;ZeroMemory(ri);HSBI_ReconciliationResult rr=HSBI_CompareReconciliation(ri);Check("T24","HSBI-RECON-002",true,rr.outcome==HSBI_RECON_CLEAN_START);
 Check("T25","HSBI-GEN-030",false,HSBI_SubmitActionStub().success);Check("T26","HSBI-GEN-030",true,HSBI_RealTradingForbiddenAtHSB1().passed);
 Print("HSBI_TEST_SUMMARY|PASS=",g_pass,"|FAIL=",g_fail);
}