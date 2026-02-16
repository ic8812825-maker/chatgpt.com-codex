#ifndef ALE_DO_ERRORS_ERRORFACTORY_MQH_INCLUDED
#define ALE_DO_ERRORS_ERRORFACTORY_MQH_INCLUDED

#include "ErrorContext.mqh"

class CErrorFactory
  {
public:
   static ErrorContext Create(const ErrorCode code,const string message)
     {
      ErrorContext ctx;
      ctx.code=code;
      ctx.message=message;
      return(ctx);
     }
  };

#endif // ALE_DO_ERRORS_ERRORFACTORY_MQH_INCLUDED
