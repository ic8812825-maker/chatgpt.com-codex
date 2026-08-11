#ifndef HSBI_FUTURE_SMALL_RISK_EVALUATOR_MQH
#define HSBI_FUTURE_SMALL_RISK_EVALUATOR_MQH
#include "../Money/HSBI_BasketMoneyEvaluator.mqh"
struct HSBI_FutureSmallRiskResult{HSBI_CalculationStatus status;bool valid;double riskValue;double priorRisk;double tolerance;HSBI_ReasonCode reason;string details;};
HSBI_FutureSmallRiskResult HSBI_EvaluateFutureSmallRisk(const HSBI_BasketMoneyResult &basket,const double priorRisk,const double tolerance,const bool riskAvailable)
{
   HSBI_FutureSmallRiskResult r;ZeroMemory(r);r.status=HSBI_CALC_UNAVAILABLE;r.priorRisk=priorRisk;r.tolerance=tolerance;r.reason=HSBI_REASON_NOT_INITIALIZED;r.details="RISK_UNAVAILABLE";if(!riskAvailable||!basket.valid)return r;
   r.riskValue=basket.transitionLoss+basket.totalMargin+basket.grossExposure;if(!HSBI_IsFiniteNumber(r.riskValue)||!HSBI_IsFiniteNumber(priorRisk)||!HSBI_IsFiniteNumber(tolerance)||tolerance<0.0){r.status=HSBI_CALC_ERROR;r.details="NONFINITE_RISK";return r;}
   if(r.riskValue>=priorRisk-tolerance){r.status=HSBI_CALC_REJECT;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details="RISK_NOT_REDUCED";return r;}r.status=HSBI_CALC_PASS;r.valid=true;r.reason=HSBI_REASON_OK;r.details="PASS";return r;
}
#endif
