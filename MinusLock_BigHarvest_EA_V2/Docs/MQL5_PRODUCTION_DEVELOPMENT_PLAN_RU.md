# MQL5-FIRST ПЛАН ДОВЕДЕНИЯ MINUSLOCK BIGHARVEST EA V2 ДО ПРОФЕССИОНАЛЬНОГО УРОВНЯ

## 1. Назначение документа

Этот документ фиксирует результат проверки текущей документации и production-кода советника `MinusLock_BigHarvest_EA_V2`, а также устанавливает строгую последовательность дальнейшей работы.

Главное обязательное правило:

> Вся дальнейшая разработка выполняется только как разработка, интеграция, компиляция, тестирование и доведение production-кода советника на MQL5. Python не является этапом разработки, источником готовности, доказательством production-реализации или условием перехода к реальной торговле.

Допустимые средства доказательства дальнейших этапов:

- исходный код `.mq5` и `.mqh`;
- MetaEditor compiler;
- встроенные MQL5 unit/integration test scripts;
- MQL5 Service/Script/Expert test harness внутри этого проекта;
- MT5 Strategy Tester;
- визуальный режим Strategy Tester;
- журнал Experts/Journal;
- история orders/deals/positions;
- MQL5 CSV/JSON evidence, сформированные самим советником или MQL5 test harness;
- demo forward test;
- ограниченный real-money shadow/production режим после отдельного разрешения пользователя.

Запрещено считать Python-модель доказательством того, что production-код советника корректно работает в MetaTrader 5.

---

## 2. Граница работ

Все действия выполняются строго внутри:

`MinusLock_BigHarvest_EA_V2`

Запрещено:

- изменять файлы за пределами указанного каталога;
- переносить production-логику в Python;
- создавать новую торговую систему вместо реализации утверждённой документации;
- объявлять этап завершённым только по статическому наличию функций;
- включать реальную торговлю до завершения всех production-gates;
- смешивать legacy, Split Big и Hybrid Split Big без явно выбранного режима и нормативного контракта.

---

## 3. Проверенный текущий статус

### 3.1. Документация

В проекте уже существует подробная дорожная карта:

`Docs/PROJECT_STATUS_AND_REAL_TRADING_ROADMAP_RU.md`.

Она содержит правильную общую идею последовательного движения от нормативной документации к коду, persistence, Strategy Tester, stress tests, demo и ограниченной реальной торговле.

Однако дорожная карта требует корректировки по следующим причинам:

1. Она содержит отдельный этап `Python ↔ MQL5 oracle parity`.
2. Ряд последних этапов 3.1.5 был закрыт преимущественно Python-доказательствами.
3. В последних отчётах прямо указано, что production MQL5 не изменялся.
4. Наличие Python proof не доказывает MetaEditor compile, реальное исполнение заявок, broker retcodes, deal history, partial execution, restart или recovery в MT5.
5. Текущий основной документ статуса не полностью синхронизирован с последней восьмой корректирующей приёмкой 3.1.5.156.
6. Старые отчёты и доказательства не должны автоматически давать статус PASS будущему MQL5-коду.

### 3.2. Production-код

Главный эксперт:

`MinusLock_BigHarvest_EA.mq5`.

Он уже подключает значительный набор модулей:

- Config;
- Types;
- LotUtils;
- PositionUtils;
- GeometryEngine;
- TradeEngine;
- RecoveryMath;
- BrokerMoneyModel;
- Hybrid Geometry/Rounding/Transition/Catch-Up/Margin/Worst-Case/Future-Small/Decision;
- RiskManager;
- StateMachine;
- PendingContractEngine;
- PositionResolutionEngine;
- StateIntegrityEngine;
- ReconciliationEngine.

Это хорошая архитектурная база, но само наличие include-файлов не доказывает их production-связность.

### 3.3. Критические факты текущей конфигурации

В `Include/Config.mqh` по умолчанию:

- `UseLegacySingleBigGeometry = true`;
- `UseSplitBigGeometry = false`;
- `UseHybridSplitBigGeometry = false`;
- `AllowRealTrading = false`;
- `UseInternalSimulation = false`.

При этом `IsInternalSimulationMode()` возвращает `UseInternalSimulation || !AllowRealTrading`. Следовательно, при стандартном `AllowRealTrading=false` советник использует simulation path независимо от значения `UseInternalSimulation`.

