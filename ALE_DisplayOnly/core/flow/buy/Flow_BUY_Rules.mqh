#ifndef ALE_DO_CORE_FLOW_BUY_FLOW_BUY_RULES_MQH_INCLUDED
#define ALE_DO_CORE_FLOW_BUY_FLOW_BUY_RULES_MQH_INCLUDED

bool Flow_BUY_CheckRules(const FlowSnapshot &snapshot)
  {
   return(snapshot.metric>=0.0);
  }

#endif // ALE_DO_CORE_FLOW_BUY_FLOW_BUY_RULES_MQH_INCLUDED
