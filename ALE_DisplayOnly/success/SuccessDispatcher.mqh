#ifndef __ALE_DisplayOnly_SUCCESS_SUCCESSDISPATCHER_MQH__
#define __ALE_DisplayOnly_SUCCESS_SUCCESSDISPATCHER_MQH__

#include "SuccessFactory.mqh"
#include "SuccessLogger.mqh"

void SuccessDispatcher_Dispatch(const SuccessCode code,const string message)
  {
   SuccessContext ctx=SuccessFactory_Create(code,message);
   SuccessLogger_Log(ctx);
  }

#endif // __ALE_DisplayOnly_SUCCESS_SUCCESSDISPATCHER_MQH__
