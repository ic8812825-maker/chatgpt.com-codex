#ifndef HSBI_FUTURE_SMALL_PROOF_AGGREGATOR_MQH
#define HSBI_FUTURE_SMALL_PROOF_AGGREGATOR_MQH
#include "HSBI_FutureSmallSolver.mqh"
enum HSBI_ProofSelectionPolicy { HSBI_PROOF_POLICY_WORST_CASE,HSBI_PROOF_POLICY_FINAL_LEVEL,HSBI_PROOF_POLICY_EXPLICIT_CONTROL_LEVEL };
struct HSBI_FutureSmallAggregateProof
{
   bool valid;int levelCount,evaluatedLevelCount,rejectedLevelCount;
   double worstRecoveryMoney,minimumRecoveryMoney,worstMargin,maximumMargin,worstRisk,maximumRisk;
   double worstGrossExposure,maximumGrossExposure,worstTransitionLoss,maximumTransitionLoss;
   double minimumCompressionLots,minimumCompressionRatio,finalFar,maximumFutureTransitions,safetyBuffer;
   int worstRecoveryLevel,worstMarginLevel,worstRiskLevel,worstExposureLevel,worstTransitionLossLevel,catchUpControlLevel;
   bool allMoneyProofsValid,allMarginProofsValid,allRiskProofsValid,allTransitionLossProofsValid;
   bool allControlSnapshotsValid,allCostSnapshotsValid,allFarProjectionsValid,exactProof,conservativeBound,runtimeConfirmed;
   HSBI_ProofSelectionPolicy selectionPolicy;string aggregateDigest;HSBI_ReasonCode reason;string details;
};
string HSBI_AggregateDigest(const HSBI_FutureSmallAggregateProof &a,const string levelsDigest)
{return "AGG|"+IntegerToString((int)a.selectionPolicy)+"|"+IntegerToString(a.levelCount)+"|"+DoubleToString(a.minimumRecoveryMoney,8)+"|"+
   DoubleToString(a.maximumMargin,8)+"|"+DoubleToString(a.maximumRisk,8)+"|"+DoubleToString(a.maximumGrossExposure,8)+"|"+
   DoubleToString(a.maximumTransitionLoss,8)+"|"+DoubleToString(a.minimumCompressionLots,8)+"|"+DoubleToString(a.minimumCompressionRatio,12)+"|"+
   DoubleToString(a.finalFar,8)+"|"+IntegerToString(a.worstRecoveryLevel)+"|"+IntegerToString(a.worstMarginLevel)+"|"+
   IntegerToString(a.worstRiskLevel)+"|"+IntegerToString(a.worstExposureLevel)+"|"+IntegerToString(a.worstTransitionLossLevel)+"|"+
   IntegerToString(a.catchUpControlLevel)+"|"+levelsDigest;}
