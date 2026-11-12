#property strict
// DG01 isolated Script: tests only. No trading, provider, network or persistence calls.
#include "../../Include/Core/HSBI_Version.mqh"
#include "../Reference/HSBI_DG01_identity_candidate.mqh"
#include "../Reference/hsbi_02b_r0h_native_codec.mqh"
#include "../../Include/Core/HSBI_Invariants.mqh"
#include "../../Include/Money/HSBI_MoneyState.mqh"
#include "../../Include/Money/HSBI_AllocationLedgerTypes.mqh"
#include "../../Include/Money/HSBI_ReserveCatchUpEvaluator.mqh"
#include "../../Include/Risk/HSBI_RiskGateResult.mqh"
#include "../../Include/Execution/HSBI_TransactionTypes.mqh"
int dg_pass=0,dg_fail=0,dg_infra=0;
void DGCheck(const string id,const bool condition,const string scope){if(condition)dg_pass++;else dg_fail++;Print("DG01|",id,"|",condition?"PASS":"FAIL","|",scope);}
void DGFixture(HSBI_EconomicLedgerRecordV2 &r){ZeroMemory(r);r.knownFieldsMask=536870911;r.schemaVersion=1;r.broker="FIXTURE";r.server="OFFLINE";r.accountLogin=1;r.symbol="X";r.magic=7;r.cycleId=1;r.dealTicket=11;r.orderTicket=12;r.positionIdentifier=13;r.actionId=4;r.eventId=5;r.role=HSBI_ROLE_BIG_CORE;r.entryType=1;r.dealType=1;r.timestampMsc=1000;r.volume=1;r.price=100;r.profit=r.dealNet=50;r.currency="USD";r.precision=2;r.sourcePlanApplicable=true;r.sourcePlan=1;r.sourcePolicyApplicable=true;r.sourcePolicyVersion=1;}
HSBI_ReserveCatchUpInput DGReserve(){HSBI_ReserveCatchUpInput x;ZeroMemory(x);x.runtimeMode=HSBI_RUNTIME_SHADOW;x.allocationPolicy.reserveShare=.8;x.allocationPolicy.policyVersion=3;x.allocationPolicy.snapshotId=6;x.allocationPolicy.valid=x.allocationPolicy.fresh=true;x.reserveEligibleMoney=50;x.reserveEligibleMoneyAlreadyAllocated=true;x.farLossIncreaseMoney=10;x.executionSafetyBuffer=1;x.netBigVolume=4;x.farVolume=1;x.farDirection=HSBI_DIRECTION_SELL;x.planId=5;x.stateRevision=7;x.snapshotId=6;x.sourceDealId=101;x.sourceEventId=10;x.projected=x.moneyAvailable=x.fresh=true;
 HSBI_MoneyProofIdentity i;ZeroMemory(i);i.accountLogin=1;i.symbol="X";i.magic=7;i.cycleId=1;i.positionIdentifier=13;i.role=HSBI_ROLE_BIG_CORE;i.direction=HSBI_DIRECTION_BUY;i.sourceDealId=101;i.sourceEventId=10;i.snapshotId=6;i.planId=5;i.stateRevision=7;x.reserveSourceProof.identity=i;x.reserveSourceProof.valid=x.reserveSourceProof.projected=x.reserveSourceProof.runtimeConfirmed=true;x.reserveSourceProof.status=HSBI_CALC_PASS;x.reserveSourceProof.netMoney=50;x.expectedReserveIdentity=i;i.role=HSBI_ROLE_FAR;i.direction=HSBI_DIRECTION_SELL;i.positionIdentifier=14;i.sourceDealId=102;i.sourceEventId=11;x.farLossProof=x.reserveSourceProof;x.farLossProof.identity=i;x.farLossProof.netMoney=-10;x.expectedFarIdentity=i;
 x.reserveAllocationSource.sourceDealKey="D101";x.reserveAllocationSource.sourceAllocationKey="A101";x.reserveAllocationSource.sourceDealId=101;x.reserveAllocationSource.allocationEventId=44;x.reserveAllocationSource.allocationPolicyVersion=3;x.reserveAllocationSource.allocatableNet=x.reserveAllocationSource.reserveAllocated=50;x.reserveAllocationSource.valid=x.reserveAllocationSource.allocationConfirmed=x.reserveAllocationSource.sourceReconciled=true;x.consumptionKey.sourceDealKey="D101";x.consumptionKey.sourceAllocationKey="A101";x.consumptionKey.planId=5;x.consumptionKey.stateRevision=7;x.consumptionKey.consumptionEventId=88;x.consumptionKey.consumer="CatchUp";return x;}
