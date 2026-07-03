# Big Scenario Trace Report

## Approved model

`BigScenarioNet = ClosedBigNet + ClosedSmallNet` is the approved Big-scenario harvest base. The simulator verifies that `CloseFarBudget` and `ReserveAdd` are calculated only from `BigScenarioNet`, and that reserve is not used for partial Far close.

## Trace: 90_10

| Level | FarLotBefore | BigLot | SmallLot | ClosedBigNet | ClosedSmallNet | BigScenarioNet | CloseFarBudget | ReserveAdd | CloseFarLotRounded | FarLotAfter | ReserveAfter | RecoveryPL | ReserveCoverage | NextAction |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1.00 | 1.15 | 0.29 | 115.00 | -29.00 | 86.00 | 77.40 | 8.60 | 0.38 | 0.62 | 8.60 | -115.40 | 0.0694 | NEXT_BIG_LEVEL |
| 2 | 0.62 | 0.71 | 0.18 | 71.00 | -18.00 | 53.00 | 47.70 | 5.30 | 0.23 | 0.39 | 13.90 | -64.10 | 0.1782 | NEXT_BIG_LEVEL |
| 3 | 0.39 | 0.45 | 0.12 | 45.00 | -12.00 | 33.00 | 29.70 | 3.30 | 0.14 | 0.25 | 17.20 | -32.80 | 0.3440 | NEXT_BIG_LEVEL |
| 4 | 0.25 | 0.29 | 0.08 | 29.00 | -8.00 | 21.00 | 18.90 | 2.10 | 0.09 | 0.16 | 19.30 | -12.70 | 0.6031 | NEXT_BIG_LEVEL |
| 5 | 0.16 | 0.18 | 0.05 | 18.00 | -5.00 | 13.00 | 11.70 | 1.30 | 0.05 | 0.11 | 20.60 | -1.40 | 0.9364 | NEXT_BIG_LEVEL |
| 6 | 0.11 | 0.13 | 0.04 | 13.00 | -4.00 | 9.00 | 8.10 | 0.90 | 0.04 | 0.07 | 21.50 | 7.50 | 1.5357 | FINAL_CLOSE |

Summary: TotalClosedFarLot=0.93, RemainingFarLot=0.07, ReserveAfter=21.5, LevelsToFinalClose=6, RecoveryPL=7.5, ReserveCoverage=1.53571429, FinalAction=FINAL_CLOSE.

## Trace: 20_80

| Level | FarLotBefore | BigLot | SmallLot | ClosedBigNet | ClosedSmallNet | BigScenarioNet | CloseFarBudget | ReserveAdd | CloseFarLotRounded | FarLotAfter | ReserveAfter | RecoveryPL | ReserveCoverage | NextAction |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1.00 | 1.15 | 0.29 | 115.00 | -29.00 | 86.00 | 17.20 | 68.80 | 0.08 | 0.92 | 68.80 | -115.20 | 0.3739 | NEXT_BIG_LEVEL |
| 2 | 0.92 | 1.06 | 0.27 | 106.00 | -27.00 | 79.00 | 15.80 | 63.20 | 0.07 | 0.85 | 132.00 | -38.00 | 0.7765 | NEXT_BIG_LEVEL |
| 3 | 0.85 | 0.98 | 0.25 | 98.00 | -25.00 | 73.00 | 14.60 | 58.40 | 0.07 | 0.78 | 190.40 | 34.40 | 1.2205 | FINAL_CLOSE |

Summary: TotalClosedFarLot=0.22, RemainingFarLot=0.78, ReserveAfter=190.4, LevelsToFinalClose=3, RecoveryPL=34.4, ReserveCoverage=1.22051282, FinalAction=FINAL_CLOSE.

## 90/10 vs 20/80 comparison

| Metric | 90/10 | 20/80 | Expected profile |
|---|---:|---:|---|
| TotalClosedFarLot | 0.93 | 0.22 | 90/10 closes Far faster |
| RemainingFarLot | 0.07 | 0.78 | 90/10 leaves less Far |
| ReserveAfter | 21.5 | 190.4 | 20/80 builds reserve faster |
| LevelsToFinalClose | 6 | 3 | profile-dependent |
| RecoveryPL | 7.5 | 34.4 | reserve/Far tradeoff |
| ReserveCoverage | 1.53571429 | 1.22051282 | profile-dependent |

Conclusion: 90/10 maximizes the part of `BigScenarioNet` allocated to partial Far close and does not use reserve for that partial close. 20/80 accumulates reserve faster but reduces Far more slowly.

