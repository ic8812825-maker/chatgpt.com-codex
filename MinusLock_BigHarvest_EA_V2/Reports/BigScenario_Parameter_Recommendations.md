# Big Scenario Parameter Recommendations

## Scope

Offline Python search for the Big-only trend path. `StartLot` is fixed at `1.00` in every row and is not optimized.
The model rejects parameter sets that fail `BigRatio^2 * RemainBigOnSmall < 1`, so Small-scenario compression is not intentionally broken.

## MT5 invalidation notice

The supplied MT5 Strategy Tester report is the source of truth and invalidates the previous one-level production claim for `BigScenario_Best_1.set`: MT5 reached `MinusLock_BIG_L11`, returned `OnTester=-1`, and ended with open managed positions. These rows are offline algebraic candidates only and must not be used as working-parameter recommendations until the optimizer is upgraded to replay MT5 deal data.

## Top Python-calibrated candidate (MT5 not confirmed)

- TOP-1: `TestID=346` / `LOCAL_ROUND_AROUND_TOP` / `Score=-245000.7617768`.
- Parameters: StartLot=1.00, BigRatio=1.1, SmallRatio=0.25, CloseFarShare=0.9, ReserveShare=0.1, BigMoveStart=260, BigMoveStep=110, FarDistance=180, MaxHarvestLevels=20.
- Result: LevelsUsed=3, TotalPositionsOpened=8, TotalPositionsClosed=11, RecoveryPL=0.67407082, ReserveCoverage=1.02497515, FinalState=STATE_CLOSED_PROFIT, StopReason=FINAL_CLOSE_RESERVE_COVERS_FAR.
- Why selected by the calibrated Python score: it has the lowest calibrated level count found in this run, keeps StartLot fixed at 1.00, satisfies Small-scenario compression, and avoids the explicitly invalidated MT5 BIG_L11 signature. It remains MT5_CANDIDATE_NOT_CONFIRMED and is not production-approved.

## TOP-10

| Rank | TestID | Group | Levels | Opened | Closed | BigRatio | SmallRatio | CloseFarShare | ReserveShare | BigStart | BigStep | FarDistance | RecoveryPL | ReserveCoverage | Score |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 346 | LOCAL_ROUND_AROUND_TOP | 3 | 8 | 11 | 1.1 | 0.25 | 0.9 | 0.1 | 260 | 110 | 180 | 0.67407082 | 1.02497515 | -245000.7617768 |
| 2 | 342 | LOCAL_ROUND_AROUND_TOP | 3 | 8 | 11 | 1.1 | 0.25 | 0.85 | 0.15 | 260 | 110 | 180 | 13.47331056 | 1.4538207 | -245329.8848244 |
| 3 | 239 | FIRST_ROUND_50_PLUS | 3 | 8 | 11 | 1.1 | 0.25 | 0.85 | 0.15 | 260 | 100 | 180 | 10.28136848 | 1.31744782 | -245875.4415332 |
| 4 | 240 | FIRST_ROUND_50_PLUS | 3 | 8 | 11 | 1.1 | 0.25 | 0.85 | 0.15 | 260 | 100 | 220 | 10.28136848 | 1.31744782 | -245875.4415332 |
| 5 | 241 | FIRST_ROUND_50_PLUS | 3 | 8 | 11 | 1.1 | 0.25 | 0.85 | 0.15 | 260 | 100 | 275 | 10.28136848 | 1.31744782 | -245875.4415332 |
| 6 | 242 | FIRST_ROUND_50_PLUS | 3 | 8 | 11 | 1.1 | 0.25 | 0.85 | 0.15 | 260 | 100 | 350 | 10.28136848 | 1.31744782 | -245875.4415332 |
| 7 | 341 | LOCAL_ROUND_AROUND_TOP | 3 | 8 | 11 | 1.1 | 0.25 | 0.85 | 0.15 | 260 | 100 | 180 | 10.28136848 | 1.31744782 | -245875.4415332 |
| 8 | 358 | LOCAL_ROUND_AROUND_TOP | 3 | 8 | 11 | 1.1 | 0.27 | 0.85 | 0.15 | 260 | 110 | 180 | 10.06136242 | 1.3106549 | -245878.3208858 |
| 9 | 370 | LOCAL_ROUND_AROUND_TOP | 3 | 8 | 11 | 1.11 | 0.25 | 0.8 | 0.2 | 260 | 110 | 180 | 24.28792547 | 1.69222891 | -246198.8978543 |
| 10 | 357 | LOCAL_ROUND_AROUND_TOP | 3 | 8 | 11 | 1.1 | 0.27 | 0.85 | 0.15 | 260 | 100 | 180 | 6.87756872 | 1.19601723 | -246421.6225898 |

## TOP-1 / TOP-3 summary

### TOP-1: TestID 346

