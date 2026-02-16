#pragma once

#include "ErrorFactory.mqh"
#include "ErrorLogger.mqh"

void ErrorDispatcher_Dispatch(const ErrorCode code,const string message)
  {
   ErrorContext ctx=ErrorFactory_Create(code,message);
   ErrorLogger_Log(ctx);
  }
