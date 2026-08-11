#ifndef HSBI_CATCH_UP_MODEL_MQH
#define HSBI_CATCH_UP_MODEL_MQH
#include "HSBI_CatchUpTypes.mqh"
HSBI_CatchUpResult HSBI_EvaluateCatchUp(const HSBI_CatchUpInput &x)
{
   HSBI_CatchUpResult r;ZeroMemory(r);r.reserveShare=x.reserveShare;r.netBigVolume=x.netBigVolume;r.farVolume=x.farVolume;r.reserveGainMoney=x.reserveGainMoney;r.farLossIncreaseMoney=x.farLossIncreaseMoney;r.executionSafetyBuffer=x.executionSafetyBuffer;r.status=HSBI_CALC_REJECT;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;
   if(!x.snapshotFresh){r.reason=HSBI_REASON_STALE_SNAPSHOT;return r;}
   if(!x.moneyAvailable){r.status=HSBI_CALC_UNAVAILABLE;r.reason=HSBI_REASON_NOT_INITIALIZED;return r;}
   if(x.farDirection!=HSBI_DIRECTION_BUY&&x.farDirection!=HSBI_DIRECTION_SELL)return r;
   if(!HSBI_IsFiniteNumber(x.reserveShare)||!HSBI_IsFiniteNumber(x.netBigVolume)||!HSBI_IsFiniteNumber(x.farVolume)||!HSBI_IsFiniteNumber(x.reserveGainMoney)||!HSBI_IsFiniteNumber(x.farLossIncreaseMoney)||!HSBI_IsFiniteNumber(x.executionSafetyBuffer))return r;
   if(x.reserveShare<=0.0||x.reserveShare>1.0||x.netBigVolume<=0.0||x.farVolume<=0.0||x.executionSafetyBuffer<0.0)return r;
   if(x.reserveShare*x.netBigVolume<=x.farVolume)return r;
   r.catchUpMargin=x.reserveGainMoney-x.farLossIncreaseMoney-x.executionSafetyBuffer;
   if(r.catchUpMargin<=0.0)return r;
   r.passed=true;r.status=HSBI_CALC_PASS;r.reason=HSBI_REASON_OK;return r;
}
#endif
