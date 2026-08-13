#ifndef HSBI_BROKER_MONEY_TYPES_MQH
#define HSBI_BROKER_MONEY_TYPES_MQH
#include "../Core/HSBI_Types.mqh"
#include "../Core/HSBI_ReasonCodes.mqh"
enum HSBI_CalculationStatus{HSBI_CALC_PASS,HSBI_CALC_REJECT,HSBI_CALC_ERROR,HSBI_CALC_UNAVAILABLE};
enum HSBI_BrokerPropertyStatus{HSBI_BROKER_PROPERTIES_VALID,HSBI_BROKER_PROPERTIES_INVALID,HSBI_BROKER_PROPERTIES_STALE,HSBI_BROKER_PROPERTIES_UNAVAILABLE};
struct HSBI_BrokerProperties{string symbol;double point;double tickSize;int digits;double volumeMin;double volumeMax;double volumeStep;double tickValueProfit;double tickValueLoss;bool valid;bool fresh;ulong snapshotId;datetime timestamp;};
struct HSBI_MoneyCalculationResult{HSBI_CalculationStatus status;bool valid;bool projected;bool actual;string symbol;HSBI_Direction direction;double volume;double openPrice;double closePrice;double grossProfit;double commission;double swap;double fee;double spreadCost;double slippageBuffer;double netMoney;ulong snapshotId;HSBI_ReasonCode reason;string details;};
struct HSBI_MarginCalculationResult{HSBI_CalculationStatus status;bool valid;bool projected;double margin;double volume;double price;string symbol;HSBI_Direction direction;ulong snapshotId;HSBI_ReasonCode reason;string details;};
bool HSBI_IsFiniteNumber(const double value){return MathIsValidNumber(value);}
HSBI_BrokerPropertyStatus HSBI_ValidateBrokerProperties(const HSBI_BrokerProperties &p)
{
   if(!p.valid)return HSBI_BROKER_PROPERTIES_UNAVAILABLE;
   if(!p.fresh)return HSBI_BROKER_PROPERTIES_STALE;
   if(p.symbol==""||p.digits<0||p.snapshotId==0||p.timestamp<=0)return HSBI_BROKER_PROPERTIES_INVALID;
   if(!HSBI_IsFiniteNumber(p.point)||!HSBI_IsFiniteNumber(p.tickSize)||!HSBI_IsFiniteNumber(p.volumeMin)||!HSBI_IsFiniteNumber(p.volumeMax)||!HSBI_IsFiniteNumber(p.volumeStep)||!HSBI_IsFiniteNumber(p.tickValueProfit)||!HSBI_IsFiniteNumber(p.tickValueLoss))return HSBI_BROKER_PROPERTIES_INVALID;
   if(p.point<=0.0||p.tickSize<=0.0||p.volumeMin<=0.0||p.volumeMax<p.volumeMin||p.volumeStep<=0.0||p.tickValueProfit<0.0||p.tickValueLoss<0.0)return HSBI_BROKER_PROPERTIES_INVALID;
   return HSBI_BROKER_PROPERTIES_VALID;
}
#endif
