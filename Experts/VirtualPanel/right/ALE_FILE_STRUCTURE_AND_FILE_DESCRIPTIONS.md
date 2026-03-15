# ALE (`Experts/VirtualPanel/right`) — структура папок и описание каждого файла

Документ даёт **полную карту текущего содержимого** `right`:
1) дерево папок/файлов,
2) краткое, но предметное описание **каждого файла**,
3) что уже реализовано внутри.

---

## 1. Полная структура

```text
Experts/VirtualPanel/right
├─ ale
│  ├─ ALE_ARCHITECTURE_LOCK.md
│  ├─ ALE_IMPLEMENTATION_GUIDE.md
│  ├─ ALE_PROJECT_FULL_DESCRIPTION.md
│  ├─ NEXT_STEP_PROPOSAL.md
│  ├─ config
│  │  └─ CALRiskConfig.mqh
│  ├─ core
│  │  ├─ CALContext.mqh
│  │  ├─ CALDeterministicRunner.mqh
│  │  ├─ CALEngine.mqh
│  │  ├─ CALEvent.mqh
│  │  ├─ CALFlowEngine.mqh
│  │  ├─ CALStateMachine.mqh
│  │  ├─ CBuyEngine.mqh
│  │  └─ CSellEngine.mqh
│  ├─ exposure
│  │  ├─ CALConvexityAnalyzer.mqh
│  │  ├─ CALDeltaSurface.mqh
│  │  ├─ CALExposureFlow.mqh
│  │  └─ CALGammaProfile.mqh
│  ├─ geometry
│  │  ├─ CALATRStep.mqh
│  │  ├─ CALFixedStep.mqh
│  │  ├─ CALGeometryBase.mqh
│  │  ├─ CALGridBuilder.mqh
│  │  └─ CALLogGeometry.mqh
│  ├─ interfaces
│  │  ├─ IALEngine.mqh
│  │  ├─ IALExposureModel.mqh
│  │  ├─ IALGeometry.mqh
│  │  ├─ IALRiskModel.mqh
│  │  ├─ IFSM.mqh
│  │  ├─ IGeometryEngine.mqh
│  │  └─ IMarketAdapter.mqh
│  ├─ math
│  │  ├─ ALE_FORMAL_SPEC.md
│  │  ├─ ALE_INVARIANTS.md
│  │  ├─ ALE_MONTE_CARLO_SPEC.md
│  │  ├─ ALE_PHASE_MODEL.md
│  │  ├─ ALE_RISK_PROOF.md
│  │  ├─ CALClosedForm.mqh
│  │  ├─ CALCriticalMu.mqh
│  │  ├─ CALGBMModel.mqh
│  │  ├─ CALPhaseDiagram.mqh
│  │  └─ CALReturnProbability.mqh
│  ├─ optimization
│  │  ├─ CALExpectationModel.mqh
│  │  ├─ CALGridOptimizer.mqh
│  │  ├─ CALLotOptimizer.mqh
│  │  └─ CALOptimalK.mqh
│  ├─ positions
│  │  ├─ CALDeltaTracker.mqh
│  │  ├─ CALLotModel.mqh
│  │  ├─ CALPositionBook.mqh
│  │  └─ CALVirtualPosition.mqh
│  └─ risk
│     ├─ CALDrawdownModel.mqh
│     ├─ CALMarginModel.mqh
│     ├─ CALRiskEngine.mqh
│     ├─ CALSafeMode.mqh
│     └─ CALWorstCase.mqh
└─ tests
   ├─ TestALE.mqh
   ├─ TestALEContracts.mqh
   ├─ TestALERegression.mqh
   ├─ TestGeometry.mqh
   └─ TestRisk.mqh
```

---

## 2. Описание каждого файла

## 2.1 `ale/` (архитектурные документы проекта)

- **`ale/ALE_ARCHITECTURE_LOCK.md`**  
  Архитектурный «замок»: фиксирует правила слоям, зависимости между модулями и запреты на архитектурные нарушения.

