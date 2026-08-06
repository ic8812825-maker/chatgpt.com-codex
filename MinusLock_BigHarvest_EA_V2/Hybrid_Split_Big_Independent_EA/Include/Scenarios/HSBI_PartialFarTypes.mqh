#ifndef HSBI_PARTIAL_FAR_TYPES_MQH
#define HSBI_PARTIAL_FAR_TYPES_MQH
#include "HSBI_ScenarioTypes.mqh"
struct HSBI_PartialFarContract{HSBI_ScenarioContract base;double budgetReserved;double requestedCloseVolume;double actualClosedVolume;bool finalReserveReferenced;};
#endif