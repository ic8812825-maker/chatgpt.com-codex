# Журнал текущего статуса проекта и дорожная карта до реальной торговли

## Проект

`MinusLock_BigHarvest_EA_V2`

## Обязательная граница работ

Все дальнейшие изменения, проверки, тесты, отчёты и коммиты выполняются строго внутри каталога:

`MinusLock_BigHarvest_EA_V2`

Выход за пределы этого каталога запрещён.

## Главное правило управления этапами

1. Каждый этап разбивается на самостоятельные пункты.
2. После выполнения каждого пункта создаётся отдельный коммит.
3. Сообщение коммита обязательно пишется на русском языке и содержит номер этапа и краткое, но содержательное описание результата.
4. После завершения этапа программист формирует итоговый отчёт этапа внутри `Docs`.
5. Переход к следующему этапу запрещён до прямого подтверждения пользователя.
6. Если во время этапа обнаружено противоречие документации, математики или кода, оно не замалчивается: создаётся запись в отчёте с категорией, риском, файлами, формулами и требуемым решением.
7. Нельзя объявлять пункт или этап завершённым только по статическому наличию кода. Для каждого результата должны существовать проверяемые доказательства: формулы, тест-векторы, исходные тесты, MetaEditor compile, Strategy Tester runtime или фактические deal-ledger проверки — в зависимости от уровня этапа.

---

# 1. Назначение этого журнала

Этот документ является единым управляющим журналом проекта. Он фиксирует:

- текущее фактическое состояние;
- известные расхождения между документацией и кодом;
- главный приоритет дальнейших работ;
- полный план доведения системы до контролируемой торговли на реальном счёте;
- критерии готовности каждого этапа;
- текущий выполненный этап;
- следующий разрешённый к выполнению этап;
- запрет перехода без подтверждения пользователя.

Основной приоритет всего плана — `Hybrid Split Big`.

Документация рассматривается как нормативная основа. Код не имеет права определять торговую математику самостоятельно или противоречить утверждённым формулам.

---

# 2. Текущий статус проекта

## 2.1. Что уже существует

В проекте уже присутствуют:

- отдельные роли `Far`, `BigCore`, `BigTrend`, `SmallBase`, `NewFar`;
- базовая математическая модель трёх законов Hybrid Split Big;
- отдельные документы по формулам, инвариантам, денежному потоку, finite catch-up, Future Small, MQL5 mapping и proof-моделям;
- MQL5-модули геометрии, денежной модели, округления, finite catch-up, margin, worst-case и принятия решения;
- Python-инструменты и тестовые модели Hybrid Split Big;
- механизм opt-in, при котором Hybrid Split Big не должен молча заменять legacy-логику;
- отдельные reason codes, reject/error outcomes, fingerprints и trace;
- частичная реализация transaction safety, persistence и reconciliation;
- база для проверки Symbol + Magic + CycleID + identifier.

## 2.2. Что пока нельзя считать завершённым

На текущем состоянии нельзя подтверждать готовность Hybrid Split Big к реальной торговле, потому что остаются как минимум следующие критические разрывы:

1. Документация неоднородна: доказательные профили, фактические default-параметры и будущая нормативная модель местами смешаны.
2. Нет единого утверждённого нормативного документа, который однозначно превосходит все старые отчёты и черновики.
3. Полная рекурсивная проверка `Future Small` отсутствует; реализован только ограниченный depth-1 preview.
4. Основной Risk gate не везде вычисляет реальный денежный риск нового цикла до контрольной цены.
5. Final Close preview в основной цепочке принятия решения не является полноценным обязательным денежным gate.
6. Point-by-point монотонность `RecoveryPL` существует как отдельная проверка, но должна быть доказанно встроена в единый обязательный pre-open contract.
7. Minimum-safe `NewFar` должен определяться дискретным broker-valid Solver, а не только фиксированным `TargetNewFarRatio`.
8. Нет единого persisted money-ledger контракта для `RealizedCyclePL`, `FinalReserveReal`, `PartialFarBudget`, `Carry`, `TransitionBudget`, actual consumption и residual.
9. Нет полной гарантии exactly-once для всех денежных событий при повторном запуске, partial execution и reconciliation.
10. Нет завершённого единого terminal-safe протокола.
11. Нет подтверждённой компиляции MetaEditor `0 errors / 0 warnings` для итоговой версии.
12. Нет доказанной runtime-паритетности MQL5 с Python oracle на одном наборе тест-векторов.
13. Нет полного Strategy Tester evidence pack для Big, Small, reverse, restart, partial fill, spread/slippage/margin stress.
14. Нет утверждённого ограничения параметров для первого real-money режима.

