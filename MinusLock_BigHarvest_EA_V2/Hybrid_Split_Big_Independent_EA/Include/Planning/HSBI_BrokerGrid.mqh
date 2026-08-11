#ifndef HSBI_BROKER_GRID_MQH
#define HSBI_BROKER_GRID_MQH
#include "../Money/HSBI_BrokerMoneyTypes.mqh"
enum HSBI_GridRoundingMode{HSBI_GRID_FLOOR,HSBI_GRID_CEIL,HSBI_GRID_NEAREST};
enum HSBI_PriceSide{HSBI_PRICE_SIDE_NONE,HSBI_PRICE_SIDE_BID,HSBI_PRICE_SIDE_ASK};
enum HSBI_VolumePurpose{HSBI_VOLUME_BIG_CORE,HSBI_VOLUME_BIG_TREND,HSBI_VOLUME_SMALL_BASE,HSBI_VOLUME_PARTIAL_FAR};
double HSBI_GridTolerance(const double step){return MathMax(1.0e-10,MathAbs(step)*1.0e-8);}
bool HSBI_IsPriceOnTickGrid(const double price,const double tickSize)
{
   if(!HSBI_IsFiniteNumber(price)||!HSBI_IsFiniteNumber(tickSize)||price<=0.0||tickSize<=0.0)return false;
   double ticks=price/tickSize;return MathAbs(ticks-MathRound(ticks))<=HSBI_GridTolerance(tickSize)/tickSize;
}
double HSBI_NormalizePriceToTick(const double price,const double tickSize,const HSBI_GridRoundingMode mode)
{
   if(!HSBI_IsFiniteNumber(price)||!HSBI_IsFiniteNumber(tickSize)||price<=0.0||tickSize<=0.0)return 0.0;
   double ticks=price/tickSize;double units=MathRound(ticks);if(mode==HSBI_GRID_FLOOR)units=MathFloor(ticks+1.0e-12);else if(mode==HSBI_GRID_CEIL)units=MathCeil(ticks-1.0e-12);
   double normalized=units*tickSize;return HSBI_IsPriceOnTickGrid(normalized,tickSize)?normalized:0.0;
}
bool HSBI_ValidatePriceGrid(const double price,const HSBI_BrokerProperties &p){return HSBI_ValidateBrokerProperties(p)==HSBI_BROKER_PROPERTIES_VALID&&HSBI_IsPriceOnTickGrid(price,p.tickSize);}
double HSBI_PriceDistanceInTicks(const double first,const double second,const double tickSize){if(!HSBI_IsFiniteNumber(first)||!HSBI_IsFiniteNumber(second)||tickSize<=0.0)return 0.0;return MathAbs(second-first)/tickSize;}
bool HSBI_IsVolumeOnGrid(const double volume,const double step)
{
   if(!HSBI_IsFiniteNumber(volume)||!HSBI_IsFiniteNumber(step)||volume<=0.0||step<=0.0)return false;
   double units=volume/step;return MathAbs(units-MathRound(units))<=HSBI_GridTolerance(step)/step;
}
double HSBI_FloorVolumeToStep(const double volume,const double step){if(!HSBI_IsFiniteNumber(volume)||!HSBI_IsFiniteNumber(step)||volume<=0.0||step<=0.0)return 0.0;return MathFloor(volume/step+1.0e-12)*step;}
double HSBI_CeilVolumeToStep(const double volume,const double step){if(!HSBI_IsFiniteNumber(volume)||!HSBI_IsFiniteNumber(step)||volume<=0.0||step<=0.0)return 0.0;return MathCeil(volume/step-1.0e-12)*step;}
double HSBI_NormalizeVolume(const double volume,const double step,const HSBI_VolumePurpose purpose)
{
   if(purpose==HSBI_VOLUME_SMALL_BASE)return HSBI_CeilVolumeToStep(volume,step);
   return HSBI_FloorVolumeToStep(volume,step);
}
bool HSBI_ValidateVolume(const double volume,const HSBI_BrokerProperties &p)
{
   if(HSBI_ValidateBrokerProperties(p)!=HSBI_BROKER_PROPERTIES_VALID||!HSBI_IsFiniteNumber(volume))return false;
   return volume>=p.volumeMin-HSBI_GridTolerance(p.volumeStep)&&volume<=p.volumeMax+HSBI_GridTolerance(p.volumeStep)&&HSBI_IsVolumeOnGrid(volume,p.volumeStep);
}
#endif
