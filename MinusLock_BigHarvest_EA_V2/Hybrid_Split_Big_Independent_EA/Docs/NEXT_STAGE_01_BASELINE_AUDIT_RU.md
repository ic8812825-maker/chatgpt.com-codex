# Этап 1 — исходное состояние и карта проекта

## Протокол снимка
```text
EXECUTION_MODE=GITHUB_API
BASE_SHA=9309e0b11745d4499f875ecd5744a68c1f7d2ea7
LOCAL_WORKTREE_STATUS=NOT_APPLICABLE
REMOTE_BASELINE_VERIFIED=YES
GIT_TREE_TRUNCATED=false
STAGE_01_TESTS=NOT_RUN
```
Снимок получен через GitHub Git refs/commit/recursive tree до каких-либо записей в рамках этого задания. Ветка `refs/heads/work` указывала на BASE_SHA; корневой tree коммита: `a2f091e7543a17ab9c8e6393ef01ece46567c943`. Рекурсивный ответ содержит 2631 записей по репозиторию, `truncated=false`; разрешённый каталог существует. Проверка локального рабочего дерева не выполнялась и не подменяется удалённым снимком. До подготовки этого отчёта изменений в репозиторий данным исполнением не вносилось.

## Инвентаризация разрешённого каталога
В снимке 1013 blob-файлов: `Docs/` — 87, `Include/` — 81, `Tests/` — 667, `Reports/` — 171, по одному в `Logs/` и `Sets/`, пять файлов в корне каталога. Количества включают служебные файлы и исторические артефакты; это не количество исполняемых тестов.

Корень: `Hybrid_Split_Big_Independent_EA.mq5`, `README_RU.md`, `BUILD_INFO.md`, `CHANGELOG_RU.md`, `PROJECT_MAP_RU.md`. Основной MQ5-файл прочитан: `OnInit` устанавливает disabled runtime policy, `OnTick` вызывает `HSBI_SubmitActionStub()`, `OnTimer` обновляет диагностический снимок. Это наблюдение по исходнику, а не результат компиляции или доказательство отсутствия всех путей отправки ордеров.

### Карта исходников
- `Include/Core/`: контекст, идентификаторы, роли, FSM, инварианты, runtime policy и типы.
- `Include/Money/`: broker money/margin, cost, level/basket/candidate evaluators, proof identity, reserve allocation/catch-up и ledger types. Для этапа 2 основной объект — `HSBI_BasketMoneyEvaluator.mqh`; связанные контракты — `Docs/24_BROKER_MONEY_MODEL_RU.md`, `Docs/31_MONEY_PROOF_IDENTITY_RU.md`, `Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md`.
- `Include/Planning/`: broker grid, control prices, geometry, future small и New Far solver/candidate. Для этапа 3 — `HSBI_NewFarSolver.mqh`, `HSBI_NewFarCandidate.mqh`, `Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md`, `Docs/28_NEW_FAR_SOLVER_RU.md`, `Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md`.
- `Include/Risk/`: risk gates, future-small и New Far gate types.
- `Include/Execution/`: intent, preflight, outcome, ownership, transaction types и no-trade stub.
- `Include/Persistence/`: execution journal, snapshot, reconciliation и persistence contracts.
- `Include/Runtime/`: decision/restart validators и transaction barrier.
- `Include/Scenarios/`: контракты Initial Lock, Big Harvest, Partial Far, Small Transition, Final Close.
- `Include/Diagnostics/`: logger, diagnostics, panel model.

### Карта проверок и доказательств
`Tests/Contracts/` содержит JSON-контракты и регистры; `Tests/Vectors/` — golden, boundary, negative, historical и causal fixtures; `Tests/Reference/` — Python reference/economic/identity/provenance models и adapters; `Tests/Static/` — verifiers, regressions, mutation, adversarial и acceptance scripts; `Tests/MQL5/` — MQL5 harness; `Tests/Evidence/` — сохранённые результаты предыдущих ревизий; `Tests/StrategyTester/` — каталог для тестера. `Reports/` содержит исторические отчёты. Сохранённые PASS и evidence не являются свежим запуском для BASE_SHA.

## Нормативная и историческая граница
Документы `Docs/00–32` содержат charter, glossary, роли, математическую/геометрическую модели, FSM, execution, ledger, сценарии, solver, risk, persistence, traceability, testing, readiness и decisions. `README_RU.md`, `BUILD_INFO.md`, `PROJECT_MAP_RU.md` содержат последовательные исторические статусные блоки; старые PASS/READY и superseded нельзя автоматически считать актуальным разрешением на реализацию или торговлю. Необходимо отдельно сверять действующий decision registry, последнюю ревизию и source of truth.

## Предварительные зоны независимого аудита (не выводы о дефектах)
1. Money: разделить projected и actual money, проверять единицы измерения, цены закрытия Bid/Ask, spread/commission/swap, исключение первоначального lock profit, неповторное зачисление allocation, reserve только для разрешённого назначения и точное тождество RecoveryPL.
2. New Far: проверить направление, допустимую сетку объёма/цены, единственность Far, catch-up, objective/tiebreak, broker margin и fail-closed поведение.
3. Проверки: независимо пересчитывать expected results; выявлять self-confirming oracle, исторический false PASS, подмену версии и отсутствие привязки evidence к SHA.

## Ограничения доказательств и дальнейший порядок
```text
METAEDITOR_COMPILE=NOT_RUN
MQL5_TESTS=NOT_RUN
PYTHON_TESTS=NOT_RUN
STRATEGY_TESTER=NOT_RUN
BROKER_RUNTIME_PROOF=NOT_RUN
FULL_ECONOMIC_CORRECTNESS=NOT_PROVEN
MODEL_CHANGES_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```
Этап 1 является только инвентаризацией, без правок экономической модели или production logic. Далее: этап 2 — формулы Money; этап 3 — New Far; этап 4 — независимые тесты с честным NOT_RUN, если нет исполняющей среды; этап 5 — только минимальные доказанные исправления с отдельным разрешением при затрагивании утверждённой модели; этап 6 — false-PASS; этап 7 — итоговый отчёт. Перед каждой записью — повторная проверка remote HEAD, единственный commit на этап, non-force fast-forward с expected SHA и проверка changed files.
