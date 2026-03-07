#ifndef __RUNALLTESTS_MQH__
#define __RUNALLTESTS_MQH__

#include "TestALE.mqh"
#include "TestGeometry.mqh"
#include "TestRisk.mqh"

struct CALTestSummary
{
   int total;
   int passed;
   int failed;

   void Reset(){ total=0; passed=0; failed=0; }
};

bool RunTestCase(const string name,const bool ok,CALTestSummary &sum)
{
   sum.total++;
   if(ok)
   {
      sum.passed++;
      PrintFormat("[ALE TEST] PASS: %s",name);
      return true;
   }

   sum.failed++;
   PrintFormat("[ALE TEST] FAIL: %s",name);
   return false;
}

bool RunAllALETests(CALTestSummary &summary)
{
   summary.Reset();

   bool all_ok=true;
   all_ok = RunTestCase("TestALE_DualFlowIntegration",TestALE_DualFlowIntegration(),summary) && all_ok;
   all_ok = RunTestCase("TestALE_DeterministicReplayHarness",TestALE_DeterministicReplayHarness(),summary) && all_ok;
   all_ok = RunTestCase("TestALE_ReplayScenario_Uptrend",TestALE_ReplayScenario_Uptrend(),summary) && all_ok;
   all_ok = RunTestCase("TestALE_ReplayScenario_Oscillation",TestALE_ReplayScenario_Oscillation(),summary) && all_ok;
   all_ok = RunTestCase("TestALE_ReplayScenario_Crash",TestALE_ReplayScenario_Crash(),summary) && all_ok;
   all_ok = RunTestCase("TestALE_ReplayScenario_VShape",TestALE_ReplayScenario_VShape(),summary) && all_ok;
   all_ok = RunTestCase("TestALE_StateTraceMatcher",TestALE_StateTraceMatcher(),summary) && all_ok;
   all_ok = RunTestCase("TestALE_CSVExports",TestALE_CSVExports(),summary) && all_ok;
   all_ok = RunTestCase("TestALE_BuyFlowIsolation",TestALE_BuyFlowIsolation(),summary) && all_ok;
   all_ok = RunTestCase("TestALE_SellFlowIsolation",TestALE_SellFlowIsolation(),summary) && all_ok;

   all_ok = RunTestCase("TestGeometry_BuySellGrids",TestGeometry_BuySellGrids(),summary) && all_ok;
   all_ok = RunTestCase("TestGeometry_LogGridMonotonicity",TestGeometry_LogGridMonotonicity(),summary) && all_ok;

   all_ok = RunTestCase("TestRisk_WorstDDMargin",TestRisk_WorstDDMargin(),summary) && all_ok;
   all_ok = RunTestCase("TestRisk_ConfigThresholdsAffectSAFE",TestRisk_ConfigThresholdsAffectSAFE(),summary) && all_ok;
   all_ok = RunTestCase("TestRisk_ZeroEquityFinite",TestRisk_ZeroEquityFinite(),summary) && all_ok;
   all_ok = RunTestCase("TestRisk_GlobalSafeThresholdBoundaries",TestRisk_GlobalSafeThresholdBoundaries(),summary) && all_ok;

   PrintFormat("[ALE TEST] total=%d passed=%d failed=%d",summary.total,summary.passed,summary.failed);
   return all_ok;
}

#endif
