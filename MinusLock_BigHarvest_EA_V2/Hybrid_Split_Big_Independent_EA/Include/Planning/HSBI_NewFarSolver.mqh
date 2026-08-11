#ifndef HSBI_NEW_FAR_SOLVER_MQH
#define HSBI_NEW_FAR_SOLVER_MQH
#include "HSBI_NewFarCandidate.mqh"
#include "HSBI_FutureSmallSolver.mqh"
#include "../Execution/HSBI_OwnershipGuardTypes.mqh"
#include "../Risk/HSBI_NewFarGateTypes.mqh"
#include "../Money/HSBI_CandidateMoneyEvaluator.mqh"
#include "../Money/HSBI_ReserveCatchUpEvaluator.mqh"
enum HSBI_SolverStatus { HSBI_SOLVER_SELECTED,HSBI_SOLVER_NO_SAFE_CANDIDATE,HSBI_SOLVER_SOURCE_MISMATCH,HSBI_SOLVER_STALE_SNAPSHOT,
   HSBI_SOLVER_PROOF_FAILED,HSBI_SOLVER_MARGIN_FAILED,HSBI_SOLVER_RISK_FAILED,HSBI_SOLVER_TRANSITION_LOSS_FAILED,
   HSBI_SOLVER_BROKER_GRID_FAILED,HSBI_SOLVER_RECONCILIATION_REQUIRED,HSBI_SOLVER_TERMINAL_SAFE };
