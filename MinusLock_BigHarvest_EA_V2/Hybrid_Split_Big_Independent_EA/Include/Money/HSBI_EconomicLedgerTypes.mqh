#ifndef HSBI_ECONOMIC_LEDGER_TYPES_MQH
#define HSBI_ECONOMIC_LEDGER_TYPES_MQH
#include "../Core/HSBI_Enums.mqh"
#include "../Core/HSBI_Identifiers.mqh"
#include "../Core/HSBI_ReasonCodes.mqh"
struct HSBI_EconomicLedgerRecord{ulong dealTicket;ulong orderTicket;ulong positionIdentifier;string symbol;long magic;ulong cycleId;ulong actionId;ulong eventId;HSBI_Role role;int entryType;double volume;double price;double profit;double swap;double commission;double fee;double dealNet;datetime timestamp;string sourceDealKey;bool valid;};
string HSBI_BuildSourceDealKey(const HSBI_EconomicLedgerRecord &r){return r.symbol+"|"+LongToString(r.magic)+"|"+HSBI_UlongToString(r.cycleId)+"|"+HSBI_UlongToString(r.dealTicket);}
bool HSBI_ValidateEconomicRecord(const HSBI_EconomicLedgerRecord &r){return r.dealTicket>0&&r.orderTicket>0&&r.positionIdentifier>0&&r.symbol!=""&&r.cycleId>0&&r.actionId>0&&r.eventId>0&&r.volume>0&&r.sourceDealKey!=""&&r.valid;}
bool HSBI_SameEconomicRecord(const HSBI_EconomicLedgerRecord &a,const HSBI_EconomicLedgerRecord &b){return a.sourceDealKey==b.sourceDealKey&&MathAbs(a.dealNet-b.dealNet)<0.0000001&&a.volume==b.volume&&a.price==b.price;}
int HSBI_ClassifyEconomicDuplicate(const HSBI_EconomicLedgerRecord &existing,const HSBI_EconomicLedgerRecord &incoming){if(existing.sourceDealKey!=incoming.sourceDealKey)return 0;return HSBI_SameEconomicRecord(existing,incoming)?1:2;}
string HSBI_SerializeEconomicRecord(const HSBI_EconomicLedgerRecord &r){return r.sourceDealKey+"|"+DoubleToString(r.volume,8)+"|"+DoubleToString(r.price,8)+"|"+DoubleToString(r.dealNet,8);}
bool HSBI_IsHarvestSourceEntry(const HSBI_EconomicLedgerRecord &r){return r.entryType!=0&&r.dealNet>0.0;}
#endif
