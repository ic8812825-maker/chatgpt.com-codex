#ifndef HSBI_RUNTIME_POLICY_MQH
#define HSBI_RUNTIME_POLICY_MQH
#include "HSBI_Enums.mqh"
// HSB.2C-R1-P1 is orchestration-only: dispatch is unconditionally disabled.
struct HSBI_RuntimePolicy
{
   HSBI_RuntimeMode mode;
   bool diagnosticsAllowed,staticCalculationAllowed,injectedFixtureAllowed;
   bool productionPreflightAllowed,persistenceAllowed,terminalCompletionAllowed,brokerDispatchAllowed;
   bool valid;
};
HSBI_RuntimePolicy HSBI_BuildRuntimePolicy(const HSBI_RuntimeMode mode)
{
   HSBI_RuntimePolicy p;ZeroMemory(p);p.mode=mode;
   if(mode==HSBI_RUNTIME_UNSPECIFIED)return p;
   if(mode==HSBI_RUNTIME_DISABLED){p.diagnosticsAllowed=true;p.valid=true;return p;}
   if(mode==HSBI_RUNTIME_UNIT_TEST){p.diagnosticsAllowed=true;p.staticCalculationAllowed=true;p.injectedFixtureAllowed=true;p.valid=true;return p;}
   if(mode==HSBI_RUNTIME_STRATEGY_TESTER_DRY_RUN||mode==HSBI_RUNTIME_DEMO_DRY_RUN){p.diagnosticsAllowed=true;p.staticCalculationAllowed=true;p.persistenceAllowed=true;p.valid=true;return p;}
   if(mode==HSBI_RUNTIME_SHADOW){p.diagnosticsAllowed=true;p.staticCalculationAllowed=true;p.productionPreflightAllowed=true;p.persistenceAllowed=true;p.valid=true;return p;}
   if(mode==HSBI_RUNTIME_PRODUCTION||mode==HSBI_RUNTIME_ADMIN_VERIFICATION){p.diagnosticsAllowed=true;p.staticCalculationAllowed=true;p.productionPreflightAllowed=true;p.persistenceAllowed=true;p.terminalCompletionAllowed=true;p.valid=true;return p;}
   return p; // legacy real modes are fail-closed at this stage
}
bool HSBI_IsInjectedProofAllowed(const HSBI_RuntimeMode mode){return HSBI_BuildRuntimePolicy(mode).injectedFixtureAllowed;}
bool HSBI_IsProductionPreflightAllowed(const HSBI_RuntimeMode mode){return HSBI_BuildRuntimePolicy(mode).productionPreflightAllowed;}
bool HSBI_IsBrokerDispatchAllowed(const HSBI_RuntimeMode mode){return false;}
bool HSBI_IsStaticCalculationAllowed(const HSBI_RuntimeMode mode){return HSBI_BuildRuntimePolicy(mode).staticCalculationAllowed;}
// Source zero is the typed RUNTIME_TERMINAL source; all fake/unverified sources are non-zero.
bool HSBI_IsCompletionSourceAllowed(const HSBI_RuntimeMode mode,const int source)
{return HSBI_BuildRuntimePolicy(mode).terminalCompletionAllowed&&source==0;}
#endif
