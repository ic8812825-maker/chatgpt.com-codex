#ifndef HSBI_RUNTIME_MODE_MQH
#define HSBI_RUNTIME_MODE_MQH
#include "HSBI_Enums.mqh"
#include "HSBI_ReasonCodes.mqh"
struct HSBI_RuntimePolicy{HSBI_RuntimeMode mode;bool calculationsAllowed;bool stateTransitionsAllowed;bool tradeIntentsAllowed;bool brokerRequestsAllowed;bool realAccountAllowed;bool persistenceWritesAllowed;bool diagnosticsAllowed;};
HSBI_RuntimePolicy HSBI_BuildRuntimePolicy(const HSBI_RuntimeMode mode){HSBI_RuntimePolicy p;p.mode=mode;p.calculationsAllowed=(mode==HSBI_RUNTIME_UNIT_TEST||mode==HSBI_RUNTIME_STRATEGY_TESTER_DRY_RUN);p.stateTransitionsAllowed=p.calculationsAllowed;p.tradeIntentsAllowed=false;p.brokerRequestsAllowed=false;p.realAccountAllowed=false;p.persistenceWritesAllowed=false;p.diagnosticsAllowed=true;return p;}
bool HSBI_IsRuntimeModeAllowedAtStage1(const HSBI_RuntimeMode mode){return mode==HSBI_RUNTIME_DISABLED||mode==HSBI_RUNTIME_UNIT_TEST||mode==HSBI_RUNTIME_STRATEGY_TESTER_DRY_RUN;}
#endif