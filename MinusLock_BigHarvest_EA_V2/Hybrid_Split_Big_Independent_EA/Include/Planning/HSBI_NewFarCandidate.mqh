#ifndef HSBI_NEW_FAR_CANDIDATE_MQH
#define HSBI_NEW_FAR_CANDIDATE_MQH
#include "../Core/HSBI_Types.mqh"
#include "../Core/HSBI_ReasonCodes.mqh"
struct HSBI_NewFarCandidate{double candidateVolume;double normalizedVolume;double oldFarVolume;double compressionLots;double compressionRatio;double riskNext;double marginNext;HSBI_Status futureSmallStatus;HSBI_Status finiteCatchUpStatus;bool nextCycleFeasible;bool moneyProofValid;bool marginProofValid;bool riskProofValid;bool futureSmallProofValid;bool catchUpProofValid;ulong sourceBigCoreIdentifier;ulong sourceBigCoreTicket;HSBI_Status validationStatus;HSBI_ReasonCode reason;int futureTransitionCount;double safetyBuffer;string moneyProofDigest;string marginProofDigest;string riskProofDigest;string futureSmallProofDigest;string catchUpProofDigest;string candidateDigest;};
struct HSBI_ProjectedNewFar{double volume;ulong planId;ulong stateRevision;string digest;bool valid;};
struct HSBI_ActualNewFar{double residualVolume;ulong sourceIdentifier;ulong sourceDealId;ulong planId;ulong stateRevision;bool fillsConfirmed;bool actual;bool valid;};
HSBI_ValidationResult HSBI_ValidateNewFarCandidateStructure(const HSBI_NewFarCandidate &c){bool ok=c.normalizedVolume>0.0&&c.normalizedVolume<c.oldFarVolume&&c.compressionLots>0.0&&c.sourceBigCoreIdentifier>0&&c.sourceBigCoreTicket>0;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_INVALID_VOLUME,"HSBI-NF-001","");}
bool HSBI_IsCandidateSourceValid(const HSBI_NewFarCandidate &c,const ulong originalIdentifier,const ulong originalTicket){return c.sourceBigCoreIdentifier==originalIdentifier&&c.sourceBigCoreTicket==originalTicket;}
int HSBI_CompareCandidateTieBreak(const HSBI_NewFarCandidate &a,const HSBI_NewFarCandidate &b)
{
   bool av=a.validationStatus==HSBI_STATUS_VALID&&a.nextCycleFeasible&&a.moneyProofValid&&a.marginProofValid&&a.riskProofValid&&a.futureSmallProofValid&&a.catchUpProofValid,bv=b.validationStatus==HSBI_STATUS_VALID&&b.nextCycleFeasible&&b.moneyProofValid&&b.marginProofValid&&b.riskProofValid&&b.futureSmallProofValid&&b.catchUpProofValid;if(av!=bv)return av?-1:1;
   if(a.riskNext<b.riskNext)return -1;if(a.riskNext>b.riskNext)return 1;
   if(a.marginNext<b.marginNext)return -1;if(a.marginNext>b.marginNext)return 1;
   if(a.futureTransitionCount<b.futureTransitionCount)return -1;if(a.futureTransitionCount>b.futureTransitionCount)return 1;
   if(a.safetyBuffer>b.safetyBuffer)return -1;if(a.safetyBuffer<b.safetyBuffer)return 1;
   if(a.normalizedVolume<b.normalizedVolume)return -1;if(a.normalizedVolume>b.normalizedVolume)return 1;
   return StringCompare(a.candidateDigest,b.candidateDigest);
}
#endif
