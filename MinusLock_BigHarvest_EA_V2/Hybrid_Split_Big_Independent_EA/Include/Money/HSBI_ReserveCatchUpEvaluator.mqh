#ifndef HSBI_RESERVE_CATCH_UP_EVALUATOR_MQH
#define HSBI_RESERVE_CATCH_UP_EVALUATOR_MQH
#include "HSBI_AllocationPolicyTypes.mqh"
#include "HSBI_LevelMoneyEvaluator.mqh"
struct HSBI_ReserveCatchUpInput
{
   HSBI_AllocationPolicySnapshot allocationPolicy;
   double reserveEligibleMoney;
   bool reserveEligibleMoneyAlreadyAllocated;
   double farLossIncreaseMoney;
   double executionSafetyBuffer;
   double netBigVolume;
   double farVolume;
   HSBI_Direction farDirection;
   HSBI_BrokerMoneyEvaluationResult reserveSourceProof;
   HSBI_BrokerMoneyEvaluationResult farLossProof;
   ulong sourceDealId;
   ulong sourceEventId;
   ulong planId;
   ulong stateRevision;
   ulong snapshotId;
   bool projected;
   bool moneyAvailable;
   bool fresh;
};
struct HSBI_ReserveCatchUpResult
{
   HSBI_CalculationStatus status;
   bool valid;
   bool projected;
   double reserveShare;
   double reserveEligibleMoney;
   double reserveGainMoney;
   double farLossIncreaseMoney;
   double executionSafetyBuffer;
   double catchUpMargin;
   ulong sourceDealId;
   ulong sourceEventId;
   ulong planId;
   ulong stateRevision;
   HSBI_ReasonCode reason;
   string details;
};
HSBI_ReserveCatchUpResult HSBI_EvaluateReserveCatchUp(const HSBI_ReserveCatchUpInput &x)
{
   HSBI_ReserveCatchUpResult r; ZeroMemory(r);
   r.status=HSBI_CALC_UNAVAILABLE; r.reason=HSBI_REASON_NOT_INITIALIZED; r.details="RESERVE_SOURCE_UNAVAILABLE";
   r.projected=x.projected; r.reserveShare=x.allocationPolicy.reserveShare;
   r.reserveEligibleMoney=x.reserveEligibleMoney; r.farLossIncreaseMoney=x.farLossIncreaseMoney;
   r.executionSafetyBuffer=x.executionSafetyBuffer; r.sourceDealId=x.sourceDealId;
   r.sourceEventId=x.sourceEventId; r.planId=x.planId; r.stateRevision=x.stateRevision;
   if(!HSBI_ValidateAllocationPolicy(x.allocationPolicy) || !x.moneyAvailable || !x.fresh ||
      x.snapshotId==0 || x.planId==0 || x.stateRevision==0) return r;
   if(!x.reserveSourceProof.valid || !x.farLossProof.valid || !x.reserveSourceProof.projected ||
      !x.farLossProof.projected || x.reserveSourceProof.status!=HSBI_CALC_PASS ||
      x.farLossProof.status!=HSBI_CALC_PASS) return r;
   if(!HSBI_IsFiniteNumber(x.reserveEligibleMoney) || !HSBI_IsFiniteNumber(x.farLossIncreaseMoney) ||
      !HSBI_IsFiniteNumber(x.executionSafetyBuffer) || !HSBI_IsFiniteNumber(x.netBigVolume) ||
      !HSBI_IsFiniteNumber(x.farVolume)) { r.status=HSBI_CALC_ERROR; r.details="NONFINITE_CATCH_UP"; return r; }
   if(x.reserveEligibleMoney<=0.0 || x.farLossIncreaseMoney<0.0 || x.executionSafetyBuffer<0.0 ||
      x.netBigVolume<=0.0 || x.farVolume<=0.0) { r.status=HSBI_CALC_REJECT; r.details="INVALID_CATCH_UP_INPUT"; return r; }
   r.reserveGainMoney=x.reserveEligibleMoneyAlreadyAllocated ? x.reserveEligibleMoney :
                      x.reserveEligibleMoney*x.allocationPolicy.reserveShare;
   if(x.allocationPolicy.reserveShare*x.netBigVolume<=x.farVolume) {
      r.status=HSBI_CALC_REJECT; r.details="LOT_CONDITION_FAILED"; return r;
   }
   r.catchUpMargin=r.reserveGainMoney-x.farLossIncreaseMoney-x.executionSafetyBuffer;
   if(r.catchUpMargin<=0.0) { r.status=HSBI_CALC_REJECT; r.details="MONEY_CONDITION_FAILED"; return r; }
   r.status=HSBI_CALC_PASS; r.valid=true; r.reason=HSBI_REASON_OK; r.details="PASS"; return r;
}
string HSBI_ReserveCatchUpDigest(const HSBI_ReserveCatchUpResult &r)
{
   return IntegerToString((int)r.status)+"|"+IntegerToString((int)r.valid)+"|"+
      DoubleToString(r.reserveShare,12)+"|"+DoubleToString(r.reserveEligibleMoney,8)+"|"+
      DoubleToString(r.reserveGainMoney,8)+"|"+DoubleToString(r.farLossIncreaseMoney,8)+"|"+
      DoubleToString(r.executionSafetyBuffer,8)+"|"+DoubleToString(r.catchUpMargin,8)+"|"+
      HSBI_UlongToString(r.sourceDealId)+"|"+HSBI_UlongToString(r.sourceEventId)+"|"+
      HSBI_UlongToString(r.planId)+"|"+HSBI_UlongToString(r.stateRevision);
}
#endif
