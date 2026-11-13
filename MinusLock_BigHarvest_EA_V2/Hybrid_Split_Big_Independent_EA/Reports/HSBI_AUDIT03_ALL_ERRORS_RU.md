# AUDIT03 — единый реестр ошибок и незакрытых обязательств

**Текущий срез COVERAGE-COMPLETION:** 50 записей, P0=14/P1=31/P2=5; ERR-048/049 — новые локальные SOURCE_DEFECT, ERR-050 — AMBIGUOUS_SPECIFICATION. Первоначальные47 карточек и их ID сохранены; старые сводки ниже являются историческими. Окончательная переоценка и снятая transitionShare-гипотеза — в конце файла.

База: `6231bfbe94d39fbbb469b90a93e01426a83756bb`. Метод: ручная алгебра и статическое чтение, **без запуска кода системы, тестов и компиляции**. Каждый статус ниже относится к указанному scope. P0 означает блокирующий риск будущего включения/денежного контракта; это не заявление об отправке ордеров текущим EA. Основной EA остаётся DISABLED и вызывает неторговый stub.

Классификации SOURCE_DEFECT — статическое нарушение локального предиката, CONTRADICTION — несовместимость требований, UNPROVEN_CLAIM — отсутствие полного доказательства. Неполнота интеграции не называется действующим эксплуатационным обходом. Все записи OPEN. Новизна считается только относительно 29 FSA IDs: отсутствие прямого соответствия не означает первое обнаружение в истории D/NUM/R0.

Это единственный реестр; остальные отчёты ссылаются на его ID. Сокращения путей ниже относительны к HSBI. Указанные фрагменты — семантическая запись выражений, не новый исполняемый код.

| ID | Severity | Category | Stage | File | Lines | Proof Status | Related Improvement |
|---|---|---|---|---|---|---|---|
| HSBI-A03-ERR-001 | P0 | IDENTITY | Economic source / replay | Include/Money/HSBI_EconomicLedgerTypes.mqh | 9 | SOURCE_DEFECT | HSBI-A03-IMP-001 |
| HSBI-A03-ERR-002 | P0 | IDENTITY | Source discovery | Include/Money/HSBI_EconomicLedgerTypes.mqh | 6-7 | SOURCE_DEFECT | HSBI-A03-IMP-001 |
| HSBI-A03-ERR-003 | P1 | IDENTITY | Serialization | Include/Money/HSBI_EconomicLedgerTypes.mqh | 11 | POTENTIAL_RISK | HSBI-A03-IMP-002 |
| HSBI-A03-ERR-004 | P0 | IDENTITY | Allocation replay | Include/Money/HSBI_AllocationLedgerTypes.mqh | 8 | SOURCE_DEFECT | HSBI-A03-IMP-003 |
| HSBI-A03-ERR-005 | P0 | MONEY_ACCOUNTING | Allocation | Include/Money/HSBI_AllocationLedgerTypes.mqh | 7 | SOURCE_DEFECT | HSBI-A03-IMP-003 |
| HSBI-A03-ERR-006 | P1 | MONEY_ACCOUNTING | Allocation phases | Docs/04_MATHEMATICAL_MODEL_RU.md | 30 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-003 |
| HSBI-A03-ERR-007 | P0 | RESERVE | Reserve eligibility | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh | 44-47 | SOURCE_DEFECT | HSBI-A03-IMP-004 |
| HSBI-A03-ERR-008 | P0 | RESERVE | Reserve preview | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh | 63-70 | SOURCE_DEFECT | HSBI-A03-IMP-004 |
| HSBI-A03-ERR-009 | P0 | RISK | Risk preflight | Include/Risk/HSBI_RiskGateResult.mqh | 6 | SOURCE_DEFECT | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-010 | P0 | RISK | Fill confirmation | Include/Execution/HSBI_TransactionTypes.mqh | 15 | SOURCE_DEFECT | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-011 | P0 | MONEY_ACCOUNTING | Money state | Include/Money/HSBI_MoneyState.mqh | 5 | SOURCE_DEFECT | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-012 | P0 | IDENTITY | Position discovery | Include/Core/HSBI_Context.mqh | 19-24,48-53 | SOURCE_DEFECT | HSBI-A03-IMP-006 |
| HSBI-A03-ERR-013 | P0 | NEW_FAR | NewFar provenance | Include/Planning/HSBI_NewFarSolver.mqh | 119-124 | MISSING_CONTRACT | HSBI-A03-IMP-001 |
| HSBI-A03-ERR-014 | P1 | LOT_SIZING | Basket opening | Include/Planning/HSBI_GeometrySolver.mqh | 28-35 | SOURCE_DEFECT | HSBI-A03-IMP-007 |
| HSBI-A03-ERR-015 | P1 | GEOMETRY | Basket planning | Docs/04_MATHEMATICAL_MODEL_RU.md | 9 | CONTRADICTION | HSBI-A03-IMP-007 |
| HSBI-A03-ERR-016 | P1 | FSM | Full cycle | Hybrid_Split_Big_Independent_EA.mq5 | 19-44 | UNPROVEN_CLAIM | HSBI-A03-IMP-008 |
| HSBI-A03-ERR-017 | P1 | PERSISTENCE | Restart | Include/Persistence/HSBI_PersistenceInterface.mqh | 5-7 | UNPROVEN_CLAIM | HSBI-A03-IMP-009 |
| HSBI-A03-ERR-018 | P1 | CATCH_UP | Future Catch-Up | Include/Planning/HSBI_FutureSmallProofAggregator.mqh | 44,50-52 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-010 |
| HSBI-A03-ERR-019 | P1 | NEW_FAR | NewFar selection | Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md | 22-23 | CONTRADICTION | HSBI-A03-IMP-011 |
| HSBI-A03-ERR-020 | P1 | GEOMETRY | Future geometry | Include/Planning/HSBI_FutureSmallSolver.mqh | 89-90,143 | SOURCE_DEFECT | HSBI-A03-IMP-012 |
| HSBI-A03-ERR-021 | P1 | FUTURE_SMALL | Future Small | Include/Planning/HSBI_FutureSmallSolver.mqh | 12-16,142-147 | UNPROVEN_CLAIM | HSBI-A03-IMP-013 |
| HSBI-A03-ERR-022 | P1 | MONEY_ACCOUNTING | Valuation / Harvest | Include/Money/HSBI_CostModel.mqh | 13-18 | MISSING_CONTRACT | HSBI-A03-IMP-014 |
| HSBI-A03-ERR-023 | P1 | BROKER_MODEL | Initial Lock | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md | 6-12 | MISSING_CONTRACT | HSBI-A03-IMP-015 |
| HSBI-A03-ERR-024 | P2 | BROKER_MODEL | Market snapshots | Include/Planning/HSBI_ControlPrices.mqh | 11 | MISSING_CONTRACT | HSBI-A03-IMP-016 |
| HSBI-A03-ERR-025 | P1 | FSM | All commits | Include/Core/HSBI_StateMachine.mqh | 6 | SOURCE_DEFECT | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-026 | P1 | STABILITY | Plan digest | Include/Planning/HSBI_NewFarSolver.mqh | 35-45,106 | SOURCE_DEFECT | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-027 | P2 | DOCUMENTATION | Evidence interpretation | Tests/Static/ | LINE_NOT_VERIFIED | POTENTIAL_RISK | HSBI-A03-IMP-017 |
| HSBI-A03-ERR-028 | P2 | DOCUMENTATION | Normative hierarchy | Docs/03_FULL_SYSTEM_MANUAL_RU.md | 50-51 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-017 |
| HSBI-A03-ERR-029 | P2 | IMPLEMENTATION_MISMATCH | Production acceptance | Docs/04_MATHEMATICAL_MODEL_RU.md | 42-43 | UNPROVEN_CLAIM | HSBI-A03-IMP-018 |
| HSBI-A03-ERR-030 | P1 | IDENTITY | Journal replay | Include/Persistence/HSBI_ExecutionJournal.mqh | 21-29 | SOURCE_DEFECT | HSBI-A03-IMP-009 |
| HSBI-A03-ERR-031 | P1 | TERMINATION | Terminal residual | Include/Planning/HSBI_FutureSmallSolver.mqh | 144-149 | SOURCE_DEFECT | HSBI-A03-IMP-013 |
| HSBI-A03-ERR-032 | P1 | TERMINATION | Full recovery | Docs/04_MATHEMATICAL_MODEL_RU.md | 33-36 | UNPROVEN_CLAIM | HSBI-A03-IMP-013 |
| HSBI-A03-ERR-033 | P0 | MONEY_ACCOUNTING | Funding / allocation | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md | 6-24 | MISSING_CONTRACT | HSBI-A03-IMP-004 |
| HSBI-A03-ERR-034 | P1 | MARGIN | All opens/closes | Include/Money/HSBI_BasketMoneyEvaluator.mqh | 17 | MISSING_CONTRACT | HSBI-A03-IMP-015 |
| HSBI-A03-ERR-035 | P1 | RISK | Small Transition | Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | 9,20 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-019 |
| HSBI-A03-ERR-036 | P1 | MONEY_ACCOUNTING | Initial / FinalClose | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md | 20 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-020 |
| HSBI-A03-ERR-037 | P1 | FUTURE_SMALL | Price proof | Docs/05_GEOMETRY_MODEL_RU.md | 22 | UNPROVEN_CLAIM | HSBI-A03-IMP-021 |
| HSBI-A03-ERR-038 | P0 | RISK | Open residual risk | Docs/04_MATHEMATICAL_MODEL_RU.md | 33-36 | UNPROVEN_CLAIM | HSBI-A03-IMP-021 |
| HSBI-A03-ERR-039 | P2 | BROKER_MODEL | Broker lot admission | Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md | 9 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-007 |
| HSBI-A03-ERR-040 | P1 | MONEY_ACCOUNTING | Numeric boundaries | Include/Planning/HSBI_BrokerGrid.mqh | 26-27 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-002 |
| HSBI-A03-ERR-041 | P1 | RISK | Small Transition | Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | 12-14 | MISSING_CONTRACT | HSBI-A03-IMP-022 |
| HSBI-A03-ERR-042 | P1 | STABILITY | Full strategy | Docs/03_FULL_SYSTEM_MANUAL_RU.md | 12-18 | UNPROVEN_CLAIM | HSBI-A03-IMP-021 |
| HSBI-A03-ERR-043 | P1 | CATCH_UP | Catch-Up basis | Include/Money/HSBI_CatchUpModel.mqh | 10-15 | MISSING_CONTRACT | HSBI-A03-IMP-010 |
| HSBI-A03-ERR-044 | P1 | MONEY_ACCOUNTING | Final Close | Include/Money/HSBI_MoneyTypes.mqh | 7-9 | MISSING_CONTRACT | HSBI-A03-IMP-020 |
| HSBI-A03-ERR-045 | P1 | NEW_FAR | NewFar commit boundary | Include/Planning/HSBI_NewFarSolver.mqh | 108-113,149-151 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-011 |
| HSBI-A03-ERR-046 | P1 | BUY_SELL_DIRECTION | Both directions | Docs/03_FULL_SYSTEM_MANUAL_RU.md | 12 | CONTRADICTION | HSBI-A03-IMP-007 |
| HSBI-A03-ERR-047 | P1 | MONEY_ACCOUNTING | Big/Small attribution | Include/Money/HSBI_BasketMoneyEvaluator.mqh | 17 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-004 |