## 2.3. Текущий строгий статус

`Hybrid Split Big` находится в состоянии:

`МАТЕМАТИЧЕСКАЯ И АРХИТЕКТУРНАЯ БАЗА СОЗДАНА, НОРМАТИВНАЯ КОНСОЛИДАЦИЯ И PRODUCTION-РЕАЛИЗАЦИЯ НЕ ЗАВЕРШЕНЫ`.

Реальная торговля запрещена до прохождения всех обязательных этапов этого плана.

---

# 3. Самое важное, что необходимо сделать в первую очередь

## Приоритет №1 — исправить и заморозить нормативную документацию Hybrid Split Big

Нельзя начинать дальнейшее расширение торгового кода, пока не определён единственный нормативный источник истины.

Причина:

- сейчас отдельные документы описывают разные профили коэффициентов;
- часть документов фиксирует будущие требования как будто они уже полностью реализованы;
- отдельные формулы уровня A могут быть ошибочно восприняты как торговое разрешение уровня B;
- legacy, Split Big и Hybrid параметры могут быть смешаны;
- без утверждённой спецификации невозможно доказать, что код реализует именно требуемую систему.

Поэтому следующий этап должен быть посвящён не добавлению новых сделок, а полной ревизии и консолидации документации.

---

# 4. Полная дорожная карта

# Этап 3.1. Нормативная консолидация документации Hybrid Split Big

## Цель

Создать единую, непротиворечивую и математически проверяемую спецификацию, на которую будет ссылаться весь MQL5-код и все тесты.

## Пункты

### 3.1.1. Инвентаризация всей папки `Docs`

Программист обязан:

- перечислить все документы;
- определить назначение каждого;
- присвоить статус: `NORMATIVE`, `SUPPORTING`, `REPORT`, `HISTORICAL`, `OBSOLETE`, `CONFLICTING`;
- указать, какие документы содержат формулы, параметры, state transitions, money ledger, execution contract, тестовые доказательства;
- выявить дублирование и устаревшие утверждения.

Результат: `Docs/DOCUMENTATION_INVENTORY_AND_AUTHORITY_RU.md`.

Коммит:

`Этап 3.1.1: проведена инвентаризация и классификация документации Hybrid Split Big`.

### 3.1.2. Таблица всех противоречий

Обязательные категории:

- разные значения коэффициентов;
- разные определения Reserve;
- разные формулы RecoveryPL;
- разные роли BigCore/BigTrend;
- разные условия NewFar;
- fixed target против minimum-safe Solver;
- разная трактовка Risk;
- разные условия Final Close;
- различия по Future Small depth;
- различия между mathematical proof и production-ready claim;
- конфликт legacy/Split/Hybrid параметров.

Для каждого расхождения:

- документы и разделы;
- обе формулировки;
- математический анализ;
- риск;
- рекомендуемое нормативное решение;
- статус решения: `OPEN`, `USER_DECISION_REQUIRED`, `RESOLVED`.

Результат: `Docs/HYBRID_SPLIT_BIG_DOCUMENTATION_CONFLICTS_RU.md`.

Коммит:

`Этап 3.1.2: зафиксированы противоречия документации и варианты нормативного решения`.

### 3.1.3. Единый словарь и размерности

Должны быть однозначно определены:

- все позиции и роли;
- lots, ratios, points, price, money, percent, state, identifier;
- знаки каждой денежной величины;
- projected и actual значения;
- source of truth каждого значения;
- допустимые tolerance;
- запрет смешения raw и normalized lots.

Результат: нормативный раздел в главном мануале.

Подтверждённый управляющий статус после remote publication recovery:

```text
STAGE_3_1_3_STATUS=CLOSED
FINAL_PUBLISHED_COMMIT=018d25e3722d7830dd85d1e04e19583660e55f28
REMOTE_BRANCH=work
REMOTE_PUBLICATION_VERIFIED=YES
NEXT_ALLOWED_STAGE=3.1.4
STAGE_3_1_4_STARTED=NO
AWAITING_USER_APPROVAL=YES
```

