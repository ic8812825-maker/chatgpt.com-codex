# Refined Geometry Sweep Report

## 1. Зачем нужен второй refined sweep

Первый geometry sweep нашёл previous best вокруг `1.25 / 0.37 / 0.35 / 40/60 / 7 / 3`. Refined sweep сужает сетку вокруг него, чтобы проверить более тонкие значения и подготовить кандидатов для MT5 Strategy Tester.

## 2. Почему previous best был выбран

Previous best имел CompressionRatio = 0.8125, BigNetPower = 0.7875 и прежний score = 750. Это улучшило старую геометрию 0.91, но оставило пространство для поиска CompressionRatio ближе к 0.72–0.80 и ReserveShare 0.55–0.70.

## 3. Какие диапазоны проверены

- BigRatio: [1.2, 1.22, 1.25, 1.27, 1.3]
- SmallRatio: [0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42]
- CloseBigOnSmall: [0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39]
- CloseFarShare / ReserveShare: [(0.3, 0.7), (0.35, 0.65), (0.4, 0.6), (0.45, 0.55), (0.5, 0.5), (0.55, 0.45), (0.6, 0.4)]
- MaxHarvestLevels: [5, 7, 9]
- MaxReverseCycles: [2, 3, 5]

## 4. Сколько raw combinations

20160

## 5. Сколько filtered combinations

10143

## 6. Сколько tested combinations

10017; scenarios per combination = 9.

## 7. Какие фильтры применены

SmallRatio > CloseBigOnSmall, SmallCoverageGap >= 0.015, CompressionRatio between 0.68 and 0.86, BigNetPower >= 0.72, CloseFarShare + ReserveShare = 1.00, MaxHarvestLevels >= 5.

## 8. Top 10 candidates

| Rank | Score | BigRatio | SmallRatio | CloseBigOnSmall | RemainBigOnSmall | CloseFarShare | ReserveShare | MaxHarvestLevels | MaxReverseCycles | CompressionRatio | BigNetPower | SmallCoverageGap | PassCount | StopMaxLevelsCount | WorstCycleFinalPL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1510 | 1.2 | 0.35 | 0.32 | 0.68 | 0.45 | 0.55 | 7 | 2 | 0.816 | 0.78 | 0.03 | 4 | 0 | 0.0 |
| 2 | 1510 | 1.2 | 0.35 | 0.32 | 0.68 | 0.45 | 0.55 | 7 | 3 | 0.816 | 0.78 | 0.03 | 4 | 0 | 0.0 |
| 3 | 1510 | 1.2 | 0.35 | 0.32 | 0.68 | 0.45 | 0.55 | 7 | 5 | 0.816 | 0.78 | 0.03 | 4 | 0 | 0.0 |
| 4 | 1510 | 1.2 | 0.35 | 0.32 | 0.68 | 0.45 | 0.55 | 9 | 2 | 0.816 | 0.78 | 0.03 | 4 | 0 | 0.0 |
| 5 | 1510 | 1.2 | 0.35 | 0.32 | 0.68 | 0.45 | 0.55 | 9 | 3 | 0.816 | 0.78 | 0.03 | 4 | 0 | 0.0 |
| 6 | 1510 | 1.2 | 0.35 | 0.32 | 0.68 | 0.45 | 0.55 | 9 | 5 | 0.816 | 0.78 | 0.03 | 4 | 0 | 0.0 |
| 7 | 1510 | 1.2 | 0.35 | 0.33 | 0.67 | 0.45 | 0.55 | 7 | 2 | 0.804 | 0.78 | 0.02 | 4 | 0 | 0.0 |
| 8 | 1510 | 1.2 | 0.35 | 0.33 | 0.67 | 0.45 | 0.55 | 7 | 3 | 0.804 | 0.78 | 0.02 | 4 | 0 | 0.0 |
| 9 | 1510 | 1.2 | 0.35 | 0.33 | 0.67 | 0.45 | 0.55 | 7 | 5 | 0.804 | 0.78 | 0.02 | 4 | 0 | 0.0 |
| 10 | 1510 | 1.2 | 0.35 | 0.33 | 0.67 | 0.45 | 0.55 | 9 | 2 | 0.804 | 0.78 | 0.02 | 4 | 0 | 0.0 |

## 9. Worst 10 candidates

| Rank | Score | BigRatio | SmallRatio | CloseBigOnSmall | RemainBigOnSmall | CloseFarShare | ReserveShare | MaxHarvestLevels | MaxReverseCycles | CompressionRatio | BigNetPower | SmallCoverageGap | PassCount | StopMaxLevelsCount | WorstCycleFinalPL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 570 | 1.25 | 0.42 | 0.32 | 0.68 | 0.55 | 0.45 | 5 | 2 | 0.85 | 0.725 | 0.1 | 2 | 2 | -276.27 |
| 2 | 570 | 1.25 | 0.42 | 0.32 | 0.68 | 0.55 | 0.45 | 5 | 3 | 0.85 | 0.725 | 0.1 | 2 | 2 | -276.27 |
| 3 | 570 | 1.25 | 0.42 | 0.32 | 0.68 | 0.55 | 0.45 | 5 | 5 | 0.85 | 0.725 | 0.1 | 2 | 2 | -276.27 |
| 4 | 570 | 1.25 | 0.42 | 0.33 | 0.67 | 0.55 | 0.45 | 5 | 2 | 0.8375 | 0.725 | 0.09 | 2 | 2 | -276.27 |
| 5 | 570 | 1.25 | 0.42 | 0.33 | 0.67 | 0.55 | 0.45 | 5 | 3 | 0.8375 | 0.725 | 0.09 | 2 | 2 | -276.27 |
| 6 | 570 | 1.25 | 0.42 | 0.33 | 0.67 | 0.55 | 0.45 | 5 | 5 | 0.8375 | 0.725 | 0.09 | 2 | 2 | -276.27 |
| 7 | 570 | 1.25 | 0.42 | 0.32 | 0.68 | 0.6 | 0.4 | 5 | 2 | 0.85 | 0.725 | 0.1 | 2 | 2 | -266.9 |
| 8 | 570 | 1.25 | 0.42 | 0.32 | 0.68 | 0.6 | 0.4 | 5 | 3 | 0.85 | 0.725 | 0.1 | 2 | 2 | -266.9 |
| 9 | 570 | 1.25 | 0.42 | 0.32 | 0.68 | 0.6 | 0.4 | 5 | 5 | 0.85 | 0.725 | 0.1 | 2 | 2 | -266.9 |
| 10 | 570 | 1.25 | 0.42 | 0.33 | 0.67 | 0.6 | 0.4 | 5 | 2 | 0.8375 | 0.725 | 0.09 | 2 | 2 | -266.9 |

