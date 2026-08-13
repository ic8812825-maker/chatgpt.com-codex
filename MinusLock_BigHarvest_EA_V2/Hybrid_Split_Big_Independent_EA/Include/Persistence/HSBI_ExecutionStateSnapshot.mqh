#ifndef HSBI_EXECUTION_STATE_SNAPSHOT_MQH
#define HSBI_EXECUTION_STATE_SNAPSHOT_MQH
#include "HSBI_ExecutionJournal.mqh"
enum HSBI_ExecutionRecoveryStatus{HSBI_RECOVERY_ACCEPTED,HSBI_RECOVERY_REJECTED,HSBI_RECOVERY_UNAVAILABLE};
struct HSBI_ExecutionStateSnapshot
{
   int schemaVersion,snapshotVersion;long accountLogin;string symbol;long magic;ulong cycleId,stateRevision;
   ulong lastConfirmedActionId,lastConfirmedEventId;string lastJournalDigest;HSBI_ExecutionIntent pendingIntent,completedIntent,invalidatedIntent;
   int activeIntentCount,completedActionCount;bool reconciliationConflict,failClosed,journalChainValid,fresh;
   datetime creationTimestamp,updateTimestamp;string snapshotDigest;
};
string HSBI_ExecutionStateSnapshotDigest(const HSBI_ExecutionStateSnapshot &x)
{return IntegerToString(x.schemaVersion)+"|"+IntegerToString(x.snapshotVersion)+"|"+LongToString(x.accountLogin)+"|"+x.symbol+"|"+
   LongToString(x.magic)+"|"+HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+
   HSBI_UlongToString(x.lastConfirmedActionId)+"|"+HSBI_UlongToString(x.lastConfirmedEventId)+"|"+x.lastJournalDigest+"|"+
   x.pendingIntent.digest+"|"+x.completedIntent.digest+"|"+x.invalidatedIntent.digest+"|"+IntegerToString(x.activeIntentCount)+"|"+
   IntegerToString(x.completedActionCount)+"|"+IntegerToString((int)x.reconciliationConflict)+"|"+IntegerToString((int)x.failClosed)+"|"+
   IntegerToString((int)x.journalChainValid)+"|"+IntegerToString((int)x.fresh)+"|"+LongToString((long)x.creationTimestamp)+"|"+LongToString((long)x.updateTimestamp);}
bool HSBI_ValidateNestedExecutionIntent(const HSBI_ExecutionIntent &i,const HSBI_ExecutionStateSnapshot &x)
{
   if(i.intentId==0)return true;
   return HSBI_ValidateExecutionIntentStructure(i)&&i.accountLogin==x.accountLogin&&i.symbol==x.symbol&&i.magic==x.magic&&
      i.cycleId==x.cycleId&&i.stateRevision==x.stateRevision&&i.planId>0&&i.expectedActionId>0;
}
bool HSBI_IsActiveIntentStatus(const HSBI_IntentStatus s)
{return s==HSBI_INTENT_CREATED||s==HSBI_INTENT_PREFLIGHT_PASSED||s==HSBI_INTENT_PERSISTED||s==HSBI_INTENT_DISPATCH_BLOCKED||s==HSBI_INTENT_OUTCOME_PENDING||s==HSBI_INTENT_OUTCOME_RECEIVED||s==HSBI_INTENT_RECONCILING;}
bool HSBI_ValidateExecutionStateSnapshot(const HSBI_ExecutionStateSnapshot &x,const int schema,const int version,const long account,const string symbol,const long magic,const ulong cycle,const ulong minimumRevision)
{
   if(x.schemaVersion!=schema||x.snapshotVersion!=version||x.accountLogin!=account||x.symbol!=symbol||x.magic!=magic||x.cycleId!=cycle||
      x.stateRevision<minimumRevision||!x.fresh||!x.journalChainValid||x.reconciliationConflict||x.failClosed||x.creationTimestamp<=0||x.updateTimestamp<x.creationTimestamp||
      x.snapshotDigest!=HSBI_ExecutionStateSnapshotDigest(x)||x.activeIntentCount<0||x.activeIntentCount>1||x.completedActionCount<0||x.completedActionCount>1)return false;
   if(!HSBI_ValidateNestedExecutionIntent(x.pendingIntent,x)||!HSBI_ValidateNestedExecutionIntent(x.completedIntent,x)||!HSBI_ValidateNestedExecutionIntent(x.invalidatedIntent,x))return false;
   bool pendingExists=x.pendingIntent.intentId>0,completedExists=x.completedIntent.intentId>0,invalidatedExists=x.invalidatedIntent.intentId>0;
   if((x.activeIntentCount==1)!=pendingExists||pendingExists&&!HSBI_IsActiveIntentStatus(x.pendingIntent.status))return false;
   if(completedExists&&x.completedIntent.status!=HSBI_INTENT_COMPLETED)return false;
   if(invalidatedExists&&x.invalidatedIntent.status!=HSBI_INTENT_INVALIDATED&&x.invalidatedIntent.status!=HSBI_INTENT_CONFLICT&&x.invalidatedIntent.status!=HSBI_INTENT_SUPERSEDED)return false;
   if(completedExists&&pendingExists)return false;
   if(completedExists&&pendingExists&&x.completedIntent.expectedActionId==x.pendingIntent.expectedActionId)return false;
   if(invalidatedExists&&x.activeIntentCount>0&&x.invalidatedIntent.expectedActionId==x.pendingIntent.expectedActionId)return false;
   return true;
}
HSBI_ExecutionRecoveryStatus HSBI_RecoverExecutionState(const HSBI_ExecutionStateSnapshot &x,const int schema,const int version,const long account,const string symbol,const long magic,const ulong cycle,const ulong revision)
{return HSBI_ValidateExecutionStateSnapshot(x,schema,version,account,symbol,magic,cycle,revision)?HSBI_RECOVERY_ACCEPTED:(x.snapshotDigest==""?HSBI_RECOVERY_UNAVAILABLE:HSBI_RECOVERY_REJECTED);}
#endif