Указанный commit — опубликованный и независимо scope-проверенный recovery HEAD
перед этой document-only записью статуса. Доказательства находятся в
`STAGE_3_1_3_11_GITHUB_PUBLICATION_RECOVERY_REPORT_RU.md`. Этап 3.1.4 этим
статусом не начинается.

Коммит:

`Этап 3.1.3: унифицированы термины, размерности и денежные знаки Hybrid Split Big`.

### 3.1.4. Полная проверка трёх законов

Подтверждённый статус Этапа 3.1.4:

```text
STAGE_3_1_4_STATUS=CLOSED
NEXT_ALLOWED_STAGE=3.1.5
CORRECTION_BASE_COMMIT=d10ebe3fad63edc5325933a5daf0bb21db18c28f
PREVIOUS_VALIDATED_EVIDENCE_COMMIT=ac2a43e294464498ed27acc3aadc14471b4ba927
STAGE_3_1_5_STARTED=NO
AWAITING_USER_APPROVAL=YES
```

Три закона прошли symbolic, broker-normalized, money, pointwise, event, rounding
и finite checks. Это не изменяет production logic и не начинает Этап 3.1.5.

Должны быть повторно доказаны:

1. Reserve Catch-Up:
   `FinalReserveShare * (C + T - S) > F` как необходимая лотовая база и level-by-level money proof как обязательный production gate.
2. RecoveryPL:
   `C + T - S - F > 0` как аналитический slope и point-by-point broker-money monotonicity как production gate.
3. Compression:
   `0 < N < F`, `NextBigGross < OldFar`, `GrossNext < GrossOld`, `RiskNext < RiskOld`, bounded `q < 1` и строгая broker-rounded конечность.

Должны быть отдельно описаны случаи, когда лотовая формула проходит, а money/margin/worst-case gate отклоняет план.

Коммит:

`Этап 3.1.4: перепроверены и формализованы три закона Hybrid Split Big`.

### 3.1.5. Нормативная денежная модель

Необходимо утвердить:

- `OrderCalcProfit` как источник projected money;
- actual deals как источник realized money;
- BUY-close=Bid, SELL-close=Ask;
- commission/swap/fee/slippage/spread allocation;
- запрет двойного учёта;
- формулы RecoveryPLCloseNow;
- FinalReserve как tagged subset realized profit;
- PartialFarBudget, Carry, TransitionBudget и residual;
- exactly-once event keys.

Коммит:

`Этап 3.1.5: утверждена единая денежная модель и запрет двойного учёта`.

### 3.1.6. Нормативная геометрия Big и Small

Зафиксировать:

- точную последовательность Initial Lock → Far;
- Big open geometry;
- Big Harvest operations;
- Small Transition operations;
- что именно может стать NewFar;
- запрет BigTrend/SmallBase/legacy-tail как NewFar;
- revalidation после каждого irreversible action;
- terminal-safe маршруты.

Коммит:

`Этап 3.1.6: утверждена нормативная геометрия Big Harvest и Small Transition`.

### 3.1.7. Утверждение профиля параметров

Нужно разделить:

- mathematical proof profiles;
- diagnostic profiles;
- production candidate;
- запрещённые/экспериментальные профили.

Нельзя автоматически заменить фактический профиль рекомендацией. Выбор production candidate требует отдельного подтверждения пользователя.

Коммит:

`Этап 3.1.7: разделены доказательные и рабочие профили параметров Hybrid Split Big`.

### 3.1.8. Создание единственного нормативного мануала

Создать или полностью переписать один документ, который является единственным источником истины. Все остальные документы должны либо ссылаться на него, либо быть помечены как supporting/historical.

Рекомендуемое имя:

`Docs/HYBRID_SPLIT_BIG_NORMATIVE_SPECIFICATION_RU.md`.

Коммит:

`Этап 3.1.8: создана единая нормативная спецификация Hybrid Split Big`.

## Критерий готовности этапа 3.1

- нет открытых противоречий без явной пометки;
- все формулы имеют размерности;
- различены analytic и broker-money proof;
- определены все state transitions;
- определён единый параметрический профиль либо список решений пользователя;
- создан итоговый отчёт;
- пользователь подтвердил переход.

## Итоговый отчёт

