#ifndef __BH_HYBRID_DECISION_ENGINE_MQH__
#define __BH_HYBRID_DECISION_ENGINE_MQH__

void HybridResetResult(HybridEvaluationResult &r)
{
   r.applicable=true; r.evaluated=false; r.passed=false; r.terminal=false;
   r.finalCode=HYBRID_FINAL_NONE; r.failedGate=HYBRID_GATE_IDENTITY;
   r.rejectCode=HYBRID_REJECT_NONE; r.errorCode=HYBRID_ERROR_NONE; r.terminalCode=HYBRID_TERMINAL_NONE;
   r.evaluatedGateMask=0; r.passedGateMask=0; r.failedStage=""; r.reason=""; r.trace="";
}

void HybridMarkGateEvaluated(HybridEvaluationResult &result,HybridGateCode gate)
{
   result.evaluatedGateMask |= ((ulong)1 << (int)gate);
}

void HybridMarkGatePass(HybridEvaluationResult &result,HybridGateCode gate)
{
   HybridMarkGateEvaluated(result,gate);
   result.passedGateMask |= ((ulong)1 << (int)gate);
}

bool HybridFail(HybridEvaluationResult &r,HybridGateCode gate,HybridRejectCode rejectCode,string stage,string reason)
{
   HybridMarkGateEvaluated(r,gate);
   r.evaluated=true; r.passed=false; r.finalCode=HYBRID_CANDIDATE_REJECTED;
   r.failedGate=gate; r.rejectCode=rejectCode; r.failedStage=stage; r.reason=reason;
   return false;
}

bool HybridError(HybridEvaluationResult &r,HybridGateCode gate,HybridErrorCode errorCode,string stage,string reason)
{
   HybridMarkGateEvaluated(r,gate);
   r.evaluated=true; r.passed=false; r.finalCode=HYBRID_CANDIDATE_REJECTED;
   r.failedGate=gate; r.errorCode=errorCode; r.failedStage=stage; r.reason=reason;
   return false;
}

bool ValidateHybridAllocationConfig(string &reason)
{
   reason="";
   if(!MathIsValidNumber(HybridPartialFarShare) || !MathIsValidNumber(HybridFinalReserveShare) || !MathIsValidNumber(HybridCarryShare)) { reason="HYBRID_ALLOCATION_NOT_FINITE"; return false; }
   if(HybridPartialFarShare<0 || HybridFinalReserveShare<0 || HybridCarryShare<0) { reason="HYBRID_ALLOCATION_NEGATIVE"; return false; }
   double sum=HybridPartialFarShare+HybridFinalReserveShare+HybridCarryShare;
   if(MathAbs(sum-1.0)>MoneyCalculationTolerance) { reason=StringFormat("HYBRID_ALLOCATION_SUM %.8f",sum); return false; }
   return true;
}

