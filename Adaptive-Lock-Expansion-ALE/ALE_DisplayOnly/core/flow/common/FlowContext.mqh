#ifndef ALE_DO_CORE_FLOW_COMMON_FLOWCONTEXT_MQH_INCLUDED
#define ALE_DO_CORE_FLOW_COMMON_FLOWCONTEXT_MQH_INCLUDED

#include "GeometryContext.mqh"
#include "MarginContext.mqh"
#include "ExecutionContext.mqh"

struct FlowContext
  {
   GeometryContext geometry;
   MarginContext margin;
   ExecutionContext execution;
   double signal_strength;
  };

#endif // ALE_DO_CORE_FLOW_COMMON_FLOWCONTEXT_MQH_INCLUDED
