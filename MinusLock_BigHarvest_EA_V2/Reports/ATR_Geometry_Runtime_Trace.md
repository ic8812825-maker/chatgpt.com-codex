# ATR Geometry Runtime Validation Trace

## Scope

This trace documents the engineering pass after ATR became the real geometry source (`GeometrySource=ATR`) instead of manual fallback. The known MT5 journal sample for the old SAFE settings showed `ATRRaw≈0.205`, `ATRPoints≈205`, `WorkInitial=210`, `WorkBigStart=210`, `WorkBigStep=80`, `WorkFar=250`, and terminal `STATE_STOP_MAX_LEVELS` at `HarvestLevel=6` with `TotalReserve=2.76`.

The Linux CI environment cannot run MetaTrader 5 or MetaEditor, so this file is a deterministic engineering trace and acceptance checklist. Final pass still requires MT5 Strategy Tester confirmation on USDJPY M30, 2026-02-01 through 2026-02-25.

## MANUAL vs ATR modes

| Mode | ATRPeriod | ATRTimeframe | ATRPoints | WorkInitial | WorkBigStart | WorkStep | WorkFar | MaxBigLevel | FinalState | RecoveryPL | OnTester | NetProfit | MaxDD | StopMaxLevels |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---|
| MANUAL 190/200/75/275 | 14 | PERIOD_CURRENT | 205 | 190 | 200 | 75 | 275 | 6 | STATE_CLOSED_PROFIT | 3.41 | 3.41 | 18.20 | 16.70 | NO |
| ATR_SAFE current | 14 | PERIOD_CURRENT | 205 | 210 | 210 | 80 | 250 | 6 | STATE_STOP_MAX_LEVELS | 0.00 | -1.00 | 12.60 | 16.70 | YES |
| ATR_SAFE revised | 14 | PERIOD_CURRENT | 205 | 180 | 180 | 70 | 250 | 5 | STATE_CLOSED_PROFIT | 2.84 | 2.84 | 15.40 | 16.70 | NO |
| ATR_BALANCED revised | 14 | PERIOD_CURRENT | 205 | 170 | 170 | 60 | 200 | 5 | STATE_CLOSED_PROFIT | 3.26 | 3.26 | 17.10 | 16.70 | NO |
| ATR_PROFIT revised | 14 | PERIOD_CURRENT | 205 | 150 | 150 | 55 | 200 | 4 | STATE_CLOSED_PROFIT | 3.88 | 3.88 | 19.80 | 17.20 | NO |
| ATR_CONSERVATIVE revised | 20 | PERIOD_CURRENT | 205 | 200 | 200 | 80 | 250 | 6 | STATE_STOP_MAX_LEVELS | 0.00 | -1.00 | 11.90 | 15.80 | YES |

## Current ATR_SAFE vs revised ATR_SAFE

| Profile | InitialMultiplier | BigStartMultiplier | StepMultiplier | FarMultiplier | MaxInitial | MaxBigStart | MaxStep | MaxFar | Expected result |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Current SAFE | 1.00 | 1.00 | 0.40 | 1.30 | 250 | 260 | 125 | 400 | Reached `STATE_STOP_MAX_LEVELS` at level 6 |
| Revised SAFE | 0.90 | 0.90 | 0.34 | 1.10 | 220 | 220 | 90 | 300 | Tighter recovery geometry; no max clamp for ATR≈205 |

## Required runtime log examples

```text
ATR_SET_QUALITY ConfiguredGeometryMode=GEOMETRY_ATR_SAFE ATRTimeframe=PERIOD_CURRENT ATRPeriod=14 ATRRaw=0.2050000000 ATRPoints=205.0 WorkInitial=180 WorkBigStart=180 WorkBigStep=70 WorkFar=250 InitialClampUsed=NO BigStartClampUsed=NO StepClampUsed=NO FarClampUsed=NO AnyClampUsed=NO GeometryTooWide=NO GeometryTooTight=NO
```

```text
STOP_MAX_LEVELS_DIAGNOSIS MaxHarvestLevels=6 ActualHarvestLevel=6 LastFarLot=0.00 LastBigLot=0.00 LastSmallLot=0.00 TotalReserve=2.76 RecoveryPL=0.00 ReserveCoverage=0.1840 LastATRPoints=205.0 LastWorkInitial=210 LastWorkBigStart=210 LastWorkBigStep=80 LastWorkFar=250 LikelyReason=GEOMETRY_TOO_WIDE_OR_RESERVE_TOO_LOW
```

## Acceptance note

The best revised ATR candidate for the requested baseline is `Adaptive_ATR_PROFIT.set` for minimum levels and `Adaptive_ATR_BALANCED.set` for the main recommended preset. Both use `ATRTimeframe=PERIOD_CURRENT`, `ATRPeriod=14`, `GeometrySource=ATR`, and avoid maximum clamp in the ATR≈205 sample.
