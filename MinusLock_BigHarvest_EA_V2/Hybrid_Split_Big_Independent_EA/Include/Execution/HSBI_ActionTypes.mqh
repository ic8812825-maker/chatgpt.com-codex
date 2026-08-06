#ifndef HSBI_ACTION_TYPES_MQH
#define HSBI_ACTION_TYPES_MQH
#include "../Core/HSBI_Enums.mqh"
struct HSBI_ActionRecord{ulong actionId;ulong parentActionId;ulong planId;ulong cycleId;ulong stateRevision;HSBI_ActionType actionType;HSBI_Role expectedRole;ulong expectedTicket;ulong expectedIdentifier;double expectedVolume;HSBI_Status status;datetime createdAt;int retryCount;datetime timeoutAt;};
bool HSBI_ValidateActionRecord(const HSBI_ActionRecord &a){return a.actionId>0&&a.planId>0&&a.cycleId>0&&a.stateRevision>0&&a.actionType!=HSBI_ACTION_NONE&&a.expectedVolume>=0.0;}
#endif