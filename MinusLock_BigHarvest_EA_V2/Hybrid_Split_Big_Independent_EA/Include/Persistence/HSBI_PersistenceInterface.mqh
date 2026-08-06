#ifndef HSBI_PERSISTENCE_INTERFACE_MQH
#define HSBI_PERSISTENCE_INTERFACE_MQH
#include "HSBI_SnapshotTypes.mqh"
#include "HSBI_JournalTypes.mqh"
#define HSBI_PRODUCTION_SHA256_IMPLEMENTED false
struct HSBI_PersistenceResult{bool success;HSBI_ReasonCode reason;ulong revision;string digest;};
HSBI_PersistenceResult HSBI_PersistSnapshotStub(const HSBI_SnapshotRecord &s){HSBI_PersistenceResult r;r.success=false;r.reason=HSBI_REASON_PERSISTENCE_NOT_IMPLEMENTED;r.revision=s.stateRevision;r.digest="";return r;}
#endif