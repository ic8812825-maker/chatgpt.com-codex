# 25. Broker Grid и rounding HSB.2A

Price grid определяется `SYMBOL_TRADE_TICK_SIZE`, а не Digits. Pure API различает FLOOR, CEIL, NEAREST, повторно проверяет normalized price и считает distance in ticks. Invalid/off-grid/nonfinite/stale price fail-closed.

Volume grid задаётся VolumeMin/Max/Step с floating tolerance. BigCore, BigTrend и PartialFar contract используют floor; SmallBase — ceil. Partial Far здесь не реализован. После rounding обязательны bounds, finiteness и кратность step; разрушенная geometry отклоняется.

Нормативные примеры: при step 0.01 raw 0.256 → floor 0.25, ceil 0.26; при step 0.10 → 0.20/0.30. Point нельзя сравнивать с Price без conversion, lots нельзя складывать с ratio.

```text
FUTURE_SMALL=NOT_IMPLEMENTED_IN_HSB_2A
NEW_FAR_SOLVER=NOT_IMPLEMENTED_IN_HSB_2A
TRADE_EXECUTION=NOT_IMPLEMENTED
PRODUCTION_PERSISTENCE=NOT_IMPLEMENTED
REAL_TRADING_ALLOWED=NO
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_RUNTIME_TESTS=USER_VERIFICATION_REQUIRED
```
