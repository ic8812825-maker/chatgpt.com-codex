#ifndef __ALE_DisplayOnly_CORE_FLOW_SELL_FLOW_SELL_RULES_MQH__
#define __ALE_DisplayOnly_CORE_FLOW_SELL_FLOW_SELL_RULES_MQH__

bool Flow_SELL_CheckRules(const FlowSnapshot &snapshot)
  {
   return(snapshot.metric<=0.0 || snapshot.metric>=0.0);
  }

#endif // __ALE_DisplayOnly_CORE_FLOW_SELL_FLOW_SELL_RULES_MQH__
