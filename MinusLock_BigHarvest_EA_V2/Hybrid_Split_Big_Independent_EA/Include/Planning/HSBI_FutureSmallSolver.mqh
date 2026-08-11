#ifndef HSBI_FUTURE_SMALL_SOLVER_MQH
#define HSBI_FUTURE_SMALL_SOLVER_MQH
#include "HSBI_FutureSmallTypes.mqh"
bool HSBI_CalculateFutureSmallDepth(const double f,const double vmin,const double q,const double step,int &depth)
{
   depth=0; if(!HSBI_IsFiniteNumber(f)||!HSBI_IsFiniteNumber(vmin)||!HSBI_IsFiniteNumber(q)||
      !HSBI_IsFiniteNumber(step)||f<=0.0||vmin<=0.0||vmin>f||q<=0.0||q>=1.0||step<=0.0) return false;
   double value=MathLog(vmin/f)/MathLog(q); if(!HSBI_IsFiniteNumber(value)||value<0.0||value>2147483647.0) return false;
   depth=(int)MathCeil(value); return true;
}
bool HSBI_ValidateConservativeBound(const double initialFar,const double observedFar,const double q,const int depth,
   const bool rounding,const bool costs,const bool margin,const bool risk,const bool loss)
{
   return depth>=2&&q>0.0&&q<1.0&&rounding&&costs&&margin&&risk&&loss&&initialFar>0.0&&observedFar>0.0&&
      observedFar<=initialFar*MathPow(q,depth)+1e-10;
}
bool HSBI_ValidateLevelMarket(const HSBI_FutureSmallLevelMarketSnapshot &m,const int level,const HSBI_BrokerProperties &b,const HSBI_Direction d)
{
   if(m.levelIndex!=level||!m.valid||!m.fresh||!m.normalized||m.snapshotId==0||m.timestamp<=0||m.symbol!=b.symbol||
      !HSBI_IsFiniteNumber(m.bid)||!HSBI_IsFiniteNumber(m.ask)||!HSBI_IsFiniteNumber(m.selectedPrice)||m.bid<=0.0||m.ask<m.bid||
      MathAbs(m.tickSize-b.tickSize)>HSBI_GridTolerance(b.tickSize)||!HSBI_IsPriceOnTickGrid(m.selectedPrice,m.tickSize)) return false;
   if(d==HSBI_DIRECTION_BUY) return m.side==HSBI_PRICE_SIDE_BID&&MathAbs(m.selectedPrice-m.bid)<=HSBI_GridTolerance(m.tickSize);
   if(d==HSBI_DIRECTION_SELL) return m.side==HSBI_PRICE_SIDE_ASK&&MathAbs(m.selectedPrice-m.ask)<=HSBI_GridTolerance(m.tickSize);
   return false;
}
bool HSBI_ValidateLevelCosts(const HSBI_FutureSmallLevelCostSnapshot &c,const int level)
{
   return c.levelIndex==level&&c.valid&&c.fresh&&c.snapshotId>0&&HSBI_ValidateCostSnapshot(c.farCosts,false)&&
      HSBI_ValidateCostSnapshot(c.coreCosts,false)&&HSBI_ValidateCostSnapshot(c.trendCosts,false)&&HSBI_ValidateCostSnapshot(c.smallCosts,false);
}
bool HSBI_ValidateFarProjection(const HSBI_FutureFarProjection &p,const HSBI_BrokerProperties &b,const double before)
{
   if(!p.valid||!p.projected||p.actual||!p.confirmed||p.source==HSBI_FAR_PROJECTION_UNAVAILABLE||p.projectedFar<=0.0||
      p.projectedFar>=before||!HSBI_ValidateVolume(p.projectedFar,b)) return false;
   if(p.source==HSBI_FAR_PROJECTION_BIGCORE_RESIDUAL) return p.sourceIdentifier>0&&p.sourceDealId>0;
   return p.source==HSBI_FAR_PROJECTION_EXPLICIT_MODEL&&p.sourceIdentifier>0;
}
HSBI_ControlPrice HSBI_LevelControlPrice(const HSBI_FutureSmallLevelMarketSnapshot &m,const HSBI_BrokerProperties &b,const HSBI_Direction d)
{
   HSBI_ControlPrice p; ZeroMemory(p); p.symbol=m.symbol;p.bid=m.bid;p.ask=m.ask;p.mid=(m.bid+m.ask)/2.0;
   p.selectedPrice=m.selectedPrice;p.direction=d;p.side=m.side;p.point=b.point;p.tickSize=m.tickSize;p.digits=b.digits;
   p.timestamp=m.timestamp;p.snapshotId=m.snapshotId;p.fresh=m.fresh;p.normalized=m.normalized;p.valid=m.valid;return p;
}
bool HSBI_ValidateFutureSmallInput(const HSBI_FutureSmallInput &x)
{
   if(x.testOnlyApproximation||!HSBI_ValidateAllocationPolicy(x.allocationPolicy)||!x.brokerPropertiesValid||!x.snapshotsFresh||
      !x.roundingIncluded||!x.costsIncluded||!x.moneyState.available||!x.moneyState.fresh||!x.riskState.available||
      !x.riskState.fresh||!x.marginState.available||!x.marginState.fresh) return false;
   if(HSBI_ValidateBrokerProperties(x.broker)!=HSBI_BROKER_PROPERTIES_VALID||x.cycleId==0||x.stateRevision==0||x.planId==0||
      x.maximumDepth<2||x.maximumDepth>128||x.levelMarketSnapshotCount<x.maximumDepth||x.levelCostSnapshotCount<x.maximumDepth||
      x.farProjectionCount<x.maximumDepth||x.currentFar<=0.0||x.volumeStep<=0.0||x.conservativeQ<=0.0||x.conservativeQ>=1.0) return false;
   if(x.maxNewFarRatio<=0.0||x.maxNewFarRatio>=1.0||x.minimumCompressionLots<=0.0||
      x.minimumCompressionRatio<=0.0||x.minimumCompressionRatio>=1.0) return false;
   return x.farDirection==HSBI_DIRECTION_BUY||x.farDirection==HSBI_DIRECTION_SELL;
}
HSBI_FutureSmallLevelResult HSBI_EvaluateFutureSmallLevel(const HSBI_FutureSmallLevelInput &x)
{
   HSBI_FutureSmallLevelResult r; ZeroMemory(r);r.levelIndex=x.levelIndex;r.farBefore=x.farBefore;
   r.status=HSBI_FS_UNPROVEN;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details="LEVEL_UNPROVEN";
   if(x.testOnlyApproximation||!HSBI_ValidateLevelMarket(x.market,x.levelIndex,x.broker,x.farProjection.source==HSBI_FAR_PROJECTION_UNAVAILABLE?HSBI_DIRECTION_NONE:x.market.side==HSBI_PRICE_SIDE_BID?HSBI_DIRECTION_BUY:HSBI_DIRECTION_SELL)||
      !HSBI_ValidateLevelCosts(x.costs,x.levelIndex)||!HSBI_ValidateFarProjection(x.farProjection,x.broker,x.farBefore)) return r;
   HSBI_GeometryResult g=HSBI_SolveBigGeometry(x.farBefore,x.coreRatio,x.trendRatio,x.smallRatio,x.broker,true,true);
   if(!g.valid){r.details="GEOMETRY_FAILED";return r;}
   r.coreVolume=g.coreVolume;r.trendVolume=g.trendVolume;r.smallVolume=g.smallVolume;r.netBigVolume=g.netBigVolume;
   r.recoverySlopeLots=g.recoverySlopeLots;r.farAfter=x.farProjection.projectedFar;
   r.compressionLots=x.farBefore-r.farAfter;r.compressionRatio=r.compressionLots/x.farBefore;
   if(r.farAfter>x.maxNewFarRatio*x.farBefore+HSBI_GridTolerance(x.broker.volumeStep)||
      r.compressionLots<x.minimumCompressionLots-HSBI_GridTolerance(x.broker.volumeStep)||r.compressionRatio<x.minimumCompressionRatio-1e-10) {
      r.details="COMPRESSION_FAILED";return r;
   }
   HSBI_BasketMoneyResult basket;
   if(x.useInjectedBrokerProof){basket=x.injectedBrokerProof;if(!basket.valid||!basket.brokerRuntimeConfirmed){r.details="INJECTED_PROOF_UNCONFIRMED";return r;}}
   else {
      HSBI_BasketMoneyInput bi;ZeroMemory(bi);bi.farVolume=x.farBefore;bi.coreVolume=g.coreVolume;bi.trendVolume=g.trendVolume;bi.smallVolume=g.smallVolume;
      bi.farDirection=(x.market.side==HSBI_PRICE_SIDE_BID?HSBI_DIRECTION_BUY:HSBI_DIRECTION_SELL);bi.symbol=x.broker.symbol;bi.broker=x.broker;
      bi.controlPrice=HSBI_LevelControlPrice(x.market,x.broker,bi.farDirection);bi.farOpenPrice=x.farOpenPrice;bi.coreOpenPrice=x.coreOpenPrice;
      bi.trendOpenPrice=x.trendOpenPrice;bi.smallOpenPrice=x.smallOpenPrice;bi.farCosts=x.costs.farCosts;bi.coreCosts=x.costs.coreCosts;
      bi.trendCosts=x.costs.trendCosts;bi.smallCosts=x.costs.smallCosts;bi.executionSafetyBuffer=x.executionSafetyBuffer;bi.snapshotId=x.market.snapshotId;
      basket=HSBI_EvaluateBasketMoney(bi);
   }
   r.basketProof=basket;if(!basket.valid){r.details="BROKER_MONEY_OR_MARGIN_UNAVAILABLE";return r;}
   HSBI_FutureSmallRiskInput ri;ZeroMemory(ri);ri.basket=basket;ri.priorRisk=x.riskState.currentRisk;ri.tolerance=x.riskState.riskTolerance;
   ri.evaluatedRisk=x.evaluatedRisk;ri.source=x.riskProofSource;ri.runtimeConfirmed=x.riskRuntimeConfirmed;ri.testOnly=x.riskTestOnly;
   ri.fresh=x.riskState.fresh;ri.snapshotId=x.riskProofSnapshotId;
   HSBI_FutureSmallRiskResult risk=HSBI_EvaluateFutureSmallRisk(ri);if(!risk.valid){r.details="RISK_RUNTIME_PROOF_UNAVAILABLE_OR_FAILED";return r;}
   r.recoveryMoney=basket.recoveryMoney;r.totalMargin=basket.totalMargin;r.grossExposure=basket.grossExposure;r.transitionLoss=basket.transitionLoss;
   r.riskValue=risk.riskValue;r.moneyIncluded=true;r.marginIncluded=true;r.riskIncluded=true;r.transitionLossIncluded=true;
   if(r.recoveryMoney<=x.moneyState.recoveryMoney||r.totalMargin>x.marginState.allowedMargin||r.grossExposure>=x.priorGrossExposure||
      r.netBigVolume>=x.priorBigGross||r.transitionLoss>x.transitionLossCap){r.details="LEVEL_GATES_FAILED";return r;}
   r.valid=true;r.status=HSBI_FS_EXACT_PROOF;r.reason=HSBI_REASON_OK;r.details="EXACT_LEVEL";return r;
}
string HSBI_FutureSmallLevelDigest(const HSBI_FutureSmallLevelProof &p)
{
   return IntegerToString(p.levelIndex)+"|"+DoubleToString(p.farBefore,8)+"|"+DoubleToString(p.farAfter,8)+"|"+
      DoubleToString(p.coreVolume,8)+"|"+DoubleToString(p.trendVolume,8)+"|"+DoubleToString(p.smallVolume,8)+"|"+
      DoubleToString(p.netBigVolume,8)+"|"+DoubleToString(p.recoverySlopeLots,8)+"|"+DoubleToString(p.projectedRecoveryMoney,8)+"|"+
      DoubleToString(p.projectedMargin,8)+"|"+DoubleToString(p.grossExposure,8)+"|"+DoubleToString(p.projectedRisk,8)+"|"+
      DoubleToString(p.transitionLoss,8)+"|"+DoubleToString(p.compressionLots,8)+"|"+DoubleToString(p.compressionRatio,12)+"|"+
      DoubleToString(p.controlPrice,8)+"|"+DoubleToString(p.bid,8)+"|"+DoubleToString(p.ask,8)+"|"+DoubleToString(p.tickSize,8)+"|"+
      HSBI_UlongToString(p.controlSnapshotId)+"|"+HSBI_UlongToString(p.farCostSnapshotId)+"|"+HSBI_UlongToString(p.coreCostSnapshotId)+"|"+
      HSBI_UlongToString(p.trendCostSnapshotId)+"|"+HSBI_UlongToString(p.smallCostSnapshotId)+"|"+IntegerToString((int)p.moneyProofStatus)+"|"+
      IntegerToString((int)p.marginProofStatus)+"|"+IntegerToString((int)p.riskProofStatus)+"|"+IntegerToString((int)p.transitionLossProofStatus)+"|"+
      IntegerToString((int)p.proofStatus)+"|"+IntegerToString((int)p.reason);
}
string HSBI_FutureSmallProofDigest(const HSBI_FutureSmallResult &r)
{
   string d="FS|"+HSBI_UlongToString(r.planId)+"|"+HSBI_UlongToString(r.stateRevision);
   for(int i=0;i<r.provenDepth;i++) d+="|L|"+HSBI_FutureSmallLevelDigest(r.levels[i]);
   return d+"|END|"+IntegerToString((int)r.status)+"|"+IntegerToString(r.provenDepth)+"|"+
      DoubleToString(r.terminalFar,8)+"|"+IntegerToString((int)r.finiteSequence)+"|"+IntegerToString((int)r.plateauDetected);
}
HSBI_FutureSmallResult HSBI_SolveFutureSmall(const HSBI_FutureSmallInput &x)
{
   HSBI_FutureSmallResult r;ZeroMemory(r);r.status=HSBI_FS_REJECTED;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;
   r.planId=x.planId;r.stateRevision=x.stateRevision;r.details="INVALID_INPUT";if(!HSBI_ValidateFutureSmallInput(x))return r;
   if(!HSBI_CalculateFutureSmallDepth(x.currentFar,x.volumeMin,x.conservativeQ,x.volumeStep,r.theoreticalDepth)){r.details="NONFINITE_DEPTH";return r;}
   double far=x.currentFar,priorBig=x.currentBigGross,priorExposure=x.currentGrossExposure;HSBI_MoneyStateSnapshot money=x.moneyState;
   HSBI_RiskSnapshot risk=x.riskState;HSBI_MarginSnapshot margin=x.marginState;bool terminal=false,boundConditions=true;
   for(int k=0;k<x.maximumDepth;k++) {
      HSBI_FutureSmallLevelInput li;ZeroMemory(li);li.levelIndex=k+1;li.farBefore=far;li.coreRatio=x.coreRatio;li.trendRatio=x.trendRatio;
      li.smallRatio=x.smallRatio;li.broker=x.broker;li.market=x.levelMarketSnapshots[k];li.costs=x.levelCostSnapshots[k];li.farProjection=x.farProjections[k];
      li.farOpenPrice=x.farOpenPrice;li.coreOpenPrice=x.coreOpenPrice;li.trendOpenPrice=x.trendOpenPrice;li.smallOpenPrice=x.smallOpenPrice;
      li.moneyState=money;li.riskState=risk;li.marginState=margin;li.minimumCompressionLots=x.minimumCompressionLots;
      li.minimumCompressionRatio=x.minimumCompressionRatio;li.maxNewFarRatio=x.maxNewFarRatio;li.transitionLossCap=x.transitionLossCap;
      li.executionSafetyBuffer=x.executionSafetyBuffer;li.priorBigGross=priorBig;li.priorGrossExposure=priorExposure;li.planId=x.planId;li.stateRevision=x.stateRevision;
      li.evaluatedRisk=x.evaluatedRisks[k];li.riskProofSource=x.riskProofSources[k];li.riskRuntimeConfirmed=x.riskRuntimeConfirmed[k];
      li.riskTestOnly=x.riskTestOnly[k];li.riskProofSnapshotId=x.riskProofSnapshotIds[k];li.useInjectedBrokerProof=x.useInjectedBrokerProofs;
      li.testOnlyApproximation=x.testOnlyApproximation;if(x.useInjectedBrokerProofs)li.injectedBrokerProof=x.injectedBrokerProofs[k];
      HSBI_FutureSmallLevelResult level=HSBI_EvaluateFutureSmallLevel(li);if(!level.valid){r.details=level.details;r.proofDigest=HSBI_FutureSmallProofDigest(r);return r;}
      HSBI_FutureSmallLevelProof p;ZeroMemory(p);p.levelIndex=level.levelIndex;p.farBefore=level.farBefore;p.farAfter=level.farAfter;
      p.coreVolume=level.coreVolume;p.trendVolume=level.trendVolume;p.smallVolume=level.smallVolume;p.netBigVolume=level.netBigVolume;
      p.compressionLots=level.compressionLots;p.compressionRatio=level.compressionRatio;p.recoverySlopeLots=level.recoverySlopeLots;
      p.projectedRecoveryMoney=level.recoveryMoney;p.projectedReserve=x.expectedReserve;p.projectedMargin=level.totalMargin;p.projectedRisk=level.riskValue;
      p.transitionLoss=level.transitionLoss;p.grossExposure=level.grossExposure;p.controlPrice=li.market.selectedPrice;p.bid=li.market.bid;p.ask=li.market.ask;
      p.tickSize=li.market.tickSize;p.controlSnapshotId=li.market.snapshotId;p.farCostSnapshotId=li.costs.farCosts.snapshotId;
      p.coreCostSnapshotId=li.costs.coreCosts.snapshotId;p.trendCostSnapshotId=li.costs.trendCosts.snapshotId;p.smallCostSnapshotId=li.costs.smallCosts.snapshotId;
      p.moneyIncluded=level.moneyIncluded;p.marginIncluded=level.marginIncluded;p.riskIncluded=level.riskIncluded;p.transitionLossIncluded=level.transitionLossIncluded;
      p.moneyProofStatus=level.basketProof.status;p.marginProofStatus=level.basketProof.status;p.riskProofStatus=HSBI_CALC_PASS;
      p.transitionLossProofStatus=level.basketProof.status;p.reserveSourceProof=level.basketProof.core;p.farLossProof=level.basketProof.far;p.proofStatus=HSBI_FS_EXACT_PROOF;p.reason=HSBI_REASON_OK;p.levelDigest=HSBI_FutureSmallLevelDigest(p);
      r.levels[k]=p;r.provenDepth=k+1;
      if(level.farAfter>x.conservativeQ*level.farBefore+HSBI_GridTolerance(x.volumeStep))boundConditions=false;
      far=level.farAfter;priorBig=level.netBigVolume;priorExposure=level.grossExposure;money.recoveryMoney=level.recoveryMoney;
      risk.currentRisk=level.riskValue;margin.currentMargin=level.totalMargin;if(far<=x.volumeMin+HSBI_GridTolerance(x.volumeStep)){terminal=true;break;}
   }
   r.terminalFar=far;r.finiteSequence=terminal;bool bound=boundConditions&&HSBI_ValidateConservativeBound(x.currentFar,far,x.conservativeQ,r.provenDepth,x.roundingIncluded,x.costsIncluded,true,true,true);
   r.valid=r.provenDepth>=2&&(terminal||bound);r.status=terminal&&r.provenDepth>=2?HSBI_FS_EXACT_PROOF:(bound?HSBI_FS_CONSERVATIVE_BOUND:HSBI_FS_UNPROVEN);
   r.reason=r.valid?HSBI_REASON_OK:HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details=r.valid?(r.status==HSBI_FS_EXACT_PROOF?"EXACT_PROOF":"CONSERVATIVE_BOUND"):"UNPROVEN";
   r.proofDigest=HSBI_FutureSmallProofDigest(r);return r;
}
#endif
