# Offline Best Parameters for MinusLock_BigHarvest_EA_V2

## Scope and limitations

This report is generated without MT5. It is a deterministic offline filter, not a replacement for MetaTrader Strategy Tester.
It uses the strict success rule `RecoveryPL = FinalBalance - CycleStartBalance`; AccountPL versus InitialDeposit is diagnostic only.
InitialIgnoredProfit is excluded from pass/fail, matching the EA realRecoveryPL / OnTester contract.
Rejected rows are diagnostics only: they cannot enter TOP ACCEPT and cannot generate production `.set` files.

## Optimization model

- Synthetic scenarios: A_BIG_WINS, B_SMALL_WINS, C_ALTERNATING, D_FALSE_REVERSE, E_ADVERSE_TREND, F_MAX_LEVELS, G_WORST_CASE.
- Total combinations theoretical: 9,676,800,000.
- Total combinations tested: 110,000 (100,000 broad + 10,000 local mini-search).
- Coverage ratio: 0.001137%.
- Mathematically rejected or unstable rows in CSV: 109,659.
- P/L model: `Lot × Points × PointValuePerLot` minus spread/slippage/commission costs.
- Compression filter: `BigRatio² × RemainBigOnSmall < 1` plus simulated `NewBig < OldFar` checks.
- FinalRank = ProfitScore + StabilityScore + RobustnessScore only for ACCEPT rows; rejected rows receive a terminal rank penalty.

## Selected ACCEPT parameter sets

LOWLOT candidate found at StartLot=0.05.

### SAFE

- StartLot=0.05, BigRatio=1.12, SmallRatio=0.34
- CloseBigOnSmall=0.32 / RemainBigOnSmall=0.68
- CloseFarShare=0.3 / ReserveShare=0.7, SmallReserveShare=0.03
- Trigger/steps: Initial=100, BigStart=100, BigStep=100, FarDistance=300
- MaxHarvestLevels=6, MaxReverseCycles=7, MaxSpreadPoints=30
- RecoveryPL mean/min/max: 2.5 / 0.3 / 4.96
- MaxDD=0.45, MaxMarginUsed=140.0, StabilityScore=98.0889, RobustnessScore=100.0, FinalRank=2230.6839, Verdict=ACCEPT
- Why selected: ACCEPT row with the best available FinalRank inside its risk category and no false AccountPL pass.

### BALANCED

- StartLot=0.1, BigRatio=1.16, SmallRatio=0.38
- CloseBigOnSmall=0.4 / RemainBigOnSmall=0.6
- CloseFarShare=0.22 / ReserveShare=0.78, SmallReserveShare=0.05
- Trigger/steps: Initial=200, BigStart=200, BigStep=75, FarDistance=300
- MaxHarvestLevels=9, MaxReverseCycles=10, MaxSpreadPoints=30
- RecoveryPL mean/min/max: 4.58 / 0.13 / 10.38
- MaxDD=4.11, MaxMarginUsed=270.0, StabilityScore=94.959, RobustnessScore=100.0, FinalRank=3462.274, Verdict=ACCEPT
- Why selected: ACCEPT row with the best available FinalRank inside its risk category and no false AccountPL pass.

### AGGRESSIVE

- AGGRESSIVE_NOT_FOUND: no ACCEPT candidate matched this category. No `.set` file was generated from a rejected row.

### LOWLOT_SAFE

- StartLot=0.05, BigRatio=1.1, SmallRatio=0.35
- CloseBigOnSmall=0.35 / RemainBigOnSmall=0.65
- CloseFarShare=0.1 / ReserveShare=0.9, SmallReserveShare=0.07
- Trigger/steps: Initial=70, BigStart=150, BigStep=100, FarDistance=250
- MaxHarvestLevels=7, MaxReverseCycles=10, MaxSpreadPoints=30
- RecoveryPL mean/min/max: 2.95 / 0.07 / 8.03
- MaxDD=0.59, MaxMarginUsed=140.0, StabilityScore=97.057, RobustnessScore=100.0, FinalRank=2516.127, Verdict=ACCEPT
- Why selected: ACCEPT row with the best available FinalRank inside its risk category and no false AccountPL pass.

