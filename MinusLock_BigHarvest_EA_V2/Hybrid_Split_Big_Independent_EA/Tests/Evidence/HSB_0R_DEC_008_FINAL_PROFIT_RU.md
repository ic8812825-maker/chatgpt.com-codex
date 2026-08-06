# HSBI-DEC-008 — minimum Final Close profit

Статус: `DEFERRED_WITH_SAFE_CONTRACT`.

Единый primary gate: `RecoveryPLCloseNow >= MinimumRecoveryProfitMoney + ExecutionSafetyBufferMoney + MoneyTolerance`. Все величины — money в валюте счёта. MinimumRecoveryProfitMoney обязан быть >0, buffer >=0 и итоговый threshold выше расчётного шума и ожидаемых close costs.

Points/percent могут быть дополнительными constraints, но не source of truth. RecoveryPLCloseNow включает RealizedCycleNet и broker-model close-now open positions; allocation buckets повторно не прибавляются. Конкретное minimum — конфигурация без real default. Stale snapshot, unknown deal, pending transaction или negative result блокируют Final Close.

Owner: `Money/FinalCloseCalculator`. Tests: threshold equality, tolerance, costs, double-counting guard, BUY/SELL close side.