- **`ale/ALE_IMPLEMENTATION_GUIDE.md`**  
  Пошаговое руководство по реализации и расширению ALE: какие классы обязательны, в каком порядке добавлять функциональность, как не нарушить architecture lock.

- **`ale/ALE_PROJECT_FULL_DESCRIPTION.md`**  
  Подробный обзор реализованных частей ALE, формул и тестового покрытия (добавленный ранее документ общего уровня).

- **`ale/NEXT_STEP_PROPOSAL.md`**  
  Предложение следующей итерации (контрактный lock SAFE и инвариантов) + критерии приёмки и границы scope.

---

## 2.2 `ale/config`

- **`ale/config/CALRiskConfig.mqh`**  
  Центральная структура конфигурации риска/стабильности.
  Уже есть:
  - поля лимитов риска (`dd_max`, `stress_limit`, `dd_prob_limit`, `global_margin_limit`),
  - параметры SAFE-функции (`alpha`, `beta`, `gamma`, `k`),
  - рыночные параметры (`sigma`, `dt`),
  - параметры капитала (`initial_equity`, `growth_g`) и operational-limits,
  - `SetDefaults()` и строгая `IsValid()` валидация,
  - guardrail устойчивости: `k*growth_g` обязан быть в диапазоне `(0,1)`.

---

## 2.3 `ale/core`

- **`ale/core/CALContext.mqh`**  
  Базовые enum состояния/потока и контейнеры контекста:
  - `ENUM_ALE_STATE` (`IDLE/BASE/EXPANSION/HARVEST/RESET/SAFE`),
  - `ENUM_ALE_FLOW` (`BUY=1`, `SELL=-1`),
  - `CALStreamContext` (дельта, pnl, exposure, dd, margin, gamma, convexity, safe-флаг),
  - `CALContext` с агрегаторами total-метрик (`NetDeltaTotal`, `NetExposureTotal`, `TotalPnL`).

- **`ale/core/CALDeterministicRunner.mqh`**  
  Детерминированный раннер сценариев:
  - держит `CALEngine` + конфиг,
  - умеет `SetConfig`, `Run(prices[], n)`, `Reset`,
  - автоматически seed-ит BUY/SELL виртуальными позициями перед первым прогоном,
  - отдаёт кешированные `ContextBuy/ContextSell` для regression-оракулов.

- **`ale/core/CALEngine.mqh`**  
  Главный оркестратор двух потоков.
  Уже есть:
  - инициализация BUY/SELL stream-двигателей,
  - синхронизация `m_context` из двух потоков,
  - агрегаторы PnL/Delta/Exposure,
  - `CheckGlobalSAFE()` с глобальными условиями,
  - `Harvest()` (полный SAFE форс обоих потоков),
  - `OnPriceUpdate()` с обработкой SAFE/harvest/state-change событий,
  - API `BuildGrid`, `AddVirtual` и read-only доступ к метрикам.

- **`ale/core/CALEvent.mqh`**  
  Модель доменных событий ALE.
  Уже есть:
  - enum типов событий (`STATE_CHANGE_*`, `DRAWDOWN_EXCEEDED`, `SAFE_TRIGGERED`, `SAFE_TRIGGERED_GLOBAL`),
  - методы `OnStateChangeBuy/Sell`, `OnDrawdownExceeded`, `OnSAFETriggered*`,
  - хранение `from/to state` и текстового сообщения.

- **`ale/core/CALFlowEngine.mqh`**  
  Ядро потоковой обработки `CALStreamEngine`.
  Уже есть:
  - pipeline `Geometry -> Positions -> Exposure -> Risk -> Optimization -> FSM`,
  - SAFE-блокировка действий (`AddVirtual`, `BuildGrid`) при активном SAFE,
  - расчёт pnl/net_delta/exposure/gamma/convexity,
  - интеграция risk-report,
  - расчёт оптимизационных величин (`k_growth`, `hedge_lot`, `lot_opt`, `levels_opt`, `ev`, `closed-form`),
  - переходы FSM по сигналам,
  - `ForceSAFE()`.
  Примечание: часть оптимизационных величин сейчас вычисляется как scaffolding (не вносит прямой вклад в динамику).

