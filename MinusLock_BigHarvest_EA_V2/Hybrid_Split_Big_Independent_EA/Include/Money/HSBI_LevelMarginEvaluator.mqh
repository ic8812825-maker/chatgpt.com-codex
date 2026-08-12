#ifndef HSBI_LEVEL_MARGIN_EVALUATOR_MQH
#define HSBI_LEVEL_MARGIN_EVALUATOR_MQH
#include "HSBI_LevelMoneyEvaluator.mqh"
#include "HSBI_BrokerMarginModel.mqh"
HSBI_MarginCalculationResult HSBI_EvaluateProjectedLegMargin(const HSBI_BrokerMoneyEvaluationInput &x)
{
   HSBI_MarginCalculationResult r;ZeroMemory(r);r.status=HSBI_CALC_REJECT;r.projected=true;r.symbol=x.symbol;r.direction=x.direction;r.volume=x.volume;r.price=x.openPrice;r.snapshotId=x.snapshotId;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details="INVALID_INPUT";
   if(!x.projected||x.timestamp<=0||x.snapshotId==0||x.snapshotId!=x.broker.snapshotId||x.symbol==""||x.symbol!=x.broker.symbol)return r;
   r=HSBI_CalculateProjectedMargin(x.broker,x.direction,x.volume,x.openPrice);
   if(r.valid&&(!HSBI_IsFiniteNumber(r.margin)||r.margin<0.0)){r.valid=false;r.status=HSBI_CALC_ERROR;r.details="NONFINITE_OR_NEGATIVE_MARGIN";}
   return r;
}
#endif
