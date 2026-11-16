# HSBI-03G-R1 — совместимость MINIMUM_SAFE_V1

DocumentVersion=HSBI-03G-R1-V1
SourceCommitSHA=e68e73e1b252d20e15588645004f9066c6ae88f0
Scope=Selected companion objective / proposed all-level binding
EvidenceClass=STATIC_REVIEWED; MATH_DERIVED; TEST_SPECIFIED_NOT_RUN
NormativeStatus=PROPOSED_AWAITING_OWNER_APPROVAL
Dependencies=NewFar A already selected; CR-09; D-08/10/11/12/13/15/16

Репозиторий: `ic8812825-maker/chatgpt.com-codex`, ветка `work`. Все пути ниже находятся внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`. Новый текст является проектом контракта, а не утверждением реализации. Выбор D-06 A и companion NewFar A сохраняется; полный CR-09 не утверждён. Формальных approval receipts нет.

PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.

UNAVAILABLE означает отсутствие обязательного доказательства; CONFLICT — противоречие данных; REJECT — доказанное нарушение. Каждый результат запрещает новый финансовый эффект, delta=0. NO_OP допустим только после проверки подлинного полного прежнего event body и receipt. Числа математических примеров не являются брокерскими константами.

## Сохраняемый выбор и source conflict

- [Reports/HSBI_03F_R2_NEWFAR_MINIMUM_SAFE_NORMATIVE_LOCK_RU.md:1–77](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03F_R2_NEWFAR_MINIMUM_SAFE_NORMATIVE_LOCK_RU.md#L1-L77). SourceBlobSHA=`91aeb48e911c2891c8267b9fedd831f991ceaf56`; EvidenceClass=STATIC_REVIEWED.
- [Reports/HSBI_03E_NEWFAR_OBJECTIVE_RESOLUTION_RU.md:24–54](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03E_NEWFAR_OBJECTIVE_RESOLUTION_RU.md#L24-L54). SourceBlobSHA=`a29b28fe806b7bd53cc49a34803b25b4b9b55543`; EvidenceClass=STATIC_REVIEWED.
- [Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:9–25](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md#L9-L25). SourceBlobSHA=`f779a1a87ab2d0163c17d6c855c206047d970cec`; EvidenceClass=STATIC_REVIEWED.
- [Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md:3–7](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md#L3-L7). SourceBlobSHA=`33796d41e5efa824fff32a38f4d09fefe90b5e0b`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_NewFarCandidate.mqh:26–40](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarCandidate.mqh#L26-L40) — HSBI_IsCompleteCandidateProof / HSBI_CompareCandidateTieBreak. SourceBlobSHA=`758f1c89cf75701d3616dabec2fcb06413ee2d4a`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_NewFarSolver.mqh:138–151](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarSolver.mqh#L138-L151) — candidate safetyBuffer / selection. SourceBlobSHA=`3d19eccd6cd318b9b4591e2bc0ccaa95f661930d`; EvidenceClass=STATIC_REVIEWED.

CompanionPolicyId=NEWFAR-OBJECTIVE;SelectedVariant=A;SelectedPolicy=MINIMUM_SAFE_V1;OwnerSelection=CONFIRMED_IN_CONVERSATION;FormalApprovalReceipt=NOT_REGISTERED. Выбор не открывается заново и не считается утверждением полного CR-09. Никакого семнадцатого CanonicalDecisionId нет.

Выбранный lexicographic minimum:
(N, RiskNext, MarginNext, FutureTransitionCount, −m(c), CanonicalCandidateTieID), где m(c)=min по ВСЕМ required levels CatchUpMargin_l. Safety feasibility проверяется до objective; weighted penalty, relaxing caps или выбор по одной хорошей margin запрещены. Нет feasible candidate →NO_SAFE_CANDIDATE; missing evidence отдельно отражается как UNAVAILABLE/INCOMPLETE в diagnostics, а не как доказательство отсутствия математически возможного решения.

Docs14 minimum-safe и Docs29/comparator risk-first расходятся по приоритету N. Current safetyBuffer=single control margin, не m(c). Поэтому даже смена порядка comparator без all-level proof не реализует выбранную политику. Общие правила совпадают: только admissible candidates, deterministic ordering, неизменность plan, risk/margin/compression guards. Расхождения требуют будущих versioned amendments и разрешения на код, не автоматического изменения настоящим audit.

## Явные математические примеры

Все candidate rows имеют frozen required set {L1,L2}; единицы risk/margin сопоставимы в пределах fixture, volume grid0.1. Transition cap12, initialRisk30,tolerance1,marginCap100,oldFar1. Остальные feasibility clauses предпосланы как математические условия, не provider evidence. Меньший N небезопасного x никогда не участвует.

| Candidate | N | Risk | Margin | Transitions | T_max | M_L1/M_L2 | Feasible | Rank minimum-safe / risk-first |
|---|---:|---:|---:|---:|---:|---|---|---|
| a |0.2|18|40|2|10|2/2|MODEL_ONLY|1/2|
| b |0.3|12|50|3|6|4/4|MODEL_ONLY|2/1|
| x |0.1|1|20|1|3|4/−1|NO|excluded|

Minimum-safe выбирает a, existing risk-first b. Это не universal dominance: b снижает measured risk, a уменьшает объём и margin. Owner objective уже A; новая работа не пересматривает preference.

Tie fixture: одинаковый N0.2,Risk10,Margin40,Transitions2. d: M=(10,1), e: M=(4,3). Истинный m(d)=1,m(e)=3 →e; один control L1 ошибочно предпочёл бы d. Full tie d/e с одинаковыми numeric tuple решается только approved CanonicalCandidateTieID total order. При перестановке входного candidate списка победитель сохраняется. Смена RequiredLevelIDs или profile требует новых proofs, не перестановки старого rank.

## Profile и deterministic order

ObjectiveVersion=MINIMUM_SAFE_V1. CandidateSetManifest замораживает полный объявленный grid, ограничения и required-level manifest до расчёта. Недопустимые и unknown candidates не превращаются в feasible; если утверждение «минимальный допустимый N» требует исключить smaller candidates, неизвестный smaller candidate нельзя тихо отбросить и выдать больший как доказанно minimum-safe. Разрешается diagnostic best-known-feasible с отдельным nonqualified статусом, без финансового разрешения.

CanonicalCandidateTieIDProfileVersion остаётся AWAITING_EVIDENCE. Требуются injective versioned encoding account/candidate/grid/input/proof scope и deterministic total order байтов canonical UTF-8 либо другого явно утверждённого wire profile. Нельзя использовать время, ticket delivery order, randomness или hash-table iteration. Digest не доказывает source authenticity, а округлённый DoubleToString digest не доказан как collision-free representation. Exact equality/profile/unsupported values должны определяться numeric/codec bundle, не локальным epsilon comparator.

## Legacy и persisted plans

ResultSchemaVersion/ProofSchemaVersion/NumericProfileVersion/ObjectiveVersion/RequiredLevelManifestVersion/CostBasisVersion входят в original receipt и plan binding. Новый objective/required scope меняет plan version. Старые RISK_FIRST планы сохраняются со старой semantics; нельзя назвать их MINIMUM_SAFE без re-evaluation. При unknown version →UNSUPPORTED/QUARANTINE, no silent migration. Новые native vectors добавляются отдельной versioned группой; старые expected/frozen artifacts не меняются.

Tests T108/T118–T120 в Docs29 относятся к прежнему deterministic/immutability scope. Они могут потребовать новой параллельной expectation group при будущей смене objective. Само имя test не доказывает execution. Исторические 7 PASS/16 FAIL C++ shim не пересчитываются под новую policy. Native qualification должна отдельно подтвердить full feasible path, tie/permutation/profile handling и post-fill residual revalidation.

OpenQuestions: full CR09 approval, numeric/codec TieID profile, complete candidate grid authority, all-level evidence, legacy compatibility receipts.
AcceptanceCriteria: OBJECTIVE-01…08 qualification; unsafe/missing proof не улучшает rank; minAllMargin вместо control; persisted schema mismatch блокирует; production comparator неизменён.

Связи: [all-level](HSBI_03G_R1_ALL_LEVEL_FEASIBILITY_PROOF_RU.md), [vectors](HSBI_03G_R1_QUALIFICATION_TEST_SPEC_RU.md), [ballot](HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md).
