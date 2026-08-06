#ifndef HSBI_DECISION_RESULT_MQH
#define HSBI_DECISION_RESULT_MQH
#include "../Core/HSBI_ReasonCodes.mqh"
struct HSBI_DecisionResult{bool accepted;HSBI_Status status;HSBI_ReasonCode reason;ulong gateMask;string requirementId;string details;};
#endif