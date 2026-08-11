#ifndef HSBI_CALCULATION_GATE_TYPES_MQH
#define HSBI_CALCULATION_GATE_TYPES_MQH
#include "../Money/HSBI_BrokerMoneyTypes.mqh"
enum HSBI_CalculationFailure{HSBI_CALC_FAILURE_NONE,HSBI_INVALID_SYMBOL_PROPERTIES,HSBI_INVALID_TICK_SIZE,HSBI_INVALID_VOLUME_STEP,HSBI_INVALID_PRICE_GRID,HSBI_INVALID_VOLUME,HSBI_INVALID_RATIO,HSBI_INVALID_DIRECTION,HSBI_STALE_SNAPSHOT,HSBI_WRONG_CLOSE_SIDE,HSBI_NONFINITE_MONEY,HSBI_NONFINITE_MARGIN,HSBI_BROKER_MONEY_UNAVAILABLE,HSBI_BROKER_MARGIN_UNAVAILABLE,HSBI_RECOVERY_SLOPE_FAILED,HSBI_CATCH_UP_FAILED};
struct HSBI_CalculationGateResult{HSBI_CalculationStatus status;bool passed;HSBI_CalculationFailure failure;HSBI_ReasonCode reason;string details;};
HSBI_CalculationGateResult HSBI_FailClosed(const HSBI_CalculationStatus status,const HSBI_CalculationFailure failure,const HSBI_ReasonCode reason,const string details)
{
   HSBI_CalculationGateResult r;r.status=status;r.passed=(status==HSBI_CALC_PASS);r.failure=failure;r.reason=reason;r.details=details;return r;
}
bool HSBI_CalculationResultFlagsValid(const bool valid,const bool projected,const bool actual,const HSBI_CalculationStatus status)
{
   if(projected&&actual)return false;if(valid!=(status==HSBI_CALC_PASS))return false;return true;
}
#endif
