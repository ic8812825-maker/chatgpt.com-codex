#property strict
#property script_show_inputs
// Offline predicate checks only. No trade API or order submission.
#include "../../Include/Money/HSBI_EconomicLedgerTypes.mqh"
#include "../../Include/Money/HSBI_AllocationLedgerTypes.mqh"
#include "../../Include/Execution/HSBI_TransactionTypes.mqh"
int failures=0;
void Check(const string id,const bool actual,const bool expected)
{Print("HSBI_CLOSE|",id,"|actual=",actual,"|expected=",expected,"|",actual==expected?"PASS":"FAIL");if(actual!=expected)failures++;}
void OnStart()
{
 HSBI_EconomicLedgerRecord a;ZeroMemory(a);a.sourceDealKey="FIXTURE";a.dealNet=50;a.profit=50;a.volume=1;a.price=100;
 HSBI_EconomicLedgerRecord b=a;b.profit=60;b.commission=-10;
 Check("P0-01",HSBI_SameEconomicRecord(a,b),false);
 HSBI_AllocationLedgerRecord x;ZeroMemory(x);x.sourceDealKey="FIXTURE";x.allocationEventId=1;x.finalReserveAllocated=50;
 HSBI_AllocationLedgerRecord y=x;y.finalReserveAllocated=0;y.partialFarAllocated=50;
 Check("P0-02",HSBI_ClassifyAllocationDuplicate(x,y)==2,true);
 Check("P0-10",HSBI_RetryAllowed(1,1,HSBI_TX_UNKNOWN,true),false);
 Print("HSBI_CLOSE|SUMMARY|failures=",failures,"|NATIVE_PREDICATES_ONLY|NO_BROKER_DISPATCH");
}
