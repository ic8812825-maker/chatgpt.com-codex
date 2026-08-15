#ifndef HSBI_CONTEXT_MQH
#define HSBI_CONTEXT_MQH
#include "HSBI_Identifiers.mqh"
#include "HSBI_Roles.mqh"
#include "HSBI_RuntimeMode.mqh"
#include "HSBI_ReasonCodes.mqh"
struct HSBI_RecoveryContext{long accountLogin;string symbol;long magic;ulong cycleId;HSBI_State currentState;HSBI_State previousState;ulong stateRevision;HSBI_RuntimeMode runtimeMode;HSBI_PositionDescriptor far;HSBI_PositionDescriptor bigCore;HSBI_PositionDescriptor bigTrend;HSBI_PositionDescriptor smallBase;HSBI_PositionDescriptor initialBuy;HSBI_PositionDescriptor initialSell;HSBI_PositionDescriptor newFarCandidate;ulong activePlanId;HSBI_Status candidatePlanStatus;ulong marketSnapshotId;ulong geometrySnapshotId;ulong pendingActionId;ulong pendingEventId;HSBI_Status expectedOutcome;HSBI_Status fillState;double realizedCycleNet;double finalReserve;double partialFarBudget;double transitionBudget;double carry;double residual;ulong ledgerRevision;ulong snapshotId;int schemaVersion;int moneyStateVersion;ulong journalRevision;int reconciliationStatus;HSBI_ReasonCode lastReason;string lastTransition;bool lastValidationPassed;};
void HSBI_InitializeContext(HSBI_RecoveryContext &c,const HSBI_RuntimeMode mode){ZeroMemory(c);c.runtimeMode=mode;c.currentState=HSBI_STATE_DISABLED;c.previousState=HSBI_STATE_DISABLED;c.schemaVersion=HSBI_SCHEMA_VERSION;c.moneyStateVersion=HSBI_MONEY_STATE_VERSION;c.lastReason=HSBI_REASON_OK;}
void HSBI_ResetContext(HSBI_RecoveryContext &c){HSBI_InitializeContext(c,HSBI_RUNTIME_DISABLED);}
bool HSBI_ContextPositionValid(const HSBI_PositionDescriptor &p)
{
   if(p.role==HSBI_ROLE_NONE)return p.ticket==0&&p.identifier==0&&p.actualVolume==0.0&&p.requestedVolume==0.0;
   if(!HSBI_IsKnownRole(p.role)||p.actualVolume<0.0||p.requestedVolume<0.0)return false;
   if(p.ticket>0&&p.identifier==0)return false;
   if(p.identity.role!=HSBI_ROLE_NONE&&p.identity.role!=p.role)return false;
   if(p.identity.positionIdentifier>0&&p.identity.positionIdentifier!=p.identifier)return false;
   return true;
}
bool HSBI_ContextRolesConflict(const HSBI_RecoveryContext &c)
{
   if(c.far.role!=HSBI_ROLE_NONE&&c.far.role!=HSBI_ROLE_FAR)return true;
   if(c.bigCore.role!=HSBI_ROLE_NONE&&c.bigCore.role!=HSBI_ROLE_BIG_CORE)return true;
   if(c.bigTrend.role!=HSBI_ROLE_NONE&&c.bigTrend.role!=HSBI_ROLE_BIG_TREND)return true;
   if(c.smallBase.role!=HSBI_ROLE_NONE&&c.smallBase.role!=HSBI_ROLE_SMALL_BASE)return true;
   return false;
}
bool HSBI_ContextPositionInScope(const HSBI_RecoveryContext &c,const HSBI_PositionDescriptor &p)
{
   if(p.role==HSBI_ROLE_NONE)return true;
   if(!HSBI_IsValidIdentity(p.identity))return false;
   return p.identity.accountLogin==c.accountLogin&&p.identity.symbol==c.symbol&&p.identity.magic==c.magic&&p.identity.cycleId==c.cycleId;
}
bool HSBI_ValidateContext(const HSBI_RecoveryContext &c)
{
   if(c.runtimeMode<HSBI_RUNTIME_DISABLED||c.runtimeMode>HSBI_RUNTIME_REAL_LIMITED)return false;
   if(!HSBI_IsRuntimeModeAllowedAtStage1(c.runtimeMode))return false;
   if(c.currentState<HSBI_STATE_DISABLED||c.currentState>HSBI_STATE_CYCLE_CLOSED)return false;
   if(c.previousState<HSBI_STATE_DISABLED||c.previousState>HSBI_STATE_CYCLE_CLOSED)return false;
   if(c.schemaVersion!=HSBI_SCHEMA_VERSION)return false;
   if(c.moneyStateVersion!=HSBI_MONEY_STATE_VERSION)return false;
   if(c.accountLogin<=0||c.symbol==""||c.magic==0||c.cycleId==0)return false;
   if(c.stateRevision==0&&c.previousState!=c.currentState)return false;
   if(c.stateRevision==0&&c.currentState!=HSBI_STATE_DISABLED&&c.currentState!=HSBI_STATE_IDLE)return false;
   if(c.reconciliationStatus<0||c.reconciliationStatus>5)return false;
   if(!HSBI_ContextPositionValid(c.far)||!HSBI_ContextPositionValid(c.bigCore)||!HSBI_ContextPositionValid(c.bigTrend)||!HSBI_ContextPositionValid(c.smallBase)||!HSBI_ContextPositionValid(c.initialBuy)||!HSBI_ContextPositionValid(c.initialSell)||!HSBI_ContextPositionValid(c.newFarCandidate))return false;
   if(!HSBI_ContextPositionInScope(c,c.far)||!HSBI_ContextPositionInScope(c,c.bigCore)||!HSBI_ContextPositionInScope(c,c.bigTrend)||!HSBI_ContextPositionInScope(c,c.smallBase)||!HSBI_ContextPositionInScope(c,c.initialBuy)||!HSBI_ContextPositionInScope(c,c.initialSell)||!HSBI_ContextPositionInScope(c,c.newFarCandidate))return false;
   if(HSBI_ContextRolesConflict(c))return false;
   int farCount=0;
   if(c.far.role==HSBI_ROLE_FAR)farCount++;
   if(c.bigCore.role==HSBI_ROLE_FAR)farCount++;
   if(c.bigTrend.role==HSBI_ROLE_FAR)farCount++;
   if(c.smallBase.role==HSBI_ROLE_FAR)farCount++;
   if(farCount>1)return false;
   if(c.currentState==HSBI_STATE_CYCLE_CLOSED&&c.pendingActionId!=0)return false;
   HSBI_RuntimePolicy policy=HSBI_BuildRuntimePolicy(c.runtimeMode);
   if(policy.brokerDispatchAllowed)return false;
   if(HSBI_TRADING_IMPLEMENTED||HSBI_REAL_TRADING_ALLOWED)return false;
   return true;
}
#endif
