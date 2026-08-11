#ifndef HSBI_SNAPSHOT_TYPES_MQH
#define HSBI_SNAPSHOT_TYPES_MQH
#include "../Core/HSBI_Context.mqh"
#include "../Planning/HSBI_CandidatePlan.mqh"
#include "../Execution/HSBI_ActionTypes.mqh"
#include "../Money/HSBI_MoneyState.mqh"
struct HSBI_SnapshotRecord{int schemaVersion;int moneyStateVersion;ulong cycleId;HSBI_State state;ulong stateRevision;HSBI_RuntimeMode runtimeMode;string candidatePlanDigest;HSBI_ActionRecord pendingAction;string rolesDigest;string ticketsDigest;string identifiersDigest;string volumesDigest;HSBI_MoneyState moneyState;string economicLedgerDigest;string allocationLedgerDigest;int reconciliationStatus;datetime timestamp;string checksum;};
bool HSBI_ValidateSnapshotSchema(const HSBI_SnapshotRecord &s){return s.schemaVersion==HSBI_SNAPSHOT_SCHEMA_VERSION&&s.moneyStateVersion==HSBI_MONEY_STATE_VERSION&&s.stateRevision>0&&s.timestamp>0;}
ulong HSBI_TestDigest(const HSBI_SnapshotRecord &s){string v=IntegerToString(s.schemaVersion)+"|"+HSBI_UlongToString(s.cycleId)+"|"+HSBI_UlongToString(s.stateRevision)+"|"+s.candidatePlanDigest;ulong h=2166136261;for(int i=0;i<StringLen(v);i++){h^=(uchar)StringGetCharacter(v,i);h*=16777619;}return h;}
#endif
