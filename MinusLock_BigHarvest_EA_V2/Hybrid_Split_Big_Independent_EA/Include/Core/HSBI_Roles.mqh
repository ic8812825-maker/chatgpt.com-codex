#ifndef HSBI_ROLES_MQH
#define HSBI_ROLES_MQH
#include "HSBI_Identifiers.mqh"
#include "HSBI_Types.mqh"
struct HSBI_PositionDescriptor{HSBI_Identity identity;ulong ticket;ulong identifier;HSBI_Role role;HSBI_Direction direction;double requestedVolume;double actualVolume;double openPrice;double currentClosePrice;HSBI_Status status;ulong creationActionId;ulong lastEventId;};
bool HSBI_IsKnownRole(const HSBI_Role role){return role>=HSBI_ROLE_INITIAL_BUY&&role<=HSBI_ROLE_NEW_FAR;}
HSBI_ValidationResult HSBI_ValidatePositionDescriptor(const HSBI_PositionDescriptor &p){if(!HSBI_IsKnownRole(p.role))return HSBI_Result(false,HSBI_REASON_UNKNOWN_ROLE,"HSBI-ID-010","unknown role");if(p.actualVolume<0.0||p.requestedVolume<0.0)return HSBI_Result(false,HSBI_REASON_INVALID_VOLUME,"HSBI-ID-010","negative volume");if(p.ticket>0&&p.identifier==0)return HSBI_Result(false,HSBI_REASON_INVALID_IDENTITY,"HSBI-ID-010","ticket without identifier");return HSBI_Result(true,HSBI_REASON_OK,"HSBI-ID-010","");}
bool HSBI_CanPromoteToFar(const HSBI_PositionDescriptor &p,const ulong originalBigCoreIdentifier){return p.role==HSBI_ROLE_BIG_CORE&&p.identifier==originalBigCoreIdentifier&&p.actualVolume>0.0;}
bool HSBI_ValidateRoleTransition(const HSBI_Role from,const HSBI_Role to){if(to==HSBI_ROLE_FAR)return from==HSBI_ROLE_BIG_CORE||from==HSBI_ROLE_NEW_FAR;return from==to;}
int HSBI_CountFarRoles(const HSBI_PositionDescriptor &a,const HSBI_PositionDescriptor &b,const HSBI_PositionDescriptor &c,const HSBI_PositionDescriptor &d){int n=0;if(a.role==HSBI_ROLE_FAR)n++;if(b.role==HSBI_ROLE_FAR)n++;if(c.role==HSBI_ROLE_FAR)n++;if(d.role==HSBI_ROLE_FAR)n++;return n;}
#endif