- **`ale/core/CALStateMachine.mqh`**  
  Реализация FSM и сигналов.
  Уже есть:
  - `ENUM_ALE_SIGNAL`,
  - матрица разрешённых переходов,
  - принудительный SAFE при нелегальном переходе,
  - особое правило: из `SAFE` разрешён только `RESET`,
  - `TransitionBySignal()` для основных бизнес-сигналов.

- **`ale/core/CBuyEngine.mqh`**  
  Тонкий обёрточный файл: подключает `CALFlowEngine.mqh`; `CBuyEngine` фактически определяется в нём и наследует `CALStreamEngine` с направлением BUY.

- **`ale/core/CSellEngine.mqh`**  
  Аналогично `CBuyEngine.mqh`: обёртка над тем же движком; `CSellEngine` задаётся через направление SELL.

---

## 2.4 `ale/exposure`

- **`ale/exposure/CALConvexityAnalyzer.mqh`**  
  Простейшая модель convexity: `convexity = gamma * abs(delta)` (и для BUY, и для SELL).

- **`ale/exposure/CALDeltaSurface.mqh`**  
  Модель дельта-поверхности.
  Уже есть:
  - `DeltaFromBook(book)`,
  - вспомогательные сигнальные функции `DeltaForBuy/DeltaForSell` относительно центра.

- **`ale/exposure/CALExposureFlow.mqh`**  
  Оркестратор метрик экспозиции потока.
  Уже есть:
  - `Init(direction)` и `Recalculate(book, price)`,
  - вычисления `exposure`, `pnl`, `delta_surface`, `gamma_profile`, `convexity`,
  - интерфейсные геттеры (`Exposure`, `DeltaSurface`, `GammaProfile`, `Convexity`, `PnL`).

- **`ale/exposure/CALGammaProfile.mqh`**  
  Расчёт гаммы как модуль конечной разности: `|(delta_right-delta_left)/dp|`.

---

## 2.5 `ale/geometry`

- **`ale/geometry/CALATRStep.mqh`**  
  Геометрия сетки с шагом от ATR.
  Уже есть:
  - `SetATR()` с fallback на дефолт,
  - построение уровней `center + direction*step*(i+1)`,
  - рост лотов по уровням (`0.01*(1+0.5*i)`).

- **`ale/geometry/CALFixedStep.mqh`**  
  Линейная фиксированная геометрия.
  Уже есть:
  - конфигурация шага,
  - построение равномерной сетки уровней,
  - линейный профиль лотов (`0.01*(i+1)`).

- **`ale/geometry/CALGeometryBase.mqh`**  
  Базовый класс для геометрий.
  Уже есть:
  - `m_step`, `SetStep`,
  - безопасные accessor-методы `LevelPrice()` и `Lot()` с проверкой индексов.

- **`ale/geometry/CALGridBuilder.mqh`**  
  Обёртка/делегатор над `IALGeometry`.
  Уже есть:
  - `SetGeometry(...)`,
  - `BuildGrid(...)` с проверками `NULL` и `levels>0`.

- **`ale/geometry/CALLogGeometry.mqh`**  
  Логарифмически расширяющаяся геометрия.
  Уже есть:
  - параметр базы `base>1`,
  - нелинейная дистанция уровней,
  - степенной профиль лотов.

---

## 2.6 `ale/interfaces`

- **`ale/interfaces/IALEngine.mqh`**  
  Контракт главного движка (Init, OnPriceUpdate, метрики BUY/SELL, доступ к общему контексту).

