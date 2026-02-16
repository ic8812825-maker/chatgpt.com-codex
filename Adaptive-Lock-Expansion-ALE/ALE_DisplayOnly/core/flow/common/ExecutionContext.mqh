#ifndef ALE_DO_CORE_FLOW_COMMON_EXECUTIONCONTEXT_MQH_INCLUDED
#define ALE_DO_CORE_FLOW_COMMON_EXECUTIONCONTEXT_MQH_INCLUDED

class ExecutionContext
  {
public:
   long timestamp;
   int  tick_index;

          ExecutionContext() : timestamp(0), tick_index(0) {}
  };

#endif // ALE_DO_CORE_FLOW_COMMON_EXECUTIONCONTEXT_MQH_INCLUDED
