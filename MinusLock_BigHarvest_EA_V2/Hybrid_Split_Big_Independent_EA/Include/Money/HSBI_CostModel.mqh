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
bool HSBI_TryActualDealNet(const double profit,const HSBI_CostSnapshot &c,double &netMoney)
{
   netMoney=0.0;if(!HSBI_IsFiniteNumber(profit)||!HSBI_ValidateCostSnapshot(c,true))return false;netMoney=profit+c.swap+c.commission+c.fee;return HSBI_IsFiniteNumber(netMoney);
}
bool HSBI_TryProjectedNetMoney(const double grossProfit,const HSBI_CostSnapshot &c,const double executionSafetyBuffer,double &netMoney)
{
   netMoney=0.0;if(!HSBI_IsFiniteNumber(grossProfit)||!HSBI_IsFiniteNumber(executionSafetyBuffer)||executionSafetyBuffer<0.0||!HSBI_ValidateCostSnapshot(c,false))return false;
   netMoney=grossProfit+c.swap+c.commission+c.fee-c.spreadCost-c.slippageBuffer-executionSafetyBuffer;return HSBI_IsFiniteNumber(netMoney);
}
#endif
