#ifndef ALE_DO_ERRORS_ERRORDISPATCHER_MQH_INCLUDED
#define ALE_DO_ERRORS_ERRORDISPATCHER_MQH_INCLUDED

#include "ErrorFactory.mqh"
#include "ErrorLogger.mqh"

void ErrorDispatcher_Dispatch(const ErrorCode code,const string message)
  {
   ErrorContext ctx=ErrorFactory_Create(code,message);
   ErrorLogger_Log(ctx);
  }

#endif // ALE_DO_ERRORS_ERRORDISPATCHER_MQH_INCLUDED
