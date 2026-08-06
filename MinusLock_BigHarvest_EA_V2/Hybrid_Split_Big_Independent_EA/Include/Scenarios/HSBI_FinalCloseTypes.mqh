#ifndef HSBI_FINAL_CLOSE_TYPES_MQH
#define HSBI_FINAL_CLOSE_TYPES_MQH
#include "HSBI_ScenarioTypes.mqh"
struct HSBI_FinalCloseContract{HSBI_ScenarioContract base;double recoveryPLCloseNow;double threshold;double allowedCoverage;bool pendingActionsAbsent;bool positionsReconciled;};
#endif