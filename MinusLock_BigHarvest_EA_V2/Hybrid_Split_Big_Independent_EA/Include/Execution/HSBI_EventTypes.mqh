#ifndef HSBI_EVENT_TYPES_MQH
#define HSBI_EVENT_TYPES_MQH
#include "../Core/HSBI_Enums.mqh"
struct HSBI_EventRecord{ulong eventId;ulong actionId;HSBI_EventType eventType;ulong orderTicket;ulong dealTicket;ulong positionIdentifier;double actualVolume;double actualPrice;datetime timestamp;HSBI_Status status;};
bool HSBI_ValidateEventRecord(const HSBI_EventRecord &e){return e.eventId>0&&e.actionId>0&&e.eventType!=HSBI_EVENT_NONE&&e.actualVolume>=0.0;}
#endif