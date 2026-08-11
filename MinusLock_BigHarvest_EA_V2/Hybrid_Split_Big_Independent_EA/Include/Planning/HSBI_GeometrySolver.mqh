#ifndef HSBI_GEOMETRY_SOLVER_MQH
#define HSBI_GEOMETRY_SOLVER_MQH
#include "HSBI_GeometryTypes.mqh"
#include "HSBI_BrokerGrid.mqh"
struct HSBI_GeometryResult{HSBI_CalculationStatus status;bool valid;double farVolume;double rawCoreVolume;double rawTrendVolume;double rawSmallVolume;double coreVolume;double trendVolume;double smallVolume;double netBigVolume;double recoverySlopeLots;bool coreRoundedDown;bool trendRoundedDown;bool smallRoundedUp;bool slopePassed;bool brokerGridPassed;ulong snapshotId;HSBI_ReasonCode reason;string details;};
bool HSBI_ValidateRecoverySlope(const double coreVolume,const double trendVolume,const double smallVolume,const double farVolume,const bool brokerGridPassed,double &slope)
{
   slope=0.0;if(!brokerGridPassed||!HSBI_IsFiniteNumber(coreVolume)||!HSBI_IsFiniteNumber(trendVolume)||!HSBI_IsFiniteNumber(smallVolume)||!HSBI_IsFiniteNumber(farVolume))return false;
   if(coreVolume<0.0||trendVolume<0.0||smallVolume<=0.0||farVolume<=0.0)return false;
   slope=coreVolume+trendVolume-smallVolume-farVolume;return HSBI_IsFiniteNumber(slope)&&slope>0.0;
}
HSBI_GeometryResult HSBI_SolveBigGeometry(const double farVolume,const double coreRatio,const double trendRatio,const double smallRatio,const HSBI_BrokerProperties &p,const bool moneyPrerequisite,const bool riskPrerequisite)
{
   HSBI_GeometryResult r;ZeroMemory(r);r.status=HSBI_CALC_REJECT;r.reason=HSBI_REASON_INVALID_VOLUME;r.details="INVALID_GEOMETRY";r.farVolume=farVolume;r.snapshotId=p.snapshotId;
   if(HSBI_ValidateBrokerProperties(p)!=HSBI_BROKER_PROPERTIES_VALID){r.status=HSBI_CALC_UNAVAILABLE;r.details="INVALID_BROKER_GRID";return r;}
   if(!moneyPrerequisite||!riskPrerequisite){r.details="FAILED_MONEY_OR_RISK_PREREQUISITE";return r;}
   if(!HSBI_IsFiniteNumber(coreRatio)||!HSBI_IsFiniteNumber(trendRatio)||!HSBI_IsFiniteNumber(smallRatio)||coreRatio<=0.0||trendRatio<0.0||smallRatio<=0.0){r.details="INVALID_RATIO";return r;}
   if(!HSBI_ValidateVolume(farVolume,p)){r.details="INVALID_FAR_VOLUME";return r;}
   r.rawCoreVolume=farVolume*coreRatio;r.rawTrendVolume=farVolume*trendRatio;r.rawSmallVolume=farVolume*smallRatio;
   if(!HSBI_IsFiniteNumber(r.rawCoreVolume)||!HSBI_IsFiniteNumber(r.rawTrendVolume)||!HSBI_IsFiniteNumber(r.rawSmallVolume)){r.status=HSBI_CALC_ERROR;r.details="VOLUME_OVERFLOW";return r;}
   r.coreVolume=HSBI_FloorVolumeToStep(r.rawCoreVolume,p.volumeStep);r.trendVolume=(r.rawTrendVolume==0.0?0.0:HSBI_FloorVolumeToStep(r.rawTrendVolume,p.volumeStep));r.smallVolume=HSBI_CeilVolumeToStep(r.rawSmallVolume,p.volumeStep);
   r.coreRoundedDown=r.coreVolume<=r.rawCoreVolume+HSBI_GridTolerance(p.volumeStep);r.trendRoundedDown=r.trendVolume<=r.rawTrendVolume+HSBI_GridTolerance(p.volumeStep);r.smallRoundedUp=r.smallVolume+HSBI_GridTolerance(p.volumeStep)>=r.rawSmallVolume;
   bool coreGrid=(r.coreVolume==0.0||(HSBI_IsVolumeOnGrid(r.coreVolume,p.volumeStep)&&r.coreVolume<=p.volumeMax));bool trendGrid=(r.trendVolume==0.0||(HSBI_IsVolumeOnGrid(r.trendVolume,p.volumeStep)&&r.trendVolume<=p.volumeMax));
   r.brokerGridPassed=coreGrid&&trendGrid&&HSBI_ValidateVolume(r.smallVolume,p);if(!r.brokerGridPassed){r.details="INVALID_NORMALIZED_VOLUME";return r;}
   r.netBigVolume=r.coreVolume+r.trendVolume-r.smallVolume;r.slopePassed=HSBI_ValidateRecoverySlope(r.coreVolume,r.trendVolume,r.smallVolume,r.farVolume,r.brokerGridPassed,r.recoverySlopeLots)&&r.recoverySlopeLots>HSBI_GridTolerance(p.volumeStep);
   if(r.netBigVolume<=0.0||!r.slopePassed){r.details="RECOVERY_SLOPE_FAILED";return r;}
   r.status=HSBI_CALC_PASS;r.valid=true;r.reason=HSBI_REASON_OK;r.details="PASS";return r;
}
#endif
