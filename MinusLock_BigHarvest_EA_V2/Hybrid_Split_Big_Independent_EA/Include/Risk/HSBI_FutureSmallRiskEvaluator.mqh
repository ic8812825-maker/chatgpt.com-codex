#ifndef HSBI_FUTURE_SMALL_RISK_EVALUATOR_MQH
#define HSBI_FUTURE_SMALL_RISK_EVALUATOR_MQH
#include "../Money/HSBI_BasketMoneyEvaluator.mqh"
enum HSBI_RiskProofSource
{
   HSBI_RISK_SOURCE_RUNTIME,
   HSBI_RISK_SOURCE_INJECTED_TEST_ONLY,
   HSBI_RISK_SOURCE_PROXY_TEST_ONLY,
   HSBI_RISK_SOURCE_UNAVAILABLE
};
struct HSBI_FutureSmallRiskInput
{
   HSBI_BasketMoneyResult basket;
   double priorRisk;
   double tolerance;
   double evaluatedRisk;
   HSBI_RiskProofSource source;
   bool runtimeConfirmed;
   bool testOnly;
   bool fresh;
   ulong snapshotId;
};
struct HSBI_FutureSmallRiskResult
{
   HSBI_CalculationStatus status; bool valid; double riskValue,priorRisk,tolerance;
   HSBI_RiskProofSource source; bool runtimeConfirmed,testOnly;
   HSBI_ReasonCode reason; string details;
};
HSBI_FutureSmallRiskResult HSBI_EvaluateFutureSmallRisk(const HSBI_FutureSmallRiskInput &x)
{
   HSBI_FutureSmallRiskResult r; ZeroMemory(r); r.status=HSBI_CALC_UNAVAILABLE;
   r.priorRisk=x.priorRisk; r.tolerance=x.tolerance; r.source=x.source;
   r.runtimeConfirmed=x.runtimeConfirmed; r.testOnly=x.testOnly;
   r.reason=HSBI_REASON_NOT_INITIALIZED; r.details="RISK_RUNTIME_PROOF_UNAVAILABLE";
   if(!x.fresh || x.snapshotId==0 || !x.basket.valid) return r;
   if(x.source!=HSBI_RISK_SOURCE_RUNTIME || !x.runtimeConfirmed || x.testOnly) {
      r.riskValue=(x.source==HSBI_RISK_SOURCE_PROXY_TEST_ONLY) ?
         x.basket.transitionLoss+x.basket.totalMargin+x.basket.grossExposure : x.evaluatedRisk;
      r.details="RISK_PROXY_OR_TEST_ONLY_FORBIDDEN"; return r;
   }
   r.riskValue=x.evaluatedRisk;
   if(!HSBI_IsFiniteNumber(r.riskValue)||!HSBI_IsFiniteNumber(x.priorRisk)||
      !HSBI_IsFiniteNumber(x.tolerance)||x.tolerance<0.0) {
      r.status=HSBI_CALC_ERROR; r.details="NONFINITE_RISK"; return r;
   }
   if(r.riskValue>=x.priorRisk-x.tolerance) {
      r.status=HSBI_CALC_REJECT; r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;
      r.details="RISK_NOT_REDUCED"; return r;
   }
   r.status=HSBI_CALC_PASS; r.valid=true; r.reason=HSBI_REASON_OK; r.details="PASS"; return r;
}
#endif
