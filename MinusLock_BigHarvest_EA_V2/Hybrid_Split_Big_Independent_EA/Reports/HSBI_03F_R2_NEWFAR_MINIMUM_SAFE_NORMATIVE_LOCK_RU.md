# HSBI-03F-R2 — NewFar MINIMUM_SAFE_V1: выбранный normative lock

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

Status=OWNER_SELECTED_A_TEXT_PINNED;FormalApprovalReceipt=NOT_REGISTERED.
LockId=HSBI_NEWFAR_MINIMUM_SAFE_SELECTION_LOCK_V1;SelectedVariant=A;SelectedPolicy=MINIMUM_SAFE_V1;SelectedTextVersion=HSBI-03E-R1.
SourceFile=Reports/HSBI_03E_NEWFAR_OBJECTIVE_RESOLUTION_RU.md;SourceBlobSHA=a29b28fe806b7bd53cc49a34803b25b4b9b55543;commonF24–35,A39–44,selectedparagraph42.

## Точный выбранный paragraph

> Сначала построить полный declared candidate set и выполнить одинаковую F(c) для всех required proofs. Среди feasible normalized grid volumes выбрать lexicographic minimum tuple (N,RiskNext,MarginNext,FutureTransitionCount,−m(c),CanonicalCandidateTieID). Это minimum-safe-first. При одинаковом N сохраняются Doc14 risk/margin/transitions/safety tie rules; последний deterministic key разрешает лишь полное числовое равенство и не подтверждает authenticity. Нельзя выбрать candidate вне F. Если ни одного feasible candidate — NO_SAFE_CANDIDATE без state delta. Непроверенный required tail — UNPROVEN/UNAVAILABLE. Новая objective policy меняет plan digest; старый persisted plan не переписывается.

Не меняется опубликованная версия; R2 фиксирует выбор владельца вбеседе. Tuple:
(N,RiskNext,MarginNext,FutureTransitionCount,−m(c),CanonicalCandidateTieID).
m(c)=min_l CatchUpMargin_l по объявленному requiredset. SafetyF beforeoptimization,не weightedpenalty. Missing required proof не candidate с«достаточно хорошим»objective.

## Источники и совпадения/противоречия

Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:9–23 ascendingvalidgrid,0<N<F,compression,money/risk/margin/future/terminalgates,firstminimumsafe.
Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md:3–7,35–37 completeproof и risk-first tuple.
Include/Planning/HSBI_NewFarCandidate.mqh:26–40 HSBI_IsCompleteCandidateProof/HSBI_CompareCandidateTieBreak;SourceBlobSHA=758f1c89cf75701d3616dabec2fcb06413ee2d4a.
Include/Planning/HSBI_NewFarSolver.mqh:108–151 enumeratescandidates,controlCatchUp,gate,safe[],comparatorselection;source47–59 input/plandigest;source140 selectedcontrolmargin safetyBuffer.
Reports/HSBI_03E_CONTRACT_DEPENDENCY_RECONCILIATION_RU.md:recovery/newfarbundle;HSBI_03E_OWNER_FINAL_DECISION_BALLOT_RU.md:CR09/companionchoice;CR09 fullapproval stillAWAITING.

| Правило | Совпадает | Требуется будущее согласование |
|---|---|---|
| Proof feasibility до selection | Doc14,Doc29,selectedA по намерению | ActualallrequiredCatchUp/sourceevidence ещёне обеспечены |
| Primarycriterion | Doc14:Nfirst,selectedA:Nfirst | Doc29/currentcomparator:Riskfirst |
| Secondary Risk/Margin/Transitions | Names совпадают | Порядокдействуетпосле N,а не beforeN |
| Safety buffer | selectedA:−minallmargin | currentcode140:onecontrolcatchmargin |
| Final tiebreak | deterministic totalTieID | codec/profile/evidenceAWAITING;roundedtextdigest не auth |
| Actual residual beforepromotion | Doc14:25,Docs13:17 | ExistingselectedN не actualpromotion,ERR045OPEN |

Currentcode не объявлен соответствующим выбранному A. Будущий changeDoc29:3 и comparator36–40 потребует отдельного versionedamendment/allowlist/implementationpermission;этим этапомне разрешён.
Выбор objective разрешаетстратегическийприоритет, нонеутверждает 15 других moneycontracts. Inputrequirementm(c)выбран; полный CR09 с requiredset,cost/funding/tail/providerdefinitions ещё AWAITING. Нельзяприэтомназвать currentonecontrolmargin корректным minimum.

## Проверяемое различие

Two feasiblemodel candidates,identicalprofiles:
a:N0.2,Risk18,Margin40,Transitions2,m2;
b:N0.3,Risk12,Margin50,Transitions3,m4.
SelectedA→a;currentrisk-first→b. Это lexicographic derivation,не nativePASS ине brokerreachabilityproof.
Unsafe x:N0.1,Risk1,m−1 исключёнобоимипорядками.
При equalN дальнейший risk/marginorder сохраняется. Эти примеры не заменяют полноценный all-level feasibility.

## Тесты и persistedplans

Непосредственнопрочитаны Tests/MQL5/HSBI_Skeleton_Tests.mq5:
-180–195:T104–T119 преимущественно failure/status/count/immutableplan cases;нет assertselectedminimumvsrisk.
-196:T120 equalN/Risk/Margin/Transitions/safety,последний digest tie;изменение primaryorder самопосебенеобязаноизменитьэтот expected.
-288–292:T208/T211aggregate maxloss/controlpolicy;не assertminimumCatchUp.
В 11scannedMQL/C++testsource не найдено assert чтения solverresult.transitionLoss. Это staticcoveragefinding,не testexecution.
Будущие paired A/B выборы, m_all vsm_control,unsafeexclusion,permutation/determinism,strictgrid/actualresidual и versionmismatch tests обязательны. Frozenhistoricalexpected не переписываются; при policychange новая versioned suite.

Persistedplans должны получить ObjectiveVersion=MINIMUM_SAFE_V1,requiredLevelSet/profile/cost/providerreferences и schema receipts. Старые plan bytes/digests не пересчитываютсядлявидимогосовпадения. Старый risk-firstplan сохраняется historicalread-only,новая action→reconcile/replan поотдельной compatibilitypolicy,не auto-resume. Changingonlycomparator withoutplanversion silentlychangesbehaviour и недопустимо.

## Приёмка и unresolved

Приёмка: exactsourcequote42;Nprimarytuple;Fbeforeobjective;no newpermission;explicitDoc29/comparator/tie/minscope incompatibilities;versionedfuturetests/migration.
Unresolved:CanonicalCandidateTieIDencoding,native/currency/grid/source/cost/snapshotprofiles;fullCR09all-levelpolicy;provider/journal/actualresidual;future amendments. R11stillNO.
Связи: [owner](HSBI_03F_R2_OWNER_POLICY_SELECTION_RU.md),[ERR018](HSBI_03F_R2_ERR018_SOURCE_LEVEL_AUDIT_RU.md),[proofs](HSBI_03F_R2_TRANSITION_CATCHUP_MATH_PROOFS_RU.md),[futurecontract](HSBI_03F_R2_TRANSITION_CATCHUP_CONTRACT_V1_RU.md),[readiness](HSBI_03F_R2_DEPENDENCY_AND_READINESS_MATRIX_RU.md).
