// Test-only portability harness: unchanged MQL headers, NOT a MetaEditor result.
#include <cmath>
#include <limits>
#include <string>
#include <sstream>
#include <iomanip>
#include <iostream>
using string=std::string;
using datetime=long;
string LongToString(long x){return std::to_string(x);}
string IntegerToString(int x){return std::to_string(x);}
string StringSubstr(const string&s,int p,int n){return s.substr(p,n);}
string DoubleToString(double x,int digits){std::ostringstream s;s<<std::fixed<<std::setprecision(digits)<<x;return s.str();}
double MathAbs(double x){return std::fabs(x);}
#include "../../Include/Money/HSBI_EconomicLedgerTypes.mqh"
#include "../../Include/Money/HSBI_AllocationLedgerTypes.mqh"
#include "../../Include/Money/HSBI_MoneyState.mqh"
#include "../../Include/Risk/HSBI_RiskGateResult.mqh"
#include "../../Include/Execution/HSBI_TransactionTypes.mqh"
int checks=0,failures=0;
void check(const char*id,int actual,int expected){++checks;bool ok=actual==expected;failures+=!ok;std::cout<<id<<"\t"<<actual<<"\t"<<expected<<"\t"<<(ok?"PASS":"FAIL")<<"\n";}
int main(){
 HSBI_EconomicLedgerRecord a{};a.dealTicket=1;a.orderTicket=2;a.positionIdentifier=3;a.symbol="X";a.magic=7;a.cycleId=1;a.actionId=1;a.eventId=1;a.volume=1;a.price=100;a.profit=50;a.dealNet=50;a.sourceDealKey=HSBI_BuildSourceDealKey(a);a.valid=true;a.role=HSBI_ROLE_BIG_CORE;a.entryType=1;
 auto b=a;check("ECON-CONTROL",HSBI_ClassifyEconomicDuplicate(a,b),1);
 b.profit=60;b.commission=-10;check("P0-01-EQUAL-NET",HSBI_ClassifyEconomicDuplicate(a,b),2);
 b=a;b.price=101;check("PRICE-MISMATCH",HSBI_ClassifyEconomicDuplicate(a,b),2);
 b=a;b.positionIdentifier=99;check("POSITION-MISMATCH",HSBI_ClassifyEconomicDuplicate(a,b),2);
 b=a;b.role=HSBI_ROLE_SMALL_BASE;check("ROLE-MISMATCH",HSBI_ClassifyEconomicDuplicate(a,b),2);
 b=a;b.sourceDealKey="malformed";check("SOURCE-KEY-REBUILD",HSBI_ValidateEconomicRecord(b),0);
 b=a;b.volume=std::numeric_limits<double>::infinity();check("NONFINITE-VOLUME",HSBI_ValidateEconomicRecord(b),0);
 b=a;b.role=static_cast<HSBI_Role>(99);check("INVALID-ECON-ENUM",HSBI_ValidateEconomicRecord(b),0);
 HSBI_AllocationLedgerRecord x{};x.sourceDealKey="S";x.allocationEventId=1;x.sourceDealNet=50;x.finalReserveAllocated=50;x.available=50;x.valid=true;auto y=x;
 check("ALLOC-CONTROL",HSBI_ValidateAllocationConservation(x),1);
 y.finalReserveAllocated=0;y.partialFarAllocated=50;check("P0-02-VECTOR",HSBI_ClassifyAllocationDuplicate(x,y),2);
 y=x;y.finalReserveAllocated=-50;y.partialFarAllocated=100;check("NEGATIVE-BUCKET",HSBI_ValidateAllocationConservation(y),0);
 y=x;y.finalReserveAllocated=0;check("COMMITTED-UNDERALLOCATION-PROPOSED",HSBI_ValidateAllocationConservation(y),0);
 y=x;y.consumed=50;y.available=50;check("P0-03-EXHAUSTED-PROPOSED",HSBI_CanConsumeAmount(y,1),0);
 check("FINAL-RESERVE-ISOLATION",HSBI_CanConsumeBucket(HSBI_BUCKET_FINAL_RESERVE,true),0);
 check("INVALID-BUCKET",HSBI_CanConsumeBucket(static_cast<HSBI_MoneyBucket>(99),false),0);
 HSBI_RiskInput r{};r.snapshotFresh=true;r.projectedMarginLevel=200;r.freeMarginAfter=100;HSBI_RiskLimits l{100,100,0,100,100,100,100,100,100,100};
 check("RISK-CONTROL",HSBI_ValidateRiskInput(r,l).passed,1);
 r.worstCaseLoss=std::numeric_limits<double>::quiet_NaN();check("P0-04-NAN",HSBI_ValidateRiskInput(r,l).passed,0);
 r.worstCaseLoss=0;l.maxWorstCaseLoss=std::numeric_limits<double>::quiet_NaN();r.worstCaseLoss=1000;check("NAN-LIMIT",HSBI_ValidateRiskInput(r,l).passed,0);
 HSBI_MoneyState m{};m.finalReserve=std::numeric_limits<double>::infinity();m.valid=true;m.revision=1;check("P0-05-INF",HSBI_ValidateMoneyState(m),0);
 HSBI_TransactionBarrierInput t{};t.transaction={1,2,HSBI_TX_COMPLETED,1,1,true,true};t.expectedActionId=1;t.lastAppliedEventId=1;t.expectedStateRevision=t.actualStateRevision=1;t.actualDealRead=t.ownershipConfirmed=true;
 check("FILL-CONTROL",HSBI_TransactionBarrierPassed(t),1);
 t.transaction.accumulatedVolume=std::numeric_limits<double>::quiet_NaN();check("P0-07-NAN-FILL",HSBI_TransactionBarrierPassed(t),0);
 t.transaction.accumulatedVolume=1;t.actualStateRevision=0;check("P0-09-REVISION",HSBI_TransactionBarrierPassed(t),0);
 check("P0-10-UNKNOWN-RETRY",HSBI_RetryAllowed(1,1,HSBI_TX_UNKNOWN,true),0);
 std::cout<<"SUMMARY\t"<<checks<<"\t"<<failures<<"\n";
 return failures?1:0;
}
