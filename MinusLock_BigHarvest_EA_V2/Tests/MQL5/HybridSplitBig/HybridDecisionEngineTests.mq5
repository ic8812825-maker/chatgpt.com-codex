#property strict
#property script_show_inputs

#include "../../../Include/Config.mqh"
#include "../../../Include/Types.mqh"
#include "../../../Include/LotUtils.mqh"
#include "../../../Include/SimulationEngine.mqh"
#include "../../../Include/RecoveryMath.mqh"
#include "../../../Include/BrokerMoneyModel.mqh"
#include "../../../Include/HybridRoundingModel.mqh"
#include "../../../Include/HybridCatchUpModel.mqh"
#include "../../../Include/HybridMarginModel.mqh"
#include "../../../Include/HybridWorstCaseModel.mqh"
#include "../../../Include/HybridFutureSmallSolver.mqh"
#include "../../../Include/HybridDecisionEngine.mqh"
#include "HybridDecisionFixtures.mqh"
#include "HybridDecisionAssertions.mqh"

void OnStart()
{
   HybridCycleSnapshot s;
   HybridCandidatePlan p;
   HybridEvaluationResult r;

   BuildHybridDefaultSnapshot(s);
   EvaluateHybridCandidate(s,p,r);
   if(!UseHybridSplitBigGeometry)
      HybridAssertTrue(!r.applicable && !r.passed && r.finalCode==HYBRID_FINAL_NONE,"Hybrid disabled returns NOT_APPLICABLE",r.reason);

   BuildHybridDefaultSnapshot(s);
   s.symbol="INVALID";
   EvaluateHybridCandidate(s,p,r);
   if(UseHybridSplitBigGeometry)
      HybridAssertReject(r,HYBRID_REJECT_IDENTITY,"Invalid Symbol rejects identity");

   BuildHybridDefaultSnapshot(s);
   s.cycleId=0;
   EvaluateHybridCandidate(s,p,r);
   if(UseHybridSplitBigGeometry)
      HybridAssertReject(r,HYBRID_REJECT_IDENTITY,"Invalid CycleID rejects identity");

   BuildHybridDefaultSnapshot(s);
   EvaluateHybridCandidate(s,p,r);
   if(UseHybridSplitBigGeometry)
      HybridAssertReject(r,HYBRID_REJECT_LAW1,"beta 0.70 current geometry rejects Law 1");

   double rawSmall=1.001;
   HybridAssertTrue(NormalizeHybridSmallLot(rawSmall)>=rawSmall,"Small UP rounding is used",DoubleToString(NormalizeHybridSmallLot(rawSmall),8));

   if(HybridDecisionTestFailures>0)
      PrintFormat("HYBRID_DECISION_ENGINE_TESTS FAILURES=%d",HybridDecisionTestFailures);
   else
      Print("HYBRID_DECISION_ENGINE_TESTS PASS");
}
