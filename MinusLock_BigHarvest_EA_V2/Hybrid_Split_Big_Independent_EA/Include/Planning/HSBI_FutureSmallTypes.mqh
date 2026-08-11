#ifndef HSBI_FUTURE_SMALL_TYPES_MQH
#define HSBI_FUTURE_SMALL_TYPES_MQH
#include "HSBI_GeometrySolver.mqh"
#include "../Money/HSBI_BasketMoneyEvaluator.mqh"
#include "../Money/HSBI_AllocationPolicyTypes.mqh"
#include "../Risk/HSBI_FutureSmallRiskEvaluator.mqh"
enum HSBI_FutureSmallProofStatus { HSBI_FS_EXACT_PROOF, HSBI_FS_CONSERVATIVE_BOUND, HSBI_FS_UNPROVEN, HSBI_FS_REJECTED };
enum HSBI_FutureFarProjectionSource { HSBI_FAR_PROJECTION_BIGCORE_RESIDUAL, HSBI_FAR_PROJECTION_EXPLICIT_MODEL, HSBI_FAR_PROJECTION_UNAVAILABLE };
struct HSBI_MoneyStateSnapshot { double recoveryMoney; double reserve; bool available; bool fresh; ulong snapshotId; };
struct HSBI_RiskSnapshot { double currentRisk; double riskTolerance; double currentGrossExposure; double nextGrossExposureLimit; bool available; bool fresh; ulong snapshotId; };
struct HSBI_MarginSnapshot { double currentMargin; double allowedMargin; bool available; bool fresh; ulong snapshotId; };
struct HSBI_ControlPriceSnapshot { string symbol; double selectedPrice; double tickSize; bool valid; bool fresh; ulong snapshotId; };
struct HSBI_FutureSmallLevelMarketSnapshot
{
   int levelIndex; string symbol; double bid; double ask; double selectedPrice; double tickSize;
   HSBI_PriceSide side; datetime timestamp; ulong snapshotId; bool fresh; bool normalized; bool valid;
};
struct HSBI_FutureSmallLevelCostSnapshot
{
   int levelIndex; HSBI_CostSnapshot farCosts; HSBI_CostSnapshot coreCosts;
   HSBI_CostSnapshot trendCosts; HSBI_CostSnapshot smallCosts;
   ulong snapshotId; bool fresh; bool valid; bool sharedCostSnapshot;
};
struct HSBI_FutureFarProjection
{
   double projectedFar; HSBI_FutureFarProjectionSource source; ulong sourceIdentifier; ulong sourceDealId;
   bool projected; bool actual; bool confirmed; bool valid; HSBI_ReasonCode reason;
};
struct HSBI_FutureSmallInput
{
   HSBI_AllocationPolicySnapshot allocationPolicy;
   double currentFar,coreRatio,trendRatio,smallRatio,maxNewFarRatio,minimumCompressionLots,minimumCompressionRatio;
   int maximumDepth; double conservativeQ,volumeMin,volumeMax,volumeStep,tickSize; HSBI_Direction farDirection;
   HSBI_MoneyStateSnapshot moneyState; HSBI_RiskSnapshot riskState; HSBI_MarginSnapshot marginState;
   HSBI_ControlPriceSnapshot controlPrice; HSBI_ControlPrice typedControlPrice; HSBI_BrokerProperties broker;
   double farOpenPrice,coreOpenPrice,trendOpenPrice,smallOpenPrice,transitionLossCap,executionSafetyBuffer;
   double expectedReserve,currentBigGross,currentGrossExposure; ulong cycleId,stateRevision,planId;
   bool snapshotsFresh,brokerPropertiesValid,costsIncluded,roundingIncluded,terminalRouteAllowed;
   bool useInjectedBrokerProofs,testOnlyApproximation;
   int levelMarketSnapshotCount,levelCostSnapshotCount,farProjectionCount;
   HSBI_FutureSmallLevelMarketSnapshot levelMarketSnapshots[128];
   HSBI_FutureSmallLevelCostSnapshot levelCostSnapshots[128];
   HSBI_FutureFarProjection farProjections[128];
   double evaluatedRisks[128]; HSBI_RiskProofSource riskProofSources[128];
   bool riskRuntimeConfirmed[128]; bool riskTestOnly[128]; ulong riskProofSnapshotIds[128];
   HSBI_BasketMoneyResult injectedBrokerProofs[128];
};
struct HSBI_FutureSmallLevelProof
{
   int levelIndex; double farBefore,coreVolume,trendVolume,smallVolume,netBigVolume,farAfter;
   double compressionLots,compressionRatio,recoverySlopeLots,projectedRecoveryMoney,projectedReserve;
   double projectedMargin,projectedRisk,transitionLoss,grossExposure,controlPrice,bid,ask,tickSize;
   ulong controlSnapshotId,farCostSnapshotId,coreCostSnapshotId,trendCostSnapshotId,smallCostSnapshotId;
   bool moneyIncluded,marginIncluded,riskIncluded,transitionLossIncluded;
   HSBI_CalculationStatus moneyProofStatus,marginProofStatus,riskProofStatus,transitionLossProofStatus;
   HSBI_FutureSmallProofStatus proofStatus; HSBI_ReasonCode reason; string levelDigest; HSBI_BrokerMoneyEvaluationResult reserveSourceProof; HSBI_BrokerMoneyEvaluationResult farLossProof;
};
struct HSBI_FutureSmallResult
{
   bool valid; HSBI_FutureSmallProofStatus status; int provenDepth,theoreticalDepth; double terminalFar;
   bool finiteSequence,plateauDetected; ulong planId,stateRevision; string proofDigest;
   HSBI_ReasonCode reason; string details; HSBI_FutureSmallLevelProof levels[128];
};
struct HSBI_FutureSmallLevelInput
{
   int levelIndex; double farBefore,coreRatio,trendRatio,smallRatio; HSBI_Direction farDirection; HSBI_BrokerProperties broker;
   HSBI_FutureSmallLevelMarketSnapshot market; HSBI_FutureSmallLevelCostSnapshot costs;
   HSBI_FutureFarProjection farProjection; double farOpenPrice,coreOpenPrice,trendOpenPrice,smallOpenPrice;
   HSBI_MoneyStateSnapshot moneyState; HSBI_RiskSnapshot riskState; HSBI_MarginSnapshot marginState;
   double minimumCompressionLots,minimumCompressionRatio,maxNewFarRatio,transitionLossCap,executionSafetyBuffer;
   double priorBigGross,priorGrossExposure; double evaluatedRisk; HSBI_RiskProofSource riskProofSource; bool riskRuntimeConfirmed,riskTestOnly; ulong riskProofSnapshotId; ulong planId,stateRevision;
   bool useInjectedBrokerProof,testOnlyApproximation; HSBI_BasketMoneyResult injectedBrokerProof;
};
struct HSBI_FutureSmallLevelResult
{
   bool valid; int levelIndex; double farBefore,farAfter,coreVolume,trendVolume,smallVolume,netBigVolume;
   double recoverySlopeLots,recoveryMoney,totalMargin,grossExposure,transitionLoss,compressionLots,compressionRatio,riskValue;
   bool moneyIncluded,marginIncluded,riskIncluded,transitionLossIncluded;
   HSBI_FutureSmallProofStatus status; HSBI_ReasonCode reason; string details;
   HSBI_BasketMoneyResult basketProof;
};
#endif