- **`ale/interfaces/IALExposureModel.mqh`**  
  Контракт модели экспозиции (Recalculate, Exposure, DeltaSurface, GammaProfile).

- **`ale/interfaces/IALGeometry.mqh`**  
  Контракт геометрии + структура `CALGrid` (массивы уровней и лотов).

- **`ale/interfaces/IALRiskModel.mqh`**  
  Контракт риск-модели (`CalculateDD`, `SAFE`).

- **`ale/interfaces/IFSM.mqh`**  
  Контракт FSM (`Current`, `Transition`).

- **`ale/interfaces/IGeometryEngine.mqh`**  
  Дополнительный абстрактный контракт геометрического движка (`NextDistance`, `ExpansionVolume`).

- **`ale/interfaces/IMarketAdapter.mqh`**  
  Контракт рыночного адаптера (`Bid/Ask/Spread/ATR/MarginRequired/TickValue`) для отвязки доменной логики от источника котировок.

---

## 2.7 `ale/math` (формальные модели и вычислительные модули)

### Документы

- **`ale/math/ALE_FORMAL_SPEC.md`**  
  Формальная спецификация модели ALE (термины, ограничения, связь компонентов).

- **`ale/math/ALE_INVARIANTS.md`**  
  Набор инвариантов системы (state/risk/additivity/determinism и др.).

- **`ale/math/ALE_MONTE_CARLO_SPEC.md`**  
  Описание MC-постановки для проверки вероятностных свойств и stress-поведения.

- **`ale/math/ALE_PHASE_MODEL.md`**  
  Описание фазовой модели устойчивости (`theta = k*g`) и зон stable/marginal/explosive.

- **`ale/math/ALE_RISK_PROOF.md`**  
  Математические обоснования риск-ограничений и SAFE-доминантности.

### Код

- **`ale/math/CALClosedForm.mqh`**  
  Closed-form ожидания PnL: `E = p_return*gain - (1-p_return)*loss`.

- **`ale/math/CALCriticalMu.mqh`**  
  Критическая `mu`-оценка: `mu_crit = 0.5*sigma^2 + k`.

- **`ale/math/CALGBMModel.mqh`**  
  GBM-утилиты:
  - аналитический `Forward(...)`,
  - Monte Carlo-оценка вероятности достижения цели,
  - внутренний LCG-генератор для воспроизводимого псевдо-шума.

- **`ale/math/CALPhaseDiagram.mqh`**  
  Фазовая диаграмма устойчивости:
  - `StabilityIndex(k,g)=k*g`,
  - `DetectPhase` (`<0.9`, `<1`, `>=1`),
  - `StabilityLimit(sigma)=exp(-sigma^2/2)`,
  - `IsStable(k,g,sigma)`.
  Также есть вспомогательные функции критической DD-границы.

- **`ale/math/CALReturnProbability.mqh`**  
  Вероятностные функции:
  - `ToCenter(distance,sigma)` как гауссово затухание,
  - `HitLevelGBM(...)` для вероятности касания уровня (с клиппингом экспоненты).

---

## 2.8 `ale/optimization`

- **`ale/optimization/CALExpectationModel.mqh`**  
  Обёртка над `CALClosedForm` для оценки ожидания (BUY/SELL).

- **`ale/optimization/CALGridOptimizer.mqh`**  
  Оптимизатор числа уровней сетки с проверкой стабильности фазы.

- **`ale/optimization/CALLotOptimizer.mqh`**  
  Оптимизатор лота по risk-factor и устойчивости фазы.

- **`ale/optimization/CALOptimalK.mqh`**  
  Подбор `k` с «стабилизацией» относительно фазовой границы; также содержит `HedgeLot(...)`.

---

## 2.9 `ale/positions`

- **`ale/positions/CALDeltaTracker.mqh`**  
  Расчёт net-delta и tail-slope по `CALPositionBook`.

