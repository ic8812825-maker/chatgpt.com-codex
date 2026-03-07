#ifndef __ALE_RUNALLTESTS_MQH__
#define __ALE_RUNALLTESTS_MQH__

#include "..\\..\\tests\\TestALE.mqh"
#include "..\\..\\tests\\TestGeometry.mqh"
#include "..\\..\\tests\\TestRisk.mqh"

struct CALE2ETestSummary
{
   int total;
   int passed;
   int failed;

   void Reset(){ total=0; passed=0; failed=0; }
};

bool RunALETest(const string name,const bool ok,CALE2ETestSummary &sum)
{
   sum.total++;
   if(ok)
   {
      sum.passed++;
      PrintFormat("[ALE][RUNNER] PASS: %s",name);
      return true;
   }

   sum.failed++;
   PrintFormat("[ALE][RUNNER] FAIL: %s",name);
   return false;
}

// Unified runner requested by technical assignment.
// Example:
//   CALE2ETestSummary s;
//   const bool ok=RunAllALEBehaviorTests(s);
bool RunAllALEBehaviorTests(CALE2ETestSummary &summary)
{
   summary.Reset();
   bool all_ok=true;

   // ALE core tests (dual-flow + deterministic replays)
   all_ok = RunALETest("TestALE_DualFlowIntegration",TestALE_DualFlowIntegration(),summary) && all_ok;
   all_ok = RunALETest("TestALE_DeterministicReplayHarness",TestALE_DeterministicReplayHarness(),summary) && all_ok;
   all_ok = RunALETest("TestALE_ReplayScenario_Uptrend",TestALE_ReplayScenario_Uptrend(),summary) && all_ok;
   all_ok = RunALETest("TestALE_ReplayScenario_Oscillation",TestALE_ReplayScenario_Oscillation(),summary) && all_ok;
   all_ok = RunALETest("TestALE_ReplayScenario_Crash",TestALE_ReplayScenario_Crash(),summary) && all_ok;
   all_ok = RunALETest("TestALE_ReplayScenario_VShape",TestALE_ReplayScenario_VShape(),summary) && all_ok;
   all_ok = RunALETest("TestALE_StateTraceMatcher",TestALE_StateTraceMatcher(),summary) && all_ok;
   all_ok = RunALETest("TestALE_CSVExports",TestALE_CSVExports(),summary) && all_ok;

   // Explicit BUY/SELL flow separation checks
   all_ok = RunALETest("TestALE_BuyFlowIsolation",TestALE_BuyFlowIsolation(),summary) && all_ok;
   all_ok = RunALETest("TestALE_SellFlowIsolation",TestALE_SellFlowIsolation(),summary) && all_ok;

   // Geometry tests
   all_ok = RunALETest("TestGeometry_BuySellGrids",TestGeometry_BuySellGrids(),summary) && all_ok;
   all_ok = RunALETest("TestGeometry_LogGridMonotonicity",TestGeometry_LogGridMonotonicity(),summary) && all_ok;

   // Risk tests
   all_ok = RunALETest("TestRisk_WorstDDMargin",TestRisk_WorstDDMargin(),summary) && all_ok;
   all_ok = RunALETest("TestRisk_ConfigThresholdsAffectSAFE",TestRisk_ConfigThresholdsAffectSAFE(),summary) && all_ok;
   all_ok = RunALETest("TestRisk_ZeroEquityFinite",TestRisk_ZeroEquityFinite(),summary) && all_ok;
   all_ok = RunALETest("TestRisk_GlobalSafeThresholdBoundaries",TestRisk_GlobalSafeThresholdBoundaries(),summary) && all_ok;

   PrintFormat("[ALE][RUNNER] total=%d passed=%d failed=%d",summary.total,summary.passed,summary.failed);
   return all_ok;
}

#endif
