# MT5 Parameter Confirmation Plan

Python-модель показывает кандидатов. Финальное подтверждение обязательно через MT5 Strategy Tester.

## Top candidate

- BigRatio = 1.25
- SmallRatio = 0.37
- CloseBigOnSmall = 0.35
- RemainBigOnSmall = 0.65
- CloseFarShare = 0.4
- ReserveShare = 0.6
- MaxHarvestLevels = 7
- MaxReverseCycles = 3
- FarDistanceMode = REAL_PRICE_DISTANCE
- EnableCycleMathCsv = true
- AllowRealTrading = true

## Second candidate

- BigRatio = 1.25
- SmallRatio = 0.37
- CloseBigOnSmall = 0.35
- RemainBigOnSmall = 0.65
- CloseFarShare = 0.4
- ReserveShare = 0.6
- MaxHarvestLevels = 7
- MaxReverseCycles = 5
- FarDistanceMode = REAL_PRICE_DISTANCE
- EnableCycleMathCsv = true
- AllowRealTrading = true

## Conservative candidate

- BigRatio = 1.3
- SmallRatio = 0.42
- CloseBigOnSmall = 0.4
- RemainBigOnSmall = 0.6
- CloseFarShare = 0.5
- ReserveShare = 0.5
- MaxHarvestLevels = 5
- MaxReverseCycles = 10
- FarDistanceMode = REAL_PRICE_DISTANCE
- EnableCycleMathCsv = true
- AllowRealTrading = true

## Reports to collect

- Strategy Tester report
- Experts journal with CYCLE_MATH and REAL_CYCLE_MATH
- MQL5/Files/MinusLock_CycleMath.csv
- OnTester value
- Final state and last system close comment
- Open-position check for the MagicNumber

## PASS criteria

- State = STATE_CLOSED_PROFIT
- RealRecoveryPL > 0
- OnTester > 0 and equals real recovery result, not theoretical CycleFinalPL
- No managed positions remain open
- No STOP_MAX_LEVELS / STATE_UNCLOSED_CYCLE / STATE_ERROR

## FAIL criteria

- RealRecoveryPL <= 0
- OnTester = -1
- STOP_MAX_LEVELS, invalid reverse geometry, reverse limit, or unmanaged open positions
- Missing CYCLE_MATH / REAL_CYCLE_MATH diagnostics
