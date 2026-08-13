#ifndef HSBI_EXTERNAL_OUTCOME_MQH
#define HSBI_EXTERNAL_OUTCOME_MQH
#include "HSBI_ExecutionPreflight.mqh"
enum HSBI_ExternalOutcomeStatus{HSBI_EXTERNAL_PENDING,HSBI_EXTERNAL_COMPLETED,HSBI_EXTERNAL_REJECTED,HSBI_EXTERNAL_PARTIAL,HSBI_EXTERNAL_CONFLICT};
enum HSBI_OutcomeSource{HSBI_OUTCOME_RUNTIME_TERMINAL,HSBI_OUTCOME_EXTERNAL_UNVERIFIED,HSBI_OUTCOME_SIMULATED,HSBI_OUTCOME_INJECTED_TEST_ONLY,HSBI_OUTCOME_PROXY};
struct HSBI_ExternalTransactionOutcome
{
   ulong actionId,eventId,dealId,positionIdentifier,ticket;long accountLogin;string symbol;long magic;
   HSBI_Direction direction;HSBI_Role role;double volume,price;ulong stateRevision,cycleId,planId;
   HSBI_OutcomeSource source;bool runtimeConfirmed,positionActuallyRead,dealActuallyRead;datetime readTimestamp;
   HSBI_ExternalOutcomeStatus status;string digest;
};
string HSBI_ExternalOutcomeDigest(const HSBI_ExternalTransactionOutcome &x)
{return HSBI_UlongToString(x.actionId)+"|"+HSBI_UlongToString(x.eventId)+"|"+HSBI_UlongToString(x.dealId)+"|"+
   HSBI_UlongToString(x.positionIdentifier)+"|"+HSBI_UlongToString(x.ticket)+"|"+LongToString(x.accountLogin)+"|"+x.symbol+"|"+
   LongToString(x.magic)+"|"+IntegerToString((int)x.direction)+"|"+IntegerToString((int)x.role)+"|"+DoubleToString(x.volume,8)+"|"+
   DoubleToString(x.price,12)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.planId)+"|"+
   IntegerToString((int)x.source)+"|"+IntegerToString((int)x.runtimeConfirmed)+"|"+IntegerToString((int)x.positionActuallyRead)+"|"+
   IntegerToString((int)x.dealActuallyRead)+"|"+LongToString((long)x.readTimestamp)+"|"+IntegerToString((int)x.status);}
struct HSBI_ExecutionReconciliationInput{HSBI_RuntimeMode runtimeMode;HSBI_ExecutionIntent intent;HSBI_ExternalTransactionOutcome outcome;ulong lastAppliedEventId;bool reconciliationConflict,snapshotFresh,ownershipPassed;double volumeTolerance,priceTolerance;};
struct HSBI_ExecutionReconciliationResult{bool valid,completionAllowed,noMutationBeforeCommit;HSBI_IntentStatus targetStatus;HSBI_ReasonCode reason;string details;string digest;};
HSBI_ExecutionReconciliationResult HSBI_ReconcileExecutionOutcome(const HSBI_ExecutionReconciliationInput &x)
{
   HSBI_ExecutionReconciliationResult r;ZeroMemory(r);r.targetStatus=HSBI_INTENT_RECONCILING;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details="RECONCILIATION_REJECTED";r.noMutationBeforeCommit=true;
   if((x.runtimeMode!=HSBI_RUNTIME_PRODUCTION&&x.runtimeMode!=HSBI_RUNTIME_ADMIN_VERIFICATION)||!HSBI_ValidateExecutionIntentDigest(x.intent)||x.outcome.digest!=HSBI_ExternalOutcomeDigest(x.outcome)||x.reconciliationConflict||!x.snapshotFresh||!x.ownershipPassed)return r;
   if(x.outcome.status!=HSBI_EXTERNAL_COMPLETED||x.outcome.source!=HSBI_OUTCOME_RUNTIME_TERMINAL||!x.outcome.runtimeConfirmed||!x.outcome.positionActuallyRead||!x.outcome.dealActuallyRead)return r;
   if(x.outcome.actionId!=x.intent.expectedActionId||x.outcome.eventId<=x.lastAppliedEventId||x.outcome.dealId==0||x.outcome.positionIdentifier!=x.intent.sourcePositionIdentifier||
      x.outcome.ticket!=x.intent.sourceTicket||x.outcome.accountLogin!=x.intent.accountLogin||x.outcome.symbol!=x.intent.symbol||x.outcome.magic!=x.intent.magic||
      x.outcome.direction!=x.intent.direction||x.outcome.role!=x.intent.role||x.outcome.stateRevision!=x.intent.stateRevision||x.outcome.cycleId!=x.intent.cycleId||
      x.outcome.planId!=x.intent.planId||MathAbs(x.outcome.volume-x.intent.normalizedVolume)>x.volumeTolerance||MathAbs(x.outcome.price-x.intent.controlPrice)>x.priceTolerance)return r;
   r.valid=true;r.completionAllowed=true;r.targetStatus=HSBI_INTENT_COMPLETED;r.reason=HSBI_REASON_OK;r.details="RECONCILIATION_PASSED";r.digest=x.intent.digest+"|"+x.outcome.digest;return r;
}
#endif
