#ifndef HSBI_ALLOCATION_POLICY_TYPES_MQH
#define HSBI_ALLOCATION_POLICY_TYPES_MQH
#include "HSBI_BrokerMoneyTypes.mqh"
#include "../Core/HSBI_Identifiers.mqh"
struct HSBI_AllocationPolicySnapshot
{
   double reserveShare;
   double partialFarShare;
   double transitionShare;
   double carryShare;
   ulong policyVersion;
   ulong snapshotId;
   bool valid;
   bool fresh;
};
bool HSBI_ValidateAllocationPolicy(const HSBI_AllocationPolicySnapshot &p)
{
   if(!p.valid || !p.fresh || p.policyVersion==0 || p.snapshotId==0) return false;
   if(!HSBI_IsFiniteNumber(p.reserveShare) || !HSBI_IsFiniteNumber(p.partialFarShare) ||
      !HSBI_IsFiniteNumber(p.transitionShare) || !HSBI_IsFiniteNumber(p.carryShare)) return false;
   if(p.reserveShare<0.0 || p.reserveShare>1.0 || p.partialFarShare<0.0 ||
      p.transitionShare<0.0 || p.carryShare<0.0) return false;
   return p.reserveShare+p.partialFarShare+p.transitionShare+p.carryShare<=1.0+1e-12;
}
string HSBI_AllocationPolicyDigest(const HSBI_AllocationPolicySnapshot &p)
{
   return DoubleToString(p.reserveShare,12)+"|"+DoubleToString(p.partialFarShare,12)+"|"+
          DoubleToString(p.transitionShare,12)+"|"+DoubleToString(p.carryShare,12)+"|"+
          HSBI_UlongToString(p.policyVersion)+"|"+HSBI_UlongToString(p.snapshotId)+"|"+
          IntegerToString((int)p.valid)+"|"+IntegerToString((int)p.fresh);
}
#endif