Это должно быть переработано в явный, однозначный и безопасный runtime-mode contract. Нельзя допускать, чтобы флаг разрешения реальной торговли одновременно неявно выбирал архитектурный движок исполнения.

### 3.4. Текущий вердикт

Текущий проект нельзя считать готовым к реальному счёту.

Фактическое состояние:

`СИЛЬНАЯ ДОКУМЕНТАЦИОННАЯ И МАТЕМАТИЧЕСКАЯ БАЗА + ЧАСТИЧНАЯ MQL5-АРХИТЕКТУРА, НО PRODUCTION-INTEGRATION, METAEDITOR COMPILE, MT5 RUNTIME И REAL-ACCOUNT SAFETY НЕ ДОКАЗАНЫ`.

Следующий допустимый этап по существующей последовательности — `3.1.6`, но его необходимо выполнять уже в MQL5-first режиме.

---

# 4. Обязательная последовательность дальнейшей работы

Ни один этап нельзя менять местами. Переход разрешён только после PASS предыдущего этапа и отдельного подтверждения пользователя.

---

# ЭТАП A. ЗАВЕРШЕНИЕ НОРМАТИВНОЙ БАЗЫ ПЕРЕД ИЗМЕНЕНИЕМ ТОРГОВОГО КОДА

## A.1. Этап 3.1.6 — нормативная геометрия Big и Small

### Цель

Зафиксировать одну точную production-последовательность действий, которую должен реализовать MQL5-код.

### Обязательные результаты

1. Полная последовательность Initial Lock.
2. Закрытие плюсовой стартовой позиции.
3. Явное правило полного исключения initial profit из Recovery.
4. Присвоение оставшейся минусовой позиции роли Far.
5. Big open geometry.
6. Роли BigCore, BigTrend и SmallBase.
7. Big Harvest close order.
8. Источник PartialFarBudget.
9. Запрет использования FinalReserve для partial Far.
10. Immediate Final Close gate с `RecoveryPL > 0`.
11. Small Transition close order.
12. Единственный допустимый источник NewFar.
13. Запрет BigTrend, SmallBase, old Far и foreign position как NewFar.
14. Правила actual-volume verification после каждого закрытия.
15. Safe/terminal маршруты при reject, partial fill, disconnect и mismatch.

### MQL5 mapping

Для каждого действия указать:

- функцию `.mqh`;
- входное состояние;
- preconditions;
- irreversible trade action;
- expected deal;
- persisted phase;
- postconditions;
- reason code;
- recovery route.

### Критерий PASS

Ни одна операция Big/Small не имеет двух противоречащих трактовок.

---

## A.2. Этап 3.1.7 — утверждение production-профиля параметров

### Цель

Разделить параметры на:

- legacy;
- Split Big;
- Hybrid Split Big;
- diagnostic;
- test-only;
- production-candidate;
- запрещённые.

### Обязательные изменения документации

1. Установить один production-candidate profile.
2. Не включать его в код автоматически до завершения MQL5-проверок.
3. Определить допустимые диапазоны всех ratio.
4. Зафиксировать инварианты сумм долей.
5. Зафиксировать ограничения после broker rounding.
6. Удалить неоднозначность между `BigRatio/SmallRatio` и `BigCoreRatio/BigTrendRatio/SmallBaseToFarRatio`.
7. Определить, какие legacy-inputs игнорируются в Hybrid mode.

### Критерий PASS

Каждый input имеет единственное назначение в каждом runtime mode.

---

## A.3. Этап 3.1.8 — единая нормативная спецификация

Создать окончательный `HYBRID_SPLIT_BIG_NORMATIVE_SPECIFICATION_RU.md`.

Все production-функции MQL5 должны ссылаться на requirement IDs из этой спецификации.

### Критерий PASS

Нет открытого нормативного конфликта, который влияет на сделку, деньги, объём, state или recovery.

---

# ЭТАП B. ПОЛНЫЙ MQL5 CODE AUDIT И ТРАССИРОВКА

## B.1. Инвентаризация production-кода

Проверить каждый `.mq5` и `.mqh` внутри проекта.

Для каждого файла создать таблицу:

- назначение;
- публичные функции;
- изменяемое глобальное состояние;
- торговые действия;
- persistence действия;
- dependence graph;
- нормативные requirement IDs;
- состояние реализации: `COMPLETE`, `PARTIAL`, `STUB`, `LEGACY_ONLY`, `UNREACHABLE`, `UNPROVEN`;
- риски.

