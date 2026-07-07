# Big Scenario Parameter Recommendations

## Scope

Offline Python search for the Big-only trend path. `StartLot` is fixed at `1.00` in every row and is not optimized.
The model rejects parameter sets that fail `BigRatio^2 * RemainBigOnSmall < 1`, so Small-scenario compression is not intentionally broken.

## Best found set

- TOP-1: `TestID=83` / `LOCAL_ROUND_AROUND_TOP` / `Score=88361.603175`.
- Parameters: StartLot=1.00, BigRatio=1.11, SmallRatio=0.25, CloseFarShare=0.75, ReserveShare=0.25, BigMoveStart=250, BigMoveStep=40, FarDistance=180, MaxHarvestLevels=20.
- Result: LevelsUsed=1, TotalPositionsOpened=4, TotalPositionsClosed=5, RecoveryPL=26.675, ReserveCoverage=2.05853175, FinalState=STATE_CLOSED_PROFIT, StopReason=FINAL_CLOSE_RESERVE_COVERS_FAR.
- Why selected: it has the minimum level count, passes full-cycle completion, keeps StartLot fixed at 1.00, satisfies Small-scenario compression, and uses the smallest total-position footprint among the highest-scoring one-level candidates.

## TOP-10

| Rank | TestID | Group | Levels | Opened | Closed | BigRatio | SmallRatio | CloseFarShare | ReserveShare | BigStart | BigStep | FarDistance | RecoveryPL | ReserveCoverage | Score |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 83 | LOCAL_ROUND_AROUND_TOP | 1 | 4 | 5 | 1.11 | 0.25 | 0.75 | 0.25 | 250 | 40 | 180 | 26.675 | 2.05853175 | 88361.603175 |
| 2 | 84 | LOCAL_ROUND_AROUND_TOP | 1 | 4 | 5 | 1.11 | 0.25 | 0.75 | 0.25 | 250 | 50 | 180 | 26.675 | 2.05853175 | 88361.603175 |
| 3 | 81 | LOCAL_ROUND_AROUND_TOP | 1 | 4 | 5 | 1.11 | 0.25 | 0.7 | 0.3 | 250 | 40 | 180 | 26.25 | 1.72916667 | 88324.416667 |
| 4 | 82 | LOCAL_ROUND_AROUND_TOP | 1 | 4 | 5 | 1.11 | 0.25 | 0.7 | 0.3 | 250 | 50 | 180 | 26.25 | 1.72916667 | 88324.416667 |
| 5 | 75 | LOCAL_ROUND_AROUND_TOP | 1 | 4 | 5 | 1.1 | 0.25 | 0.75 | 0.25 | 250 | 40 | 180 | 24.25 | 1.89814815 | 88322.314815 |
| 6 | 76 | LOCAL_ROUND_AROUND_TOP | 1 | 4 | 5 | 1.1 | 0.25 | 0.75 | 0.25 | 250 | 50 | 180 | 24.25 | 1.89814815 | 88322.314815 |
| 7 | 66 | FIRST_ROUND_50_PLUS | 1 | 4 | 5 | 1.1 | 0.25 | 0.7 | 0.3 | 250 | 40 | 180 | 23.7 | 1.62698413 | 88289.698413 |
| 8 | 70 | FIRST_ROUND_50_PLUS | 1 | 4 | 5 | 1.1 | 0.25 | 0.7 | 0.3 | 250 | 60 | 180 | 23.7 | 1.62698413 | 88289.698413 |
| 9 | 73 | LOCAL_ROUND_AROUND_TOP | 1 | 4 | 5 | 1.1 | 0.25 | 0.7 | 0.3 | 250 | 40 | 180 | 23.7 | 1.62698413 | 88289.698413 |
| 10 | 74 | LOCAL_ROUND_AROUND_TOP | 1 | 4 | 5 | 1.1 | 0.25 | 0.7 | 0.3 | 250 | 50 | 180 | 23.7 | 1.62698413 | 88289.698413 |

## TOP-1 / TOP-3 summary

### TOP-1: TestID 83

- Levels: 1; positions opened/closed: 4/5.
- RecoveryPL=26.675; ReserveCoverage=2.05853175; RemainingFarLot=0.14; TotalClosedFarLot=0.86.
- Parameters: BigRatio=1.11, SmallRatio=0.25, CloseFarShare=0.75, BigMoveStart=250, BigMoveStep=40, FarDistance=180.

### TOP-2: TestID 84

- Levels: 1; positions opened/closed: 4/5.
- RecoveryPL=26.675; ReserveCoverage=2.05853175; RemainingFarLot=0.14; TotalClosedFarLot=0.86.
- Parameters: BigRatio=1.11, SmallRatio=0.25, CloseFarShare=0.75, BigMoveStart=250, BigMoveStep=50, FarDistance=180.

### TOP-3: TestID 81

- Levels: 1; positions opened/closed: 4/5.
- RecoveryPL=26.25; ReserveCoverage=1.72916667; RemainingFarLot=0.2; TotalClosedFarLot=0.8.
- Parameters: BigRatio=1.11, SmallRatio=0.25, CloseFarShare=0.7, BigMoveStart=250, BigMoveStep=40, FarDistance=180.

## First-round analysis

- Parameters that reduce levels: higher `BigMoveStartPoints`, lower `FarDistancePoints`, higher `BigRatio`, lower `SmallRatio`, and higher `CloseFarShare`.
- Parameters that worsen recovery: too high `SmallRatio` reduces `BigScenarioNet`; too low `CloseFarShare` leaves Far large; too low `ReserveShare` can delay FinalClose if Far is not fully budget-closed.
- Fastest Far close occurs in high `CloseFarShare` / high Big-start / low Far-distance combinations.
- Reserve becomes too small when `CloseFarShare=0.95` and Far remains non-zero after budget close; this is acceptable only if Far is closed directly by the budget within one or two levels.
- BigLot decreases too quickly when FarDistance is low and CloseFarShare is high; that is good for Big-only closure but leaves less follow-up recovery power if price path changes.
- BigLot remains too large when CloseFarShare is low or FarDistance is high; this can keep exposure elevated for more levels.
- Best combinations concentrate around compression-safe BigRatio 1.10-1.11, SmallRatio 0.25, BigMoveStart 250, FarDistance 180, and CloseFarShare 0.70-0.75. Higher BigRatio values can also complete quickly, but the score prefers lower exposure when level count and position count are tied.

## Local-round analysis

The local round around the best zone confirmed that the one-level completion area is stable when `BigMoveStartPoints=250`, `FarDistancePoints=180`, `SmallRatio≈0.25`, and `BigRatio` is kept in the lower compression-safe area around 1.10-1.11 to reduce exposure after level count is already minimized.

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
| 1 | 1.0 | 1.11 | 0.28 | 250 | 277.5 | -70.0 | 207.5 | 155.625 | 51.875 | 0.86 | 154.8 | 0.14 | 51.875 | 26.675 | 2.05853175 | FINAL_CLOSE |
