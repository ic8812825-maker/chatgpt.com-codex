# Детальный отчёт аудита и тестирования ALE (`Experts/VirtualPanel/right/ale`)

## 1) Объём работ

Выполнены доработки **строго по правой ALE-части** и её тестовому контуру:

- `Experts/VirtualPanel/right/ale/*`
- `Experts/VirtualPanel/right/tests/*`

Цели: повысить надёжность, детерминизм, проверяемость dual-flow BUY/SELL, добавить инфраструктуру behavioral regression.

---

## 2) Что реализовано

## P0 — Критическая надёжность

### 2.1 NaN/Inf guards в runtime-пайплайне

В `CALFlowEngine::Process` добавлены stage-guard проверки с принудительным SAFE fallback:

- Stage `Geometry` (grid levels, pnl, net_delta)
- Stage `Exposure` (exposure, gamma, convexity)
- Stage `Risk` (worst_dd, margin)
- Stage `Math` (k_growth, mu_forward, p_ret, mu_crit, lot_opt, ev, cf)

При невалидном значении:

- логируется причина,
- форсируется SAFE (`ForceSAFE()`),
- поток прерывает текущий шаг обработки.

Это покрывает оба потока, потому что `CALStreamEngine` используется и для BUY, и для SELL.

### 2.2 Конфигурируемые runtime-инварианты

Расширен `CALRiskConfig`:

- `MAX_POSITIONS`
- `MIN_LOT`
- `ENABLE_STRICT_RUNTIME_CHECKS`

Параметры синхронизированы через canonical/alias поля и прокинуты в `CALPositionBook`.

### 2.3 Управляемая строгость проверок в PositionBook

В `CALPositionBook` добавлено:

- `SetStrictRuntimeChecks(bool)`
- применение лимитов из конфига через `SetLimits(...)`
- инварианты + rollback для mutation операций (`Add/Edit/Remove`).

Теперь есть режимы:

- strict=true: пост-проверки инвариантов обязательны;
- strict=false: допускается облегчённый режим (инварианты пропускаются).

---

## P1 — Поддерживаемость и расширение

### 2.4 CSV экспорт + machine-readable XML

Добавлен `core/CALExportHelper.mqh`:

- экспорт replay-контекста в `ale_replay_context.csv` (step-by-step `CALContext`);
- экспорт позиций BUY/SELL в CSV;
- экспорт JUnit-style summary XML (`ExportJUnitXML`) для CI/DevOps.

`ale/tests/RunAllTests.mq5` теперь формирует `ale_runner_junit.xml` после выполнения suite.

### 2.5 Required state-trace matcher

В `CALDeterministicRunner` добавлено:

- `CALStateTraceExpectation`;
- `ReplayWithExpectedTrace(...)`.

Функция сравнивает фактический timeline состояний BUY/SELL на каждом шаге с ожидаемым массивом состояний.

---

## P2 — Функциональное развитие

### 2.6 Новый сценарий replay: V-shape

В `CALDeterministicRunner` добавлен сценарий:

- `ALE_REPLAY_VSHAPE`.

Сценарий генерирует падение до pivot и обратное восстановление.

### 2.7 Расширение unit-набора

В `TestALE.mqh` добавлены:

- `TestALE_ReplayScenario_VShape`
- `TestALE_StateTraceMatcher`
- `TestALE_CSVExports`

Обновлены раннеры:

- `right/tests/RunAllTests.mqh`
- `right/ale/tests/RunAllTests.mqh`

---

## 3) Детальные результаты тестов

### 3.1 ALE unit-tests (targeted)

Команда:

- `pytest -q Experts/VirtualPanel/right/tests`

Результат:

- **26 passed**

Покрытие включает:

- dual-flow wiring;
- risk-config wiring;
- strict/global SAFE semantics;
- NaN/Inf guard stages presence;
- configurable invariants fields;
- V-shape/state-trace/export hooks;
- include/structure/signature integrity.

### 3.2 Repository smoke

Команда:

- `pytest -q`

Результат:

- **26 passed**

### 3.3 Репозиторная верификация

Команда:

- `bash verify-all.sh work`

Результат:

- Выполнено успешно.
- Синхронизация с remote проверена.
- Предупреждения только ожидаемые (optional probe files в самом verify-script).

---

## 4) Ключевые выводы по качеству

1. **Надёжность выросла на runtime уровне**: невалидные числа теперь не “просачиваются” дальше в FSM/риск-модель.
2. **Dual-flow сохранён**: защитные проверки работают симметрично для BUY и SELL, без перекрёстного загрязнения.
3. **Тестируемость улучшена**: появился state-trace matcher для deterministic regression.
4. **DevOps readiness**: есть XML summary и CSV timeline артефакты для анализа прогонов.

---

## 5) Улучшения и предложения (следующий шаг)

### P0+ (рекомендуется сразу)

1. Добавить отдельный negative-test для intentional NaN injection через тестовый double/mock слой математики.
2. Вынести названия guard stage/metric в enum-константы (уменьшит риск опечаток в логах).
3. Добавить счётчик guard-triggered SAFE в `CALContext` (для телеметрии стабильности).

### P1+

4. Экспортировать не только финальный XML suite, но и per-testcase breakdown в JUnit (`<testcase>` на каждую ALE-проверку).
5. Сделать версионируемый формат CSV (`schema_version`) для надёжного последующего парсинга.

### P2+

6. Добавить replay-сценарии `flat` и `spike` как отдельные enum-ветки (с явной проверкой SAFE/event trace).
7. Реализовать compare-runner (baseline vs current) для автоматической регрессии по state timeline.

---

## 6) Практический итог

Текущая версия ALE в `right/ale` стала существенно более предсказуемой и проверяемой:

- есть runtime NaN/Inf fail-safe;
- есть конфигурируемая строгость инвариантов;
- есть deterministic replay + state trace matching;
- есть CSV/XML артефакты для CI и аудита;
- unit/pytest контур расширен и стабилен.
