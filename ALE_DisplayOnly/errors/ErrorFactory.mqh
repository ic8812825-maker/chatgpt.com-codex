#ifndef __ALE_DisplayOnly_ERRORS_ERRORFACTORY_MQH__
#define __ALE_DisplayOnly_ERRORS_ERRORFACTORY_MQH__

#include "ErrorContext.mqh"

ErrorContext ErrorFactory_Create(const ErrorCode code,const string message)
  {
   ErrorContext ctx;
   ctx.code=code;
   ctx.message=message;
   return(ctx);
  }

#endif // __ALE_DisplayOnly_ERRORS_ERRORFACTORY_MQH__
