# Offline Best Parameters for MinusLock_BigHarvest_EA_V2

## Scope and limitations

This report is generated without MT5. It is a deterministic offline filter, not a replacement for MetaTrader Strategy Tester.
It uses the strict success rule `RecoveryPL = FinalBalance - CycleStartBalance`; AccountPL versus InitialDeposit is diagnostic only.
InitialIgnoredProfit is excluded from pass/fail, matching the EA realRecoveryPL / OnTester contract.
Rejected rows are never selectable for `.set` generation and always receive a hard score/final-rank penalty.

## Optimization model

- Synthetic scenarios: A_BIG_WINS, B_SMALL_WINS, C_ALTERNATING, D_FALSE_REVERSE, E_ADVERSE_TREND, F_MAX_LEVELS, G_WORST_CASE.
- Total combinations theoretical: 9,676,800,000.
- Total combinations tested: 110,000 (global=100,000, local=10,000).
- Coverage ratio: 0.00113674%.
- Mathematically rejected or unstable rows in CSV: 109,381.
- P/L model: `Lot × Points × PointValuePerLot` minus spread/slippage/commission costs.
- Compression filter: `BigRatio² × RemainBigOnSmall < 1` plus simulated `NewBig < OldFar` checks.
- Ranking is two-stage: Verdict first, then FinalRank only inside ACCEPT; TOP REJECTED is diagnostics only.
- STOP_MAX_LEVELS, STATE_CLOSED_RECOVERY_LOSS, compression violations and drawdown/margin breaches receive hard penalties.

## Selected parameter sets

LOWLOT candidate found at StartLot=0.05

### SAFE

- StartLot=0.05, BigRatio=1.12, SmallRatio=0.36
- CloseBigOnSmall=0.32 / RemainBigOnSmall=0.68
- CloseFarShare=0.2 / ReserveShare=0.8, SmallReserveShare=0.03
- Trigger/steps: Initial=100, BigStart=200, BigStep=75, FarDistance=300
- MaxHarvestLevels=9, MaxReverseCycles=10, MaxSpreadPoints=30
- RecoveryPL mean/min/max: 2.67 / 0.3 / 7.13
- MaxDD=0.45, MaxMarginUsed=140.0, ProfitScore=2093.96, StabilityScore=97.7714, RobustnessScore=100.0, FinalRank=2291.7314
- Verdict=ACCEPT, IsSelectableForSetFile=YES
- Why selected: ACCEPT row with the best available FinalRank inside its risk category and no false AccountPL pass.

### BALANCED

- StartLot=0.1, BigRatio=1.13, SmallRatio=0.37
- CloseBigOnSmall=0.34 / RemainBigOnSmall=0.66
- CloseFarShare=0.24 / ReserveShare=0.76, SmallReserveShare=0.1
- Trigger/steps: Initial=70, BigStart=150, BigStep=100, FarDistance=300
- MaxHarvestLevels=10, MaxReverseCycles=10, MaxSpreadPoints=30
- RecoveryPL mean/min/max: 6.76 / 1.02 / 12.66
- MaxDD=3.76, MaxMarginUsed=260.0, ProfitScore=4692.155, StabilityScore=94.2575, RobustnessScore=100.0, FinalRank=4886.4125
- Verdict=ACCEPT, IsSelectableForSetFile=YES
- Why selected: ACCEPT row with the best available FinalRank inside its risk category and no false AccountPL pass.

### AGGRESSIVE

- AGGRESSIVE_NOT_FOUND: no Verdict=ACCEPT candidate satisfied this category filter.

### LOWLOT_SAFE

- StartLot=0.05, BigRatio=1.12, SmallRatio=0.34
- CloseBigOnSmall=0.36 / RemainBigOnSmall=0.64
- CloseFarShare=0.22 / ReserveShare=0.78, SmallReserveShare=0.07
- Trigger/steps: Initial=150, BigStart=200, BigStep=75, FarDistance=300
- MaxHarvestLevels=8, MaxReverseCycles=5, MaxSpreadPoints=30
- RecoveryPL mean/min/max: 2.67 / 0.3 / 7.13
- MaxDD=0.45, MaxMarginUsed=140.0, ProfitScore=2093.96, StabilityScore=97.7714, RobustnessScore=100.0, FinalRank=2291.7314
- Verdict=ACCEPT, IsSelectableForSetFile=YES
- Why selected: ACCEPT row with the best available FinalRank inside its risk category and no false AccountPL pass.

