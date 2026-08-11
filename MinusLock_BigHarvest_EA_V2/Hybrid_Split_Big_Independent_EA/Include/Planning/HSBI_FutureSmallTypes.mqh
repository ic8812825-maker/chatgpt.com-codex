#ifndef HSBI_FUTURE_SMALL_TYPES_MQH
#define HSBI_FUTURE_SMALL_TYPES_MQH
#include "HSBI_GeometrySolver.mqh"
enum HSBI_FutureSmallProofStatus{HSBI_FS_EXACT_PROOF,HSBI_FS_CONSERVATIVE_BOUND,HSBI_FS_UNPROVEN,HSBI_FS_REJECTED};
struct HSBI_MoneyStateSnapshot{double recoveryMoney;double reserve;bool available;bool fresh;ulong snapshotId;};
struct HSBI_RiskSnapshot{double currentRisk;double riskTolerance;double currentGrossExposure;double nextGrossExposureLimit;bool available;bool fresh;ulong snapshotId;};
struct HSBI_MarginSnapshot{double currentMargin;double allowedMargin;bool available;bool fresh;ulong snapshotId;};
struct HSBI_ControlPriceSnapshot{string symbol;double selectedPrice;double tickSize;bool valid;bool fresh;ulong snapshotId;};
struct HSBI_FutureSmallInput{double currentFar;double coreRatio;double trendRatio;double smallRatio;double maxNewFarRatio;double minimumCompressionLots;double minimumCompressionRatio;int maximumDepth;double conservativeQ;double volumeMin;double volumeMax;double volumeStep;double tickSize;HSBI_Direction farDirection;HSBI_MoneyStateSnapshot moneyState;HSBI_RiskSnapshot riskState;HSBI_MarginSnapshot marginState;HSBI_ControlPriceSnapshot controlPrice;ulong cycleId;ulong stateRevision;ulong planId;double commission;double swap;double fee;double slippageBuffer;double transitionLossCap;double transitionLossPerLevel;double expectedReserve;double currentGrossExposure;double riskDecreasePerLevel;double projectedRecoveryMoneyPerLevel;bool snapshotsFresh;bool brokerPropertiesValid;bool costsIncluded;bool roundingIncluded;bool terminalRouteAllowed;};
struct HSBI_FutureSmallLevelProof{int levelIndex;double farBefore;double coreVolume;double trendVolume;double smallVolume;double netBigVolume;double farAfter;double compressionLots;double compressionRatio;double recoverySlopeLots;double projectedRecoveryMoney;double projectedReserve;double projectedMargin;double projectedRisk;double transitionLoss;HSBI_FutureSmallProofStatus proofStatus;HSBI_ReasonCode reason;};
struct HSBI_FutureSmallResult{bool valid;HSBI_FutureSmallProofStatus status;int provenDepth;int theoreticalDepth;double terminalFar;bool finiteSequence;bool plateauDetected;ulong planId;ulong stateRevision;string proofDigest;HSBI_ReasonCode reason;string details;HSBI_FutureSmallLevelProof levels[];};
#endif
