# ALE_IMPLEMENTATION_GUIDE.md
## Пошаговое руководство реализации `right/ale`

Версия: 1.0

---

## 1. Назначение

Документ определяет, как реализовывать и расширять ALE по слоям:
- какие классы должны существовать,
- какие методы обязательны,
- какие зависимости допустимы/запрещены,
- как не нарушить `ALE_ARCHITECTURE_LOCK.md`.

Это руководство для разработчика, работающего в `Experts/VirtualPanel/right/ale/`.

---

## 2. Общие правила реализации

1. Потоки BUY/SELL полностью изолированы.
2. `CALEngine` — только оркестратор и агрегатор.
3. Math-layer — чистые функции, без бизнес-состояния.
4. SAFE имеет приоритет над расширением.
5. Любой новый модуль должен быть покрыт тестами контракта/регрессии.

---

## 3. Структура каталогов и ответственность

### 3.1 `core/`
Ответственность:
- управление жизненным циклом потоков,
- FSM,
- orchestration,
- deterministic runner.

Ключевые файлы:
- `CALContext.mqh`
- `CALStateMachine.mqh`
- `CALFlowEngine.mqh`
- `CALEngine.mqh`
- `CALDeterministicRunner.mqh`

### 3.2 `config/`
- `CALRiskConfig.mqh`: параметры риска/стабильности, `IsValid()` guardrails.

### 3.3 `geometry/`
- построение сеток и уровней;
- никаких зависимостей на risk/fsm.

### 3.4 `positions/`
- виртуальные позиции;
- PnL/lot/delta bookkeeping.

### 3.5 `exposure/`
- расчёт delta/gamma/convexity поверх позиции.

### 3.6 `risk/`
- drawdown/margin/worst-case/SAFE decisions;
- использует math, но не зависит от UI.

### 3.7 `math/`
- чистые вычисления: phase/GBM/probability/closed-form.

### 3.8 `optimization/`
- подбор параметров в допустимой (не EXPLOSIVE) области.

### 3.9 `interfaces/`
- стабильные контракты API.

### 3.10 `tests/`
- contract tests + regression + risk/geometry/integration.

---

## 4. Порядок реализации нового функционала

Рекомендуемый порядок:
1. Зафиксировать математику в `math/*.md`.
2. Добавить/обновить интерфейс в `interfaces/`.
3. Реализовать math-модуль (если нужен).
4. Реализовать слой `risk`/`exposure`/`positions`.
5. Интегрировать в `CALFlowEngine`.
6. Обновить оркестрацию в `CALEngine` (если требуется).
7. Добавить тесты в `tests/`.

---

## 5. Обязательные классы и методы

## 5.1 Core

### `CALContext`
Должен содержать stream-local контексты BUY/SELL и агрегаты.

### `CALStateMachine`
Обязательные методы:
- `Transition(next_state)`
- `TransitionBySignal(signal)`
- `Current()`

### `CALFlowEngine`
Обязательные методы:
- `Init(direction, config)`
- `Process(price)`
- `AddVirtual(price, lot)`
- `BuildGrid(center, levels, out_grid)`
- `Context()`
- `ForceSAFE()`

### `CALEngine`
Обязательные методы:
- `SetRiskConfig(config)`
- `Init()`
- `OnPriceUpdate(price)`
- `Context()`
- read-only API (`NetDeltaBuy`, `NetDeltaSell`, ...)

### `CALDeterministicRunner`
Обязательные методы:
- `SetConfig(config)`
- `Run(prices[], n)`
- `Reset()`
- `ContextBuy()` / `ContextSell()`

---

## 5.2 Config

### `CALRiskConfig`
Обязательные поля:
- `dd_max`, `stress_limit`, `dd_prob_limit`, `global_margin_limit`
- `alpha`, `beta`, `gamma`, `k`
- `sigma`, `dt`, `initial_equity`, `growth_g`

Обязательные методы:
- `SetDefaults()`
- `IsValid()`

---

## 5.3 Math

### `CALPhaseDiagram`
Обязательные методы:
- `StabilityIndex(k,g)`
- `DetectPhase(k,g)`
- `StabilityLimit(sigma)`
- `IsStable(k,g,sigma)`

