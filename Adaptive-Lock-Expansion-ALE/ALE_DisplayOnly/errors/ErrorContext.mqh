#ifndef ALE_DO_ERRORS_ERRORCONTEXT_MQH_INCLUDED
#define ALE_DO_ERRORS_ERRORCONTEXT_MQH_INCLUDED

#include "ErrorCodes.mqh"

struct ErrorContext
  {
   ErrorCode code;
   string message;
  };

#endif // ALE_DO_ERRORS_ERRORCONTEXT_MQH_INCLUDED
