# ALE Audit Report — Separate BUY/SELL brains + COMMON brain

## 1. Scope

Реализация и проверка выполнены для:

- `Experts/VirtualPanel/right/ale/*`
- `Experts/VirtualPanel/right/tests/*`

Цель: сделать ALE как три координируемых мозга:

1. `BUY brain` — полностью независимые вычисления BUY.
2. `SELL brain` — полностью независимые вычисления SELL.
3. `COMMON brain` — агрегирование BUY+SELL и global SAFE анализ.

---

## 2. Что реализовано по ТЗ

## 2.1 Этап 1 — разделение потоков

Добавлены независимые ядра:

- `core/CALEngineBuy.mqh`
- `core/CALEngineSell.mqh`

Оба мозга:

- инициализируют собственный поток;
- держат собственный FSM/SAFE/risk/exposure path;
- получают свой `CALRiskConfig`;
- обрабатывают тик изолированно;
- не читают контекст противоположного потока.

Это обеспечивает реальную dual-flow изоляцию на уровне brain-модулей.

## 2.2 Этап 2 — общий мозг

Добавлен агрегатор:

- `core/CALEngineCommon.mqh`

Функции common brain:

- агрегирует BUY/SELL: `net_delta`, `pnl`, `exposure`, `margin`, `worst_dd`;
- считает global SAFE по комбинации:
  - локальные SAFE-флаги потоков,
  - aggregate margin limit,
  - aggregate drawdown limit;
- поддерживает собственный FSM (`state_common`).

## 2.3 Этап 3 — FSM и события

Обновлён `CALEvent`:

- добавлен `ALE_EVENT_STATE_CHANGE_COMMON`;
- добавлен обработчик `OnStateChangeCommon(...)`.

Обновлён orchestrator `CALEngine`:

- синхронизирует состояния/контексты BUY/SELL/COMMON;
- генерирует события `OnStateChangeBuy`, `OnStateChangeSell`, `OnStateChangeCommon`, `OnSAFETriggered`, `OnDrawdownExceeded`.

## 2.4 Этап 4 — интеграция через интерфейс

`IALEngine` расширен read-only API для UI:

- состояния: `StateBuy()`, `StateSell()`, `StateCommon()`;
- агрегаты: `NetDeltaCommon()`, `PnLCommon()`, `ExposureCommon()`, `MarginCommon()`, `WorstDDCommon()`, `SAFECommon()`;
- общий read-only контекст: `Context()`.

---

## 3. P0/P1/P2 улучшения, сохранённые и интегрированные

## P0

- NaN/Inf guard asserts в `CALFlowEngine::Process` (Geometry/Exposure/Risk/Math).
- Configurable runtime invariants через `CALRiskConfig`:
  - `MAX_POSITIONS`,
  - `MIN_LOT`,
  - `ENABLE_STRICT_RUNTIME_CHECKS`.
- `CALPositionBook` использует эти настройки и rollback-поведение на мутациях.

## P1

- `CALExportHelper` экспортирует:
  - timeline `CALContext` в CSV,
  - позиции BUY/SELL в CSV,
  - JUnit-style XML summary.
- `CALDeterministicRunner` поддерживает state-trace matcher (`ReplayWithExpectedTrace`).

## P2

- Добавлен replay сценарий `ALE_REPLAY_VSHAPE`.
- Расширены unit-тесты по V-shape/trace/export.

---

## 4. Unit testing — детальные результаты

### 4.1 Команды

1. `pytest -q Experts/VirtualPanel/right/tests`
2. `pytest -q`
3. `bash verify-all.sh ale_separate_brains`

### 4.2 Фактические результаты

- Targeted suite: **28 passed**.
- Full suite: **28 passed**.
- Repository verify: **PASS** (с ожидаемыми warning по optional probe files).

### 4.3 Зафиксированный файл результатов

Сформирован подробный файл:

- `Experts/VirtualPanel/right/ale/tests/UnitTestResults_ALE.txt`

Файл содержит:

- список групп проверок;
- pass/fail статус по ключевым требованиям;
- отдельный раздел по dual-flow изоляции и common-агрегации.

---

## 5. Ключевые выводы

1. **Изоляция потоков усилилась архитектурно**: BUY и SELL вычисляются отдельными brain-модулями.
2. **COMMON brain централизует кросс-поточный анализ** без нарушения независимости локальных расчётов.
3. **FSM-модель стала полнее**: теперь явное состояние common-мозга и соответствующие события.
4. **Тестируемость заметно выросла**: unit-сетка покрывает split brains, агрегацию и экспортные артефакты.

---

## 6. Улучшения и предложения (следующий шаг)

### P0+ (критически полезно)

1. Добавить property-based генератор ценовых траекторий (помимо фиксированных сценариев),
   чтобы искать нестабильные edge-case комбинации.
2. Добавить счётчики guard-triggered SAFE отдельно для BUY/SELL/COMMON в контекст.
3. Добавить hard-assert на неизменность чужого контекста при локальной обработке brain-модуля.

### P1+

4. Расширить JUnit XML до per-testcase granular output.
5. Добавить schema-version и checksum для CSV-артефактов.
6. Добавить markdown summary generator из `UnitTestResults_ALE.txt` для release-нот.

### P2+

7. Добавить сценарии `flat`, `spike`, `gap` и mandatory expected state trace для каждого.
8. Добавить сравнение baseline vs current (regression delta) по:
   - state timeline,
   - SAFE trigger points,
   - aggregated risk metrics.

---

## 7. Итог

Текущая версия ALE в `right/ale` соответствует целевому направлению “отдельные мозги BUY/SELL + общий мозг COMMON”,
имеет рабочий unit-контур с успешным прогоном и готова к следующему шагу углублённой поведенческой валидации.
