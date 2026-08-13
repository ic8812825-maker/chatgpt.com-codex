#ifndef HSBI_JOURNAL_TYPES_MQH
#define HSBI_JOURNAL_TYPES_MQH
#include "../Execution/HSBI_ActionTypes.mqh"
#include "../Execution/HSBI_EventTypes.mqh"
struct HSBI_JournalRecord{ulong revision;ulong cycleId;ulong stateRevision;HSBI_ActionRecord action;HSBI_EventRecord event;datetime timestamp;string previousDigest;string recordDigest;bool committed;};
bool HSBI_ValidateJournalRecord(const HSBI_JournalRecord &r){return r.revision>0&&r.cycleId>0&&r.stateRevision>0&&r.timestamp>0&&r.recordDigest!="";}
string HSBI_SerializeJournalIds(const HSBI_JournalRecord &r){return HSBI_UlongToString(r.revision)+"|"+HSBI_UlongToString(r.cycleId)+"|"+HSBI_UlongToString(r.stateRevision)+"|"+HSBI_SerializeActionIds(r.action)+"|"+HSBI_SerializeEventIds(r.event);}
#endif
