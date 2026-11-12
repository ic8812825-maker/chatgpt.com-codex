// Non-trading Script. No handlers for ticks/trades, account/provider calls or persistence writes.
#property strict
#include "../../Include/Money/HSBI_EconomicLedgerTypes.mqh"
#include "../../Include/Money/HSBI_AllocationLedgerTypes.mqh"
#include "../../Include/Money/HSBI_MoneyState.mqh"
#include "../../Include/Risk/HSBI_RiskGateResult.mqh"
#include "../../Include/Execution/HSBI_TransactionTypes.mqh"
int failures=0;
void Assert(const string id,const bool ok){Print("AUDIT02|",id,"|",ok?"PASS":"FAIL");if(!ok)failures++;}
void OnStart()
{
 HSBI_EconomicLedgerRecord a,b;ZeroMemory(a);a.sourceDealKey="TEST|101";a.volume=1;a.price=100;a.profit=50;a.dealNet=50;b=a;
 Assert("ECON_EXACT",HSBI_ClassifyEconomicDuplicate(a,b)==1);
 b.profit=70;b.commission=-20;Assert("ECON_COMPONENT_CONFLICT",HSBI_ClassifyEconomicDuplicate(a,b)==2);
 HSBI_AllocationLedgerRecord x,y;ZeroMemory(x);x.sourceDealKey="TEST|101";x.allocationEventId=1;x.sourceDealNet=50;x.finalReserveAllocated=50;x.available=50;x.valid=true;y=x;
 Assert("ALLOC_VALID",HSBI_ValidateAllocationConservation(x));y.finalReserveAllocated=0;y.partialFarAllocated=50;Assert("ALLOC_VECTOR_CONFLICT",HSBI_ClassifyAllocationDuplicate(x,y)==2);
 y=x;y.finalReserveAllocated=-50;y.partialFarAllocated=100;Assert("NEGATIVE_BUCKET_REJECT",!HSBI_ValidateAllocationConservation(y));
 HSBI_MoneyState s;ZeroMemory(s);s.finalReserve=50;s.revision=1;s.valid=true;Assert("MONEY_VALID",HSBI_ValidateMoneyState(s));s.finalReserve=-1;Assert("NEGATIVE_MONEY_REJECT",!HSBI_ValidateMoneyState(s));
 Print("AUDIT02|FAILURES|",failures);
}
