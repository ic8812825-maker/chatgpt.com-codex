# Parameter Geometry Sweep Report

## 1. Цель подбора

Проведён полный Python-sweep геометрии MinusLock_BigHarvest_EA, чтобы найти кандидаты для MT5 Strategy Tester. PASS в модели считается только как предварительный кандидат: финально подтверждать нужно по RealRecoveryPL в MT5.

## 2. Почему текущая геометрия слабая

Текущий набор 1.30 / 0.37 / 0.30 даёт CompressionRatio = 1.30 × 0.70 = 0.91, то есть хвост после Small-at-Far уменьшается только примерно на 9%. Этот набор был отфильтрован правилом: CompressionRatio >= 0.90.

## 3. Формула CompressionRatio

```text
CompressionRatio = BigRatio × RemainBigOnSmall
RemainBigOnSmall = 1 - CloseBigOnSmall
NewFarLot = OldFarLot × CompressionRatio
```

## 4. Формула BigNetPower

```text
BigNetPower = BigRatio × (1 - SmallRatio)
```

## 5. Фильтры плохих комбинаций

Raw combinations: 17640. Filtered combinations: 11160. Tested combinations: 6480. Scenarios per combination: 7.

Фильтры: CloseBigOnSmall < SmallRatio, CompressionRatio между 0.60 и 0.90, BigNetPower >= 0.65, SmallRatio < 0.60, CloseBigOnSmall < 0.65.

## 6. Таблица Top 10

| Rank | Score | BigRatio | SmallRatio | CloseBigOnSmall | RemainBigOnSmall | CloseFarShare | ReserveShare | MaxHarvestLevels | MaxReverseCycles | CompressionRatio | BigNetPower | PassCount | StopMaxLevelsCount | RealFailSequencePL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 750 | 1.25 | 0.37 | 0.35 | 0.65 | 0.4 | 0.6 | 7 | 3 | 0.8125 | 0.7875 | 4 | 0 | 47.4 |
| 2 | 750 | 1.25 | 0.37 | 0.35 | 0.65 | 0.4 | 0.6 | 7 | 5 | 0.8125 | 0.7875 | 4 | 0 | 47.4 |
| 3 | 750 | 1.25 | 0.37 | 0.35 | 0.65 | 0.4 | 0.6 | 7 | 10 | 0.8125 | 0.7875 | 4 | 0 | 47.4 |
| 4 | 750 | 1.25 | 0.37 | 0.35 | 0.65 | 0.4 | 0.6 | 10 | 3 | 0.8125 | 0.7875 | 4 | 0 | 47.4 |
| 5 | 750 | 1.25 | 0.37 | 0.35 | 0.65 | 0.4 | 0.6 | 10 | 5 | 0.8125 | 0.7875 | 4 | 0 | 47.4 |
| 6 | 750 | 1.25 | 0.37 | 0.35 | 0.65 | 0.4 | 0.6 | 10 | 10 | 0.8125 | 0.7875 | 4 | 0 | 47.4 |
| 7 | 750 | 1.35 | 0.42 | 0.4 | 0.6 | 0.4 | 0.6 | 7 | 3 | 0.81 | 0.783 | 4 | 0 | 46.8 |
| 8 | 750 | 1.35 | 0.42 | 0.4 | 0.6 | 0.4 | 0.6 | 7 | 5 | 0.81 | 0.783 | 4 | 0 | 46.8 |
| 9 | 750 | 1.35 | 0.42 | 0.4 | 0.6 | 0.4 | 0.6 | 7 | 10 | 0.81 | 0.783 | 4 | 0 | 46.8 |
| 10 | 750 | 1.35 | 0.42 | 0.4 | 0.6 | 0.4 | 0.6 | 10 | 3 | 0.81 | 0.783 | 4 | 0 | 46.8 |

## 7. Таблица Worst 10

