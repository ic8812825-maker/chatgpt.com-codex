#pragma once

#include "ErrorContext.mqh"

ErrorContext ErrorFactory_Create(const ErrorCode code,const string message)
  {
   ErrorContext ctx;
   ctx.code=code;
   ctx.message=message;
   return(ctx);
  }
