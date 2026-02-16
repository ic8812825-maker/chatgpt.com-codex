#ifndef __ALE_DisplayOnly_ERRORS_ERRORDISPATCHER_MQH__
#define __ALE_DisplayOnly_ERRORS_ERRORDISPATCHER_MQH__

#include "ErrorFactory.mqh"
#include "ErrorLogger.mqh"

void ErrorDispatcher_Dispatch(const ErrorCode code,const string message)
  {
   ErrorContext ctx=ErrorFactory_Create(code,message);
   ErrorLogger_Log(ctx);
  }

#endif // __ALE_DisplayOnly_ERRORS_ERRORDISPATCHER_MQH__
