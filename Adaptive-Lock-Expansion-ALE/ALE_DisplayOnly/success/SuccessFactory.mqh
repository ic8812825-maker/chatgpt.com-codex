#ifndef __ALE_DisplayOnly_SUCCESS_SUCCESSFACTORY_MQH__
#define __ALE_DisplayOnly_SUCCESS_SUCCESSFACTORY_MQH__

#include "SuccessContext.mqh"

SuccessContext SuccessFactory_Create(const SuccessCode code,const string message)
  {
   SuccessContext ctx;
   ctx.code=code;
   ctx.message=message;
   return(ctx);
  }

#endif // __ALE_DisplayOnly_SUCCESS_SUCCESSFACTORY_MQH__