## HSBI-A03-ERR-001 — Economic equality теряет компоненты

- Исторические связи: FSA-001. Статус: OPEN; P0; IDENTITY; SOURCE_DEFECT.
- Этап: Economic source / replay. Источник и проверенные строки: `Include/Money/HSBI_EconomicLedgerTypes.mqh:9`. Функция/раздел: `HSBI_SameEconomicRecord`.
- Исходное правило/выражение: `Equal key, Net, volume, price`.

**Ожидание, фактическая логика и обоснование.** При одном key P=50,C=0 и P=60,C=-10 дают Net=50. Предикат не сравнивает компоненты, поэтому объявляет их одинаковыми. Требуется immutable equality полного payload, а не равенство итога.

**Последствия и зависимости.** Затрагивает Economic source / replay; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-001 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-002 — Namespace ключа не содержит account

- Исторические связи: FSA-001. Статус: OPEN; P0; IDENTITY; SOURCE_DEFECT.
- Этап: Source discovery. Источник и проверенные строки: `Include/Money/HSBI_EconomicLedgerTypes.mqh:6-7`. Функция/раздел: `HSBI_BuildSourceDealKey`.
- Исходное правило/выражение: `Symbol, Magic, Cycle, Deal`.

**Ожидание, фактическая логика и обоснование.** Два account с одинаковыми Symbol/Magic/Cycle/Deal неразличимы для этой структуры; AccountLogin отсутствует. Смена Magic/Cycle, напротив, меняет ключ того же broker deal. Это дефект source namespace, не доказанный повтор funding в работающем EA.

**Последствия и зависимости.** Затрагивает Source discovery; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-001 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-003 — Текстовый сериализатор не является полным codec

- Исторические связи: FSA-001; NUM-CODEC. Статус: OPEN; P1; IDENTITY; POTENTIAL_RISK.
- Этап: Serialization. Источник и проверенные строки: `Include/Money/HSBI_EconomicLedgerTypes.mqh:11`. Функция/раздел: `HSBI_SerializeEconomicRecord`.
- Исходное правило/выражение: `DoubleToString(...,8)`.

**Ожидание, фактическая логика и обоснование.** Компоненты payload отсутствуют; значения 1.000000001 и 1.000000002 теряются при восьми знаках. Если строка используется как authoritative identity, возможна коллизия. Если только диагностика, запретить её использование как proof. Полный downstream persistence не установлен.

**Последствия и зависимости.** Затрагивает Serialization; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-002 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-004 — Равная сумма подменяет allocation vector

- Исторические связи: FSA-002. Статус: OPEN; P0; IDENTITY; SOURCE_DEFECT.
- Этап: Allocation replay. Источник и проверенные строки: `Include/Money/HSBI_AllocationLedgerTypes.mqh:8`. Функция/раздел: `HSBI_ClassifyAllocationDuplicate`.
- Исходное правило/выражение: `Same event and equal total`.

**Ожидание, фактическая логика и обоснование.** FinalReserve=50,PartialFar=0 и FinalReserve=0,PartialFar=50 имеют общий итог 50, но разные назначения. При том же событии требуется CONFLICT. Предикат сравнивает итог вместо immutable вектора.

**Последствия и зависимости.** Затрагивает Allocation replay; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-003 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-005 — Отрицательные buckets проходят conservation

- Исторические связи: FSA-007. Статус: OPEN; P0; MONEY_ACCOUNTING; SOURCE_DEFECT.
- Этап: Allocation. Источник и проверенные строки: `Include/Money/HSBI_AllocationLedgerTypes.mqh:7`. Функция/раздел: `HSBI_ValidateAllocationConservation`.
- Исходное правило/выражение: `total<=source`.

**Ожидание, фактическая логика и обоснование.** Reserve=-50,PartialFar=100,source=50 удовлетворяют проверке общей суммы. Неотрицательность каждого bucket не следует из суммы и должна проверяться независимо.

**Последствия и зависимости.** Затрагивает Allocation; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-003 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-006 — PREPARED и полное COMMITTED не разделены

- Исторические связи: FSA-007; D-01. Статус: OPEN; P1; MONEY_ACCOUNTING; AMBIGUOUS_SPECIFICATION.
- Этап: Allocation phases. Источник и проверенные строки: `Docs/04_MATHEMATICAL_MODEL_RU.md:30; Include/Money/HSBI_AllocationLedgerTypes.mqh:7`. Функция/раздел: `Allocation conservation`.
- Исходное правило/выражение: `sum=source versus sum<=source`.

**Ожидание, фактическая логика и обоснование.** Grant10 от source50 допустим как PREPARED с Unallocated40, но не как полное распределение без остатка. Тип не доказывает фазу/судьбу 40. Не следует автоматически запрещать частичное preparation; требуется явный фазовый контракт.

**Последствия и зависимости.** Затрагивает Allocation phases; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-003 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-007 — Consumption не привязан к allocation authority

- Исторические связи: FSA-003. Статус: OPEN; P0; RESERVE; SOURCE_DEFECT.
- Этап: Reserve eligibility. Источник и проверенные строки: `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:44-47; Include/Money/HSBI_ReserveAllocationTypes.mqh:25-26`. Функция/раздел: `HSBI_ValidateReserveConsumption`.
- Исходное правило/выражение: `Nonempty sourceKey/allocationKey and current plan/revision`.

**Ожидание, фактическая логика и обоснование.** Сохранить корректный allocation A и изменить только непустой consumption allocationKey на B. Shape predicate не сравнивает его с authority A. Требуется обязательный caller binding полного source/allocation namespace. Это локальное разрешение preview, не фактическое списание.

**Последствия и зависимости.** Затрагивает Reserve eligibility; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-004 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-008 — Исчерпанный source снова даёт projected gain

- Исторические связи: FSA-004. Статус: OPEN; P0; RESERVE; SOURCE_DEFECT.
- Этап: Reserve preview. Источник и проверенные строки: `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:63-70`. Функция/раздел: `HSBI_EvaluateReserveCatchUp`.
- Исходное правило/выражение: `alreadyConsumed checked only in allocated branch`.

**Ожидание, фактическая логика и обоснование.** Source50,alreadyConsumed50,reserveAllocated0,eligible50,share0.8,AlreadyAllocated=false: gain40. Расходованный исходный ресурс не вычтен в этой ветви. Все прочие proof/grid/lot gates должны быть удовлетворены отдельно; пример не доказывает реальный debit.

**Последствия и зависимости.** Затрагивает Reserve preview; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-004 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-009 — Risk Gate не задаёт finite domain

- Исторические связи: FSA-005. Статус: OPEN; P0; RISK; SOURCE_DEFECT.
- Этап: Risk preflight. Источник и проверенные строки: `Include/Risk/HSBI_RiskGateResult.mqh:6`. Функция/раздел: `HSBI_ValidateRiskInput`.
- Исходное правило/выражение: `Ordered comparisons only`.

**Ожидание, фактическая логика и обоснование.** NaN projected margin не больше и не меньше обычных границ: ordered comparisons не доказывают допустимость. Требуется explicit finite/positive input domain до сравнений. Статическое следствие сравнения NaN; нативное выполнение здесь запрещено.

**Последствия и зависимости.** Затрагивает Risk preflight; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-005 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-010 — Transaction volume equality пропускает nonfinite

