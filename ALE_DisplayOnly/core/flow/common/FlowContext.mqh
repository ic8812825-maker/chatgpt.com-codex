#ifndef __ALE_DisplayOnly_CORE_FLOW_COMMON_FLOWCONTEXT_MQH__
#define __ALE_DisplayOnly_CORE_FLOW_COMMON_FLOWCONTEXT_MQH__

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

#endif // __ALE_DisplayOnly_CORE_FLOW_COMMON_FLOWCONTEXT_MQH__
