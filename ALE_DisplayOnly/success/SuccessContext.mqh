#ifndef ALE_DO_SUCCESS_SUCCESSCONTEXT_MQH_INCLUDED
#define ALE_DO_SUCCESS_SUCCESSCONTEXT_MQH_INCLUDED

#include "SuccessCodes.mqh"

class SuccessContext
  {
public:
   SuccessCode code;
   string      message;

               SuccessContext() : code(SUCCESS_NONE), message("") {}
  };

#endif // ALE_DO_SUCCESS_SUCCESSCONTEXT_MQH_INCLUDED
