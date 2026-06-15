# Refined MT5 Confirmation Plan

Python-модель показывает кандидатов. Финальное подтверждение обязательно через MT5 Strategy Tester.

## Top refined candidate

- BigRatio = 1.2
- SmallRatio = 0.35
- CloseBigOnSmall = 0.32
- RemainBigOnSmall = 0.68
- CloseFarShare = 0.45
- ReserveShare = 0.55
- MaxHarvestLevels = 7
- MaxReverseCycles = 2
- FarDistanceMode = REAL_PRICE_DISTANCE
- EnableCycleMathCsv = true
- AllowRealTrading = true

## Second refined candidate

- BigRatio = 1.2
- SmallRatio = 0.35
- CloseBigOnSmall = 0.32
- RemainBigOnSmall = 0.68
- CloseFarShare = 0.45
- ReserveShare = 0.55
- MaxHarvestLevels = 7
- MaxReverseCycles = 3
- FarDistanceMode = REAL_PRICE_DISTANCE
- EnableCycleMathCsv = true
- AllowRealTrading = true

## Conservative candidate

- BigRatio = 1.25
- SmallRatio = 0.38
- CloseBigOnSmall = 0.35
- RemainBigOnSmall = 0.65
- CloseFarShare = 0.3
- ReserveShare = 0.7
- MaxHarvestLevels = 7
- MaxReverseCycles = 3
- FarDistanceMode = REAL_PRICE_DISTANCE
- EnableCycleMathCsv = true
- AllowRealTrading = true

## Required MT5 artifacts

- Strategy Tester HTML/XML report
- Experts journal containing CYCLE_MATH and REAL_CYCLE_MATH
- MQL5/Files/MinusLock_CycleMath.csv
- Final state and last close comment
- OnTester value
- Check that MagicNumber positions are fully closed

## PASS criteria

- State = STATE_CLOSED_PROFIT
- RealRecoveryPL > 0
- OnTester > 0 and equals real recovery result, not theoretical CycleFinalPL
- No STOP_MAX_LEVELS / STATE_UNCLOSED_CYCLE / invalid geometry / reverse limit
- No managed positions remain open

## FAIL criteria

- RealRecoveryPL <= 0
- OnTester = -1
- STOP_MAX_LEVELS or end-of-test position closure
- Missing Cycle Math CSV or REAL_CYCLE_MATH diagnostics
