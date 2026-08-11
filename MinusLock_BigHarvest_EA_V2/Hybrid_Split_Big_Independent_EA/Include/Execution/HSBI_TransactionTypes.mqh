#ifndef HSBI_TRANSACTION_TYPES_MQH
#define HSBI_TRANSACTION_TYPES_MQH
enum HSBI_TransactionOutcome{HSBI_TX_PLACED,HSBI_TX_PARTIAL,HSBI_TX_COMPLETED,HSBI_TX_REJECTED,HSBI_TX_TIMEOUT,HSBI_TX_CONFLICT,HSBI_TX_UNKNOWN};
struct HSBI_TransactionMetadata{ulong actionId;ulong eventId;HSBI_TransactionOutcome outcome;double accumulatedVolume;double expectedVolume;bool actualPositionRead;bool ledgerApplied;};
bool HSBI_IsCompletedOutcome(const HSBI_TransactionOutcome o){return o==HSBI_TX_COMPLETED;}
bool HSBI_TransactionPermitsStateTransition(const HSBI_TransactionMetadata &m,const ulong expectedActionId)
{
   return expectedActionId>0&&m.actionId==expectedActionId&&m.eventId>0&&m.outcome==HSBI_TX_COMPLETED&&m.actualPositionRead&&!m.ledgerApplied;
}
bool HSBI_IsRetryOfSameAction(const ulong originalActionId,const ulong retryActionId){return originalActionId>0&&originalActionId==retryActionId;}
bool HSBI_IsFreshEvent(const ulong lastEventId,const ulong eventId){return eventId>lastEventId;}
#endif
