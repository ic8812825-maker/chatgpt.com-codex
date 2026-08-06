#ifndef HSBI_INVARIANTS_MQH
#define HSBI_INVARIANTS_MQH
#include "HSBI_Context.mqh"
#include "HSBI_StateValidator.mqh"
HSBI_ValidationResult HSBI_ExactlyOneFarOrZero(const HSBI_RecoveryContext &c){int n=HSBI_CountFarRoles(c.far,c.bigCore,c.bigTrend,c.smallBase);return HSBI_Result(n<=1,n<=1?HSBI_REASON_OK:HSBI_REASON_DUPLICATE_FAR,"HSBI-ID-010",IntegerToString(n));}
HSBI_ValidationResult HSBI_NoDualTail(const HSBI_RecoveryContext &c){return HSBI_ExactlyOneFarOrZero(c);}
HSBI_ValidationResult HSBI_NoUnknownRole(const HSBI_PositionDescriptor &p){return HSBI_Result(HSBI_IsKnownRole(p.role)||p.role==HSBI_ROLE_NONE,HSBI_IsKnownRole(p.role)||p.role==HSBI_ROLE_NONE?HSBI_REASON_OK:HSBI_REASON_UNKNOWN_ROLE,"HSBI-ID-010","");}
HSBI_ValidationResult HSBI_ContextIdentityComplete(const HSBI_RecoveryContext &c){bool ok=c.accountLogin>0&&c.symbol!=""&&c.magic!=0;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_INVALID_IDENTITY,"HSBI-ID-010","");}
HSBI_ValidationResult HSBI_StateRevisionMonotonic(const ulong before,const ulong after){bool ok=after>=before;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_INTERNAL_INVARIANT_FAILED,"HSBI-FSM-002","");}
HSBI_ValidationResult HSBI_NoPendingActionConflict(const HSBI_RecoveryContext &c){bool ok=!(c.pendingActionId>0&&c.currentState==HSBI_STATE_CYCLE_CLOSED);return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_PENDING_ACTION,"HSBI-TX-006","");}
HSBI_ValidationResult HSBI_NoFinalReserveForPartialFar(const HSBI_MoneyBucket source){bool ok=source!=HSBI_BUCKET_FINAL_RESERVE;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_FINAL_RESERVE_FOR_PARTIAL_FAR,"HSBI-PF-001","");}
HSBI_ValidationResult HSBI_AllocationConservation(const double allocated,const double available){bool ok=allocated<=available+0.0000001;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_LEDGER_CONSERVATION_FAILED,"HSBI-MONEY-014","");}
HSBI_ValidationResult HSBI_RealTradingForbiddenAtHSB1(){return HSBI_Result(!HSBI_REAL_TRADING_ALLOWED&&!HSBI_TRADING_IMPLEMENTED,HSBI_REASON_OK,"HSBI-GEN-030","");}
#endif