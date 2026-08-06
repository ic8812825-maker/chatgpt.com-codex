#ifndef HSBI_TYPES_MQH
#define HSBI_TYPES_MQH
#include "HSBI_Enums.mqh"
struct HSBI_ValidationResult{bool passed;int reason;string requirementId;string details;};
struct HSBI_U64Id{ulong value;bool valid;};
struct HSBI_Timestamp{datetime value;bool valid;};
HSBI_ValidationResult HSBI_Result(const bool passed,const int reason,const string req,const string details){HSBI_ValidationResult r;r.passed=passed;r.reason=reason;r.requirementId=req;r.details=details;return r;}
#endif