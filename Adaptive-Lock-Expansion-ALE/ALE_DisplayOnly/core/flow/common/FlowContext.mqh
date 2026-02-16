#pragma once

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
