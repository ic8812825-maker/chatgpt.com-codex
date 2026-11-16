# HSBI-03F-R2 — Фиксация выбора владельца

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


Status=OWNER_SELECTION_RECORDED_AUDIT_ONLY.

## Основание и точные версии

Основание — прямое поручение владельца HSBI-03F-R2 в текущей беседе. Предыдущий HSBI-03F-DRAFT-1 не превращается в подписанный документ и не публикуется задним числом.

| Выбор | Опубликованный источник | SourceBlobSHA |
|---|---|---|
| D-06 A | Reports/HSBI_03E_D06_POLICY_RESOLUTION_RU.md:29–67; выбранный paragraph56 |39342ea57a83a8dcd2f8e22ff8b87747c371d0ca|
| NewFar A | Reports/HSBI_03E_NEWFAR_OBJECTIVE_RESOLUTION_RU.md:24–44; выбранный paragraph42 |a29b28fe806b7bd53cc49a34803b25b4b9b55543|

Оба файла непосредственно перечитаны на SourceCommitSHA; контрольные blobs совпали. Текст HSBI-03E-R1 не изменяется.

## Записи выбора, не формальные receipts

```text
DecisionId=D-06
Variant=A
Policy=D06-A/HSBI-03E-R1
OwnerSelection=CONFIRMED_IN_CONVERSATION
FormalApprovalReceipt=NOT_REGISTERED
ImplementationPermission=NO

CompanionPolicyId=NEWFAR-OBJECTIVE
Variant=A
Policy=MINIMUM_SAFE_V1
PolicyTextVersion=HSBI-03E-R1
OwnerSelection=CONFIRMED_IN_CONVERSATION
FormalApprovalReceipt=NOT_REGISTERED
ImplementationPermission=NO
```

Не создаются цифровая подпись, credential владельца или вымышленный approval hash/date. Git commit author не заменяет owner signature.

## Смысл выбранной политики

D-06: R_all=Σ уникальных actual postings; E=R_all+O_phys−C_rem; Q=E−H_in; RecoveryRealized_A=R_all−I; RecoveryResult_A=Q−I.
Инвариант: E−H_in−RecoveryResult_A=I.
FinalClose result gate: RecoveryResult_A≥MinimumRecoveryProfitMoney+H_gate+MoneyTolerance; coverage, freshness, ownership/revision, отсутствие pending/unknown и actual completion проверяются отдельно.

NewFar: lexmin(N,RiskNext,MarginNext,FutureTransitionCount,−m(c),CanonicalCandidateTieID) только после feasibility; m(c) — minimum по required levels. Control margin не подставляется вместо minimum. Выбор входного требования к objective не утверждает весь CR-09, его source/funding/numeric/required-set/tail manifests.

## Все 16 самостоятельных решений

| № | CanonicalDecisionId | Состояние |
|---|---|---|
| D01 | D-01 | AWAITING |
| D02 | D-02 | AWAITING |
| D03 | D-03 | AWAITING |
| D04 | D-04 | AWAITING |
| D05 | D-05 | AWAITING; reset authority UNBOUND |
| D06 | D-06 | OWNER_SELECTED_A; formal receipt отсутствует |
| D07 | D-07 | AWAITING |
| D08 | D-08 | AWAITING |
| D09 | CR-09 | FULL_APPROVAL_AWAITING |
| D10 | NUM-EXACT-1 | AWAITING |
| D11 | NUM-DOMAIN-1 | AWAITING/EVIDENCE_BLOCKED |
| D12 | NUM-CODEC | AWAITING/NATIVE_NOT_RUN |
| D13 | SNAP-FIXTURE-1 | AWAITING/PROVIDER_BLOCKED |
| D14 | FUNDING-GLOBAL-ATTRIBUTION | AWAITING |
| D15 | MQL-DOMAIN | AWAITING/NATIVE_NOT_RUN |
| D16 | BALANCE-SCHEMA-MAPPING | AWAITING |

DECISIONS_TOTAL=16; DECISIONS_OWNER_SELECTED=1; DECISIONS_AWAITING=15; COMPANION_OBJECTIVE_SELECTED=1; REGISTERED_APPROVAL_RECEIPTS=0.
Companion objective не является семнадцатым денежным решением.

## Приёмка, зависимости и оставшиеся вопросы

Приёмка этой записи: точные source blobs и версии, один выбранный money ID, 15 ожидающих решений, один companion и ноль формальных receipts.
Источник dependency scope: Reports/HSBI_03E_OWNER_FINAL_DECISION_BALLOT_RU.md и HSBI_03E_CONTRACT_DEPENDENCY_RECONCILIATION_RU.md, manifests четырёх bundles.

Не установлены CostBasisManifest, H_in/H_gate, Initial group membership, CanonicalCandidateTieID, реальные numeric/codec/provider/snapshot profiles, source inventory/journal, reset authority D05 и legacy mapping. ERR038 остаётся OPEN. Исторические Docs29 и comparator сохраняют risk-first до отдельного согласованного изменения.

Связи: [D06 lock](HSBI_03F_R2_D06_A_NORMATIVE_LOCK_RU.md), [NewFar lock](HSBI_03F_R2_NEWFAR_MINIMUM_SAFE_NORMATIVE_LOCK_RU.md), [ERR018](HSBI_03F_R2_ERR018_SOURCE_LEVEL_AUDIT_RU.md), [TL001](HSBI_03F_R2_TL001_REGISTERED_FINDING_RU.md), [readiness](HSBI_03F_R2_DEPENDENCY_AND_READINESS_MATRIX_RU.md).