## B.2. Include graph

Построить MQL5 include graph и проверить:

- циклические зависимости;
- скрытые глобальные зависимости;
- дублирование money/lot/price calculations;
- функции с одинаковым смыслом;
- legacy branches внутри Hybrid path;
- unreachable modules;
- вызовы simulation-функций из production path.

## B.3. Call graph торговых действий

Найти все вызовы:

- Buy/Sell;
- PositionClose;
- PositionClosePartial;
- OrderSend;
- HistorySelect;
- HistoryDealGet*;
- PositionSelect*;
- GlobalVariable*;
- FileOpen/FileWrite;
- EventSetTimer;
- OnTradeTransaction.

Для каждого вызова доказать:

- Symbol + Magic + CycleID + identifier scope;
- ticket ownership;
- idempotency;
- обработку retcode;
- сохранение phase до/после irreversible action;
- reconciliation path.

## B.4. Матрица `Норма → MQL5-код → MQL5-тест → MT5 evidence`

Python-колонка исключается из обязательного production-gate.

### Критерий PASS этапа B

100% нормативных требований имеют MQL5 owner-функцию и тестовый способ проверки.

---

# ЭТАП C. РАЗДЕЛЕНИЕ RUNTIME MODES

## C.1. Ввести явный enum режима

Например:

- `RUNTIME_DISABLED`;
- `RUNTIME_MQL5_TEST`;
- `RUNTIME_STRATEGY_TESTER`;
- `RUNTIME_DEMO`;
- `RUNTIME_REAL_LIMITED`.

`AllowRealTrading` не должен выбирать simulation engine.

## C.2. Разделить права

Отдельно определить:

- разрешение расчётов;
- разрешение формирования plan;
- разрешение market request;
- разрешение demo;
- разрешение real;
- emergency close permission.

## C.3. Fail-closed startup

OnInit обязан блокировать запуск при:

- netting account;
- неверном symbol trade mode;
- конфликтующем geometry mode;
- невалидном parameter profile;
- старой schema persistence;
- foreign managed positions;
- ambiguous state;
- невозможности прочитать history;
- несовпадении broker properties;
- отсутствии production approval token для real mode.

### Критерий PASS

Ни один test/simulation branch не может быть случайно использован на real account.

---

# ЭТАП D. ЕДИНЫЙ PRODUCTION CONTEXT И IDENTITY

## D.1. Cycle identity

Каждый цикл должен иметь:

- Symbol;
- Magic;
- CycleID;
- StateRevision;
- PlanID;
- EventID;
- PositionIdentifier;
- Role;
- ParentEventID.

## D.2. Единственный владелец состояния

Запретить разрозненное изменение глобальных полей из разных модулей.

Ввести один `RecoveryContext` и контролируемые transition-функции.

## D.3. Role registry

В каждый момент должно существовать:

- не более одного Far;
- установленное нормативом количество BigCore/BigTrend/SmallBase;
- отсутствие orphan managed positions;
- отсутствие foreign position consumption.

### Критерий PASS

Любая позиция однозначно связывается с циклом, ролью и событием открытия.

---

# ЭТАП E. MQL5 MONEY ENGINE PRODUCTION INTEGRATION

## E.1. Projected money

Все прогнозы рассчитываются через broker-native MQL5:

- `OrderCalcProfit`;
- `OrderCalcMargin`;
- SYMBOL_TRADE_TICK_SIZE;
- SYMBOL_TRADE_TICK_VALUE_PROFIT;
- SYMBOL_TRADE_TICK_VALUE_LOSS;
- Bid/Ask по стороне закрытия;
- broker volume min/max/step.

## E.2. Actual money

Источник истины после сделки — actual deal history:

- DEAL_PROFIT;
- DEAL_COMMISSION;
- DEAL_SWAP;
- DEAL_FEE;
- DEAL_ENTRY;
- DEAL_POSITION_ID;
- DEAL_VOLUME;
- DEAL_PRICE.

## E.3. Ledger

Реализовать в production MQL5:

- RealizedCycleNet;
- FinalReserveAvailable/Consumed;
- PartialFarBudgetAvailable/Consumed;
- CarryAvailable/Consumed;
- TransitionBudgetAvailable/Consumed;
- Residual;
- source-deal ownership;
- exactly-once EventKey;
- conflict detection;
- rebuild from history.

## E.4. Запрет двойного учёта

Reserve — tagged subset actual realized money, а не дополнительная прибыль.

