#ifndef HSBI_NO_TRADE_EXECUTION_MQH
#define HSBI_NO_TRADE_EXECUTION_MQH
#include "../Core/HSBI_ReasonCodes.mqh"
struct HSBI_NoTradeResult{bool success;HSBI_ReasonCode reason;};
HSBI_NoTradeResult HSBI_SubmitActionStub(){HSBI_NoTradeResult r;r.success=false;r.reason=HSBI_REASON_TRADING_NOT_IMPLEMENTED;return r;}
HSBI_NoTradeResult HSBI_OpenPositionStub(){return HSBI_SubmitActionStub();}
HSBI_NoTradeResult HSBI_ClosePositionStub(){return HSBI_SubmitActionStub();}
HSBI_NoTradeResult HSBI_PartialCloseStub(){return HSBI_SubmitActionStub();}
#endif