`Docs/STAGE_3_1_DOCUMENTATION_CONSOLIDATION_REPORT_RU.md`.

---

# Этап 3.2. Трассировка «норма → код → тест»

## Цель

Для каждого нормативного требования определить точную функцию MQL5, поле состояния, persisted ledger и тест.

## Пункты

1. Создать requirement IDs для всех законов, gates и execution contracts.
2. Построить таблицу `Requirement → Docs → MQL5 → Python → MQL5 test → Runtime evidence`.
3. Найти требования без реализации.
4. Найти код без нормативного основания.
5. Найти тесты, которые проверяют не ту формулу.
6. Запретить объявление требования закрытым без evidence.

Коммиты: отдельный коммит на каждый пункт с номером `Этап 3.2.x`.

Критерий готовности: 100% обязательных требований имеют mapping и статус.

Переход только после подтверждения пользователя.

---

# Этап 3.3. Исправление pre-open Decision Engine

## Цель

До открытия первой Hybrid-корзины доказать её допустимость во всех обязательных сценариях.

## Пункты

1. Устранить конфликтующие geometry mode flags.
2. Встроить обязательный point-by-point broker-money RecoveryPL gate.
3. Реализовать полный finite catch-up Base/Worst contract.
4. Реализовать реальный money-based RiskOld/RiskNext.
5. Реализовать настоящий Final Close preview gate.
6. Реализовать broker-valid minimum-safe NewFar Solver.
7. Реализовать Future Small с утверждённой глубиной.
8. Реализовать future margin, risk, gross, finite catch-up и worst-case.
9. Создать immutable Candidate Plan с fingerprint/revision.
10. Запретить любое открытие при неполном gate mask.

Критерий готовности: Candidate Allowed возможен только при полном наборе нормативных PASS.

Переход только после подтверждения пользователя.

---

# Этап 3.4. Единый persisted money ledger

## Цель

Исключить потерю, повторное начисление и неявный источник денег.

## Пункты

1. `RealizedCyclePL` по Symbol+Magic+CycleID+identifier.
2. `FinalReserveReal` как tagged subset, не дополнительная прибыль.
3. `PartialFarBudgetAvailable/Consumed`.
4. `CarryAvailable/Consumed`.
5. `TransitionBudgetAvailable/Consumed`.
6. `UnallocatedResidual`.
7. Event key и exactly-once.
8. Rebuild ledger from history.
9. Reserve mismatch и double-count detection.
10. Cumulative transition loss limits.

Критерий готовности: ledger полностью восстанавливается после restart и совпадает с deal history в tolerance.

Переход только после подтверждения пользователя.

---

# Этап 3.5. Big Harvest production execution

## Цель

Реализовать безопасное исполнение Big-сценария строго по immutable plan.

## Пункты

1. Revalidate positions, prices, costs, state revision.
2. Close BigCore, BigTrend, SmallBase по утверждённому порядку.
3. Получить actual deal net.
4. Выполнить allocation transaction ровно один раз.
5. Рассчитать partial Far только из PartialFarBudget.
6. Verify actual Far remain.
7. Проверить Final Close.
8. Либо создать следующий уровень, либо safe route.
9. Обработать partial fill/reject/slippage deviation.
10. Сохранить полный execution trace.

Критерий готовности: ни один шаг не продолжает plan после mismatch без reconciliation.

Переход только после подтверждения пользователя.

---

# Этап 3.6. Small Transition production execution

## Цель

Безопасно закрыть старый цикл и создать ровно один меньший NewFar.

## Нормативный порядок

`SmallBase close → OldFar close → BigTrend close → staged BigCore close → actual remain verify → next preview → NewFar promote`.

## Пункты

1. Re-solve на актуальных ценах.
2. Persist immutable transition plan.
3. Проверять actual result после каждого deal.
4. Запретить переход к следующему действию при mismatch.
5. Убедиться, что только остаток BigCore становится NewFar.
6. Проверить `0 < N < F` после actual rounding/fills.
7. Проверить NextBig/Gross/Risk/Margin.
8. Проверить новый finite catch-up и Future Small.
9. Создать следующий цикл либо terminal-safe route.
10. Проверить restart на каждой фазе.

Критерий готовности: ни OldFar, ни BigTrend, ни SmallBase не остаются скрытыми хвостами; существует ровно один NewFar.

