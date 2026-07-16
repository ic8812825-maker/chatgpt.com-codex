# Денежный шлюз улучшения RecoveryPL в Big

Перед открытием Split legs используются фактически нормализованные Core/Trend/Small/Far lots. Для целевого Big-level каждая leg проектируется через `OrderCalcProfit` с Bid/Ask execution, commission, directional swap fallback, spread expansion, slippage и position/order buffers.

```text
ProjectedBigRecoveryDelta = CoreNet + TrendNet + SmallNet + FarNet
```

Открытие запрещено, если calculation invalid, net exposure ниже `MinimumNetBigExposureLots` или delta ниже `MinimumBigRecoveryImprovementMoney`. Проверка повторяется для каждого level через `GetBigMovePoints(level)`.

Это runtime gate, но не MT5-доказательство: MetaEditor и Strategy Tester не запускались. Production статус остаётся NOT_CONFIRMED.
