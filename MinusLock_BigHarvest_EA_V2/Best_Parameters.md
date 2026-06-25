# Offline Best Parameters for MinusLock_BigHarvest_EA_V2

## Scope and limitations

This report is generated without MT5. It is a deterministic offline filter, not a replacement for MetaTrader Strategy Tester.
It uses the strict success rule `RecoveryPL = FinalBalance - CycleStartBalance`; AccountPL versus InitialDeposit is diagnostic only.
InitialIgnoredProfit is excluded from pass/fail, matching the EA realRecoveryPL / OnTester contract.

## Optimization model

- Synthetic scenarios: A_BIG_WINS, B_SMALL_WINS, C_ALTERNATING, D_FALSE_REVERSE, E_ADVERSE_TREND, F_MAX_LEVELS, G_WORST_CASE.
- Sampled combinations: 25,000 from a theoretical grid of 9,676,800,000 combinations.
- Mathematically rejected or unstable rows in CSV: 24,978.
- P/L model: `Lot × Points × PointValuePerLot` minus spread/slippage/commission costs.
- Compression filter: `BigRatio² × RemainBigOnSmall < 1` plus simulated `NewBig < OldFar` checks.
- STOP_MAX_LEVELS, STATE_CLOSED_RECOVERY_LOSS, compression violations and drawdown/margin breaches receive hard penalties.

## Selected parameter sets

### SAFE

- StartLot=0.05, BigRatio=1.1, SmallRatio=0.35
- CloseBigOnSmall=0.3 / RemainBigOnSmall=0.7
- CloseFarShare=0.15 / ReserveShare=0.85, SmallReserveShare=0.1
- Trigger/steps: Initial=200, BigStart=150, BigStep=75, FarDistance=300
- MaxHarvestLevels=9, MaxReverseCycles=5, MaxSpreadPoints=30
- RecoveryPL mean/min/max: 2.04 / 0.3 / 4.72
- MaxDD=0.45, MaxMarginUsed=140.0, Score=1584.65, Verdict=ACCEPT
- Why selected: ACCEPT row with the best available score inside its risk category and no false AccountPL pass.

### BALANCED

- StartLot=0.05, BigRatio=1.15, SmallRatio=0.35
- CloseBigOnSmall=0.35 / RemainBigOnSmall=0.65
- CloseFarShare=0.25 / ReserveShare=0.75, SmallReserveShare=0.05
- Trigger/steps: Initial=70, BigStart=200, BigStep=75, FarDistance=300
- MaxHarvestLevels=8, MaxReverseCycles=7, MaxSpreadPoints=30
- RecoveryPL mean/min/max: 2.8 / 0.73 / 7.77
- MaxDD=0.94, MaxMarginUsed=140.0, Score=2036.63, Verdict=ACCEPT
- Why selected: ACCEPT row with the best available score inside its risk category and no false AccountPL pass.

### AGGRESSIVE

- StartLot=1.0, BigRatio=1.15, SmallRatio=0.35
- CloseBigOnSmall=0.3 / RemainBigOnSmall=0.7
- CloseFarShare=0.1 / ReserveShare=0.9, SmallReserveShare=0.07
- Trigger/steps: Initial=150, BigStart=200, BigStep=100, FarDistance=100
- MaxHarvestLevels=8, MaxReverseCycles=3, MaxSpreadPoints=30
- RecoveryPL mean/min/max: 59.42 / -142.65 / 155.49
- MaxDD=142.65, MaxMarginUsed=2560.0, Score=-1593.495, Verdict=REJECTED_RECOVERY_LOSS
- Why selected: stress-only candidate; offline model rejects it, so it must not be treated as a default until MT5 proves recovery profitability.

### LOWLOT_SAFE

- StartLot=0.05, BigRatio=1.1, SmallRatio=0.35
- CloseBigOnSmall=0.3 / RemainBigOnSmall=0.7
- CloseFarShare=0.4 / ReserveShare=0.6, SmallReserveShare=0.1
- Trigger/steps: Initial=150, BigStart=200, BigStep=75, FarDistance=300
- MaxHarvestLevels=5, MaxReverseCycles=5, MaxSpreadPoints=30
- RecoveryPL mean/min/max: 1.42 / 0.14 / 3.91
- MaxDD=0.45, MaxMarginUsed=140.0, Score=1082.3, Verdict=ACCEPT
- Why selected: ACCEPT row with the best available score inside its risk category and no false AccountPL pass.

## Top-20 by score