Переход только после подтверждения пользователя.

---

# Этап 3.7. Reconciliation, persistence и terminal-safe protocol

## Цель

Обеспечить безопасное восстановление после restart, disconnect, partial execution и ручного вмешательства.

## Пункты

1. Persist state revision, plan phase, identifiers, ledger.
2. Rebuild positions by Symbol+Magic+CycleID+identifier.
3. Detect orphan/missing/duplicate positions.
4. Detect duplicate event application.
5. Разрешённые действия в terminal-safe state.
6. Запрет новых открытий в error/terminal state.
7. Manual intervention report.
8. Clean start policy.
9. Multi-symbol isolation.
10. Chaos tests restart после каждого transaction phase.

Критерий готовности: после любого перезапуска состояние либо однозначно восстанавливается, либо блокируется безопасно.

Переход только после подтверждения пользователя.

---

# Этап 3.8. MQL5 compile и статическая валидация

## Пункты

1. MetaEditor compile `0 errors / 0 warnings`.
2. Проверка include graph.
3. Проверка unused/dead paths.
4. Проверка enum/state completeness.
5. Проверка no implicit conversions по money/lot/identifier.
6. Проверка всех reason codes.
7. Обновление BUILD_INFO.
8. Сохранение compile evidence в `Docs`.

Критерий готовности: воспроизводимая компиляция итогового commit SHA.

Переход только после подтверждения пользователя.

---

# Этап 3.9. Oracle parity: Python ↔ MQL5

## Цель

Одинаковые входы должны давать одинаковые решения, деньги, объёмы и reason codes.

## Пункты

1. Единые JSON/CSV test vectors.
2. Valid, reject, rounding, min-lot, money, margin, worst-case cases.
3. Big finite catch-up sequence.
4. Small transition sequence.
5. Restart/exactly-once cases.
6. Допуски money/price/lot.
7. Автоматический parity report.

Критерий готовности: 100% обязательных тест-векторов совпадают в пределах утверждённых tolerance.

Переход только после подтверждения пользователя.

---

# Этап 3.10. Strategy Tester functional validation

## Пункты

1. Initial Lock и исключение Initial Profit.
2. Big scenario на уровнях L1…Lmax.
3. Reserve catch-up.
4. Partial Far без Reserve.
5. Small transition.
6. Несколько reversals до terminal volume.
7. Far BUY и Far SELL.
8. Spread, commission, swap, slippage.
9. Margin limit.
10. Max levels/reverse limits.
11. Restart and recovery fixtures.
12. Multi-symbol + Magic isolation.

Критерий готовности: отсутствуют нарушения инвариантов, unexplained money mismatch и orphan positions.

Переход только после подтверждения пользователя.

---

# Этап 3.11. Stress, adversarial и длительные тесты

## Пункты

- gaps;
- spread expansion;
- rejected orders;
- partial fills;
- delayed deals;
- swap over several days;
- min lot and coarse lot step;
- high volatility;
- trend without pullback;
- repeated reversals;
- low free margin;
- terminal-safe activation;
- random restart points;
- long multi-symbol simulation.

Критерий готовности: система не нарушает money ledger, identity, one-Far и no-open-after-error invariants.

Переход только после подтверждения пользователя.

---

# Этап 3.12. Оптимизация параметров без изменения логики

Выполняется только после доказательства правильности алгоритма.

## Пункты

1. Определить допустимую область параметров из трёх законов.
2. Исключить математически невалидные комбинации.
3. Оптимизировать как единую систему, а не независимые inputs.
4. Отдельно оценить return, drawdown, margin, reverse count, final close rate.
5. Walk-forward и out-of-sample.
6. Проверка устойчивости соседних параметров.
7. Выбрать conservative production candidate.

Запрещено автоматически применять найденный профиль без подтверждения пользователя.

Переход только после подтверждения пользователя.

---

# Этап 3.13. Demo forward test

## Пункты

1. Ограниченный список символов.
2. Минимальный lot.
3. Полное логирование.
4. Сверка actual deals с projected model.
5. Ежедневный ledger reconciliation.
6. Анализ всех rejects и terminal states.
7. Минимально достаточный объём завершённых циклов.
8. Отсутствие ручного скрытого исправления результатов.

Критерий готовности: длительный demo forward test без P0/P1 нарушений.

