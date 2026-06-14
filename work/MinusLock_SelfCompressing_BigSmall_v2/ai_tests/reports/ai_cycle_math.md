# AI Cycle Math

| Level | Scenario | FarLotBefore | BigLot | SmallLot | NetProfit | Reserve | FarRemainLoss | FinalClose | State | Action |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BIG_HARVEST | 1.00 | 1.30 | 0.48 | 82.00 | 8.20 | 128.00 | NO | STATE_BIG_HARVEST | REPEAT_HARVEST |
| 2 | SMALL_AT_FAR | 0.64 | 0.83 | 0.31 | 14.00 | 8.20 | 118.00 | NO | STATE_SMALL_SCENARIO | OPEN_NEW_BIG_SMALL |
| 3 | SMALL_AT_FAR | 0.59 | 0.77 | 0.28 | 10.00 | 8.20 | 108.00 | NO | STATE_SMALL_SCENARIO | OPEN_NEW_BIG_SMALL |
| 4 | BIG_HARVEST | 0.54 | 0.70 | 0.26 | 88.00 | 17.00 | 30.00 | NO | STATE_BIG_HARVEST | REPEAT_HARVEST |
| 5 | SMALL_AT_FAR | 0.15 | 0.20 | 0.07 | 2.00 | 17.00 | 28.00 | NO | STATE_UNCLOSED_CYCLE | CLOSE_RESIDUAL_FAR |
