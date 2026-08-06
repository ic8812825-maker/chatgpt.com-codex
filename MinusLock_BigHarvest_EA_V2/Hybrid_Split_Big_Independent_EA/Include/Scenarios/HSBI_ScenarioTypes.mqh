#ifndef HSBI_SCENARIO_TYPES_MQH
#define HSBI_SCENARIO_TYPES_MQH
#include "../Core/HSBI_Enums.mqh"
#include "../Core/HSBI_ReasonCodes.mqh"
struct HSBI_ScenarioContract{string inputDigest;ulong planId;string preconditions;string expectedActions;string expectedPostconditions;HSBI_ReasonCode failureReason;bool reconciliationRequired;HSBI_Status status;};
#endif