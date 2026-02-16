#ifndef ALE_DO_CORE_FLOW_COMMON_FLOWSNAPSHOT_MQH_INCLUDED
#define ALE_DO_CORE_FLOW_COMMON_FLOWSNAPSHOT_MQH_INCLUDED

// Immutable DTO: only plain data, no methods/calculations/references.
struct FlowSnapshot
  {
   double metric;
   long version;
  };

#endif // ALE_DO_CORE_FLOW_COMMON_FLOWSNAPSHOT_MQH_INCLUDED
