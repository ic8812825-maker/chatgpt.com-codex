#ifndef HSBI_GEOMETRY_TYPES_MQH
#define HSBI_GEOMETRY_TYPES_MQH
#include "HSBI_ControlPrices.mqh"
struct HSBI_GeometrySnapshot{ulong snapshotId;double farReferencePrice;double bigMoveStartPoints;double bigMoveStepPoints;double smallOffsetPoints;int level;HSBI_ControlPriceSet controls;bool valid;};
struct HSBI_NormalizedLots{double farLots;double coreLots;double trendLots;double smallLots;double volumeMin;double volumeMax;double volumeStep;bool valid;};
struct HSBI_RecoveryDirectionResult{double baseMoney;double nextTickMoney;double deltaMoney;bool directionCorrect;bool moneyAvailable;bool priceFresh;HSBI_CalculationStatus status;HSBI_ReasonCode reason;};
#endif