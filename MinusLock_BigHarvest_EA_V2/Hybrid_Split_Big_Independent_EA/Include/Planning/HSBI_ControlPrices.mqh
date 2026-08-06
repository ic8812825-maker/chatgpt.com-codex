#ifndef HSBI_CONTROL_PRICES_MQH
#define HSBI_CONTROL_PRICES_MQH
#include "../Core/HSBI_Types.mqh"
#include "../Core/HSBI_ReasonCodes.mqh"
struct HSBI_PricePoint{double value;datetime timestamp;ulong snapshotId;bool normalized;bool valid;};
struct HSBI_MarketSnapshot{string symbol;double bid;double ask;double point;double tickSize;int digits;datetime timestamp;ulong snapshotId;int freshnessSeconds;double spreadPoints;string source;bool normalized;};
struct HSBI_ControlPriceSet{HSBI_PricePoint currentClosePrice;HSBI_PricePoint nextBigControlPrice;HSBI_PricePoint smallTransitionControlPrice;HSBI_PricePoint adverseRiskControlPrice;HSBI_PricePoint gapStressPrice;HSBI_PricePoint finalClosePrice;};
bool HSBI_IsSnapshotFresh(const HSBI_MarketSnapshot &s,const datetime now){return s.timestamp>0&&s.freshnessSeconds>=0&&(now-s.timestamp)<=s.freshnessSeconds;}
double HSBI_NormalizePriceToTick(const double price,const double tickSize){if(tickSize<=0.0)return 0.0;return MathRound(price/tickSize)*tickSize;}
double HSBI_ResolveCloseSide(const HSBI_Direction d,const HSBI_MarketSnapshot &s){if(d==HSBI_DIRECTION_BUY)return s.bid;if(d==HSBI_DIRECTION_SELL)return s.ask;return 0.0;}
HSBI_ValidationResult HSBI_ValidateMarketSnapshot(const HSBI_MarketSnapshot &s){bool ok=s.symbol!=""&&s.bid>0&&s.ask>=s.bid&&s.point>0&&s.tickSize>0&&s.snapshotId>0;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_STALE_SNAPSHOT,"HSBI-GEO-005","");}
HSBI_ValidationResult HSBI_ValidateControlPriceSet(const HSBI_ControlPriceSet &p){bool ok=p.currentClosePrice.valid&&p.nextBigControlPrice.valid&&p.smallTransitionControlPrice.valid&&p.finalClosePrice.valid;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_OFF_GRID_PRICE,"HSBI-DEC-003","");}
#endif