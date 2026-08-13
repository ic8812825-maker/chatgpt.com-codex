#ifndef HSBI_EXECUTION_JOURNAL_MQH
#define HSBI_EXECUTION_JOURNAL_MQH
#include "../Execution/HSBI_ExecutionIntent.mqh"
enum HSBI_IntentJournalEntryType{HSBI_JE_INTENT_CREATED,HSBI_JE_PREFLIGHT_RESULT,HSBI_JE_INTENT_PERSISTED,HSBI_JE_DISPATCH_NOT_PERFORMED,HSBI_JE_EXTERNAL_OUTCOME_RECEIVED,HSBI_JE_RECONCILIATION_STARTED,HSBI_JE_RECONCILIATION_PASSED,HSBI_JE_RECONCILIATION_REJECTED,HSBI_JE_INTENT_COMPLETED,HSBI_JE_INTENT_EXPIRED,HSBI_JE_INTENT_INVALIDATED,HSBI_JE_CONFLICT_DETECTED};
enum HSBI_JournalAppendStatus{HSBI_JOURNAL_APPENDED,HSBI_JOURNAL_NO_OP,HSBI_JOURNAL_CONFLICT,HSBI_JOURNAL_REJECTED};
struct HSBI_ExecutionJournalEntry
{
   ulong journalEntryId,intentId,planId,cycleId,stateRevision,actionId,eventId;HSBI_IntentJournalEntryType entryType;
   HSBI_Status entryStatus;datetime timestamp;long accountLogin;string symbol;long magic;
   string previousEntryDigest,currentEntryDigest,payloadDigest;
};
string HSBI_ExecutionJournalEntryDigest(const HSBI_ExecutionJournalEntry &x)
{return HSBI_UlongToString(x.journalEntryId)+"|"+HSBI_UlongToString(x.intentId)+"|"+HSBI_UlongToString(x.planId)+"|"+
   HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+HSBI_UlongToString(x.actionId)+"|"+
   HSBI_UlongToString(x.eventId)+"|"+IntegerToString((int)x.entryType)+"|"+IntegerToString((int)x.entryStatus)+"|"+
   LongToString((long)x.timestamp)+"|"+LongToString(x.accountLogin)+"|"+x.symbol+"|"+LongToString(x.magic)+"|"+
   x.previousEntryDigest+"|"+x.payloadDigest;}
bool HSBI_ValidateJournalEntry(const HSBI_ExecutionJournalEntry &x,const string expectedPrevious,const ulong cycleId,const ulong planId,const ulong revision)
{return x.journalEntryId>0&&x.intentId>0&&x.actionId>0&&x.timestamp>0&&x.cycleId==cycleId&&x.planId==planId&&x.stateRevision==revision&&
   x.previousEntryDigest==expectedPrevious&&x.payloadDigest!=""&&x.currentEntryDigest==HSBI_ExecutionJournalEntryDigest(x);}
bool HSBI_IsDuplicateJournalEntry(const HSBI_ExecutionJournalEntry &a,const HSBI_ExecutionJournalEntry &b)
{return a.journalEntryId==b.journalEntryId&&a.intentId==b.intentId&&a.actionId==b.actionId&&a.eventId==b.eventId&&a.currentEntryDigest==b.currentEntryDigest;}
bool HSBI_IsJournalEntryConflict(const HSBI_ExecutionJournalEntry &a,const HSBI_ExecutionJournalEntry &b)
{return a.journalEntryId==b.journalEntryId&&a.intentId==b.intentId&&a.actionId==b.actionId&&a.currentEntryDigest!=b.currentEntryDigest;}
HSBI_JournalAppendStatus HSBI_ClassifyJournalAppend(const HSBI_ExecutionJournalEntry &candidate,const HSBI_ExecutionJournalEntry &last,const string expectedPrevious,const ulong cycleId,const ulong planId,const ulong revision)
{
   if(HSBI_IsDuplicateJournalEntry(candidate,last))return HSBI_JOURNAL_NO_OP;
   if(HSBI_IsJournalEntryConflict(candidate,last))return HSBI_JOURNAL_CONFLICT;
   return HSBI_ValidateJournalEntry(candidate,expectedPrevious,cycleId,planId,revision)&&candidate.journalEntryId==last.journalEntryId+1&&candidate.eventId>last.eventId?HSBI_JOURNAL_APPENDED:HSBI_JOURNAL_REJECTED;
}
bool HSBI_ValidateJournalChain(const HSBI_ExecutionJournalEntry &entries[],const int count,const ulong cycleId,const ulong planId,const ulong revision)
{
   if(count<=0)return false;string previous="";bool reconciliationPassed=false,completed=false;
   for(int i=0;i<count;i++){
      HSBI_ExecutionJournalEntry e=entries[i];
      if(!HSBI_ValidateJournalEntry(e,previous,cycleId,planId,revision))return false;
      if(i>0&&(e.journalEntryId!=entries[i-1].journalEntryId+1||e.eventId<=entries[i-1].eventId))return false;
      if(e.entryType==HSBI_JE_RECONCILIATION_PASSED){if(completed)return false;reconciliationPassed=true;}
      if(e.entryType==HSBI_JE_INTENT_COMPLETED){if(!reconciliationPassed||completed)return false;completed=true;}
      if(completed&&(e.entryType==HSBI_JE_INTENT_CREATED||e.entryType==HSBI_JE_PREFLIGHT_RESULT||e.entryType==HSBI_JE_INTENT_PERSISTED||e.entryType==HSBI_JE_EXTERNAL_OUTCOME_RECEIVED))return false;
      previous=e.currentEntryDigest;
   }
   return true;
}
#endif
