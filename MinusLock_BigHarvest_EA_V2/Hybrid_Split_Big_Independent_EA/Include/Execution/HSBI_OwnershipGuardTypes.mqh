#ifndef HSBI_OWNERSHIP_GUARD_TYPES_MQH
#define HSBI_OWNERSHIP_GUARD_TYPES_MQH
#include "../Core/HSBI_Identifiers.mqh"
#include "../Core/HSBI_Roles.mqh"
#include "../Core/HSBI_ReasonCodes.mqh"
struct HSBI_OwnershipGuardInput{HSBI_Identity expectedIdentity;HSBI_Identity actualIdentity;ulong expectedTicket;ulong actualTicket;HSBI_Role expectedRole;HSBI_Role actualRole;HSBI_Direction expectedDirection;HSBI_Direction actualDirection;double expectedVolume;double actualVolume;ulong expectedStateRevision;ulong actualStateRevision;ulong planId;ulong actionId;};
struct HSBI_OwnershipGuardResult{bool allowed;HSBI_ReasonCode reason;ulong mismatchMask;bool requiresReconciliation;};
HSBI_OwnershipGuardResult HSBI_EvaluateOwnership(const HSBI_OwnershipGuardInput &x){HSBI_OwnershipGuardResult r;r.allowed=true;r.reason=HSBI_REASON_OK;r.mismatchMask=0;r.requiresReconciliation=false;if(!HSBI_SamePositionOwner(x.expectedIdentity,x.actualIdentity)){r.mismatchMask|=1;}if(x.expectedRole!=x.actualRole)r.mismatchMask|=2;if(x.expectedDirection!=x.actualDirection)r.mismatchMask|=4;if(MathAbs(x.expectedVolume-x.actualVolume)>0.0000001)r.mismatchMask|=8;if(x.expectedStateRevision!=x.actualStateRevision)r.mismatchMask|=16;if(x.planId==0||x.actionId==0)r.mismatchMask|=32;if(x.expectedTicket==0||x.actualTicket!=x.expectedTicket)r.mismatchMask|=64;if(r.mismatchMask!=0){r.allowed=false;r.reason=HSBI_REASON_INVALID_IDENTITY;r.requiresReconciliation=true;}return r;}
bool HSBI_TicketMatchesObservation(const HSBI_PositionDescriptor &expected,const HSBI_PositionDescriptor &actual)
{
   return expected.ticket>0&&actual.ticket==expected.ticket&&HSBI_SamePositionOwner(expected.identity,actual.identity)&&expected.identifier==actual.identifier&&expected.role==actual.role;
}
bool HSBI_IsActualBigCoreResidual(const HSBI_PositionDescriptor &position,const ulong originalIdentifier)
{
   return position.role==HSBI_ROLE_BIG_CORE&&position.identifier==originalIdentifier&&position.identity.positionIdentifier==originalIdentifier&&position.actualVolume>0.0;
}
#endif
