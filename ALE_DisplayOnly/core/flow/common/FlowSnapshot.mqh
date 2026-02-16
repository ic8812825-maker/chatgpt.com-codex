#ifndef ALE_DO_CORE_FLOW_COMMON_FLOWSNAPSHOT_MQH_INCLUDED
#define ALE_DO_CORE_FLOW_COMMON_FLOWSNAPSHOT_MQH_INCLUDED

class FlowSnapshot
  {
public:
   double metric;
   long   version;

            FlowSnapshot() : metric(0.0), version(0) {}
  };

#endif // ALE_DO_CORE_FLOW_COMMON_FLOWSNAPSHOT_MQH_INCLUDED
