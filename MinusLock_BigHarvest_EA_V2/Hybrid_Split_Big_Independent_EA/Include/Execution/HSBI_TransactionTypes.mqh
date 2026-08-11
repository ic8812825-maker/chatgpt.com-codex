#ifndef HSBI_TRANSACTION_TYPES_MQH
#define HSBI_TRANSACTION_TYPES_MQH
enum HSBI_TransactionOutcome{HSBI_TX_PLACED,HSBI_TX_PARTIAL,HSBI_TX_COMPLETED,HSBI_TX_REJECTED,HSBI_TX_TIMEOUT,HSBI_TX_CONFLICT,HSBI_TX_UNKNOWN};
struct HSBI_TransactionMetadata{ulong actionId;ulong eventId;HSBI_TransactionOutcome outcome;double accumulatedVolume;double expectedVolume;bool actualPositionRead;bool ledgerApplied;};
struct HSBI_TransactionBarrierInput{HSBI_TransactionMetadata transaction;ulong expectedActionId;ulong lastAppliedEventId;ulong expectedStateRevision;ulong actualStateRevision;bool actualDealRead;bool ownershipConfirmed;bool reconciliationConflict;};
bool HSBI_IsCompletedOutcome(const HSBI_TransactionOutcome o){return o==HSBI_TX_COMPLETED;}
bool HSBI_IsRetryOfSameAction(const ulong originalActionId,const ulong retryActionId){return originalActionId>0&&originalActionId==retryActionId;}
bool HSBI_IsFreshEvent(const ulong lastEventId,const ulong eventId){return eventId>lastEventId;}
bool HSBI_TransactionBarrierPassed(const HSBI_TransactionBarrierInput &x)
{
   if(x.transaction.outcome!=HSBI_TX_COMPLETED)return false;
   if(x.expectedActionId==0||x.transaction.actionId!=x.expectedActionId)return false;
   if(!HSBI_IsFreshEvent(x.lastAppliedEventId,x.transaction.eventId))return false;
   if(!x.transaction.actualPositionRead||!x.actualDealRead||!x.ownershipConfirmed)return false;
   if(x.transaction.expectedVolume<=0.0||MathAbs(x.transaction.accumulatedVolume-x.transaction.expectedVolume)>0.0000001)return false;
   if(x.actualStateRevision!=x.expectedStateRevision)return false;
   if(x.reconciliationConflict)return false;
   return true;
}
bool HSBI_RetryAllowed(const ulong originalActionId,const ulong retryActionId,const HSBI_TransactionOutcome priorOutcome,const bool pendingOrReconciling)
{
   return pendingOrReconciling&&HSBI_IsRetryOfSameAction(originalActionId,retryActionId)&&priorOutcome!=HSBI_TX_COMPLETED;
}
#endif
