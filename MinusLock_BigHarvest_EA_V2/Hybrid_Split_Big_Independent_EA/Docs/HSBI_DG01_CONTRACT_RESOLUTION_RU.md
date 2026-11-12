# DG01 — разрешение контрактов (предложения)

Все16 выборов остаются AWAITING_ADMIN_APPROVAL. Status readiness не равен approval. Исторические canonical IDs сохранены; отображаемые D-09..D-16 не подменяют CR/NUM/SNAP/FUNDING/MQL/BALANCE IDs.

## D-01 (D-01)
- **SourceContract**: Docs08/legacy Remaining и C3 Gross naming conflict.
- **Conflict**: Bare Gross смешивает исходный grant и неиспользованный остаток.
- **PreferredSemantics**: G=C+R+F; RemainingGross=R+F; Available=F только после complete reconciliation/journal.
- **Alternatives**: Сохранить legacy RemainingGross как отдельную read-only view, без переименования в Free.
- **MathematicalJustification**: G50 C10 R15 F25: 50=10+15+25; RemainingGross40=15+25; 10+15+40=65 — двойной учёт.
- **Counterexample**: G50,C10,R15,F25: RemainingGross40,Free25. Подмена Free на40 завышает spending на15.
- **DependentDefects**: ['FSA-002', 'FSA-004', 'FSA-007', 'FSA-008']
- **ProductionModules**: ['Include/Money/HSBI_AllocationLedgerTypes.mqh', 'Include/Money/HSBI_MoneyState.mqh', 'Include/Money/HSBI_ReserveCatchUpEvaluator.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: READY_FOR_ADMIN_DECISION
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## D-02 (D-02)
- **SourceContract**: Docs08 actual deals; C3 disjoint money types.
- **Conflict**: Одинаковые числа и kind-флаги не подтверждают actual или spendable ресурс.
- **PreferredSemantics**: Шесть денежных типов не взаимозаменяемы; каждый переход требует independent source/posted/policy/journal boundary.
- **Alternatives**: Оставить прогнозные view только в planning, с явным запретом funding/consumption.
- **MathematicalJustification**: Projected100 без подтверждённых закрытий не даёт grant; complete-empty history может доказывать0, incomplete history даёт UNAVAILABLE.
- **Counterexample**: Projected100, фактических deals нет → AvailableReserve не100; при неизвестной history UNAVAILABLE, не0.
- **DependentDefects**: ['FSA-001', 'FSA-004', 'FSA-010']
- **ProductionModules**: ['Include/Money/HSBI_EconomicLedgerTypes.mqh', 'Include/Money/HSBI_ReserveCatchUpEvaluator.mqh', 'Include/Planning/HSBI_NewFarSolver.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: READY_FOR_ADMIN_DECISION
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## D-03 (D-03)
- **SourceContract**: Docs31 роли BigCore/BigTrend; production LevelMoney reserveGain включает Small.
- **Conflict**: Small-only profit может ошибочно получить Big Reserve назначение.
- **PreferredSemantics**: Small-only positive → ResidualHeld; transfer только отдельным approved policy/event.
- **Alternatives**: Отдельный подтверждённый transfer contract с debit+credit, новым event и policy; сейчас отсутствует.
- **MathematicalJustification**: Core0 Trend0 Small10 =>BigReserve0, SmallResidualHeld10. Переименование роли не создаёт второй источник.
- **Counterexample**: Core0,Trend0,Small10 → BigReserve0,ResidualHeld10.
- **DependentDefects**: ['FSA-004', 'FSA-019']
- **ProductionModules**: ['Include/Money/HSBI_CostModel.mqh', 'Include/Money/HSBI_ReserveCatchUpEvaluator.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: READY_FOR_ADMIN_DECISION
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## D-04 (D-04)
- **SourceContract**: Far loss absolute/incremental proposals; historical baseline lineage не реализован.
- **Conflict**: Incremental10 ошибочно покрывается Reserve30 при absolute50.
- **PreferredSemantics**: AbsoluteFarLoss рабочий кандидат; Incremental только отдельная диагностика с независимым basis.
- **Alternatives**: Самостоятельная incremental risk model после утверждения baseline/volume/restart lineage.
- **MathematicalJustification**: Absolute50 baseline40 incremental10; Reserve30 покрывает10, но не50. BUY закрывается Bid, SELL Ask.
- **Counterexample**: Absolute50,baseline40,reserve30: incremental10 покрыт, absolute margin=-20.
- **DependentDefects**: ['FSA-015']
- **ProductionModules**: ['Include/Planning/HSBI_FutureSmallProofAggregator.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: READY_FOR_ADMIN_DECISION
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## D-05 (D-05)
- **SourceContract**: Docs08 signed closing net; C2/C3 текущий batch assessment, без sticky журнала.
- **Conflict**: Current final loss, историческое breach и peak loss неэквивалентны.
- **PreferredSemantics**: Владелец выбирает current signed loss, sticky breach либо peak historical loss; выбор здесь не сделан.
- **Alternatives**: ['A: current loss=max(0,-cumulative signed net)', 'B: sticky flag until separately authorized reset', 'C: peak=max historical prefix loss']
- **MathematicalJustification**: Fills -15,+100 Cap12: current15→0; sticky false→true и остаётся true; peak15→15. A cap gate восстанавливается, B/C нет.
- **Counterexample**: Fills-15,+100,cap12: A loss15→0; B breach true→true; C peak15→15.
- **DependentDefects**: ['FSA-006', 'FSA-015']
- **ProductionModules**: ['Include/Execution/HSBI_TransactionTypes.mqh', 'Include/Planning/HSBI_FutureSmallProofAggregator.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: Confirmed batch membership, ordered partial fills, component costs, restart preservation of selected metric and reset authority; no policy selected here.
- **MigrationRisk**: Final cumulative Net85 cannot reconstruct earlier breach15. Missing ordered history/reset journal => UNAVAILABLE for sticky/peak migration; do not infer no breach.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: CONTRACT_CONFLICT
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## D-06 (D-06)
- **SourceContract**: Signed Profit/Swap/Commission/Fee и independent cost coverage; buffer headroom не actual debit.
- **Conflict**: Неизвестное пересечение basis/window может дать двойное вычитание или скрытый ноль.
- **PreferredSemantics**: Каждый обязательный cost покрывается ровно один раз по independent basis/window; unknown overlap не безопасный0.
- **Alternatives**: Сводный buffer только с доказанной coverage map; размер и overlap подтверждаются отдельно.
- **MathematicalJustification**: Commission -2 уже в net50 нельзя ещё раз вычитать до48. Unknown slippage не0; RequiredBalance10.5 не означает debit10.5.
- **Counterexample**: Ask101→Bid110 уже даёт9; вычет того же spread1 даёт8 только при доказанном совпадении cost basis.
- **DependentDefects**: ['FSA-019']
- **ProductionModules**: ['Include/Money/HSBI_CostModel.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: INSUFFICIENT_EVIDENCE
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## D-07 (D-07)
- **SourceContract**: Docs08 exact NO_OP/changed CONFLICT; C3 in-memory != durable/concurrent.
- **Conflict**: Replay ordering, durable commit и отсутствие истории смешивались.
- **PreferredSemantics**: Global source funding journal + immutable replay + atomic durable commit/CAS; локальная idempotency не exactly-once backend.
- **Alternatives**: Authenticated receipt-first policy с отдельно утверждённым поведением unavailable source/history.
- **MathematicalJustification**: Grant50 debit10 event1 =>40; exact event1 остаётся40; changed event1 amount11 =>CONFLICT. Restart без journal не доказывает отсутствие event.
- **Counterexample**: Две allocations используют source50 по30: local budgets проходят, общий debit60>50.
- **DependentDefects**: ['FSA-003', 'FSA-004', 'FSA-013', 'FSA-027']
- **ProductionModules**: ['Include/Money/HSBI_ReserveCatchUpEvaluator.mqh', 'Include/Persistence/HSBI_ExecutionJournal.mqh', 'Include/Persistence/HSBI_PersistenceInterface.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: READY_FOR_ADMIN_DECISION
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## D-08 (D-08)
- **SourceContract**: Docs08/31/32 independent source; production source key без Account/Broker/Server.
- **Conflict**: Expected из proof и key по symbol/magic/cycle/deal допускают самоподтверждение и namespace collisions.
- **PreferredSemantics**: SourceKey=(Broker,Server,Account,Deal), full immutable body; NEW identity не funding; unknown facts UNAVAILABLE.
- **Alternatives**: Independent signed/verified adapter receipt того же payload digest; не self-copy.
- **MathematicalJustification**: Два accounts с Deal11 различны. Profit60/Commission-10 и70/-20 при net50 — same source, changed payload =>CONFLICT.
- **Counterexample**: Profit50/Commission0 и Profit60/Commission-10 при одном source → CONFLICT, несмотря на Net50.
- **DependentDefects**: ['FSA-001', 'FSA-002', 'FSA-003', 'FSA-009', 'FSA-010']
- **ProductionModules**: ['Include/Core/HSBI_Context.mqh', 'Include/Money/HSBI_AllocationLedgerTypes.mqh', 'Include/Money/HSBI_EconomicLedgerTypes.mqh', 'Include/Money/HSBI_ReserveCatchUpEvaluator.mqh', 'Include/Planning/HSBI_NewFarSolver.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: READY_FOR_ADMIN_DECISION
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## CR-09 (D-09)
- **SourceContract**: Production worstTransitionLossLevel; C3 A all-level/B single-level.
- **Conflict**: MaxTransition level не гарантирует минимальный CatchUpMargin; прогноз не actual resource.
- **PreferredSemantics**: Явно выбрать ALL_LEVEL либо SINGLE_LEVEL scope; all-level требует minMargin>0 по каждому required level.
- **Alternatives**: SINGLE_LEVEL assessment отдельно, никогда не повышается до all-level или dispatch authorization.
- **MathematicalJustification**: L1 margin79 transition50, L2 margin-6 transition1: B positive L1, all-level обязан отклонить L2.
- **Counterexample**: T1=10,margin1=9;T2=5,margin2=-11: worst-transition не worst-catchup.
- **DependentDefects**: ['FSA-015']
- **ProductionModules**: ['Include/Planning/HSBI_FutureSmallProofAggregator.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: BLOCKED_BY_DEPENDENCY
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## NUM-EXACT-1 (D-10)
- **SourceContract**: R0D Fraction reference; raw double внешняя граница и неподтверждённый MQL domain.
- **Conflict**: Округление projected потерь и потеря малых дебетов могут менять знак proof.
- **PreferredSemantics**: Exact settled money representation; projected risk не округляется до безопасного0.
- **Alternatives**: Fixed-point/checked rational production domain с доказанными intermediate bounds.
- **MathematicalJustification**: 1e28-.010-(1e28-.005)=-.005. INT64_MAX minor units после двух debit1 равен INT64_MAX-2.
- **Counterexample**: Reserve1e28,два расхода.01 требуют точный decrement.02; arbitrary Decimal context не доказательство.
- **DependentDefects**: ['FSA-005', 'FSA-006', 'FSA-007', 'FSA-008']
- **ProductionModules**: ['Include/Execution/HSBI_TransactionTypes.mqh', 'Include/Money/HSBI_AllocationLedgerTypes.mqh', 'Include/Money/HSBI_MoneyState.mqh', 'Include/Risk/HSBI_RiskGateResult.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: READY_FOR_ADMIN_DECISION
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## NUM-DOMAIN-1 (D-11)
- **SourceContract**: R0D lattice10^-64 abs<10^65; fixture money digits0..8.
- **Conflict**: Reference-domain существенно шире int64 minor units и broker precision facts.
- **PreferredSemantics**: Явный supported currency/precision/range и отказ за domain; unlimited Fraction не MQL domain.
- **Alternatives**: Более широкий multiword/fixed-point domain после доказательства всех intermediates.
- **MathematicalJustification**: 1e28 dollars =>1e30 cents вне int64; MAX+MAX-MAX-MAX final0 всё равно требует wide accumulator либо отдельного domain refusal.
- **Counterexample**: INT64_MAX+1 выходит за signed64; float IDs после2^53 теряют различие.
- **DependentDefects**: ['FSA-005', 'FSA-006', 'FSA-022']
- **ProductionModules**: ['Include/Core/HSBI_StateMachine.mqh', 'Include/Execution/HSBI_TransactionTypes.mqh', 'Include/Risk/HSBI_RiskGateResult.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: INSUFFICIENT_EVIDENCE
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## NUM-CODEC (D-12)
- **SourceContract**: R0D fixture typed codec, R1 raw64/NFC proposal, C3 native codec не проверен.
- **Conflict**: Wire identity и financial rounding смешивались; MQL compatibility не доказана.
- **PreferredSemantics**: F64Z рекомендуется как candidate raw captured codec; T17Z — альтернатива; native compatibility не подтверждена.
- **Alternatives**: HSBI-T17Z-1: typed length-prefixed UTF8 + canonical scientific17 raw doubles, explicit zero equivalence.; HSBI-F64Z-1: typed length-prefixed binary fields + finite64 raw bits, reconstructed arithmetic.
- **MathematicalJustification**: Raw .1 имеет bits3fb999999999999a и text1.0000000000000001e-001; str1/int1/bool1 не должны совпасть.
- **Counterexample**: +0/-0 должны иметь явную Z policy; ulong9007199254740993 не проводить черезdouble.
- **DependentDefects**: ['FSA-001', 'FSA-010', 'FSA-026']
- **ProductionModules**: ['Include/Money/HSBI_EconomicLedgerTypes.mqh', 'Include/Planning/HSBI_NewFarSolver.mqh', 'Tests/Reference/hsbi_02b_r0h_native_harness.mq5']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: INSUFFICIENT_EVIDENCE
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## SNAP-FIXTURE-1 (D-13)
- **SourceContract**: R0D content receipt; C2 ID/fresh только provider fixture assertion.
- **Conflict**: ID999+fresh не доказывают content/freshness полного snapshot.
- **PreferredSemantics**: Versioned strict schema+typed content+независимый receipt; fixture receipt не broker authenticity.
- **Alternatives**: ID-only provider attestation исключительно с ограниченным scope, не full proof.
- **MathematicalJustification**: Один ID3 с изменённым fingerprint должен быть CONFLICT; обновлённый receipt из самого altered object не independent proof.
- **Counterexample**: string1 и numeric1 не эквивалентны без явного schema codec; copied receipt не независим.
- **DependentDefects**: ['FSA-010', 'FSA-021']
- **ProductionModules**: ['Include/Planning/HSBI_ControlPrices.mqh', 'Include/Planning/HSBI_NewFarSolver.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: READY_FOR_ADMIN_DECISION
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## FUNDING-GLOBAL-ATTRIBUTION (D-14)
- **SourceContract**: C3 source-local cap доказан, глобальные account debit/credit и concurrency UNPROVEN.
- **Conflict**: Сумма grants одного источника не равна доказанному свободному капиталу всего счёта.
- **PreferredSemantics**: Единый source-level inventory across allocations, roles и restarts; transfer/reversal отдельными событиями.
- **Alternatives**: Явно ограничить все текущие утверждения source-local fixture scope, без production available.
- **MathematicalJustification**: Source50 allocations40+20 запрещены. Source50 плюс unaccounted account debit30 не доказывает account free50.
- **Counterexample**: Перестановка Magic/Cycle не создаёт новый broker deal и новую прибыль.
- **DependentDefects**: ['FSA-001', 'FSA-003', 'FSA-004', 'FSA-013']
- **ProductionModules**: ['Include/Money/HSBI_EconomicLedgerTypes.mqh', 'Include/Money/HSBI_ReserveCatchUpEvaluator.mqh', 'Include/Persistence/HSBI_PersistenceInterface.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: BLOCKED_BY_DEPENDENCY
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## MQL-DOMAIN (D-15)
- **SourceContract**: C3 Python signed64 simulation и g++ subset; MetaEditor NOT_RUN.
- **Conflict**: Математическая проверка не доказывает нативные ulong/long/double/UTF8 conversions.
- **PreferredSemantics**: Native long/ulong/double/UTF8, overflow, finite-only и codec goldens обязательны до acceptance.
- **Alternatives**: Wider fixed-point/multiword adapter, исключительно после native tests.
- **MathematicalJustification**: INT64_MIN*(-1) и MAX+1 недопустимы. TimestampMsc signed long не должен наследовать весь ulong range.
- **Counterexample**: NaN делает оба ordered comparisons ложными; revision ULONG_MAX+1 требует stop.
- **DependentDefects**: ['FSA-005', 'FSA-006', 'FSA-008', 'FSA-022', 'FSA-026']
- **ProductionModules**: ['Include/Core/HSBI_StateMachine.mqh', 'Include/Execution/HSBI_TransactionTypes.mqh', 'Include/Money/HSBI_MoneyState.mqh', 'Include/Risk/HSBI_RiskGateResult.mqh', 'Tests/Reference/hsbi_02b_r0h_native_harness.mq5']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: INSUFFICIENT_EVIDENCE
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL

## BALANCE-SCHEMA-MAPPING (D-16)
- **SourceContract**: Legacy RemainingGross и новый Free profile.
- **Conflict**: Silent rename возвращает reserved/consumed ресурс в available.
- **PreferredSemantics**: Legacy Remaining мигрирует только при известном gross/free/consumed/reserved/owner/currency mapping.
- **Alternatives**: Сохранить legacy read-only и выполнять append-only migration только по independent receipts.
- **MathematicalJustification**: G50 C10 Remaining40 Reserved15 =>Free25. Unknown currency/precision/owner =>UNAVAILABLE, неFree40.
- **Counterexample**: Remaining40,Reserved15 означает Free25, а не40; при неизвестном owner migration UNAVAILABLE.
- **DependentDefects**: ['FSA-007', 'FSA-008', 'FSA-013']
- **ProductionModules**: ['Include/Money/HSBI_AllocationLedgerTypes.mqh', 'Include/Money/HSBI_MoneyState.mqh', 'Include/Persistence/HSBI_PersistenceInterface.mqh']
- **RequiredTests**: ['Positive/negative literal vectors', 'Immutable source/identity changes', 'Zero deltas on reject/no-op', 'Per-guard causal mutation where implemented']
- **RequiredNativeEvidence**: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
- **MigrationRisk**: Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.
- **StopConditions**: ['Unknown namespace/units/origin/legacy', 'Unapproved dependent policy', 'Native or independent provider evidence missing at implementation acceptance']
- **ReadinessStatus**: BLOCKED_BY_DEPENDENCY
- **ApprovalStatus**: AWAITING_ADMIN_APPROVAL