HSBI_PositionDescriptor DGPosition(ulong id){HSBI_PositionDescriptor p;ZeroMemory(p);p.role=HSBI_ROLE_FAR;p.ticket=p.identifier=id;p.actualVolume=p.requestedVolume=1;p.direction=HSBI_DIRECTION_SELL;p.openPrice=100;p.currentClosePrice=101;p.creationActionId=p.lastEventId=1;p.identity.accountLogin=1;p.identity.symbol="X";p.identity.magic=7;p.identity.cycleId=1;p.identity.positionIdentifier=id;p.identity.role=HSBI_ROLE_FAR;return p;}
#include "HSBI_DG01_codec_cases.mqh"
void OnStart(){
 HSBI_EconomicLedgerRecordV2 a,b,independentFixture;DGFixture(a);DGFixture(independentFixture);b=a;
 string fieldNames[29]={"SchemaVersion","Broker","Server","AccountLogin","Symbol","Magic","CycleID","DealTicket","OrderTicket","PositionIdentifier","ActionID","EventID","Role","EntryType","DealType","TimestampMsc","Volume","Price","Profit","Swap","Commission","Fee","DealNet","Currency","Precision","SourcePlanApplicable","SourcePlan","SourcePolicyApplicable","SourcePolicyVersion"};
 for(int field=0;field<29;field++){
  b=a;
  switch(field){case 0:b.schemaVersion++;break;case 1:b.broker="OTHER";break;case 2:b.server="OTHER";break;case 3:b.accountLogin++;break;case 4:b.symbol="OTHER";break;case 5:b.magic++;break;case 6:b.cycleId++;break;case 7:b.dealTicket++;break;case 8:b.orderTicket++;break;case 9:b.positionIdentifier++;break;case 10:b.actionId++;break;case 11:b.eventId++;break;case 12:b.role=HSBI_ROLE_FAR;break;case 13:b.entryType=0;break;case 14:b.dealType=0;break;case 15:b.timestampMsc++;break;case 16:b.volume++;break;case 17:b.price++;break;case 18:b.profit++;break;case 19:b.swap++;break;case 20:b.commission++;break;case 21:b.fee++;break;case 22:b.dealNet++;break;case 23:b.currency="EUR";break;case 24:b.precision++;break;case 25:b.sourcePlanApplicable=false;break;case 26:b.sourcePlan++;break;case 27:b.sourcePolicyApplicable=false;break;case 28:b.sourcePolicyVersion++;break;}
  DGCheck("E1-FIELD-"+fieldNames[field],!HSBI_SameEconomicPayloadV2(a,b),"LOCAL_IMMUTABLE_FIELD_EQUALITY_NOT_RECONCILIATION");
 }
HSBI_EconomicLedgerRecordV2 registry[];ArrayResize(registry,1);registry[0]=a;
 HSBI_EconomicLedgerRecordV2 emptyRegistry[];DGCheck("E1-NEW-OBSERVATION",HSBI_ClassifyEconomicIdentityV2(a,independentFixture,true,emptyRegistry,true)==HSBI_ECON_V2_NEW,"IDENTITY_OBSERVATION_NOT_FUNDING");
 DGCheck("E1-EXACT",HSBI_ClassifyEconomicIdentityV2(a,independentFixture,true,registry,true)==HSBI_ECON_V2_NO_OP,"PROPOSED_V2");
 b=a;b.profit+=1;DGCheck("E1-PROFIT",HSBI_ClassifyEconomicIdentityV2(b,b,true,registry,true)==HSBI_ECON_V2_CONFLICT,"PROPOSED_V2");
 b=a;b.swap=-1;DGCheck("E1-SWAP",HSBI_ClassifyEconomicIdentityV2(b,b,true,registry,true)==HSBI_ECON_V2_CONFLICT,"PROPOSED_V2");
 b=a;b.commission=-1;DGCheck("E1-COMMISSION",HSBI_ClassifyEconomicIdentityV2(b,b,true,registry,true)==HSBI_ECON_V2_CONFLICT,"PROPOSED_V2");
 b=a;b.fee=-1;DGCheck("E1-FEE",HSBI_ClassifyEconomicIdentityV2(b,b,true,registry,true)==HSBI_ECON_V2_CONFLICT,"PROPOSED_V2");
 b=a;b.profit=60;b.commission=-10;DGCheck("E1-SAME-NET",HSBI_ClassifyEconomicIdentityV2(b,b,true,registry,true)==HSBI_ECON_V2_CONFLICT,"PROPOSED_V2");
 b=a;b.magic=8;DGCheck("E1-MAGIC-NOT-NEW-SOURCE",HSBI_ClassifyEconomicIdentityV2(b,b,true,registry,true)==HSBI_ECON_V2_CONFLICT,"PROPOSED_V2");
 b=a;b.accountLogin=2;DGCheck("E1-FOREIGN-AUTHORITY",HSBI_ClassifyEconomicIdentityV2(b,a,true,registry,true)==HSBI_ECON_V2_UNAVAILABLE,"PROPOSED_V2");
 DGCheck("E1-UNKNOWN-PROVENANCE",HSBI_ClassifyEconomicIdentityV2(a,independentFixture,false,registry,true)==HSBI_ECON_V2_UNAVAILABLE,"PROPOSED_V2");
 DGCheck("E1-UNKNOWN-REGISTRY",HSBI_ClassifyEconomicIdentityV2(a,independentFixture,true,registry,false)==HSBI_ECON_V2_UNAVAILABLE,"PROPOSED_V2");
 b=a;b.knownFieldsMask=0;DGCheck("E1-UNKNOWN-FACTS",HSBI_ValidateEconomicRecordV2(b)==HSBI_ECON_V2_UNAVAILABLE,"PROPOSED_V2");
 b=a;b.accountLogin=9223372036854775807;DGCheck("E1-LONG-MAX-ACCOUNT",HSBI_ValidateEconomicRecordV2(b)==HSBI_ECON_V2_NO_OP,"PROPOSED_V2_TYPED_BOUNDARY");b=a;b.dealTicket=18446744073709551615;DGCheck("E1-ULONG-MAX-DEAL",HSBI_ValidateEconomicRecordV2(b)==HSBI_ECON_V2_NO_OP,"PROPOSED_V2_TYPED_BOUNDARY");
 b=a;b.schemaVersion=2;DGCheck("E1-UNKNOWN-SCHEMA",HSBI_ValidateEconomicRecordV2(b)==HSBI_ECON_V2_UNAVAILABLE,"PROPOSED_V2");
 b=a;b.profit=0;b.dealNet=0;a=b;a.profit=-0.0;DGCheck("E1-CANONICAL-ZERO",HSBI_SameEconomicPayloadV2(a,b),"PROPOSED_V2_ZERO_POLICY");DGFixture(a);
 double nan=MathArcsin(2.0);bool nanReady=!MathIsValidNumber(nan);
 if(!nanReady){dg_infra++;Print("DG01|GEN-NAN|INFRASTRUCTURE_ERROR|nonfinite fixture unavailable");}
 else {b=a;b.profit=nan;DGCheck("E1-NONFINITE",HSBI_ValidateEconomicRecordV2(b)==HSBI_ECON_V2_REJECT,"PROPOSED_V2");}
 HSBI_AllocationLedgerRecord al,other;ZeroMemory(al);al.sourceDealKey="D101";al.allocationEventId=44;al.sourceDealNet=al.available=al.finalReserveAllocated=50;al.valid=true;al.status=HSBI_STATUS_COMPLETED;other=al;
 DGCheck("E2-VECTOR-EXACT",HSBI_ClassifyAllocationDuplicate(al,other)==1,"CURRENT_SOURCE");other.finalReserveAllocated=0;other.partialFarAllocated=50;DGCheck("E2-SAME-TOTAL",HSBI_ClassifyAllocationDuplicate(al,other)==2,"CURRENT_SOURCE_EXPECTED_DEFECT");
 other=al;other.finalReserveAllocated=-50;other.partialFarAllocated=100;DGCheck("E2-NEGATIVE-BUCKET",!HSBI_ValidateAllocationConservation(other),"CURRENT_SOURCE_EXPECTED_DEFECT");other=al;other.finalReserveAllocated=60;DGCheck("E2-OVERALLOCATION",!HSBI_ValidateAllocationConservation(other),"CURRENT_SOURCE");
 HSBI_ReserveCatchUpInput x=DGReserve(),y=x;DGCheck("E2-BOUND-SOURCE",HSBI_EvaluateReserveCatchUp(x).valid,"CURRENT_SOURCE");y.reserveEligibleMoneyAlreadyAllocated=false;y.reserveAllocationSource.reserveAllocated=0;y.reserveAllocationSource.alreadyConsumed=50;DGCheck("E2-ALREADY-CONSUMED",!HSBI_EvaluateReserveCatchUp(y).valid,"CURRENT_SOURCE_EXPECTED_DEFECT");
 y=x;y.consumptionKey.sourceAllocationKey="FOREIGN";DGCheck("E2-FOREIGN-ALLOCATION",!HSBI_EvaluateReserveCatchUp(y).valid,"CURRENT_SOURCE_EXPECTED_DEFECT");
 y=x;y.hasPriorConsumption=true;y.priorConsumptionKey=y.consumptionKey;DGCheck("E2-DUPLICATE-CONSUMPTION",!HSBI_EvaluateReserveCatchUp(y).valid,"CURRENT_SOURCE_NEW_PERMISSION_BLOCKED");
 y=x;y.reserveAllocationSource.sourceReconciled=false;DGCheck("E2-UNKNOWN-AUTHORITY",!HSBI_EvaluateReserveCatchUp(y).valid,"CURRENT_SOURCE_NO_GRANT_NOT_TYPED_UNAVAILABLE");
 HSBI_RiskInput ri;HSBI_RiskLimits lim;ZeroMemory(ri);ZeroMemory(lim);ri.snapshotFresh=true;ri.projectedMargin=10;ri.projectedMarginLevel=1000;ri.freeMarginAfter=100;lim.maxProjectedMargin=100;lim.minMarginLevel=100;lim.maxGrossExposure=100;lim.maxManagedPositions=10;lim.maxWorstCaseLoss=lim.maxTransitionLoss=lim.maxSpread=lim.maxCycleDrawdown=lim.maxAccountDrawdown=100;
 DGCheck("E3-RISK-VALID",HSBI_ValidateRiskInput(ri,lim).passed,"CURRENT_SOURCE");
 if(nanReady){ri.projectedMargin=nan;DGCheck("E3-NAN-MARGIN",!HSBI_ValidateRiskInput(ri,lim).passed,"CURRENT_SOURCE_EXPECTED_DEFECT");}
 ri.projectedMargin=-1;DGCheck("E3-NEGATIVE-MARGIN",!HSBI_ValidateRiskInput(ri,lim).passed,"PROPOSED_NONNEGATIVE_DOMAIN_NOT_APPROVED");
 double top=0;R0H_Unbits((ulong)9218868437227405311,top);double inf=top;inf*=2.0;
 if(MathIsValidNumber(inf)){dg_infra++;Print("DG01|GEN-INF|INFRASTRUCTURE_ERROR|infinity fixture unavailable");}
 else {HSBI_MoneyState ms;ZeroMemory(ms);ms.valid=true;ms.revision=1;ms.finalReserve=inf;DGCheck("E3-INFINITY-MONEY",!HSBI_ValidateMoneyState(ms),"CURRENT_SOURCE_EXPECTED_DEFECT");}
 HSBI_TransactionBarrierInput tx,ty;ZeroMemory(tx);tx.expectedActionId=tx.transaction.actionId=1;tx.transaction.eventId=2;tx.lastAppliedEventId=1;tx.transaction.expectedVolume=tx.transaction.accumulatedVolume=1;tx.transaction.actualPositionRead=tx.actualDealRead=tx.ownershipConfirmed=true;tx.expectedStateRevision=tx.actualStateRevision=7;tx.transaction.outcome=HSBI_TX_COMPLETED;
 DGCheck("E3-TX-VALID",HSBI_TransactionBarrierPassed(tx),"CURRENT_SOURCE");if(nanReady){ty=tx;ty.transaction.accumulatedVolume=nan;DGCheck("E3-NAN-FILL",!HSBI_TransactionBarrierPassed(ty),"CURRENT_SOURCE_EXPECTED_DEFECT");}
 ty=tx;ty.transaction.outcome=HSBI_TX_PARTIAL;DGCheck("E3-PARTIAL",!HSBI_TransactionBarrierPassed(ty),"CURRENT_SOURCE");ty=tx;ty.ownershipConfirmed=false;DGCheck("E3-OWNERSHIP",!HSBI_TransactionBarrierPassed(ty),"CURRENT_SOURCE");ty=tx;ty.actualDealRead=false;DGCheck("E3-MISSING-CONFIRMATION",!HSBI_TransactionBarrierPassed(ty),"CURRENT_SOURCE");
 HSBI_RecoveryContext ctx;HSBI_InitializeContext(ctx,HSBI_RUNTIME_DISABLED);ctx.accountLogin=1;ctx.symbol="X";ctx.magic=7;ctx.cycleId=1;ctx.currentState=ctx.previousState=HSBI_STATE_FAR_ACTIVE;ctx.stateRevision=1;ctx.far=DGPosition(100);DGCheck("E4-ONE-FAR",HSBI_ValidateContext(ctx),"CURRENT_SOURCE");
 ctx.initialBuy=DGPosition(101);DGCheck("E4-DISTINCT-FAR-SLOTS",!HSBI_ValidateContext(ctx),"CURRENT_SOURCE_EXPECTED_DEFECT");ctx.initialBuy=ctx.far;DGCheck("E4-ALIAS-OBSERVATION",ctx.initialBuy.identifier==ctx.far.identifier,"PHYSICAL_ALIAS_ONLY_SLOT_ACCEPTANCE_UNDECIDED");
 y=x;y.reserveSourceProof.identity.accountLogin=2;DGCheck("E4-INDEPENDENT-EXPECTED",!HSBI_ValidateReserveSourceProof(y.reserveSourceProof,x.expectedReserveIdentity),"LOCAL_EQUALITY");y.expectedReserveIdentity=y.reserveSourceProof.identity;DGCheck("E4-COPIED-EXPECTED",HSBI_ValidateReserveSourceProof(y.reserveSourceProof,y.expectedReserveIdentity),"OBSERVATION_NOT_PROVIDER_PROOF_NOT_SOLVER_BYPASS");
 DGCheck("E4-MISSING-PROVIDER",HSBI_ClassifyEconomicIdentityV2(a,independentFixture,false,registry,true)==HSBI_ECON_V2_UNAVAILABLE,"PROPOSED_V2_BOUNDARY");b=a;b.dealTicket=99;DGCheck("E4-UNKNOWN-SOURCE",HSBI_ClassifyEconomicIdentityV2(b,a,true,registry,true)==HSBI_ECON_V2_UNAVAILABLE,"PROPOSED_V2_BOUNDARY");
 DGCodecTests();
 Print("[HSBI_DG01_NATIVE_RESULT] PASS=",dg_pass," FAIL=",dg_fail," INFRASTRUCTURE_ERRORS=",dg_infra,"; NO_TRADING=YES");
}
