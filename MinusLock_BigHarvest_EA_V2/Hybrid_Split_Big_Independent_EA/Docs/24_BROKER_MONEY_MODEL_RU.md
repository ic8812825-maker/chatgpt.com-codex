# 24. Broker-Money Model HSB.2A

`HSBI_BrokerProperties` фиксирует Symbol, Point, TickSize, Digits, volume grid, asymmetric tick values, snapshot identity и freshness. Lot, Price, Point, TickSize, Money, Ratio/Percent, Ticket и PositionIdentifier не смешиваются; projected никогда не записывается как actual, а FinalReserve не является дополнительной прибылью.

`HSBI_CalculateProjectedProfit` валидирует properties, direction, Bid/Ask close side, price/volume grids и projected costs, затем вызывает только расчётный `OrderCalcProfit`. `HSBI_CalculateProjectedMargin` аналогично использует только `OrderCalcMargin`. Ошибка broker API возвращает `UNAVAILABLE`, не ноль. Wrappers не получают Context/ledger/roles/FSM и ничего не изменяют.

Actual DealNet: `Profit + Swap + Commission + Fee`. Projected net дополнительно вычитает spread cost, expected slippage и execution safety buffer. Actual/projected cost snapshots несовместимы; знаки commission/swap/fee сохраняются.

Catch-Up требует одновременно `ReserveShare × Bnet > F` и `ReserveGainMoney > FarLossIncreaseMoney + ExecutionSafetyBuffer`; без broker money — `UNAVAILABLE`. Far BUY и Far SELL типизированы.

Fail-closed statuses: PASS, REJECT, ERROR, UNAVAILABLE. NaN/infinity, stale/unknown properties, invalid grids/direction/money/margin отклоняются.

```text
FUTURE_SMALL=NOT_IMPLEMENTED_IN_HSB_2A
NEW_FAR_SOLVER=NOT_IMPLEMENTED_IN_HSB_2A
TRADE_EXECUTION=NOT_IMPLEMENTED
PRODUCTION_PERSISTENCE=NOT_IMPLEMENTED
REAL_TRADING_ALLOWED=NO
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_RUNTIME_TESTS=USER_VERIFICATION_REQUIRED
```