## TOP ACCEPT

| Rank | RunID | FinalRank | ProfitScore | StabilityScore | RobustnessScore | StartLot | BigRatio | SmallRatio | CloseBig | CloseFar | RecoveryPL_Min | MaxDD | Verdict |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 107668 | 3462.274 | 3267.315 | 94.959 | 100.0 | 0.1 | 1.16 | 0.38 | 0.4 | 0.22 | 0.13 | 4.11 | ACCEPT |
| 2 | 102168 | 3019.5995 | 2822.775 | 96.8245 | 100.0 | 0.1 | 1.15 | 0.38 | 0.36 | 0.2 | 0.33 | 1.58 | ACCEPT |
| 3 | 108460 | 2976.1717 | 2780.335 | 95.8367 | 100.0 | 0.1 | 1.12 | 0.34 | 0.3 | 0.2 | 0.11 | 3.86 | ACCEPT |
| 4 | 103040 | 2850.1518 | 2655.335 | 94.8168 | 100.0 | 0.1 | 1.12 | 0.38 | 0.38 | 0.28 | 0.61 | 2.5 | ACCEPT |
| 5 | 55566 | 2516.127 | 2319.07 | 97.057 | 100.0 | 0.05 | 1.1 | 0.35 | 0.35 | 0.1 | 0.07 | 0.59 | ACCEPT |
| 6 | 100001 | 2516.127 | 2319.07 | 97.057 | 100.0 | 0.05 | 1.1 | 0.35 | 0.35 | 0.1 | 0.07 | 0.59 | ACCEPT |
| 7 | 102063 | 2513.7498 | 2317.105 | 96.6448 | 100.0 | 0.05 | 1.13 | 0.34 | 0.34 | 0.3 | 0.49 | 1.21 | ACCEPT |
| 8 | 102105 | 2513.7498 | 2317.105 | 96.6448 | 100.0 | 0.05 | 1.13 | 0.35 | 0.34 | 0.3 | 0.49 | 1.21 | ACCEPT |
| 9 | 101591 | 2468.1132 | 2271.505 | 96.6082 | 100.0 | 0.05 | 1.16 | 0.35 | 0.32 | 0.24 | 0.49 | 1.21 | ACCEPT |
| 10 | 102717 | 2468.1132 | 2271.505 | 96.6082 | 100.0 | 0.05 | 1.16 | 0.4 | 0.32 | 0.2 | 0.49 | 1.21 | ACCEPT |
| 11 | 103179 | 2468.1132 | 2271.505 | 96.6082 | 100.0 | 0.05 | 1.15 | 0.38 | 0.4 | 0.24 | 0.49 | 1.21 | ACCEPT |
| 12 | 104290 | 2468.1132 | 2271.505 | 96.6082 | 100.0 | 0.05 | 1.16 | 0.38 | 0.4 | 0.2 | 0.49 | 1.21 | ACCEPT |
| 13 | 104735 | 2468.1132 | 2271.505 | 96.6082 | 100.0 | 0.05 | 1.14 | 0.39 | 0.34 | 0.28 | 0.49 | 1.21 | ACCEPT |
| 14 | 105340 | 2468.1132 | 2271.505 | 96.6082 | 100.0 | 0.05 | 1.13 | 0.38 | 0.4 | 0.24 | 0.49 | 1.21 | ACCEPT |
| 15 | 108097 | 2468.1132 | 2271.505 | 96.6082 | 100.0 | 0.05 | 1.14 | 0.35 | 0.3 | 0.2 | 0.49 | 1.21 | ACCEPT |
| 16 | 109852 | 2432.6569 | 2234.895 | 97.7619 | 100.0 | 0.05 | 1.16 | 0.35 | 0.34 | 0.24 | 0.99 | 1.06 | ACCEPT |
| 17 | 107558 | 2408.6594 | 2212.59 | 96.0694 | 100.0 | 0.1 | 1.14 | 0.39 | 0.4 | 0.22 | 0.02 | 1.58 | ACCEPT |
| 18 | 18268 | 2305.8931 | 2108.51 | 97.3831 | 100.0 | 0.05 | 1.15 | 0.35 | 0.35 | 0.25 | 0.73 | 0.94 | ACCEPT |
| 19 | 101641 | 2305.8931 | 2108.51 | 97.3831 | 100.0 | 0.05 | 1.15 | 0.38 | 0.3 | 0.3 | 0.73 | 0.94 | ACCEPT |
| 20 | 102060 | 2305.8931 | 2108.51 | 97.3831 | 100.0 | 0.05 | 1.15 | 0.35 | 0.38 | 0.24 | 0.73 | 0.94 | ACCEPT |

