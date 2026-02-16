#pragma once

#include "SuccessFactory.mqh"
#include "SuccessLogger.mqh"

void SuccessDispatcher_Dispatch(const SuccessCode code,const string message)
  {
   SuccessContext ctx=SuccessFactory_Create(code,message);
   SuccessLogger_Log(ctx);
  }
