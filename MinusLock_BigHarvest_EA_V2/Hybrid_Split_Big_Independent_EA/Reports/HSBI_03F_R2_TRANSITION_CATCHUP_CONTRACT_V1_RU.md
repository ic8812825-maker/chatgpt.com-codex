# HSBI-03F-R2 — HSBI_TRANSITION_AND_CATCHUP_CONTRACT_V1

Version=**HSBI-03F-R2-V1**. SourceCommitSHA=`ae367ff2925da4d845a413326c840fe468ff451b`.
Repository=`ic8812825-maker/chatgpt.com-codex`; Branch=`work`.
Все относительные пути относятся к `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`.

D-06 A и companion NewFar A выбраны владельцем в беседе. FormalApprovalReceipt=NOT_REGISTERED. Остальные 15 денежных решений остаются AWAITING/BLOCKED; CR09_FULL_APPROVAL=AWAITING.
EvidenceClass: CONFIRMED_STATIC/STATIC_CONFIRMED — чтение исходного кода; MATH_DERIVED — математический вывод при указанных предпосылках; TEST_SPECIFIED_NOT_RUN — заданный, но не выполненный тест; HISTORICAL_TEST_RESULT — прежний artifact.
Native, compile, runtime, mutation, crash и concurrency испытания на этом этапе не запускались.

EXECUTION_MODE=GITHUB_MCP_REMOTE_ONLY; LOCAL_FILE_OPERATIONS=0; NATIVE_MQL5_TESTS=NOT_RUN.
PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO.
Новый contract с пометкой PROPOSED не считается утверждённым или реализованным. UNAVAILABLE означает отсутствие обязательного evidence, CONFLICT — противоречие, REJECT — известное нарушение. Все три результата запрещают новый финансовый эффект. NO_OP требует проверки полного прежнего body/receipt.

Критические SourceBlobSHA:
- `Include/Planning/HSBI_NewFarSolver.mqh`: `3d19eccd6cd318b9b4591e2bc0ccaa95f661930d`.
- `Include/Planning/HSBI_FutureSmallProofAggregator.mqh`: `4678ae152960e98b9f398b4497786061d7e8a524`.
- `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh`: `87a8b7e97727ce6e47c2a2f0abc3e237f6203204`.

Status=PROPOSED_AWAITING_CR09_AND_DEPENDENT_BUNDLES.
EvidenceClass=CONTRACT_PROPOSAL_SUPPORTED_BY_STATIC_AND_MATH_REVIEW.
Этот текст не реализация и не формальный approval. Выбранный MINIMUM_SAFE_V1 требует корректного m(c),но полный CR09,его provider/numeric/funding manifests остаются AWAITING.

## 1. Источники и предмет изменения

Docs04:15,24,30,33–36;Docs08:6–24;Docs13:9–20;Docs30:3–7;Docs31:3–7;Docs32:3–7.
Точные пути этих Docs и SourceBlobSHA находятся в source inventory [finalverdict](HSBI_03F_R2_FINAL_VERDICT_RU.md).
Include/Planning/HSBI_FutureSmallSolver.mqh:87–147 (SourceBlobSHA=be55c93f051f57ddffd189b9d2e8eee4c3ddaf9d);
HSBI_FutureSmallTypes.mqh:48–62 (ee962ed40a99b0d0a1fdd22f2ee071cc3fb6cbcc);
HSBI_NewFarCandidate.mqh:7–31 (758f1c89cf75701d3616dabec2fcb06413ee2d4a);
HSBI_NewFarSolver.mqh:118–151;ReserveAllocationTypes:15–30;RuntimeDecisionTypes:11–17/Validator19–28.
Мотив: singlecontrolCatchUp не all-requiredproof;result.transitionLoss сейчас FarLoss;volume/source/basis не должны смешиваться.

## 2. Обязательный envelope каждой денежной метрики

Каждое значение несёт MetricKind,Value/UnavailableReason,CurrencyCode,MinorUnitScale,NumericProfileVersion,CostBasisManifestID/Version,ScopeID,PlanID,StateRevision,RegistryRevision,SourceOrProjectionReferences,Snapshot/CostReceiptReferences,ValueKind(ACTUAL_SETTLED/PROJECTED/DERIVED_PROJECTED),ProofSchemaVersion и OriginalReceiptBinding.
Идентичность account/broker/server/symbol/magic/cycle проверяется независимо от предъявленного DTO. OriginPlan исторического source не обязан равняться current consumption plan;их связь отдельна.
ProjectedReference=(ProjectionPlan,LevelID,Role,InstrumentProfile),а не выдуманный будущий DealTicket. PhysicalSourceKey=(Broker,Server,Account,DealTicket) существует только для independently confirmed fact. Projection не создаёт grant.
Snapshot binding включает original content receipt,clock domain/skew/expiry/reconciliation epoch. Self-hash не auth.
Currency/profile/basis mismatch→CONFLICT;known bad type/nonfinite/range→REJECT;unknown evidence→UNAVAILABLE,delta0.
Exact settled signed64 checked;projection с approved numericerrorbounds и finitedomain. Если errorbound неизвестен, positive floating scalar не safetyproof.
Общие metadata применяются коВСЕМ monetary rows ниже; для counts explicitlycurrency/costNOT_APPLICABLE,но scope/revision/receipt обязательны.

