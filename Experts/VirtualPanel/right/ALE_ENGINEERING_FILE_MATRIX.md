# ALE Engineering Matrix (`Experts/VirtualPanel/right`)

Ниже — инженерная матрица по **каждому файлу**: назначение, ключевые сущности и статус реализации.

## Root docs

| Файл | Назначение | Ключевые сущности | Статус |
|---|---|---|---|
| `ale/ALE_ARCHITECTURE_LOCK.md` | Архитектурные ограничения и правила зависимостей | Layer constraints, dependency matrix | ✅ Зафиксировано |
| `ale/ALE_IMPLEMENTATION_GUIDE.md` | Гайд по порядку реализации и расширению | Mandatory classes/methods, workflow | ✅ Зафиксировано |
| `ale/ALE_PROJECT_FULL_DESCRIPTION.md` | Полное текстовое описание текущей реализации ALE | Архитектура, формулы, тесты | ✅ Добавлено |
| `ale/NEXT_STEP_PROPOSAL.md` | Предложение следующей итерации развития | Contract Lock iteration scope | ✅ Зафиксировано |

## Config

| Файл | Назначение | Ключевые сущности | Статус |
|---|---|---|---|
| `ale/config/CALRiskConfig.mqh` | Централизованный риск-конфиг и валидация | `CALRiskConfig`, `SetDefaults()`, `IsValid()` | ✅ Работает |

## Core

| Файл | Назначение | Ключевые сущности | Статус |
|---|---|---|---|
| `ale/core/CALContext.mqh` | Потоковый и агрегированный контекст системы | `ENUM_ALE_STATE`, `ENUM_ALE_FLOW`, `CALStreamContext`, `CALContext` | ✅ Работает |
| `ale/core/CALDeterministicRunner.mqh` | Детерминированный запуск сценариев для regression | `CALDeterministicRunner`, `Run()`, `Reset()`, `Context*()` | ✅ Работает |
| `ale/core/CALEngine.mqh` | Главный оркестратор BUY/SELL потоков | `CALEngine`, `OnPriceUpdate()`, `CheckGlobalSAFE()` | ✅ Работает |
| `ale/core/CALEvent.mqh` | Модель событий и сообщений ALE | `ENUM_ALE_EVENT_TYPE`, `CALEvent` | ✅ Работает |
| `ale/core/CALFlowEngine.mqh` | Ядро потокового pipeline (geo→pos→exposure→risk→opt→FSM) | `CALStreamEngine`, `CBuyEngine`, `CSellEngine` | ✅ Работает (часть opt — scaffolding) |
| `ale/core/CALStateMachine.mqh` | FSM переходы и сигналы | `ENUM_ALE_SIGNAL`, `CALStateMachine` | ✅ Работает |
| `ale/core/CBuyEngine.mqh` | Тонкая обёртка include для buy-потока | include `CALFlowEngine.mqh` | ✅ Есть |
| `ale/core/CSellEngine.mqh` | Тонкая обёртка include для sell-потока | include `CALFlowEngine.mqh` | ✅ Есть |

## Exposure

| Файл | Назначение | Ключевые сущности | Статус |
|---|---|---|---|
| `ale/exposure/CALConvexityAnalyzer.mqh` | Расчёт convexity | `ConvexityBuy()`, `ConvexitySell()` | ✅ Работает |
| `ale/exposure/CALDeltaSurface.mqh` | Delta-модель поверхности | `DeltaFromBook()`, `DeltaForBuy/Sell()` | ✅ Работает |
| `ale/exposure/CALExposureFlow.mqh` | Оркестрация exposure-метрик потока | `CALExposureFlow`, `Recalculate()` | ✅ Работает |
| `ale/exposure/CALGammaProfile.mqh` | Расчёт gamma по конечной разности | `FromDeltaSurface()` | ✅ Работает |

## Geometry

| Файл | Назначение | Ключевые сущности | Статус |
|---|---|---|---|
| `ale/geometry/CALATRStep.mqh` | ATR-based геометрия сетки | `CALATRStep`, `SetATR()`, `BuildGrid()` | ✅ Работает |
| `ale/geometry/CALFixedStep.mqh` | Геометрия с фиксированным шагом | `CALFixedStep`, `SetStep()`, `BuildGrid()` | ✅ Работает |
| `ale/geometry/CALGeometryBase.mqh` | Базовый класс геометрии | `CALGeometryBase`, `LevelPrice()`, `Lot()` | ✅ Работает |
| `ale/geometry/CALGridBuilder.mqh` | Делегатор построения сеток | `CALGridBuilder`, `SetGeometry()`, `BuildGrid()` | ✅ Работает |
| `ale/geometry/CALLogGeometry.mqh` | Логарифмическая геометрия | `CALLogGeometry`, `SetBase()`, `BuildGrid()` | ✅ Работает |

## Interfaces

| Файл | Назначение | Ключевые сущности | Статус |
|---|---|---|---|
| `ale/interfaces/IALEngine.mqh` | Контракт ALE-движка | `IALEngine` | ✅ Контракт |
| `ale/interfaces/IALExposureModel.mqh` | Контракт exposure-модуля | `IALExposureModel` | ✅ Контракт |
| `ale/interfaces/IALGeometry.mqh` | Контракт геометрии + `CALGrid` | `IALGeometry`, `CALGrid` | ✅ Контракт |
| `ale/interfaces/IALRiskModel.mqh` | Контракт risk-модуля | `IALRiskModel` | ✅ Контракт |
| `ale/interfaces/IFSM.mqh` | Контракт FSM | `IFSM` | ✅ Контракт |
| `ale/interfaces/IGeometryEngine.mqh` | Контракт геометрического движка | `IGeometryEngine` | ✅ Контракт |
| `ale/interfaces/IMarketAdapter.mqh` | Контракт рыночного адаптера | `IMarketAdapter` | ✅ Контракт |

