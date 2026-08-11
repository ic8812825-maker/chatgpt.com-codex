#ifndef HSBI_CANDIDATE_PLAN_MQH
#define HSBI_CANDIDATE_PLAN_MQH
#include "HSBI_GeometryTypes.mqh"
#include "../Core/HSBI_Identifiers.mqh"
struct HSBI_CandidatePlan{ulong planId;ulong cycleId;ulong stateRevision;string positionFingerprint;ulong marketSnapshotId;HSBI_Identity farIdentity;double farLots;double coreLots;double trendLots;double smallLots;HSBI_NormalizedLots normalizedLots;HSBI_ControlPriceSet controlPrices;HSBI_GeometrySnapshot geometry;string moneyPreviewDigest;string riskPreviewDigest;string futureSmallDigest;string newFarSolverDigest;ulong gateMask;string rejectionReasons;datetime createdAt;bool immutable;};
bool HSBI_ValidateCandidatePlan(const HSBI_CandidatePlan &p){return p.planId>0&&p.cycleId>0&&p.stateRevision>0&&p.marketSnapshotId>0&&p.immutable&&HSBI_IsValidIdentity(p.farIdentity);}
string HSBI_CandidatePlanFingerprint(const HSBI_CandidatePlan &p){return HSBI_UlongToString(p.planId)+"|"+HSBI_UlongToString(p.cycleId)+"|"+HSBI_UlongToString(p.stateRevision)+"|"+p.positionFingerprint+"|"+HSBI_UlongToString(p.marketSnapshotId);}
bool HSBI_SameCandidatePlan(const HSBI_CandidatePlan &a,const HSBI_CandidatePlan &b){return HSBI_CandidatePlanFingerprint(a)==HSBI_CandidatePlanFingerprint(b);}
#endif
