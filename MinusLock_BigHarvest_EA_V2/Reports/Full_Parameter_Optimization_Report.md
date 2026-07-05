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
| 1 | Random Search | random_106 | 5 | 5 | 10 | 57 | 16.70 | 46.00 | 0.7300 | 33.11 | 1.18 | 0.40 | 0.90 | 4 |
| 2 | Random Search | random_000 | 5 | 5 | 10 | 57 | 16.70 | 40.25 | 0.8500 | 24.20 | 1.16 | 0.25 | 0.75 | 3 |
| 3 | Random Search | random_014 | 5 | 5 | 10 | 57 | 16.70 | 27.80 | 1.2120 | 6.13 | 1.16 | 0.36 | 0.50 | 2 |
| 4 | Random Search | random_008 | 5 | 5 | 10 | 57 | 16.70 | 38.50 | 0.6850 | 19.07 | 1.15 | 0.30 | 0.90 | 2 |
| 5 | Random Search | random_150 | 5 | 5 | 10 | 57 | 16.70 | 38.50 | 0.6850 | 19.07 | 1.15 | 0.30 | 0.90 | 1 |
| 6 | Random Search | random_144 | 5 | 5 | 10 | 57 | 16.70 | 34.50 | 0.6850 | 11.87 | 1.14 | 0.30 | 0.90 | 1 |
| 7 | Random Search | random_152 | 5 | 5 | 10 | 57 | 16.70 | 16.80 | 1.3370 | -12.17 | 1.14 | 0.36 | 0.40 | 0 |
| 8 | Random Search | random_051 | 5 | 5 | 10 | 57 | 16.70 | 22.50 | 1.0425 | -5.44 | 1.14 | 0.40 | 0.65 | 4 |
| 9 | Random Search | random_052 | 5 | 5 | 10 | 57 | 16.70 | 22.90 | 0.7210 | -8.58 | 1.12 | 0.38 | 0.90 | 0 |
| 10 | Random Search | random_122 | 5 | 5 | 10 | 59 | 16.70 | 48.25 | 0.8500 | 38.60 | 1.18 | 0.25 | 0.75 | 0 |
| 11 | Latin Hypercube | lhs_029 | 5 | 5 | 10 | 59 | 16.70 | 48.25 | 0.8500 | 38.60 | 1.18 | 0.25 | 0.75 | 3 |
| 12 | Latin Hypercube | lhs_059 | 5 | 5 | 10 | 59 | 16.70 | 48.25 | 0.8500 | 38.60 | 1.18 | 0.25 | 0.75 | 3 |
| 13 | Random Search | random_063 | 5 | 5 | 10 | 59 | 16.70 | 50.50 | 0.6850 | 40.67 | 1.18 | 0.30 | 0.90 | 0 |
| 14 | Random Search | random_110 | 5 | 5 | 10 | 59 | 16.70 | 35.50 | 1.3100 | 21.17 | 1.18 | 0.30 | 0.40 | 2 |
| 15 | Random Search | random_115 | 5 | 5 | 10 | 59 | 16.70 | 46.00 | 0.7300 | 33.11 | 1.18 | 0.40 | 0.90 | 3 |
| 16 | Random Search | random_024 | 5 | 5 | 10 | 59 | 16.70 | 40.70 | 0.7030 | 23.25 | 1.16 | 0.34 | 0.90 | 4 |
| 17 | Bayesian Candidate | bayes_064 | 5 | 5 | 10 | 59 | 16.70 | 39.80 | 0.7120 | 21.73 | 1.16 | 0.36 | 0.90 | 2 |
| 18 | Local Refinement | local_b1.16_s0.36_cf0.9_far250 | 5 | 5 | 10 | 59 | 16.70 | 39.80 | 0.7120 | 21.73 | 1.16 | 0.36 | 0.90 | 2 |
| 19 | Bayesian Candidate | bayes_000 | 5 | 5 | 10 | 59 | 16.70 | 38.90 | 0.7210 | 20.22 | 1.16 | 0.38 | 0.90 | 2 |
| 20 | Bayesian Candidate | bayes_017 | 5 | 5 | 10 | 59 | 16.70 | 38.90 | 0.7210 | 20.22 | 1.16 | 0.38 | 0.90 | 2 |

## Recommended configuration

The universal recommendation is the `Recommended.set` preset. The primary goal preset is `Minimum_Big_Levels.set`. Both are generated under `Sets/Optimization_Presets/`.

