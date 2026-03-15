# ALE (Adaptive Lock Expansion) — полное описание текущей реализации проекта

> Область анализа: `Experts/VirtualPanel/right`.
> Этот документ фиксирует **что уже реализовано в коде на текущий момент** и какие формулы/инварианты реально присутствуют.

## 1) Назначение и архитектурная идея

ALE реализован как двухпоточная система (BUY/SELL) с изоляцией потоков и общей оркестрацией в `CALEngine`.

- Поток BUY и поток SELL ведутся раздельно, каждый со своим состоянием, позицией, риском, SAFE-флагом.
- Итоговые метрики агрегируются линейно:
  - `NetDeltaTotal = buy.net_delta + sell.net_delta`
  - `NetExposureTotal = buy.exposure + sell.exposure`
  - `TotalPnL = buy.pnl + sell.pnl`
- SAFE-режим имеет высший приоритет: локальный SAFE любого потока и глобальные лимиты могут принудительно перевести систему в защитное состояние.

---

## 2) Слои и ключевые компоненты

## 2.1 Core (оркестрация и lifecycle)

### `CALContext`
Содержит состояние обоих потоков:
- `state`, `net_delta`, `pnl`, `exposure`, `worst_dd`, `margin`, `gamma`, `convexity`, `safe_active`.
- Агрегаторы total-метрик (`NetDeltaTotal`, `NetExposureTotal`, `TotalPnL`).

### `CALStateMachine`
Реализован FSM со state-моделью:
`IDLE -> BASE -> EXPANSION -> HARVEST -> RESET`, плюс доминирующий `SAFE`.

Логика:
- Матрица разрешённых переходов задана явно.
- Любой переход в `SAFE` разрешён.
- Из `SAFE` запрещено идти куда-либо, кроме `RESET`.
- При запрещённом переходе FSM принудительно уходит в `SAFE`.

### `CALStreamEngine` (`CALFlowEngine.mqh`)
Это «двигатель потока» (используется и для BUY, и для SELL).

Pipeline в `Process(price)`:
1. Проверка SAFE.
2. Построение геометрии сетки.
3. Пересчёт позиций/PnL/дельты.
4. Пересчёт exposure/gamma/convexity.
5. Расчёт risk-report (dd/margin/probability/stress/SAFE).
6. Расчёт оптимизационных величин (`k`, lot, levels, EV и т.д.).
7. FSM-переход по сигналам (price move / drawdown exceeded / harvest).

### `CALEngine`
Верхний оркестратор:
- Держит `CBuyEngine`, `CSellEngine`, объединённый `CALContext`, события `CALEvent`, `CALRiskConfig`.
- На каждом тике:
  - вызывает `Process` обоих потоков,
  - выполняет `CheckGlobalSAFE`,
  - при необходимости вызывает `Harvest(ALE_HARVEST_FULL)` (форс SAFE в обоих потоках),
  - обновляет события state-change/SAFE/DD exceed.

Глобальные SAFE-условия:
- хотя бы один поток `safe_active == true`;
- `buy.margin + sell.margin > global_margin_limit`;
- `buy.worst_dd + sell.worst_dd > 2 * dd_max * initial_equity`.

### `CALDeterministicRunner`
Служебный deterministic-раннер для regression:
- хранит конфиг;
- даёт `Reset()` + `Run(prices[], n)`;
- при первом запуске seed-ит обе стороны виртуальными позициями;
- предоставляет `ContextBuy()`, `ContextSell()`, `Context()`.

---

## 2.2 Config

### `CALRiskConfig`
Реализован централизованный риск-конфиг со значениями по умолчанию и строгой валидацией.

Базовые параметры:
- ограничения риска: `dd_max`, `stress_limit`, `dd_prob_limit`, `global_margin_limit`;
- SAFE-фаза: `alpha`, `beta`, `gamma`, `k`;
- рынок/модель: `sigma`, `dt`;
- капитал/рост: `initial_equity`, `growth_g`;
- ограничения среды: `min_margin_level`, `atr_limit`, `spread_limit`, `p_safe`;
- money/risk: `risk_fraction`, `grid_step_R`, `harvest_target`, `cluster_target`.

Критический guardrail:
- в `IsValid()` проверяется `stability = k * growth_g` и требуется `0 < stability < 1`.

---

## 2.3 Geometry

### `CALFixedStep`
Линейная сетка:
- уровень: `level[i] = center + direction * step * (i+1)`
- лот: `lot[i] = 0.01 * (i+1)`

### `CALLogGeometry`
Логарифмически расширяющаяся сетка:
- дистанция уровня: `dist_i = step * (base^(i+1) - 1)`
- уровень: `level[i] = center + direction * dist_i`
- лот: `lot[i] = 0.01 * base^(0.5*i)`

