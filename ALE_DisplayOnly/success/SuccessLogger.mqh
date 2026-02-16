#ifndef ALE_DO_SUCCESS_SUCCESSLOGGER_MQH_INCLUDED
#define ALE_DO_SUCCESS_SUCCESSLOGGER_MQH_INCLUDED

#include "SuccessContext.mqh"

class CSuccessLogger
  {
public:
   static void Log(const SuccessContext &ctx)
     {
      Print("Success: ",ctx.message);
     }
  };

#endif // ALE_DO_SUCCESS_SUCCESSLOGGER_MQH_INCLUDED