## TOP ACCEPT

Only `Verdict=ACCEPT` rows are shown here and only these rows can create `.set` files.

| Rank | RunID | FinalRank | ProfitScore | StabilityScore | RobustnessScore | StartLot | BigRatio | SmallRatio | CloseBig | Reserve | RecoveryPL_Min | MaxDD |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 103840 | 4886.4125 | 4692.155 | 94.2575 | 100.0 | 0.1 | 1.13 | 0.37 | 0.34 | 0.76 | 1.02 | 3.76 |
| 2 | 109432 | 3915.4163 | 3719.755 | 95.6613 | 100.0 | 0.1 | 1.13 | 0.39 | 0.32 | 0.7 | 0.33 | 1.67 |
| 3 | 102896 | 3821.3137 | 3627.295 | 94.0187 | 100.0 | 0.1 | 1.15 | 0.39 | 0.36 | 0.8 | 0.33 | 4.11 |
| 4 | 105820 | 3602.3696 | 3408.245 | 94.1246 | 100.0 | 0.1 | 1.15 | 0.4 | 0.36 | 0.76 | 0.33 | 4.11 |
| 5 | 108522 | 3602.3696 | 3408.245 | 94.1246 | 100.0 | 0.1 | 1.14 | 0.39 | 0.36 | 0.74 | 0.33 | 4.11 |
| 6 | 103222 | 3186.7096 | 2992.575 | 94.1346 | 100.0 | 0.1 | 1.13 | 0.39 | 0.38 | 0.8 | 0.33 | 4.11 |
| 7 | 100459 | 3055.4196 | 2859.565 | 95.8546 | 100.0 | 0.1 | 1.13 | 0.39 | 0.3 | 0.78 | 0.11 | 0.91 |
| 8 | 109477 | 3055.4196 | 2859.565 | 95.8546 | 100.0 | 0.1 | 1.13 | 0.38 | 0.3 | 0.76 | 0.11 | 0.91 |
| 9 | 108192 | 3051.8443 | 2856.205 | 95.6393 | 100.0 | 0.1 | 1.12 | 0.4 | 0.34 | 0.8 | 0.07 | 1.67 |
| 10 | 104608 | 3024.226 | 2828.55 | 95.676 | 100.0 | 0.1 | 1.14 | 0.39 | 0.36 | 0.7 | 0.33 | 4.11 |
| 11 | 104617 | 3024.226 | 2828.55 | 95.676 | 100.0 | 0.1 | 1.15 | 0.4 | 0.38 | 0.72 | 0.33 | 4.11 |
| 12 | 108141 | 2968.2079 | 2773.53 | 94.6779 | 100.0 | 0.1 | 1.13 | 0.4 | 0.38 | 0.76 | 0.33 | 4.11 |
| 13 | 108163 | 2895.5593 | 2699.16 | 96.3993 | 100.0 | 0.1 | 1.12 | 0.4 | 0.36 | 0.7 | 1.47 | 4.11 |
| 14 | 106871 | 2720.1583 | 2522.465 | 97.6933 | 100.0 | 0.1 | 1.14 | 0.4 | 0.38 | 0.8 | 0.33 | 1.59 |
| 15 | 100709 | 2574.204 | 2377.43 | 96.774 | 100.0 | 0.1 | 1.16 | 0.37 | 0.32 | 0.76 | 0.8 | 4.1 |
| 16 | 101976 | 2528.7535 | 2333.075 | 95.6785 | 100.0 | 0.1 | 1.12 | 0.38 | 0.4 | 0.8 | 0.34 | 1.59 |
| 17 | 105569 | 2528.7535 | 2333.075 | 95.6785 | 100.0 | 0.1 | 1.12 | 0.38 | 0.38 | 0.78 | 0.34 | 1.59 |
| 18 | 55566 | 2444.947 | 2247.89 | 97.057 | 100.0 | 0.05 | 1.1 | 0.35 | 0.35 | 0.9 | 0.07 | 0.59 |
| 19 | 101804 | 2441.3298 | 2244.685 | 96.6448 | 100.0 | 0.05 | 1.13 | 0.4 | 0.36 | 0.7 | 0.49 | 1.21 |
| 20 | 102788 | 2441.3298 | 2244.685 | 96.6448 | 100.0 | 0.05 | 1.14 | 0.4 | 0.32 | 0.7 | 0.49 | 1.21 |