- Исторические связи: FSA-006. Статус: OPEN; P0; RISK; SOURCE_DEFECT.
- Этап: Fill confirmation. Источник и проверенные строки: `Include/Execution/HSBI_TransactionTypes.mqh:15`. Функция/раздел: `HSBI_TransactionBarrierPassed`.
- Исходное правило/выражение: `abs(accumulated-expected)>epsilon`.

**Ожидание, фактическая логика и обоснование.** Для NaN accumulated разность NaN, сравнение с epsilon ложно; нельзя вывести completed volume. Confirmation flags не заменяют finite/domain проверку. Нет доказанного dispatch-path в текущем main.

**Последствия и зависимости.** Затрагивает Fill confirmation; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-005 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-011 — MoneyState допускает бесконечный bucket

- Исторические связи: FSA-008. Статус: OPEN; P0; MONEY_ACCOUNTING; SOURCE_DEFECT.
- Этап: Money state. Источник и проверенные строки: `Include/Money/HSBI_MoneyState.mqh:5`. Функция/раздел: `HSBI_ValidateMoneyState`.
- Исходное правило/выражение: `buckets>=0`.

**Ожидание, фактическая логика и обоснование.** +Infinity неотрицательна, но не является допустимой денежной суммой. valid/revision требуют отдельной scope-спецификации: не всякий helper обязан проверять lifecycle-флаг, однако finite обязательно для денежной арифметики.

**Последствия и зависимости.** Затрагивает Money state; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-005 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-012 — Exactly-one Far проверяется не по всем slots

- Исторические связи: FSA-009. Статус: OPEN; P0; IDENTITY; SOURCE_DEFECT.
- Этап: Position discovery. Источник и проверенные строки: `Include/Core/HSBI_Context.mqh:19-24,48-53`. Функция/раздел: `HSBI_ValidateContext`.
- Исходное правило/выражение: `Four selected slots`.

**Ожидание, фактическая логика и обоснование.** Разные actual identifier100 в far и101 в initialBuy с ролью FAR не суммируются как два Far. При общем owner требование единственности всё равно нарушено. Два alias одного physical position нельзя считать двумя позициями; нужен registry уникальных identifier.

**Последствия и зависимости.** Затрагивает Position discovery; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-006 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-013 — Expected proof создаётся из предъявленного proof

- Исторические связи: FSA-010; D-08. Статус: OPEN; P0; NEW_FAR; MISSING_CONTRACT.
- Этап: NewFar provenance. Источник и проверенные строки: `Include/Planning/HSBI_NewFarSolver.mqh:119-124; Docs/31_MONEY_PROOF_IDENTITY_RU.md:3-7`. Функция/раздел: `HSBI_SolveNewFar / expectedReserveIdentity`.
- Исходное правило/выражение: `expected=proof.identity`.

**Ожидание, фактическая логика и обоснование.** Копирование a в expected делает equality(a,expected) тождественным. Сам helper корректно сравнивает два значения; независимое происхождение от broker/EA-origin provider не установлено. Успешный полный NewFar bypass не доказан и здесь не утверждается.

**Последствия и зависимости.** Затрагивает NewFar provenance; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-001 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-014 — Обязательный Core может исчезнуть после floor

- Исторические связи: FSA-011. Статус: OPEN; P1; LOT_SIZING; SOURCE_DEFECT.
- Этап: Basket opening. Источник и проверенные строки: `Include/Planning/HSBI_GeometrySolver.mqh:28-35`. Функция/раздел: `HSBI_SolveBigGeometry`.
- Исходное правило/выражение: `core==0 OR grid/max`.

**Ожидание, фактическая логика и обоснование.** F=.1,Rc=.01,Rt=3,Rs=.1,step=.01: rawCore=.001,Core0,Trend.3,Small.01,slope.19. Положительный slope не доказывает существование обязательной Core-ноги. Нужны Core>=Vmin и actual residual origin.

**Последствия и зависимости.** Затрагивает Basket opening; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-007 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-015 — Optional Trend несовместим с money evaluation

- Исторические связи: FSA-029. Статус: OPEN; P1; GEOMETRY; CONTRADICTION.
- Этап: Basket planning. Источник и проверенные строки: `Docs/04_MATHEMATICAL_MODEL_RU.md:9; Include/Planning/HSBI_GeometrySolver.mqh:30-33; Include/Money/HSBI_BasketMoneyEvaluator.mqh:15-16`. Функция/раздел: `Trend Rt=0`.
- Исходное правило/выражение: `T=0 admitted / all legs required`.

**Ожидание, фактическая логика и обоснование.** Rc>0,Rt=0,Rs>0 разрешены геометрией, но basket evaluator требует valid money/margin всех четырёх legs с положительным volume. Выбрать active-leg schema: не отправлять нулевую ногу брокеру либо явно запретить Rt=0 нормативно.

**Последствия и зависимости.** Затрагивает Basket planning; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-007 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-016 — Полный жизненный цикл отсутствует в main

- Исторические связи: FSA-012; FSA-014. Статус: OPEN; P1; FSM; UNPROVEN_CLAIM.
- Этап: Full cycle. Источник и проверенные строки: `Hybrid_Split_Big_Independent_EA.mq5:19-44; Include/Core/HSBI_StateMachine.mqh:5-7; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md:6-21`. Функция/раздел: `OnTick / pure state transitions`.
- Исходное правило/выражение: `Stub and limited topology`.

**Ожидание, фактическая логика и обоснование.** OnTick только обновляет reason от SubmitActionStub; normal topology обрывается после CoreOpening. Список состояний и pure apply не являются event-driven lifecycle. Это намеренный неторговый каркас, не ошибочно работающий торговый автомат.

**Последствия и зависимости.** Затрагивает Full cycle; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-008 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-017 — Durable и concurrent exactly-once не реализованы

- Исторические связи: FSA-013; D-07. Статус: OPEN; P1; PERSISTENCE; UNPROVEN_CLAIM.
- Этап: Restart. Источник и проверенные строки: `Include/Persistence/HSBI_PersistenceInterface.mqh:5-7; Docs/16_PERSISTENCE_AND_RESTART_RU.md:12-15`. Функция/раздел: `HSBI_PersistSnapshotStub`.
- Исходное правило/выражение: `success=false`.

**Ожидание, фактическая логика и обоснование.** При отсутствии backend нет доказательства commit-before-retry, CAS или восстановления глобального source register. NO_OP в памяти не доказывает once после crash. Stub честно отказывает, не является скрытой успешной persistence.

**Последствия и зависимости.** Затрагивает Restart; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-009 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-018 — Worst Transition не означает worst Catch-Up

- Исторические связи: FSA-015; CR-09. Статус: OPEN; P1; CATCH_UP; AMBIGUOUS_SPECIFICATION.
- Этап: Future Catch-Up. Источник и проверенные строки: `Include/Planning/HSBI_FutureSmallProofAggregator.mqh:44,50-52; Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md:5`. Функция/раздел: `catchUpControlLevel`.
- Исходное правило/выражение: `argmax TransitionLoss`.

**Ожидание, фактическая логика и обоснование.** Уровень A:Transition10,R30,L20,B1=>margin9. B:Transition5,R10,L20,B1=>margin-11. Проверка только A не доказывает minMargin>0. ALL_LEVEL min-margin — предложенный CR-09, не молча действующий утверждённый норматив; SINGLE/FINAL scope должен называться явно.

**Последствия и зависимости.** Затрагивает Future Catch-Up; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-010 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-019 — Minimum-safe N против global risk-first

- Исторические связи: FSA-016. Статус: OPEN; P1; NEW_FAR; CONTRADICTION.
- Этап: NewFar selection. Источник и проверенные строки: `Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:22-23; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md:3-7; Include/Planning/HSBI_NewFarCandidate.mqh:33-40`. Функция/раздел: `Candidate objective`.
- Исходное правило/выражение: `first minimum N / minimum risk first`.

**Ожидание, фактическая логика и обоснование.** Два safe кандидата N=.1,risk10 и N=.2,risk5: minimum-N выбирает .1, risk-first выбирает .2. Оба порядка детерминированы, но не эквивалентны. Без решения владельца нельзя объявить один лишь техническим tie-break другого.

**Последствия и зависимости.** Затрагивает NewFar selection; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-011 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-020 — NextBigGross подменён netBigVolume

- Исторические связи: FSA-017. Статус: OPEN; P1; GEOMETRY; SOURCE_DEFECT.
- Этап: Future geometry. Источник и проверенные строки: `Include/Planning/HSBI_FutureSmallSolver.mqh:89-90,143; Docs/04_MATHEMATICAL_MODEL_RU.md:21`. Функция/раздел: `Future Small compression gates`.
- Исходное правило/выражение: `netBigVolume>=priorBigGross`.

**Ожидание, фактическая логика и обоснование.** OldBigGross1, next C=.7,T=.5,S=1: nextBigGross1.2,net.2. Net.2<1 не доказывает gross1.2<1. Отдельные Far/slope gates могут потребовать другой полный fixture; логическая неэквивалентность сравнения от этого не исчезает.

**Последствия и зависимости.** Затрагивает Future geometry; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-012 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-021 — Конечный prefix не доказывает uniform tail