bool ValidateHybridSnapshot(const HybridCycleSnapshot &snapshot,HybridEvaluationResult &result)
{
   if(snapshot.symbol=="" || snapshot.symbol!=_Symbol) return HybridFail(result,HYBRID_GATE_IDENTITY,HYBRID_REJECT_IDENTITY,"IDENTITY","HYBRID_SYMBOL_MISMATCH");
   if(snapshot.magic!=MagicNumber) return HybridFail(result,HYBRID_GATE_IDENTITY,HYBRID_REJECT_IDENTITY,"IDENTITY","HYBRID_MAGIC_MISMATCH");
   if(snapshot.cycleId==0) return HybridFail(result,HYBRID_GATE_IDENTITY,HYBRID_REJECT_IDENTITY,"IDENTITY","HYBRID_CYCLE_ID_INVALID");
   if(snapshot.farIdentifier==0) return HybridFail(result,HYBRID_GATE_IDENTITY,HYBRID_REJECT_IDENTITY,"IDENTITY","HYBRID_FAR_IDENTIFIER_INVALID");
   if(snapshot.farDirection!=DIR_BUY && snapshot.farDirection!=DIR_SELL) return HybridFail(result,HYBRID_GATE_IDENTITY,HYBRID_REJECT_IDENTITY,"IDENTITY","HYBRID_FAR_DIRECTION_INVALID");
   if(snapshot.farLot<=0 || snapshot.farOpenPrice<=0) return HybridFail(result,HYBRID_GATE_IDENTITY,HYBRID_REJECT_IDENTITY,"IDENTITY","HYBRID_FAR_INVALID");
   if(snapshot.bid<=0 || snapshot.ask<=0 || snapshot.ask<snapshot.bid) return HybridFail(result,HYBRID_GATE_IDENTITY,HYBRID_REJECT_IDENTITY,"IDENTITY","HYBRID_MARKET_INVALID");
   if(snapshot.equity<=0 || snapshot.margin<0 || snapshot.freeMargin<0) return HybridFail(result,HYBRID_GATE_IDENTITY,HYBRID_REJECT_IDENTITY,"IDENTITY","HYBRID_ACCOUNT_MONEY_INVALID");
   if(!MathIsValidNumber(snapshot.farLot) || !MathIsValidNumber(snapshot.farOpenPrice) || !MathIsValidNumber(snapshot.bid) || !MathIsValidNumber(snapshot.ask) || !MathIsValidNumber(snapshot.equity) || !MathIsValidNumber(snapshot.margin) || !MathIsValidNumber(snapshot.freeMargin)) return HybridError(result,HYBRID_GATE_IDENTITY,HYBRID_ERROR_INVALID_SNAPSHOT,"IDENTITY","HYBRID_SNAPSHOT_NOT_FINITE");
   long marginMode=AccountInfoInteger(ACCOUNT_MARGIN_MODE);
   if(!UseInternalSimulation && marginMode!=ACCOUNT_MARGIN_MODE_RETAIL_HEDGING) return HybridFail(result,HYBRID_GATE_IDENTITY,HYBRID_REJECT_IDENTITY,"IDENTITY","HYBRID_REQUIRES_HEDGING_ACCOUNT");
   HybridMarkGatePass(result,HYBRID_GATE_IDENTITY);
   return true;
}

bool ValidateHybridConfiguration(HybridEvaluationResult &result)
{
   string reason="";
   if(!ValidateHybridAllocationConfig(reason)) return HybridFail(result,HYBRID_GATE_CONFIG,HYBRID_REJECT_CONFIG_ALLOCATION,"CONFIG",reason);
   if(BigCoreRatio<=0 || BigTrendRatio<=0 || SmallBaseToFarRatio<=0) return HybridFail(result,HYBRID_GATE_CONFIG,HYBRID_REJECT_CONFIG,"CONFIG","HYBRID_RATIO_INVALID");
   if(TargetNewFarRatio<=0 || TargetNewFarRatio>=1 || MaximumNewBigToOldFarRatio<=0 || MaximumNewBigToOldFarRatio>=1.0+MoneyCalculationTolerance) return HybridFail(result,HYBRID_GATE_CONFIG,HYBRID_REJECT_CONFIG,"CONFIG","HYBRID_TARGET_OR_NEXT_BIG_LIMIT_INVALID");
   if(MinimumReserveCatchUpRatio<=0 || MinimumRecoverySlopeMoneyPerPoint<0 || MaximumTransitionLossMoney<0 || MaxMarginPercent<=0 || MinimumSafeMarginLevel<=0) return HybridFail(result,HYBRID_GATE_CONFIG,HYBRID_REJECT_CONFIG,"CONFIG","HYBRID_LIMIT_INVALID");
   double thirdLaw=(BigCoreRatio+BigTrendRatio)*TargetNewFarRatio;
   if(thirdLaw>=MaximumNewBigToOldFarRatio+MoneyCalculationTolerance) return HybridFail(result,HYBRID_GATE_CONFIG,HYBRID_REJECT_CONFIG,"CONFIG",StringFormat("HYBRID_THIRD_LAW_CONFIG %.6f >= %.6f",thirdLaw,MaximumNewBigToOldFarRatio));
   if(!ValidateCommissionModel(reason)) return HybridFail(result,HYBRID_GATE_CONFIG,HYBRID_REJECT_CONFIG,"CONFIG",reason);
   HybridMarkGatePass(result,HYBRID_GATE_CONFIG);
   return true;
}

