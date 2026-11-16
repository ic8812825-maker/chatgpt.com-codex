# HSBI-03G-R1 — область, источники и границы доказательств

DocumentVersion=HSBI-03G-R1-V1
SourceCommitSHA=e68e73e1b252d20e15588645004f9066c6ae88f0
Scope=Remote scope / audit-spec package
EvidenceClass=STATIC_REVIEWED
NormativeStatus=PROPOSED_AWAITING_OWNER_APPROVAL
Dependencies=HSBI-03F-R2; pinned source tree

Репозиторий: `ic8812825-maker/chatgpt.com-codex`, ветка `work`. Все пути ниже находятся внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`. Новый текст является проектом контракта, а не утверждением реализации. Выбор D-06 A и companion NewFar A сохраняется; полный CR-09 не утверждён. Формальных approval receipts нет.

PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.

UNAVAILABLE означает отсутствие обязательного доказательства; CONFLICT — противоречие данных; REJECT — доказанное нарушение. Каждый результат запрещает новый финансовый эффект, delta=0. NO_OP допустим только после проверки подлинного полного прежнего event body и receipt. Числа математических примеров не являются брокерскими константами.

## Проверенная база и механизм работы

На начало текущего выполнения ref `refs/heads/work` указывает на `e68e73e1b252d20e15588645004f9066c6ae88f0`. Контрольная база совпадает. Корневой tree SHA: `1be2e2949ee06d5c7ee34e276df1d31b2401e998`. Единственный родитель базы: `ae367ff2925da4d845a413326c840fe468ff451b`. В Reports было 308 записей; все десять целевых имён отсутствовали. Время текущей проверки: {"current_time":"2026-11-16 18:15:29 UTC"}.

Для проекта применяются только GitHub MCP fetch_file/fetch и Git Data create_blob/create_tree/create_commit/update_ref. Нет локального checkout, clone, поиска файлов или локального Git. Ruleset ChatGPT1 и настройки не читаются и не изменяются. PR, CodeQL и другие ветки не используются. Создание объектов Git само по себе не публикует их; публикация требует отдельного non-force update_ref с expected_sha, равным базе.

### Честная граница операций с вложением

До прямого распоряжения на выполнение пользователь отдельно велел прочитать приложенный текстовый файл. Для этого в предыдущем проходе были выполнены одна загрузка вложения и одна команда чтения только этого вложения. Это локальные операции, поэтому значение LOCAL_FILE_OPERATIONS=0 для всей беседы было бы ложным. В текущем выполнении после распоряжения локальные файловые операции отсутствуют; локальные операции с репозиторием отсутствовали во всех проходах. Вложение не включается в GitHub diff и не объявляется частью project tree.

```text
CURRENT_EXECUTION_MODE=GITHUB_MCP_REMOTE_ONLY
CURRENT_EXECUTION_LOCAL_FILE_OPERATIONS=0
LOCAL_REPOSITORY_FILE_OPERATIONS=0
EARLIER_ATTACHMENT_DOWNLOAD_CALLS=1
EARLIER_ATTACHMENT_READ_COMMANDS=1
CONVERSATION_LOCAL_FILE_OPERATIONS=NONZERO_ATTACHMENT_ONLY
LOCAL_CHECKOUT_CREATED=NO
```

## Источники, прочитанные непосредственно из закреплённого commit

Таблица является inventory фактических чтений, а не заявлением о полном аудите 1 529 файлов. Строки в ссылках других документов считаются от начала соответствующего blob. Исторические тексты могут иметь собственный SourceCommitSHA; ниже зафиксирован именно blob, доступный в базе этого этапа.

| Путь относительно проекта | SourceBlobSHA | Число строк при split по LF |
|---|---|---:|
| Reports/HSBI_03F_R2_D06_A_NORMATIVE_LOCK_RU.md | ffd81b9575790a166c50979fd7b1a4c85715a011 | 76 |
| Reports/HSBI_03F_R2_DEPENDENCY_AND_READINESS_MATRIX_RU.md | f9ddf0c5b936ccccfc3ee5495e1fd314d2655049 | 89 |
| Reports/HSBI_03F_R2_ERR018_SOURCE_LEVEL_AUDIT_RU.md | fa093a00c2887f92da6a8436b0e1c6b1ed32905d | 160 |
| Reports/HSBI_03F_R2_FINAL_VERDICT_RU.md | c4f09ad0a28ee8aa041937d112cc8384d799ee24 | 246 |
| Reports/HSBI_03F_R2_NEWFAR_MINIMUM_SAFE_NORMATIVE_LOCK_RU.md | 91aeb48e911c2891c8267b9fedd831f991ceaf56 | 77 |
| Reports/HSBI_03F_R2_OWNER_POLICY_SELECTION_RU.md | 3674348a620f40cb5532a5a965cfd76c2d119431 | 95 |
| Reports/HSBI_03F_R2_TEST_VECTOR_SPECIFICATION_RU.md | 0b74240e22fe0248977bb7448baac5039383452e | 157 |
| Reports/HSBI_03F_R2_TL001_REGISTERED_FINDING_RU.md | 8de58af1d808cc8d04816e46e77d59f45a7a49a0 | 105 |
| Reports/HSBI_03F_R2_TRANSITION_CATCHUP_CONTRACT_V1_RU.md | 47e6dc4fc3fbb6602b33242519cea3e121068d31 | 122 |
| Reports/HSBI_03F_R2_TRANSITION_CATCHUP_MATH_PROOFS_RU.md | 427f90083629a8e5207952e509a0e4fcefedc377 | 153 |
| Reports/HSBI_03E_OWNER_FINAL_DECISION_BALLOT_RU.md | 62472656ad4af5acba65144e30f36cbca05a5abd | 224 |
| Reports/HSBI_03E_CONTRACT_DEPENDENCY_RECONCILIATION_RU.md | ceb6440e45dee9a67dab478dfbc48d4325e8db3f | 106 |
| Reports/HSBI_03E_NUMERIC_CONTRACT_MANIFEST_V1_RU.md | 6b9fcc61124e5d9d88f96cee420c3596fada0ff2 | 130 |
| Reports/HSBI_R11_P0_DEPENDENCY_PLAN_RU.md | 8ac398a8dae93dbcbc28e2fbeddc70a7501b2f76 | 224 |
| Docs/04_MATHEMATICAL_MODEL_RU.md | f290e753e62b004dbdc0c4f8ef24fda46b9b6d7c | 44 |
| Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md | 9bab98f4df7e162dd26fcf07f6e267bc079bd5ba | 26 |
| Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md | 0d9e9321bea27b83397e9eb3348434fbbed61970 | 28 |
| Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md | 1dc796cb19748ad7e70ac9bcac611e8e18dbdcdd | 19 |
| Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | 4ecebeb09c9dcfbbf9d3927b980e44fd81289cf6 | 24 |
| Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md | f779a1a87ab2d0163c17d6c855c206047d970cec | 29 |
| Docs/24_BROKER_MONEY_MODEL_RU.md | fd4ca5dfb7835d22bde5d8971b7849226cc3b237 | 22 |
| Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md | 33796d41e5efa824fff32a38f4d09fefe90b5e0b | 38 |
| Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | 0c4b5f9ea4aab1618a280a5c4510f89b76fb9646 | 16 |
| Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md | f93a0cb48b7e1683883823ace9df9d6ede9697f3 | 25 |
| Docs/16_PERSISTENCE_AND_RESTART_RU.md | 5b1bd202c865828407eecdd8cffc04c4cae949f7 | 22 |
| Docs/25_BROKER_GRID_AND_ROUNDING_RU.md | 7e1357c5540bc92d7aaee142404aadc144f1a632 | 18 |
| Docs/31_MONEY_PROOF_IDENTITY_RU.md | 95dfd5d807899d180632504dc01aa843b76ab1f5 | 8 |
| Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | 77c9a05a0df23cb238dda71798bc2c158ffdbdbf | 8 |
| Include/Planning/HSBI_FutureSmallSolver.mqh | be55c93f051f57ddffd189b9d2e8eee4c3ddaf9d | 152 |
| Include/Planning/HSBI_FutureSmallTypes.mqh | ee962ed40a99b0d0a1fdd22f2ee071cc3fb6cbcc | 83 |
| Include/Planning/HSBI_FutureSmallProofAggregator.mqh | 4678ae152960e98b9f398b4497786061d7e8a524 | 61 |
| Include/Planning/HSBI_NewFarSolver.mqh | 3d19eccd6cd318b9b4591e2bc0ccaa95f661930d | 155 |
| Include/Planning/HSBI_NewFarCandidate.mqh | 758f1c89cf75701d3616dabec2fcb06413ee2d4a | 43 |
| Include/Planning/HSBI_GeometrySolver.mqh | 707cc1678ca4d98888b3acc2599838094fe13a78 | 39 |
| Include/Planning/HSBI_BrokerGrid.mqh | 82a06297b2c98113f18d92ebf3cd7bdc615749a0 | 39 |
| Include/Planning/HSBI_ControlPrices.mqh | 2540db9d53533319319b698d999187f785f0815c | 26 |
| Include/Money/HSBI_BasketMoneyEvaluator.mqh | 4bea204e91a4719b4b24086304cb51051909a7de | 30 |
| Include/Money/HSBI_ReserveCatchUpEvaluator.mqh | 87a8b7e97727ce6e47c2a2f0abc3e237f6203204 | 84 |
| Include/Money/HSBI_ReserveAllocationTypes.mqh | f1464320f1f853f12f8e3f3ddc3708bad2a0cd4d | 36 |
| Include/Money/HSBI_AllocationPolicyTypes.mqh | 720942a0049cacc76691e600efdef7018e91d482 | 33 |
| Include/Money/HSBI_CostModel.mqh | 293a22c0ff14bc6d635e0cc50c79c8e3d4a7d5cd | 21 |
| Include/Money/HSBI_LevelMoneyEvaluator.mqh | 3c89ae2355945ec7c75fac2694967ae5f1785967 | 17 |
| Include/Money/HSBI_BrokerMoneyModel.mqh | 4dbee633bceb914365e536acc00208955c01588f | 23 |
| Include/Money/HSBI_BrokerMoneyTypes.mqh | ebcd16b2a9ea770d9c8525f5ed3285f3a5129870 | 21 |
| Include/Money/HSBI_BrokerMarginModel.mqh | a8c0f43465785d7d6c82517124c3e3b028862337 | 19 |
| Include/Money/HSBI_LevelMarginEvaluator.mqh | 2227a0ef16caa44f4e4ffefcf860499773dbf471 | 14 |
| Include/Money/HSBI_MoneyProofIdentity.mqh | cb00b547b9f4d3d9eac7a473415b25627c3ac91d | 31 |
| Include/Money/HSBI_CandidateMoneyEvaluator.mqh | 5402799247ff948b2616306060764004b468abf2 | 29 |
| Include/Money/HSBI_EconomicLedgerTypes.mqh | e589337d228323dba278b242d01e61fc0ee733fe | 14 |
| Include/Money/HSBI_AllocationLedgerTypes.mqh | 87f86ec7498bd115f5a21da34d596c0ce0c2170a | 11 |
| Include/Risk/HSBI_NewFarGateTypes.mqh | 7d50669bda8ff2d000566ad7a38281140a77ae83 | 19 |
| Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh | 870d84b3f49a85e7db5c6d5ead777efea1c9faa3 | 53 |
| Include/Runtime/HSBI_RuntimeDecisionTypes.mqh | 0cc2619ed6ce7a93ea28c3c655a8d147e18a9231 | 19 |
| Include/Runtime/HSBI_RuntimeDecisionValidator.mqh | aecbf35e7ced9fd756d80803c63626b9b52c0846 | 31 |
| Include/Core/HSBI_Identifiers.mqh | d05a05147f7641040dbf7261ebdd04832d643997 | 25 |
| Include/Core/HSBI_RuntimePolicy.mqh | 657fe730c1a3df306848d1de00af87aa589be449 | 31 |
| Include/Persistence/HSBI_ExecutionJournal.mqh | e65d6d9b0f04a3e236952ec577ea144bf57ee2b2 | 46 |
| Include/Persistence/HSBI_PersistenceInterface.mqh | 36b7181f50fe4554d24f9ea6813906f9f4240d49 | 8 |
| Tests/Close/production_subset_results.json | 192fe577764407499c6334d8e07c55ad78afeed7 | 161 |
| Tests/MQL5/HSBI_Skeleton_Tests.mq5 | 75052d49e55a5f43534143052b28c0b94ba2b516 | 552 |
| Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md | a36d0fb1c37da7dcab02e54e9738e01befc16084 | 743 |
| Reports/HSBI_03E_SNAPSHOT_AUTHORITY_CONTRACT_RU.md | 31898e975924c9e54b94be06352e9f08fbfdcc3e | 103 |
| Reports/HSBI_03E_D06_POLICY_RESOLUTION_RU.md | 39342ea57a83a8dcd2f8e22ff8b87747c371d0ca | 105 |
| Reports/HSBI_03E_NEWFAR_OBJECTIVE_RESOLUTION_RU.md | a29b28fe806b7bd53cc49a34803b25b4b9b55543 | 124 |

## Что подтверждено и что не подтверждено

- [Include/Planning/HSBI_NewFarSolver.mqh:114–151](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarSolver.mqh#L114-L151) — HSBI_SolveNewFar. SourceBlobSHA=`3d19eccd6cd318b9b4591e2bc0ccaa95f661930d`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_FutureSmallProofAggregator.mqh:23–58](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_FutureSmallProofAggregator.mqh#L23-L58) — HSBI_AggregateFutureSmallProof. SourceBlobSHA=`4678ae152960e98b9f398b4497786061d7e8a524`; EvidenceClass=STATIC_REVIEWED.
- [Reports/HSBI_03F_R2_OWNER_POLICY_SELECTION_RU.md:1–95](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03F_R2_OWNER_POLICY_SELECTION_RU.md#L1-L95). SourceBlobSHA=`3674348a620f40cb5532a5a965cfd76c2d119431`; EvidenceClass=STATIC_REVIEWED.

Статически подтверждены single-control CatchUp и несовпадение семантики возвращаемого transitionLoss с проверенным basket maximum. Новый этап не доказывает нативный unsafe SELECTED, фактическое расходование reserve или брокерскую достижимость математической fixture. TL001 остаётся CONFIRMED_STATIC / P1_PROPOSED, official ERR-ID не присваивается. ERR018 остаётся OPEN_CONTRACT_GAP. Чтение не закрывает P0.

Старый C++ shim artifact сохраняет 7 PASS / 16 FAIL: это HISTORICAL_TEST_RESULT, не результат нового запуска. Два contract-dependent сценария нельзя нормализовать переписыванием expected. Все новые vectors — TEST_SPECIFIED_NOT_RUN. Нативные, compile, runtime, crash, concurrency и mutation проверки не выполнялись.

## План целостности публикации

Разрешены ровно десять новых путей, перечисленных в задании. Перед публикацией повторно читаются HEAD и Reports. Изменившийся HEAD означает STOP, а не автоматический перенос материалов на неизвестную базу. Tree строится на исходном root tree с добавлением только десяти blobs. Commit имеет ровно одного родителя — исходный HEAD. До update_ref проверяется diff: ровно десять added paths, без modified/deleted. После update_ref повторно читаются все файлы из work, сравниваются содержимое и blob SHA, проверяются parent, diff и remote HEAD.

Отчёт намеренно не содержит собственного будущего commit SHA: такое self-reference нельзя вычислить до создания commit. Итог публикации и фактические hashes приводятся в ответе исполнителя после проверки, а не заранее как SUCCESS.

OpenQuestions: owner choices CR09-SUB-01…11, numeric/native/provider evidence и будущие amendments остаются открытыми.
AcceptanceCriteria: pinned inventory воспроизводим; diff содержит только разрешённые добавления; итоговый ответ подтверждает remote SHA и десять blob SHA; никаких вымышленных PASS.

Связи: [итоговые gates](HSBI_03G_R1_FINAL_READINESS_VERDICT_RU.md), [owner ballot](HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md).
