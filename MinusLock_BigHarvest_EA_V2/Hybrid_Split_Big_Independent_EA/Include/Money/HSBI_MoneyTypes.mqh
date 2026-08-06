#ifndef HSBI_MONEY_TYPES_MQH
#define HSBI_MONEY_TYPES_MQH
struct HSBI_MoneyAmount{double value;bool actual;datetime timestamp;ulong snapshotId;string source;bool valid;};
struct HSBI_DealNetRecord{double profit;double swap;double commission;double fee;double dealNet;bool actual;datetime timestamp;ulong snapshotId;bool valid;};
struct HSBI_MoneyTolerance{double value;bool valid;};
struct HSBI_RecoveryPLSnapshot{double realizedCycleNet;double openPositionsCloseNowNet;double recoveryPLCloseNow;double minimumProfit;double executionBuffer;double tolerance;double threshold;bool allowed;datetime timestamp;ulong snapshotId;};
struct HSBI_FinalCloseThreshold{double minimumProfit;double executionBuffer;double tolerance;double threshold;bool valid;};
struct HSBI_TransitionLossSnapshot{double transitionNet;double transitionLossMoney;double absoluteCap;double equityCap;double oldFarRiskCap;double cumulativeCap;double allowedCap;bool allowed;};
HSBI_RecoveryPLSnapshot HSBI_BuildRecoveryPL(const double realized,const double openNet,const HSBI_FinalCloseThreshold &t){HSBI_RecoveryPLSnapshot r;r.realizedCycleNet=realized;r.openPositionsCloseNowNet=openNet;r.recoveryPLCloseNow=realized+openNet;r.minimumProfit=t.minimumProfit;r.executionBuffer=t.executionBuffer;r.tolerance=t.tolerance;r.threshold=t.threshold;r.allowed=r.recoveryPLCloseNow>=r.threshold;return r;}
#endif