Переход только после подтверждения пользователя.

---

# Этап 3.14. Shadow/limited real-money readiness

## Пункты

1. Отдельный approved symbol list.
2. Минимальный StartLot.
3. Жёсткий MaxDrawdown.
4. Жёсткий MaxMarginPercent.
5. Max one active Hybrid cycle per symbol.
6. Daily loss and emergency stop.
7. Manual kill switch.
8. Automatic terminal-safe notification.
9. Backup and recovery procedure.
10. Предварительный real-money checklist.

Даже после завершения этапа включение реальной торговли требует отдельного явного подтверждения пользователя.

---

# Этап 3.15. Ограниченная реальная торговля

Первый real-money запуск допускается только после подтверждения пользователя и только с утверждёнными ограничениями.

Любое нарушение money ledger, identity, Recovery monotonicity, margin, risk, partial execution или persistence немедленно возвращает проект к соответствующему предыдущему этапу.

---

# 5. Обязательный формат отчёта каждого пункта

Каждый отчёт программиста должен содержать:

1. Номер этапа и пункта.
2. Цель.
3. Проверенные файлы.
4. Изменённые файлы.
5. Нормативные требования.
6. Формулы и размерности.
7. Реализацию.
8. Тесты.
9. Фактические результаты.
10. Найденные замечания.
11. Неустранённые риски.
12. Статус: `PASS`, `PARTIAL`, `BLOCKED`, `REJECTED`.
13. Commit SHA.
14. Условие перехода.
15. Строку: `Ожидается подтверждение пользователя для перехода к следующему пункту/этапу`.

---

# 6. Правила коммитов

Примеры допустимых сообщений:

- `Этап 3.1.1: проведена инвентаризация документации Hybrid Split Big`
- `Этап 3.3.4: реализован денежный RiskOld/RiskNext с контрольной ценой`
- `Этап 3.6.3: добавлена остановка Small Transition при partial execution`

Недопустимы сообщения:

- `fix`;
- `update`;
- `changes`;
- `готово`;
- сообщения без номера этапа;
- объединение нескольких независимых пунктов в один непрозрачный коммит.

---

# 7. Текущий выполненный этап

## Этап 3.0 — создан управляющий журнал проекта

Статус: `ВЫПОЛНЕНО`.

Выполнено:

- зафиксирована граница работ;
- определён текущий статус;
- установлен главный приоритет;
- составлен полный поэтапный план до ограниченной реальной торговли;
- определены критерии перехода;
- установлено обязательное подтверждение пользователя;
- установлен формат отчётов и коммитов.

Этот этап не изменяет торговую логику.

---

# 8. Следующий этап по плану

## Этап 3.1 — нормативная консолидация документации Hybrid Split Big

Первый пункт:

`Этап 3.1.1 — полная инвентаризация, классификация и определение приоритета всех документов в Docs`.

Начинать этап 3.1 разрешается только после подтверждения пользователя.

---

# 9. Финальный контрольный принцип

Документация определяет математику.

Математика определяет обязательные gates.

Gates определяют допустимый код.

Код подтверждается тестами.

Тесты подтверждаются runtime evidence.

Реальная торговля допускается только после прохождения всей цепочки и отдельного подтверждения пользователя.

---

# Статус после Этапа 3.1.5

```text
STAGE_3_1_4_STATUS=CLOSED
STAGE_3_1_5_STATUS=CLOSED
STATIC_NORMATIVE_MONEY_MODEL=PASS
PRODUCTION_MQL5_MAPPING=PARTIAL
EXACT_MT5_RUNTIME_EXECUTION=NOT_PROVEN_BY_STAGE_3_1_5
REAL_TRADING_ALLOWED=NO
NEXT_ALLOWED_STAGE=3.1.6
STAGE_3_1_6_STARTED=NO
AWAITING_USER_APPROVAL=YES
```

Этап 3.1.6 не начат; требуется отдельное разрешение пользователя.

## Коррекция 3.1.5.20

`PREVIOUS_STAGE_3_1_5_PASS=SUPERSEDED`; `STAGE_3_1_5_STATUS=REOPENED_FOR_CORRECTION`;
`NEXT_ALLOWED_STAGE=NONE`; `STAGE_3_1_6_STARTED=NO`; `REAL_TRADING_ALLOWED=NO`.
