#pragma once

#include "SuccessContext.mqh"

void SuccessLogger_Log(const SuccessContext &ctx)
  {
   Print("Success: ",ctx.message);
  }
