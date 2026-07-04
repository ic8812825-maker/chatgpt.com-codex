# Full Parameter Optimization Engineering Report

## Scope and safety

This is an offline engineering optimization study for all `input` parameters in `Include/Config.mqh`. It does not change StateMachine, Geometry Engine, RecoveryMath, Trade Engine, opening/closing logic or order/state sequencing. Generated presets are candidates for MT5 validation, not MT5-approved final parameters.

## Search methodology

The study combines compact full-grid sweeps, deterministic random search, Latin-hypercube-style stratification, Bayesian-style exploitation around promising regions, and local refinement around the lowest-Big-level area. Ranking is lexicographic in spirit: Maximum Big Level, Big Levels, Max Open Positions, Recovery Duration, Max Drawdown, RecoveryPL, ReserveCoverage, then profit metrics.

## Generated files

- `Reports/Full_Parameter_Optimization_Candidates.csv`
- `Reports/Parameter_Optimization_Summary.csv`
- `Reports/Parameter_Sensitivity.csv`
- `Reports/Parameter_Dependency_Data.csv`
- `Sets/Optimization_Presets/*.set`

## Top candidates

| Rank | Method | Name | MaxBigLevel | BigLevels | OpenPositions | DurationBars | MaxDD% | RecoveryPL | ReserveCoverage | NetProfit | BigRatio | SmallRatio | CloseFarShare | GeometryMode |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Random Search | random_109 | 5 | 5 | 10 | 57 | 16.70 | 46.00 | 0.7300 | 33.11 | 1.18 | 0.40 | 0.90 | 4 |
| 2 | Random Search | random_152 | 5 | 5 | 10 | 57 | 16.70 | 15.40 | 1.0335 | -18.33 | 1.12 | 0.38 | 0.65 | 4 |
| 3 | Random Search | random_085 | 5 | 5 | 10 | 59 | 16.70 | 47.80 | 0.7120 | 36.13 | 1.18 | 0.36 | 0.90 | 2 |
| 4 | Random Search | random_036 | 5 | 5 | 10 | 59 | 16.70 | 40.75 | 0.6625 | 22.85 | 1.15 | 0.25 | 0.90 | 1 |
| 5 | Random Search | random_042 | 5 | 5 | 10 | 59 | 16.70 | 36.70 | 0.7030 | 16.05 | 1.15 | 0.34 | 0.90 | 1 |
| 6 | Random Search | random_154 | 5 | 5 | 10 | 59 | 16.70 | 29.25 | 0.9750 | 5.90 | 1.14 | 0.25 | 0.65 | 0 |
| 7 | Random Search | random_069 | 5 | 5 | 10 | 59 | 16.70 | 29.50 | 0.9175 | 5.66 | 1.15 | 0.40 | 0.75 | 1 |
| 8 | Random Search | random_097 | 5 | 5 | 10 | 59 | 16.70 | 19.00 | 1.3550 | -7.99 | 1.15 | 0.40 | 0.40 | 0 |
| 9 | Random Search | random_029 | 5 | 5 | 10 | 59 | 16.70 | 30.00 | 0.8725 | 6.02 | 1.14 | 0.30 | 0.75 | 3 |
| 10 | Random Search | random_067 | 5 | 5 | 10 | 59 | 16.70 | 31.80 | 0.7120 | 7.33 | 1.14 | 0.36 | 0.90 | 4 |
| 11 | Random Search | random_147 | 5 | 5 | 10 | 59 | 16.70 | 30.90 | 0.7210 | 5.82 | 1.14 | 0.38 | 0.90 | 3 |
| 12 | Random Search | random_019 | 5 | 5 | 10 | 59 | 16.70 | 24.25 | 0.8500 | -4.60 | 1.12 | 0.25 | 0.75 | 4 |
| 13 | Random Search | random_039 | 5 | 5 | 10 | 59 | 16.70 | 24.25 | 0.8500 | -4.60 | 1.12 | 0.25 | 0.75 | 0 |
| 14 | Random Search | random_141 | 5 | 5 | 10 | 59 | 16.70 | 22.00 | 0.7300 | -10.09 | 1.12 | 0.40 | 0.90 | 2 |
| 15 | Random Search | random_037 | 5 | 5 | 10 | 60 | 16.70 | 36.25 | 0.8500 | 17.00 | 1.15 | 0.25 | 0.75 | 4 |
| 16 | Random Search | random_117 | 5 | 5 | 10 | 59 | 16.70 | 16.25 | 0.8500 | -19.00 | 1.10 | 0.25 | 0.75 | 4 |
| 17 | Random Search | random_143 | 5 | 5 | 10 | 59 | 16.70 | 16.25 | 0.8500 | -19.00 | 1.10 | 0.25 | 0.75 | 3 |
| 18 | Random Search | random_080 | 5 | 5 | 10 | 59 | 16.70 | 16.70 | 0.7030 | -19.95 | 1.10 | 0.34 | 0.90 | 2 |
| 19 | Latin Hypercube | lhs_029 | 5 | 5 | 10 | 61 | 16.70 | 48.25 | 0.8500 | 38.60 | 1.18 | 0.25 | 0.75 | 3 |
| 20 | Latin Hypercube | lhs_059 | 5 | 5 | 10 | 61 | 16.70 | 48.25 | 0.8500 | 38.60 | 1.18 | 0.25 | 0.75 | 3 |

