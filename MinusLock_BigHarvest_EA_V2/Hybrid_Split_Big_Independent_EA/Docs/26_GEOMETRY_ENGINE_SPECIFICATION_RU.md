# 26. Geometry Engine HSB.2A

Норматив: `C=floor(F×Rc)`, `T=floor(F×Rt)`, `S=ceil(F×Rs)`, `Bnet=C+T−S`. Все величины volume — lots; ratios безразмерны. После broker rounding проверяются bounds/grid, `Bnet>0` и recovery slope `C+T−S−F>0`.

Slope — только lot-level filter: не broker-money proof, не Final Close proof, не резерв и не разрешение торговли. Invalid ratios/Far/grid/nonfinite/overflow/failed prerequisites возвращают fail-closed result.

Direction contract использует фактические broker-money результаты в P и следующем благоприятном tick: для Far SELL проверяется P+TickSize, для Far BUY — P−TickSize. Без money evidence monotonicity недоступна. Future Small, NewFar, compression, transition и role promotion отсутствуют.

```text
FUTURE_SMALL=NOT_IMPLEMENTED_IN_HSB_2A
NEW_FAR_SOLVER=NOT_IMPLEMENTED_IN_HSB_2A
TRADE_EXECUTION=NOT_IMPLEMENTED
PRODUCTION_PERSISTENCE=NOT_IMPLEMENTED
REAL_TRADING_ALLOWED=NO
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_RUNTIME_TESTS=USER_VERIFICATION_REQUIRED
```
