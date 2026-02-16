#ifndef __ALE_DisplayOnly_CORE_FLOW_COMMON_FLOWSNAPSHOT_MQH__
#define __ALE_DisplayOnly_CORE_FLOW_COMMON_FLOWSNAPSHOT_MQH__

// Immutable DTO: only plain data, no methods/calculations/references.
struct FlowSnapshot
  {
   double metric;
   long version;
  };

#endif // __ALE_DisplayOnly_CORE_FLOW_COMMON_FLOWSNAPSHOT_MQH__
