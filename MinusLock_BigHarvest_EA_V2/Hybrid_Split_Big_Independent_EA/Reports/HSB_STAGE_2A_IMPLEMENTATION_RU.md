# HSB.2A — отчёт реализации расчётного слоя

Статически реализованы broker properties, price/volume grids, typed control prices/costs, OrderCalcProfit/OrderCalcMargin wrappers, Big geometry, recovery slope/direction, Catch-Up и unified fail-closed gates. Harness содержит непрерывные уникальные T01–T70. Broker wrappers используют только calculation APIs и не меняют Context, ledger, roles или FSM.

MetaEditor/MT5 evidence выполняет администратор. Ручной review не объявляется compile/runtime PASS. HSB.2B не начат; торговых API и execution нет.

```text
FUTURE_SMALL=NOT_IMPLEMENTED_IN_HSB_2A
NEW_FAR_SOLVER=NOT_IMPLEMENTED_IN_HSB_2A
TRADE_EXECUTION=NOT_IMPLEMENTED
PRODUCTION_PERSISTENCE=NOT_IMPLEMENTED
REAL_TRADING_ALLOWED=NO
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_RUNTIME_TESTS=USER_VERIFICATION_REQUIRED
```