ATR set-file standard: primary ATR presets use ATRTimeframe=0 (PERIOD_CURRENT) and ATRPeriod=14. ATRPeriod=20 is reserved only for Conservative, Ultra_Conservative and ATR_Conservative because it is smoother, slower and intentionally more cautious.

## Sensitivity summary

| Parameter | Recommended | Working range | Influence |
|---|---|---|---|
| GeometryMode | 2 | 1–2–4 | Среднее |
| BigRatio | 1.14 | 1.15–1.16–1.18 | Сильное |
| SmallRatio | 0.36 | 0.25–0.3–0.38 | Сильное |
| CloseFarShare | 0.75 | 0.65–0.75–0.9 | Очень сильное |
| ReserveShare | 0.25 | 0.1–0.25–0.35 | Очень сильное |
| BigMoveStartPoints | 200 | 190–200–210 | Среднее |
| BigMoveStepPoints | 75 | 75–80–90 | Сильное |
| FarDistancePoints | 275 | 225–250–275 | Среднее |
| ATRPeriod | 14 | 14–20 | Низкое |
| ATRTimeframe | 0 | 0–30–60 | Низкое |
| ATRBigStartMultiplier | 1.15 | 1.0–1.1–1.15 | Сильное |
| ATRFarMultiplier | 1.5 | 1.3–1.45–1.5 | Среднее |
| MaxHarvestLevels | 6 | 5–6–7 | Очень сильное |
| MaxReverseCycles | 10 | 10–12 | Сильное |
| MaxAccountMarginPercent | 55.0 | 45.0–55.0 | Среднее |

## Mathematical dependency data

Plot-ready dependency data is written to `Reports/Parameter_Dependency_Data.csv` for BigRatio -> Big Levels, SmallRatio -> RecoveryPL, CloseFarShare -> Remaining Far proxy, ReserveShare -> ReserveCoverage, ATR -> Geometry/Duration proxy and Geometry -> Recovery Time proxy.

## Full input-parameter recommendation table

| Parameter | Current value | Recommended value | Working range | Influence | Comment |
|---|---|---|---|---|---|
| StartLot | 0.10 | 0.1 | 0.1 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| BigRatio | 1.15 | 1.14 | 1.15–1.16–1.18 | Сильное | Synthetic rank spread=52268.4; recommended preset anchor |
| SmallRatio | 0.25 | 0.36 | 0.25–0.3–0.38 | Сильное | Synthetic rank spread=55850.1; recommended preset anchor |
| CloseBigOnSmall | 0.40 | 0.4 | 0.4 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| RemainBigOnSmall | 0.60 | 0.6 | 0.6 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| CloseFarShare | 0.20 | 0.75 | 0.65–0.75–0.9 | Очень сильное | Synthetic rank spread=112514.5; recommended preset anchor |
| ReserveShare | 0.80 | 0.25 | 0.1–0.25–0.35 | Очень сильное | Synthetic rank spread=112514.5; recommended preset anchor |
| SmallReserveShare | 0.05 | 0.05 | 0.05 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| UseRecommended5050Preset | false | false | false | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| InitialTriggerPoints | 100 | 190 | 190 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| BigMoveStartPoints | 100 | 200 | 190–200–210 | Среднее | Synthetic rank spread=20584.0; recommended preset anchor |
| BigMoveStepPoints | 50 | 75 | 75–80–90 | Сильное | Synthetic rank spread=57001.9; recommended preset anchor |
| FarDistancePoints | 200 | 275 | 225–250–275 | Среднее | Synthetic rank spread=29001.8; recommended preset anchor |
| FarDistanceMode | REAL_PRICE_DISTANCE | 3 | 3 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| GeometryMode | GEOMETRY_MANUAL | 2 | 1–2–4 | Среднее | Synthetic rank spread=12648.3; recommended preset anchor |
| ATRTimeframe | PERIOD_M30 | 0 | 0–30–60 | Низкое | Synthetic rank spread=1066.8; recommended preset anchor |
| ATRPeriod | 14 | 14 | 14–20 | Низкое | Synthetic rank spread=1401.4; recommended preset anchor |
| ATRInitialMultiplier | 1.00 | 1.0 | 1.0–1.05 | Сильное | Synthetic rank spread=34122.0; recommended preset anchor |
| ATRBigStartMultiplier | 1.00 | 1.15 | 1.0–1.1–1.15 | Сильное | Synthetic rank spread=35567.7; recommended preset anchor |
| ATRStepMultiplier | 0.40 | 0.4 | 0.35–0.4–0.45 | Среднее | Synthetic rank spread=15329.7; recommended preset anchor |
| ATRFarMultiplier | 1.30 | 1.5 | 1.3–1.45–1.5 | Среднее | Synthetic rank spread=15568.3; recommended preset anchor |
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
| MaxHarvestLevels | 7 | 6 | 5–6–7 | Очень сильное | Synthetic rank spread=136384.0; recommended preset anchor |
| SmallFarTouchOffsetPoints | 0 | 0 | 0 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MaxReverseCycles | 7 | 10 | 10–12 | Сильное | Synthetic rank spread=34170.6; recommended preset anchor |
| MinReverseStrength | 0.10 | 0.12 | 0.12 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| WarningReverseStrength | 0.15 | 0.18 | 0.18 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| StrongReverseStrength | 0.25 | 0.3 | 0.3 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MinProjectedReserveCoverage | 1.00 | 1.1 | 1.1 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| StopOnInvalidReverseGeometry | true | true | true | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| StopOnReverseLimit | true | true | true | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| AllowNegativeSmallReverseNet | false | false | false | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| LotStep | 0.01 | 0.01 | 0.01 | Низкое | Synthetic rank spread=0.0; recommended preset anchor |
| MaxSpreadPoints | 40.0 | 40.0 | 40.0–60.0 | Сильное | Synthetic rank spread=34631.9; recommended preset anchor |
| MaxMarginPercent | 60.0 | 55.0 | 45.0–55.0 | Сильное | Synthetic rank spread=32117.9; recommended preset anchor |
| MaxDrawdownPercent | 25.0 | 22.0 | 18.0–22.0–25.0 | Сильное | Synthetic rank spread=77628.7; recommended preset anchor |
| MaxManagedPositions | 8 | 10 | 10–8 | Сильное | Synthetic rank spread=32117.9; recommended preset anchor |
| MaxAccountMarginPercent | 60.0 | 55.0 | 45.0–55.0 | Среднее | Synthetic rank spread=22581.5; recommended preset anchor |
| MaxActiveSymbols | 10 | 10 | 10–6 | Сильное | Synthetic rank spread=32117.9; recommended preset anchor |
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
| TerminalStateLogIntervalSeconds | 300 | 300 | 300 | Низкое | Terminal-state reconciliation throttle; log hygiene only |
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
- `Sets/Optimization_Presets/ATR_Conservative.set`
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

