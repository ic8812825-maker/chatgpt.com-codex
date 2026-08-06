#ifndef HSBI_CONTEXT_MQH
#define HSBI_CONTEXT_MQH
#include "HSBI_Identifiers.mqh"
#include "HSBI_Roles.mqh"
#include "HSBI_RuntimeMode.mqh"
#include "HSBI_ReasonCodes.mqh"
struct HSBI_RecoveryContext{long accountLogin;string symbol;long magic;ulong cycleId;HSBI_State currentState;HSBI_State previousState;ulong stateRevision;HSBI_RuntimeMode runtimeMode;HSBI_PositionDescriptor far;HSBI_PositionDescriptor bigCore;HSBI_PositionDescriptor bigTrend;HSBI_PositionDescriptor smallBase;HSBI_PositionDescriptor initialBuy;HSBI_PositionDescriptor initialSell;HSBI_PositionDescriptor newFarCandidate;ulong activePlanId;HSBI_Status candidatePlanStatus;ulong marketSnapshotId;ulong geometrySnapshotId;ulong pendingActionId;ulong pendingEventId;HSBI_Status expectedOutcome;HSBI_Status fillState;double realizedCycleNet;double finalReserve;double partialFarBudget;double transitionBudget;double carry;double residual;ulong ledgerRevision;ulong snapshotId;int schemaVersion;ulong journalRevision;int reconciliationStatus;HSBI_ReasonCode lastReason;string lastTransition;bool lastValidationPassed;};
void HSBI_InitializeContext(HSBI_RecoveryContext &c,const HSBI_RuntimeMode mode){ZeroMemory(c);c.runtimeMode=mode;c.currentState=HSBI_STATE_DISABLED;c.previousState=HSBI_STATE_DISABLED;c.schemaVersion=HSBI_SCHEMA_VERSION;c.lastReason=HSBI_REASON_OK;}
void HSBI_ResetContext(HSBI_RecoveryContext &c){HSBI_InitializeContext(c,HSBI_RUNTIME_DISABLED);}
bool HSBI_ValidateContext(const HSBI_RecoveryContext &c){return c.stateRevision>=0 && HSBI_IsRuntimeModeAllowedAtStage1(c.runtimeMode);}
#endif