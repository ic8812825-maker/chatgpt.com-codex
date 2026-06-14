# AI Cycle Math

| Level | Scenario | FarLotBefore | BigLot | SmallLot | NetProfit | Reserve | FarRemainLoss | FinalClose | State | Action |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BIG_HARVEST | 1.00 | 1.30 | 0.48 | 82.00 | 8.20 | 128.00 | NO | STATE_BIG_HARVEST | REPEAT_HARVEST |
| 2 | SMALL_AT_FAR | 0.64 | 0.83 | 0.31 | 12.00 | 8.20 | 116.00 | NO | STATE_SMALL_SCENARIO | OPEN_NEW_BIG_SMALL |
| 3 | SMALL_AT_FAR | 0.58 | 0.75 | 0.28 | 10.00 | 8.20 | 104.00 | NO | STATE_SMALL_SCENARIO | OPEN_NEW_BIG_SMALL |
| 4 | BIG_HARVEST | 0.52 | 0.68 | 0.25 | 86.00 | 16.80 | 28.00 | NO | STATE_BIG_HARVEST | REPEAT_HARVEST |
| 5 | SMALL_AT_FAR | 0.14 | 0.18 | 0.07 | 4.00 | 16.80 | 26.00 | NO | STATE_UNCLOSED_CYCLE | CLOSE_RESIDUAL_FAR |