## TOP REJECTED

Diagnostics only: rejected rows have `IsSelectableForSetFile=NO`, penalized Score, and `FinalRank=-999999999.0`.

| Rank | RunID | Score | FinalRank | Verdict | StartLot | BigRatio | SmallRatio | RecoveryPL_Min | StopMax | LossCount | Compression |
|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 106131 | -939597.48 | -999999999.0 | REJECTED_STOP_MAX_LEVELS | 0.05 | 1.18 | 0.36 | -0.03 | 1 | 2 | 0 |
| 2 | 15171 | -952034.085 | -999999999.0 | REJECTED_STOP_MAX_LEVELS | 0.05 | 1.25 | 0.35 | -0.02 | 1 | 1 | 0 |
| 3 | 103609 | -963298.605 | -999999999.0 | REJECTED_COMPRESSION | 0.05 | 1.17 | 0.3 | -0.06 | 0 | 1 | 5 |
| 4 | 99571 | -965699.82 | -999999999.0 | REJECTED_COMPRESSION | 0.05 | 1.18 | 0.3 | -0.06 | 0 | 2 | 6 |
| 5 | 4168 | -967772.62 | -999999999.0 | REJECTED_COMPRESSION | 0.05 | 1.18 | 0.3 | -0.06 | 0 | 1 | 4 |
| 6 | 106417 | -967922.15 | -999999999.0 | REJECTED_COMPRESSION | 0.05 | 1.17 | 0.33 | -0.06 | 0 | 2 | 4 |
| 7 | 39373 | -972555.355 | -999999999.0 | REJECTED_COMPRESSION | 0.1 | 1.2 | 0.35 | -0.16 | 0 | 1 | 2 |
| 8 | 104497 | -975298.04 | -999999999.0 | REJECTED_COMPRESSION | 0.05 | 1.17 | 0.32 | -0.06 | 0 | 1 | 5 |
| 9 | 100294 | -976466.935 | -999999999.0 | REJECTED_COMPRESSION | 0.05 | 1.17 | 0.33 | -0.06 | 0 | 2 | 4 |
| 10 | 101677 | -976466.935 | -999999999.0 | REJECTED_COMPRESSION | 0.05 | 1.17 | 0.31 | -0.06 | 0 | 2 | 4 |
| 11 | 105003 | -976566.4 | -999999999.0 | REJECTED_COMPRESSION | 0.05 | 1.17 | 0.31 | -0.06 | 0 | 1 | 5 |
| 12 | 107865 | -982604.255 | -999999999.0 | REJECTED_RECOVERY_LOSS | 0.1 | 1.16 | 0.36 | -0.18 | 0 | 1 | 0 |
| 13 | 101349 | -984249.235 | -999999999.0 | REJECTED_RECOVERY_LOSS | 0.1 | 1.13 | 0.4 | -0.17 | 0 | 1 | 0 |
| 14 | 107124 | -985489.345 | -999999999.0 | REJECTED_STOP_MAX_LEVELS | 0.1 | 1.16 | 0.35 | -0.13 | 1 | 1 | 0 |
| 15 | 107655 | -985782.76 | -999999999.0 | REJECTED_RECOVERY_LOSS | 0.1 | 1.15 | 0.4 | -0.17 | 0 | 1 | 0 |
| 16 | 105173 | -985949.46 | -999999999.0 | REJECTED_RECOVERY_LOSS | 0.1 | 1.14 | 0.4 | -0.17 | 0 | 1 | 0 |
| 17 | 100087 | -986699.485 | -999999999.0 | REJECTED_RECOVERY_LOSS | 0.1 | 1.13 | 0.4 | -0.17 | 0 | 1 | 0 |
| 18 | 106577 | -986699.485 | -999999999.0 | REJECTED_RECOVERY_LOSS | 0.1 | 1.15 | 0.39 | -0.17 | 0 | 1 | 0 |
| 19 | 107590 | -987992.83 | -999999999.0 | REJECTED_RECOVERY_LOSS | 0.1 | 1.15 | 0.4 | -0.17 | 0 | 1 | 0 |
| 20 | 104363 | -988108.985 | -999999999.0 | REJECTED_RECOVERY_LOSS | 0.1 | 1.16 | 0.37 | -0.18 | 0 | 1 | 0 |

