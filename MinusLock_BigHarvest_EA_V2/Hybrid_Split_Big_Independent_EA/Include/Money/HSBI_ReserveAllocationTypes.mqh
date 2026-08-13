#ifndef HSBI_RESERVE_ALLOCATION_TYPES_MQH
#define HSBI_RESERVE_ALLOCATION_TYPES_MQH
#include "HSBI_AllocationPolicyTypes.mqh"
struct HSBI_ReserveAllocationSource
{
   string sourceDealKey,sourceAllocationKey; ulong sourceDealId,allocationEventId,allocationPolicyVersion;
   double allocatableNet,reserveAllocated,partialFarAllocated,transitionAllocated,carryAllocated,residualAllocated,alreadyConsumed;
   bool allocationConfirmed,sourceReconciled,valid;
};
struct HSBI_ReserveConsumptionKey
{
   string sourceDealKey,sourceAllocationKey; ulong planId,stateRevision,consumptionEventId; string consumer;
};
enum HSBI_ReserveConsumptionStatus { HSBI_CONSUMPTION_ALLOWED,HSBI_CONSUMPTION_DUPLICATE_NOOP,HSBI_CONSUMPTION_CONFLICT,HSBI_CONSUMPTION_REJECTED };
bool HSBI_ValidateReserveAllocationSource(const HSBI_ReserveAllocationSource &x)
{
   if(!x.valid||!x.allocationConfirmed||!x.sourceReconciled||x.sourceDealKey==""||x.sourceAllocationKey==""||
      x.sourceDealId==0||x.allocationEventId==0||x.allocationPolicyVersion==0||x.allocatableNet<=0.0)return false;
   if(!HSBI_IsFiniteNumber(x.allocatableNet)||!HSBI_IsFiniteNumber(x.reserveAllocated)||!HSBI_IsFiniteNumber(x.partialFarAllocated)||
      !HSBI_IsFiniteNumber(x.transitionAllocated)||!HSBI_IsFiniteNumber(x.carryAllocated)||!HSBI_IsFiniteNumber(x.residualAllocated)||
      !HSBI_IsFiniteNumber(x.alreadyConsumed)||x.reserveAllocated<0.0||x.partialFarAllocated<0.0||x.transitionAllocated<0.0||
      x.carryAllocated<0.0||x.residualAllocated<0.0||x.alreadyConsumed<0.0)return false;
   return x.reserveAllocated+x.partialFarAllocated+x.transitionAllocated+x.carryAllocated+x.residualAllocated+x.alreadyConsumed<=x.allocatableNet+1e-10;
}
bool HSBI_ValidateReserveConsumption(const HSBI_ReserveConsumptionKey &x,const ulong planId,const ulong revision)
{return x.sourceDealKey!=""&&x.sourceAllocationKey!=""&&x.consumptionEventId>0&&x.consumer!=""&&x.planId==planId&&x.stateRevision==revision;}
bool HSBI_IsDuplicateReserveConsumption(const HSBI_ReserveConsumptionKey &a,const HSBI_ReserveConsumptionKey &b)
{return a.sourceDealKey==b.sourceDealKey&&a.sourceAllocationKey==b.sourceAllocationKey&&a.planId==b.planId&&a.stateRevision==b.stateRevision&&a.consumptionEventId==b.consumptionEventId&&a.consumer==b.consumer;}
bool HSBI_ReserveConsumptionConflict(const HSBI_ReserveConsumptionKey &a,const HSBI_ReserveConsumptionKey &b)
{return (a.sourceAllocationKey==b.sourceAllocationKey||a.consumptionEventId==b.consumptionEventId)&&!HSBI_IsDuplicateReserveConsumption(a,b);}
string HSBI_ReserveAllocationSourceDigest(const HSBI_ReserveAllocationSource &x)
{return x.sourceDealKey+"|"+x.sourceAllocationKey+"|"+HSBI_UlongToString(x.sourceDealId)+"|"+HSBI_UlongToString(x.allocationEventId)+"|"+HSBI_UlongToString(x.allocationPolicyVersion)+"|"+DoubleToString(x.allocatableNet,8)+"|"+DoubleToString(x.reserveAllocated,8)+"|"+DoubleToString(x.partialFarAllocated,8)+"|"+DoubleToString(x.transitionAllocated,8)+"|"+DoubleToString(x.carryAllocated,8)+"|"+DoubleToString(x.residualAllocated,8)+"|"+DoubleToString(x.alreadyConsumed,8);}
string HSBI_ReserveConsumptionKeyDigest(const HSBI_ReserveConsumptionKey &x)
{return x.sourceDealKey+"|"+x.sourceAllocationKey+"|"+HSBI_UlongToString(x.planId)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+HSBI_UlongToString(x.consumptionEventId)+"|"+x.consumer;}
#endif