## TOP REJECTED

| Rank | RunID | ScoreAfterPenalty | Verdict | StartLot | BigRatio | SmallRatio | CloseBig | CloseFar | RecoveryPL_Min | StopMax | LossCount | CompressionRatio |
|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 15171 | -952034.085 | REJECTED_STOP_MAX_LEVELS | 0.05 | 1.25 | 0.35 | 0.4 | 0.4 | -0.02 | 1 | 1 | 1.0 |
| 2 | 99571 | -965699.82 | REJECTED_COMPRESSION | 0.05 | 1.18 | 0.3 | 0.3 | 0.1 | -0.06 | 0 | 2 | 1.0 |
| 3 | 4168 | -967772.62 | REJECTED_COMPRESSION | 0.05 | 1.18 | 0.3 | 0.35 | 0.1 | -0.06 | 0 | 1 | 1.0 |
| 4 | 108314 | -969673.15 | REJECTED_COMPRESSION | 0.05 | 1.18 | 0.32 | 0.34 | 0.24 | -0.06 | 0 | 2 | 1.0 |
| 5 | 103926 | -970643.08 | REJECTED_STOP_MAX_LEVELS | 0.1 | 1.16 | 0.35 | 0.4 | 0.26 | -0.13 | 1 | 1 | 1.0 |
| 6 | 39373 | -972555.355 | REJECTED_COMPRESSION | 0.1 | 1.2 | 0.35 | 0.35 | 0.2 | -0.16 | 0 | 1 | 1.0 |
| 7 | 106353 | -977799.375 | REJECTED_COMPRESSION | 0.05 | 1.17 | 0.31 | 0.32 | 0.24 | -0.06 | 0 | 2 | 1.0 |
| 8 | 109909 | -988532.44 | REJECTED_COMPRESSION | 0.05 | 1.17 | 0.33 | 0.36 | 0.24 | -0.06 | 0 | 1 | 1.0 |
| 9 | 108871 | -990349.395 | REJECTED_STOP_MAX_LEVELS | 0.1 | 1.13 | 0.37 | 0.32 | 0.28 | -0.07 | 2 | 3 | 1.0 |
| 10 | 105921 | -990461.41 | REJECTED_RECOVERY_LOSS | 0.1 | 1.14 | 0.38 | 0.36 | 0.3 | -0.17 | 0 | 1 | 1.0 |
| 11 | 88912 | -991000.43 | REJECTED_STOP_MAX_LEVELS | 0.05 | 1.15 | 0.35 | 0.35 | 0.3 | -0.09 | 1 | 1 | 1.0 |
| 12 | 103721 | -991000.43 | REJECTED_STOP_MAX_LEVELS | 0.05 | 1.16 | 0.4 | 0.4 | 0.28 | -0.09 | 1 | 1 | 1.0 |
| 13 | 51991 | -991035.38 | REJECTED_COMPRESSION | 0.05 | 1.2 | 0.3 | 0.35 | 0.15 | -0.21 | 0 | 2 | 1.0 |
| 14 | 30125 | -991173.425 | REJECTED_COMPRESSION | 0.05 | 1.18 | 0.35 | 0.3 | 0.1 | -0.23 | 0 | 1 | 1.0 |
| 15 | 51025 | -991371.965 | REJECTED_STOP_MAX_LEVELS | 0.05 | 1.18 | 0.35 | 0.5 | 0.4 | -0.08 | 1 | 1 | 1.0 |
| 16 | 102514 | -991504.685 | REJECTED_STOP_MAX_LEVELS | 0.05 | 1.12 | 0.35 | 0.4 | 0.26 | -0.08 | 1 | 1 | 1.0 |
| 17 | 65977 | -991551.395 | REJECTED_COMPRESSION | 0.05 | 1.18 | 0.3 | 0.3 | 0.15 | -0.21 | 0 | 4 | 1.0 |
| 18 | 107896 | -991674.285 | REJECTED_STOP_MAX_LEVELS | 0.05 | 1.16 | 0.38 | 0.36 | 0.3 | -0.14 | 1 | 2 | 1.0 |
| 19 | 109635 | -992120.905 | REJECTED_RECOVERY_LOSS | 0.1 | 1.15 | 0.4 | 0.34 | 0.26 | -0.17 | 0 | 1 | 1.0 |
| 20 | 62037 | -992427.895 | REJECTED_COMPRESSION | 0.1 | 1.18 | 0.35 | 0.3 | 0.1 | -0.63 | 0 | 1 | 1.0 |

