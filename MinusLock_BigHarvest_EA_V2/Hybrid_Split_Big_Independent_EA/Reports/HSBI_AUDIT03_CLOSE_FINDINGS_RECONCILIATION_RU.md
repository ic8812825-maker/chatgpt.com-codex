# AUDIT03 CLOSE — сверка ERR / IMP

База `398da88424f3fb7b30e5315fbc3bf89219dd9ad2`; ветка `work`. Все новые изменения контрактов — **PROPOSED**. Owner approval отсутствует.

Исторический реестр содержит 50 IDs: P0=14, P1=31, P2=5. Это унаследованный register, а не 50 заново подтверждённых production defects. Новые ERR IDs не присвоены. Ни один OPEN не закрыт. ERR-050 остаётся AMBIGUOUS_SPECIFICATION. Снятая гипотеза о transitionShare не возвращена в дефекты.

| ERR | Priority | Source | Текущая проверка | IMP |
|---|---|---|---|---|
| HSBI-A03-ERR-001 | P0 | `Include/Money/HSBI_EconomicLedgerTypes.mqh:9` | C++ P0-01: equal-net altered components → duplicate1 вместо conflict2 | HSBI-A03-IMP-001 |
| HSBI-A03-ERR-002 | P0 | `Include/Money/HSBI_EconomicLedgerTypes.mqh:6-7` | Economic record:6–7 AccountLogin/Broker/Server отсутствуют; namespace не различает accounts | HSBI-A03-IMP-001 |
| HSBI-A03-ERR-003 | P1 | `Include/Money/HSBI_EconomicLedgerTypes.mqh:11` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-002 |
| HSBI-A03-ERR-004 | P0 | `Include/Money/HSBI_AllocationLedgerTypes.mqh:8` | C++ P0-02: разные векторы с равной суммой → duplicate1 | HSBI-A03-IMP-003 |
| HSBI-A03-ERR-005 | P0 | `Include/Money/HSBI_AllocationLedgerTypes.mqh:7` | C++ NEGATIVE-BUCKET принят; −50+100=50 | HSBI-A03-IMP-003 |
| HSBI-A03-ERR-006 | P1 | `Docs/04_MATHEMATICAL_MODEL_RU.md:30` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-003 |
| HSBI-A03-ERR-007 | P0 | `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:44-47` | Reserve evaluator:44–47 проверяет shape/sourceDealId, не exact source/allocation key binding | HSBI-A03-IMP-004 |
| HSBI-A03-ERR-008 | P0 | `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:63-70` | Reserve evaluator:67–70 unallocated ветвь не отвергает alreadyConsumed>0; global availability не запрашивается | HSBI-A03-IMP-004 |
| HSBI-A03-ERR-009 | P0 | `Include/Risk/HSBI_RiskGateResult.mqh:6` | C++ P0-04: NaN risk принят; NAN-LIMIT принят | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-010 | P0 | `Include/Execution/HSBI_TransactionTypes.mqh:15` | C++ P0-07-NAN-FILL и P0-10-UNKNOWN-RETRY приняты; обязательность caller не доказана | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-011 | P0 | `Include/Money/HSBI_MoneyState.mqh:5` | C++ P0-05: +Infinity reserve принят | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-012 | P0 | `Include/Core/HSBI_Context.mqh:19-24,48-53` | Context:19–24,48–53 охватывает четыре слота, initialBuy/initialSell/newFarCandidate вне Far count; полный global registry не проверен | HSBI-A03-IMP-006 |
| HSBI-A03-ERR-013 | P0 | `Include/Planning/HSBI_NewFarSolver.mqh:119-124` | NewFar:119–124 перезаписывает proof identity из caller DTO; provider authenticity не следует из equality | HSBI-A03-IMP-001 |
| HSBI-A03-ERR-014 | P1 | `Include/Planning/HSBI_GeometrySolver.mqh:28-35` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-007 |
| HSBI-A03-ERR-015 | P1 | `Docs/04_MATHEMATICAL_MODEL_RU.md:9` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-007 |
| HSBI-A03-ERR-016 | P1 | `Hybrid_Split_Big_Independent_EA.mq5:19-44` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-008 |
| HSBI-A03-ERR-017 | P1 | `Include/Persistence/HSBI_PersistenceInterface.mqh:5-7` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-009 |
| HSBI-A03-ERR-018 | P1 | `Include/Planning/HSBI_FutureSmallProofAggregator.mqh:44,50-52` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-010 |
| HSBI-A03-ERR-019 | P1 | `Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:22-23` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-011 |
| HSBI-A03-ERR-020 | P1 | `Include/Planning/HSBI_FutureSmallSolver.mqh:89-90,143` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-012 |
| HSBI-A03-ERR-021 | P1 | `Include/Planning/HSBI_FutureSmallSolver.mqh:12-16,142-147` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-013 |
| HSBI-A03-ERR-022 | P1 | `Include/Money/HSBI_CostModel.mqh:13-18` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-014 |
| HSBI-A03-ERR-023 | P1 | `Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:6-12` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-015 |
| HSBI-A03-ERR-024 | P2 | `Include/Planning/HSBI_ControlPrices.mqh:11` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-016 |
| HSBI-A03-ERR-025 | P1 | `Include/Core/HSBI_StateMachine.mqh:6` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-026 | P1 | `Include/Planning/HSBI_NewFarSolver.mqh:35-45,106` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-027 | P2 | `Tests/Static/:LINE_NOT_VERIFIED` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-017 |
| HSBI-A03-ERR-028 | P2 | `Docs/03_FULL_SYSTEM_MANUAL_RU.md:50-51` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-017 |
| HSBI-A03-ERR-029 | P2 | `Docs/04_MATHEMATICAL_MODEL_RU.md:42-43` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-018 |
| HSBI-A03-ERR-030 | P1 | `Include/Persistence/HSBI_ExecutionJournal.mqh:21-29` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-009 |
| HSBI-A03-ERR-031 | P1 | `Include/Planning/HSBI_FutureSmallSolver.mqh:144-149` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-013 |
| HSBI-A03-ERR-032 | P1 | `Docs/04_MATHEMATICAL_MODEL_RU.md:33-36` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-013 |
| HSBI-A03-ERR-033 | P0 | `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6-24` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-004 |
| HSBI-A03-ERR-034 | P1 | `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-015 |
| HSBI-A03-ERR-035 | P1 | `Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:9,20` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-019 |
| HSBI-A03-ERR-036 | P1 | `Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:20` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-020 |
| HSBI-A03-ERR-037 | P1 | `Docs/05_GEOMETRY_MODEL_RU.md:22` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-021 |
| HSBI-A03-ERR-038 | P0 | `Docs/04_MATHEMATICAL_MODEL_RU.md:33-36` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-021 |
| HSBI-A03-ERR-039 | P2 | `Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:9` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-007 |
| HSBI-A03-ERR-040 | P1 | `Include/Planning/HSBI_BrokerGrid.mqh:26-27` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-002 |
| HSBI-A03-ERR-041 | P1 | `Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:12-14` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-022 |
| HSBI-A03-ERR-042 | P1 | `Docs/03_FULL_SYSTEM_MANUAL_RU.md:12-18` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-021 |
| HSBI-A03-ERR-043 | P1 | `Include/Money/HSBI_CatchUpModel.mqh:10-15` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-010 |
| HSBI-A03-ERR-044 | P1 | `Include/Money/HSBI_MoneyTypes.mqh:7-9` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-020 |
| HSBI-A03-ERR-045 | P1 | `Include/Planning/HSBI_NewFarSolver.mqh:108-113,149-151` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-011 |
| HSBI-A03-ERR-046 | P1 | `Docs/03_FULL_SYSTEM_MANUAL_RU.md:12` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-007 |
| HSBI-A03-ERR-047 | P1 | `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | HSBI-A03-IMP-004 |
| HSBI-A03-ERR-048 | P0 | `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:24–76` | Reserve:61–74 нет equalities eligible=proof.net и farLoss=max(0,−farProof.net); NewFar:121–122 их вычисляет, direct-public mismatch не solver exploit | IMP-004/010 |
| HSBI-A03-ERR-049 | P1 | `Include/Execution/HSBI_ExecutionIntent.mqh:28–40` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | IMP-005/007/008 |
| HSBI-A03-ERR-050 | P1 | `Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:27–40` | NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена | IMP-009 |

ERR-033 — global funding contract gap и ERR-038 — отсутствие unconditional loss bound остаются P0 blockers, но не объявляются здесь исправимыми одной equality-проверкой.

C++ 16 FAIL включают два явно PROPOSED ожидания (committed equality и exhausted-source semantics): существующий DTO не определяет полный lifecycle, поэтому эти FAIL не превращены автоматически в новые безусловные source defects. Остальные локальные counterexamples также не доказывают работу торгового exploit в disabled main. Все исторические 22 IMP IDs сохраняются без переназначения.
