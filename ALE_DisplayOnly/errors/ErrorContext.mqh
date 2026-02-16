#ifndef ALE_DO_ERRORS_ERRORCONTEXT_MQH_INCLUDED
#define ALE_DO_ERRORS_ERRORCONTEXT_MQH_INCLUDED

#include "ErrorCodes.mqh"

class ErrorContext
  {
public:
   ErrorCode code;
   string    message;

             ErrorContext() : code(ERROR_NONE), message("") {}
  };

#endif // ALE_DO_ERRORS_ERRORCONTEXT_MQH_INCLUDED
