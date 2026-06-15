# Far Distance Mode Comparison

> Python-модель не заменяет MT5 Strategy Tester. Она пересчитывает расстояние Far с учётом первых 100 пунктов initial lock.

## Was first 100 points counted before?

Частично: старый режим `FIXED_200` давал правильный Level 1 при `InitialTrigger=100` и `BigMove=100`, но не различал Level 2/3 режимы `INITIAL_PLUS_CURRENT` и `INITIAL_PLUS_CUMULATIVE` и не сбрасывал дистанцию явно после Small-at-Far.

## Correct Level 1

For `InitialTriggerPoints=100` and `BigMoveLevel1=100`, `EffectiveFarDistance=200`. If a model returns 100, it is wrong.

- EffectiveFarDistance: 200
- CloseFarLotRounded: 0.36
- FarRemainLoss: 128.00
- FinalCloseAllowed: NO

## Variant / Mode Table

| Variant | FarDistanceMode | Level | Scenario | InitialFarDistance | CurrentBigMove | CumulativeBigMove | EffectiveFarDistance | FarLotBefore | BigLot | SmallLot | NetProfit | CloseFarBudget | ReserveAdd | TotalReserve | CloseFarLotRounded | FarRemainLot | FarRemainLoss | FinalCloseAllowed | State | CycleFinalPL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 90/10 | FIXED_200 | 1 | BIG_HARVEST | 100 | 100 | 100 | 200 | 1.00 | 1.30 | 0.48 | 82.00 | 73.80 | 8.20 | 8.20 | 0.36 | 0.64 | 128.00 | NO | STATE_BIG_HARVEST | -119.80 |
| 90/10 | FIXED_200 | 2 | SMALL_AT_FAR | 0 | 0 | 0 | 0 | 0.64 | 0.83 | 0.31 | 12.00 | 0.00 | 0.00 | 8.20 | 0.25 | 0.58 | 0.00 | YES | STATE_CLOSED_PROFIT | 8.20 |
| 90/10 | INITIAL_PLUS_CURRENT | 1 | BIG_HARVEST | 100 | 100 | 100 | 200 | 1.00 | 1.30 | 0.48 | 82.00 | 73.80 | 8.20 | 8.20 | 0.36 | 0.64 | 128.00 | NO | STATE_BIG_HARVEST | -119.80 |
| 90/10 | INITIAL_PLUS_CURRENT | 2 | SMALL_AT_FAR | 0 | 0 | 0 | 0 | 0.64 | 0.83 | 0.31 | 12.00 | 0.00 | 0.00 | 8.20 | 0.25 | 0.58 | 0.00 | YES | STATE_CLOSED_PROFIT | 8.20 |
| 90/10 | INITIAL_PLUS_CUMULATIVE | 1 | BIG_HARVEST | 100 | 100 | 100 | 200 | 1.00 | 1.30 | 0.48 | 82.00 | 73.80 | 8.20 | 8.20 | 0.36 | 0.64 | 128.00 | NO | STATE_BIG_HARVEST | -119.80 |
| 90/10 | INITIAL_PLUS_CUMULATIVE | 2 | SMALL_AT_FAR | 0 | 0 | 0 | 0 | 0.64 | 0.83 | 0.31 | 12.00 | 0.00 | 0.00 | 8.20 | 0.25 | 0.58 | 0.00 | YES | STATE_CLOSED_PROFIT | 8.20 |
| 60/40 | FIXED_200 | 1 | BIG_HARVEST | 100 | 100 | 100 | 200 | 1.00 | 1.30 | 0.47 | 83.00 | 49.80 | 33.20 | 33.20 | 0.24 | 0.76 | 152.00 | NO | STATE_BIG_HARVEST | -118.80 |
| 60/40 | FIXED_200 | 2 | SMALL_AT_FAR | 0 | 0 | 0 | 0 | 0.76 | 0.99 | 0.36 | 2.00 | 0.00 | 0.00 | 33.20 | 0.35 | 0.64 | 0.00 | YES | STATE_CLOSED_PROFIT | 33.20 |
| 60/40 | INITIAL_PLUS_CURRENT | 1 | BIG_HARVEST | 100 | 100 | 100 | 200 | 1.00 | 1.30 | 0.47 | 83.00 | 49.80 | 33.20 | 33.20 | 0.24 | 0.76 | 152.00 | NO | STATE_BIG_HARVEST | -118.80 |
| 60/40 | INITIAL_PLUS_CURRENT | 2 | SMALL_AT_FAR | 0 | 0 | 0 | 0 | 0.76 | 0.99 | 0.36 | 2.00 | 0.00 | 0.00 | 33.20 | 0.35 | 0.64 | 0.00 | YES | STATE_CLOSED_PROFIT | 33.20 |
| 60/40 | INITIAL_PLUS_CUMULATIVE | 1 | BIG_HARVEST | 100 | 100 | 100 | 200 | 1.00 | 1.30 | 0.47 | 83.00 | 49.80 | 33.20 | 33.20 | 0.24 | 0.76 | 152.00 | NO | STATE_BIG_HARVEST | -118.80 |
| 60/40 | INITIAL_PLUS_CUMULATIVE | 2 | SMALL_AT_FAR | 0 | 0 | 0 | 0 | 0.76 | 0.99 | 0.36 | 2.00 | 0.00 | 0.00 | 33.20 | 0.35 | 0.64 | 0.00 | YES | STATE_CLOSED_PROFIT | 33.20 |
| 50/50 | FIXED_200 | 1 | BIG_HARVEST | 100 | 100 | 100 | 200 | 1.00 | 1.30 | 0.47 | 83.00 | 41.50 | 41.50 | 41.50 | 0.20 | 0.80 | 160.00 | NO | STATE_BIG_HARVEST | -118.50 |
| 50/50 | FIXED_200 | 2 | SMALL_AT_FAR | 0 | 0 | 0 | 0 | 0.80 | 1.04 | 0.37 | 2.00 | 0.00 | 0.00 | 41.50 | 0.36 | 0.68 | 0.00 | YES | STATE_CLOSED_PROFIT | 41.50 |
| 50/50 | INITIAL_PLUS_CURRENT | 1 | BIG_HARVEST | 100 | 100 | 100 | 200 | 1.00 | 1.30 | 0.47 | 83.00 | 41.50 | 41.50 | 41.50 | 0.20 | 0.80 | 160.00 | NO | STATE_BIG_HARVEST | -118.50 |
| 50/50 | INITIAL_PLUS_CURRENT | 2 | SMALL_AT_FAR | 0 | 0 | 0 | 0 | 0.80 | 1.04 | 0.37 | 2.00 | 0.00 | 0.00 | 41.50 | 0.36 | 0.68 | 0.00 | YES | STATE_CLOSED_PROFIT | 41.50 |
| 50/50 | INITIAL_PLUS_CUMULATIVE | 1 | BIG_HARVEST | 100 | 100 | 100 | 200 | 1.00 | 1.30 | 0.47 | 83.00 | 41.50 | 41.50 | 41.50 | 0.20 | 0.80 | 160.00 | NO | STATE_BIG_HARVEST | -118.50 |
| 50/50 | INITIAL_PLUS_CUMULATIVE | 2 | SMALL_AT_FAR | 0 | 0 | 0 | 0 | 0.80 | 1.04 | 0.37 | 2.00 | 0.00 | 0.00 | 41.50 | 0.36 | 0.68 | 0.00 | YES | STATE_CLOSED_PROFIT | 41.50 |