## Why rejected

- REJECTED_STOP_MAX_LEVELS: 82,290 rows rejected by hard filters or simulated scenario outcomes.
- REJECTED_RECOVERY_LOSS: 14,408 rows rejected by hard filters or simulated scenario outcomes.
- REJECTED_COMPRESSION_FORMULA: 8,545 rows rejected by hard filters or simulated scenario outcomes.
- REJECTED_COMPRESSION: 4,137 rows rejected by hard filters or simulated scenario outcomes.
- REJECTED_NON_POSITIVE_MIN_RECOVERY: 1 rows rejected by hard filters or simulated scenario outcomes.

Typical causes:
- REJECTED_COMPRESSION: simulated `NewBig >= OldFar` or other compression failure after Small scenario.
- REJECTED_STOP_MAX_LEVELS: scenario reached MaxHarvestLevels and closed by STOP_MAX_LEVELS instead of profit.
- REJECTED_RECOVERY_LOSS / REJECTED_NON_POSITIVE_MIN_RECOVERY: at least one scenario failed the real RecoveryPL criterion.
- REJECTED_MARGIN / REJECTED_DRAWDOWN: offline stress exceeded configured risk caps.

## Sensitivity Analysis

- BigRatio and RemainBigOnSmall are the most dangerous geometry pair because `BigRatio² × RemainBigOnSmall` controls compression.
- BigRatio above 1.20 or RemainBigOnSmall above 0.65 sharply narrows the safe compression zone in the offline model.
- SmallRatio below 0.20 weakens recovery in Small-heavy scenarios; values around 0.30–0.40 survive more local-search scenarios.
- CloseFarShare that is too high can starve reserve; too low can leave Far exposure unresolved and push MaxLevels.
- Wider MaxSpreadPoints reduces RecoveryPL_Min and can convert otherwise acceptable sets into recovery-loss rejects.

## Stability analysis

StabilityScore penalizes RecoveryPL variance, drawdown variance, STOP_MAX_LEVELS frequency and recovery-loss frequency. Higher is better; negative values indicate scenario instability even if mean RecoveryPL is high.

## Robustness analysis

RobustnessScore measures how many synthetic scenarios closed profitably and subtracts penalties for compression, STOP_MAX_LEVELS and recovery-loss events. ACCEPT requires all scenarios to remain structurally valid and profitable by real RecoveryPL.

## Required MT5 validation after offline filtering

Run every generated `.set` file in MT5 Strategy Tester:
1. USDJPY M30 2026.04.01 — 2026.06.17
2. USDJPY M30 2025.01.01 — 2026.06.17
3. EURUSD M30 2025.01.01 — 2026.06.17
4. GBPUSD M30 2025.01.01 — 2026.06.17
5. XAUUSD M30 2025.01.01 — 2026.06.17

Acceptance in MT5 still requires no STATE_INTEGRITY_ERROR, no STATE_RECOVERY_MISMATCH, no unresolved positions, no false STATE_CLOSED_PROFIT, and `OnTester > 0` only by real RecoveryPL.
