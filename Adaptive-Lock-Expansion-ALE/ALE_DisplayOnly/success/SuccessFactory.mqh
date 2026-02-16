#ifndef ALE_DO_SUCCESS_SUCCESSFACTORY_MQH_INCLUDED
#define ALE_DO_SUCCESS_SUCCESSFACTORY_MQH_INCLUDED

#include "SuccessContext.mqh"

class CSuccessFactory
  {
public:
   static SuccessContext Create(const SuccessCode code,const string message)
     {
      SuccessContext ctx;
      ctx.code=code;
      ctx.message=message;
      return(ctx);
     }
  };

#endif // ALE_DO_SUCCESS_SUCCESSFACTORY_MQH_INCLUDED
