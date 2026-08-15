#property strict
#property version "1.00"
#property description "Hybrid Split Big independent non-trading skeleton"

#include "Include/Core/HSBI_Version.mqh"
#include "Include/Core/HSBI_Enums.mqh"
#include "Include/Core/HSBI_Types.mqh"
#include "Include/Core/HSBI_ReasonCodes.mqh"
#include "Include/Core/HSBI_RuntimePolicy.mqh"
#include "Include/Core/HSBI_RuntimeMode.mqh"
#include "Include/Core/HSBI_Context.mqh"
#include "Include/Core/HSBI_Invariants.mqh"
#include "Include/Execution/HSBI_NoTradeExecution.mqh"
#include "Include/Diagnostics/HSBI_Logger.mqh"
#include "Include/Diagnostics/HSBI_Diagnostics.mqh"

HSBI_RecoveryContext g_hsbi_context;

int OnInit()
{
   HSBI_InitializeContext(g_hsbi_context,HSBI_RUNTIME_DISABLED);
   HSBI_Log("HSBI-GEN-033",HSBI_REASON_OK,"NON_TRADING_SKELETON initialized");
   EventSetTimer(1);
   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   HSBI_Log("HSBI-GEN-033",HSBI_REASON_OK,"NON_TRADING_SKELETON deinitialized");
}

void OnTick()
{
   HSBI_NoTradeResult blocked=HSBI_SubmitActionStub();
   g_hsbi_context.lastReason=blocked.reason;
}

void OnTimer()
{
   HSBI_UpdateDiagnosticSnapshot(g_hsbi_context);
}
