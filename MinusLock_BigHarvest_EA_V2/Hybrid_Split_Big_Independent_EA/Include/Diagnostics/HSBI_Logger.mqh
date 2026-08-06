#ifndef HSBI_LOGGER_MQH
#define HSBI_LOGGER_MQH
#include "../Core/HSBI_Context.mqh"
enum HSBI_LogSeverity{HSBI_LOG_TRACE,HSBI_LOG_INFO,HSBI_LOG_WARNING,HSBI_LOG_ERROR,HSBI_LOG_CRITICAL};
struct HSBI_LogRecord{HSBI_LogSeverity severity;string requirementId;HSBI_ReasonCode reason;ulong cycleId;ulong planId;ulong actionId;ulong eventId;HSBI_State state;string symbol;long magic;string message;datetime timestamp;};
void HSBI_Log(const string requirementId,const HSBI_ReasonCode reason,const string message){Print("HSBI|",requirementId,"|",HSBI_ReasonToString(reason),"|",message);}
#endif