## 10. Previous Best vs Refined Best

| Metric | Previous Best | Refined Top | Difference |
|---|---:|---:|---:|
| Score | 1510 | 1510 | 0 |
| PassCount | 4 | 4 | 0 |
| StopMaxLevelsCount | 0 | 0 | 0 |
| CompressionRatio | 0.8125 | 0.816 | 0.0035 |
| BigNetPower | 0.7875 | 0.78 | -0.0075 |
| WorstCycleFinalPL | 0.0 | 0.0 | 0.0 |
| MaxOpenLots | 2.71 | 2.62 | -0.09 |
| MaxDrawdownEstimate | 541.5 | 503.5 | -38.0 |

## 11. Разбор CompressionRatio

Top candidate CompressionRatio = 0.816. Target zone is 0.72–0.82, so tail compression stays within the refined target while avoiding too-aggressive compression below 0.68.

## 12. Разбор BigNetPower

Top candidate BigNetPower = 0.78. It remains inside or above the target 0.74–0.82 band and above the hard filter 0.72.

## 13. Разбор SmallCoverageGap

Top candidate SmallCoverageGap = 0.03. The target is 0.02–0.05 so Small can cover the closed part of Big without making Big-harvest too weak.

## 14. Разбор ReserveShare

Top candidate ReserveShare = 0.55. Refined scoring gives a bonus for ReserveShare >= 0.55 because reserve protects final close validation.

## 15. Сценарий REAL_REPORT_SEQUENCE

Refined top: state = STATE_CLOSED_PROFIT, PL estimate = 42.9. This is still a Python estimate and must be validated by MT5 real history P/L.

## 16. Сценарий LONG_SMALL_PRESSURE

Refined top: state = STATE_CLOSED_PROFIT, PL estimate = 0.0. This scenario checks repeated Small-at-Far compression pressure.

## 17. Лучший кандидат

- BigRatio: 1.2
- SmallRatio: 0.35
- CloseBigOnSmall: 0.32
- RemainBigOnSmall: 0.68
- CloseFarShare / ReserveShare: 0.45 / 0.55
- MaxHarvestLevels / MaxReverseCycles: 7 / 2
- CompressionRatio: 0.816
- BigNetPower: 0.78
- SmallCoverageGap: 0.03
- PassCount: 4
- StopMaxLevelsCount: 0
- WorstCycleFinalPL: 0.0
- Score: 1510

## 18. Второй кандидат

- BigRatio: 1.2
- SmallRatio: 0.35
- CloseBigOnSmall: 0.32
- RemainBigOnSmall: 0.68
- CloseFarShare / ReserveShare: 0.45 / 0.55
- MaxHarvestLevels / MaxReverseCycles: 7 / 3
- CompressionRatio: 0.816
- BigNetPower: 0.78
- SmallCoverageGap: 0.03
- PassCount: 4
- StopMaxLevelsCount: 0
- WorstCycleFinalPL: 0.0
- Score: 1510

## 19. Консервативный кандидат

- BigRatio: 1.25
- SmallRatio: 0.38
- CloseBigOnSmall: 0.35
- RemainBigOnSmall: 0.65
- CloseFarShare / ReserveShare: 0.3 / 0.7
- MaxHarvestLevels / MaxReverseCycles: 7 / 3
- CompressionRatio: 0.8125
- BigNetPower: 0.775
- SmallCoverageGap: 0.03
- PassCount: 4
- StopMaxLevelsCount: 0
- WorstCycleFinalPL: 0.0
- Score: 1510

## 20. Риски

- Python-модель не заменяет MT5 Strategy Tester.
- `CycleFinalPL`/`RealRecoveryPLEstimate` are model estimates, not broker-executed P/L.
- MT5 must confirm `RealRecoveryPL > 0`, no managed open positions, and `OnTester > 0` only for real positive recovery.
- More reserve can reduce STOP risk but may slow Far-lot reduction; more Far close can reduce Far faster but can weaken final reserve.

## 21. Что подтвердить в MT5

Run Top, Second, and Conservative candidates from `refined_mt5_confirmation_plan.md` with `FarDistanceMode = REAL_PRICE_DISTANCE`, `EnableCycleMathCsv = true`, and real recovery validation enabled. Collect Strategy Tester report, Experts log, `MinusLock_CycleMath.csv`, `REAL_CYCLE_MATH`, final state, last close comment, and OnTester.
