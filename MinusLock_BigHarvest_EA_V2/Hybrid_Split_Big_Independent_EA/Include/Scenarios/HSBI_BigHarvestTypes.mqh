#ifndef HSBI_BIG_HARVEST_TYPES_MQH
#define HSBI_BIG_HARVEST_TYPES_MQH
#include "HSBI_ScenarioTypes.mqh"
struct HSBI_BigHarvestContract{HSBI_ScenarioContract base;ulong candidatePlanId;ulong controlSnapshotId;string sourceDealSetDigest;bool allocationAfterCompletion;};
#endif