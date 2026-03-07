#property strict
#property script_show_inputs
#property description "ALE test launcher script/EA for environments with MQL runtime"

#include "RunAllTests.mqh"

// Example usage:
// 1) Attach script to chart in MT5.
// 2) It runs full ALE static/unit-style suite and prints summary.
// 3) Non-zero retcode indicates test failure.

int OnInit()
{
   CALTestSummary summary;
   const bool ok=RunAllALETests(summary);
   const int rc=(ok?INIT_SUCCEEDED:INIT_FAILED);
   PrintFormat("[ALE TEST RUNNER] done: total=%d passed=%d failed=%d rc=%d",summary.total,summary.passed,summary.failed,rc);
   return rc;
}

void OnDeinit(const int reason)
{
   (void)reason;
}

void OnTick(){}