- Исторические связи: FSA-018. Статус: OPEN; P1; FUTURE_SMALL; UNPROVEN_CLAIM.
- Этап: Future Small. Источник и проверенные строки: `Include/Planning/HSBI_FutureSmallSolver.mqh:12-16,142-147; Docs/27_FUTURE_SMALL_SOLVER_RU.md:5`. Функция/раздел: `HSBI_ValidateConservativeBound`.
- Исходное правило/выражение: `observedFar<=initialFar*q^depth`.

**Ожидание, фактическая логика и обоснование.** F0=1,q=.8,F1=.8,F2=.64 согласованы, но F3=.64>.512. Конечные флаги costs/margin/risk не устанавливают квантор по всем будущим состояниям. Нужны uniform assumptions и inductive transition bound либо ограниченный preview scope.

**Последствия и зависимости.** Затрагивает Future Small; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-013 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-022 — Нет обязательной модели cost coverage

- Исторические связи: FSA-019; D-06. Статус: OPEN; P1; MONEY_ACCOUNTING; MISSING_CONTRACT.
- Этап: Valuation / Harvest. Источник и проверенные строки: `Include/Money/HSBI_CostModel.mqh:13-18; Docs/24_BROKER_MONEY_MODEL_RU.md:7`. Функция/раздел: `ProjectedNet cost basis`.
- Исходное правило/выражение: `gross + signed costs - positive allowances`.

**Ожидание, фактическая логика и обоснование.** BUY openAsk101,closeBid110: gross9 уже содержит spread. Повторное вычитание того же spread1 даёт8. Это условный пример повторного cost; не каждый spread buffer дублирует gross. Требуется CostID/basis/window/included/extra/unknown независимо от названия.

**Последствия и зависимости.** Затрагивает Valuation / Harvest; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-014 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-023 — Hedging/account admission не установлен сквозным guard

- Исторические связи: FSA-020. Статус: OPEN; P1; BROKER_MODEL; MISSING_CONTRACT.
- Этап: Initial Lock. Источник и проверенные строки: `Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:6-12; Hybrid_Split_Big_Independent_EA.mq5:19-26`. Функция/раздел: `Initial opposing positions`.
- Исходное правило/выражение: `BUY and SELL independent roles`.

**Ожидание, фактическая логика и обоснование.** На netting account встречные сделки могут уменьшить одну позицию, а не создать две независимые legs. Нужен admission по account mode и capability contract. Нет активного открытия в main; это предпосылка будущей реализации.

**Последствия и зависимости.** Затрагивает Initial Lock; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-015 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-024 — Freshness не определяет допустимый future skew

- Исторические связи: FSA-021. Статус: OPEN; P2; BROKER_MODEL; MISSING_CONTRACT.
- Этап: Market snapshots. Источник и проверенные строки: `Include/Planning/HSBI_ControlPrices.mqh:11`. Функция/раздел: `Price freshness`.
- Исходное правило/выражение: `now-timestamp<=maximumAge`.

**Ожидание, фактическая логика и обоснование.** now100,ts1000,maxAge10 проходят только верхнюю границу возраста. Допустимый clock skew и authoritative clock не заданы. Нельзя без решения вводить нулевой skew для всех provider; требуется окно и независимое время.

**Последствия и зависимости.** Затрагивает Market snapshots; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-016 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-025 — Revision increment не проверяет переполнение

- Исторические связи: FSA-022. Статус: OPEN; P1; FSM; SOURCE_DEFECT.
- Этап: All commits. Источник и проверенные строки: `Include/Core/HSBI_StateMachine.mqh:6`. Функция/раздел: `HSBI_ProposeStateTransition`.
- Исходное правило/выражение: `stateRevision+1`.

**Ожидание, фактическая логика и обоснование.** Для ulong maximum следующий монотонный идентификатор не представим. Guard exhaustion отсутствует. Конкретное native wrap/trap не запускалось; статически обещанная монотонность без domain guard недоказуема.

**Последствия и зависимости.** Затрагивает All commits; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-005 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-026 — Digest читает arrays до проверки depth

- Исторические связи: FSA-023. Статус: OPEN; P1; STABILITY; SOURCE_DEFECT.
- Этап: Plan digest. Источник и проверенные строки: `Include/Planning/HSBI_NewFarSolver.mqh:35-45,106`. Функция/раздел: `HSBI_FutureSmallTemplateDigest`.
- Исходное правило/выражение: `for i<maximumDepth`.

**Ожидание, фактическая логика и обоснование.** Digest вызывается до глубокой FutureSmall validation, а maximumDepth используется как bound fixed arrays128. maximumDepth129 даёт обращение за capacity. Реальный runtime exception не запускался; порядок dereference/validation статически неверен для внешнего DTO.

**Последствия и зависимости.** Затрагивает Plan digest; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-005 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-027 — Historical scope-checkers нельзя считать актуальной экономической проверкой

- Исторические связи: FSA-024. Статус: OPEN; P2; DOCUMENTATION; POTENTIAL_RISK.
- Этап: Evidence interpretation. Источник и проверенные строки: `Tests/Static/:LINE_NOT_VERIFIED`. Функция/раздел: `Frozen stage checkers`.
- Исходное правило/выражение: `stage-specific inventories`.

**Ожидание, фактическая логика и обоснование.** Новые audit-only файлы меняют tracked scope, но не экономику. Старый checker может отвергнуть scope или проверить узкую fixture; его статус нельзя переносить на полный цикл. В AUDIT03 runners не исполнялись, свежие exit codes отсутствуют. Требуется отдельная классификация historical scope/result.

**Последствия и зависимости.** Затрагивает Evidence interpretation; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-017 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-028 — Историческое COMPLETE имеет локальную область

- Исторические связи: FSA-025. Статус: OPEN; P2; DOCUMENTATION; AMBIGUOUS_SPECIFICATION.
- Этап: Normative hierarchy. Источник и проверенные строки: `Docs/03_FULL_SYSTEM_MANUAL_RU.md:50-51; Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md:1-309`. Функция/раздел: `Historical readiness labels`.
- Исходное правило/выражение: `OPEN_P0=0 versus lifecycle boundary`.

**Ожидание, фактическая логика и обоснование.** Документы содержат исторические этапные статусы и явные поздние границы NOT_PROVEN/no trading. Нельзя читать OPEN_P0=0 как текущую гарантию всех формул; нельзя также игнорировать уточняющий footer и объявлять документ безусловным обещанием. Нужны dated scope и precedence matrix.

**Последствия и зависимости.** Затрагивает Normative hierarchy; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-017 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-029 — Native соответствие математической модели не доказано этим аудитом

- Исторические связи: FSA-026. Статус: OPEN; P2; IMPLEMENTATION_MISMATCH; UNPROVEN_CLAIM.
- Этап: Production acceptance. Источник и проверенные строки: `Docs/04_MATHEMATICAL_MODEL_RU.md:42-43; Hybrid_Split_Big_Independent_EA.mq5:1-44`. Функция/раздел: `Native execution boundary`.
- Исходное правило/выражение: `Documentary algebra != runtime proof`.

**Ожидание, фактическая логика и обоснование.** Статический разбор не доказывает MetaEditor ABI, broker precision и фактические deals. Текущее задание прямо запрещает тесты/компиляцию; NOT_RUN не означает FAIL компилятора и не превращается в PASS.

**Последствия и зависимости.** Затрагивает Production acceptance; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-018 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-030 — Journal duplicate раннее body validation

- Исторические связи: FSA-027. Статус: OPEN; P1; IDENTITY; SOURCE_DEFECT.
- Этап: Journal replay. Источник и проверенные строки: `Include/Persistence/HSBI_ExecutionJournal.mqh:21-29`. Функция/раздел: `HSBI_ClassifyJournalAppend`.
- Исходное правило/выражение: `duplicate before ValidateJournalEntry`.

**Ожидание, фактическая логика и обоснование.** Сохранить ids/currentEntryDigest старого entry и изменить payloadDigest. Duplicate сравнивает прежний digest, не пересчитывает body, и возвращает NO_OP раньше validation. Нужна immutable body equality/проверка digest до replay classification.

**Последствия и зависимости.** Затрагивает Journal replay; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-009 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-031 — Terminal-route input не доказывает terminal execution

- Исторические связи: FSA-028. Статус: OPEN; P1; TERMINATION; SOURCE_DEFECT.
- Этап: Terminal residual. Источник и проверенные строки: `Include/Planning/HSBI_FutureSmallSolver.mqh:144-149; Docs/27_FUTURE_SMALL_SOLVER_RU.md:5`. Функция/раздел: `finiteSequence at volumeMin`.
- Исходное правило/выражение: `far<=volumeMin implies terminal`.

**Ожидание, фактическая логика и обоснование.** Достижение Vmin>0 не закрывает позицию и не доказывает operational route. Ветвь terminal не связывает результат с исполнимым terminal close. Условный geometric bound не заменяет отдельный terminal outcome.

**Последствия и зависимости.** Затрагивает Terminal residual; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-013 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-032 — Finite volume reduction не означает завершение цикла

- Исторические связи: FSA-018; FSA-028. Статус: OPEN; P1; TERMINATION; UNPROVEN_CLAIM.
- Этап: Full recovery. Источник и проверенные строки: `Docs/04_MATHEMATICAL_MODEL_RU.md:33-36`. Функция/раздел: `K and terminal close`.
- Исходное правило/выражение: `q^k bound`.

**Ожидание, фактическая логика и обоснование.** Индукция доказывает объём при успешных переходах; не гарантирует исполнение следующего шага, цену, margin, время или закрытие min lot. При F=Vmin есть ненулевой остаток, даже если depth=0 математически. Нужны terminal liquidity и feasible transition contracts.

