#ifndef ALE_DO_SUCCESS_SUCCESSDISPATCHER_MQH_INCLUDED
#define ALE_DO_SUCCESS_SUCCESSDISPATCHER_MQH_INCLUDED

#include "SuccessFactory.mqh"
#include "SuccessLogger.mqh"

void SuccessDispatcher_Dispatch(const SuccessCode code,const string message)
  {
   SuccessContext ctx=SuccessFactory_Create(code,message);
   SuccessLogger_Log(ctx);
  }

#endif // ALE_DO_SUCCESS_SUCCESSDISPATCHER_MQH_INCLUDED
