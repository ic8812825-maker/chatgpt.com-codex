#ifndef HSBI_RUNTIME_TRANSACTION_BARRIER_MQH
#define HSBI_RUNTIME_TRANSACTION_BARRIER_MQH
#include "HSBI_RuntimeRestartValidator.mqh"
struct HSBI_RuntimeBarrierInput{HSBI_RuntimeDecisionContext context;ulong expectedEventId,expectedActionId,expectedPlanId,expectedCycleId,expectedStateRevision,lastCompletedActionId;string expectedDigest,lastCompletedPayloadDigest,payloadDigest;bool snapshotsFresh,reconciliationAllowed,positionRead,ticketConfirmed,volumeConfirmed,directionConfirmed,ownershipConfirmed,moneyConfirmed,marginConfirmed,riskConfirmed,persistencePrepared,completedOutcome,retryRequested;};
HSBI_RuntimeDecisionResult HSBI_CanAdvanceRuntimeDecision(const HSBI_RuntimeBarrierInput &b)
{
 HSBI_RuntimeDecisionResult admission=HSBI_ValidateRuntimeDecisionContext(b.context,b.context.accountLogin,b.context.symbol,b.context.magic,b.expectedCycleId,b.expectedPlanId,b.expectedStateRevision);if(!admission.valid)return admission;
 if(b.completedOutcome||b.lastCompletedActionId==b.expectedActionId){if(b.lastCompletedActionId==b.expectedActionId&&b.lastCompletedPayloadDigest==b.payloadDigest)return HSBI_RuntimeReject(b.context,HSBI_DECISION_NO_OP,HSBI_RD_OK,"HSBI-2D-BARRIER-NOOP");return HSBI_RuntimeReject(b.context,HSBI_DECISION_CONFLICT,HSBI_RD_PENDING_ACTION_CONFLICT,"HSBI-2D-BARRIER-COMPLETED");}
 if(!b.snapshotsFresh)return HSBI_RuntimeReject(b.context,HSBI_DECISION_STALE,HSBI_RD_STALE_SNAPSHOT,"HSBI-2D-BARRIER-FRESH");
 if(!b.reconciliationAllowed)return HSBI_RuntimeReject(b.context,HSBI_DECISION_RECONCILIATION_REQUIRED,HSBI_RD_RECONCILIATION_REQUIRED,"HSBI-2D-BARRIER-RECON");
 if(b.context.eventId<=b.expectedEventId)return HSBI_RuntimeReject(b.context,HSBI_DECISION_REJECTED,HSBI_RD_EVENT_NOT_FRESH,"HSBI-2D-BARRIER-EVENT");
 if(b.context.actionId!=b.expectedActionId)return HSBI_RuntimeReject(b.context,HSBI_DECISION_CONFLICT,HSBI_RD_ACTION_ID_MISMATCH,"HSBI-2D-BARRIER-ACTION");
 if(!b.positionRead||!b.ticketConfirmed||!b.volumeConfirmed||!b.directionConfirmed||!b.ownershipConfirmed)return HSBI_RuntimeReject(b.context,HSBI_DECISION_REJECTED,HSBI_RD_POSITION_NOT_CONFIRMED,"HSBI-2D-BARRIER-POS");
 if(!b.moneyConfirmed||!b.marginConfirmed)return HSBI_RuntimeReject(b.context,HSBI_DECISION_UNAVAILABLE,HSBI_RD_MONEY_UNAVAILABLE,"HSBI-2D-BARRIER-MONEY");if(!b.riskConfirmed)return HSBI_RuntimeReject(b.context,HSBI_DECISION_UNAVAILABLE,HSBI_RD_RISK_UNAVAILABLE,"HSBI-2D-BARRIER-RISK");
 if(!b.persistencePrepared)return HSBI_RuntimeReject(b.context,HSBI_DECISION_PERSISTENCE_REQUIRED,HSBI_RD_PERSISTENCE_REQUIRED,"HSBI-2D-BARRIER-PERSIST");
 if(b.expectedDigest==""||b.expectedDigest!=b.context.inputDigest)return HSBI_RuntimeReject(b.context,HSBI_DECISION_CONFLICT,HSBI_RD_DIGEST_MISMATCH,"HSBI-2D-BARRIER-DIGEST");
 admission.outputDigest=b.context.inputDigest+"|ADVANCE";admission.requirementId="HSBI-2D-BARRIER";return admission;
}
#endif