## Math docs

| Файл | Назначение | Ключевые сущности | Статус |
|---|---|---|---|
| `ale/math/ALE_FORMAL_SPEC.md` | Формальная спецификация ALE | Формальные определения модели | ✅ Документ |
| `ale/math/ALE_INVARIANTS.md` | Инварианты системы | I1..I* invariants | ✅ Документ |
| `ale/math/ALE_MONTE_CARLO_SPEC.md` | Спецификация Monte Carlo | MC assumptions, сценарии | ✅ Документ |
| `ale/math/ALE_PHASE_MODEL.md` | Фазовая модель устойчивости | `theta=k*g`, stable/marginal/explosive | ✅ Документ |
| `ale/math/ALE_RISK_PROOF.md` | Доказательные риск-заметки | SAFE-доминантность, bounded-risk | ✅ Документ |

## Math code

| Файл | Назначение | Ключевые сущности | Статус |
|---|---|---|---|
| `ale/math/CALClosedForm.mqh` | Closed-form ожидание PnL | `ExpectedPnL()` | ✅ Работает |
| `ale/math/CALCriticalMu.mqh` | Критическая mu-функция | `Evaluate(sigma,k)` | ✅ Работает |
| `ale/math/CALGBMModel.mqh` | GBM forward + MC probability | `Forward()`, `MonteCarloReturnProb()` | ✅ Работает |
| `ale/math/CALPhaseDiagram.mqh` | Фазовая диаграмма устойчивости | `StabilityIndex()`, `DetectPhase()`, `IsStable()` | ✅ Работает |
| `ale/math/CALReturnProbability.mqh` | Вероятности возврата/касания уровня | `ToCenter()`, `HitLevelGBM()` | ✅ Работает |

## Optimization

| Файл | Назначение | Ключевые сущности | Статус |
|---|---|---|---|
| `ale/optimization/CALExpectationModel.mqh` | Обёртка expectation для BUY/SELL | `ForBuy()`, `ForSell()` | ✅ Работает |
| `ale/optimization/CALGridOptimizer.mqh` | Оптимизация уровней сетки | `OptimizeLevelsBuy/Sell()` | ✅ Работает |
| `ale/optimization/CALLotOptimizer.mqh` | Оптимизация лота | `OptimizeBuy/Sell()` | ✅ Работает |
| `ale/optimization/CALOptimalK.mqh` | Выбор стабильного `k` и hedge lot | `FindBuy/Sell()`, `HedgeLot()` | ✅ Работает |

## Positions

| Файл | Назначение | Ключевые сущности | Статус |
|---|---|---|---|
| `ale/positions/CALDeltaTracker.mqh` | Net-delta и tail-slope | `CalculateNetDelta()`, `CalculateTailSlope()` | ✅ Работает |
| `ale/positions/CALLotModel.mqh` | Модель lot-эскалации и лимитов | `LotAtLevel()`, `CumulativeMaxVolume()`, `CanAddLevel()` | ✅ Работает |
| `ale/positions/CALPositionBook.mqh` | Книга виртуальных позиций | `Add()`, `TotalPnL()`, `PnLAtPrice()`, `Delta()` | ✅ Работает |
| `ale/positions/CALVirtualPosition.mqh` | Описание позиции и её PnL | `Init()`, `UpdatePnL()` | ✅ Работает |

## Risk

| Файл | Назначение | Ключевые сущности | Статус |
|---|---|---|---|
| `ale/risk/CALDrawdownModel.mqh` | Расчёт относительного drawdown | `Drawdown()` | ✅ Работает |
| `ale/risk/CALMarginModel.mqh` | Расчёт маржи | `MarginFromLots()`, `MarginBuy/Sell()` | ✅ Работает |
| `ale/risk/CALRiskEngine.mqh` | Композитная риск-оценка и SAFE-решение | `CALRiskReport`, `Evaluate()`, `SafeL0()` | ✅ Работает |
| `ale/risk/CALSafeMode.mqh` | SAFE-фазовая и триггерная логика | `EvaluatePhase()`, `EvaluateTriggers()` | ✅ Работает |
| `ale/risk/CALWorstCase.mqh` | Worst-case drawdown по endpoint’ам | `DrawdownFromEndpoints()`, `EvaluateBuy/Sell()` | ✅ Работает |

## Tests

| Файл | Назначение | Ключевые сущности | Статус |
|---|---|---|---|
| `tests/TestALE.mqh` | Интеграционные проверки dual-flow/FSM/инвариантов | `TestALE_DualFlowIntegration()` | ✅ Есть |
| `tests/TestALEContracts.mqh` | Контрактные проверки SAFE/additivity/phase | `TestPhaseDiagramGuard()`, `TestSAFEBypassContract()`, `TestAdditivityContract()` | ✅ Есть |
| `tests/TestALERegression.mqh` | Regression оракулы + replay/reset | `TestALE_RegressionOracles()` | ✅ Есть |
| `tests/TestGeometry.mqh` | Тесты геометрии и симметрии | `TestGeometry_BuySellGrids()` | ✅ Есть |
| `tests/TestRisk.mqh` | Тесты risk/margin/worst-dd | `TestRisk_WorstDDMargin()` | ✅ Есть |

---

## Быстрый итог

- Это «табличная» версия инвентаризации для инженерной навигации.
- Можно использовать как чек-лист при PR-review: есть ли изменения в контракте/формулах/слоях.
