# Compare 90/10 vs 50/50 — Python Model

> Python-модель показывает кандидата для MT5-подтверждения. Это не финальная победа стратегии.

## Summary

- 90/10: State=STATE_CLOSED_PROFIT, CycleFinalPL=8.20, Reason=FinalCloseAllowed after Small-at-Far
- 50/50: State=STATE_CLOSED_PROFIT, CycleFinalPL=41.50, Reason=FinalCloseAllowed after Small-at-Far
- 60/40 neighbor: State=STATE_CLOSED_PROFIT, CycleFinalPL=33.20, Reason=FinalCloseAllowed after Small-at-Far

90/10 ломается, потому что резерв после Big-harvest растёт медленно, а после Small-at-Far новый Far всё ещё требует FarRemainLoss выше TotalReserve.
50/50 сохраняет больше NetProfit в Reserve, поэтому FinalCloseAllowed срабатывает раньше в этой Python-последовательности.

## A: CloseFarShare=0.90 / ReserveShare=0.10

| Level | Scenario | FarLotBefore | BigLot | SmallLot | NetProfit | CloseFarBudget | ReserveAdd | TotalReserve | FarRemainLoss | FinalCloseAllowed | State |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BIG_HARVEST | 1.00 | 1.30 | 0.48 | 82.00 | 73.80 | 8.20 | 8.20 | 128.00 | NO | STATE_BIG_HARVEST |
| 2 | SMALL_AT_FAR | 0.64 | 0.83 | 0.31 | 12.00 | 0.00 | 0.00 | 8.20 | 0.00 | YES | STATE_CLOSED_PROFIT |

Result: State=STATE_CLOSED_PROFIT, CycleFinalPL=8.20, Reason=FinalCloseAllowed after Small-at-Far

## B: CloseFarShare=0.50 / ReserveShare=0.50

| Level | Scenario | FarLotBefore | BigLot | SmallLot | NetProfit | CloseFarBudget | ReserveAdd | TotalReserve | FarRemainLoss | FinalCloseAllowed | State |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BIG_HARVEST | 1.00 | 1.30 | 0.47 | 83.00 | 41.50 | 41.50 | 41.50 | 160.00 | NO | STATE_BIG_HARVEST |
| 2 | SMALL_AT_FAR | 0.80 | 1.04 | 0.37 | 2.00 | 0.00 | 0.00 | 41.50 | 0.00 | YES | STATE_CLOSED_PROFIT |

Result: State=STATE_CLOSED_PROFIT, CycleFinalPL=41.50, Reason=FinalCloseAllowed after Small-at-Far

## C: CloseFarShare=0.60 / ReserveShare=0.40

| Level | Scenario | FarLotBefore | BigLot | SmallLot | NetProfit | CloseFarBudget | ReserveAdd | TotalReserve | FarRemainLoss | FinalCloseAllowed | State |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BIG_HARVEST | 1.00 | 1.30 | 0.47 | 83.00 | 49.80 | 33.20 | 33.20 | 152.00 | NO | STATE_BIG_HARVEST |
| 2 | SMALL_AT_FAR | 0.76 | 0.99 | 0.36 | 2.00 | 0.00 | 0.00 | 33.20 | 0.00 | YES | STATE_CLOSED_PROFIT |

Result: State=STATE_CLOSED_PROFIT, CycleFinalPL=33.20, Reason=FinalCloseAllowed after Small-at-Far

