#ifndef HSBI_FUTURE_SMALL_SOLVER_MQH
#define HSBI_FUTURE_SMALL_SOLVER_MQH
#include "HSBI_FutureSmallTypes.mqh"
bool HSBI_ValidateFutureSmallInput(const HSBI_FutureSmallInput &x)
{
   if(!x.brokerPropertiesValid||!x.snapshotsFresh||!x.roundingIncluded||!x.costsIncluded)return false;
   if(!x.moneyState.available||!x.moneyState.fresh||!x.riskState.available||!x.riskState.fresh||!x.marginState.available||!x.marginState.fresh||!x.controlPrice.valid||!x.controlPrice.fresh)return false;
   if(x.cycleId==0||x.stateRevision==0||x.planId==0||x.maximumDepth<1||x.maximumDepth>128)return false;
   if(!HSBI_IsFiniteNumber(x.currentFar)||!HSBI_IsFiniteNumber(x.conservativeQ)||!HSBI_IsFiniteNumber(x.volumeStep)||x.currentFar<=0.0||x.volumeStep<=0.0||x.conservativeQ<=0.0||x.conservativeQ>=1.0)return false;
   if(x.maxNewFarRatio<=0.0||x.maxNewFarRatio>=1.0||x.minimumCompressionLots<=0.0||x.minimumCompressionRatio<=0.0||x.minimumCompressionRatio>=1.0)return false;
   if(x.farDirection!=HSBI_DIRECTION_BUY&&x.farDirection!=HSBI_DIRECTION_SELL)return false;
   return true;
}
HSBI_FutureSmallResult HSBI_SolveFutureSmall(const HSBI_FutureSmallInput &x)
{
   HSBI_FutureSmallResult r;ZeroMemory(r);r.status=HSBI_FS_REJECTED;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.planId=x.planId;r.stateRevision=x.stateRevision;r.details="INVALID_INPUT";
   if(!HSBI_ValidateFutureSmallInput(x))return r;
   double logDepth=MathLog(x.volumeMin/x.currentFar)/MathLog(x.conservativeQ);if(!HSBI_IsFiniteNumber(logDepth)||logDepth<0.0){r.details="NONFINITE_DEPTH";return r;}r.theoreticalDepth=(int)MathCeil(logDepth);
   HSBI_BrokerProperties p;ZeroMemory(p);p.symbol=x.controlPrice.symbol;p.point=x.tickSize;p.tickSize=x.tickSize;p.digits=8;p.volumeMin=x.volumeMin;p.volumeMax=x.volumeMax;p.volumeStep=x.volumeStep;p.tickValueProfit=0.0;p.tickValueLoss=0.0;p.valid=true;p.fresh=true;p.snapshotId=x.controlPrice.snapshotId;p.timestamp=TimeCurrent();
   ArrayResize(r.levels,x.maximumDepth);double far=x.currentFar;
   for(int k=0;k<x.maximumDepth;k++)
   {
      HSBI_FutureSmallLevelProof level;ZeroMemory(level);level.levelIndex=k+1;level.farBefore=far;double nextFar=HSBI_FloorVolumeToStep(far*x.conservativeQ,x.volumeStep);level.farAfter=nextFar;level.compressionLots=far-nextFar;level.compressionRatio=level.compressionLots/far;
      if(nextFar<=0.0){if(x.terminalRouteAllowed){ArrayResize(r.levels,k);r.valid=true;r.status=HSBI_FS_EXACT_PROOF;r.finiteSequence=true;r.terminalFar=0.0;r.provenDepth=k;r.reason=HSBI_REASON_OK;r.details="TERMINAL_ROUTE";return r;}r.details="NO_TERMINAL_ROUTE";return r;}
      if(nextFar>=far||level.compressionLots+HSBI_GridTolerance(x.volumeStep)<x.volumeStep){r.plateauDetected=true;r.details="BROKER_GRID_PLATEAU";return r;}
      if(nextFar>x.maxNewFarRatio*far+HSBI_GridTolerance(x.volumeStep)||level.compressionLots<x.minimumCompressionLots-HSBI_GridTolerance(x.volumeStep)||level.compressionRatio<x.minimumCompressionRatio-1.0e-10){r.details="COMPRESSION_FAILED";return r;}
      HSBI_GeometryResult g=HSBI_SolveBigGeometry(far,x.coreRatio,x.trendRatio,x.smallRatio,p,true,true);if(!g.valid){r.details="GEOMETRY_OR_SLOPE_FAILED";return r;}
      level.coreVolume=g.coreVolume;level.trendVolume=g.trendVolume;level.smallVolume=g.smallVolume;level.netBigVolume=g.netBigVolume;level.recoverySlopeLots=g.recoverySlopeLots;level.projectedRecoveryMoney=x.moneyState.recoveryMoney+x.projectedRecoveryMoneyPerLevel*(k+1);level.projectedReserve=x.expectedReserve;level.projectedMargin=x.marginState.currentMargin*MathPow(x.conservativeQ,k+1);level.projectedRisk=x.riskState.currentRisk-x.riskDecreasePerLevel*(k+1);level.transitionLoss=x.transitionLossPerLevel*(k+1);
      double nextExposure=x.currentGrossExposure*MathPow(x.conservativeQ,k+1);if(level.projectedRecoveryMoney<=x.moneyState.recoveryMoney||level.projectedMargin>x.marginState.allowedMargin||level.projectedRisk>=x.riskState.currentRisk-x.riskState.riskTolerance||nextExposure>=x.currentGrossExposure||nextExposure>x.riskState.nextGrossExposureLimit||level.transitionLoss>x.transitionLossCap){r.details="MONEY_RISK_MARGIN_OR_LOSS_FAILED";return r;}
      level.proofStatus=HSBI_FS_EXACT_PROOF;level.reason=HSBI_REASON_OK;r.levels[k]=level;r.provenDepth=k+1;far=nextFar;
   }
   r.terminalFar=far;r.finiteSequence=(far<=x.volumeMin||x.terminalRouteAllowed);r.valid=r.provenDepth==x.maximumDepth;r.status=(r.finiteSequence?HSBI_FS_EXACT_PROOF:HSBI_FS_CONSERVATIVE_BOUND);r.reason=r.valid?HSBI_REASON_OK:HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details=r.valid?(r.finiteSequence?"EXACT_PROOF":"CONSERVATIVE_BOUND"):"UNPROVEN";r.proofDigest=HSBI_UlongToString(x.planId)+"|"+DoubleToString(r.terminalFar,8)+"|"+IntegerToString(r.provenDepth);return r;
}
#endif
