#ifndef ALE_DO_SUCCESS_SUCCESSDISPATCHER_MQH_INCLUDED
#define ALE_DO_SUCCESS_SUCCESSDISPATCHER_MQH_INCLUDED

#include "SuccessFactory.mqh"
#include "SuccessLogger.mqh"

class CSuccessDispatcher
  {
public:
   static void Dispatch(const SuccessCode code,const string message)
     {
      SuccessContext ctx=CSuccessFactory::Create(code,message);
      CSuccessLogger::Log(ctx);
     }
  };

#endif // ALE_DO_SUCCESS_SUCCESSDISPATCHER_MQH_INCLUDED