## Recommended configuration

The universal recommendation is the `Recommended.set` preset. The primary goal preset is `Minimum_Big_Levels.set`. Both are generated under `Sets/Optimization_Presets/`.

## Sensitivity summary

| Parameter | Recommended | Working range | Influence |
|---|---|---|---|
| GeometryMode | 2 | 2–3–4 | Среднее |
| BigRatio | 1.14 | 1.15–1.16–1.18 | Сильное |
| SmallRatio | 0.36 | 0.25–0.36–0.38 | Сильное |
| CloseFarShare | 0.75 | 0.65–0.75–0.9 | Очень сильное |
| ReserveShare | 0.25 | 0.1–0.25–0.35 | Очень сильное |
| BigMoveStartPoints | 200 | 190–210–220 | Среднее |
| BigMoveStepPoints | 75 | 70–80–90 | Сильное |
| FarDistancePoints | 275 | 225–250–275 | Сильное |
| ATRPeriod | 20 | 14–20–21 | Низкое |
| ATRTimeframe | 60 | 30–60 | Низкое |
| ATRBigStartMultiplier | 1.15 | 1.0–1.1–1.15 | Сильное |
| ATRFarMultiplier | 1.5 | 1.3–1.45–1.5 | Среднее |
| MaxHarvestLevels | 6 | 5–6–8 | Очень сильное |
| MaxReverseCycles | 10 | 10–12 | Сильное |
| MaxAccountMarginPercent | 55.0 | 45.0–55.0 | Среднее |

## Mathematical dependency data

Plot-ready dependency data is written to `Reports/Parameter_Dependency_Data.csv` for BigRatio -> Big Levels, SmallRatio -> RecoveryPL, CloseFarShare -> Remaining Far proxy, ReserveShare -> ReserveCoverage, ATR -> Geometry/Duration proxy and Geometry -> Recovery Time proxy.

## Full input-parameter recommendation table

