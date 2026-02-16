#ifndef __ALE_DisplayOnly_ERRORS_ERRORLOGGER_MQH__
#define __ALE_DisplayOnly_ERRORS_ERRORLOGGER_MQH__

#include "ErrorContext.mqh"

void ErrorLogger_Log(const ErrorContext &ctx)
  {
   Print("Error: ",ctx.message);
  }

#endif // __ALE_DisplayOnly_ERRORS_ERRORLOGGER_MQH__
