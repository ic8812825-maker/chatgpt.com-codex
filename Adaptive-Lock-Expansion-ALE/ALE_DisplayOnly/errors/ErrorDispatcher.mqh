#ifndef ALE_DO_ERRORS_ERRORDISPATCHER_MQH_INCLUDED
#define ALE_DO_ERRORS_ERRORDISPATCHER_MQH_INCLUDED

#include "ErrorFactory.mqh"
#include "ErrorLogger.mqh"

class CErrorDispatcher
  {
public:
   static void Dispatch(const ErrorCode code,const string message)
     {
      ErrorContext ctx=CErrorFactory::Create(code,message);
      CErrorLogger::Log(ctx);
     }
  };

#endif // ALE_DO_ERRORS_ERRORDISPATCHER_MQH_INCLUDED
