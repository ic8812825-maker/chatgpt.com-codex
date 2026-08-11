#ifndef HSBI_NEW_FAR_GATE_TYPES_MQH
#define HSBI_NEW_FAR_GATE_TYPES_MQH
#include "HSBI_CalculationGateTypes.mqh"
struct HSBI_NewFarGateInput{double marginNext;double allowedMargin;double riskNext;double riskOld;double riskTolerance;double grossExposureNext;double grossExposureOld;double transitionLoss;double absoluteLossCap;double equityPercentCap;double oldFarRiskCap;double cumulativeCycleLossCap;bool marginAvailable;bool riskAvailable;bool transitionCapAvailable;bool moneyAvailable;bool snapshotFresh;};
struct HSBI_NewFarGateResult{bool passed;HSBI_CalculationStatus status;double allowedTransitionLoss;HSBI_CalculationFailure failure;HSBI_ReasonCode reason;};
HSBI_NewFarGateResult HSBI_EvaluateNewFarGates(const HSBI_NewFarGateInput &x)
{
   HSBI_NewFarGateResult r;ZeroMemory(r);r.status=HSBI_CALC_REJECT;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;
   if(!x.snapshotFresh){r.failure=HSBI_STALE_SNAPSHOT;r.reason=HSBI_REASON_STALE_SNAPSHOT;return r;}
   if(!x.marginAvailable||!x.riskAvailable||!x.transitionCapAvailable||!x.moneyAvailable){r.status=HSBI_CALC_UNAVAILABLE;r.failure=HSBI_BROKER_MONEY_UNAVAILABLE;return r;}
   if(!HSBI_IsFiniteNumber(x.absoluteLossCap)||!HSBI_IsFiniteNumber(x.equityPercentCap)||!HSBI_IsFiniteNumber(x.oldFarRiskCap)||!HSBI_IsFiniteNumber(x.cumulativeCycleLossCap)||x.absoluteLossCap<0.0||x.equityPercentCap<0.0||x.oldFarRiskCap<0.0||x.cumulativeCycleLossCap<0.0){r.failure=HSBI_CATCH_UP_FAILED;return r;}
   r.allowedTransitionLoss=MathMin(MathMin(x.absoluteLossCap,x.equityPercentCap),MathMin(x.oldFarRiskCap,x.cumulativeCycleLossCap));
   if(!HSBI_IsFiniteNumber(x.marginNext)||x.marginNext>x.allowedMargin){r.failure=HSBI_NONFINITE_MARGIN;return r;}
   if(!HSBI_IsFiniteNumber(x.riskNext)||x.riskNext>=x.riskOld-x.riskTolerance||!HSBI_IsFiniteNumber(x.grossExposureNext)||x.grossExposureNext>=x.grossExposureOld){r.failure=HSBI_RECOVERY_SLOPE_FAILED;return r;}
   if(!HSBI_IsFiniteNumber(x.transitionLoss)||x.transitionLoss>r.allowedTransitionLoss){r.failure=HSBI_CATCH_UP_FAILED;return r;}
   r.passed=true;r.status=HSBI_CALC_PASS;r.failure=HSBI_CALC_FAILURE_NONE;r.reason=HSBI_REASON_OK;return r;
}
#endif
