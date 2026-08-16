#ifndef HSBI_RUNTIME_DECISION_VALIDATOR_MQH
#define HSBI_RUNTIME_DECISION_VALIDATOR_MQH
#include "HSBI_RuntimeDecisionTypes.mqh"
HSBI_RuntimeDecisionResult HSBI_RuntimeReject(const HSBI_RuntimeDecisionContext &x,const HSBI_RuntimeDecisionStatus status,const HSBI_RuntimeDecisionReason reason,const string req){HSBI_RuntimeDecisionResult r;ZeroMemory(r);r.status=status;r.reason=reason;r.planId=x.planId;r.cycleId=x.cycleId;r.stateRevision=x.stateRevision;r.inputDigest=x.inputDigest;r.requirementId=req;return r;}
bool HSBI_RuntimePositionMatches(const HSBI_PositionDescriptor &p,const HSBI_RuntimeDecisionContext &x,const HSBI_Role role){return p.identifier>0&&p.ticket>0&&p.actualVolume>0.0&&p.role==role&&p.direction!=HSBI_DIRECTION_NONE&&p.identity.accountLogin==x.accountLogin&&p.identity.symbol==x.symbol&&p.identity.magic==x.magic&&p.identity.cycleId==x.cycleId;}
HSBI_RuntimeDecisionResult HSBI_ValidateRuntimeDecisionContext(const HSBI_RuntimeDecisionContext &x,const long account,const string symbol,const long magic,const ulong cycle,const ulong plan,const ulong revision)
{
 if(!x.immutable||!HSBI_IsProductionPreflightAllowed(x.runtimeMode))return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_CONTEXT_INVALID,"HSBI-2D-CTX");
 if(x.accountLogin!=account||x.symbol!=symbol||x.magic!=magic||x.cycleId!=cycle||x.planId!=plan)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_IDENTITY_MISMATCH,"HSBI-2D-ID");
 if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,"HSBI-2D-REV");
 if(x.schemaVersion!=HSBI_SCHEMA_VERSION)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_SCHEMA_VERSION_MISMATCH,"HSBI-2D-SCHEMA");
 if(x.moneyStateVersion!=HSBI_MONEY_STATE_VERSION)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_MONEY_STATE_VERSION_MISMATCH,"HSBI-2D-MONEY-VERSION");
 if(!x.marketFresh||!x.costFresh||!x.allocationPolicy.fresh)return HSBI_RuntimeReject(x,HSBI_DECISION_STALE,HSBI_RD_STALE_SNAPSHOT,"HSBI-2D-FRESH");
 if(x.reconciliationConflict)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_RECONCILIATION_CONFLICT,"HSBI-2D-RECON");
 if(!x.reconciliationConfirmed)return HSBI_RuntimeReject(x,HSBI_DECISION_RECONCILIATION_REQUIRED,HSBI_RD_RECONCILIATION_REQUIRED,"HSBI-2D-RECON");
 if(x.eventId==0||x.actionId==0)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,x.eventId==0?HSBI_RD_EVENT_NOT_FRESH:HSBI_RD_ACTION_ID_MISMATCH,"HSBI-2D-EVENT");
 if(!x.positionActuallyRead||!x.ownershipConfirmed)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_POSITION_NOT_CONFIRMED,"HSBI-2D-POS");
 if(!x.residualActual||!HSBI_RuntimePositionMatches(x.actualResidual,x,HSBI_ROLE_BIG_CORE))return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_ACTUAL_RESIDUAL_REQUIRED,"HSBI-2D-RESIDUAL");
 if(!x.aggregate.valid||x.aggregate.levelCount<2||x.aggregate.evaluatedLevelCount!=x.aggregate.levelCount||!x.aggregate.runtimeConfirmed||!x.aggregate.allMoneyProofsValid||!x.aggregate.allMarginProofsValid||!x.aggregate.allRiskProofsValid)return HSBI_RuntimeReject(x,HSBI_DECISION_UNAVAILABLE,HSBI_RD_FUTURE_SMALL_INCOMPLETE,"HSBI-2D-FS");
 if(!HSBI_IsCompleteCandidateProof(x.candidate)||x.candidate.sourceBigCoreIdentifier!=x.actualResidual.identifier||x.candidate.sourceBigCoreTicket!=x.actualResidual.ticket)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_NEW_FAR_INVALID,"HSBI-2D-NF");
 if(!x.catchUp.valid||!x.catchUp.runtimeConfirmed||!x.catchUp.reserveSourceIdentityValid||!x.catchUp.farLossSourceIdentityValid)return HSBI_RuntimeReject(x,HSBI_DECISION_UNAVAILABLE,HSBI_RD_CATCH_UP_INVALID,"HSBI-2D-CATCHUP");
 if(!x.moneyRuntimeConfirmed||!HSBI_ValidateMoneyProofIdentity(x.moneyIdentity)||!x.marginRuntimeConfirmed)return HSBI_RuntimeReject(x,HSBI_DECISION_UNAVAILABLE,HSBI_RD_MONEY_UNAVAILABLE,"HSBI-2D-MONEY");
 if(!x.riskRuntimeConfirmed||!HSBI_ValidateMoneyProofIdentity(x.riskIdentity))return HSBI_RuntimeReject(x,HSBI_DECISION_UNAVAILABLE,HSBI_RD_RISK_UNAVAILABLE,"HSBI-2D-RISK");
 if(!HSBI_ValidateAllocationPolicy(x.allocationPolicy)||!HSBI_ValidateReserveAllocationSource(x.allocationSource))return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_ALLOCATION_CONFLICT,"HSBI-2D-ALLOC");
 if(x.consumptionConflict||!HSBI_ValidateReserveConsumption(x.consumptionKey,x.planId,x.stateRevision))return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_CONSUMPTION_CONFLICT,"HSBI-2D-CONSUME");
 if(!x.persistencePrepared)return HSBI_RuntimeReject(x,HSBI_DECISION_PERSISTENCE_REQUIRED,HSBI_RD_PERSISTENCE_REQUIRED,"HSBI-2D-PERSIST");
 if(x.inputDigest==""||x.inputDigest!=HSBI_RuntimeDecisionContextDigest(x))return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_DIGEST_MISMATCH,"HSBI-2D-DIGEST");
 HSBI_RuntimeDecisionResult r=HSBI_RuntimeReject(x,HSBI_DECISION_VALID,HSBI_RD_OK,"HSBI-2D-VALID");r.valid=true;r.selectedCandidate=x.candidate;r.selectedAggregate=x.aggregate;r.catchUp=x.catchUp;r.allocation=x.allocationSource;r.requiredNextState=HSBI_STATE_RECONCILING;r.pendingActionId=x.actionId;r.outputDigest=x.inputDigest+"|VALID";return r;
}
#endif
