#ifndef HSBI_RUNTIME_MODE_MQH
#define HSBI_RUNTIME_MODE_MQH
#include "HSBI_RuntimePolicy.mqh"
// Stage-1 compatibility predicate; all policy construction is canonical.
bool HSBI_IsRuntimeModeAllowedAtStage1(const HSBI_RuntimeMode mode)
{return mode==HSBI_RUNTIME_DISABLED||mode==HSBI_RUNTIME_UNIT_TEST||mode==HSBI_RUNTIME_STRATEGY_TESTER_DRY_RUN;}
#endif
