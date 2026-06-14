# Compare 90/10 vs 50/50 — Python Model

> Python-модель показывает кандидата для MT5-подтверждения. Это не финальная победа стратегии.

## Summary

- 90/10: State=STATE_UNCLOSED_CYCLE, CycleFinalPL=-9.20, Reason=STOP_MAX_LEVELS after Small-at-Far
- 50/50: State=STATE_CLOSED_PROFIT, CycleFinalPL=20.50, Reason=FinalCloseAllowed after Big-harvest
- 60/40 neighbor: State=STATE_CLOSED_PROFIT, CycleFinalPL=15.20, Reason=FinalCloseAllowed after Big-harvest

90/10 ломается, потому что резерв после Big-harvest растёт медленно, а после Small-at-Far новый Far всё ещё требует FarRemainLoss выше TotalReserve.
50/50 сохраняет больше NetProfit в Reserve, поэтому FinalCloseAllowed срабатывает раньше в этой Python-последовательности.

## A: CloseFarShare=0.90 / ReserveShare=0.10

| Level | Scenario | FarLotBefore | BigLot | SmallLot | NetProfit | CloseFarBudget | ReserveAdd | TotalReserve | FarRemainLoss | FinalCloseAllowed | State |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BIG_HARVEST | 1.00 | 1.30 | 0.48 | 82.00 | 73.80 | 8.20 | 8.20 | 128.00 | NO | STATE_BIG_HARVEST |
| 2 | SMALL_AT_FAR | 0.64 | 0.83 | 0.31 | 12.00 | 0.00 | 0.00 | 8.20 | 116.00 | NO | STATE_SMALL_SCENARIO |
| 3 | SMALL_AT_FAR | 0.58 | 0.75 | 0.28 | 10.00 | 0.00 | 0.00 | 8.20 | 104.00 | NO | STATE_SMALL_SCENARIO |
| 4 | BIG_HARVEST | 0.52 | 0.68 | 0.25 | 86.00 | 77.40 | 8.60 | 16.80 | 28.00 | NO | STATE_BIG_HARVEST |
| 5 | SMALL_AT_FAR | 0.14 | 0.18 | 0.07 | 4.00 | 0.00 | 0.00 | 16.80 | 26.00 | NO | STATE_UNCLOSED_CYCLE |

Result: State=STATE_UNCLOSED_CYCLE, CycleFinalPL=-9.20, Reason=STOP_MAX_LEVELS after Small-at-Far

## B: CloseFarShare=0.50 / ReserveShare=0.50

| Level | Scenario | FarLotBefore | BigLot | SmallLot | NetProfit | CloseFarBudget | ReserveAdd | TotalReserve | FarRemainLoss | FinalCloseAllowed | State |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BIG_HARVEST | 1.00 | 1.30 | 0.47 | 83.00 | 41.50 | 41.50 | 41.50 | 160.00 | NO | STATE_BIG_HARVEST |
| 2 | SMALL_AT_FAR | 0.80 | 1.04 | 0.37 | 2.00 | 0.00 | 0.00 | 41.50 | 136.00 | NO | STATE_SMALL_SCENARIO |
| 3 | SMALL_AT_FAR | 0.68 | 0.88 | 0.32 | 2.00 | 0.00 | 0.00 | 41.50 | 114.00 | NO | STATE_SMALL_SCENARIO |
| 4 | BIG_HARVEST | 0.57 | 0.74 | 0.27 | 94.00 | 47.00 | 47.00 | 88.50 | 68.00 | YES | STATE_CLOSED_PROFIT |

Result: State=STATE_CLOSED_PROFIT, CycleFinalPL=20.50, Reason=FinalCloseAllowed after Big-harvest

## C: CloseFarShare=0.60 / ReserveShare=0.40

| Level | Scenario | FarLotBefore | BigLot | SmallLot | NetProfit | CloseFarBudget | ReserveAdd | TotalReserve | FarRemainLoss | FinalCloseAllowed | State |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BIG_HARVEST | 1.00 | 1.30 | 0.47 | 83.00 | 49.80 | 33.20 | 33.20 | 152.00 | NO | STATE_BIG_HARVEST |
| 2 | SMALL_AT_FAR | 0.76 | 0.99 | 0.36 | 2.00 | 0.00 | 0.00 | 33.20 | 128.00 | NO | STATE_SMALL_SCENARIO |
| 3 | SMALL_AT_FAR | 0.64 | 0.83 | 0.30 | 2.00 | 0.00 | 0.00 | 33.20 | 108.00 | NO | STATE_SMALL_SCENARIO |
| 4 | BIG_HARVEST | 0.54 | 0.70 | 0.25 | 90.00 | 54.00 | 36.00 | 69.20 | 54.00 | YES | STATE_CLOSED_PROFIT |

Result: State=STATE_CLOSED_PROFIT, CycleFinalPL=15.20, Reason=FinalCloseAllowed after Big-harvest

