#ifndef HSBI_RUNTIME_RESTART_VALIDATOR_MQH
#define HSBI_RUNTIME_RESTART_VALIDATOR_MQH
#include "HSBI_RuntimeDecisionValidator.mqh"
struct HSBI_RestartedRuntimeState{HSBI_RuntimeDecisionContext current;HSBI_ExecutionStateSnapshot persisted;ulong expectedPlanId,expectedStateRevision,expectedEventId,expectedActionId;HSBI_PositionDescriptor persistedResidual;HSBI_ReserveAllocationSource persistedAllocation;HSBI_ReserveConsumptionKey persistedConsumption;bool snapshotPresent,historyUnchanged,sourceReused,duplicateConsumption,payloadConflict,unresolvedPending,brokerMoneyConfirmed,reconciliationConfirmed;string persistedDigest;};
HSBI_RuntimeDecisionResult HSBI_ValidateRestartedRuntimeState(const HSBI_RestartedRuntimeState &s)
{
 if(!s.snapshotPresent||s.persistedDigest=="")return HSBI_RuntimeReject(s.current,HSBI_DECISION_PERSISTENCE_REQUIRED,HSBI_RD_PERSISTENCE_REQUIRED,"HSBI-2D-RESTART");
 if(!HSBI_ValidateExecutionStateSnapshot(s.persisted,s.current.schemaVersion,s.persisted.snapshotVersion,s.current.accountLogin,s.current.symbol,s.current.magic,s.current.cycleId,s.expectedStateRevision))return HSBI_RuntimeReject(s.current,HSBI_DECISION_CONFLICT,HSBI_RD_DIGEST_MISMATCH,"HSBI-2D-RESTART-SNAPSHOT");
 if(s.current.planId!=s.expectedPlanId||s.current.stateRevision!=s.expectedStateRevision||s.current.eventId!=s.expectedEventId||s.current.actionId!=s.expectedActionId)return HSBI_RuntimeReject(s.current,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,"HSBI-2D-RESTART-ID");
 if(!s.historyUnchanged||s.sourceReused||s.payloadConflict)return HSBI_RuntimeReject(s.current,HSBI_DECISION_CONFLICT,HSBI_RD_DOUBLE_COUNT_BLOCKED,"HSBI-2D-RESTART-HISTORY");
 if(s.duplicateConsumption)return HSBI_RuntimeReject(s.current,HSBI_DECISION_NO_OP,HSBI_RD_OK,"HSBI-2D-RESTART-NOOP");
 if(s.unresolvedPending)return HSBI_RuntimeReject(s.current,HSBI_DECISION_PERSISTENCE_REQUIRED,HSBI_RD_PENDING_ACTION_CONFLICT,"HSBI-2D-RESTART-PENDING");
 if(!s.brokerMoneyConfirmed||!s.reconciliationConfirmed)return HSBI_RuntimeReject(s.current,HSBI_DECISION_RECONCILIATION_REQUIRED,HSBI_RD_RECONCILIATION_REQUIRED,"HSBI-2D-RESTART-PROOF");
 if(s.persistedResidual.identifier!=s.current.actualResidual.identifier||s.persistedResidual.ticket!=s.current.actualResidual.ticket||s.persistedResidual.actualVolume!=s.current.actualResidual.actualVolume||s.persistedResidual.role!=s.current.actualResidual.role||s.persistedResidual.direction!=s.current.actualResidual.direction)return HSBI_RuntimeReject(s.current,HSBI_DECISION_CONFLICT,HSBI_RD_POSITION_NOT_CONFIRMED,"HSBI-2D-RESTART-POS");
 if(HSBI_ReserveAllocationSourceDigest(s.persistedAllocation)!=HSBI_ReserveAllocationSourceDigest(s.current.allocationSource)||HSBI_ReserveConsumptionKeyDigest(s.persistedConsumption)!=HSBI_ReserveConsumptionKeyDigest(s.current.consumptionKey))return HSBI_RuntimeReject(s.current,HSBI_DECISION_CONFLICT,HSBI_RD_ALLOCATION_CONFLICT,"HSBI-2D-RESTART-ALLOC");
 return HSBI_ValidateRuntimeDecisionContext(s.current,s.current.accountLogin,s.current.symbol,s.current.magic,s.current.cycleId,s.current.planId,s.current.stateRevision);
}
#endif