| Rank | Score | BigRatio | SmallRatio | CloseBigOnSmall | RemainBigOnSmall | CloseFarShare | ReserveShare | MaxHarvestLevels | MaxReverseCycles | CompressionRatio | BigNetPower | PassCount | StopMaxLevelsCount | RealFailSequencePL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 70 | 1.3 | 0.5 | 0.35 | 0.65 | 0.9 | 0.1 | 5 | 3 | 0.845 | 0.65 | 2 | 2 | 6.5 |
| 2 | 70 | 1.3 | 0.5 | 0.35 | 0.65 | 0.9 | 0.1 | 5 | 5 | 0.845 | 0.65 | 2 | 2 | 6.5 |
| 3 | 70 | 1.3 | 0.5 | 0.35 | 0.65 | 0.9 | 0.1 | 5 | 10 | 0.845 | 0.65 | 2 | 2 | 6.5 |
| 4 | 70 | 1.3 | 0.5 | 0.35 | 0.65 | 0.9 | 0.1 | 7 | 3 | 0.845 | 0.65 | 2 | 2 | 6.5 |
| 5 | 70 | 1.3 | 0.5 | 0.35 | 0.65 | 0.9 | 0.1 | 7 | 5 | 0.845 | 0.65 | 2 | 2 | 6.5 |
| 6 | 70 | 1.3 | 0.5 | 0.35 | 0.65 | 0.9 | 0.1 | 7 | 10 | 0.845 | 0.65 | 2 | 2 | 6.5 |
| 7 | 70 | 1.3 | 0.5 | 0.35 | 0.65 | 0.9 | 0.1 | 10 | 3 | 0.845 | 0.65 | 2 | 2 | 6.5 |
| 8 | 70 | 1.3 | 0.5 | 0.35 | 0.65 | 0.9 | 0.1 | 10 | 5 | 0.845 | 0.65 | 2 | 2 | 6.5 |
| 9 | 70 | 1.3 | 0.5 | 0.35 | 0.65 | 0.9 | 0.1 | 10 | 10 | 0.845 | 0.65 | 2 | 2 | 6.5 |
| 10 | 70 | 1.2 | 0.45 | 0.3 | 0.7 | 0.9 | 0.1 | 5 | 3 | 0.84 | 0.66 | 2 | 2 | 6.6 |

## 8. Проверка текущего кандидата

- BigRatio: 1.3
- SmallRatio: 0.37
- CloseBigOnSmall: 0.3
- RemainBigOnSmall: 0.7
- CloseFarShare / ReserveShare: 0.7 / 0.3
- MaxHarvestLevels / MaxReverseCycles: 5 / 10
- CompressionRatio: 0.91
- BigNetPower: 0.819
- PassCount: 2 из 7
- StopMaxLevelsCount: 2
- RealFailSequencePL estimate: 24.6
- Score: 120
- FilterReason: CompressionRatio >= 0.90

## 9. Проверка сбалансированного кандидата

- BigRatio: 1.3
- SmallRatio: 0.42
- CloseBigOnSmall: 0.4
- RemainBigOnSmall: 0.6
- CloseFarShare / ReserveShare: 0.5 / 0.5
- MaxHarvestLevels / MaxReverseCycles: 5 / 10
- CompressionRatio: 0.78
- BigNetPower: 0.754
- PassCount: 3 из 7
- StopMaxLevelsCount: 1
- RealFailSequencePL estimate: 37.5
- Score: 500
- FilterReason: OK

## 10. Проверка сильного сжатия

- BigRatio: 1.3
- SmallRatio: 0.45
- CloseBigOnSmall: 0.42
- RemainBigOnSmall: 0.58
- CloseFarShare / ReserveShare: 0.5 / 0.5
- MaxHarvestLevels / MaxReverseCycles: 5 / 10
- CompressionRatio: 0.754
- BigNetPower: 0.715
- PassCount: 3 из 7
- StopMaxLevelsCount: 1
- RealFailSequencePL estimate: 35.5
- Score: 500
- FilterReason: OK

## 11. Лучший найденный набор

- BigRatio: 1.25
- SmallRatio: 0.37
- CloseBigOnSmall: 0.35
- RemainBigOnSmall: 0.65
- CloseFarShare: 0.4
- ReserveShare: 0.6
- MaxHarvestLevels: 7
- MaxReverseCycles: 3
- CompressionRatio: 0.8125
- BigNetPower: 0.7875
- Score: 750

## 12. Почему он выбран

Кандидат выбран Python-score: закрытые сценарии, положительная оценка recovery P/L, CompressionRatio в целевой зоне 0.70–0.82, BigNetPower >= 0.70, ReverseStrengthMin >= 0.15 и меньше штрафов за STOP_MAX_LEVELS/invalid geometry. Это математический кандидат, а не финальное доказательство прибыльности.

## 13. Риски

- Python-модель не заменяет MT5 Strategy Tester.
- RealRecoveryPLEstimate не учитывает реальные спреды, комиссии, свопы, проскальзывание и исполнение брокера.
- Все top-кандидаты нужно проверять с `FarDistanceMode = REAL_PRICE_DISTANCE` и `EnableCycleMathCsv = true`.
- OnTester в MT5 должен возвращать PASS только при `RealRecoveryPL > 0`.

## 14. Какие параметры нужно подтвердить в MT5

Подтвердить Top candidate, Second candidate и Conservative candidate из `mt5_parameter_confirmation_plan.md`; собрать Strategy Tester report, Experts log, `MinusLock_CycleMath.csv`, `REAL_CYCLE_MATH`, итоговый state и OnTester.
