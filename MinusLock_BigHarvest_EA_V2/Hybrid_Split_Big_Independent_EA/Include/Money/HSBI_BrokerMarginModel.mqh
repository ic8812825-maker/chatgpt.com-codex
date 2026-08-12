#ifndef HSBI_BROKER_MARGIN_MODEL_MQH
#define HSBI_BROKER_MARGIN_MODEL_MQH
#include "HSBI_BrokerMoneyTypes.mqh"
#include "../Planning/HSBI_BrokerGrid.mqh"
HSBI_MarginCalculationResult HSBI_CalculateProjectedMargin(const HSBI_BrokerProperties &p,const HSBI_Direction direction,const double volume,const double price)
{
   HSBI_MarginCalculationResult r;ZeroMemory(r);r.status=HSBI_CALC_REJECT;r.projected=true;r.symbol=p.symbol;r.direction=direction;r.volume=volume;r.price=price;r.snapshotId=p.snapshotId;r.reason=HSBI_REASON_INVALID_IDENTITY;r.details="INVALID_SYMBOL_PROPERTIES";
   if(HSBI_ValidateBrokerProperties(p)!=HSBI_BROKER_PROPERTIES_VALID)return r;
   if(direction!=HSBI_DIRECTION_BUY&&direction!=HSBI_DIRECTION_SELL){r.details="INVALID_DIRECTION";return r;}
   if(!HSBI_ValidateVolume(volume,p)){r.reason=HSBI_REASON_INVALID_VOLUME;r.details="INVALID_VOLUME";return r;}
   if(!HSBI_ValidatePriceGrid(price,p)){r.reason=HSBI_REASON_OFF_GRID_PRICE;r.details="INVALID_PRICE_GRID";return r;}
   double margin=0.0;ENUM_ORDER_TYPE orderType=(direction==HSBI_DIRECTION_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL);
   if(!OrderCalcMargin(orderType,p.symbol,volume,price,margin)){r.status=HSBI_CALC_UNAVAILABLE;r.reason=HSBI_REASON_NOT_INITIALIZED;r.details="BROKER_MARGIN_UNAVAILABLE";return r;}
   if(!HSBI_IsFiniteNumber(margin)){r.status=HSBI_CALC_ERROR;r.details="NONFINITE_MARGIN";return r;}
   if(margin<0.0){r.status=HSBI_CALC_ERROR;r.details="NEGATIVE_MARGIN";return r;}
   r.margin=margin;r.status=HSBI_CALC_PASS;r.valid=true;r.reason=HSBI_REASON_OK;r.details="PASS";return r;
}
#endif
