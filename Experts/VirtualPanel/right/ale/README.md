# ALE (right/ale) module map

Этот каталог содержит движок Adaptive Lock Expansion (ALE) для правой части `VirtualPanel`.

## Новая архитектура “отдельные мозги + общий мозг”

- `CALEngineBuy` — независимый мозг BUY.
- `CALEngineSell` — независимый мозг SELL.
- `CALEngineCommon` — общий мозг агрегации BUY+SELL (net delta, pnl, exposure, margin, global SAFE).
- `CALEngine` — оркестратор, который синхронизирует три мозга и эмитит события.

## Карта модулей

- `core/`
  - `CALEngine.mqh` — orchestrator трех мозгов и событий.
  - `CALEngineBuy.mqh` — изолированный BUY brain.
  - `CALEngineSell.mqh` — изолированный SELL brain.
  - `CALEngineCommon.mqh` — агрегаторный common brain.
  - `CALFlowEngine.mqh` — потоковый движок одного направления с NaN/Inf guard и SAFE fallback.
  - `CALDeterministicRunner.mqh` — детерминированный replay runner, state-trace matcher и сценарии (`uptrend`, `downtrend`, `oscillation`, `crash`, `V-shape`).
  - `CALExportHelper.mqh` — CSV/XML экспорт (`CALContext` timeline, позиции, JUnit-like summary).
  - `CALContext.mqh` — контекст BUY/SELL/COMMON.
- `config/`
  - `CALRiskConfig.mqh` — пороги риска/SAFE + runtime-invariants config:
    - `MAX_POSITIONS`
    - `MIN_LOT`
    - `ENABLE_STRICT_RUNTIME_CHECKS`
- `positions/`
  - `CALPositionBook.mqh` — виртуальные позиции + инварианты + rollback.
- `tests/`
  - `RunAllTests.mqh/.mq5` — единый MQL runner ALE unit/behavior тестов + XML summary.

## Read-only метрики для UI

Через `IALEngine` доступны:

- состояния: `StateBuy()`, `StateSell()`, `StateCommon()`;
- метрики: `NetDeltaCommon()`, `PnLCommon()`, `ExposureCommon()`, `MarginCommon()`, `WorstDDCommon()`, `SAFECommon()`;
- полный read-only context: `Context()`.

## Пример deterministic replay + CSV

```cpp
CALRiskConfig cfg;
cfg.SetDefaults();

CALDeterministicRunner runner;
runner.Init(cfg);
runner.AttachVirtuals(1.1000,0.10,1.1000,0.10);

CALReplayResult res;
runner.ReplayScenario(ALE_REPLAY_VSHAPE,1.1000,0.0005,20,res);
// ale_replay_context.csv будет записан внутри Replay().
```