### Критерий PASS

После restart ledger восстанавливается из MT5 history и совпадает с persisted snapshot в tolerance.

---

# ЭТАП F. PRE-OPEN DECISION ENGINE

До отправки первого ордера CandidatePlan обязан пройти все gates:

1. Identity gate.
2. Geometry gate.
3. Broker lot gate.
4. RecoveryPL point-by-point gate.
5. Reserve catch-up gate.
6. Compression gate.
7. Minimum-safe NewFar solver.
8. RiskOld/RiskNext money gate.
9. Margin gate.
10. Spread/slippage/swap/commission gate.
11. Future Small gate.
12. Finite catch-up gate.
13. Final Close preview gate.
14. Max positions gate.
15. Max levels/reverse gate.
16. Account drawdown/daily loss gate.
17. Full gate-mask completeness.

Plan должен быть immutable и содержать fingerprint broker inputs.

Перед OrderSend выполняется повторная revalidation.

### Критерий PASS

Открытие невозможно при одном отсутствующем, stale или failed gate.

---

# ЭТАП G. TRADE EXECUTION ENGINE

## G.1. Единая оболочка OrderSend

Каждый запрос обязан логировать:

- request;
- check result;
- retcode;
- deal/order;
- requested/filled volume;
- requested/actual price;
- deviation;
- filling mode;
- attempt number;
- idempotency key.

## G.2. Partial fill

Нельзя продолжать plan по requested volume. Только actual filled volume определяет следующий шаг.

## G.3. Retry policy

Разделить retcodes на:

- retryable;
- reprice/revalidate;
- reconciliation required;
- fatal/terminal-safe.

## G.4. Transaction-driven progression

State advance должен подтверждаться `OnTradeTransaction` и deal history, а не только возвратом торговой функции.

### Критерий PASS

Ни одна irreversible sequence не продолжает исполнение без подтверждённого actual result.

---

# ЭТАП H. BIG HARVEST PRODUCTION PATH

Строгая последовательность:

1. Revalidate immutable plan.
2. Persist `BIG_EXECUTION_STARTED`.
3. Закрыть нормативные Big/Small роли в утверждённом порядке.
4. Дождаться actual deals.
5. Reconcile actual net.
6. Выполнить allocation exactly once.
7. Проверить immediate Final Close.
8. Если Final Close запрещён — рассчитать partial Far только из PartialFarBudget.
9. Выполнить partial Far по Far ticket.
10. Verify Far remain.
11. Пересчитать следующий уровень.
12. Либо открыть новый basket, либо перейти в safe state.

### Обязательные инварианты

- Reserve не используется для partial Far.
- Final Close требует положительного RecoveryPL.
- Big/Small money берётся из actual closes.
- Foreign deals не финансируют цикл.
- Дубликат события не меняет деньги повторно.

---

# ЭТАП I. SMALL TRANSITION PRODUCTION PATH

Строгая последовательность определяется нормативной спецификацией, ориентировочно:

1. Re-solve на актуальных Bid/Ask.
2. Persist transition plan.
3. Close SmallBase.
4. Confirm actual deal.
5. Close OldFar.
6. Confirm actual deal.
7. Close BigTrend по нормативу.
8. Staged close BigCore.
9. Verify actual BigCore remain.
10. Доказать `0 < NewFar < OldFar` после broker rounding и fills.
11. Promote только остаток разрешённой роли в NewFar.
12. Rebuild next-cycle geometry.
13. Проверить RecoveryPL, reserve, risk, margin, finite catch-up и Future Small.
14. Persist завершение transition.

### Критерий PASS

После перехода существует ровно один новый Far; нет old Far, скрытого BigTrend tail, SmallBase tail или orphan position.

---

# ЭТАП J. PERSISTENCE И RECONCILIATION

## J.1. Write-ahead state

До irreversible action сохранять intent/phase/event key.

## J.2. Restart matrix

Проверить restart:

- до запроса;
- после запроса, до transaction;
- после partial fill;
- после deal, до allocation;
- после allocation, до state advance;
- между каждым шагом Big;
- между каждым шагом Small;
- во время Final Close;
- во время partial Far;
- при повреждённом persisted store.

## J.3. Safe outcomes

После restart система обязана либо:

- восстановить ровно одно состояние;
- завершить reconciliation;
- перейти в terminal-safe и запретить новые открытия.

### Критерий PASS