### `CALGridBuilder`
Адаптер над `IALGeometry`: валидирует входы и делегирует построение активной геометрии.

---

## 2.4 Positions

### `CALVirtualPosition`
Формула PnL:
- BUY: `(bid - price_open) * lot * contract_size`
- SELL: `(price_open - ask) * lot * contract_size`

### `CALPositionBook`
Реализовано:
- add позиции;
- перерасчёт PnL;
- `TotalPnL`, `TotalLot`, `TotalAbsLot`, `Delta`, `PnLAtPrice`.

Ключевая формула:
- `PnLAtPrice = Σ lot_i * direction_i * (p - price_i) * contract_size`

### `CALDeltaTracker`
- `CalculateNetDelta(book, direction)`:
  - BUY: `+|Delta(book)|`
  - SELL: `-|Delta(book)|`
- `CalculateTailSlope = Delta(book) / dp`.

### `CALLotModel`
Лот-эскалация и ограничения:
- `LotAtLevel(level) = base_lot * alpha^level`, где `alpha ∈ [0.5, 0.85]`.
- `CumulativeMaxVolume = base_lot / (1 - alpha)`.
- `CanAddLevel`: `current_cum + next_lot <= vmax`.
- `HedgeLot = min(l0 * k, max_safe_volume)`.

---

## 2.5 Exposure

### `CALDeltaSurface`
- `DeltaFromBook = book.Delta()`.
- Сигнальная модель:
  - BUY: `+1` если `price >= center`, иначе `-1`.
  - SELL: знак противоположный BUY.

### `CALGammaProfile`
- `gamma = |(delta_right - delta_left) / dp|`.

### `CALConvexityAnalyzer`
- `convexity = gamma * |delta|` (для BUY и SELL одинаково).

### `CALExposureFlow`
Вычисляет:
- `exposure = TotalAbsLot * price`
- `pnl = PnLAtPrice(price)`
- `delta_surface`, `gamma_profile`, `convexity`.

---

## 2.6 Risk

### `CALMarginModel`
Маржа строго монотонна по модулю лота:
- `MarginFromLots = |lot| * contract_size * margin_rate`
- `margin_rate = 1/leverage` (если leverage > 0, иначе 1)

### `CALWorstCase`
Closed-form worst DD на концах линейного сегмента:
- `DD = max(-pnl_min, -pnl_max)`

### `CALDrawdownModel`
- `Drawdown = max(0, (peak - equity) / peak)`

### `CALSafeMode`
Фазовый триггер SAFE:
- `f = alpha*margin + beta*dd + gamma*|delta| + max(0, -gamma_value) - k`
- SAFE если `f > 0`

Доп. триггеры SAFE:
- `margin_level < min_margin`
- `drawdown > max_dd`
- `atr > atr_limit`
- `spread > spread_limit`
- `p_return < p_safe`

### `CALRiskEngine`
Возвращает `CALRiskReport`:
- `worst_dd`, `margin`, `dd_probability`, `stress_ratio`, `safe_triggered`.

Что считает в `Evaluate(...)`:
1. Базовый DD: `max(0, -ctx.pnl)`.
2. Маржа по стороне (BUY/SELL).
3. Worst-case на сценарном интервале цен `[0.9*price, 1.1*price]`:
   - `pnl_min = ctx.pnl + DeltaSurface*(p_min - price)`
   - `pnl_max = ctx.pnl + DeltaSurface*(p_max - price)`
   - `dd_wc = WorstCase(pnl_min, pnl_max)`
4. `dd_probability = HitLevelGBM(price, p_min, mu=0, sigma)`.
5. `stress_ratio = worst_dd / (equity * dd_max)`.
6. Композитный SAFE-флаг на основе:
   - stress limit;
   - `dd_probability` лимита;
   - абсолютного DD лимита;
   - `EvaluatePhase(...)`;
   - `EvaluateTriggers(...)`;
   - фазовой неустойчивости (`PHASE_EXPLOSIVE`/`!IsStable`).

Формула безопасного стартового лота:
- `SafeL0 = equity * clamp(risk_fraction, 0.01..0.05) / (R * (k + alpha/(1-alpha)^2))`
- где `alpha = clamp(growth_g, 0.5..0.85)`, `R = grid_step_R`.

---

## 2.7 Math

### `CALPhaseDiagram`
- Индекс устойчивости: `theta = k * g`.
- Фазы:
  - `theta < 0.9` -> `STABLE`
  - `0.9 <= theta < 1.0` -> `MARGINAL`
  - `theta >= 1.0` -> `EXPLOSIVE`
- Волатильностный предел:
  - `StabilityLimit(sigma) = exp(-sigma^2 / 2)`
- Устойчивость:
  - `IsStable <=> k*g < exp(-sigma^2/2)`