**Последствия и зависимости.** Затрагивает Full recovery; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-013 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-033 — Нет сквозного projected→available funding proof

- Исторические связи: D-02; FUNDING-GLOBAL-ATTRIBUTION. Статус: OPEN; P0; MONEY_ACCOUNTING; MISSING_CONTRACT.
- Этап: Funding / allocation. Источник и проверенные строки: `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6-24; Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:24-28`. Функция/раздел: `Economic authority chain`.
- Исходное правило/выражение: `projected && !actual source proof`.

**Ожидание, фактическая логика и обоснование.** Прогноз100 при отсутствии confirmed deals оставляет confirmed available неизвестным/не созданным; если полная history подтверждает отсутствие источников — доступно0. Preview может быть valid, но не spendable grant. Нужны независимый reconciler, source-level registry, owner reservations и atomic journal. Две allocations50 одного источника50 не должны дать100.

**Последствия и зависимости.** Затрагивает Funding / allocation; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-004 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-034 — Standalone margin и endpoint не доказывают account/path margin

- Исторические связи: D-06; MQL-DOMAIN. Статус: OPEN; P1; MARGIN; MISSING_CONTRACT.
- Этап: All opens/closes. Источник и проверенные строки: `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17; Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:9-15`. Функция/раздел: `sum leg margin`.
- Исходное правило/выражение: `sum OrderCalcMargin per leg`.

**Ожидание, фактическая логика и обоснование.** Сумма standalone оценок не равна по определению whole-account hedged/tier margin. Existing900,new200,cap1000 требуют account basis; сравнение200<=1000 допустимо лишь если1000 — именно оставшийся лимит, не total cap. Требуется явный incremental/total/prefix contract.

**Последствия и зависимости.** Затрагивает All opens/closes; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-015 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-035 — Current signed loss не определяет historical breach policy

- Исторические связи: D-05. Статус: OPEN; P1; RISK; AMBIGUOUS_SPECIFICATION.
- Этап: Small Transition. Источник и проверенные строки: `Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:9,20; Docs/04_MATHEMATICAL_MODEL_RU.md:24`. Функция/раздел: `TransitionLoss`.
- Исходное правило/выражение: `max(0,-sum fills)`.

**Ожидание, фактическая логика и обоснование.** Fills -15,+100,cap12: current loss15→0, peak15→15, sticky breach true→true. Формула current верна для текущего net, но не эквивалентна двум историческим политикам. Фраза exceeded loss cap требует выбора reset/window/restart/prefix policy.

**Последствия и зависимости.** Затрагивает Small Transition; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-019 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-036 — Strategy RecoveryPL и полный economic CyclePnL имеют разную границу

- Исторические связи: D-02; F35. Статус: OPEN; P1; MONEY_ACCOUNTING; AMBIGUOUS_SPECIFICATION.
- Этап: Initial / FinalClose. Источник и проверенные строки: `Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:20; Docs/04_MATHEMATICAL_MODEL_RU.md:18`. Функция/раздел: `Initial Profit excluded`.
- Исходное правило/выражение: `InitialProfit not in RealizedCycleNet`.

**Ожидание, фактическая логика и обоснование.** Исключение стартовой прибыли допустимо как консервативная strategy metric, но тогда это не полный PnL от открытия Initial Lock. Opening costs не harvest grant, но экономические расходы. Разделить EconomicCyclePnL, RecoveryMetric и eligibility; не приписывать exclusion само по себе арифметическую ошибку.

**Последствия и зависимости.** Затрагивает Initial / FinalClose; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-020 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-037 — Локальная price monotonicity не покрывает market paths

- Исторические связи: FSA-018; F39. Статус: OPEN; P1; FUTURE_SMALL; UNPROVEN_CLAIM.
- Этап: Price proof. Источник и проверенные строки: `Docs/05_GEOMETRY_MODEL_RU.md:22; Include/Planning/HSBI_GeometrySolver.mqh:12-19`. Функция/раздел: `Recovery money direction`.
- Исходное правило/выражение: `nextTickMoney>baseMoney`.

**Ожидание, фактическая логика и обоснование.** Одна пара цен не доказывает каждый tick, gaps, spread shifts, swap или валютную конверсию. При постоянном K производная K*D, но при K(P),cost(P) нужны дополнительные члены. Требуется admitted symbol model и точный диапазон, а не универсальный вывод.

**Последствия и зависимости.** Затрагивает Price proof; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-021 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-038 — Безусловный upper loss bound не следует из lot contraction

- Исторические связи: FSA-018; FSA-028. Статус: OPEN; P0; RISK; UNPROVEN_CLAIM.
- Этап: Open residual risk. Источник и проверенные строки: `Docs/04_MATHEMATICAL_MODEL_RU.md:33-36; Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:6-18`. Функция/раздел: `Unhedged Far loss`.
- Исходное правило/выражение: `F>0 and unbounded adverse price`.

**Ожидание, фактическая логика и обоснование.** Для оставшегося SELL F>0 при линейной выплате K>0 loss=FK(P-Popen) не ограничен при P→∞. Это контрпример безусловной теореме, не опровержение условного safety contract. Нужны ограничение цены/экспозиции, гарантированный exit и slippage/маржа/ликвидность. Stop trigger сам по себе не гарантирует цену.

**Последствия и зависимости.** Затрагивает Open residual risk; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-021 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-039 — Разный origin volume grid

- Исторические связи: F48. Статус: OPEN; P2; BROKER_MODEL; AMBIGUOUS_SPECIFICATION.
- Этап: Broker lot admission. Источник и проверенные строки: `Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:9; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md:5; Include/Planning/HSBI_BrokerGrid.mqh:7-36`. Функция/раздел: `Grid definition`.
- Исходное правило/выражение: `Vmin+n*step versus n*step`.

**Ожидание, фактическая логика и обоснование.** При Vmin=.03,step=.02 первый набор .03,.05, второй допустимый над min .04,.06. Нельзя молча считать origins эквивалентными. Не утверждается, что такой grid разрешён конкретным брокером; admission может требовать min/step integer.

**Последствия и зависимости.** Затрагивает Broker lot admission; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-007 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-040 — Exact settled arithmetic и floating tolerance не имеют общего approved boundary

- Исторические связи: NUM-EXACT-1; NUM-DOMAIN-1. Статус: OPEN; P1; MONEY_ACCOUNTING; AMBIGUOUS_SPECIFICATION.
- Этап: Numeric boundaries. Источник и проверенные строки: `Include/Planning/HSBI_BrokerGrid.mqh:26-27; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md:5`. Функция/раздел: `floor/ceil tolerance; money precision`.
- Исходное правило/выражение: `floor(x/step+1e-12)`.

**Ожидание, фактическая логика и обоснование.** Для x/step=n-delta,0<delta<1e-12, математический floor с допуском может дать n вместо n-1. Это допустимо лишь при явно определённой capture uncertainty; settled conservation нельзя заменять epsilon. Reference рационалы не доказывают int64/double domain MQL5.

**Последствия и зависимости.** Затрагивает Numeric boundaries; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-002 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-041 — Закрытие хеджей может временно увеличить Net

- Исторические связи: Нет отдельного FSA ID; связь FSA-017. Статус: OPEN; P1; RISK; MISSING_CONTRACT.
- Этап: Small Transition. Источник и проверенные строки: `Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:12-14; Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:9-15`. Функция/раздел: `Ordered close prefixes`.
- Исходное правило/выражение: `Small→Far→Trend→Core part`.

**Ожидание, фактическая логика и обоснование.** F1,C1.2,T1,S.5,N.6: Net .7→1.2→2.2→1.2→.6; Gross3.7→3.2→2.2→1.2→.6. Endpoint contraction не ограничивает промежуточную направленность. Нужен prefix risk/margin при каждом partial fill и отказе следующего close; порядок без решения не менять.

**Последствия и зависимости.** Затрагивает Small Transition; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-022 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-042 — Recovery slope не доказывает profitability/stability

- Исторические связи: Нет отдельного FSA ID. Статус: OPEN; P1; STABILITY; UNPROVEN_CLAIM.
- Этап: Full strategy. Источник и проверенные строки: `Docs/03_FULL_SYSTEM_MANUAL_RU.md:12-18; Docs/04_MATHEMATICAL_MODEL_RU.md:12,42-43`. Функция/раздел: `Strategy-wide claims`.
- Исходное правило/выражение: `positive favorable slope`.

**Ожидание, фактическая логика и обоснование.** D>0 доказывает чувствительность при благоприятном ходе, не вероятность такого хода, ожидаемую доходность или bounded drawdown. Контрмаршрут adverse price/издержки может не дать прибыльного выхода. Сам мануал ограничивает proof scope; это незакрытая общая обязанность, не установленное ложное обещание автора.

**Последствия и зависимости.** Затрагивает Full strategy; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-021 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-043 — Absolute и signed incremental loss не типизированы

- Исторические связи: D-04. Статус: OPEN; P1; CATCH_UP; MISSING_CONTRACT.
- Этап: Catch-Up basis. Источник и проверенные строки: `Include/Money/HSBI_CatchUpModel.mqh:10-15; Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`. Функция/раздел: `farLossIncreaseMoney`.
- Исходное правило/выражение: `margin=R-L-B`.

