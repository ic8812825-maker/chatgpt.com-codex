#ifndef HSBI_CANDIDATE_MONEY_EVALUATOR_MQH
#define HSBI_CANDIDATE_MONEY_EVALUATOR_MQH
#include "../Planning/HSBI_FutureSmallSolver.mqh"
struct HSBI_CandidateMoneyEvaluationResult{HSBI_CalculationStatus status;bool valid;HSBI_FutureSmallResult futureSmallProof;HSBI_BasketMoneyResult firstLevelBasket;string moneyProofDigest;string marginProofDigest;string riskProofDigest;HSBI_ReasonCode reason;string details;};
HSBI_CandidateMoneyEvaluationResult HSBI_EvaluateCandidateMoney(const HSBI_FutureSmallInput &candidateInput)
{
   HSBI_CandidateMoneyEvaluationResult r;ZeroMemory(r);r.status=HSBI_CALC_UNAVAILABLE;r.reason=HSBI_REASON_NOT_INITIALIZED;r.details="CANDIDATE_PROOF_UNAVAILABLE";if(candidateInput.testOnlyApproximation||candidateInput.useInjectedBrokerProofs)return r;r.futureSmallProof=HSBI_SolveFutureSmall(candidateInput);if(!r.futureSmallProof.valid||r.futureSmallProof.provenDepth<2)return r;
   HSBI_FutureSmallLevelProof first=r.futureSmallProof.levels[0];r.moneyProofDigest=DoubleToString(first.projectedRecoveryMoney,8);r.marginProofDigest=DoubleToString(first.projectedMargin,8);r.riskProofDigest=DoubleToString(first.projectedRisk,8);r.status=HSBI_CALC_PASS;r.valid=true;r.reason=HSBI_REASON_OK;r.details="PASS";return r;
}
#endif
