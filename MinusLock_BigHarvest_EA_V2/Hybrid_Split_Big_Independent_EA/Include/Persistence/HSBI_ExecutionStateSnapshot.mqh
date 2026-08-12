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
bool HSBI_ValidateExecutionStateSnapshot(const HSBI_ExecutionStateSnapshot &x,const int schema,const int version,const long account,const string symbol,const long magic,const ulong cycle,const ulong minimumRevision)
{
   if(x.schemaVersion!=schema||x.snapshotVersion!=version||x.accountLogin!=account||x.symbol!=symbol||x.magic!=magic||x.cycleId!=cycle||
      x.stateRevision<minimumRevision||!x.fresh||!x.journalChainValid||x.reconciliationConflict||x.failClosed||x.creationTimestamp<=0||x.updateTimestamp<x.creationTimestamp||
      x.snapshotDigest!=HSBI_ExecutionStateSnapshotDigest(x)||x.activeIntentCount>1||x.completedActionCount>1)return false;
   if(x.completedIntent.intentId>0&&x.pendingIntent.intentId>0)return false;
   return true;
}
HSBI_ExecutionRecoveryStatus HSBI_RecoverExecutionState(const HSBI_ExecutionStateSnapshot &x,const int schema,const int version,const long account,const string symbol,const long magic,const ulong cycle,const ulong revision)
{return HSBI_ValidateExecutionStateSnapshot(x,schema,version,account,symbol,magic,cycle,revision)?HSBI_RECOVERY_ACCEPTED:(x.snapshotDigest==""?HSBI_RECOVERY_UNAVAILABLE:HSBI_RECOVERY_REJECTED);}
#endif
