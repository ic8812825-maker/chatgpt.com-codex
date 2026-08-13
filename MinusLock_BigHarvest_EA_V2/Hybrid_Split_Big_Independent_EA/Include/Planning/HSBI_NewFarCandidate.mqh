#ifndef HSBI_NEW_FAR_CANDIDATE_MQH
#define HSBI_NEW_FAR_CANDIDATE_MQH
#include "../Core/HSBI_Types.mqh"
#include "../Core/HSBI_ReasonCodes.mqh"
struct HSBI_NewFarCandidate
{
   double candidateVolume,normalizedVolume,oldFarVolume,compressionLots,compressionRatio,riskNext,marginNext;
   HSBI_Status futureSmallStatus,finiteCatchUpStatus; bool nextCycleFeasible,moneyProofValid,marginProofValid,riskProofValid;
   bool futureSmallProofValid,catchUpProofValid,allocationPolicyValid,controlSnapshotsValid,costSnapshotsValid,fullDigestValid;
   bool aggregateProofValid,aggregateRuntimeConfirmed; double aggregateMinimumRecoveryMoney,aggregateWorstMargin,aggregateWorstRisk,aggregateWorstGrossExposure,aggregateWorstTransitionLoss;
   int aggregateWorstMarginLevel,aggregateWorstRiskLevel,aggregateWorstExposureLevel,aggregateWorstTransitionLossLevel; string aggregateProofDigest;
   ulong sourceBigCoreIdentifier,sourceBigCoreTicket; HSBI_Status validationStatus; HSBI_ReasonCode reason;
   int futureTransitionCount; double safetyBuffer,reserveShare,reserveEligibleMoney,reserveGainMoney,farLossIncreaseMoney;
   string moneyProofDigest,marginProofDigest,riskProofDigest,futureSmallProofDigest,catchUpProofDigest;
   string allocationPolicyDigest,controlPriceDigest,costSnapshotDigest,candidateDigest;
};
struct HSBI_ProjectedNewFar { double volume; ulong planId,stateRevision; string digest; bool valid; };
struct HSBI_ActualNewFar { double residualVolume; ulong sourceIdentifier,sourceDealId,planId,stateRevision; bool fillsConfirmed,actual,valid; };
HSBI_ValidationResult HSBI_ValidateNewFarCandidateStructure(const HSBI_NewFarCandidate &c)
{
   bool ok=c.normalizedVolume>0.0&&c.normalizedVolume<c.oldFarVolume&&c.compressionLots>0.0&&c.sourceBigCoreIdentifier>0&&c.sourceBigCoreTicket>0;
   return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_INVALID_VOLUME,"HSBI-NF-001","");
}
bool HSBI_IsCandidateSourceValid(const HSBI_NewFarCandidate &c,const ulong id,const ulong ticket)
{return c.sourceBigCoreIdentifier==id&&c.sourceBigCoreTicket==ticket;}
bool HSBI_IsCompleteCandidateProof(const HSBI_NewFarCandidate &c)
{
   return c.validationStatus==HSBI_STATUS_VALID&&c.nextCycleFeasible&&c.moneyProofValid&&c.marginProofValid&&c.riskProofValid&&
      c.futureSmallProofValid&&c.catchUpProofValid&&c.aggregateProofValid&&c.aggregateRuntimeConfirmed&&c.aggregateProofDigest!=""&&c.allocationPolicyValid&&c.controlSnapshotsValid&&c.costSnapshotsValid&&
      c.fullDigestValid&&c.moneyProofDigest!=""&&c.marginProofDigest!=""&&c.riskProofDigest!=""&&c.futureSmallProofDigest!=""&&
      c.catchUpProofDigest!=""&&c.allocationPolicyDigest!=""&&c.controlPriceDigest!=""&&c.costSnapshotDigest!=""&&c.candidateDigest!="";
}
int HSBI_CompareCandidateTieBreak(const HSBI_NewFarCandidate &a,const HSBI_NewFarCandidate &b)
{
   bool av=HSBI_IsCompleteCandidateProof(a),bv=HSBI_IsCompleteCandidateProof(b);if(av!=bv)return av?-1:1;
   if(a.riskNext!=b.riskNext)return a.riskNext<b.riskNext?-1:1;if(a.marginNext!=b.marginNext)return a.marginNext<b.marginNext?-1:1;
   if(a.futureTransitionCount!=b.futureTransitionCount)return a.futureTransitionCount<b.futureTransitionCount?-1:1;
   if(a.safetyBuffer!=b.safetyBuffer)return a.safetyBuffer>b.safetyBuffer?-1:1;
   if(a.normalizedVolume!=b.normalizedVolume)return a.normalizedVolume<b.normalizedVolume?-1:1;
   return StringCompare(a.candidateDigest,b.candidateDigest);
}
#endif
