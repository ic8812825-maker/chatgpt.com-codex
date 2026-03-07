# ALE (right/ale) module map

Этот каталог содержит движок Adaptive Lock Expansion (ALE) для правой части `VirtualPanel`.

## Карта модулей

- `core/`
  - `CALEngine.mqh` — оркестратор dual-flow BUY/SELL, global SAFE, события.
  - `CALFlowEngine.mqh` — потоковый движок одного направления.
  - `CALDeterministicRunner.mqh` — детерминированный replay runner для behavioral-сценариев.
  - `CALContext.mqh` — контекст и state-модели потока/агрегата.
- `config/`
  - `CALRiskConfig.mqh` — централизованные пороги риска/SAFE.
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
  - `RunAllTests.mqh/.mq5` — единый MQL runner ALE unit/behavior тестов.

## Debug

Для расширенного логирования включите макрос перед подключением модулей:

```cpp
#define VP_DEBUG 1
#include "core/CALDebug.mqh"
```
