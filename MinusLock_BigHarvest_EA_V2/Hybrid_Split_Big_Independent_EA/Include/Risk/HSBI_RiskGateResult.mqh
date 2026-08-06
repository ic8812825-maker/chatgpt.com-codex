#ifndef HSBI_RISK_GATE_RESULT_MQH
#define HSBI_RISK_GATE_RESULT_MQH
#include "HSBI_RiskTypes.mqh"
#include "../Core/HSBI_ReasonCodes.mqh"
struct HSBI_RiskGateResult{bool passed;ulong gateMask;int failedGate;HSBI_ReasonCode reason;bool failClosed;};
HSBI_RiskGateResult HSBI_ValidateRiskInput(const HSBI_RiskInput &x,const HSBI_RiskLimits &l){HSBI_RiskGateResult r;r.passed=false;r.gateMask=0;r.failedGate=0;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.failClosed=true;if(!x.snapshotFresh){r.reason=HSBI_REASON_STALE_SNAPSHOT;return r;}if(x.projectedMargin>l.maxProjectedMargin){r.failedGate=1;return r;}if(x.projectedMarginLevel<l.minMarginLevel){r.failedGate=2;return r;}if(x.freeMarginAfter<l.minFreeMargin){r.failedGate=3;return r;}if(x.cycleDrawdown>l.maxCycleDrawdown||x.accountDrawdown>l.maxAccountDrawdown){r.failedGate=4;return r;}if(x.grossExposure>l.maxGrossExposure||x.managedPositions>l.maxManagedPositions){r.failedGate=5;return r;}if(x.worstCaseLoss>l.maxWorstCaseLoss||x.transitionLoss>l.maxTransitionLoss||x.spread>l.maxSpread){r.failedGate=6;return r;}r.passed=true;r.gateMask=63;r.failedGate=-1;r.reason=HSBI_REASON_OK;return r;}
#endif