Exactly-once подтверждён MQL5 runtime-сценариями и actual MT5 history.

---

# ЭТАП K. RISK MANAGER ПРОФЕССИОНАЛЬНОГО УРОВНЯ

Реализовать и доказать:

- per-cycle risk;
- aggregate account risk;
- margin level forecast;
- max margin usage;
- max equity drawdown;
- daily loss limit;
- max active symbols;
- max managed positions;
- max cycle duration;
- max spread;
- gap protection;
- swap-duration limit;
- consecutive trade-error circuit breaker;
- emergency stop;
- manual kill switch;
- no-new-cycle mode;
- close-only mode;
- real-money hard limits compiled into approved profile.

### Критерий PASS

Ни один вход не обходит account-level и cycle-level gates.

---

# ЭТАП L. НАБЛЮДАЕМОСТЬ И АУДИТ

Добавить production diagnostics:

- machine-readable reason codes;
- state transition log;
- plan fingerprint;
- order/deal correlation;
- ledger event log;
- reconciliation report;
- periodic health snapshot;
- panel с режимом, state, Far/Big/Small, reserve, budgets, margin, drawdown и последней ошибкой;
- log throttling без потери critical events;
- MQL5-generated evidence files.

### Критерий PASS

По одному комплекту логов можно восстановить каждое решение и денежное изменение цикла.

---

# ЭТАП M. METAEDITOR COMPILE GATE

1. Compile главного EA.
2. Compile всех MQL5 test scripts.
3. `0 errors`.
4. Цель: `0 warnings`.
5. Проверить strict mode.
6. Проверить implicit conversions.
7. Проверить enum completeness.
8. Проверить include graph.
9. Проверить dead/unreachable production paths.
10. Сохранить compile log и SHA.

Без PASS этапа M Strategy Tester запрещён как приёмочное доказательство итоговой версии.

---

# ЭТАП N. ВСТРОЕННЫЕ MQL5-ТЕСТЫ

Создать MQL5 test harness внутри проекта.

Обязательные группы:

- lot normalization;
- price/tick grid;
- money signs BUY/SELL;
- commission/swap/fee;
- RecoveryPL;
- reserve catch-up;
- compression;
- NewFar solver;
- risk/margin;
- event keys;
- ledger allocation/consumption;
- duplicate/conflict events;
- persistence serialization;
- state transitions;
- reason codes;
- terminal-safe rules.

Python не участвует в критерии PASS.

---

# ЭТАП O. MT5 STRATEGY TESTER — ФУНКЦИОНАЛЬНАЯ МАТРИЦА

Проверить минимум:

1. Initial Lock BUY-profit/SELL-Far.
2. Initial Lock SELL-profit/BUY-Far.
3. Big L1…Lmax.
4. Immediate Final Close.
5. Partial Far без reserve.
6. Reserve catch-up.
7. Small transition.
8. Несколько reversals.
9. Минимальный lot.
10. Крупный lot step.
11. Spread expansion.
12. Commission.
13. Swap.
14. Slippage.
15. Gap.
16. Reject/requote.
17. Margin block.
18. Max levels.
19. Max reverse cycles.
20. Restart fixtures.
21. Multi-symbol.
22. Same Symbol, different Magic.
23. Manual foreign position.
24. Terminal-safe recovery.

Каждый тест должен иметь expected invariants и автоматический MQL5 verdict.

---

# ЭТАП P. STRESS И ДЛИТЕЛЬНЫЕ ПРОГОНЫ

- trend without pullback;
- saw/repeated reverse;
- volatility clusters;
- spread spikes;
- weekend gap;
- delayed execution;
- long swap holding;
- low free margin;
- simultaneous symbols;
- random restart phase;
- corrupted persistence;
- duplicate transaction delivery;
- long-duration millions-of-ticks run.

Критический критерий: отсутствие orphan positions, double money consumption, foreign consumption, invalid NewFar и open-after-error.

---

# ЭТАП Q. ОПТИМИЗАЦИЯ ПАРАМЕТРОВ В MT5

Только после доказательства корректности кода.

Оптимизация выполняется Strategy Tester средствами MT5, без изменения алгоритма.

Цели оцениваются совместно:

- net profit;
- equity drawdown;
- margin;
- completion rate;
- reverse count;
- time in cycle;
- final-close rate;
- terminal-safe frequency;
- parameter-neighbour stability.

Обязательны:

