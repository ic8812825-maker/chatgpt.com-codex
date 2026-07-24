#ifndef __BH_HYBRID_DECISION_ENGINE_MQH__
#define __BH_HYBRID_DECISION_ENGINE_MQH__
// Frozen-snapshot pre-open gate. Trading modules must consume its plan only on PASS.
bool EvaluateHybridCandidate(const HybridCycleSnapshot &s,HybridCandidatePlan &p,HybridEvaluationResult &r)
{
 r.finalCode=HYBRID_CANDIDATE_REJECTED;r.rejectCode=HYBRID_REJECT_NONE;r.errorCode=HYBRID_ERROR_NONE;r.terminalCode=HYBRID_TERMINAL_NONE;r.passed=false;r.terminal=false;r.failedStage="";r.reason="";r.trace="";
 if(!UseHybridSplitBigGeometry){r.finalCode=HYBRID_CANDIDATE_ALLOWED;r.passed=true;r.reason="HYBRID_DISABLED";return true;}
 if(s.symbol!=_Symbol||s.magic!=MagicNumber||s.cycleId==0||s.farLot<=0){r.rejectCode=HYBRID_REJECT_IDENTITY;r.failedStage="IDENTITY";r.reason="HYBRID_IDENTITY";return false;}
 if(TargetNewFarRatio<=0||TargetNewFarRatio>=1||BigCoreRatio<=0||BigTrendRatio<=0||SmallBaseToFarRatio<=0){r.rejectCode=HYBRID_REJECT_CONFIG;r.failedStage="CONFIG";r.reason="HYBRID_CONFIG";return false;}
 p.coreLot=NormalizeLotDown(s.farLot*BigCoreRatio);p.trendLot=NormalizeLotDown(s.farLot*BigTrendRatio);p.smallLot=NormalizeLotDown(s.farLot*SmallBaseToFarRatio);p.newFarLot=NormalizeLotDown(s.farLot*TargetNewFarRatio);
 if(p.coreLot<=0||p.trendLot<=0||p.smallLot<=0||p.newFarLot<=0||p.newFarLot>=s.farLot){r.rejectCode=HYBRID_REJECT_VOLUME;r.failedStage="VOLUME";r.reason="HYBRID_VOLUME";return false;}
 double catchUp=WorkReserveShare*(p.coreLot+p.trendLot-p.smallLot)/s.farLot;
 if(catchUp<MinimumReserveCatchUpRatio){r.rejectCode=HYBRID_REJECT_LAW1;r.failedStage="LAW1";r.reason="HYBRID_CATCHUP";return false;}
 if(p.coreLot+p.trendLot-p.smallLot-s.farLot<=0){r.rejectCode=HYBRID_REJECT_LAW2;r.failedStage="LAW2";r.reason="HYBRID_SLOPE";return false;}
 p.nextBigGross=NormalizeLotDown(p.newFarLot*BigCoreRatio)+NormalizeLotDown(p.newFarLot*BigTrendRatio);
 if(p.nextBigGross>=s.farLot*MaximumNewBigToOldFarRatio){r.rejectCode=HYBRID_REJECT_NEXT_BIG;r.failedStage="NEXT_BIG";r.reason="HYBRID_NEXT_BIG";return false;}
 r.finalCode=HYBRID_CANDIDATE_ALLOWED;r.passed=true;r.reason="PASS";r.trace=StringFormat("KR=%.5f NewFar=%.2f NextBig=%.2f",catchUp,p.newFarLot,p.nextBigGross);return true;
}
#endif
