#ifndef HSBI_EXECUTION_INTENT_MQH
#define HSBI_EXECUTION_INTENT_MQH
#include "../Planning/HSBI_ControlPrices.mqh"
#include "../Core/HSBI_Identifiers.mqh"
enum HSBI_IntentStatus{HSBI_INTENT_CREATED,HSBI_INTENT_PREFLIGHT_PASSED,HSBI_INTENT_PERSISTED,HSBI_INTENT_DISPATCH_BLOCKED,HSBI_INTENT_OUTCOME_PENDING,HSBI_INTENT_OUTCOME_RECEIVED,HSBI_INTENT_RECONCILING,HSBI_INTENT_COMPLETED,HSBI_INTENT_REJECTED,HSBI_INTENT_EXPIRED,HSBI_INTENT_INVALIDATED,HSBI_INTENT_CONFLICT,HSBI_INTENT_SUPERSEDED};
struct HSBI_ExecutionIntent
{
   ulong intentId,planId,cycleId,stateRevision;string planDigest,candidateDigest,aggregateProofDigest;
   long accountLogin;string symbol;long magic;HSBI_Direction direction;HSBI_Role role;
   double requestedVolume,normalizedVolume,controlPrice;HSBI_PriceSide controlPriceSide;
   ulong marketSnapshotId,costSnapshotId,riskSnapshotId,marginSnapshotId;
   ulong sourcePositionIdentifier,sourceTicket,sourceDealId,sourceEventId,expectedActionId;
   string expectedTransition;datetime creationTimestamp,expiryTimestamp;HSBI_IntentStatus status;string digest;
};
string HSBI_ExecutionIntentDigest(const HSBI_ExecutionIntent &x)
{
   return HSBI_UlongToString(x.intentId)+"|"+HSBI_UlongToString(x.planId)+"|"+x.planDigest+"|"+x.candidateDigest+"|"+x.aggregateProofDigest+"|"+
      HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+LongToString(x.accountLogin)+"|"+x.symbol+"|"+LongToString(x.magic)+"|"+
      IntegerToString((int)x.direction)+"|"+IntegerToString((int)x.role)+"|"+DoubleToString(x.requestedVolume,8)+"|"+DoubleToString(x.normalizedVolume,8)+"|"+
      DoubleToString(x.controlPrice,12)+"|"+IntegerToString((int)x.controlPriceSide)+"|"+HSBI_UlongToString(x.marketSnapshotId)+"|"+
      HSBI_UlongToString(x.costSnapshotId)+"|"+HSBI_UlongToString(x.riskSnapshotId)+"|"+HSBI_UlongToString(x.marginSnapshotId)+"|"+
      HSBI_UlongToString(x.sourcePositionIdentifier)+"|"+HSBI_UlongToString(x.sourceTicket)+"|"+HSBI_UlongToString(x.sourceDealId)+"|"+
      HSBI_UlongToString(x.sourceEventId)+"|"+HSBI_UlongToString(x.expectedActionId)+"|"+x.expectedTransition+"|"+
      LongToString((long)x.creationTimestamp)+"|"+LongToString((long)x.expiryTimestamp)+"|"+IntegerToString((int)x.status);
}
bool HSBI_ValidateExecutionIntentDigest(const HSBI_ExecutionIntent &x){return x.digest!=""&&x.digest==HSBI_ExecutionIntentDigest(x);}
bool HSBI_ValidateExecutionIntentStructure(const HSBI_ExecutionIntent &x)
{
   return x.intentId>0&&x.planId>0&&x.cycleId>0&&x.stateRevision>0&&x.expectedActionId>0&&x.accountLogin>0&&x.symbol!=""&&x.magic!=0&&
      x.direction!=HSBI_DIRECTION_NONE&&x.role!=HSBI_ROLE_NONE&&x.requestedVolume>0.0&&x.normalizedVolume>0.0&&x.controlPrice>0.0&&
      x.marketSnapshotId>0&&x.costSnapshotId>0&&x.riskSnapshotId>0&&x.marginSnapshotId>0&&x.sourcePositionIdentifier>0&&x.sourceTicket>0&&
      x.sourceDealId>0&&x.sourceEventId>0&&x.creationTimestamp>0&&x.expiryTimestamp>x.creationTimestamp&&x.planDigest!=""&&x.candidateDigest!=""&&
      x.aggregateProofDigest!=""&&HSBI_ValidateExecutionIntentDigest(x);
}
string HSBI_IntentIdempotencyKey(const HSBI_ExecutionIntent &x){return HSBI_UlongToString(x.intentId)+"|"+HSBI_UlongToString(x.expectedActionId)+"|"+x.planDigest+"|"+HSBI_UlongToString(x.stateRevision);}
bool HSBI_IsSameIntentRetry(const HSBI_ExecutionIntent &a,const HSBI_ExecutionIntent &b){return HSBI_IntentIdempotencyKey(a)==HSBI_IntentIdempotencyKey(b)&&a.digest==b.digest;}
bool HSBI_IsIntentConflict(const HSBI_ExecutionIntent &a,const HSBI_ExecutionIntent &b){return HSBI_IntentIdempotencyKey(a)==HSBI_IntentIdempotencyKey(b)&&a.digest!=b.digest;}
#endif
