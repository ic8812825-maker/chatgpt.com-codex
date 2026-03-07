# ALE (right/ale) module map

Этот каталог содержит движок Adaptive Lock Expansion (ALE) для правой части `VirtualPanel`.

## Карта модулей

- `core/`
  - `CALEngine.mqh` — оркестратор dual-flow BUY/SELL, global SAFE, события.
  - `CALFlowEngine.mqh` — потоковый движок одного направления с NaN/Inf guard и SAFE fallback.
  - `CALDeterministicRunner.mqh` — детерминированный replay runner, state-trace matcher и сценарии (`trend`, `flat`, `crash`, `V-shape`).
  - `CALExportHelper.mqh` — CSV/XML экспорт (`CALContext` timeline, позиции, JUnit-like summary).
  - `CALContext.mqh` — контекст и state-модели потока/агрегата.
- `config/`
  - `CALRiskConfig.mqh` — централизованные пороги риска/SAFE + runtime invariants config:
    - `MAX_POSITIONS`
    - `MIN_LOT`
    - `ENABLE_STRICT_RUNTIME_CHECKS`
- `positions/`
  - `CALPositionBook.mqh` — хранение виртуальных позиций + runtime инварианты + rollback.
- `geometry/`
  - построение сеток уровней и шагов.
- `exposure/`
  - расчет дельты/гаммы/convexity/exposure.
- `risk/`
  - risk-engine, drawdown, margin, SAFE decisions.
- `math/`
  - вспомогательные математические модели (GBM, вероятности, phase diagram).
- `optimization/`
  - оптимизация lot/grid параметров.
- `interfaces/`
  - контракты `IALEngine`, `IFSM`, `IALRiskModel`, и др.
- `tests/`
  - `RunAllTests.mqh/.mq5` — единый MQL runner ALE unit/behavior тестов и XML summary.

## Debug

Для расширенного логирования включите макрос перед подключением модулей:

```cpp
#define VP_DEBUG 1
#include "core/CALDebug.mqh"
```

## Пример deterministic replay + CSV

```cpp
CALRiskConfig cfg;
cfg.SetDefaults();

CALDeterministicRunner runner;
runner.Init(cfg);
runner.AttachVirtuals(1.1000,0.10,1.1000,0.10);

CALReplayResult res;
runner.ReplayScenario(ALE_REPLAY_VSHAPE,1.1000,0.0005,20,res);
// ale_replay_context.csv будет записан автоматически внутри Replay().
```
