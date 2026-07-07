# MT5 Big Scenario Divergence Investigation

## Verdict

The supplied MT5 Strategy Tester report invalidates the previous offline optimizer claim that `BigScenario_Best_1.set` completes in one Big level. In MT5 the same parameter set reached `MinusLock_BIG_L11`, produced `OnTester=-1`, and the test ended with open managed exposure closed by end-of-test orders.

The current offline optimizer must **not** be used as a selector for production-working parameters. It is only a simplified algebraic Big-only trace until it is upgraded to replay MT5 deal prices, dynamic tick value, `FarDistanceMode=REAL_PRICE_DISTANCE`, spread/bid/ask execution, Small-scenario branch changes, and real terminal state guards.

## First divergence

The first material divergence occurs inside level 1 before Far partial close:

1. Python calculates `BigScenarioNet=207.50`, but MT5 realized `ClosedBigNet=147.73`, `ClosedSmallNet=-40.90`, therefore `BigScenarioNet=106.83`.
2. Python uses fixed `FarDistancePoints=180`, but the EA is configured with `FarDistanceMode=REAL_PRICE_DISTANCE`; level 1 MT5 prices imply about 505 price-distance points from Far open to Big close and an actual Far close cost of 78.27 for only 0.29 lot.
3. Python therefore closes 0.86 Far lot and predicts final close, while MT5 closes only 0.29 Far lot and opens `MinusLock_BIG_L2`.

## Python vs MT5 comparison

| Metric | Offline Python | MT5 Tester | Difference | Verdict |
|---|---:|---:|---:|---|
| BigLot L1 | 1.11 | 1.11 | 0.00 | MATCH |
| SmallLot L1 | 0.28 | 0.28 | 0.00 | MATCH |
| Big move points used for L1 | 250 | 245.0 from deal prices | 5.0 | DIVERGES: bid/ask/fill prices |
| Point value per lot | 1.0000 hard-coded | 0.5432 implied from MT5 | 0.4568 | DIVERGES: account currency/symbol tick value |
| BigScenarioNet L1 | 207.50 | 106.83 | 100.67 | FIRST MATERIAL DIVERGENCE |
| CloseFarBudget L1 | 155.62 | 80.12 | 75.50 | DIVERGES |
| ReserveAdd L1 | 51.88 | 26.71 | 25.17 | DIVERGES |
| Far loss basis | 180 points fixed | ~505.0 price-distance points / 269.90 money per lot | large | DIVERGES: EA uses REAL_PRICE_DISTANCE |
| CloseFarLot L1 | 0.86 | 0.29 | 0.57 | DIVERGES |
| FarLotAfter L1 | 0.14 | 0.71 | -0.57 | DIVERGES |
| ReserveCoverage after L1 | 2.0585 | 0.1394 estimate | 1.9192 | DIVERGES |
| Next action after L1 | FINAL_CLOSE | Open MinusLock_BIG_L2 | opposite | FIRST STATE DIVERGENCE |
| Final path | LevelsUsed=1 / STATE_CLOSED_PROFIT | Reached BIG_L11; OnTester=-1; BIG_L11/SMALL_L11/residual Far closed by end-of-test orders | invalidates optimizer claim | MT5_SOURCE_OF_TRUTH |

## Missing conditions in the previous Python model

1. Dynamic `PointValuePerLot()` for USDJPY with EUR deposit currency; previous model hard-coded `1.0`.
2. `FarDistanceMode=REAL_PRICE_DISTANCE`; previous model used fixed `FarDistancePoints=180` as the loss basis.
3. Real bid/ask entry and exit prices; previous model used exact target points.
4. Spread, slippage and fill-price drift between trigger and execution.
5. Real `HistoryDeals` net calculation, including swap/commission when present.
6. Mixed path behavior: MT5 did not remain Big-only; after level 2 the report shows Small-scenario/reverse-style transitions and direction flips.
7. Actual StateMachine guards: final close requires real recovery pass and terminal no-open-position checks; algebraic reserve coverage is insufficient.
8. End-of-test forced closures are not represented by the offline model.

## Can the current optimizer be used?

No. The previous optimizer can remain as a unit-level algebra trace for formulas, but it is not valid for choosing working MT5 parameters. It requires a redesign around MT5 deal replay or Strategy Tester CSV ingestion before it can rank production candidates.

## Required next engineering correction

- Treat `Reports/BigScenario_Parameter_Recommendations.md` and `Sets/BigScenario_Best_*.set` as invalidated offline candidates.
- Add a future optimizer mode that consumes MT5 orders/deals or EA `CycleMath` CSV and compares realized fields level-by-level.
- Rank only candidates that pass real MT5 Strategy Tester with `OnTester > 0`, no end-of-test managed positions, and no `STATE_STOP_MAX_LEVELS` / unresolved recovery state.
