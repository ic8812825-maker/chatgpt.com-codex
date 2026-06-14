# AI Cycle Math

| Level | Scenario | InitialFarDistance | CurrentBigMove | CumulativeBigMove | EffectiveFarDistance | FarLotBefore | BigLot | SmallLot | NetProfit | Reserve | FarRemainLoss | FinalClose | State | Action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BIG_HARVEST | 100 | 100 | 100 | 200 | 1.00 | 1.30 | 0.48 | 82.00 | 8.20 | 128.00 | NO | STATE_BIG_HARVEST | REPEAT_HARVEST |
| 2 | SMALL_AT_FAR | 0 | 0 | 0 | 0 | 0.64 | 0.83 | 0.31 | 12.00 | 8.20 | 0.00 | YES | STATE_CLOSED_PROFIT | FINAL_CLOSE |