The recommended mathematical operating area is ATR BALANCED/PROFIT geometry on PERIOD_CURRENT with ATRPeriod=14, BigRatio 1.14–1.16, SmallRatio 0.36–0.40, CloseFarShare 0.75–0.90, FarDistance 250–300, BigMoveStart 190–210 and BigMoveStep 70–80. ATRPeriod=20 remains only for conservative smoothing presets. The main production candidate is `Minimum_Big_Levels.set`; the balanced default is `Recommended.set`.

## ATR Geometry Runtime Validation — V2.4.23

The previous ATR_SAFE runtime sample confirmed that ATR was technically active (`RuntimeGeometryMode=GEOMETRY_ATR_SAFE`, `GeometrySource=ATR`, `ATRTimeframe=PERIOD_CURRENT`, `ATRPeriod=14`) but still reached `STATE_STOP_MAX_LEVELS` at `HarvestLevel=6` with `TotalReserve=2.76`.

The revised ATR family narrows the ATR-derived distances to improve recovery completion before the maximum level:

| Mode | ATRPeriod | ATRTimeframe | Multipliers Initial/BigStart/Step/Far | Caps Initial/BigStart/Step/Far | Role |
|---|---:|---|---|---|---|
| ATR_SAFE | 14 | PERIOD_CURRENT | 0.90 / 0.90 / 0.34 / 1.10 | 220 / 220 / 90 / 300 | safer but less stretched than old SAFE |
| ATR_BALANCED | 14 | PERIOD_CURRENT | 0.82 / 0.82 / 0.30 / 1.00 | 210 / 210 / 85 / 275 | primary recommended ATR mode |
| ATR_PROFIT | 14 | PERIOD_CURRENT | 0.72 / 0.72 / 0.26 / 0.90 | 200 / 200 / 80 / 250 | minimum Big-level candidate |
| ATR_CONSERVATIVE | 20 | PERIOD_CURRENT | 0.98 / 0.98 / 0.40 / 1.25 | 240 / 240 / 100 / 325 | smoothed cautious diagnostic mode |

See `Reports/ATR_Geometry_Runtime_Trace.md` for the MANUAL vs ATR comparison table and required MT5 re-test matrix.
