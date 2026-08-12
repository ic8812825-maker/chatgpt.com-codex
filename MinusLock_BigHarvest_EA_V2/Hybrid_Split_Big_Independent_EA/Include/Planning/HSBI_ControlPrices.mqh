#ifndef HSBI_CONTROL_PRICES_MQH
#define HSBI_CONTROL_PRICES_MQH
#include "../Core/HSBI_Types.mqh"
#include "../Core/HSBI_ReasonCodes.mqh"
#include "HSBI_BrokerGrid.mqh"
enum HSBI_ControlPriceType{HSBI_CONTROL_CURRENT_CLOSE,HSBI_CONTROL_NEXT_BIG,HSBI_CONTROL_ADVERSE_RISK,HSBI_CONTROL_GAP_STRESS,HSBI_CONTROL_FINAL_CLOSE};
struct HSBI_ControlPrice{string symbol;double bid;double ask;double mid;double selectedPrice;HSBI_Direction direction;HSBI_PriceSide side;double point;double tickSize;int digits;datetime timestamp;ulong snapshotId;bool fresh;bool normalized;bool valid;};
struct HSBI_PricePoint{double value;datetime timestamp;ulong snapshotId;bool normalized;bool valid;};
struct HSBI_MarketSnapshot{string symbol;double bid;double ask;double point;double tickSize;int digits;datetime timestamp;ulong snapshotId;int freshnessSeconds;double spreadPoints;string source;bool normalized;};
struct HSBI_ControlPriceSet{HSBI_PricePoint currentClosePrice;HSBI_PricePoint nextBigControlPrice;HSBI_PricePoint smallTransitionControlPrice;HSBI_PricePoint adverseRiskControlPrice;HSBI_PricePoint gapStressPrice;HSBI_PricePoint finalClosePrice;};
bool HSBI_IsSnapshotFresh(const HSBI_MarketSnapshot &s,const datetime now){return s.timestamp>0&&s.freshnessSeconds>=0&&(now-s.timestamp)<=s.freshnessSeconds;}
double HSBI_NormalizePriceToTick(const double price,const double tickSize){if(tickSize<=0.0)return 0.0;return MathRound(price/tickSize)*tickSize;}
double HSBI_ResolveCloseSide(const HSBI_Direction d,const HSBI_MarketSnapshot &s){if(d==HSBI_DIRECTION_BUY)return s.bid;if(d==HSBI_DIRECTION_SELL)return s.ask;return 0.0;}
HSBI_ValidationResult HSBI_ValidateMarketSnapshot(const HSBI_MarketSnapshot &s){bool ok=s.symbol!=""&&s.bid>0&&s.ask>=s.bid&&s.point>0&&s.tickSize>0&&s.snapshotId>0;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_STALE_SNAPSHOT,"HSBI-GEO-005","");}
HSBI_ValidationResult HSBI_ValidateControlPriceSet(const HSBI_ControlPriceSet &p){bool ok=p.currentClosePrice.valid&&p.nextBigControlPrice.valid&&p.smallTransitionControlPrice.valid&&p.finalClosePrice.valid;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_OFF_GRID_PRICE,"HSBI-DEC-003","");}
bool HSBI_ValidateTypedControlPrice(const HSBI_ControlPrice &p,const string expectedSymbol)
{
   if(!p.valid||!p.fresh||!p.normalized||p.timestamp<=0||p.snapshotId==0||p.symbol==""||p.symbol!=expectedSymbol)return false;
   if(!HSBI_IsFiniteNumber(p.bid)||!HSBI_IsFiniteNumber(p.ask)||!HSBI_IsFiniteNumber(p.selectedPrice)||p.bid<=0.0||p.ask<p.bid||p.tickSize<=0.0||p.point<=0.0)return false;
   if(!HSBI_IsPriceOnTickGrid(p.selectedPrice,p.tickSize))return false;
   if(p.direction==HSBI_DIRECTION_BUY)return p.side==HSBI_PRICE_SIDE_BID&&MathAbs(p.selectedPrice-p.bid)<=HSBI_GridTolerance(p.tickSize);
   if(p.direction==HSBI_DIRECTION_SELL)return p.side==HSBI_PRICE_SIDE_ASK&&MathAbs(p.selectedPrice-p.ask)<=HSBI_GridTolerance(p.tickSize);
   return false;
}
#endif