| Parameter | Current value | Recommended value | Working range | Influence | Comment |
|---|---|---|---|---|---|
| StartLot | 0.10 | 0.1 | 0.1 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| BigRatio | 1.15 | 1.14 | 1.15–1.16–1.18 | Сильное | Synthetic rank spread=46253.4; recommended preset anchor |
| SmallRatio | 0.25 | 0.36 | 0.25–0.36–0.38 | Сильное | Synthetic rank spread=63315.0; recommended preset anchor |
| CloseBigOnSmall | 0.40 | 0.4 | 0.4 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| RemainBigOnSmall | 0.60 | 0.6 | 0.6 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| CloseFarShare | 0.20 | 0.75 | 0.65–0.75–0.9 | Очень сильное | Synthetic rank spread=119535.5; recommended preset anchor |
| ReserveShare | 0.80 | 0.25 | 0.1–0.25–0.35 | Очень сильное | Synthetic rank spread=119535.5; recommended preset anchor |
| SmallReserveShare | 0.05 | 0.05 | 0.05 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| UseRecommended5050Preset | false | false | false | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| InitialTriggerPoints | 100 | 190 | 190 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| BigMoveStartPoints | 100 | 200 | 190–210–220 | Среднее | Synthetic rank spread=27887.9; recommended preset anchor |
| BigMoveStepPoints | 50 | 75 | 70–80–90 | Сильное | Synthetic rank spread=31145.9; recommended preset anchor |
| FarDistancePoints | 200 | 275 | 225–250–275 | Сильное | Synthetic rank spread=31364.4; recommended preset anchor |
| FarDistanceMode | REAL_PRICE_DISTANCE | 3 | 3 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| GeometryMode | GEOMETRY_MANUAL | 2 | 2–3–4 | Среднее | Synthetic rank spread=21299.9; recommended preset anchor |
| ATRTimeframe | PERIOD_M30 | 60 | 30–60 | Низкое | Synthetic rank spread=1615.8; recommended preset anchor |
| ATRPeriod | 14 | 20 | 14–20–21 | Низкое | Synthetic rank spread=9792.6; recommended preset anchor |
| ATRInitialMultiplier | 1.00 | 1.0 | 1.0–1.05 | Сильное | Synthetic rank spread=33763.1; recommended preset anchor |
| ATRBigStartMultiplier | 1.00 | 1.15 | 1.0–1.1–1.15 | Сильное | Synthetic rank spread=35165.1; recommended preset anchor |
| ATRStepMultiplier | 0.40 | 0.4 | 0.35–0.4–0.45 | Среднее | Synthetic rank spread=14973.6; recommended preset anchor |
| ATRFarMultiplier | 1.30 | 1.5 | 1.3–1.45–1.5 | Среднее | Synthetic rank spread=15202.1; recommended preset anchor |
| MinInitialTriggerPoints | 100 | 100 | 100 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MaxInitialTriggerPoints | 250 | 250 | 250 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MinBigMoveStartPoints | 100 | 100 | 100 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MaxBigMoveStartPoints | 260 | 260 | 260 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MinBigMoveStepPoints | 50 | 50 | 50 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MaxBigMoveStepPoints | 125 | 125 | 125 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MinFarDistancePoints | 200 | 200 | 200 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MaxFarDistancePoints | 400 | 400 | 400 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| GeometryRoundStep | 5 | 5 | 5 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| InitialRoundStep | 10 | 10 | 10 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| BigStartRoundStep | 10 | 10 | 10 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| BigStepRoundStep | 5 | 5 | 5 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| FarDistanceRoundStep | 50 | 50 | 50 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| FreezeGeometryPerCycle | true | true | true | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| PrintAdaptiveGeometryLog | true | true | true | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| AllowATRManualFallback | false | false | false | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| ShowATRIndicatorOnChart | true | true | true | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MaxHarvestLevels | 7 | 6 | 5–6–8 | Очень сильное | Synthetic rank spread=116302.1; recommended preset anchor |
| SmallFarTouchOffsetPoints | 0 | 0 | 0 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MaxReverseCycles | 7 | 10 | 10–12 | Сильное | Synthetic rank spread=33811.7; recommended preset anchor |
| MinReverseStrength | 0.10 | 0.12 | 0.12 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| WarningReverseStrength | 0.15 | 0.18 | 0.18 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| StrongReverseStrength | 0.25 | 0.3 | 0.3 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MinProjectedReserveCoverage | 1.00 | 1.1 | 1.1 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| StopOnInvalidReverseGeometry | true | true | true | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| StopOnReverseLimit | true | true | true | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| AllowNegativeSmallReverseNet | false | false | false | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| LotStep | 0.01 | 0.01 | 0.01 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MaxSpreadPoints | 40.0 | 40.0 | 40.0–60.0 | Сильное | Synthetic rank spread=34273.0; recommended preset anchor |
| MaxMarginPercent | 60.0 | 55.0 | 45.0–55.0 | Сильное | Synthetic rank spread=31759.0; recommended preset anchor |
| MaxDrawdownPercent | 25.0 | 22.0 | 18.0–22.0–25.0 | Сильное | Synthetic rank spread=77989.6; recommended preset anchor |
| MaxManagedPositions | 8 | 10 | 10–8 | Сильное | Synthetic rank spread=31759.0; recommended preset anchor |
| MaxAccountMarginPercent | 60.0 | 55.0 | 45.0–55.0 | Среднее | Synthetic rank spread=23041.9; recommended preset anchor |
| MaxActiveSymbols | 10 | 10 | 10–6 | Сильное | Synthetic rank spread=31759.0; recommended preset anchor |
| StopOnRiskGateBlocked | true | true | true | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| RiskGateLogIntervalSeconds | 60 | 60 | 60 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MaxCloseRetryAttempts | 20 | 20 | 20 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| RetryLogIntervalSeconds | 30 | 30 | 30 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MaxSlippagePoints | 30 | 30 | 30 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| CloseAllOnInvalidGeometry | true | true | true | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| CloseFarOnMaxLevels | true | true | true | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| ReserveMismatchTolerance | 0.01 | 0.01 | 0.01 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| VolumeMismatchToleranceLots | 0.001 | 0.001 | 0.001 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| ReconciliationIntervalSeconds | 300 | 300 | 300 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| PositionResolutionLookbackSeconds | 10 | 10 | 10 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MagicNumber | 20260609 | 20260609 | 20260609 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| AllowRealTrading | true | true | true | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| UseInternalSimulation | false | false | false | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| UseMarketOrders | true | true | true | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| EnableCycleMathCsv | true | true | true | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| VerboseTickLogs | false | false | false | Низкое | Synthetic rank spread=0.0; recommended preset anchor |

