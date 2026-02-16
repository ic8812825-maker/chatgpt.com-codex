#ifndef ALE_DO_ERRORS_ERRORFACTORY_MQH_INCLUDED
#define ALE_DO_ERRORS_ERRORFACTORY_MQH_INCLUDED

#include "ErrorContext.mqh"

ErrorContext ErrorFactory_Create(const ErrorCode code,const string message)
  {
   ErrorContext ctx;
   ctx.code=code;
   ctx.message=message;
   return(ctx);
  }

#endif // ALE_DO_ERRORS_ERRORFACTORY_MQH_INCLUDED
