# MT5-Calibrated BigScenario Recommendations

Status: `OLD_OFFLINE_MODEL_INVALID_FOR_FINAL_SELECTION` for the previous one-level model.

All rows below are `MT5_CANDIDATE_NOT_CONFIRMED`; no row is called best until a real MT5 Strategy Tester run confirms it.
The optimizer uses calibrated `POINT_VALUE_PER_LOT=0.54323662`, calibrated Far loss per lot `269.89655172`, spread/slippage proxy, and hard penalties for `END_OF_TEST`, `OnTester=-1`, `RemainingFarLot>0`, and `BIG_L9+`.

## TOP-10 Python-calibrated candidates

| Rank | TestID | Status | Levels | FinalState | BigRatio | SmallRatio | CloseFarShare | ReserveShare | BigStart | BigStep | FarDistance | RemainingFarLot | RecoveryPL | ReserveCoverage | Score |
|---:|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 346 | MT5_CANDIDATE_NOT_CONFIRMED | 3 | STATE_CLOSED_PROFIT | 1.1 | 0.25 | 0.9 | 0.1 | 260 | 110 | 180 | 0.1 | 0.6746697 | 1.02499734 | -245000.753569 |
| 2 | 342 | MT5_CANDIDATE_NOT_CONFIRMED | 3 | STATE_CLOSED_PROFIT | 1.1 | 0.25 | 0.85 | 0.15 | 260 | 110 | 180 | 0.11 | 13.47424496 | 1.45385217 | -245329.8723334 |
| 3 | 239 | MT5_CANDIDATE_NOT_CONFIRMED | 3 | STATE_CLOSED_PROFIT | 1.1 | 0.25 | 0.85 | 0.15 | 260 | 100 | 180 | 0.12 | 10.28229221 | 1.31747634 | -245875.4294439 |
| 4 | 240 | MT5_CANDIDATE_NOT_CONFIRMED | 3 | STATE_CLOSED_PROFIT | 1.1 | 0.25 | 0.85 | 0.15 | 260 | 100 | 220 | 0.12 | 10.28229221 | 1.31747634 | -245875.4294439 |
| 5 | 241 | MT5_CANDIDATE_NOT_CONFIRMED | 3 | STATE_CLOSED_PROFIT | 1.1 | 0.25 | 0.85 | 0.15 | 260 | 100 | 275 | 0.12 | 10.28229221 | 1.31747634 | -245875.4294439 |
| 6 | 242 | MT5_CANDIDATE_NOT_CONFIRMED | 3 | STATE_CLOSED_PROFIT | 1.1 | 0.25 | 0.85 | 0.15 | 260 | 100 | 350 | 0.12 | 10.28229221 | 1.31747634 | -245875.4294439 |
| 7 | 341 | MT5_CANDIDATE_NOT_CONFIRMED | 3 | STATE_CLOSED_PROFIT | 1.1 | 0.25 | 0.85 | 0.15 | 260 | 100 | 180 | 0.12 | 10.28229221 | 1.31747634 | -245875.4294439 |
| 8 | 358 | MT5_CANDIDATE_NOT_CONFIRMED | 3 | STATE_CLOSED_PROFIT | 1.1 | 0.27 | 0.85 | 0.15 | 260 | 110 | 180 | 0.12 | 10.06228137 | 1.31068328 | -245878.3088583 |
| 9 | 370 | MT5_CANDIDATE_NOT_CONFIRMED | 3 | STATE_CLOSED_PROFIT | 1.11 | 0.25 | 0.8 | 0.2 | 260 | 110 | 180 | 0.13 | 24.28921084 | 1.69226554 | -246198.8813376 |
| 10 | 357 | MT5_CANDIDATE_NOT_CONFIRMED | 3 | STATE_CLOSED_PROFIT | 1.1 | 0.27 | 0.85 | 0.15 | 260 | 100 | 180 | 0.13 | 6.87847718 | 1.19604312 | -246421.6109162 |

## Invalidated profile check

The MT5-invalidated profile `1.11/0.25/0.75/250/40/180` is forced to `END_OF_TEST` with `MT5_CALIBRATION_MATCH_REACHED_BIG_L11_ONTESTER_MINUS_1`; it can no longer rank above any real 5-level candidate.
