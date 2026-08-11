#ifndef HSBI_CATCH_UP_TYPES_MQH
#define HSBI_CATCH_UP_TYPES_MQH
#include "HSBI_BrokerMoneyTypes.mqh"
struct HSBI_CatchUpInput{double reserveShare;double netBigVolume;double farVolume;double reserveGainMoney;double farLossIncreaseMoney;double executionSafetyBuffer;HSBI_Direction farDirection;bool moneyAvailable;bool snapshotFresh;};
struct HSBI_CatchUpResult{double reserveShare;double netBigVolume;double farVolume;double reserveGainMoney;double farLossIncreaseMoney;double executionSafetyBuffer;double catchUpMargin;bool passed;HSBI_CalculationStatus status;HSBI_ReasonCode reason;};
#endif
