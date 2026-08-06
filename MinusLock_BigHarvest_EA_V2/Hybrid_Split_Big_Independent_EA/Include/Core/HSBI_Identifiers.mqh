#ifndef HSBI_IDENTIFIERS_MQH
#define HSBI_IDENTIFIERS_MQH
#include "HSBI_Enums.mqh"
#include "HSBI_ReasonCodes.mqh"
struct HSBI_Identity{long accountLogin;string symbol;long magic;ulong cycleId;ulong positionIdentifier;HSBI_Role role;};
bool HSBI_IsValidIdentity(const HSBI_Identity &x){return x.accountLogin>0 && x.symbol!="" && x.magic!=0 && x.cycleId>0 && x.role!=HSBI_ROLE_NONE;}
bool HSBI_SameCycle(const HSBI_Identity &a,const HSBI_Identity &b){return a.accountLogin==b.accountLogin && a.symbol==b.symbol && a.magic==b.magic && a.cycleId==b.cycleId;}
bool HSBI_SamePositionOwner(const HSBI_Identity &a,const HSBI_Identity &b){return HSBI_SameCycle(a,b)&&a.positionIdentifier==b.positionIdentifier&&a.role==b.role;}
bool HSBI_SameSymbolScope(const HSBI_Identity &a,const HSBI_Identity &b){return a.accountLogin==b.accountLogin&&a.symbol==b.symbol&&a.magic==b.magic;}
string HSBI_SerializeIdentity(const HSBI_Identity &x){return LongToString(x.accountLogin)+"|"+x.symbol+"|"+LongToString(x.magic)+"|"+IntegerToString((int)x.cycleId)+"|"+IntegerToString((int)x.positionIdentifier)+"|"+IntegerToString((int)x.role);}
#endif