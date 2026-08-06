#ifndef HSBI_INITIAL_LOCK_TYPES_MQH
#define HSBI_INITIAL_LOCK_TYPES_MQH
#include "HSBI_ScenarioTypes.mqh"
struct HSBI_InitialLockContract{HSBI_ScenarioContract base;double startLot;ulong buyActionId;ulong sellActionId;ulong rollbackActionId;bool initialProfitExcluded;};
#endif