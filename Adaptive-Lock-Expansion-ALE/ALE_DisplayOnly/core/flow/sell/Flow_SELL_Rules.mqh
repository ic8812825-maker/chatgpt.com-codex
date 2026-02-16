#ifndef ALE_DO_CORE_FLOW_SELL_FLOW_SELL_RULES_MQH_INCLUDED
#define ALE_DO_CORE_FLOW_SELL_FLOW_SELL_RULES_MQH_INCLUDED

#include "../common/FlowSnapshot.mqh"

class CFlowSellRules
  {
public:
   static bool Check(const FlowSnapshot &snapshot)
     {
      return(snapshot.metric<=0.0 || snapshot.metric>=0.0);
     }
  };

#endif // ALE_DO_CORE_FLOW_SELL_FLOW_SELL_RULES_MQH_INCLUDED