struct HSBI_TransitionPlanSnapshot { ulong planId,stateRevision; bool immutable,persisted; };
struct HSBI_ActualClosingDealsSnapshot { ulong sourceDealId,sourceEventId; bool fillsConfirmed,actual; };
struct HSBI_AllocationStateSnapshot { bool valid,fresh; ulong revision; };
struct HSBI_NewFarSolverInput
{
   HSBI_AllocationPolicySnapshot allocationPolicy; HSBI_PositionDescriptor oldFarDescriptor,originalBigCoreDescriptor,actualBigCoreResidual;
   HSBI_TransitionPlanSnapshot smallTransitionPlan; HSBI_ActualClosingDealsSnapshot actualClosingDeals;
   HSBI_MoneyStateSnapshot moneyState; HSBI_AllocationStateSnapshot allocationState; HSBI_RiskSnapshot riskState;
   HSBI_MarginSnapshot marginState; HSBI_ControlPriceSnapshot controlPrice; HSBI_BrokerProperties brokerProperties;
   HSBI_FutureSmallInput futureSmallTemplate; ulong cycleId,planId,stateRevision; double projectedVolume,maximumNewFarRatio;
   double minimumCompressionLots,minimumCompressionRatio,absoluteLossCap,equityPercentCap,oldFarRiskCap,cumulativeCycleLossCap;
   bool brokerMoneyAvailable,secondFarPresent,testOnlyApproximation; string moneyProofDigest,marginProofDigest,riskProofDigest,expectedPlanDigest;
};
struct HSBI_NewFarSolverResult
{
   bool valid; HSBI_SolverStatus status; double selectedVolume,oldFarVolume,actualResidualVolume,projectedVolume,compressionLots;
   double compressionRatio,riskNext,marginNext,transitionLoss,allowedTransitionLoss; int candidateCount,rejectedCandidateCount;
   ulong sourceIdentifier,sourceDealId,planId,stateRevision; string candidateDigest,candidateListDigest,planDigest,proofDigest;
   HSBI_ReasonCode reason; string details;
};
string HSBI_FutureSmallTemplateDigest(const HSBI_FutureSmallInput &f)
{
   string d=HSBI_AllocationPolicyDigest(f.allocationPolicy)+"|"+DoubleToString(f.currentFar,8)+"|"+DoubleToString(f.coreRatio,12)+"|"+
      DoubleToString(f.trendRatio,12)+"|"+DoubleToString(f.smallRatio,12)+"|"+IntegerToString(f.maximumDepth);
   for(int i=0;i<f.maximumDepth;i++) d+="|M"+IntegerToString(i)+"|"+HSBI_UlongToString(f.levelMarketSnapshots[i].snapshotId)+"|"+
      DoubleToString(f.levelMarketSnapshots[i].bid,8)+"|"+DoubleToString(f.levelMarketSnapshots[i].ask,8)+"|"+
      HSBI_UlongToString(f.levelCostSnapshots[i].snapshotId)+"|"+HSBI_UlongToString(f.levelCostSnapshots[i].farCosts.snapshotId)+"|"+
      HSBI_UlongToString(f.levelCostSnapshots[i].coreCosts.snapshotId)+"|"+HSBI_UlongToString(f.levelCostSnapshots[i].trendCosts.snapshotId)+"|"+
      HSBI_UlongToString(f.levelCostSnapshots[i].smallCosts.snapshotId)+"|"+DoubleToString(f.farProjections[i].projectedFar,8)+"|"+
      HSBI_UlongToString(f.riskProofSnapshotIds[i]);
   return d;
}
string HSBI_NewFarInputDigest(const HSBI_NewFarSolverInput &x)
{
   return LongToString(x.oldFarDescriptor.identity.accountLogin)+"|"+x.oldFarDescriptor.identity.symbol+"|"+LongToString(x.oldFarDescriptor.identity.magic)+"|"+
      HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.planId)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+
      DoubleToString(x.oldFarDescriptor.actualVolume,8)+"|"+HSBI_UlongToString(x.originalBigCoreDescriptor.identifier)+"|"+
      HSBI_UlongToString(x.originalBigCoreDescriptor.ticket)+"|"+DoubleToString(x.actualBigCoreResidual.actualVolume,8)+"|"+
      DoubleToString(x.projectedVolume,8)+"|"+DoubleToString(x.brokerProperties.volumeMin,8)+"|"+DoubleToString(x.brokerProperties.volumeMax,8)+"|"+
      DoubleToString(x.brokerProperties.volumeStep,8)+"|"+DoubleToString(x.brokerProperties.tickSize,8)+"|"+
      DoubleToString(x.controlPrice.selectedPrice,8)+"|"+HSBI_UlongToString(x.controlPrice.snapshotId)+"|"+
      HSBI_AllocationPolicyDigest(x.allocationPolicy)+"|"+HSBI_FutureSmallTemplateDigest(x.futureSmallTemplate)+"|"+
      x.moneyProofDigest+"|"+x.marginProofDigest+"|"+x.riskProofDigest+"|"+HSBI_UlongToString(x.riskState.snapshotId)+"|"+HSBI_UlongToString(x.marginState.snapshotId);
}
string HSBI_FinalizeNewFarPlanDigest(const HSBI_NewFarSolverInput &x,const string list){return HSBI_NewFarInputDigest(x)+"|CANDIDATES|"+list;}
bool HSBI_ValidateNewFarSource(const HSBI_NewFarSolverInput &x)
{
   if(!x.actualClosingDeals.actual||!x.actualClosingDeals.fillsConfirmed||x.actualClosingDeals.sourceDealId==0||x.actualClosingDeals.sourceEventId==0)return false;
   if(x.oldFarDescriptor.role!=HSBI_ROLE_FAR||x.originalBigCoreDescriptor.role!=HSBI_ROLE_BIG_CORE||x.actualBigCoreResidual.role!=HSBI_ROLE_BIG_CORE)return false;
   if(!HSBI_SamePositionOwner(x.originalBigCoreDescriptor.identity,x.actualBigCoreResidual.identity))return false;
   if(x.originalBigCoreDescriptor.identity.accountLogin!=x.oldFarDescriptor.identity.accountLogin||x.originalBigCoreDescriptor.identity.symbol!=x.oldFarDescriptor.identity.symbol||
      x.originalBigCoreDescriptor.identity.magic!=x.oldFarDescriptor.identity.magic||x.originalBigCoreDescriptor.identity.cycleId!=x.cycleId)return false;
   if(x.originalBigCoreDescriptor.identifier==0||x.originalBigCoreDescriptor.identifier!=x.actualBigCoreResidual.identifier||
      x.originalBigCoreDescriptor.ticket==0||x.originalBigCoreDescriptor.ticket!=x.actualBigCoreResidual.ticket)return false;
   if(x.oldFarDescriptor.direction==HSBI_DIRECTION_NONE||x.actualBigCoreResidual.direction==HSBI_DIRECTION_NONE||
      x.oldFarDescriptor.direction==x.actualBigCoreResidual.direction||x.actualBigCoreResidual.actualVolume<=0.0||
      x.actualBigCoreResidual.actualVolume>=x.oldFarDescriptor.actualVolume)return false;
   return HSBI_IsActualBigCoreResidual(x.actualBigCoreResidual,x.originalBigCoreDescriptor.identifier)&&HSBI_ValidateVolume(x.actualBigCoreResidual.actualVolume,x.brokerProperties);
}
double HSBI_AllowedTransitionLoss(const HSBI_NewFarSolverInput &x){return MathMin(MathMin(x.absoluteLossCap,x.equityPercentCap),MathMin(x.oldFarRiskCap,x.cumulativeCycleLossCap));}
HSBI_FutureSmallInput HSBI_BuildCandidateFutureSmallInput(const HSBI_NewFarSolverInput &x,const double candidate)
{
   HSBI_FutureSmallInput fs=x.futureSmallTemplate;fs.currentFar=candidate;fs.planId=x.planId;fs.stateRevision=x.stateRevision;
   fs.allocationPolicy=x.allocationPolicy;fs.useInjectedBrokerProofs=false;fs.testOnlyApproximation=false;return fs;
}
string HSBI_CandidateProofDigest(const HSBI_NewFarCandidate &c,const HSBI_NewFarSolverInput &x)
{
   return DoubleToString(c.normalizedVolume,8)+"|"+DoubleToString(x.actualBigCoreResidual.actualVolume,8)+"|"+
      DoubleToString(x.oldFarDescriptor.actualVolume,8)+"|"+DoubleToString(c.compressionLots,8)+"|"+DoubleToString(c.compressionRatio,12)+"|"+
      c.futureSmallProofDigest+"|"+c.moneyProofDigest+"|"+c.marginProofDigest+"|"+c.riskProofDigest+"|"+
      c.catchUpProofDigest+"|"+c.allocationPolicyDigest+"|"+c.controlPriceDigest+"|"+c.costSnapshotDigest;
}
HSBI_NewFarSolverResult HSBI_SolveNewFar(const HSBI_NewFarSolverInput &x)
{
   HSBI_NewFarSolverResult r;ZeroMemory(r);r.status=HSBI_SOLVER_NO_SAFE_CANDIDATE;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;
   r.oldFarVolume=x.oldFarDescriptor.actualVolume;r.actualResidualVolume=x.actualBigCoreResidual.actualVolume;r.projectedVolume=x.projectedVolume;
   r.planId=x.planId;r.stateRevision=x.stateRevision;r.sourceIdentifier=x.originalBigCoreDescriptor.identifier;r.sourceDealId=x.actualClosingDeals.sourceDealId;r.details="NO_SAFE_CANDIDATE";
   if(x.testOnlyApproximation||!HSBI_ValidateAllocationPolicy(x.allocationPolicy)){r.status=HSBI_SOLVER_PROOF_FAILED;r.details="ALLOCATION_OR_APPROXIMATION_INVALID";return r;}
   if(!x.controlPrice.fresh||!x.riskState.fresh||!x.marginState.fresh||!x.moneyState.fresh||!x.allocationState.fresh){r.status=HSBI_SOLVER_STALE_SNAPSHOT;r.details="STALE_SNAPSHOT";return r;}
   if(x.secondFarPresent){r.status=HSBI_SOLVER_RECONCILIATION_REQUIRED;r.details="SECOND_FAR";return r;}
   if(!HSBI_ValidateNewFarSource(x)){r.status=HSBI_SOLVER_SOURCE_MISMATCH;r.reason=HSBI_REASON_INVALID_IDENTITY;r.details="NEW_FAR_SOURCE_MISMATCH";return r;}
   if(!x.brokerMoneyAvailable){r.status=HSBI_SOLVER_PROOF_FAILED;r.details="BROKER_MONEY_UNAVAILABLE";return r;}
   if(x.planId==0||x.stateRevision==0||x.smallTransitionPlan.planId!=x.planId||x.smallTransitionPlan.stateRevision!=x.stateRevision||
      !x.smallTransitionPlan.immutable||!x.smallTransitionPlan.persisted){r.status=HSBI_SOLVER_RECONCILIATION_REQUIRED;r.details="PLAN_IDENTITY_MISMATCH";return r;}
   string inputDigest=HSBI_NewFarInputDigest(x);if(x.expectedPlanDigest!=""&&x.expectedPlanDigest!=inputDigest){r.status=HSBI_SOLVER_RECONCILIATION_REQUIRED;r.details="PLAN_DIGEST_MISMATCH";return r;}
   r.allowedTransitionLoss=HSBI_AllowedTransitionLoss(x);if(!HSBI_IsFiniteNumber(r.allowedTransitionLoss)||r.allowedTransitionLoss<0.0){r.status=HSBI_SOLVER_TRANSITION_LOSS_FAILED;r.details="TRANSITION_CAP_UNAVAILABLE";return r;}
   HSBI_NewFarCandidate safe[];int safeCount=0;double upper=MathMin(x.brokerProperties.volumeMax,x.actualBigCoreResidual.actualVolume);string listDigest="";
   for(double n=x.brokerProperties.volumeMin;n<=upper+HSBI_GridTolerance(x.brokerProperties.volumeStep);n+=x.brokerProperties.volumeStep) {
      r.candidateCount++;double candidate=HSBI_NormalizeVolume(n,x.brokerProperties.volumeStep,HSBI_VOLUME_PARTIAL_FAR);
      double compression=x.oldFarDescriptor.actualVolume-candidate,ratio=compression/x.oldFarDescriptor.actualVolume;
      if(!HSBI_ValidateVolume(candidate,x.brokerProperties)||candidate<=0.0||candidate>=x.oldFarDescriptor.actualVolume||candidate>x.maximumNewFarRatio*x.oldFarDescriptor.actualVolume||
         compression<x.minimumCompressionLots||ratio<x.minimumCompressionRatio){r.rejectedCandidateCount++;continue;}
      HSBI_FutureSmallInput fs=HSBI_BuildCandidateFutureSmallInput(x,candidate);HSBI_CandidateMoneyEvaluationResult cp=HSBI_EvaluateCandidateMoney(fs);
      if(!cp.valid){r.rejectedCandidateCount++;continue;}HSBI_FutureSmallResult proof=cp.futureSmallProof;HSBI_FutureSmallLevelProof first=proof.levels[0];
      HSBI_ReserveCatchUpInput ci;ZeroMemory(ci);ci.allocationPolicy=x.allocationPolicy;ci.reserveEligibleMoney=MathMax(0.0,first.reserveSourceProof.netMoney);
      ci.reserveEligibleMoneyAlreadyAllocated=false;ci.farLossIncreaseMoney=MathMax(0.0,-first.farLossProof.netMoney);ci.executionSafetyBuffer=fs.executionSafetyBuffer;
      ci.netBigVolume=first.netBigVolume;ci.farVolume=candidate;ci.farDirection=x.oldFarDescriptor.direction;ci.reserveSourceProof=first.reserveSourceProof;
      ci.farLossProof=first.farLossProof;ci.sourceDealId=x.actualClosingDeals.sourceDealId;ci.sourceEventId=x.actualClosingDeals.sourceEventId;
      ci.planId=x.planId;ci.stateRevision=x.stateRevision;ci.snapshotId=first.controlSnapshotId;ci.projected=true;ci.moneyAvailable=first.moneyIncluded;ci.fresh=fs.snapshotsFresh;
      HSBI_ReserveCatchUpResult catchResult=HSBI_EvaluateReserveCatchUp(ci);if(!catchResult.valid){r.rejectedCandidateCount++;continue;}
      HSBI_NewFarGateInput gate;ZeroMemory(gate);gate.marginNext=first.projectedMargin;gate.allowedMargin=x.marginState.allowedMargin;gate.riskNext=first.projectedRisk;
      gate.riskOld=x.riskState.currentRisk;gate.riskTolerance=x.riskState.riskTolerance;gate.grossExposureNext=first.grossExposure;
      gate.grossExposureOld=x.riskState.currentGrossExposure;gate.transitionLoss=first.transitionLoss;gate.absoluteLossCap=x.absoluteLossCap;
      gate.equityPercentCap=x.equityPercentCap;gate.oldFarRiskCap=x.oldFarRiskCap;gate.cumulativeCycleLossCap=x.cumulativeCycleLossCap;
      gate.marginAvailable=first.marginIncluded;gate.riskAvailable=first.riskIncluded;gate.transitionCapAvailable=first.transitionLossIncluded;
      gate.moneyAvailable=first.moneyIncluded;gate.snapshotFresh=fs.snapshotsFresh;if(!HSBI_EvaluateNewFarGates(gate).passed){r.rejectedCandidateCount++;continue;}
      HSBI_NewFarCandidate c;ZeroMemory(c);c.candidateVolume=n;c.normalizedVolume=candidate;c.oldFarVolume=x.oldFarDescriptor.actualVolume;
      c.compressionLots=compression;c.compressionRatio=ratio;c.riskNext=first.projectedRisk;c.marginNext=first.projectedMargin;c.futureSmallStatus=HSBI_STATUS_VALID;
      c.finiteCatchUpStatus=HSBI_STATUS_VALID;c.nextCycleFeasible=true;c.moneyProofValid=true;c.marginProofValid=true;c.riskProofValid=true;
      c.futureSmallProofValid=proof.valid;c.catchUpProofValid=catchResult.valid;c.allocationPolicyValid=true;c.controlSnapshotsValid=true;c.costSnapshotsValid=true;
      c.sourceBigCoreIdentifier=x.originalBigCoreDescriptor.identifier;c.sourceBigCoreTicket=x.originalBigCoreDescriptor.ticket;c.validationStatus=HSBI_STATUS_VALID;
      c.reason=HSBI_REASON_OK;c.futureTransitionCount=proof.theoreticalDepth;c.safetyBuffer=catchResult.catchUpMargin;c.reserveShare=catchResult.reserveShare;
      c.reserveEligibleMoney=catchResult.reserveEligibleMoney;c.reserveGainMoney=catchResult.reserveGainMoney;c.farLossIncreaseMoney=catchResult.farLossIncreaseMoney;
      c.moneyProofDigest=cp.moneyProofDigest;c.marginProofDigest=cp.marginProofDigest;c.riskProofDigest=cp.riskProofDigest;
      c.futureSmallProofDigest=cp.futureSmallProofDigest;c.catchUpProofDigest=HSBI_ReserveCatchUpDigest(catchResult);
      c.allocationPolicyDigest=HSBI_AllocationPolicyDigest(x.allocationPolicy);c.controlPriceDigest=cp.futureSmallProofDigest+"|CONTROL";
      c.costSnapshotDigest=HSBI_FutureSmallTemplateDigest(fs)+"|COST";c.candidateDigest=HSBI_CandidateProofDigest(c,x);c.fullDigestValid=c.candidateDigest!="";
      if(!HSBI_IsCompleteCandidateProof(c)){r.rejectedCandidateCount++;continue;}listDigest+=c.candidateDigest+";";ArrayResize(safe,safeCount+1);safe[safeCount++]=c;
   }
   r.candidateListDigest=listDigest;r.planDigest=HSBI_FinalizeNewFarPlanDigest(x,listDigest);if(safeCount==0)return r;
   int best=0;for(int i=1;i<safeCount;i++)if(HSBI_CompareCandidateTieBreak(safe[i],safe[best])<0)best=i;HSBI_NewFarCandidate selected=safe[best];
   r.valid=true;r.status=HSBI_SOLVER_SELECTED;r.selectedVolume=selected.normalizedVolume;r.compressionLots=selected.compressionLots;
   r.compressionRatio=selected.compressionRatio;r.riskNext=selected.riskNext;r.marginNext=selected.marginNext;r.transitionLoss=selected.farLossIncreaseMoney;
   r.candidateDigest=selected.candidateDigest;r.proofDigest=selected.futureSmallProofDigest;r.reason=HSBI_REASON_OK;r.details="SELECTED";return r;
}
#endif