**Ожидание, фактическая логика и обоснование.** Absolute50,baseline40,Reserve30: delta10 покрыт,absolute50 не покрыт. Поле increase в basket фактически берёт max(0,-FarNet). В low-level helper отрицательные Gain/Loss не запрещены явно; R=-10,L=-20,B1 дают9, если caller не обеспечивает domain. Нужны named types и mandatory caller, не новая экономика молча.

**Последствия и зависимости.** Затрагивает Catch-Up basis; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-010 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-044 — Final threshold helper доверяет неподтверждённому constructor

- Исторические связи: D-02; F11. Статус: OPEN; P1; MONEY_ACCOUNTING; MISSING_CONTRACT.
- Этап: Final Close. Источник и проверенные строки: `Include/Money/HSBI_MoneyTypes.mqh:7-9; Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md:7-11`. Функция/раздел: `HSBI_BuildRecoveryPL`.
- Исходное правило/выражение: `r.allowed=PL>=t.threshold`.

**Ожидание, фактическая логика и обоснование.** Переданный t.threshold не пересчитывается и t.valid не проверяется. При отсутствии mandatory validated-constructor contract локальная функция не доказывает полный FinalClose proof. Это scope gap, не воспроизведённый обход actual FinalClose engine, которого нет.

**Последствия и зависимости.** Затрагивает Final Close; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-020 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-045 — Selected N и actual residual имеют разный scope

- Исторические связи: FSA-010 related. Статус: OPEN; P1; NEW_FAR; AMBIGUOUS_SPECIFICATION.
- Этап: NewFar commit boundary. Источник и проверенные строки: `Include/Planning/HSBI_NewFarSolver.mqh:108-113,149-151; Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:25`. Функция/раздел: `HSBI_SolveNewFar`.
- Исходное правило/выражение: `selectedVolume<=actualResidual`.

**Ожидание, фактическая логика и обоснование.** При residual.6 solver может выбрать candidate.2. Как preview дальнейшего уменьшения это допустимо; как готовый promotion actual .6→.2 без сделки недопустимо. Разделить planning candidate и post-fill promotion assessment с равенством confirmed residual. Реальный promotion bypass не доказан.

**Последствия и зависимости.** Затрагивает NewFar commit boundary; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-011 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-046 — P+tick против зеркального Far BUY

- Исторические связи: Нет отдельного FSA ID; F39 related. Статус: OPEN; P1; BUY_SELL_DIRECTION; CONTRADICTION.
- Этап: Both directions. Источник и проверенные строки: `Docs/03_FULL_SYSTEM_MANUAL_RU.md:12; Docs/26_GEOMETRY_ENGINE_SPECIFICATION_RU.md:7; Docs/04_MATHEMATICAL_MODEL_RU.md:12,39`. Функция/раздел: `Recovery direction`.
- Исходное правило/выражение: `PL(P+tick)>PL(P) for both directions`.

**Ожидание, фактическая логика и обоснование.** При D=.7,K=1 FarSELL даёт delta+.7 на +1, зеркальный FarBUY даёт -.7. Для BUY благоприятен P-1, delta+.7. Нужен s=+1 для FarSELL,-1 для FarBUY и PL(P+s*tick)>PL(P). Это документальное противоречие, не доказательство неверных broker directions в коде.

**Последствия и зависимости.** Затрагивает Both directions; денежный/роль-связанный результат нельзя переносить за описанную границу proof. Сопоставление формул — в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), сквозной маршрут — в [полном цикле](HSBI_AUDIT03_FULL_CYCLE_REVIEW_RU.md). Для будущего подключения нужны нормативное решение применимого scope, независимая authority и нативное подтверждение обязательных callers. Никакого исправления или проверки исполнением в AUDIT03 нет.