| Rank | RunID | Score | Verdict | StartLot | BigRatio | SmallRatio | CloseBig | Reserve | RecoveryPL_Min | MaxDD | StopMax | LossCount |
|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 15171 | 47965.915 | REJECTED_STOP_MAX_LEVELS | 0.05 | 1.25 | 0.35 | 0.4 | 0.6 | -0.02 | 1.83 | 1 | 1 |
| 2 | 4168 | 32227.38 | REJECTED_COMPRESSION | 0.05 | 1.18 | 0.3 | 0.35 | 0.9 | -0.06 | 3.41 | 0 | 1 |
| 3 | 6356 | 7433.645 | REJECTED_RECOVERY_LOSS | 0.05 | 1.18 | 0.35 | 0.4 | 0.75 | -0.2 | 1.13 | 0 | 1 |
| 4 | 12152 | 5736.02 | REJECTED_RECOVERY_LOSS | 0.05 | 1.1 | 0.3 | 0.35 | 0.75 | -0.21 | 3.88 | 0 | 2 |
| 5 | 24472 | 3989.98 | REJECTED_RECOVERY_LOSS | 0.05 | 1.05 | 0.3 | 0.5 | 0.75 | -0.2 | 5.44 | 0 | 3 |
| 6 | 11854 | 3751.035 | REJECTED_RECOVERY_LOSS | 0.1 | 1.15 | 0.35 | 0.3 | 0.85 | -1.09 | 3.86 | 0 | 1 |
| 7 | 2188 | 3355.33 | REJECTED_STOP_MAX_LEVELS | 0.05 | 1.2 | 0.35 | 0.4 | 0.9 | -0.16 | 1.95 | 1 | 2 |
| 8 | 9364 | 3181.825 | REJECTED_STOP_MAX_LEVELS | 0.05 | 1.15 | 0.35 | 0.45 | 0.9 | -0.16 | 1.8 | 1 | 2 |
| 9 | 2068 | 2777.625 | REJECTED_RECOVERY_LOSS | 0.05 | 1.18 | 0.35 | 0.45 | 0.9 | -0.12 | 1.68 | 0 | 3 |
| 10 | 17120 | 2745.91 | REJECTED_STOP_MAX_LEVELS | 0.05 | 1.1 | 0.35 | 0.5 | 0.8 | -0.2 | 0.73 | 1 | 1 |
| 11 | 11127 | 2528.805 | REJECTED_RECOVERY_LOSS | 0.05 | 1.18 | 0.35 | 0.4 | 0.6 | -0.2 | 1.13 | 0 | 3 |
| 12 | 2633 | 2118.035 | REJECTED_RECOVERY_LOSS | 0.1 | 1.1 | 0.35 | 0.3 | 0.75 | 0.06 | 3.86 | 0 | 1 |
| 13 | 18268 | 2036.63 | ACCEPT | 0.05 | 1.15 | 0.35 | 0.35 | 0.75 | 0.73 | 0.94 | 0 | 0 |
| 14 | 6164 | 1874.065 | REJECTED_RECOVERY_LOSS | 0.05 | 1.15 | 0.35 | 0.4 | 0.75 | 0.86 | 1.21 | 0 | 1 |
| 15 | 14396 | 1820.64 | REJECTED_RECOVERY_LOSS | 0.1 | 1.25 | 0.35 | 0.4 | 0.8 | 0.51 | 3.15 | 0 | 1 |
| 16 | 7143 | 1800.0 | REJECTED_RECOVERY_LOSS | 0.05 | 1.18 | 0.35 | 0.5 | 0.6 | -0.12 | 1.68 | 0 | 4 |
| 17 | 7406 | 1649.605 | ACCEPT | 0.05 | 1.12 | 0.35 | 0.35 | 0.75 | 0.07 | 0.59 | 0 | 0 |
| 18 | 10667 | 1584.65 | ACCEPT | 0.05 | 1.1 | 0.35 | 0.3 | 0.85 | 0.3 | 0.45 | 0 | 0 |
| 19 | 13564 | 1568.055 | ACCEPT | 0.05 | 1.12 | 0.35 | 0.35 | 0.8 | 0.07 | 0.6 | 0 | 0 |
| 20 | 13471 | 1559.975 | ACCEPT | 0.05 | 1.1 | 0.35 | 0.35 | 0.8 | 0.3 | 0.47 | 0 | 0 |

## Rejected parameter causes

Rows are rejected for failed compression math, simulated `NewBig >= OldFar`, margin/drawdown pressure, STOP_MAX_LEVELS, closed recovery loss, or non-positive minimum recovery across scenarios.
The most sensitive parameters are BigRatio, RemainBigOnSmall, FarDistancePoints, MaxHarvestLevels and CloseFarShare/ReserveShare.
Do not raise BigRatio or RemainBigOnSmall until `BigRatio² × RemainBigOnSmall < 1` and simulated `NewBig < OldFar` still hold.

## Required MT5 validation after offline filtering

Run every generated `.set` file in MT5 Strategy Tester:
1. USDJPY M30 2026.04.01 — 2026.06.17
2. USDJPY M30 2025.01.01 — 2026.06.17
3. EURUSD M30 2025.01.01 — 2026.06.17
4. GBPUSD M30 2025.01.01 — 2026.06.17
5. XAUUSD M30 2025.01.01 — 2026.06.17

Acceptance in MT5 still requires no STATE_INTEGRITY_ERROR, no STATE_RECOVERY_MISMATCH, no unresolved positions, no false STATE_CLOSED_PROFIT, and `OnTester > 0` only by real RecoveryPL.