Direction HybridOpposite(Direction d)
{
   if(d==DIR_BUY) return DIR_SELL;
   if(d==DIR_SELL) return DIR_BUY;
   return DIR_NONE;
}

bool EvaluateHybridBaseMoneyPreview(const HybridCycleSnapshot &s,HybridCandidatePlan &p,HybridEvaluationResult &r)
{
   double point=SymbolInfoDouble(_Symbol,SYMBOL_POINT);
   if(point<=0) return HybridError(r,HYBRID_GATE_BASE_MONEY,HYBRID_ERROR_ORDER_CALC_PROFIT,"BASE_MONEY","HYBRID_POINT_INVALID");
   double bigMovePrice = p.bigDirection==DIR_BUY ? s.ask + BigMoveStartPoints*point : s.bid - BigMoveStartPoints*point;
   BrokerMoneyResult core,trend,small;
   bool ok=CalcProjectedPositionNetMoney(p.bigDirection,p.coreLot,p.bigDirection==DIR_BUY?s.ask:s.bid,bigMovePrice,true,true,core)
         && CalcProjectedPositionNetMoney(p.bigDirection,p.trendLot,p.bigDirection==DIR_BUY?s.ask:s.bid,bigMovePrice,true,true,trend)
         && CalcProjectedPositionNetMoney(p.smallDirection,p.smallLot,p.smallDirection==DIR_BUY?s.ask:s.bid,bigMovePrice,true,true,small);
   if(!ok) return HybridError(r,HYBRID_GATE_BASE_MONEY,HYBRID_ERROR_ORDER_CALC_PROFIT,"BASE_MONEY","HYBRID_ORDER_CALC_PROFIT_FAILED");
   p.projectedHarvestNet=core.netMoney+trend.netMoney+small.netMoney;
   double eligible=MathMax(0.0,p.projectedHarvestNet);
   p.projectedReserveAdd=HybridFinalReserveShare*eligible;
   p.projectedTransitionNet=0.0;
   if(p.projectedHarvestNet+MoneyCalculationTolerance < -SafetyBufferMoney) return HybridFail(r,HYBRID_GATE_BASE_MONEY,HYBRID_REJECT_BASE_MONEY,"BASE_MONEY","HYBRID_BASE_MONEY_NEGATIVE");
   HybridMarkGatePass(r,HYBRID_GATE_BASE_MONEY);
   return true;
}