**Предлагаемое устранение и подтверждение.** См. HSBI-A03-IMP-007 в [едином реестре предложений](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Приведённый контрпример должен впоследствии стать отдельным причинным отрицательным случаем вместе с положительным контролем и zero-state-delta, после разрешения тестового этапа. Зависимости и ограничения конкретного исправления зафиксированы в соответствующей карточке предложения.

## HSBI-A03-ERR-047 — Small contribution в preview Reserve имеет неопределённый policy scope

Исторические связи: D-03/M-05, но не отдельный FSA-ID. OPEN; P1; MONEY_ACCOUNTING; AMBIGUOUS_SPECIFICATION. Этап Big Harvest/Reserve attribution. Источник: `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`, `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:18-24`; proposed D-03 не утверждён.

Исходное выражение: `reserveGainMoney=max(0,CoreNet+TrendNet+SmallNet)`. При Core0,Trend0,Small10 поле равно10. Кандидат D-03 требует SmallResidualHeld10 и BigReserve0. Однако отдельный ReserveCatchUp proof требует Core/Trend role, поэтому это не доказательство successful funding из Small и не основание назвать все callers уязвимыми. Требуется назвать поле общим projected basket surplus либо явно применять утверждённую role allocation policy; не выбирать новую экономику автоматически.

Последствия: путаница attribution/preview/eligibility при будущем подключении. Зависимости: выбор D-03, independent role provenance, global allocation manifest. Предложение HSBI-A03-IMP-004 должно включать запрет неявного Small→Big transfer; отдельное подтверждённое transfer event может быть только после решения владельца. Необходимы будущие causal Small-only/Big-only/mixed tests, сейчас не выполнялись. Связанные формулы F08,F18,F60 и денежный обзор.

## Итоги

Всего 47 записей; P0=13, P1=29, P2=5, P3=0.

Классификации: AMBIGUOUS_SPECIFICATION=9, CONTRADICTION=3, MISSING_CONTRACT=9, POTENTIAL_RISK=2, SOURCE_DEFECT=16, UNPROVEN_CLAIM=8.

ERRORS_PROVEN считается как SOURCE_DEFECT + PROVEN_ERROR; это статический proof scope, не fresh runtime PASS. Все FSA-001…FSA-029 сопоставлены; многократные ссылки не увеличивают число исторических дефектов. Записи без прямого FSA: 11 (033,034,035,036,039,040,042,043,044,046,047); они пересекаются с историческими формулами/D/NUM. Итоговый счёт новизны определяется однозначно таблицей, без заявления first-ever.

## Итоговая сводная таблица

| ID | Severity | Category | Stage | File | Lines | Proof Status | Related Improvement |
|---|---|---|---|---|---|---|---|
| HSBI-A03-ERR-001 | P0 | IDENTITY | Economic source / replay | Include/Money/HSBI_EconomicLedgerTypes.mqh | 9 | SOURCE_DEFECT | HSBI-A03-IMP-001 |
| HSBI-A03-ERR-002 | P0 | IDENTITY | Source discovery | Include/Money/HSBI_EconomicLedgerTypes.mqh | 6-7 | SOURCE_DEFECT | HSBI-A03-IMP-001 |
| HSBI-A03-ERR-003 | P1 | IDENTITY | Serialization | Include/Money/HSBI_EconomicLedgerTypes.mqh | 11 | POTENTIAL_RISK | HSBI-A03-IMP-002 |
| HSBI-A03-ERR-004 | P0 | IDENTITY | Allocation replay | Include/Money/HSBI_AllocationLedgerTypes.mqh | 8 | SOURCE_DEFECT | HSBI-A03-IMP-003 |
| HSBI-A03-ERR-005 | P0 | MONEY_ACCOUNTING | Allocation | Include/Money/HSBI_AllocationLedgerTypes.mqh | 7 | SOURCE_DEFECT | HSBI-A03-IMP-003 |
| HSBI-A03-ERR-006 | P1 | MONEY_ACCOUNTING | Allocation phases | Docs/04_MATHEMATICAL_MODEL_RU.md | 30 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-003 |
| HSBI-A03-ERR-007 | P0 | RESERVE | Reserve eligibility | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh | 44-47 | SOURCE_DEFECT | HSBI-A03-IMP-004 |
| HSBI-A03-ERR-008 | P0 | RESERVE | Reserve preview | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh | 63-70 | SOURCE_DEFECT | HSBI-A03-IMP-004 |
| HSBI-A03-ERR-009 | P0 | RISK | Risk preflight | Include/Risk/HSBI_RiskGateResult.mqh | 6 | SOURCE_DEFECT | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-010 | P0 | RISK | Fill confirmation | Include/Execution/HSBI_TransactionTypes.mqh | 15 | SOURCE_DEFECT | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-011 | P0 | MONEY_ACCOUNTING | Money state | Include/Money/HSBI_MoneyState.mqh | 5 | SOURCE_DEFECT | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-012 | P0 | IDENTITY | Position discovery | Include/Core/HSBI_Context.mqh | 19-24,48-53 | SOURCE_DEFECT | HSBI-A03-IMP-006 |
| HSBI-A03-ERR-013 | P0 | NEW_FAR | NewFar provenance | Include/Planning/HSBI_NewFarSolver.mqh | 119-124 | MISSING_CONTRACT | HSBI-A03-IMP-001 |
| HSBI-A03-ERR-014 | P1 | LOT_SIZING | Basket opening | Include/Planning/HSBI_GeometrySolver.mqh | 28-35 | SOURCE_DEFECT | HSBI-A03-IMP-007 |
| HSBI-A03-ERR-015 | P1 | GEOMETRY | Basket planning | Docs/04_MATHEMATICAL_MODEL_RU.md | 9 | CONTRADICTION | HSBI-A03-IMP-007 |
| HSBI-A03-ERR-016 | P1 | FSM | Full cycle | Hybrid_Split_Big_Independent_EA.mq5 | 19-44 | UNPROVEN_CLAIM | HSBI-A03-IMP-008 |
| HSBI-A03-ERR-017 | P1 | PERSISTENCE | Restart | Include/Persistence/HSBI_PersistenceInterface.mqh | 5-7 | UNPROVEN_CLAIM | HSBI-A03-IMP-009 |
| HSBI-A03-ERR-018 | P1 | CATCH_UP | Future Catch-Up | Include/Planning/HSBI_FutureSmallProofAggregator.mqh | 44,50-52 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-010 |
| HSBI-A03-ERR-019 | P1 | NEW_FAR | NewFar selection | Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md | 22-23 | CONTRADICTION | HSBI-A03-IMP-011 |
| HSBI-A03-ERR-020 | P1 | GEOMETRY | Future geometry | Include/Planning/HSBI_FutureSmallSolver.mqh | 89-90,143 | SOURCE_DEFECT | HSBI-A03-IMP-012 |
| HSBI-A03-ERR-021 | P1 | FUTURE_SMALL | Future Small | Include/Planning/HSBI_FutureSmallSolver.mqh | 12-16,142-147 | UNPROVEN_CLAIM | HSBI-A03-IMP-013 |
| HSBI-A03-ERR-022 | P1 | MONEY_ACCOUNTING | Valuation / Harvest | Include/Money/HSBI_CostModel.mqh | 13-18 | MISSING_CONTRACT | HSBI-A03-IMP-014 |
| HSBI-A03-ERR-023 | P1 | BROKER_MODEL | Initial Lock | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md | 6-12 | MISSING_CONTRACT | HSBI-A03-IMP-015 |
| HSBI-A03-ERR-024 | P2 | BROKER_MODEL | Market snapshots | Include/Planning/HSBI_ControlPrices.mqh | 11 | MISSING_CONTRACT | HSBI-A03-IMP-016 |
| HSBI-A03-ERR-025 | P1 | FSM | All commits | Include/Core/HSBI_StateMachine.mqh | 6 | SOURCE_DEFECT | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-026 | P1 | STABILITY | Plan digest | Include/Planning/HSBI_NewFarSolver.mqh | 35-45,106 | SOURCE_DEFECT | HSBI-A03-IMP-005 |
| HSBI-A03-ERR-027 | P2 | DOCUMENTATION | Evidence interpretation | Tests/Static/ | LINE_NOT_VERIFIED | POTENTIAL_RISK | HSBI-A03-IMP-017 |
| HSBI-A03-ERR-028 | P2 | DOCUMENTATION | Normative hierarchy | Docs/03_FULL_SYSTEM_MANUAL_RU.md | 50-51 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-017 |
| HSBI-A03-ERR-029 | P2 | IMPLEMENTATION_MISMATCH | Production acceptance | Docs/04_MATHEMATICAL_MODEL_RU.md | 42-43 | UNPROVEN_CLAIM | HSBI-A03-IMP-018 |
| HSBI-A03-ERR-030 | P1 | IDENTITY | Journal replay | Include/Persistence/HSBI_ExecutionJournal.mqh | 21-29 | SOURCE_DEFECT | HSBI-A03-IMP-009 |
| HSBI-A03-ERR-031 | P1 | TERMINATION | Terminal residual | Include/Planning/HSBI_FutureSmallSolver.mqh | 144-149 | SOURCE_DEFECT | HSBI-A03-IMP-013 |
| HSBI-A03-ERR-032 | P1 | TERMINATION | Full recovery | Docs/04_MATHEMATICAL_MODEL_RU.md | 33-36 | UNPROVEN_CLAIM | HSBI-A03-IMP-013 |
| HSBI-A03-ERR-033 | P0 | MONEY_ACCOUNTING | Funding / allocation | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md | 6-24 | MISSING_CONTRACT | HSBI-A03-IMP-004 |
| HSBI-A03-ERR-034 | P1 | MARGIN | All opens/closes | Include/Money/HSBI_BasketMoneyEvaluator.mqh | 17 | MISSING_CONTRACT | HSBI-A03-IMP-015 |
| HSBI-A03-ERR-035 | P1 | RISK | Small Transition | Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | 9,20 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-019 |
| HSBI-A03-ERR-036 | P1 | MONEY_ACCOUNTING | Initial / FinalClose | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md | 20 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-020 |
| HSBI-A03-ERR-037 | P1 | FUTURE_SMALL | Price proof | Docs/05_GEOMETRY_MODEL_RU.md | 22 | UNPROVEN_CLAIM | HSBI-A03-IMP-021 |
| HSBI-A03-ERR-038 | P0 | RISK | Open residual risk | Docs/04_MATHEMATICAL_MODEL_RU.md | 33-36 | UNPROVEN_CLAIM | HSBI-A03-IMP-021 |
| HSBI-A03-ERR-039 | P2 | BROKER_MODEL | Broker lot admission | Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md | 9 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-007 |
| HSBI-A03-ERR-040 | P1 | MONEY_ACCOUNTING | Numeric boundaries | Include/Planning/HSBI_BrokerGrid.mqh | 26-27 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-002 |
| HSBI-A03-ERR-041 | P1 | RISK | Small Transition | Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | 12-14 | MISSING_CONTRACT | HSBI-A03-IMP-022 |
| HSBI-A03-ERR-042 | P1 | STABILITY | Full strategy | Docs/03_FULL_SYSTEM_MANUAL_RU.md | 12-18 | UNPROVEN_CLAIM | HSBI-A03-IMP-021 |
| HSBI-A03-ERR-043 | P1 | CATCH_UP | Catch-Up basis | Include/Money/HSBI_CatchUpModel.mqh | 10-15 | MISSING_CONTRACT | HSBI-A03-IMP-010 |
| HSBI-A03-ERR-044 | P1 | MONEY_ACCOUNTING | Final Close | Include/Money/HSBI_MoneyTypes.mqh | 7-9 | MISSING_CONTRACT | HSBI-A03-IMP-020 |
| HSBI-A03-ERR-045 | P1 | NEW_FAR | NewFar commit boundary | Include/Planning/HSBI_NewFarSolver.mqh | 108-113,149-151 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-011 |
| HSBI-A03-ERR-046 | P1 | BUY_SELL_DIRECTION | Both directions | Docs/03_FULL_SYSTEM_MANUAL_RU.md | 12 | CONTRADICTION | HSBI-A03-IMP-007 |
| HSBI-A03-ERR-047 | P1 | MONEY_ACCOUNTING | Big/Small attribution | Include/Money/HSBI_BasketMoneyEvaluator.mqh | 17 | AMBIGUOUS_SPECIFICATION | HSBI-A03-IMP-004 |

## COVERAGE-COMPLETION — переоценка прежних карточек (IDs неизменны)

ERR-002: Docs/NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md:67,118 и R0B proposal:79 включали SchemaVersion/NFC в canonical namespace; R0F identity:10 и R0G identity:11 отделяют logical source от codec/schema и запрещают guessed NFC/casefold. Нельзя автоматически выбрать один вариант. Logical source lifetime и допустимая cross-schema equivalence — D-08/NUM-CODEC administrator choice; версия представления не должна создавать новую прибыль. Это уточнение прежней root cause, не новый ID.

ERR-003: дополнительные места неполного content binding: CandidatePlan.mqh:7–8 fingerprint не включает coreLots/trendLots/smallLots/geometry/money/risk proofs; BasketMoneyEvaluator.mqh:20–27 digest не содержит reserveGainMoney/farLossIncreaseMoney/safetyBuffer; NewFarSolver.mqh:47–57 не включает все compression/risk cap values, обещанные Docs29:5. Изменение coreLots1→2 при прежних positionFingerprint/IDs не меняет SameCandidatePlan; изменение risk cap при прежних snapshot IDs требует независимого full-content receipt. Snapshot ID/диагностическая строка не заменяют весь payload. Уровень POTENTIAL_RISK сохранён: полный commit caller, использующий эти строки как единственную authority, не доказан. Исправление IMP-002/IMP-011 требует явного назначения identity versus content fingerprint.

**СНЯТАЯ РАБОЧАЯ ГИПОТЕЗА; см. исправление ниже.** ERR-005: обнаружен ещё один независимый causal clause того же nonnegative-components инварианта. AllocationPolicyTypes.mqh:19–23 проверяет transitionShare на finite, но не на >=0. reserveShare=1,partialFarShare=1,transitionShare=-1,carryShare=0 дают sum1 и проходят range/sum predicate. Ожидается отказ отрицательной share. Это source-level acceptance локального policy, не доказанный actual allocation200%. IMP-003 и IMP-005 должны охватывать каждую share отдельно. Не изменяет старое доказательство отрицательных bucket сумм.

ERR-010: тот же finite/domain gap присутствует в OwnershipGuardTypes.mqh:8 и ExternalOutcome.mqh:25–30. При finite expectedVolume1 и actualVolumeNaN ordered abs-comparison не устанавливает равенства. При volumeToleranceNaN даже finite volumes1/2 не отличаются по предикату. ExternalOutcome проверяет только intent digest, не его Structure: согласованные intent/outcome volumes-1 дают abs difference0; обязательность ранее validated immutable intent должна быть доказана caller либо проверяться entry point. Нельзя называть full transaction completion доказанным по этим bool. На текущем main отсутствует financial execution path. Новые native тесты не выполнялись; IMP-005/008 охватывают все соответствующие consumers.

ERR-013: RuntimeTransactionBarrier.mqh:7 и RuntimeRestartValidator.mqh:16 передают текущий context и его же account/symbol/magic как expected. Это локальная согласованность DTO, а не independent namespace provider. RuntimeDecisionValidator.mqh:22–23 проверяет shape money/risk identity, но не связывает все поля с независимой expected identity; marginIdentity не проходит аналогичный full equality. Полная provenance-chain остаётся MISSING_CONTRACT; сквозной NewFar bypass не повышен до PROVEN.

ERR-017: ReconciliationTypes.mqh:7 различает empty digests как CLEAN_START до identity/economic checks и сравнивает economicLedgerDigest с allocationLedgerDigest на буквальное равенство. Empty history token не доказывает complete-empty account history; два разнородных ledger roots обычно не обязаны совпадать. Если это два common reconciliation roots, такой контракт должен быть назван явно. Функция всегда сохраняет newTradingAllowed=false и не выдаёт RECONCILED, поэтому это ограниченный placeholder, не доказанный restart re-funding. Persistence schema Docs/HSB_2E_PERSISTENCE_SCHEMA_RU.md:8–16 предлагает общие имена temp/data: namespace/path-lock и crash model ещё надо доказать до backend. Не утверждается, что FileFlush/FileMove гарантируют atomic durability.

ERR-024: будущий timestamp creation у ExecutionPreflight.mqh:23 тоже не исключается одним expiry gate. Время observation/cost/market должно иметь один provider window; fresh flag и совпадающая цена сами по себе не доказывают contemporaneous snapshots. Предложенный zero-skew fixture не утверждён для broker.

ERR-028: generic READINESS/ADMIN_ACCEPTED исторических отчётов не является approval16 нынешних решений. Отдельный лист DG01 различает readiness и пустое AdministratorDecision. Новый статус этих решений по-прежнему AWAITING_ADMIN_APPROVAL.

## HSBI-A03-ERR-048 — Money amounts не связаны с предъявленными proofs на публичной границе

**OPEN; P0; RESERVE; SOURCE_DEFECT (локальная публичная функция).** Источники: Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:24–33,61–74; Include/Planning/HSBI_NewFarSolver.mqh:121–127; Docs/NEXT_STAGE_02_MONEY_AUDIT_RU.md:224; Docs/31_MONEY_PROOF_IDENTITY_RU.md:3–7. Историческая связь: M-01/M-02 смежные, но эта причина — amount binding, а не identity key или spent-source.

Функция HSBI_EvaluateReserveCatchUp проверяет source-proof shape/identity и независимые scalar поля, но не equalities reserveEligibleMoney=sourceProof.netMoney и FarLoss=max(0,-farProof.netMoney). Положительный согласованный контроль: proof Reserve50,eligible50,share.8,FarProof-20,Loss20,buffer1 даёт положительный margin19. Ручная разность gain40-loss20-buffer1=19. Остальные policy/source/lot/current flags должны быть корректны; ни один runtime вызов здесь не сделан.

Причинный отрицательный пример1: сохранить proof source10,allocation allocatable10,reserveAllocated0,alreadyConsumed0,share.8; изменить только eligible10→100. Gain становится80, хотя proof/source cap10. При Loss20/buffer1 margin59; lot gate .8*3>1 может быть удовлетворён. Пример2: согласованные proof source50/eligible50,FarProof-50,Loss50,buffer1 не проходят (margin-11); изменить только scalar Loss50→0 — formula39>0, хотя proof loss50. Требуется отказ inconsistency до численной положительности.

Current NewFar caller явно выводит эти scalars из control proofs, поэтому его именно эта инъекция не обходит. Публичный evaluator и другие будущие callers не имеют enforced typed validated amount constructor. Это не реальное списание, создание денег или доказанный solver exploit. Влияние: недостоверный local money proof, будущий Catch-Up eligibility. Исправление: IMP-004/IMP-010, обязательные source-value/currency/basis bindings либо ограниченный внутренний helper с непроходимой полной внешней границей. Выбор loss basis D-04 и money type D-02 требует владельца. Будущее подтверждение — original/control, mismatch каждого scalar, direct/public caller и zero deltas; сейчас REQUIRES_FUTURE_TEST.

## HSBI-A03-ERR-049 — Непустой enum принимается вместо известного направления/роли

**OPEN; P1; IDENTITY; SOURCE_DEFECT.** Include/Execution/HSBI_ExecutionIntent.mqh:28–40, Include/Execution/HSBI_ActionTypes.mqh:6,EventTypes.mqh:6,Include/Money/HSBI_AllocationLedgerTypes.mqh:9. Контракт: Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md:23–32; Docs/04_MATHEMATICAL_MODEL_RU.md:42. Функция HSBI_ValidateExecutionIntentStructure.

Контроль — корректный BUY/BID/BigCore intent. Изменить только direction на cast99, digest пересчитать для изоляции shape: direction!=NONE остаётся true; обе ветви BUY/SELL side mismatch не срабатывают. При остальных корректных полях Structure возвращает true статически. Аналогично role99 не NONE. Это не требование принимать недопустимый MQL literal без cast: внешняя wire/data corruption может дать integral enum value, а cast не доказывает membership. Bucket helper допускает unknown enum, если это не запрещённый FinalReserve-for-partial. Простые action/event validators проверяют !=NONE, не exhaustive membership.

Нужен closed enum validator до финансового использования и связь intent direction с typed control price. Mandatory full caller не доказан; main не отправляет ордеров. IMP-005/007/008; техническое уточнение domain, без выбора новой экономики. Native/caller integration остаётся будущим отдельным evidence.

## HSBI-A03-ERR-050 — completedActionCount не связан с содержимым snapshot

**OPEN; P1; PERSISTENCE; AMBIGUOUS_SPECIFICATION.** Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:27–40,HSBI_ValidateExecutionStateSnapshot; контракт Docs/HSB.2C_Journal_Persistence_Reconciliation.md:5 и Docs/16_PERSISTENCE_AND_RESTART_RU.md:12–15.

Контроль: fully shaped completedIntent,statusCOMPLETED,completedActionCount1,pending absent,correct snapshot digest. Изменить только count1→0 и пересчитать snapshot digest (не nested intent); bounds допускают0, completedExists проверяет status, но нет (count==1)==completedExists. Предикат сохраняет acceptance. Обратное count1 при отсутствии completedIntent также не исключается. activeIntentCount имеет явный existence binding, completedActionCount его не имеет.

Это inconsistency reconstruction DTO, а не доказанный double commit/restart spending. Нужна explicit count/body/lastConfirmedAction/Event linkage к независимому journal; исторический processing count иной семантики должен называться иначе. IMP-009; schema/recovery scope уточняет D-07/SNAP, не утверждается автоматически. No actual snapshot IO performed, никаких deltas текущим аудитом нет.

## Исправление рабочей гипотезы ERR-005 при повторном чтении

Повторное посимвольное чтение `Include/Money/HSBI_AllocationPolicyTypes.mqh:21–23` установило: условие `p.transitionShare<0.0` **присутствует** на строке22. Приведённый выше рабочий пример shares(1,1,-1,0) отвергается этим guard. Утверждение о пропущенной transitionShare nonnegativity — ошибка чтения аудитора, **NOT_CONFIRMED / WITHDRAWN**. Это не новый дефект и не результат выполненного теста. Старое доказательство ERR-005 о отрицательных buckets в другом validator (`HSBI_ValidateAllocationConservation`) сохраняется. Новый ERR-ID не присваивается. Проверка отдельных shares остаётся будущим критерием regression, но не исправлением отсутствующего guard.

### Уточнение доказательного статуса ERR-050

Acceptance несогласованных count/body следует из текста предиката. Но первичный норматив не определяет, является completedActionCount cardinality предъявленного объекта или отдельным историческим счётчиком. Поэтому итоговая классификация **AMBIGUOUS_SPECIFICATION**, а нарушение cardinality-контракта — условный вывод, не безусловно подтверждённый production SOURCE_DEFECT. F066 сохраняет UNDEFINED. Нужен владелец snapshot schema; ни historical recovery, ни double-spend этим не доказаны.

## Текущий итог COVERAGE-COMPLETION (исторические таблицы выше сохранены)

50 карточек с уникальными IDs ERR-001…050. P0=14, P1=31, P2=5, P3=0. SOURCE_DEFECT=18, CONTRADICTION=3, AMBIGUOUS_SPECIFICATION=10, MISSING_CONTRACT=9, UNPROVEN_CLAIM=8, POTENTIAL_RISK=2. Из новых: ERR-048/049 — локальные source defects, ERR-050 — неопределённость snapshot-контракта. Старые47 IDs не удалены и не переназначены. Снятая гипотеза transitionShare не входит в число дефектов.


| Новый ID | Severity | Scope | Итоговая классификация | Связанные предложения |
|---|---|---|---|---|
| HSBI-A03-ERR-048 | P0 | ReserveCatchUp public value bindings | SOURCE_DEFECT | IMP-004/010 |
| HSBI-A03-ERR-049 | P1 | Closed enums intent/action/event/bucket | SOURCE_DEFECT | IMP-005/007/008 |
| HSBI-A03-ERR-050 | P1 | completedActionCount schema semantics | AMBIGUOUS_SPECIFICATION | IMP-009 |
