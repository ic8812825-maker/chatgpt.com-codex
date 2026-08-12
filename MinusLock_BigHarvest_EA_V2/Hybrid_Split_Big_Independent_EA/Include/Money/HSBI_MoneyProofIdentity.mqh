#ifndef HSBI_MONEY_PROOF_IDENTITY_MQH
#define HSBI_MONEY_PROOF_IDENTITY_MQH
#include "../Core/HSBI_Identifiers.mqh"
struct HSBI_MoneyProofIdentity
{
   long accountLogin; string symbol; long magic; ulong cycleId; ulong positionIdentifier;
   HSBI_Role role; HSBI_Direction direction; ulong sourceDealId; ulong sourceEventId;
   ulong snapshotId; ulong planId; ulong stateRevision;
};
bool HSBI_ValidateMoneyProofIdentity(const HSBI_MoneyProofIdentity &x)
{
   return x.accountLogin>0&&x.symbol!=""&&x.magic!=0&&x.cycleId>0&&x.positionIdentifier>0&&
      x.role!=HSBI_ROLE_NONE&&x.direction!=HSBI_DIRECTION_NONE&&x.sourceDealId>0&&x.sourceEventId>0&&
      x.snapshotId>0&&x.planId>0&&x.stateRevision>0;
}
bool HSBI_IsSameMoneyProofIdentity(const HSBI_MoneyProofIdentity &a,const HSBI_MoneyProofIdentity &b)
{
   return a.accountLogin==b.accountLogin&&a.symbol==b.symbol&&a.magic==b.magic&&a.cycleId==b.cycleId&&
      a.positionIdentifier==b.positionIdentifier&&a.role==b.role&&a.direction==b.direction&&
      a.sourceDealId==b.sourceDealId&&a.sourceEventId==b.sourceEventId&&a.snapshotId==b.snapshotId&&
      a.planId==b.planId&&a.stateRevision==b.stateRevision;
}
string HSBI_MoneyProofIdentityDigest(const HSBI_MoneyProofIdentity &x)
{
   return LongToString(x.accountLogin)+"|"+x.symbol+"|"+LongToString(x.magic)+"|"+HSBI_UlongToString(x.cycleId)+"|"+
      HSBI_UlongToString(x.positionIdentifier)+"|"+IntegerToString((int)x.role)+"|"+IntegerToString((int)x.direction)+"|"+
      HSBI_UlongToString(x.sourceDealId)+"|"+HSBI_UlongToString(x.sourceEventId)+"|"+HSBI_UlongToString(x.snapshotId)+"|"+
      HSBI_UlongToString(x.planId)+"|"+HSBI_UlongToString(x.stateRevision);
}
#endif