## Required preset set files

- `Sets/Optimization_Presets/Ultra_Conservative.set`
- `Sets/Optimization_Presets/Conservative.set`
- `Sets/Optimization_Presets/Universal.set`
- `Sets/Optimization_Presets/Aggressive_Recovery.set`
- `Sets/Optimization_Presets/High_Volatility.set`
- `Sets/Optimization_Presets/Low_Volatility.set`
- `Sets/Optimization_Presets/Trend.set`
- `Sets/Optimization_Presets/Anti_Trend.set`
- `Sets/Optimization_Presets/Adaptive_ATR_SAFE.set`
- `Sets/Optimization_Presets/Adaptive_ATR_BALANCED.set`
- `Sets/Optimization_Presets/Adaptive_ATR_PROFIT.set`
- `Sets/Optimization_Presets/Multi_Symbol.set`
- `Sets/Optimization_Presets/Maximum_Recovery.set`
- `Sets/Optimization_Presets/Minimum_Big_Levels.set`
- `Sets/Optimization_Presets/Recommended.set`

## Limitations

MT5 genetic optimization and broker Strategy Tester runs cannot be executed in this container. These outputs are deterministic offline engineering candidates and must be validated in MT5 before production use. The generated candidates and presets are structured so the same ranges can be imported into MT5 Genetic Optimization as the required next validation stage.

## Final conclusion

The recommended mathematical operating area is ATR BALANCED/PROFIT geometry, BigRatio 1.14–1.16, SmallRatio 0.36–0.40, CloseFarShare 0.75–0.90, FarDistance 250–300, BigMoveStart 190–210 and BigMoveStep 70–80. The main production candidate is `Minimum_Big_Levels.set`; the balanced default is `Recommended.set`.
