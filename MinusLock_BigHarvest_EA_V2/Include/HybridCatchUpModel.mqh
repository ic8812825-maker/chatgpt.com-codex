#ifndef __BH_HYBRID_CATCHUP_MODEL_MQH__
#define __BH_HYBRID_CATCHUP_MODEL_MQH__

bool EvaluateHybridFiniteCatchUpPreview(const HybridCycleSnapshot &snapshot,const HybridCandidatePlan &plan,HybridCatchUpResult &result)
{
   result.pass=false; result.finiteLevel=-1; result.finalCoverageDeficit=0; result.finalRecoveryPL=0; result.reason="NOT_EVALUATED";
   if(MaxHarvestLevels<=0) { result.reason="MAX_HARVEST_LEVELS_INVALID"; return false; }
   double eligible = MathMax(0.0, plan.projectedHarvestNet);
   double partialAdd = HybridPartialFarShare * eligible;
   double reserveAdd = HybridFinalReserveShare * eligible;
   double carryAdd = eligible - partialAdd - reserveAdd;
   if(carryAdd < -MoneyCalculationTolerance) { result.reason="ALLOCATION_NEGATIVE_CARRY"; return false; }
   double reserve = snapshot.finalReserveReal;
   double recovery = snapshot.realizedCyclePL;
   double farCloseCost = MathMax(0.0, -plan.projectedHarvestNet);
   for(int level=1; level<=MaxHarvestLevels; level++)
   {
      reserve += reserveAdd;
      recovery += plan.projectedHarvestNet;
      double deficit = farCloseCost - reserve;
      result.finalCoverageDeficit = deficit;
      result.finalRecoveryPL = recovery;
      if(deficit <= MoneyCalculationTolerance && recovery + MoneyCalculationTolerance >= MinimumRecoveryProfitMoney)
      {
         result.pass=true; result.finiteLevel=level; result.reason="PASS"; return true;
      }
   }
   result.reason="NO_FINITE_CATCHUP_LEVEL";
   return false;
}

#endif // __BH_HYBRID_CATCHUP_MODEL_MQH__
