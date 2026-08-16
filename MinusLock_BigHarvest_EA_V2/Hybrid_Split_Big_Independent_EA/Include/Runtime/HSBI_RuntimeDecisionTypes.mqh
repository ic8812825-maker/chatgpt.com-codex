#ifndef HSBI_RUNTIME_DECISION_TYPES_MQH
#define HSBI_RUNTIME_DECISION_TYPES_MQH
#include "../Core/HSBI_Context.mqh"
#include "../Core/HSBI_RuntimePolicy.mqh"
#include "../Planning/HSBI_FutureSmallProofAggregator.mqh"
#include "../Planning/HSBI_NewFarCandidate.mqh"
#include "../Money/HSBI_ReserveCatchUpEvaluator.mqh"
#include "../Persistence/HSBI_ExecutionStateSnapshot.mqh"
enum HSBI_RuntimeDecisionStatus{HSBI_DECISION_VALID,HSBI_DECISION_REJECTED,HSBI_DECISION_UNAVAILABLE,HSBI_DECISION_STALE,HSBI_DECISION_CONFLICT,HSBI_DECISION_RECONCILIATION_REQUIRED,HSBI_DECISION_PERSISTENCE_REQUIRED,HSBI_DECISION_NO_OP};
enum HSBI_RuntimeDecisionReason{HSBI_RD_OK,HSBI_RD_CONTEXT_INVALID,HSBI_RD_IDENTITY_MISMATCH,HSBI_RD_STATE_REVISION_MISMATCH,HSBI_RD_SCHEMA_VERSION_MISMATCH,HSBI_RD_MONEY_STATE_VERSION_MISMATCH,HSBI_RD_STALE_SNAPSHOT,HSBI_RD_RECONCILIATION_REQUIRED,HSBI_RD_RECONCILIATION_CONFLICT,HSBI_RD_PERSISTENCE_REQUIRED,HSBI_RD_PENDING_ACTION_CONFLICT,HSBI_RD_EVENT_NOT_FRESH,HSBI_RD_ACTION_ID_MISMATCH,HSBI_RD_POSITION_NOT_CONFIRMED,HSBI_RD_ACTUAL_RESIDUAL_REQUIRED,HSBI_RD_FUTURE_SMALL_INCOMPLETE,HSBI_RD_NEW_FAR_INVALID,HSBI_RD_CATCH_UP_INVALID,HSBI_RD_RISK_UNAVAILABLE,HSBI_RD_MONEY_UNAVAILABLE,HSBI_RD_ALLOCATION_CONFLICT,HSBI_RD_DOUBLE_COUNT_BLOCKED,HSBI_RD_CONSUMPTION_CONFLICT,HSBI_RD_DIGEST_MISMATCH};
struct HSBI_RuntimeDecisionContext{
 long accountLogin;string symbol;long magic;ulong cycleId,planId,stateRevision;int schemaVersion,moneyStateVersion;HSBI_RuntimeMode runtimeMode;HSBI_State state;int reconciliationStatus;ulong eventId,actionId;
 HSBI_PositionDescriptor far,bigCore,bigTrend,smallBase,actualResidual;HSBI_FutureSmallAggregateProof aggregate;HSBI_NewFarCandidate candidate;HSBI_ReserveCatchUpResult catchUp;HSBI_AllocationPolicySnapshot allocationPolicy;HSBI_ReserveAllocationSource allocationSource;HSBI_ReserveConsumptionKey consumptionKey;HSBI_ExecutionStateSnapshot persistence;
 HSBI_MoneyProofIdentity moneyIdentity,riskIdentity,marginIdentity;bool immutable,marketFresh,costFresh,reconciliationConfirmed,reconciliationConflict,positionActuallyRead,ownershipConfirmed,residualActual,persistencePrepared,moneyRuntimeConfirmed,riskRuntimeConfirmed,marginRuntimeConfirmed,consumptionConflict,completedAction;string inputDigest;
};
struct HSBI_RuntimeDecisionResult{HSBI_RuntimeDecisionStatus status;HSBI_RuntimeDecisionReason reason;ulong planId,cycleId,stateRevision;string inputDigest,outputDigest;HSBI_NewFarCandidate selectedCandidate;HSBI_FutureSmallAggregateProof selectedAggregate;HSBI_ReserveCatchUpResult catchUp;HSBI_ReserveAllocationSource allocation;HSBI_State requiredNextState;ulong pendingActionId;string requirementId;bool valid;};
string HSBI_RuntimeDecisionContextDigest(const HSBI_RuntimeDecisionContext &x){return LongToString(x.accountLogin)+"|"+x.symbol+"|"+LongToString(x.magic)+"|"+HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.planId)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+IntegerToString(x.schemaVersion)+"|"+IntegerToString(x.moneyStateVersion)+"|"+IntegerToString((int)x.runtimeMode)+"|"+IntegerToString((int)x.state)+"|"+HSBI_UlongToString(x.eventId)+"|"+HSBI_UlongToString(x.actionId)+"|"+HSBI_UlongToString(x.actualResidual.identifier)+"|"+HSBI_UlongToString(x.actualResidual.ticket)+"|"+DoubleToString(x.actualResidual.actualVolume,8)+"|"+x.aggregate.aggregateDigest+"|"+x.candidate.candidateDigest+"|"+HSBI_ReserveCatchUpDigest(x.catchUp)+"|"+HSBI_ReserveAllocationSourceDigest(x.allocationSource)+"|"+HSBI_ReserveConsumptionKeyDigest(x.consumptionKey)+"|"+x.persistence.snapshotDigest;}
#endif
