#ifndef ALE_DO_ERRORS_ERRORLOGGER_MQH_INCLUDED
#define ALE_DO_ERRORS_ERRORLOGGER_MQH_INCLUDED

#include "ErrorContext.mqh"

void ErrorLogger_Log(const ErrorContext &ctx)
  {
   Print("Error: ",ctx.message);
  }

#endif // ALE_DO_ERRORS_ERRORLOGGER_MQH_INCLUDED
