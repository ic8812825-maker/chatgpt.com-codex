#ifndef HSBI_EVENT_TYPES_MQH
#define HSBI_EVENT_TYPES_MQH
#include "../Core/HSBI_Enums.mqh"
#include "../Core/HSBI_Identifiers.mqh"
struct HSBI_EventRecord{ulong eventId;ulong actionId;HSBI_EventType eventType;ulong orderTicket;ulong dealTicket;ulong positionIdentifier;double actualVolume;double actualPrice;datetime timestamp;HSBI_Status status;};
bool HSBI_ValidateEventRecord(const HSBI_EventRecord &e){return e.eventId>0&&e.actionId>0&&e.eventType!=HSBI_EVENT_NONE&&e.actualVolume>=0.0;}
string HSBI_SerializeEventIds(const HSBI_EventRecord &e){return HSBI_UlongToString(e.eventId)+"|"+HSBI_UlongToString(e.actionId)+"|"+HSBI_UlongToString(e.orderTicket)+"|"+HSBI_UlongToString(e.dealTicket)+"|"+HSBI_UlongToString(e.positionIdentifier);}
#endif
