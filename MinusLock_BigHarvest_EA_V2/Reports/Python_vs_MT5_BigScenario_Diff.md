# Python vs MT5 BigScenario Diff

Status: `OLD_OFFLINE_MODEL_INVALID_FOR_FINAL_SELECTION`.

The administrator-supplied MT5 Strategy Tester report is the calibration source. The old Python model is not allowed to be used as the final selector because it predicted `LevelsUsed=1 / STATE_CLOSED_PROFIT` while MT5 reached `BIG_L11`, returned `OnTester=-1`, and closed remaining exposure only by `END_OF_TEST` forced deals.

## Recovered MT5 calibration fields

- InitialIgnoredProfit: `108.27`.
- CycleStartBalance: `10108.27`.
- RecoveryPL estimate after L1: `-164.91905172`.
- Big levels observed: `BIG_L1` ... `BIG_L11`.
- L1 partial Far close: `0.29` lot for loss `78.27`.
- Far remaining after L1: `0.71`.
- Reserve after L1: `26.7075`.
- Final state: `END_OF_TEST_WITH_OPEN_MANAGED_POSITIONS`.
- End reason: `END_OF_TEST`.
- Dynamic point value per lot calibrated from MT5 L1 Big deal: `0.54322486`.
- Far loss per lot calibrated from MT5 L1 Far partial close: `269.89655172`.

## Level diff

| Level | Python BigLot | MT5 BigLot | Python SmallLot | MT5 SmallLot | Python BigScenarioNet | MT5 BigScenarioNet | Python FarAfter | MT5 FarAfter | Python Reserve | MT5 Reserve | Diff |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1.11 | 1.11 | 0.28 | 0.28 | 207.5 | 106.83 | 0.14 | 0.71 | 51.88 | 26.71 | FIRST_MATERIAL_DIVERGENCE: Python overstates net/budget and predicts FINAL_CLOSE; MT5 opens BIG_L2 |
| 2 | 0.0 | 0.79 | 0.0 | 0.2 | 0.0 | 0.0 | 0.0 | 0.71 | 0.0 | 26.71 | OLD_PYTHON_ALREADY_STOPPED; MT5_CONTINUED_LEVEL_SEQUENCE |
| 3 | 0.0 | 0.52 | 0.0 | 0.13 | 0.0 | 0.0 | 0.0 | 0.71 | 0.0 | 26.71 | OLD_PYTHON_ALREADY_STOPPED; MT5_CONTINUED_LEVEL_SEQUENCE |
| 4 | 0.0 | 0.34 | 0.0 | 0.09 | 0.0 | 0.0 | 0.0 | 0.71 | 0.0 | 26.71 | OLD_PYTHON_ALREADY_STOPPED; MT5_CONTINUED_LEVEL_SEQUENCE |
| 5 | 0.0 | 0.27 | 0.0 | 0.07 | 0.0 | 0.0 | 0.0 | 0.71 | 0.0 | 26.71 | OLD_PYTHON_ALREADY_STOPPED; MT5_CONTINUED_LEVEL_SEQUENCE |
| 6 | 0.0 | 0.18 | 0.0 | 0.05 | 0.0 | 0.0 | 0.0 | 0.71 | 0.0 | 26.71 | OLD_PYTHON_ALREADY_STOPPED; MT5_CONTINUED_LEVEL_SEQUENCE |
| 7 | 0.0 | 0.14 | 0.0 | 0.04 | 0.0 | 0.0 | 0.0 | 0.71 | 0.0 | 26.71 | OLD_PYTHON_ALREADY_STOPPED; MT5_CONTINUED_LEVEL_SEQUENCE |
| 8 | 0.0 | 0.12 | 0.0 | 0.03 | 0.0 | 0.0 | 0.0 | 0.71 | 0.0 | 26.71 | OLD_PYTHON_ALREADY_STOPPED; MT5_CONTINUED_LEVEL_SEQUENCE |
| 9 | 0.0 | 0.11 | 0.0 | 0.03 | 0.0 | 0.0 | 0.0 | 0.71 | 0.0 | 26.71 | OLD_PYTHON_ALREADY_STOPPED; MT5_CONTINUED_LEVEL_SEQUENCE |
| 10 | 0.0 | 0.1 | 0.0 | 0.03 | 0.0 | 0.0 | 0.0 | 0.71 | 0.0 | 26.71 | OLD_PYTHON_ALREADY_STOPPED; MT5_CONTINUED_LEVEL_SEQUENCE |
| 11 | 0.0 | 0.07 | 0.0 | 0.02 | 0.0 | 0.0 | 0.0 | 0.71 | 0.0 | 26.71 | OLD_PYTHON_ALREADY_STOPPED; MT5_CONTINUED_LEVEL_SEQUENCE |

## First divergence

The first divergence is level 1 `BigScenarioNet`: Python calculated `207.50`, MT5 realized `106.83`. Because of this, Python overestimated `CloseFarBudget`, closed `0.86` Far lot in the model, and declared `STATE_CLOSED_PROFIT`; MT5 could close only `0.29` Far lot and opened `BIG_L2`.

## Mandatory optimizer rule

Any parameter profile matching this MT5-invalidated signature must be scored as failed: `END_OF_TEST`, `OnTester=-1`, `RemainingFarLot>0`, and `BIG_L9+` are hard penalties. Final rows may be called only `MT5_CANDIDATE_NOT_CONFIRMED` until a new MT5 Strategy Tester run confirms them.
