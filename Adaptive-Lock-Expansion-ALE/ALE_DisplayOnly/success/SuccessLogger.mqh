#ifndef __ALE_DisplayOnly_SUCCESS_SUCCESSLOGGER_MQH__
#define __ALE_DisplayOnly_SUCCESS_SUCCESSLOGGER_MQH__

#include "SuccessContext.mqh"

void SuccessLogger_Log(const SuccessContext &ctx)
  {
   Print("Success: ",ctx.message);
  }

#endif // __ALE_DisplayOnly_SUCCESS_SUCCESSLOGGER_MQH__
