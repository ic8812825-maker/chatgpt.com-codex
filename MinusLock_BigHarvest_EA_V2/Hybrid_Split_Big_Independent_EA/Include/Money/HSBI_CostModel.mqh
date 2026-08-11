#ifndef HSBI_COST_MODEL_MQH
#define HSBI_COST_MODEL_MQH
#include "HSBI_BrokerMoneyTypes.mqh"
struct HSBI_CostSnapshot{double commission;double swap;double fee;double slippageBuffer;double spreadCost;bool valid;bool actual;datetime timestamp;ulong snapshotId;};
bool HSBI_ValidateCostSnapshot(const HSBI_CostSnapshot &c,const bool expectedActual)
{
   if(!c.valid||c.actual!=expectedActual||c.timestamp<=0||c.snapshotId==0)return false;
   if(!HSBI_IsFiniteNumber(c.commission)||!HSBI_IsFiniteNumber(c.swap)||!HSBI_IsFiniteNumber(c.fee)||!HSBI_IsFiniteNumber(c.slippageBuffer)||!HSBI_IsFiniteNumber(c.spreadCost))return false;
   return c.slippageBuffer>=0.0&&c.spreadCost>=0.0;
}
double HSBI_ActualDealNet(const double profit,const HSBI_CostSnapshot &c){if(!HSBI_IsFiniteNumber(profit)||!HSBI_ValidateCostSnapshot(c,true))return 0.0;return profit+c.swap+c.commission+c.fee;}
double HSBI_ProjectedNetMoney(const double grossProfit,const HSBI_CostSnapshot &c,const double executionSafetyBuffer)
{
   if(!HSBI_IsFiniteNumber(grossProfit)||!HSBI_IsFiniteNumber(executionSafetyBuffer)||executionSafetyBuffer<0.0||!HSBI_ValidateCostSnapshot(c,false))return 0.0;
   return grossProfit+c.swap+c.commission+c.fee-c.spreadCost-c.slippageBuffer-executionSafetyBuffer;
}
#endif
