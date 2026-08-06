#ifndef HSBI_ALLOCATION_LEDGER_TYPES_MQH
#define HSBI_ALLOCATION_LEDGER_TYPES_MQH
#include "../Core/HSBI_Enums.mqh"
#include "../Core/HSBI_ReasonCodes.mqh"
struct HSBI_AllocationLedgerRecord{string sourceDealKey;ulong allocationEventId;double sourceDealNet;double finalReserveAllocated;double partialFarAllocated;double transitionAllocated;double carryAllocated;double residual;double consumed;double available;HSBI_Status status;bool valid;};
double HSBI_AllocatedTotal(const HSBI_AllocationLedgerRecord &r){return r.finalReserveAllocated+r.partialFarAllocated+r.transitionAllocated+r.carryAllocated+r.residual;}
bool HSBI_ValidateAllocationConservation(const HSBI_AllocationLedgerRecord &r){if(!r.valid||r.sourceDealKey=="")return false;if(r.sourceDealNet<0.0)return HSBI_AllocatedTotal(r)<=0.0000001;return HSBI_AllocatedTotal(r)<=r.sourceDealNet+0.0000001&&r.consumed<=r.available+0.0000001;}
int HSBI_ClassifyAllocationDuplicate(const HSBI_AllocationLedgerRecord &a,const HSBI_AllocationLedgerRecord &b){if(a.sourceDealKey!=b.sourceDealKey||a.allocationEventId!=b.allocationEventId)return 0;bool same=MathAbs(HSBI_AllocatedTotal(a)-HSBI_AllocatedTotal(b))<0.0000001;return same?1:2;}
bool HSBI_CanConsumeBucket(const HSBI_MoneyBucket bucket,const bool partialFarConsumer){if(partialFarConsumer&&bucket==HSBI_BUCKET_FINAL_RESERVE)return false;return true;}
bool HSBI_CanConsumeAmount(const HSBI_AllocationLedgerRecord &r,const double amount){return amount>=0.0&&amount<=r.available+0.0000001;}
#endif