- in-sample;
- out-of-sample;
- walk-forward;
- разные символы;
- разные spread/commission profiles;
- conservative production candidate.

---

# ЭТАП R. DEMO FORWARD TEST

Условия:

- minimum lot;
- ограниченный symbol list;
- один цикл на символ;
- полный audit logging;
- ежедневный ledger reconciliation;
- сверка projected/actual money;
- расследование каждого reject и terminal-safe;
- запрет ручного скрытого исправления.

Выходной критерий определяется количеством полностью завершённых циклов и отсутствием P0/P1 дефектов, а не только длительностью теста.

---

# ЭТАП S. SHADOW REAL И LIMITED REAL

## S.1. Shadow real

Советник рассчитывает планы на реальном счёте, но не отправляет торговые запросы. Сравниваются broker properties, spread, margin, projected money и условия gates.

## S.2. Limited real

Только после отдельного письменного разрешения пользователя:

- minimum lot;
- один approved symbol;
- один активный цикл;
- hard daily loss;
- hard equity drawdown;
- hard margin limit;
- kill switch;
- close-only fallback;
- ежедневная ручная приёмка ledger;
- немедленный rollback к demo при любом P0/P1.

---

# 5. Приоритет первых практических задач

После утверждения этого плана последовательность первых кодовых работ должна быть такой:

1. Завершить нормативные этапы 3.1.6–3.1.8.
2. Провести полный MQL5 code inventory и mapping.
3. Исправить runtime mode contract.
4. Утвердить единый RecoveryContext и identity ownership.
5. Перенести/интегрировать normative money ledger в production MQL5.
6. Завершить pre-open Decision Engine.
7. Завершить transaction-driven TradeEngine.
8. Реализовать Big production sequence.
9. Реализовать Small production sequence.
10. Завершить persistence/reconciliation.
11. Завершить account/cycle risk manager.
12. Добавить observability.
13. Получить MetaEditor compile PASS.
14. Выполнить MQL5 tests.
15. Выполнить Strategy Tester matrix.
16. Выполнить stress tests.
17. Выполнить MT5 optimization.
18. Demo forward.
19. Shadow real.
20. Limited real после отдельного разрешения.

---

# 6. Формат каждого будущего пункта

Каждый пункт выполняется отдельным коммитом на русском языке и содержит:

1. номер этапа/пункта;
2. нормативное требование;
3. проверенные MQL5-файлы;
4. изменённые MQL5-файлы;
5. кодовую реализацию;
6. инварианты;
7. MQL5-тесты;
8. MetaEditor/Strategy Tester evidence;
9. фактические результаты;
10. нерешённые риски;
11. статус `PASS/PARTIAL/BLOCKED/REJECTED`;
12. commit SHA;
13. запрет перехода без подтверждения пользователя.

Недопустимый PASS:

- только Python tests;
- только markdown claim;
- только наличие функции;
- только grep/static counter;
- только отсутствие TODO;
- тест без MetaEditor/MT5 runtime там, где требуется торговое исполнение.

---

# 7. Итоговый вердикт

Существующий план полезен и не должен удаляться, но его production-часть необходимо считать superseded этим MQL5-first планом в части обязательного Python-oracle и Python-based acceptance.

Python-материалы могут оставаться историческими или supporting-доказательствами математики, но не являются направлением дальнейшей разработки.

Дальнейшая работа должна быть сосредоточена на:

- production MQL5 code;
- полном соответствии нормативной документации;
- broker-native money calculations;
- transaction-driven execution;
- exactly-once ledger;
- restart/reconciliation;
- MetaEditor compile;
- MQL5 tests;
- MT5 Strategy Tester;
- demo и строго ограниченной реальной торговле.

Текущий статус:

```text
PLAN_AUDIT=COMPLETE
EXISTING_ROADMAP_FOUND=YES
EXISTING_ROADMAP_MQL5_PRODUCTION_PART=REQUIRES_CORRECTION
PYTHON_AS_FUTURE_DEVELOPMENT_DIRECTION=PROHIBITED
MQL5_FIRST_PLAN=ESTABLISHED
CURRENT_NEXT_NORMATIVE_STAGE=3.1.6
PRODUCTION_MQL5_READY=NO
METAEDITOR_COMPILE_PROVEN=NO
MT5_RUNTIME_PROVEN=NO
REAL_TRADING_ALLOWED=NO
AWAITING_USER_APPROVAL_FOR_NEXT_STAGE=YES
```
