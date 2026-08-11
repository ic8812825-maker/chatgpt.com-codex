#ifndef HSBI_CANDIDATE_MONEY_EVALUATOR_MQH
#define HSBI_CANDIDATE_MONEY_EVALUATOR_MQH
#include "../Planning/HSBI_FutureSmallSolver.mqh"
struct HSBI_CandidateMoneyEvaluationResult
{
   HSBI_CalculationStatus status; bool valid; HSBI_FutureSmallResult futureSmallProof;
   string moneyProofDigest,marginProofDigest,riskProofDigest,futureSmallProofDigest;
   HSBI_ReasonCode reason; string details;
};
HSBI_CandidateMoneyEvaluationResult HSBI_EvaluateCandidateMoney(const HSBI_FutureSmallInput &candidateInput)
{
   HSBI_CandidateMoneyEvaluationResult r;ZeroMemory(r);r.status=HSBI_CALC_UNAVAILABLE;
   r.reason=HSBI_REASON_NOT_INITIALIZED;r.details="CANDIDATE_PROOF_UNAVAILABLE";
   if(candidateInput.testOnlyApproximation||candidateInput.useInjectedBrokerProofs)return r;
   r.futureSmallProof=HSBI_SolveFutureSmall(candidateInput);
   if(!r.futureSmallProof.valid||r.futureSmallProof.provenDepth<2)return r;
   r.futureSmallProofDigest=HSBI_FutureSmallProofDigest(r.futureSmallProof);
   r.moneyProofDigest="MONEY";r.marginProofDigest="MARGIN";r.riskProofDigest="RISK";
   for(int i=0;i<r.futureSmallProof.provenDepth;i++) {
      HSBI_FutureSmallLevelProof p=r.futureSmallProof.levels[i];
      r.moneyProofDigest+="|"+IntegerToString(i)+"|"+DoubleToString(p.projectedRecoveryMoney,8)+"|"+IntegerToString((int)p.moneyProofStatus);
      r.marginProofDigest+="|"+IntegerToString(i)+"|"+DoubleToString(p.projectedMargin,8)+"|"+IntegerToString((int)p.marginProofStatus);
      r.riskProofDigest+="|"+IntegerToString(i)+"|"+DoubleToString(p.projectedRisk,8)+"|"+IntegerToString((int)p.riskProofStatus);
   }
   if(r.futureSmallProofDigest==""||r.moneyProofDigest==""||r.marginProofDigest==""||r.riskProofDigest=="")return r;
   r.status=HSBI_CALC_PASS;r.valid=true;r.reason=HSBI_REASON_OK;r.details="PASS";return r;
}
#endif
