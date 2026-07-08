# MQL5-like Big Scenario Programmer Recommendations

## Verdict

The new search ran 550 full Python passes after the MT5 L1 gate passed. The top rows are candidates only: `MT5_CANDIDATE_NOT_CONFIRMED`.

## Strongest parameters for fewer Big levels

1. Higher `BigMoveStartPoints` and `BigMoveStepPoints` shortened level count most strongly because realized Big net grows per level.
2. Low `SmallRatio` preserved BigScenarioNet and reduced the drag from Small losses.
3. Higher `CloseFarShare` accelerated Far reduction but can starve reserve; balanced candidates usually kept ReserveCoverage barely above 1.
4. `FarDistancePoints` had lower influence in REAL_PRICE_DISTANCE proxy than actual calibrated Far-open to close distance.

## Parameters with weaker influence in this model

ATR multipliers, ReverseStrength and risk caps were retained in every row, but this deterministic Big-only replay does not trigger ATR recalculation or reverse transitions. They remain important for MT5 validation, not for this isolated Big path ranking.

## Stable combinations

Stable candidates cluster around `BigRatio=1.10-1.11`, `SmallRatio=0.25`, `CloseFarShare=0.85-0.90`, `BigMoveStartPoints=260`, `BigMoveStepPoints=100-110`, `FarDistancePoints=180`.

## Model limits

Without changing MQL5 logic, the calibrated deterministic model found a 3-level minimum among the tested grid. This is not proof that MT5 will close in 3 levels; it is only the current Python lower bound after the MT5 L1 gate.

| Rank | TestID | Group | Status | Levels | FinalState | BigRatio | SmallRatio | CloseFarShare | ReserveShare | BigStart | BigStep | FarDistance | RecoveryPL | ReserveCoverage | RemainingFar | DrawdownProxy | MarginProxy | Score |
|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 359 | ROUND2_TOP20_150 | MT5_CANDIDATE_NOT_CONFIRMED | 4 | STATE_CLOSED_PROFIT | 1.11 | 0.25 | 0.8 | 0.2 | 260 | 100 | 180 | 11.95746556 | 1.19483094 | 0.14 | 392.09655172 | 2.39 | 522522.1625396 |
| 2 | 360 | ROUND2_TOP20_150 | MT5_CANDIDATE_NOT_CONFIRMED | 4 | STATE_CLOSED_PROFIT | 1.11 | 0.25 | 0.8 | 0.2 | 260 | 100 | 180 | 11.95746556 | 1.19483094 | 0.14 | 392.09655172 | 2.39 | 522522.1625396 |
| 3 | 368 | ROUND2_TOP20_150 | MT5_CANDIDATE_NOT_CONFIRMED | 4 | STATE_CLOSED_PROFIT | 1.11 | 0.25 | 0.8 | 0.2 | 260 | 100 | 180 | 11.95746556 | 1.19483094 | 0.14 | 392.09655172 | 2.39 | 522522.1625396 |
| 4 | 369 | ROUND2_TOP20_150 | MT5_CANDIDATE_NOT_CONFIRMED | 4 | STATE_CLOSED_PROFIT | 1.11 | 0.25 | 0.8 | 0.2 | 260 | 100 | 180 | 11.95746556 | 1.19483094 | 0.14 | 392.09655172 | 2.39 | 522522.1625396 |
| 5 | 440 | ROUND2_TOP20_150 | MT5_CANDIDATE_NOT_CONFIRMED | 4 | STATE_CLOSED_PROFIT | 1.11 | 0.25 | 0.8 | 0.2 | 260 | 100 | 220 | 11.95746556 | 1.19483094 | 0.14 | 392.09655172 | 2.39 | 522522.1625396 |
| 6 | 441 | ROUND2_TOP20_150 | MT5_CANDIDATE_NOT_CONFIRMED | 4 | STATE_CLOSED_PROFIT | 1.11 | 0.25 | 0.8 | 0.2 | 260 | 100 | 220 | 11.95746556 | 1.19483094 | 0.14 | 392.09655172 | 2.39 | 522522.1625396 |
| 7 | 449 | ROUND2_TOP20_150 | MT5_CANDIDATE_NOT_CONFIRMED | 4 | STATE_CLOSED_PROFIT | 1.11 | 0.25 | 0.8 | 0.2 | 260 | 100 | 220 | 11.95746556 | 1.19483094 | 0.14 | 392.09655172 | 2.39 | 522522.1625396 |
| 8 | 450 | ROUND2_TOP20_150 | MT5_CANDIDATE_NOT_CONFIRMED | 4 | STATE_CLOSED_PROFIT | 1.11 | 0.25 | 0.8 | 0.2 | 260 | 100 | 220 | 11.95746556 | 1.19483094 | 0.14 | 392.09655172 | 2.39 | 522522.1625396 |
| 9 | 482 | ROUND3_TOP5_100 | MT5_CANDIDATE_NOT_CONFIRMED | 4 | STATE_CLOSED_PROFIT | 1.11 | 0.25 | 0.8 | 0.2 | 260 | 100 | 180 | 11.95746556 | 1.19483094 | 0.14 | 392.09655172 | 2.39 | 522522.1625396 |
| 10 | 483 | ROUND3_TOP5_100 | MT5_CANDIDATE_NOT_CONFIRMED | 4 | STATE_CLOSED_PROFIT | 1.11 | 0.25 | 0.8 | 0.2 | 260 | 100 | 180 | 11.95746556 | 1.19483094 | 0.14 | 392.09655172 | 2.39 | 522522.1625396 |