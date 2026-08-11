#ifndef HSBI_BROKER_MONEY_MODEL_MQH
#define HSBI_BROKER_MONEY_MODEL_MQH
#include "HSBI_CostModel.mqh"
#include "../Planning/HSBI_BrokerGrid.mqh"
HSBI_MoneyCalculationResult HSBI_MoneyResult(const HSBI_CalculationStatus status,const HSBI_ReasonCode reason,const string details){HSBI_MoneyCalculationResult r;ZeroMemory(r);r.status=status;r.reason=reason;r.details=details;r.projected=true;return r;}
HSBI_MoneyCalculationResult HSBI_CalculateProjectedProfit(const HSBI_BrokerProperties &p,const HSBI_Direction direction,const double volume,const double openPrice,const double closePrice,const double bid,const double ask,const HSBI_CostSnapshot &cost,const double executionSafetyBuffer)
{
   HSBI_MoneyCalculationResult r=HSBI_MoneyResult(HSBI_CALC_REJECT,HSBI_REASON_INVALID_IDENTITY,"INVALID_SYMBOL_PROPERTIES");r.symbol=p.symbol;r.direction=direction;r.volume=volume;r.openPrice=openPrice;r.closePrice=closePrice;r.snapshotId=p.snapshotId;
   if(HSBI_ValidateBrokerProperties(p)!=HSBI_BROKER_PROPERTIES_VALID)return r;
   if(direction!=HSBI_DIRECTION_BUY&&direction!=HSBI_DIRECTION_SELL){r.details="INVALID_DIRECTION";return r;}
   if(!HSBI_ValidateVolume(volume,p)){r.reason=HSBI_REASON_INVALID_VOLUME;r.details="INVALID_VOLUME";return r;}
   if(!HSBI_ValidatePriceGrid(openPrice,p)||!HSBI_ValidatePriceGrid(closePrice,p)||!HSBI_IsFiniteNumber(bid)||!HSBI_IsFiniteNumber(ask)||bid<=0.0||ask<bid){r.reason=HSBI_REASON_OFF_GRID_PRICE;r.details="INVALID_PRICE_GRID";return r;}
   double expectedClose=(direction==HSBI_DIRECTION_BUY?bid:ask);if(MathAbs(closePrice-expectedClose)>HSBI_GridTolerance(p.tickSize)){r.reason=HSBI_REASON_OFF_GRID_PRICE;r.details="WRONG_CLOSE_SIDE";return r;}
   if(!HSBI_ValidateCostSnapshot(cost,false)||executionSafetyBuffer<0.0){r.details="INVALID_COST_SNAPSHOT";return r;}
   double gross=0.0;ENUM_ORDER_TYPE orderType=(direction==HSBI_DIRECTION_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL);
   if(!OrderCalcProfit(orderType,p.symbol,volume,openPrice,closePrice,gross)){r.status=HSBI_CALC_UNAVAILABLE;r.reason=HSBI_REASON_NOT_INITIALIZED;r.details="BROKER_MONEY_UNAVAILABLE";return r;}
   if(!HSBI_IsFiniteNumber(gross)){r.status=HSBI_CALC_ERROR;r.details="NONFINITE_MONEY";return r;}
   r.grossProfit=gross;r.commission=cost.commission;r.swap=cost.swap;r.fee=cost.fee;r.spreadCost=cost.spreadCost;r.slippageBuffer=cost.slippageBuffer;r.netMoney=HSBI_ProjectedNetMoney(gross,cost,executionSafetyBuffer);
   if(!HSBI_IsFiniteNumber(r.netMoney)){r.status=HSBI_CALC_ERROR;r.details="NONFINITE_MONEY";return r;}
   r.status=HSBI_CALC_PASS;r.valid=true;r.actual=false;r.reason=HSBI_REASON_OK;r.details="PASS";return r;
}
#endif