## 3. Метрики: формула, источник, scope,допуски

| Metric | Формула/источник | Kind,scope,snapshot | Domain/error/identity |
|---|---|---|---|
| ActualTransitionLoss | max(0,−Σ unique actual closingnet) | ACTUAL_SETTLED;OperationID/membership source/fill receipts;actualclosewindow | exact≥0;полный source set и costattribution;unknownmembership unavailable |
| ProjectedBasketTransitionLoss_l | max(0,−Σ declared closing-leg projectednets_l) | PROJECTED;LevelID;его market/costsnapshot;explicitCoreclosefraction | finite≥0;projectedlegmembership/volume/basisreceipt;не actual |
| MaximumProjectedTransitionLoss | max_required T_l | DERIVED_PROJECTED;RequiredLevelSet manifest;ссылкинаВСЕ per-levelreceipts | finite≥0;empty/incomplete set unavailable;не FarLoss |
| ControlLevelAbsoluteFarLoss | max(0,−FarCloseNet_c) | PROJECTED;ControlLevelID,Farposition/projectionvolume,close-side,costsnapshot | finite≥0;никакогоб aselinesubtraction;не Tmax |
| ReserveGainMoney_l | PREVIEW:approvedeligible projectedsource allocation;FUNDING:independentlyconfirmed eligibleFree | Kind явный; source/manifest/bucket/revision;allocation/free receipt | ≥0;no Small→Big,no reshare allocated,no guessedavailable |
| CatchUpMarginByLevel_l | G_l−A_l−B_l | DERIVED_PROJECTED;matchingcurrency,volume,basis,levelreceipts | signedfinite;B disjoint;numericinterval lowerbound для gate |
| MinimumCatchUpMargin | min_required Margin_l | DERIVED_PROJECTED;полный requiredmanifest | signedfinite;empty/incomplete unavailable;controlmargin не minimum |
| RequiredLevelCount | cardinality immutable RequiredLevelIDs | COUNT;plan/revision/manifest;currency/costNOT_APPLICABLE | profile2…128 длясовместимости currentFS;unknown unsupported |
| ProvenLevelCount | count distinct required IDs withvalid completeproof | COUNT;sourceproof set/revision | 0…RequiredCount;duplicates неувеличивают; samecount≠sameset |
| ProofCompleteness | COMPLETE/INCOMPLETE/CONFLICT/UNSUPPORTED из set/evidence check | ENUM;allreceipt references incltailrequirements | не callerboolean;COMPLETE только exactrequiredset+validreceipts |

Для per-levellotgate предлагается ReserveShare_l×NetBigVolume_l>FarBefore_l с proof-boundvolumes/direction. Если иной obligation intended,он должен быть отдельно named в manifest;неоставлять Nconstant поумолчанию. Currentcode123 использует candidate—этоне approval длявсех futurelevels.
Actual net/postings и RecoveryResult D06-A несливаются: Initialexclusion касается Recovery,не удаления actual transitionlosses. D05sticky/peak/reset хранится отдельно от currentActualTransitionLoss.

## 4. Eligible reserve:два разныхрежима

PREVIEW_ONLY:
G_l получается из approved EligibleReserveSourceSet_l и allocationpolicy,с fullsource/projectionassociation. Current codeCore-only—явный profilemathfixtures,неуниверсальнаянорма всех будущих source sets. Core/Trend могут входить только поутверждённой policy;Small не BigReserve безотдельного transfer.
Unallocatedpreview→projectednet×share;alreadyallocatedpreview—связанный allocation/freeamount,неповторное share.
Будущий positiveprojectedsource не actualfunds;numericfeasiblepreview не reserve/spend.

FUNDING_AUTHORITY:
G_l≤confirmedeligibleFree по complete globalregistry. Длякаждого bucketGrant=Consumed+Reserved+Free;originalsourceallocatedonce;draft не spendable;residualheld не free-for-anyrole.
New reserve/consume/release/transfer меняют balance+eventreceipt+revision атомарно; oldexactreceipt NO_OP;alteredreceipt CONFLICT. Sourcealias/newAllocationKey не refreshcapacity. UNKNOWN outcome не release/resend.
Для sequentiallevels финансовый prefixtrace уменьшаеттотже Free иучитываеттолько actualconfirmed permittedinflows. Неисполненная futureprofit непополняет inventory.
Для mutuallyexclusive scenarios один source можновалюироватьповторно без debit,нонеиспользоватьэто каксумму independentpermissions. LevelSemantics manifest явен.

## 5. Required/provenlevels и tail

