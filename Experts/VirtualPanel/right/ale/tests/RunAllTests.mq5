#property strict
#property script_show_inputs
#property description "ALE unified behavioral regression runner"

#include "RunAllTests.mqh"
#include "..\\core\\CALExportHelper.mqh"

int OnInit()
{
   CALE2ETestSummary summary;
   const bool ok=RunAllALEBehaviorTests(summary);

   CALExportHelper exporter;
   exporter.ExportJUnitXML("ale_runner_junit.xml",summary.total,summary.failed);

   const int rc=(ok?INIT_SUCCEEDED:INIT_FAILED);
   PrintFormat("[ALE][RUNNER] done total=%d passed=%d failed=%d rc=%d",summary.total,summary.passed,summary.failed,rc);
   return rc;
}

void OnDeinit(const int reason)
{
   (void)reason;
}

void OnTick(){}
