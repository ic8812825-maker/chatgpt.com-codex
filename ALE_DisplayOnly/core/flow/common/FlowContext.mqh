#ifndef ALE_DO_CORE_FLOW_COMMON_FLOWCONTEXT_MQH_INCLUDED
#define ALE_DO_CORE_FLOW_COMMON_FLOWCONTEXT_MQH_INCLUDED

#include "GeometryContext.mqh"
#include "MarginContext.mqh"
#include "ExecutionContext.mqh"

class FlowContext
  {
public:
   GeometryContext geometry;
   MarginContext   margin;
   ExecutionContext execution;
   double          signal_strength;

                   FlowContext() : signal_strength(0.0) {}
  };

#endif // ALE_DO_CORE_FLOW_COMMON_FLOWCONTEXT_MQH_INCLUDED
