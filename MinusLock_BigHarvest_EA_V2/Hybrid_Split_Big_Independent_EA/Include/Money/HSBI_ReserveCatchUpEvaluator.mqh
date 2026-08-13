#ifndef HSBI_RESERVE_CATCH_UP_EVALUATOR_MQH
#define HSBI_RESERVE_CATCH_UP_EVALUATOR_MQH
#include "HSBI_ReserveAllocationTypes.mqh"
#include "HSBI_LevelMoneyEvaluator.mqh"
struct HSBI_ReserveCatchUpInput
{
   HSBI_AllocationPolicySnapshot allocationPolicy; double reserveEligibleMoney; bool reserveEligibleMoneyAlreadyAllocated;
   double farLossIncreaseMoney,executionSafetyBuffer,netBigVolume,farVolume; HSBI_Direction farDirection;
   HSBI_BrokerMoneyEvaluationResult reserveSourceProof,farLossProof;
   HSBI_MoneyProofIdentity expectedReserveIdentity,expectedFarIdentity;
   HSBI_ReserveAllocationSource reserveAllocationSource; HSBI_ReserveConsumptionKey consumptionKey,priorConsumptionKey;
   bool hasPriorConsumption; ulong sourceDealId,sourceEventId,planId,stateRevision,snapshotId; bool projected,moneyAvailable,fresh;
};
struct HSBI_ReserveCatchUpResult
{
   HSBI_CalculationStatus status; bool valid,projected; double reserveShare,reserveEligibleMoney,reserveGainMoney;
   double farLossIncreaseMoney,executionSafetyBuffer,catchUpMargin; ulong sourceDealId,sourceEventId,planId,stateRevision;
   bool reserveSourceIdentityValid,farLossSourceIdentityValid,allocationSourceValid,consumptionAllowed,doubleCountFree,runtimeConfirmed;
   string reserveSourceDigest,farLossSourceDigest,allocationSourceDigest,consumptionKeyDigest;
   HSBI_MoneyProofIdentity reserveIdentity,farLossIdentity; HSBI_ReasonCode reason; string details;
};
bool HSBI_ValidateReserveSourceProof(const HSBI_BrokerMoneyEvaluationResult &p,const HSBI_MoneyProofIdentity &expected)
{
   return p.valid&&p.status==HSBI_CALC_PASS&&p.projected&&!p.actual&&p.runtimeConfirmed&&p.netMoney>0.0&&
      HSBI_IsFiniteNumber(p.netMoney)&&HSBI_ValidateMoneyProofIdentity(p.identity)&&HSBI_IsSameMoneyProofIdentity(p.identity,expected)&&
      (p.identity.role==HSBI_ROLE_BIG_CORE||p.identity.role==HSBI_ROLE_BIG_TREND);
}
bool HSBI_ValidateFarLossProof(const HSBI_BrokerMoneyEvaluationResult &p,const HSBI_MoneyProofIdentity &expected)
{
   return p.valid&&p.status==HSBI_CALC_PASS&&p.projected&&!p.actual&&p.runtimeConfirmed&&HSBI_IsFiniteNumber(p.netMoney)&&
      HSBI_ValidateMoneyProofIdentity(p.identity)&&HSBI_IsSameMoneyProofIdentity(p.identity,expected)&&p.identity.role==HSBI_ROLE_FAR;
}
HSBI_ReserveCatchUpResult HSBI_EvaluateReserveCatchUp(const HSBI_ReserveCatchUpInput &x)
{
   HSBI_ReserveCatchUpResult r;ZeroMemory(r);r.status=HSBI_CALC_UNAVAILABLE;r.reason=HSBI_REASON_NOT_INITIALIZED;
   r.details="RESERVE_SOURCE_UNAVAILABLE";r.projected=x.projected;r.reserveShare=x.allocationPolicy.reserveShare;
   r.reserveEligibleMoney=x.reserveEligibleMoney;r.farLossIncreaseMoney=x.farLossIncreaseMoney;r.executionSafetyBuffer=x.executionSafetyBuffer;
   r.sourceDealId=x.sourceDealId;r.sourceEventId=x.sourceEventId;r.planId=x.planId;r.stateRevision=x.stateRevision;
   r.reserveIdentity=x.reserveSourceProof.identity;r.farLossIdentity=x.farLossProof.identity;
   r.reserveSourceIdentityValid=HSBI_ValidateReserveSourceProof(x.reserveSourceProof,x.expectedReserveIdentity);
   r.farLossSourceIdentityValid=HSBI_ValidateFarLossProof(x.farLossProof,x.expectedFarIdentity);
   r.allocationSourceValid=HSBI_ValidateReserveAllocationSource(x.reserveAllocationSource)&&
      x.reserveAllocationSource.allocationPolicyVersion==x.allocationPolicy.policyVersion&&
      x.reserveAllocationSource.sourceDealId==x.reserveSourceProof.identity.sourceDealId;
   r.consumptionAllowed=HSBI_ValidateReserveConsumption(x.consumptionKey,x.planId,x.stateRevision);
   bool duplicate=x.hasPriorConsumption&&HSBI_IsDuplicateReserveConsumption(x.consumptionKey,x.priorConsumptionKey);
   bool conflict=x.hasPriorConsumption&&HSBI_ReserveConsumptionConflict(x.consumptionKey,x.priorConsumptionKey);
   r.doubleCountFree=!duplicate&&!conflict;r.runtimeConfirmed=x.reserveSourceProof.runtimeConfirmed&&x.farLossProof.runtimeConfirmed;
   r.reserveSourceDigest=HSBI_MoneyProofIdentityDigest(x.reserveSourceProof.identity);
   r.farLossSourceDigest=HSBI_MoneyProofIdentityDigest(x.farLossProof.identity);
   r.allocationSourceDigest=HSBI_ReserveAllocationSourceDigest(x.reserveAllocationSource);
   r.consumptionKeyDigest=HSBI_ReserveConsumptionKeyDigest(x.consumptionKey);
   if(!HSBI_ValidateAllocationPolicy(x.allocationPolicy)||!x.moneyAvailable||!x.fresh||x.snapshotId==0||x.planId==0||x.stateRevision==0)return r;
   if(duplicate){r.status=HSBI_CALC_REJECT;r.details="DUPLICATE_CONSUMPTION_NOOP";return r;}
   if(conflict){r.status=HSBI_CALC_REJECT;r.details="CONSUMPTION_CONFLICT";return r;}
   if(!r.reserveSourceIdentityValid){r.status=HSBI_CALC_REJECT;r.details="RESERVE_SOURCE_IDENTITY_MISMATCH";return r;}
   if(!r.farLossSourceIdentityValid){r.status=HSBI_CALC_REJECT;r.details="FAR_LOSS_SOURCE_IDENTITY_MISMATCH";return r;}
   if(!r.allocationSourceValid||!r.consumptionAllowed||!r.doubleCountFree||!r.runtimeConfirmed){r.status=HSBI_CALC_REJECT;r.details="ALLOCATION_OR_CONSUMPTION_INVALID";return r;}
   if(!HSBI_IsFiniteNumber(x.reserveEligibleMoney)||!HSBI_IsFiniteNumber(x.farLossIncreaseMoney)||!HSBI_IsFiniteNumber(x.executionSafetyBuffer)||
      !HSBI_IsFiniteNumber(x.netBigVolume)||!HSBI_IsFiniteNumber(x.farVolume)){r.status=HSBI_CALC_ERROR;r.details="NONFINITE_CATCH_UP";return r;}
   if(x.reserveEligibleMoneyAlreadyAllocated){
      if(x.reserveAllocationSource.reserveAllocated<=0.0||x.reserveAllocationSource.reserveAllocated>x.reserveAllocationSource.allocatableNet||
         x.reserveAllocationSource.alreadyConsumed>0.0){r.status=HSBI_CALC_REJECT;r.details="ALLOCATED_SOURCE_NOT_AVAILABLE";return r;}
      r.reserveGainMoney=x.reserveAllocationSource.reserveAllocated;
   } else {
      if(x.reserveEligibleMoney<=0.0||x.sourceDealId!=x.reserveSourceProof.identity.sourceDealId||x.sourceEventId!=x.reserveSourceProof.identity.sourceEventId){
         r.status=HSBI_CALC_REJECT;r.details="ELIGIBLE_SOURCE_NOT_BOUND";return r;}
      r.reserveGainMoney=x.reserveEligibleMoney*x.allocationPolicy.reserveShare;
   }
   if(x.farLossIncreaseMoney<0.0||x.executionSafetyBuffer<0.0||x.netBigVolume<=0.0||x.farVolume<=0.0){r.status=HSBI_CALC_REJECT;r.details="INVALID_CATCH_UP_INPUT";return r;}
   if(x.allocationPolicy.reserveShare*x.netBigVolume<=x.farVolume){r.status=HSBI_CALC_REJECT;r.details="LOT_CONDITION_FAILED";return r;}
   r.catchUpMargin=r.reserveGainMoney-x.farLossIncreaseMoney-x.executionSafetyBuffer;
   if(r.catchUpMargin<=0.0){r.status=HSBI_CALC_REJECT;r.details="MONEY_CONDITION_FAILED";return r;}
   r.status=HSBI_CALC_PASS;r.valid=true;r.reason=HSBI_REASON_OK;r.details="PASS";return r;
}
string HSBI_ReserveCatchUpDigest(const HSBI_ReserveCatchUpResult &r)
{return IntegerToString((int)r.status)+"|"+IntegerToString((int)r.valid)+"|"+DoubleToString(r.reserveShare,12)+"|"+
   DoubleToString(r.reserveEligibleMoney,8)+"|"+DoubleToString(r.reserveGainMoney,8)+"|"+DoubleToString(r.farLossIncreaseMoney,8)+"|"+
   DoubleToString(r.executionSafetyBuffer,8)+"|"+DoubleToString(r.catchUpMargin,8)+"|"+r.reserveSourceDigest+"|"+r.farLossSourceDigest+"|"+
   r.allocationSourceDigest+"|"+r.consumptionKeyDigest+"|"+IntegerToString((int)r.runtimeConfirmed)+"|"+IntegerToString((int)r.doubleCountFree);}
#endif
