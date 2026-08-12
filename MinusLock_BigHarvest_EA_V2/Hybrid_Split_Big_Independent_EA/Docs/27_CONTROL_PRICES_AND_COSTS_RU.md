# 27. Control Prices и Costs HSB.2A

Typed control price содержит Symbol, Bid, Ask, Mid, selected Price, Direction, explicit Side, Point/TickSize/Digits, timestamp/snapshot и fresh/normalized/valid flags. CURRENT_CLOSE, NEXT_BIG_CONTROL, ADVERSE_RISK, GAP_STRESS и FINAL_CLOSE являются только DTO types; Final Close не реализован.

BUY position close использует Bid, SELL close — Ask. Missing/nonfinite Bid/Ask, Ask<Bid, wrong side/Symbol, stale snapshot, invalid tick size или off-grid selected price отклоняются.

Cost snapshot не смешивает actual и projected. Actual DealNet складывает signed Profit/Swap/Commission/Fee. Projected model отдельно учитывает spread/slippage/safety buffers как расходы, не превращая их в прибыль.

```text
FUTURE_SMALL=NOT_IMPLEMENTED_IN_HSB_2A
NEW_FAR_SOLVER=NOT_IMPLEMENTED_IN_HSB_2A
TRADE_EXECUTION=NOT_IMPLEMENTED
PRODUCTION_PERSISTENCE=NOT_IMPLEMENTED
REAL_TRADING_ALLOWED=NO
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_RUNTIME_TESTS=USER_VERIFICATION_REQUIRED
```
