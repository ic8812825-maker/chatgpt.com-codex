#ifndef HSBI_IDENTIFIERS_MQH
#define HSBI_IDENTIFIERS_MQH
#include "HSBI_Enums.mqh"
#include "HSBI_ReasonCodes.mqh"
struct HSBI_Identity{long accountLogin;string symbol;long magic;ulong cycleId;ulong positionIdentifier;HSBI_Role role;};
bool HSBI_IsValidIdentity(const HSBI_Identity &x){return x.accountLogin>0 && x.symbol!="" && x.magic!=0 && x.cycleId>0 && x.role!=HSBI_ROLE_NONE;}
bool HSBI_SameCycle(const HSBI_Identity &a,const HSBI_Identity &b){return a.accountLogin==b.accountLogin && a.symbol==b.symbol && a.magic==b.magic && a.cycleId==b.cycleId;}
bool HSBI_SamePositionOwner(const HSBI_Identity &a,const HSBI_Identity &b){return HSBI_SameCycle(a,b)&&a.positionIdentifier==b.positionIdentifier&&a.role==b.role;}
bool HSBI_SameSymbolScope(const HSBI_Identity &a,const HSBI_Identity &b){return a.accountLogin==b.accountLogin&&a.symbol==b.symbol&&a.magic==b.magic;}
string HSBI_UlongToString(const ulong value)
{
   if(value==0)return "0";
   ulong remaining=value;
   string result="";
   while(remaining>0)
   {
      const int digit=(int)(remaining%10);
      result=StringSubstr("0123456789",digit,1)+result;
      remaining/=10;
   }
   return result;
}
string HSBI_SerializeIdentity(const HSBI_Identity &x){return LongToString(x.accountLogin)+"|"+x.symbol+"|"+LongToString(x.magic)+"|"+HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.positionIdentifier)+"|"+IntegerToString((int)x.role);}
#endif
