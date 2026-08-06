#ifndef HSBI_RISK_TYPES_MQH
#define HSBI_RISK_TYPES_MQH
struct HSBI_RiskInput{double projectedMargin;double projectedMarginLevel;double freeMarginAfter;double cycleDrawdown;double accountDrawdown;double grossExposure;int managedPositions;double worstCaseLoss;double transitionLoss;double spread;bool snapshotFresh;};
struct HSBI_RiskLimits{double maxProjectedMargin;double minMarginLevel;double minFreeMargin;double maxCycleDrawdown;double maxAccountDrawdown;double maxGrossExposure;int maxManagedPositions;double maxWorstCaseLoss;double maxTransitionLoss;double maxSpread;};
#endif