## Why rejected

- REJECTED_STOP_MAX_LEVELS: 83,741 rows. These rows remain in CSV for diagnostics but are not selectable for `.set` generation.
- REJECTED_RECOVERY_LOSS: 12,566 rows. These rows remain in CSV for diagnostics but are not selectable for `.set` generation.
- REJECTED_COMPRESSION_FORMULA: 8,545 rows. These rows remain in CSV for diagnostics but are not selectable for `.set` generation.
- REJECTED_COMPRESSION: 4,807 rows. These rows remain in CSV for diagnostics but are not selectable for `.set` generation.

## Sensitivity Analysis

- BigRatio and RemainBigOnSmall are the most dangerous pair because `BigRatio² × RemainBigOnSmall >= 1` breaks compression before simulation.
- BigRatio above 1.20 sharply narrows the ACCEPT region unless CloseBigOnSmall is high enough to keep the next Big below the old Far.
- SmallRatio below 0.20 often weakens Small-scenario recovery; very high SmallRatio increases hedge cost and drawdown variance.
- CloseFarShare above 0.30 may reduce reserve resilience; too little CloseFarShare leaves large final Far losses.
- FarDistancePoints and BigMoveStepPoints materially change RecoveryPL variance and must be revalidated in MT5 tick data.

## Stability analysis

StabilityScore penalizes RecoveryPL variance, drawdown variance, STOP_MAX_LEVELS frequency and recovery-loss frequency. Higher values indicate a smoother cross-scenario profile.

## Robustness analysis

RobustnessScore measures how many synthetic paths close profitably and subtracts penalties for STOP_MAX_LEVELS, recovery loss and compression violations across Big trend, Small trend, alternating, false reversal, worst-case and max-level stress paths.

## Required MT5 validation after offline filtering

Run every generated `.set` file in MT5 Strategy Tester:
1. USDJPY M30 2026.04.01 — 2026.06.17
2. USDJPY M30 2025.01.01 — 2026.06.17
3. EURUSD M30 2025.01.01 — 2026.06.17
4. GBPUSD M30 2025.01.01 — 2026.06.17
5. XAUUSD M30 2025.01.01 — 2026.06.17

Acceptance in MT5 still requires no STATE_INTEGRITY_ERROR, no STATE_RECOVERY_MISMATCH, no unresolved positions, no false STATE_CLOSED_PROFIT, and `OnTester > 0` only by real RecoveryPL.
