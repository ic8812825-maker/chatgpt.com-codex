#ifndef HSBI_ROLES_MQH
#define HSBI_ROLES_MQH
#include "HSBI_Identifiers.mqh"
struct HSBI_PositionDescriptor{HSBI_Identity identity;ulong ticket;ulong identifier;HSBI_Role role;HSBI_Direction direction;double requestedVolume;double actualVolume;double openPrice;double currentClosePrice;HSBI_Status status;ulong creationActionId;ulong lastEventId;};
bool HSBI_IsKnownRole(const HSBI_Role role){return role>=HSBI_ROLE_INITIAL_BUY&&role<=HSBI_ROLE_NEW_FAR;}
#endif