bool EvaluateHybridCandidate(const HybridCycleSnapshot &s,HybridCandidatePlan &p,HybridEvaluationResult &r)
{
   HybridResetResult(r);
   ZeroMemory(p);
   p.planId=(ulong)TimeCurrent(); p.cycleId=s.cycleId; p.createdAt=TimeCurrent(); p.snapshotFingerprint=s.positionFingerprint;

   if(!UseHybridSplitBigGeometry)
   {
      r.applicable=false; r.evaluated=false; r.passed=false; r.finalCode=HYBRID_FINAL_NONE; r.reason="HYBRID_DISABLED";
      return true;
   }

   if(!ValidateHybridSnapshot(s,r)) return false;
   if(!ValidateHybridConfiguration(r)) return false;

   p.farDirection=s.farDirection;
   p.bigDirection=HybridOpposite(s.farDirection);
   p.smallDirection=s.farDirection;
   p.rawCoreLot=s.farLot*BigCoreRatio;
   p.rawTrendLot=s.farLot*BigTrendRatio;
   p.rawSmallLot=s.farLot*SmallBaseToFarRatio;
   p.rawNewFarLot=s.farLot*TargetNewFarRatio;
   p.coreLot=NormalizeHybridCoreLot(p.rawCoreLot);
   p.trendLot=NormalizeHybridTrendLot(p.rawTrendLot);
   p.smallLot=NormalizeHybridSmallLot(p.rawSmallLot);
   p.newFarLot=NormalizeHybridNewFarLot(p.rawNewFarLot);
   p.closeCoreLot=NormalizeLotDown(p.coreLot-p.newFarLot);
   p.trace=StringFormat("rawCore=%.8f normalizedCore=%.8f rawTrend=%.8f normalizedTrend=%.8f rawSmall=%.8f normalizedSmall=%.8f rawNewFar=%.8f normalizedNewFar=%.8f",p.rawCoreLot,p.coreLot,p.rawTrendLot,p.trendLot,p.rawSmallLot,p.smallLot,p.rawNewFarLot,p.newFarLot);
   HybridMarkGatePass(r,HYBRID_GATE_ROUNDING);

   double minLot=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MIN), maxLot=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MAX);
   if(minLot<=0 || maxLot<=0) return HybridFail(r,HYBRID_GATE_VOLUME,HYBRID_REJECT_VOLUME,"VOLUME","HYBRID_VOLUME_SYMBOL_INVALID");
   if(p.coreLot<minLot || p.trendLot<minLot || p.smallLot<minLot || p.newFarLot<minLot || p.coreLot>maxLot || p.trendLot>maxLot || p.smallLot>maxLot || p.newFarLot>maxLot) return HybridFail(r,HYBRID_GATE_VOLUME,HYBRID_REJECT_MIN_LOT,"VOLUME","HYBRID_COMPONENT_VOLUME_OUT_OF_RANGE");
   HybridMarkGatePass(r,HYBRID_GATE_VOLUME);

   p.catchUpRatio=HybridFinalReserveShare*(p.coreLot+p.trendLot-p.smallLot)/s.farLot;
   if(p.catchUpRatio+MoneyCalculationTolerance<MinimumReserveCatchUpRatio) return HybridFail(r,HYBRID_GATE_LAW1,HYBRID_REJECT_LAW1,"LAW1",StringFormat("HYBRID_CATCHUP KR=%.6f Required=%.6f",p.catchUpRatio,MinimumReserveCatchUpRatio));
   HybridMarkGatePass(r,HYBRID_GATE_LAW1);

   p.recoverySlopeLots=p.coreLot+p.trendLot-p.smallLot-s.farLot;
   p.recoverySlopeMoney=p.recoverySlopeLots*PointValuePerLot();
   if(p.recoverySlopeLots<=0 || p.recoverySlopeMoney+MoneyCalculationTolerance<MinimumRecoverySlopeMoneyPerPoint) return HybridFail(r,HYBRID_GATE_LAW2,HYBRID_REJECT_LAW2,"LAW2",StringFormat("HYBRID_SLOPE Lots=%.6f Money=%.6f",p.recoverySlopeLots,p.recoverySlopeMoney));
   HybridMarkGatePass(r,HYBRID_GATE_LAW2);

   if(!EvaluateHybridBaseMoneyPreview(s,p,r)) return false;

   HybridCatchUpResult catchup;
   if(!EvaluateHybridFiniteCatchUpPreview(s,p,catchup)) return HybridFail(r,HYBRID_GATE_FINITE_CATCHUP,HYBRID_REJECT_FINITE_CATCHUP,"FINITE_CATCHUP",catchup.reason);
   p.finiteCatchUpLevel=catchup.finiteLevel;
   HybridMarkGatePass(r,HYBRID_GATE_FINITE_CATCHUP);

   if(p.newFarLot<=0 || p.newFarLot>=s.farLot) return HybridFail(r,HYBRID_GATE_NEW_FAR,HYBRID_REJECT_NEW_FAR,"NEW_FAR","HYBRID_NEW_FAR_NOT_COMPRESSED");
   HybridMarkGatePass(r,HYBRID_GATE_NEW_FAR);

   p.currentBigGross=p.coreLot+p.trendLot;
   p.nextBigGross=NormalizeHybridCoreLot(p.newFarLot*BigCoreRatio)+NormalizeHybridTrendLot(p.newFarLot*BigTrendRatio);
   if(p.nextBigGross>=s.farLot*MaximumNewBigToOldFarRatio) return HybridFail(r,HYBRID_GATE_NEXT_BIG,HYBRID_REJECT_NEXT_BIG,"NEXT_BIG",StringFormat("HYBRID_NEXT_BIG %.6f Limit=%.6f",p.nextBigGross,s.farLot*MaximumNewBigToOldFarRatio));
   HybridMarkGatePass(r,HYBRID_GATE_NEXT_BIG);

   p.currentGross=s.farLot+p.coreLot+p.trendLot+p.smallLot;
   p.nextGross=p.newFarLot+p.nextBigGross+NormalizeHybridSmallLot(p.newFarLot*SmallBaseToFarRatio);
   if(p.nextGross>=p.currentGross-MoneyCalculationTolerance) return HybridFail(r,HYBRID_GATE_GROSS,HYBRID_REJECT_GROSS,"GROSS",StringFormat("HYBRID_GROSS Next=%.6f Old=%.6f",p.nextGross,p.currentGross));
   HybridMarkGatePass(r,HYBRID_GATE_GROSS);

   p.oldRisk=MathMax(0.0,-p.projectedHarvestNet);
   p.nextRisk=MathMax(0.0,p.oldRisk*TargetNewFarRatio);
   HybridMarkGatePass(r,HYBRID_GATE_RISK);

   HybridMarginPreview margin;
   if(!EvaluateHybridCandidateMargin(s,p,margin)) return HybridFail(r,HYBRID_GATE_MARGIN,HYBRID_REJECT_MARGIN,"MARGIN",margin.reason);
   p.projectedMarginBase=s.margin+margin.totalNewMargin;
   p.projectedMarginUpper=margin.conservativeUpper;
   p.projectedMarginLevel=margin.projectedMarginLevel;
   HybridMarkGatePass(r,HYBRID_GATE_MARGIN);

   HybridWorstCasePreview worst;
   if(!EvaluateHybridWorstCasePreview(s,p,worst)) return HybridFail(r,HYBRID_GATE_WORST_CASE,HYBRID_REJECT_WORST_CASE,"WORST_CASE",worst.reason);
   p.worstCaseNet=worst.worstNet;
   HybridMarkGatePass(r,HYBRID_GATE_WORST_CASE);

   HybridFutureSmallResult future;
   if(!EvaluateHybridFutureSmallDepth1(s,p,future)) return HybridFail(r,HYBRID_GATE_FUTURE_SMALL,HYBRID_REJECT_FUTURE_SMALL,"FUTURE_SMALL",future.reason);
   p.futureSmallDepthProven=future.depthProven;
   HybridMarkGatePass(r,HYBRID_GATE_FUTURE_SMALL);

   p.finalCloseAvailable=false;
   HybridMarkGatePass(r,HYBRID_GATE_FINAL_CLOSE_PREVIEW);

   r.evaluated=true; r.passed=true; r.finalCode=HYBRID_CANDIDATE_ALLOWED; r.reason="PASS";
   r.trace=StringFormat("%s KR=%.6f slopeLots=%.6f slopeMoney=%.6f NextBig=%.6f GrossOld=%.6f GrossNext=%.6f finiteLevel=%d BaseMoney=%.2f ReserveAdd=%.2f MarginUpper=%.2f MarginLevel=%.2f WorstNet=%.2f FutureDepth=%d",
                        p.trace,p.catchUpRatio,p.recoverySlopeLots,p.recoverySlopeMoney,p.nextBigGross,p.currentGross,p.nextGross,p.finiteCatchUpLevel,p.projectedHarvestNet,p.projectedReserveAdd,p.projectedMarginUpper,p.projectedMarginLevel,p.worstCaseNet,p.futureSmallDepthProven);
   p.trace=r.trace;
   return true;
}

#endif // __BH_HYBRID_DECISION_ENGINE_MQH__
