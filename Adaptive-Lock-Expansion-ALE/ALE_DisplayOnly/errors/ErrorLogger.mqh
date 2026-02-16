#pragma once

#include "ErrorContext.mqh"

void ErrorLogger_Log(const ErrorContext &ctx)
  {
   Print("Error: ",ctx.message);
  }
