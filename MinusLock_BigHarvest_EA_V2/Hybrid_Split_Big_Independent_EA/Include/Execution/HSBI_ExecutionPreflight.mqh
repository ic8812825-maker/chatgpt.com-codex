#ifndef HSBI_EXECUTION_PREFLIGHT_MQH
#define HSBI_EXECUTION_PREFLIGHT_MQH
#include "HSBI_ExecutionIntent.mqh"
#include "../Core/HSBI_RuntimePolicy.mqh"
#include "../Planning/HSBI_FutureSmallProofAggregator.mqh"
#include "../Money/HSBI_ReserveCatchUpEvaluator.mqh"
enum HSBI_PreflightStatus{HSBI_PREFLIGHT_PASS,HSBI_PREFLIGHT_REJECT,HSBI_PREFLIGHT_ERROR,HSBI_PREFLIGHT_UNAVAILABLE,HSBI_PREFLIGHT_STALE,HSBI_PREFLIGHT_CONFLICT,HSBI_PREFLIGHT_DIGEST_MISMATCH};
struct HSBI_ExecutionPreflightInput
{
   HSBI_RuntimeMode runtimeMode;HSBI_ExecutionIntent intent;HSBI_FutureSmallAggregateProof aggregate;HSBI_ReserveCatchUpResult catchUp;
   HSBI_BrokerProperties broker;HSBI_ControlPrice controlPrice;long currentAccount;string currentSymbol;long currentMagic;
   ulong currentCycleId,currentStateRevision;datetime now;bool planningFullyProven,worstCasePresent,farLossProofPresent;
   bool proxyOrTestOnly,reconciliationConflict,activeIntentPresent,marketFresh,allocationConflict;
   ulong appliedActionId;string appliedActionPayloadDigest;
};
struct HSBI_ExecutionPreflightResult{HSBI_PreflightStatus status;bool valid;HSBI_ReasonCode reason;string details;string digest;};
HSBI_ExecutionPreflightResult HSBI_ValidateExecutionPreflight(const HSBI_ExecutionPreflightInput &x)
{
   HSBI_ExecutionPreflightResult r;ZeroMemory(r);r.status=HSBI_PREFLIGHT_REJECT;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details="REJECT";
   if(!HSBI_IsProductionPreflightAllowed(x.runtimeMode)||!HSBI_ValidateExecutionIntentStructure(x.intent)){r.reason=HSBI_REASON_INVALID_INTENT_STRUCTURE;r.details="INVALID_INTENT_STRUCTURE";return r;}
   if(!HSBI_ValidateExecutionIntentDigest(x.intent)){r.status=HSBI_PREFLIGHT_DIGEST_MISMATCH;r.details="INTENT_DIGEST_MISMATCH";return r;}
   if(x.intent.planDigest==""||x.intent.candidateDigest==""||x.intent.aggregateProofDigest!=x.aggregate.aggregateDigest){r.status=HSBI_PREFLIGHT_DIGEST_MISMATCH;r.details="PLAN_CANDIDATE_AGGREGATE_DIGEST_MISMATCH";return r;}
   if(!x.marketFresh||x.now>x.intent.expiryTimestamp||!x.controlPrice.fresh){r.status=HSBI_PREFLIGHT_STALE;r.details="STALE_OR_EXPIRED";return r;}
   if(x.reconciliationConflict||x.activeIntentPresent||x.allocationConflict||(x.appliedActionId==x.intent.expectedActionId&&x.appliedActionPayloadDigest!=x.intent.digest)){r.status=HSBI_PREFLIGHT_CONFLICT;r.details="CONFLICT";return r;}
   if(!x.planningFullyProven||!x.aggregate.valid||x.aggregate.levelCount<2||!x.worstCasePresent||!x.aggregate.runtimeConfirmed||
      !x.catchUp.valid||!x.catchUp.runtimeConfirmed||!x.catchUp.reserveSourceIdentityValid||!x.catchUp.farLossSourceIdentityValid||
      !x.farLossProofPresent||x.proxyOrTestOnly){r.status=HSBI_PREFLIGHT_UNAVAILABLE;r.details="PROOF_UNAVAILABLE";return r;}
   if(x.currentAccount!=x.intent.accountLogin||x.currentSymbol!=x.intent.symbol||x.currentMagic!=x.intent.magic||x.currentCycleId!=x.intent.cycleId||
      x.currentStateRevision!=x.intent.stateRevision){r.details="IDENTITY_OR_REVISION_MISMATCH";return r;}
   if(HSBI_ValidateBrokerProperties(x.broker)!=HSBI_BROKER_PROPERTIES_VALID||!HSBI_ValidateVolume(x.intent.normalizedVolume,x.broker)||
      !HSBI_ValidateTypedControlPrice(x.controlPrice,x.intent.symbol)||MathAbs(x.intent.controlPrice-x.controlPrice.selectedPrice)>HSBI_GridTolerance(x.broker.tickSize)){
      r.details="GRID_OR_PRICE_REJECT";return r;}
   r.status=HSBI_PREFLIGHT_PASS;r.valid=true;r.reason=HSBI_REASON_OK;r.details="PASS";r.digest=x.intent.digest+"|PREFLIGHT_PASS";return r;
}
bool HSBI_IsIntentLifecycleTransitionAllowed(const HSBI_IntentStatus from,const HSBI_IntentStatus to,const bool validOutcome)
{
   if(to==HSBI_INTENT_REJECTED||to==HSBI_INTENT_EXPIRED||to==HSBI_INTENT_INVALIDATED||to==HSBI_INTENT_CONFLICT)return from!=HSBI_INTENT_COMPLETED;
   if(from==HSBI_INTENT_CREATED)return to==HSBI_INTENT_PREFLIGHT_PASSED;
   if(from==HSBI_INTENT_PREFLIGHT_PASSED)return to==HSBI_INTENT_PERSISTED;
   if(from==HSBI_INTENT_PERSISTED)return to==HSBI_INTENT_DISPATCH_BLOCKED;
   if(from==HSBI_INTENT_DISPATCH_BLOCKED)return to==HSBI_INTENT_OUTCOME_PENDING||to==HSBI_INTENT_RECONCILING;
   if(from==HSBI_INTENT_OUTCOME_PENDING)return to==HSBI_INTENT_OUTCOME_RECEIVED||to==HSBI_INTENT_RECONCILING;
   if(from==HSBI_INTENT_OUTCOME_RECEIVED)return to==HSBI_INTENT_RECONCILING;
   if(from==HSBI_INTENT_RECONCILING)return to==HSBI_INTENT_COMPLETED&&validOutcome;
   return false;
}
bool HSBI_IntentRetryAllowed(const HSBI_ExecutionIntent &x,const ulong retryActionId)
{return retryActionId==x.expectedActionId&&(x.status==HSBI_INTENT_OUTCOME_PENDING||x.status==HSBI_INTENT_RECONCILING||x.status==HSBI_INTENT_DISPATCH_BLOCKED);}
#endif