### `CALGBMModel`
- forward/step аналитика GBM.

### `CALReturnProbability`
- вероятностные функции без side effects.

---

## 5.4 Risk

### `CALRiskEngine`
Обязательные методы:
- `Init(direction, config)`
- `Evaluate(...) -> CALRiskReport`

`CALRiskReport` минимум:
- `worst_dd`
- `margin`
- `dd_probability`
- `stress_ratio`
- `safe_triggered`

### `CALSafeMode`
- `Evaluate(...)`
- SAFE threshold logic.

---

## 5.5 Optimization

### `CALOptimalK`
- `FindBuy(...)`
- `FindSell(...)`

### `CALGridOptimizer`
- `OptimizeLevelsBuy(...)`
- `OptimizeLevelsSell(...)`

### `CALLotOptimizer`
- `OptimizeBuy(...)`
- `OptimizeSell(...)`

Обязательное правило: оптимизация исключает EXPLOSIVE-параметры через `CALPhaseDiagram`.

---

## 6. Допустимые зависимости

Матрица допустимых зависимостей:

| Слой | Может зависеть от |
|------|--------------------|
| math | (никого) |
| geometry | math, config |
| positions | geometry, config |
| exposure | positions, math |
| risk | exposure, math, config |
| optimization | math, risk, config |
| core | все слои через контракты |

Запрещено:
- `math -> risk/core`;
- `risk -> core UI`;
- cross-stream mutable dependencies.

---

## 7. Псевдокод тика

```text
function StreamTick(stream, price):
  grid      = stream.geometry.BuildGrid(price)
  positions = stream.positions.Update(price, grid)
  exposure  = stream.exposure.Calculate(positions, price)
  report    = stream.risk.Evaluate(exposure, positions, config)

  if report.safe_triggered:
      stream.state = SAFE
  else:
      stream.state = stream.fsm.TransitionBySignal(...)

  stream.optimization.Update(report, config)
  return stream.context
```

---

## 8. Правила добавления нового файла

Для любого нового `*.mqh` в `right/ale`:
1. Определить слой (`math/risk/...`).
2. Проверить допустимые зависимости.
3. Добавить include-guard.
4. Добавить unit/contract test.
5. Обновить документы formal-spec при изменении контракта.

---

## 9. Тестовые требования

Минимальный набор тестов после изменений:
- `TestALE`
- `TestALEContracts`
- `TestALERegression`
- `TestRisk`
- `TestGeometry`

При изменении фазы/устойчивости дополнительно:
- сценарии `TestPhaseDiagramGuard`;
- проверки SAFE non-bypass.

---

## 10. Антипаттерны (запрещено)

1. Общий mutable `PositionBook` для BUY/SELL.
2. Общий mutable `RiskEngine` для BUY/SELL.
3. Прямые cross-stream вызовы в `CALFlowEngine`.
4. Изменение состояния из UI-слоя.
5. Бизнес-логика в `math/`.

---

## 11. Чеклист перед merge

1. `CALRiskConfig::IsValid()` не нарушен.
2. `CALPhaseDiagram` правила фазы неизменны.
3. SAFE блокирует Add/Build/Expand.
4. Аддитивность `Total = Buy + Sell` сохранена.
5. Детерминированный reset/replay воспроизводим.
6. Контрактные тесты проходят.

---

## 12. Инженерная политика изменений

Если изменение затрагивает:
- фазовую математику,
- инварианты I1–I8,
- SAFE-политику,
- изоляцию потоков,

то обязательно обновить:
- `ALE_FORMAL_SPEC.md`
- `ALE_INVARIANTS.md`
- `ALE_RISK_PROOF.md`
- `ALE_MONTE_CARLO_SPEC.md`
- `ALE_ARCHITECTURE_LOCK.md`
- этот `ALE_IMPLEMENTATION_GUIDE.md`

---

## 13. Итог

Этот документ — пошаговый операционный стандарт разработки `right/ale`.

Главный принцип:

> Сначала математический контракт, затем реализация, затем контрактные тесты.