## Summary

- 90/10 / FIXED_200: State=STATE_CLOSED_PROFIT, CycleFinalPL=8.20, Reason=FinalCloseAllowed after Small-at-Far
- 90/10 / INITIAL_PLUS_CURRENT: State=STATE_CLOSED_PROFIT, CycleFinalPL=8.20, Reason=FinalCloseAllowed after Small-at-Far
- 90/10 / INITIAL_PLUS_CUMULATIVE: State=STATE_CLOSED_PROFIT, CycleFinalPL=8.20, Reason=FinalCloseAllowed after Small-at-Far
- 60/40 / FIXED_200: State=STATE_CLOSED_PROFIT, CycleFinalPL=33.20, Reason=FinalCloseAllowed after Small-at-Far
- 60/40 / INITIAL_PLUS_CURRENT: State=STATE_CLOSED_PROFIT, CycleFinalPL=33.20, Reason=FinalCloseAllowed after Small-at-Far
- 60/40 / INITIAL_PLUS_CUMULATIVE: State=STATE_CLOSED_PROFIT, CycleFinalPL=33.20, Reason=FinalCloseAllowed after Small-at-Far
- 50/50 / FIXED_200: State=STATE_CLOSED_PROFIT, CycleFinalPL=41.50, Reason=FinalCloseAllowed after Small-at-Far
- 50/50 / INITIAL_PLUS_CURRENT: State=STATE_CLOSED_PROFIT, CycleFinalPL=41.50, Reason=FinalCloseAllowed after Small-at-Far
- 50/50 / INITIAL_PLUS_CUMULATIVE: State=STATE_CLOSED_PROFIT, CycleFinalPL=41.50, Reason=FinalCloseAllowed after Small-at-Far

## Verdict

For MT5, use `REAL_PRICE_DISTANCE` because it measures actual `ABS(CurrentClosePrice - FarOpenPrice) / Point`. For Python pre-checks without ticks, use `INITIAL_PLUS_CURRENT` and `INITIAL_PLUS_CUMULATIVE` to bound behavior. After Small-at-Far, the model resets `InitialFarDistancePoints=0` and `CumulativeBigMovePoints=0` for the new Far.