### `CALCriticalMu`
- `mu_crit = 0.5*sigma^2 + k`

### `CALReturnProbability`
- Доцентровая вероятность (гауссово затухание):
  - `z = |distance|/(sigma + 1e-8)`
  - `P = exp(-0.5*z^2)`
- Вероятность касания уровня в GBM (упрощённая closed form):
  - при `mu≈0`: `P = l/p`
  - иначе: `P = exp( clamp( -(2*mu/sigma^2)*ln(p/l), -60..20 ) )`

### `CALGBMModel`
- Forward:
  - `S(t)=S0*exp((mu-0.5*sigma^2)*t)`
- Monte Carlo:
  - дискретный шаг GBM с псевдо-`z` из LCG;
  - возвращает долю траекторий `S_T >= target`.

### `CALClosedForm`
- `ExpectedPnL = p_return*gain - (1-p_return)*loss`

---

## 2.8 Optimization

### `CALOptimalK`
- Кандидат: `candidate = max(0.1, target/(sigma+1e-6))`.
- Если не стабилен, `k` зажимается к границе устойчивости:
  - `k_safe = max(0.05, 0.99*StabilityLimit(sigma)/alpha)`.

### `CALLotOptimizer`
- `raw = base_lot * max(0.1, 1 - risk_factor)`.
- Если фаза стабильна -> `raw`, иначе ограничение `min(raw, base_lot)`.

### `CALGridOptimizer`
- Если нестабильно: `levels = max(1, base_levels-1)`.
- Если стабильно: `levels = max(1, base_levels + round(volatility))`.

### `CALExpectationModel`
- Для BUY/SELL используется единая closed-form из `CALClosedForm`.

---

## 3) Контракты интерфейсов

Реализованы интерфейсы:
- `IALEngine` (инициализация, update, доступ к метрикам и context).
- `IALRiskModel` (расчёт DD + SAFE-триггер).
- `IALGeometry` (build grid, доступ к level/lot).
- `IALExposureModel` (recalculate/exposure/delta/gamma).
- `IFSM` (current/transition).
- `IMarketAdapter` (Bid/Ask/Spread/ATR/MarginRequired/TickValue).

Это задаёт стабильную API-границу между слоями.

---

## 4) Что уже проверяется тестами

В `right/tests` есть 5 наборов:

1. **`TestALE.mqh`** — интеграция dual-flow + FSM legality + численный derivative oracle.
2. **`TestALERegression.mqh`** — regression-оракулы на фиксированных сценариях (trend up/down, oscillation, flash crash, replay/reset determinism).
3. **`TestGeometry.mqh`** — симметрия BUY/SELL сеток, равномерность шага, рост лог-геометрии.
4. **`TestRisk.mqh`** — monotonic margin, worst-dd формулы, risk-report sanity.
5. **`TestALEContracts.mqh`** — контрактные проверки SAFE-bypass, additivity, phase guard.

Примеры формул, зафиксированных тестами:
- sizing: `lot = (equity * risk_fraction)/(stop_points * tick_value)`;
- численная производная PnL по цене совпадает с дельтой (`~0.1` в оракуле);
- spread-инвариант `Ask-Bid = 0.0003` у мок-адаптера;
- запрет `SAFE -> EXPANSION`.

---

## 5) Что реализовано частично / в зачатке

Несмотря на широкую архитектуру, часть вычислений пока интегрирована как scaffolding:

- В `CALStreamEngine::Process` некоторые оптимизационные величины (`lot_opt`, `hedge_lot`, `levels_opt`, `ev`, `cf`, `mu_crit`) пока не меняют динамику (вклад умножен на `0.0`) — то есть они вычисляются и готовы к подключению, но не влияют на контекст прямо сейчас.
- `Harvest(ALE_HARVEST_PARTIAL)` объявлен, но фактически действует только `FULL` (принудительный SAFE обоих потоков).
- Функционал уже математически и архитектурно разложен на слои, но часть доменной логики включена как контрактная «рамка под расширение».

---

## 6) Краткий итог по зрелости текущего состояния

Проект ALE в `right` уже содержит:

- полноценный **каркас production-архитектуры** (core/risk/math/geometry/exposure/optimization/interfaces/tests);
- реализацию **двухпоточной модели BUY/SELL** с аддитивными агрегатами;
- **SAFE-first дизайн** (локальные и глобальные триггеры);
- формализованные **фазовые критерии устойчивости** (`theta=k*g`, `exp(-sigma^2/2)`);
- набор **регрессионных и контрактных тестов**, фиксирующих ключевые инварианты.

То есть это уже не «черновик интерфейсов», а рабочий архитектурно-математический фундамент ALE, где основные формулы реализованы и закреплены тестовыми оракулами, а следующий этап — усиление реальной исполнительной логики на основе уже рассчитанных оптимизационных сигналов.
