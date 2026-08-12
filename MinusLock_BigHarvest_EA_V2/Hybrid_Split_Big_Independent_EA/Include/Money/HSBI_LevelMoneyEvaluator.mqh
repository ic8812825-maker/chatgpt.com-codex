#ifndef HSBI_LEVEL_MONEY_EVALUATOR_MQH
#define HSBI_LEVEL_MONEY_EVALUATOR_MQH
#include "HSBI_BrokerMoneyModel.mqh"
#include "HSBI_MoneyProofIdentity.mqh"
struct HSBI_BrokerMoneyEvaluationInput{HSBI_BrokerProperties broker;string symbol;HSBI_Direction direction;double volume;double openPrice;double closePrice;double bid;double ask;HSBI_CostSnapshot costs;double executionSafetyBuffer;ulong snapshotId;datetime timestamp;bool projected;};
struct HSBI_BrokerMoneyEvaluationResult{HSBI_MoneyProofIdentity identity;bool runtimeConfirmed;HSBI_CalculationStatus status;bool valid;bool projected;bool actual;double grossProfit;double commission;double swap;double fee;double spreadCost;double slippageBuffer;double executionSafetyBuffer;double netMoney;string symbol;HSBI_Direction direction;double volume;double openPrice;double closePrice;ulong snapshotId;HSBI_ReasonCode reason;string details;};
HSBI_BrokerMoneyEvaluationResult HSBI_EvaluateProjectedLegMoney(const HSBI_BrokerMoneyEvaluationInput &x)
{
   HSBI_BrokerMoneyEvaluationResult r;ZeroMemory(r);r.status=HSBI_CALC_REJECT;r.projected=x.projected;r.actual=false;r.symbol=x.symbol;r.direction=x.direction;r.volume=x.volume;r.openPrice=x.openPrice;r.closePrice=x.closePrice;r.snapshotId=x.snapshotId;r.executionSafetyBuffer=x.executionSafetyBuffer;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details="INVALID_INPUT";
   if(!x.projected||x.timestamp<=0||x.snapshotId==0||x.snapshotId!=x.broker.snapshotId||x.symbol==""||x.symbol!=x.broker.symbol)return r;
   HSBI_MoneyCalculationResult source=HSBI_CalculateProjectedProfit(x.broker,x.direction,x.volume,x.openPrice,x.closePrice,x.bid,x.ask,x.costs,x.executionSafetyBuffer);
   r.status=source.status;r.valid=source.valid;r.projected=source.projected;r.actual=source.actual;r.grossProfit=source.grossProfit;r.commission=source.commission;r.swap=source.swap;r.fee=source.fee;r.spreadCost=source.spreadCost;r.slippageBuffer=source.slippageBuffer;r.netMoney=source.netMoney;r.reason=source.reason;r.details=source.details;
   if(r.valid&&(!HSBI_IsFiniteNumber(r.netMoney)||r.actual||!r.projected)){r.valid=false;r.status=HSBI_CALC_ERROR;r.details="INVALID_RESULT_FLAGS_OR_MONEY";}
   return r;
}
#endif
