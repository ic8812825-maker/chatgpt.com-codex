#ifndef __ALE_DisplayOnly_CORE_FLOW_BUY_FLOW_BUY_RULES_MQH__
#define __ALE_DisplayOnly_CORE_FLOW_BUY_FLOW_BUY_RULES_MQH__

bool Flow_BUY_CheckRules(const FlowSnapshot &snapshot)
  {
   return(snapshot.metric>=0.0);
  }

#endif // __ALE_DisplayOnly_CORE_FLOW_BUY_FLOW_BUY_RULES_MQH__