- Levels: 3; positions opened/closed: 8/11.
- RecoveryPL=0.67407082; ReserveCoverage=1.02497515; RemainingFarLot=0.1; TotalClosedFarLot=0.9.
- Parameters: BigRatio=1.1, SmallRatio=0.25, CloseFarShare=0.9, BigMoveStart=260, BigMoveStep=110, FarDistance=180.

### TOP-2: TestID 342

- Levels: 3; positions opened/closed: 8/11.
- RecoveryPL=13.47331056; ReserveCoverage=1.4538207; RemainingFarLot=0.11; TotalClosedFarLot=0.89.
- Parameters: BigRatio=1.1, SmallRatio=0.25, CloseFarShare=0.85, BigMoveStart=260, BigMoveStep=110, FarDistance=180.

### TOP-3: TestID 239

- Levels: 3; positions opened/closed: 8/11.
- RecoveryPL=10.28136848; ReserveCoverage=1.31744782; RemainingFarLot=0.12; TotalClosedFarLot=0.88.
- Parameters: BigRatio=1.1, SmallRatio=0.25, CloseFarShare=0.85, BigMoveStart=260, BigMoveStep=100, FarDistance=180.

## First-round analysis

- Parameters that reduce levels: higher `BigMoveStartPoints`, lower `FarDistancePoints`, higher `BigRatio`, lower `SmallRatio`, and higher `CloseFarShare`.
- Parameters that worsen recovery: too high `SmallRatio` reduces `BigScenarioNet`; too low `CloseFarShare` leaves Far large; too low `ReserveShare` can delay FinalClose if Far is not fully budget-closed.
- Fastest Far close occurs in high `CloseFarShare` / high Big-start / low Far-distance combinations.
- Reserve becomes too small when `CloseFarShare=0.95` and Far remains non-zero after budget close; this is acceptable only if Far is closed directly by the budget within one or two levels.
- BigLot decreases too quickly when FarDistance is low and CloseFarShare is high; that is good for Big-only closure but leaves less follow-up recovery power if price path changes.
- BigLot remains too large when CloseFarShare is low or FarDistance is high; this can keep exposure elevated for more levels.
- Best combinations concentrate around compression-safe BigRatio 1.10-1.11, SmallRatio 0.25, BigMoveStart 250, FarDistance 180, and CloseFarShare 0.70-0.75. Higher BigRatio values can also complete quickly, but the score prefers lower exposure when level count and position count are tied.

## Local-round analysis

The local round around the best calibrated zone found several 3-level Python-calibrated candidates with `BigMoveStartPoints≈260`, low `SmallRatio`, and high `CloseFarShare`; these are not MT5-confirmed and must be tested in Strategy Tester before use.

## Dangerous parameters / do not use

- Reject any set where `BigRatio^2 * RemainBigOnSmall >= 1`; it can break Small-scenario compression.
- Avoid high `SmallRatio` values near 0.45 for Big-only optimization; they consume too much of Big profit.
- Avoid very low `CloseFarShare` for minimum-level Big-only paths; it preserves too much Far and shifts dependency to reserve accumulation.
- Do not lower `MaxHarvestLevels` below the selected result's needed level count plus a safety buffer unless MT5 tests confirm no alternate path reaches the limit.

## Future improvements not implemented

- Add a native MT5 Big-only tester mode that emits the same CSV fields from real Strategy Tester deals.
- Add an optional optimizer objective to cap maximum Big lot and margin usage, not only levels and positions.
- Add path-mixed testing: Big-only, Small-only, alternating, and gap/slippage variants in one script.
- Add broker-specific point-value/commission/slippage calibration from Strategy Tester reports.

## Best level trace

| Level | FarLotBefore | BigLot | SmallLot | BigMovePoints | ClosedBigNet | ClosedSmallNet | BigScenarioNet | CloseFarBudget | ReserveAdd | CloseFarLotRounded | CloseFarActualCost | FarLotAfter | ReserveAfter | RecoveryPL | ReserveCoverage | NextAction |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1.0 | 1.1 | 0.28 | 255.0 | 152.37457323 | -38.786255 | 113.58831823 | 102.22948641 | 11.35883182 | 0.37 | 99.86172414 | 0.63 | 11.35883182 | -158.67599576 | 0.06680297 | NEXT_BIG_LEVEL |
| 2 | 0.63 | 0.69 | 0.18 | 365.0 | 136.81118099 | -35.6898733 | 101.12130769 | 91.00917692 | 10.11213077 | 0.33 | 89.06586207 | 0.3 | 21.47096259 | -59.49800293 | 0.26517521 | NEXT_BIG_LEVEL |
| 3 | 0.3 | 0.33 | 0.09 | 475.0 | 85.15049681 | -23.22286277 | 61.92763404 | 55.73487064 | 6.1927634 | 0.2 | 53.97931034 | 0.1 | 27.66372599 | 0.67407082 | 1.02497515 | FINAL_CLOSE |