- **`ale/positions/CALLotModel.mqh`**  
  Модель лотов/эскалации.
  Уже есть:
  - безопасный диапазон `alpha`,
  - `LotAtLevel`,
  - `CumulativeMaxVolume`,
  - `CanAddLevel`,
  - `HedgeLot`,
  - алиасы `LotForBuyLevel/LotForSellLevel`.

- **`ale/positions/CALPositionBook.mqh`**  
  Книга виртуальных позиций.
  Уже есть:
  - хранение массива `CALVirtualPosition`,
  - `Add`, `Recalc`, `Size`,
  - `TotalPnL`, `TotalLot`, `TotalAbsLot`,
  - `PnLAtPrice`, `Delta`.

- **`ale/positions/CALVirtualPosition.mqh`**  
  Структура одной виртуальной позиции + формула обновления PnL по bid/ask и направлению.

---

## 2.10 `ale/risk`

- **`ale/risk/CALDrawdownModel.mqh`**  
  Нормированный drawdown: `max(0, (peak-equity)/peak)`.

- **`ale/risk/CALMarginModel.mqh`**  
  Модель маржи:
  - `MarginFromLots = |lot|*contract_size*margin_rate`,
  - `MarginBuy/MarginSell` через `1/leverage`.

- **`ale/risk/CALRiskEngine.mqh`**  
  Главный риск-движок.
  Уже есть:
  - `CALRiskReport` (`worst_dd`, `margin`, `dd_probability`, `stress_ratio`, `safe_triggered`),
  - интеграция `CALWorstCase`, `CALMarginModel`, `CALDrawdownModel`, `CALSafeMode`, `CALReturnProbability`, `CALPhaseDiagram`,
  - `SafeL0(equity)` формула,
  - `Evaluate(...)` с composite SAFE-решением.

- **`ale/risk/CALSafeMode.mqh`**  
  SAFE-логика:
  - фазовая функция `f(alpha,beta,gamma,k, margin, dd, delta, gamma_value)`,
  - trigger-check по margin level, drawdown, ATR, spread и вероятности возврата,
  - `TriggerBuy/TriggerSell`.

- **`ale/risk/CALWorstCase.mqh`**  
  Worst-case drawdown по endpoint-модели: `max(-pnl_min, -pnl_max)` + методы `EvaluateBuy/Sell`.

---

## 2.11 `tests`

- **`tests/TestALE.mqh`**  
  Интеграционный тест dual-flow:
  - проверка аддитивности агрегатов,
  - численный derivative oracle,
  - легальность SAFE-переходов FSM,
  - базовые edge-case формулы.

- **`tests/TestALEContracts.mqh`**  
  Контрактные тесты:
  - phase guard (`k*g >= 1`),
  - SAFE non-bypass (запрет Add/Grid в SAFE),
  - additivity контракт по контексту.

- **`tests/TestALERegression.mqh`**  
  Регрессионные оракулы:
  - фиксированные сценарии цены,
  - replay/reset детерминизм,
  - finite-checks,
  - проверка инвариантов spread/derivative/SAFE legality.

- **`tests/TestGeometry.mqh`**  
  Геометрические проверки:
  - BUY/SELL симметрия сеток,
  - консистентность шага,
  - expected growth для log-геометрии.

- **`tests/TestRisk.mqh`**  
  Риск-проверки:
  - монотонность маржи,
  - формула worst drawdown,
  - sanity-проверки risk-report и `SafeL0`.

---

## 3. Быстрый вывод о текущем состоянии

В `Experts/VirtualPanel/right` уже реализован полный каркас ALE:
- документы формальной и архитектурной фиксации,
- разделение на слои (`core/config/geometry/positions/exposure/risk/math/optimization/interfaces`),
- отдельный тестовый пакет для контрактов/регрессии/риска/геометрии.

То есть структура проекта уже зрелая и расширяемая: основные доменные контракты и вычислительные модули присутствуют, а часть advanced-логики оптимизации подготовлена для дальнейшего «включения» в поведение движка.