HSBI_FutureSmallAggregateProof HSBI_AggregateFutureSmallProof(const HSBI_FutureSmallResult &p,const HSBI_ProofSelectionPolicy policy,const int explicitControlLevel)
{
   HSBI_FutureSmallAggregateProof a;ZeroMemory(a);a.levelCount=p.provenDepth;a.selectionPolicy=policy;a.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;
   a.details="PROOF_INCOMPLETE";a.allMoneyProofsValid=true;a.allMarginProofsValid=true;a.allRiskProofsValid=true;
   a.allTransitionLossProofsValid=true;a.allControlSnapshotsValid=true;a.allCostSnapshotsValid=true;a.allFarProjectionsValid=true;a.runtimeConfirmed=true;
   if(!p.valid||p.provenDepth<2||p.provenDepth>128)return a;string chain="";
   for(int i=0;i<p.provenDepth;i++){
      HSBI_FutureSmallLevelProof l=p.levels[i];a.evaluatedLevelCount++;
      bool complete=l.valid&&l.levelIndex==i+1&&l.moneyIncluded&&l.marginIncluded&&l.riskIncluded&&l.transitionLossIncluded&&
         l.controlSnapshotValid&&l.costSnapshotValid&&l.farProjectionValid&&l.proofStatus==HSBI_FS_EXACT_PROOF&&l.runtimeConfirmed;
      if(!complete)a.rejectedLevelCount++;
      a.allMoneyProofsValid&=l.valid&&l.moneyIncluded&&l.moneyProofStatus==HSBI_CALC_PASS;
      a.allMarginProofsValid&=l.valid&&l.marginIncluded&&l.marginProofStatus==HSBI_CALC_PASS;
      a.allRiskProofsValid&=l.valid&&l.riskIncluded&&l.riskProofStatus==HSBI_CALC_PASS;
      a.allTransitionLossProofsValid&=l.valid&&l.transitionLossIncluded&&l.transitionLossProofStatus==HSBI_CALC_PASS;
      a.allControlSnapshotsValid&=l.controlSnapshotValid;a.allCostSnapshotsValid&=l.costSnapshotValid;
      a.allFarProjectionsValid&=l.farProjectionValid;a.runtimeConfirmed&=l.runtimeConfirmed;
      if(i==0||l.projectedRecoveryMoney<a.minimumRecoveryMoney){a.minimumRecoveryMoney=l.projectedRecoveryMoney;a.worstRecoveryMoney=l.projectedRecoveryMoney;a.worstRecoveryLevel=l.levelIndex;}
      if(i==0||l.projectedMargin>a.maximumMargin){a.maximumMargin=l.projectedMargin;a.worstMargin=l.projectedMargin;a.worstMarginLevel=l.levelIndex;}
      if(i==0||l.projectedRisk>a.maximumRisk){a.maximumRisk=l.projectedRisk;a.worstRisk=l.projectedRisk;a.worstRiskLevel=l.levelIndex;}
      if(i==0||l.grossExposure>a.maximumGrossExposure){a.maximumGrossExposure=l.grossExposure;a.worstGrossExposure=l.grossExposure;a.worstExposureLevel=l.levelIndex;}
      if(i==0||l.transitionLoss>a.maximumTransitionLoss){a.maximumTransitionLoss=l.transitionLoss;a.worstTransitionLoss=l.transitionLoss;a.worstTransitionLossLevel=l.levelIndex;}
      if(i==0||l.compressionLots<a.minimumCompressionLots)a.minimumCompressionLots=l.compressionLots;
      if(i==0||l.compressionRatio<a.minimumCompressionRatio)a.minimumCompressionRatio=l.compressionRatio;
      chain+="|"+HSBI_FutureSmallLevelDigest(l);
   }
   a.finalFar=p.levels[p.provenDepth-1].farAfter;a.maximumFutureTransitions=p.theoreticalDepth;
   if(policy==HSBI_PROOF_POLICY_WORST_CASE)a.catchUpControlLevel=a.worstTransitionLossLevel;
   else if(policy==HSBI_PROOF_POLICY_FINAL_LEVEL)a.catchUpControlLevel=p.provenDepth;
   else a.catchUpControlLevel=explicitControlLevel;
   if(a.catchUpControlLevel<1||a.catchUpControlLevel>p.provenDepth)a.rejectedLevelCount++;
   a.exactProof=p.status==HSBI_FS_EXACT_PROOF;a.conservativeBound=p.status==HSBI_FS_CONSERVATIVE_BOUND;
   a.valid=a.rejectedLevelCount==0&&a.allMoneyProofsValid&&a.allMarginProofsValid&&a.allRiskProofsValid&&
      a.allTransitionLossProofsValid&&a.allControlSnapshotsValid&&a.allCostSnapshotsValid&&a.allFarProjectionsValid&&a.runtimeConfirmed;
   a.reason=a.valid?HSBI_REASON_OK:HSBI_REASON_INTERNAL_INVARIANT_FAILED;a.details=a.valid?"AGGREGATE_VALID":"PROOF_INCOMPLETE";
   a.aggregateDigest=HSBI_AggregateDigest(a,chain);return a;
}
#endif