RequiredLevelIDs/Order/ExpectedCount/TerminalPolicy/TailRequirement frozen в plan до evaluation. Set providedvalidIDs должен точно совпастьс requiredset;неустанавливать requiredcount из p.provenDepth послефакта.
Everyrequiredlevel имеет money,margin,risk,cost,source/eligibility,transition,Farprojection,marketclock/revision receipts и applicableprefixsafetyproof.
Unrequiredtail→UNPROVEN,не globalclaim. Если tailproofrequired,егоотсутствиеблокирует candidate. Terminal close требует operational/actualexecutioncontract,неодногофлага finiteSequence.
ProofLevelNotEvaluated/Unsupported/Missing не заменяютсянулём илисредним уровнем. Consistentcut/restartreconciliation обязателен.

## 6. Проверяемый all-level предикат

AllRequiredProofsValid =
ExactRequiredSetCovered AND AllPerLevelEvidenceValid AND RequiredTailEvidenceValid.
AllTransitionCapsPass =
for every required l:T_l≤FrozenAllowedCap_l
AND applicableActualCurrent/StickySafetyPass.
AllCatchUpMarginsPositive =
for every required l:MarginLowerBound_l>0.
OtherSafetyGatesPass =
ownership/actualresidual/grid/compression/slope/risk/margin/exposure/cost/clock
AND applicableSequentialFundingPrefixPass.
CandidateFeasible =
AllRequiredProofsValid AND AllTransitionCapsPass
AND AllCatchUpMarginsPositive AND OtherSafetyGatesPass.

При exactmath MarginLowerBound=G−A−B. При floating intervals lower=G_low−A_high−B_high с approved error budget;unknown interval→UNAVAILABLE.
Control policyWORST_CASE/FINAL/EXPLICIT определяеттолькодополнительный reporting/controlselection;неослабляет all-requiredgate в ALL_REQUIRED_V1scope.
Выбранный MINIMUM_SAFE_V1 ранжируетлишь CandidateFeasible; m(c)=minimum всех requiredmargins,не control.
Preview result должен иметь AuthorityLevel=PREVIEW_ONLY/CONDITIONAL_PREVIEW если будущие actualinflows/execution не доказаны; FundingAuthorised имеет отдельные independentcurrent+registry+transaction requirements. Никакой result неразрешает dispatch этимзаданием.

## 7. Result/proofversioning

ProposedResultSchemaVersion=HSBI-TC-RESULT-2.
ProposedProofSchemaVersion=HSBI-TC-PROOF-1.
NumericProfileVersion=UNBOUND_REQUIRED;ObjectiveVersion=MINIMUM_SAFE_V1(HSBI-03E-R1).
ContractVersion=HSBI-03F-R2-V1.
Требуются RequiredLevelManifestVersion,CostBasisVersion,SourceAuthorityProfile,SnapshotProfile,AllocationPolicyVersion,CompatibilityPolicy.
Result содержит Tmax,A_control,perlevelmargins,minMargin,required/provenIDs/counts,completeness,capreceipts,authorisationkind и bindings. На validresult recompute summaries из sealedperlevelproofs,непринимать caller-suppliedminimum.
LegacyResultHandling=READ_ONLY_UNVERSIONED_SCOPE_UNKNOWN;unversionedtransitionLoss неприниматькак Tmax или Actual.
OldcatchUpProofValid из schema без scope не all-required;новые ControlCatchUpValid и AllRequiredCatchUpValid разделены. Не upgradebool поумолчанию.
CompatibilityPolicy=EXPLICIT_SEMANTIC_MAPPING_OR_QUARANTINE. Preserveoldbytes/historyexpected. PersistedPlanMigration:retainoldrisk-firstplan,blockedreconciliation/replan подновой objective/schema,не rewrite/no autoresume. Appliedevents/consumed/sticky не reset.
Digest/receiptbinding:весь typedbody,individuallegnets/components,costamounts+IDs,levelvolumes,scope/profileversions,requiredset,control+minsummary,source/registry/journalrevisions. IDs-only или samebaskettotal недостаточны. Codec D12/native не selected—encodinggateBLOCKED.
Failedresult valuesUnavailable/None,не default0proof;publicconsumers проверяют valid/kind/scope/integrity до numericaccess.

## 8. Acceptance/unresolved

Нужны TL01…TL05/CU01…CU10 и positive/negative controls;partialactualmembership,duplicate/aliasfunding,missingrequiredIDs,staleversions,snapshotcontenttamper,noncontrolcostredistribution,signed64/binary64boundaries,errorbounds,all adapters,native/crash/concurrency evidence.
Contract можетбытьутверждёнтолько после owner выбора CR09/volume/eligibility/levelsemantics и dependent numeric/provider/journal manifests;никакого implementationpermission здесь.
Связи: [ERR018](HSBI_03F_R2_ERR018_SOURCE_LEVEL_AUDIT_RU.md),[math](HSBI_03F_R2_TRANSITION_CATCHUP_MATH_PROOFS_RU.md),[vectors](HSBI_03F_R2_TEST_VECTOR_SPECIFICATION_RU.md),[owner](HSBI_03F_R2_OWNER_POLICY_SELECTION_RU.md),[readiness](HSBI_03F_R2_DEPENDENCY_AND_READINESS_MATRIX_RU.md).
