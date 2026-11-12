// TEST-ONLY unapplied additive API candidate. No provider/registry/persistence implementation.
// Captured finite binary64 equality with +/-0 equivalent; not settled-money arithmetic.
#ifndef HSBI_DG01_IDENTITY_CANDIDATE
#define HSBI_DG01_IDENTITY_CANDIDATE
#include "../../Include/Money/HSBI_EconomicLedgerTypes.mqh"
enum HSBI_EconomicIdentityStatusV2 { HSBI_ECON_V2_NEW=0,HSBI_ECON_V2_NO_OP=1,HSBI_ECON_V2_CONFLICT=2,HSBI_ECON_V2_REJECT=3,HSBI_ECON_V2_UNAVAILABLE=4 };
struct HSBI_EconomicLedgerRecordV2
{
 ulong schemaVersion;string broker,server;long accountLogin;string symbol;long magic;
 ulong cycleId,dealTicket,orderTicket,positionIdentifier,actionId,eventId;HSBI_Role role;
 int entryType,dealType;long timestampMsc;double volume,price,profit,swap,commission,fee,dealNet;
 string currency;int precision;bool sourcePlanApplicable;ulong sourcePlan;bool sourcePolicyApplicable;ulong sourcePolicyVersion;
 // Envelope metadata: incomplete facts must not default to known zero/false.
 ulong knownFieldsMask;
};
HSBI_EconomicIdentityStatusV2 HSBI_ValidateEconomicRecordV2(const HSBI_EconomicLedgerRecordV2 &x)
{
 if(x.knownFieldsMask!=536870911)return HSBI_ECON_V2_UNAVAILABLE; // all29 immutable facts known
 if(x.schemaVersion!=1)return HSBI_ECON_V2_UNAVAILABLE;
 if(x.broker==""||x.server==""||x.accountLogin<=0||x.symbol==""||x.magic==0||x.cycleId==0||x.dealTicket==0||x.orderTicket==0||x.positionIdentifier==0||x.actionId==0||x.eventId==0||x.timestampMsc<=0)return HSBI_ECON_V2_REJECT;
 if(x.role<HSBI_ROLE_INITIAL_BUY||x.role>HSBI_ROLE_NEW_FAR||x.entryType<0||x.entryType>3||x.dealType<0||x.dealType>1)return HSBI_ECON_V2_REJECT;
 if(!MathIsValidNumber(x.volume)||!MathIsValidNumber(x.price)||!MathIsValidNumber(x.profit)||!MathIsValidNumber(x.swap)||!MathIsValidNumber(x.commission)||!MathIsValidNumber(x.fee)||!MathIsValidNumber(x.dealNet)||x.volume<=0||x.price<=0)return HSBI_ECON_V2_REJECT;
 if(x.currency==""||x.precision<0)return HSBI_ECON_V2_REJECT;
 if(x.precision>8)return HSBI_ECON_V2_UNAVAILABLE; // proposed supported profile, not universal broker limit
 if((x.sourcePlanApplicable&&x.sourcePlan==0)||(!x.sourcePlanApplicable&&x.sourcePlan!=0)||(x.sourcePolicyApplicable&&x.sourcePolicyVersion==0)||(!x.sourcePolicyApplicable&&x.sourcePolicyVersion!=0))return HSBI_ECON_V2_REJECT;
 return HSBI_ECON_V2_NO_OP;
}
bool HSBI_SameEconomicSourceKeyV2(const HSBI_EconomicLedgerRecordV2 &a,const HSBI_EconomicLedgerRecordV2 &b)
{return a.broker==b.broker&&a.server==b.server&&a.accountLogin==b.accountLogin&&a.dealTicket==b.dealTicket;}
bool HSBI_SameEconomicPayloadV2(const HSBI_EconomicLedgerRecordV2 &a,const HSBI_EconomicLedgerRecordV2 &b)
{
 return a.schemaVersion==b.schemaVersion&&HSBI_SameEconomicSourceKeyV2(a,b)&&a.symbol==b.symbol&&a.magic==b.magic&&a.cycleId==b.cycleId&&a.orderTicket==b.orderTicket&&a.positionIdentifier==b.positionIdentifier&&a.actionId==b.actionId&&a.eventId==b.eventId&&a.role==b.role&&a.entryType==b.entryType&&a.dealType==b.dealType&&a.timestampMsc==b.timestampMsc&&a.volume==b.volume&&a.price==b.price&&a.profit==b.profit&&a.swap==b.swap&&a.commission==b.commission&&a.fee==b.fee&&a.dealNet==b.dealNet&&a.currency==b.currency&&a.precision==b.precision&&a.sourcePlanApplicable==b.sourcePlanApplicable&&a.sourcePlan==b.sourcePlan&&a.sourcePolicyApplicable==b.sourcePolicyApplicable&&a.sourcePolicyVersion==b.sourcePolicyVersion;
}
HSBI_EconomicIdentityStatusV2 HSBI_ClassifyEconomicIdentityV2(const HSBI_EconomicLedgerRecordV2 &incoming,const HSBI_EconomicLedgerRecordV2 &authority,const bool independentSourceConfirmed,const HSBI_EconomicLedgerRecordV2 &records[],const bool registryComplete)
{
 HSBI_EconomicIdentityStatusV2 s=HSBI_ValidateEconomicRecordV2(incoming);if(s!=HSBI_ECON_V2_NO_OP)return s;
 if(!independentSourceConfirmed||!registryComplete)return HSBI_ECON_V2_UNAVAILABLE;
 s=HSBI_ValidateEconomicRecordV2(authority);if(s!=HSBI_ECON_V2_NO_OP)return s;
 if(!HSBI_SameEconomicSourceKeyV2(incoming,authority))return HSBI_ECON_V2_UNAVAILABLE;
 if(!HSBI_SameEconomicPayloadV2(incoming,authority))return HSBI_ECON_V2_CONFLICT;
 int found=-1;
 for(int i=0;i<ArraySize(records);i++){
  s=HSBI_ValidateEconomicRecordV2(records[i]);if(s!=HSBI_ECON_V2_NO_OP)return s;
  for(int j=0;j<i;j++)if(HSBI_SameEconomicSourceKeyV2(records[i],records[j]))return HSBI_ECON_V2_CONFLICT;
  if(HSBI_SameEconomicSourceKeyV2(incoming,records[i]))found=i;
 }
 if(found<0)return HSBI_ECON_V2_NEW; // identity observation only, never funding
 return HSBI_SameEconomicPayloadV2(incoming,records[found])?HSBI_ECON_V2_NO_OP:HSBI_ECON_V2_CONFLICT;
}
#endif
