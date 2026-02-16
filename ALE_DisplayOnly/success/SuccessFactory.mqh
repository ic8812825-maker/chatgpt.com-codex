#pragma once

#include "SuccessContext.mqh"

SuccessContext SuccessFactory_Create(const SuccessCode code,const string message)
  {
   SuccessContext ctx;
   ctx.code=code;
   ctx.message=message;
   return(ctx);
  }
