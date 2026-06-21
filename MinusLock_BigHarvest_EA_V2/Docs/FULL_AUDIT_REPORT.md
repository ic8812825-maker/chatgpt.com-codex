# Full Audit Report — MinusLock_BigHarvest_EA Current Logic

Audit date: 2026-06-15 UTC  
Branch: work  
Project folder: `MinusLock_BigHarvest_EA`  
Work-copy folder: `work/MinusLock_SelfCompressing_BigSmall_v2/MinusLock_BigHarvest_EA`  
Target GitHub URL: <https://github.com/ic8812825-maker/chatgpt.com-codex/tree/work/MinusLock_BigHarvest_EA>

## 1. Project Folder

The audited MT5-ready project is the top-level folder:

```text
MinusLock_BigHarvest_EA
```

The top-level project was compared with the work-copy project:

```text
work/MinusLock_SelfCompressing_BigSmall_v2/MinusLock_BigHarvest_EA
```

Result:

```text
diff -qr ... returned no differences.
```

Verdict: PASS — top-level EA and work-copy EA are synchronized.

## 2. Files Checked

```text
MinusLock_BigHarvest_EA/BUILD_INFO.md
MinusLock_BigHarvest_EA/Docs/MANUAL.md
MinusLock_BigHarvest_EA/Docs/TEST_PLAN.md
MinusLock_BigHarvest_EA/Include/Config.mqh
MinusLock_BigHarvest_EA/Include/Logger.mqh
MinusLock_BigHarvest_EA/Include/LotUtils.mqh
MinusLock_BigHarvest_EA/Include/PositionUtils.mqh
MinusLock_BigHarvest_EA/Include/RecoveryMath.mqh
MinusLock_BigHarvest_EA/Include/RiskManager.mqh
MinusLock_BigHarvest_EA/Include/SimulationEngine.mqh
MinusLock_BigHarvest_EA/Include/StateMachine.mqh
MinusLock_BigHarvest_EA/Include/TradeEngine.mqh
MinusLock_BigHarvest_EA/Include/Types.mqh
MinusLock_BigHarvest_EA/MinusLock_BigHarvest_EA.mq5
MinusLock_BigHarvest_EA/Tests/Manual_Test_Cases.md
```

Temporary-file scan found no `*.bak`, `*.tmp`, `*.old`, `*.pyc`, `__pycache__`, or `.DS_Store` files.

## 3. Config Check

Verified tokens and parameters:

```text
StartLot, BigRatio, SmallRatio, CloseBigOnSmall, RemainBigOnSmall,
CloseFarShare, ReserveShare, UseRecommended5050Preset,
InitialTriggerPoints, BigMoveStartPoints, BigMoveStepPoints, FarDistanceMode,
MaxHarvestLevels, SmallFarTouchOffsetPoints, MaxReverseCycles,
MinReverseStrength, WarningReverseStrength, StrongReverseStrength,
MinProjectedReserveCoverage, StopOnInvalidReverseGeometry,
StopOnReverseLimit, AllowNegativeSmallReverseNet, LotStep,
MaxSpreadPoints, MaxMarginPercent, MagicNumber, AllowRealTrading,
UseMarketOrders, EnableCycleMathCsv.
```

Verified `FarDistanceMode = REAL_PRICE_DISTANCE` by default.

Verified `UseRecommended5050Preset` switches internal work parameters without mutating MQL5 `input` variables:

```text
WorkSmallRatio = 0.36
WorkCloseBigOnSmall = 0.35
WorkRemainBigOnSmall = 0.65
WorkCloseFarShare = 0.50
WorkReserveShare = 0.50
WorkMaxHarvestLevels = 5
WorkMaxReverseCycles = 10
```

Audit runtime profile requested by the task (`CloseFarShare=0.70`, `ReserveShare=0.30`, `MaxHarvestLevels=5`, `MaxReverseCycles=10`, `AllowRealTrading=true`) is supported through MT5 input overrides. The source defaults remain conservative/manual defaults and must be overridden in Strategy Tester for the 70/30 audit run.

Verdict: PASS with MT5-input override note.

## 4. State Machine Check

Verified states:

```text
STATE_IDLE
STATE_INITIAL_LOCK_OPENED
STATE_INITIAL_PLUS_CLOSED
STATE_FAR_ACTIVE
STATE_BIG_SMALL_OPENED
STATE_BIG_HARVEST
STATE_WAIT_SMALL_TO_FAR
STATE_SMALL_SCENARIO
STATE_FINAL_CLOSE
STATE_CLOSED_PROFIT
STATE_DUAL_TAIL
STATE_INVALID_REVERSE_GEOMETRY
STATE_INVALID_SMALL_GEOMETRY
STATE_REVERSE_LIMIT
STATE_REVERSE_WARNING
STATE_STOP_MAX_LEVELS
STATE_UNCLOSED_CYCLE
STATE_STOP
STATE_ERROR
```

Verified transition flow:

```text
STATE_IDLE -> OpenInitialLock
STATE_INITIAL_LOCK_OPENED -> CheckInitialPlusClose
STATE_FAR_ACTIVE -> OpenBigSmall
STATE_BIG_SMALL_OPENED -> CheckBigOrSmallScenario
STATE_WAIT_SMALL_TO_FAR -> CheckSmallToFarTouch
STATE_BIG_HARVEST -> ProcessBigHarvest
STATE_SMALL_SCENARIO -> ProcessSmallScenario / ProcessSmallAtFarTouch
STATE_FINAL_CLOSE -> ProcessFinalClose
Terminal/fail states do not open new levels.
```

Verdict: PASS.

## 5. Initial Lock Check

Verified logic:

1. `STATE_IDLE` opens `BUY StartLot` and `SELL StartLot`.
2. Comments are `MinusLock_INITIAL_BUY` and `MinusLock_INITIAL_SELL`.
3. Trade engine assigns `MagicNumber` through `CTrade.SetExpertMagicNumber`.
4. `CheckInitialPlusClose` waits for `InitialTriggerPoints`.
5. Winning initial leg is closed.
6. Remaining losing leg becomes Far.
7. `initialIgnoredProfit` is stored separately.
8. `totalReserve` is reset to zero.
9. `cycleStartBalance` and `cycleStartTime` are recorded after the first plus closes.
10. Initial 100 points are captured as `initialFarDistancePoints`.

Verdict: PASS — first profit is excluded from recovery accounting.

## 6. Big Scenario Check

Verified Big-harvest flow:

1. Big direction movement is detected through `ProfitPoints`.
2. Big closes 100%.
3. Small closes 100%.
4. Theoretical `netProfit = profitBig - lossSmall - costs` is calculated.
5. `CloseFarBudget = netProfit * WorkCloseFarShare`.
6. `ReserveAdd = netProfit * WorkReserveShare`.
7. `TotalReserve` increases by `ReserveAdd`.
8. `EffectiveFarDistancePoints` is calculated before money-based Far close.
9. `CloseFarLotRaw = CloseFarBudget / (EffectiveFarDistancePoints * PointValuePerLot)`.
10. `CloseFarLotRounded` is normalized down and capped by Far lot.
11. Far is partially closed by the rounded lot.
12. `FarRemainLoss` uses `EffectiveFarDistancePoints`.
13. `FinalCloseAllowed` is checked.
14. If levels are exhausted, residual Far is closed with `STOP_MAX_LEVELS` and the cycle is marked `STATE_UNCLOSED_CYCLE`.

Verdict: PASS — money-budget Far close is implemented; `CloseFarShare` is not treated as a percent of Far lot.

## 7. Small Scenario Check

Verified Small-at-Far flow:

1. Small-side movement does not immediately close Small.
2. EA enters `STATE_WAIT_SMALL_TO_FAR`.
3. `FarTouchReachedForSmall` checks old Far touch with `SmallFarTouchOffsetPoints`.
4. On touch, `ProcessSmallAtFarTouch` runs.
5. Small closes 100%.
6. Old Far closes 100%.
7. Big closes by `WorkCloseBigOnSmall`.
8. Remaining Big becomes NewFar.
9. NewFar direction equals Big direction.
10. New Far inherits the real open price of the remaining Big and keeps a non-zero real distance when price moved:

```text
farOpenPrice = bigOpenPrice
currentClosePrice = currentPrice
effectiveFarDistancePoints = CalcRealPriceFarDistancePoints(currentPrice, bigOpenPrice)
expectedNextFarLoss = CalcFarRemainLoss(newFarLot, effectiveFarDistancePoints)
```

Verdict: PASS — normal Small-at-Far does not leave old Far, should not create DUAL_TAIL, and must not create an artificial zero-loss NewFar.

## 8. FarDistanceMode Check

Verified modes:

```text
FIXED_200
INITIAL_PLUS_CURRENT
INITIAL_PLUS_CUMULATIVE
REAL_PRICE_DISTANCE
```

Verified `REAL_PRICE_DISTANCE` formula:

```text
EffectiveFarDistancePoints = ABS(CurrentClosePrice - FarOpenPrice) / Point
```

Verified Level 1 design requirement:

```text
InitialTriggerPoints = 100
BigMoveStartPoints = 100
BigMoveStepPoints = 50
MaxHarvestLevels = 7
L(level) = BigMoveStartPoints + (level - 1) * BigMoveStepPoints
Expected EffectiveFarDistancePoints ≈ 200 in real price movement.
```

Verified Small-at-Far reset: the new Far does not inherit the old initial 100-point distance.

Verdict: PASS.

## 9. RealRecoveryPL Check

Verified real recovery tracking:

```text
initialIgnoredProfit
cycleStartBalance
cycleStartTime
cycleCurrentBalance
cycleBalancePL
realRecoveryPL
realCyclePL
realClosedProfit
realClosedLoss
realCommission
realSwap
realCosts
theoreticalCyclePL
realCycleProfitPositive
lastCloseWasSystemClose
lastSystemCloseComment
```

`RecalculateRealCycleStatsFromHistory` filters closed deals by:

```text
DEAL_MAGIC == MagicNumber
DEAL_ENTRY == DEAL_ENTRY_OUT
HistorySelect(cycleStartTime, TimeCurrent()+86400)
```

It sums:

```text
DEAL_PROFIT + DEAL_COMMISSION + DEAL_SWAP
```

Fallback is balance-based:

```text
RealRecoveryPL = AccountBalance - cycleStartBalance
```

Verdict: PASS — false positive theoretical recovery is no longer enough for tester PASS.

## 10. OnTester Check

Verified `OnTester` logic:

```text
RecalculateRealCycleStatsFromHistory();
passByRealPL = IsRealRecoveryPass();
return passByRealPL ? realRecoveryPL : -1.0;
```

PASS requires:

```text
State = STATE_CLOSED_PROFIT
RealRecoveryPL > 0
CountManagedOpenPositions() = 0
lastCloseWasSystemClose = true
lastSystemCloseComment = FINAL_CLOSE or CLOSED_PROFIT
```

If real recovery is negative, `OnTester = -1` even if theoretical `CycleFinalPL` is positive.

Verdict: PASS — no false PASS path found in static audit.

## 11. CSV/CYCLE_MATH Check

Verified journal/CSV diagnostics:

```text
CYCLE_MATH |
REAL_CYCLE_MATH |
MinusLock_CycleMath.csv
```

Verified core fields:

```text
Level, Scenario, FarLotBefore, BigLot, SmallLot, NetProfit,
CloseFarBudget, ReserveAdd, TotalReserve, FarRemainLoss,
FinalCloseAllowed, State, InitialFarDistancePoints,
CurrentBigMovePoints, CumulativeBigMovePoints,
EffectiveFarDistancePoints, FarDistanceMode, FarOpenPrice,
CurrentClosePrice, InitialIgnoredProfit, CycleStartBalance,
CurrentBalance, RealRecoveryPL, RealClosedProfit, RealClosedLoss,
RealCommission, RealSwap, RealCosts, TheoreticalCyclePL,
LastSystemCloseComment, PassByRealPL.
```

Verdict: PASS.

## 12. Risk Gates Check

Verified risk gates:

```text
MaxSpreadPoints
MaxMarginPercent
SpreadOk
MarginOk
IsTradingAllowedSafe
RiskGate Spread=
RiskGate Margin=
RISK GATE BLOCKED
```

In real trading mode, failed spread or margin gates block trading. In simulation mode, they log warnings but do not block simulation startup.

Verdict: PASS.

## 13. MT5 Tests

MetaEditor / MetaTrader executables are not available in this Linux container.

Status:

```text
MetaEditor compile-check: BLOCKED
Strategy Tester A 70/30: BLOCKED
Strategy Tester B 50/50 preset: BLOCKED
Strategy Tester C 90/10: BLOCKED
```

Required external MT5 confirmation:

1. Compile `MinusLock_BigHarvest_EA.mq5` in MetaEditor.
2. Run 70/30 with `FarDistanceMode=REAL_PRICE_DISTANCE` and verify negative recovery returns `OnTester=-1`.
3. Run 50/50 preset and judge only by `RealRecoveryPL`.
4. Run 90/10 and confirm no false PASS.
5. Inspect `CYCLE_MATH`, `REAL_CYCLE_MATH`, and `MinusLock_CycleMath.csv`.

## 14. Python/AI Tests

Executed checks:

```text
python work/MinusLock_SelfCompressing_BigSmall_v2/ai_tests/parameter_sweep.py
python -m pytest work/MinusLock_SelfCompressing_BigSmall_v2/ai_tests/test_scenarios.py -q
python work/MinusLock_SelfCompressing_BigSmall_v2/scripts/verify_big_harvest_ea.py
python scripts/verify_big_harvest_ea.py
```

Results:

```text
AI simulation PASS: scenarios=6 sweep=675 best_state=STATE_CLOSED_PROFIT best_pl=42.0
pytest: 20 passed
work verification harness: PASS
root verification harness: PASS
```

Static MQL brace/paren check:

```text
balanced braces/parens for 11 MQL files
```

Audit token check:

```text
AUDIT_TOKEN_CHECK PASS groups=12
```

## 15. Found Problems

No code defect was found by repository-local static, token, structure, math, and Python/AI checks.

Operational note: the audit's 70/30 MT5 profile must be set as Strategy Tester inputs because source defaults remain conservative/manual defaults.

## 16. Fixes Applied

No code fixes were required during this audit.

Created this audit report:

```text
MinusLock_BigHarvest_EA/Docs/FULL_AUDIT_REPORT.md
```

## 17. Remaining Risks

1. Native MQL5 compilation has not been executed in this Linux container.
2. Real MT5 Strategy Tester execution has not been executed in this Linux container.
3. The real 70/30 negative-balance case must be confirmed in MT5 to prove `OnTester=-1` with broker/tester costs.
4. Python/AI tests validate math and static logic, but do not replace MetaEditor compile or Strategy Tester execution.

## 18. Final Verdict

Repository-local audit verdict: PASS.

The EA matches the current intended logic at static/code level:

```text
Start Lock
→ Ignore First Profit
→ Far Recovery
→ Big-Harvest or Small-at-Far
→ RealRecoveryPL validation
→ CLOSED_PROFIT or STOP / FAIL
```

Critical audit conclusions:

1. No false PASS path was found: `OnTester` is gated by `RealRecoveryPL > 0` and system-close state.
2. The first plus is excluded from recovery accounting.
3. Big scenario closes Big and Small fully, uses money-budget Far close, and checks FinalCloseAllowed.
4. Small scenario waits for old Far, closes Small and old Far, rebuilds NewFar, and resets Far distance.
5. `REAL_PRICE_DISTANCE` is implemented for effective Far distance.
6. `CYCLE_MATH`, `REAL_CYCLE_MATH`, and CSV diagnostics are present.
7. STOP_MAX_LEVELS is a FAIL path and closes residual Far instead of leaving positions until end-of-test.

Final platform verdict remains pending MT5:

```text
MetaEditor compile-check: REQUIRED
Strategy Tester 70/30, 50/50, 90/10: REQUIRED
```

## V2.4 Safety Audit Addendum

Implemented V2.4 safety requirements:

- Risk Compression Reverse validation: `BigRatio^2 * RemainBigOnSmall < 1`.
- Strict `CloseBigOnSmall + RemainBigOnSmall == 1.0` input validation.
- Small reserve accounting via `SmallReserveShare` and `SMALL_RESERVE_ADD` logs.
- Startup trading environment diagnostics.
- Initial lock rollback with `ROLLBACK_INITIAL_BUY_WITHOUT_SELL`.
- Trade setup uses `SetExpertMagicNumber`, `SetDeviationInPoints(MaxSlippagePoints)`, and `SetTypeFillingBySymbol`.
- Reverse-limit new-Far close comments and terminal states.
- Invalid geometry emergency close/manual-intervention states.
- Restart recovery stubs using GlobalVariables.
- Retry FSM state definitions for multi-step operations.

MetaEditor compile and Strategy Tester remain required on an MT5 environment.

## V2.4.1 RiskGate Architecture Fix Audit Addendum

V2.4.1 removes the unsafe global `return` from `OnTick()` when RiskGate is blocked. `OnTick()` records `Ctx.riskGateOk` and always runs the state machine; the opening functions check the gate locally before creating new exposure. Close, partial-close, final-close, reverse-limit, invalid-geometry emergency, recovery and retry paths are intentionally independent of spread blocking.

Pending states are now operational: each `STATE_CLOSE_*_PENDING`, `STATE_REVERSE_LIMIT_CLOSE_PENDING`, and `STATE_RECOVERY_PENDING` case has a handler. Retry context is persisted through GlobalVariables (`lastRetryState`, `retryTicket`, `retryLot`, `retryAttempts`) and repeated attempts are logged at `RetryLogIntervalSeconds` intervals until success or `MaxCloseRetryAttempts` moves the EA to manual intervention.

BigHarvest reserve handling was revised so projected P/L remains diagnostic only. The reserve and Far-close budget are derived from real history aggregation (`HistorySelect`, `HistoryDealGetDouble`, `HistoryDealGetInteger(DEAL_POSITION_ID)`) and positive `RealBigHarvestNet` only.

RecoverState now restores additional fields and reconciles saved context with real positions by symbol, magic, ticket, position identifier, comment, direction, lot and open price. Disagreement enters `STATE_RECOVERY_PENDING` so the EA does not blindly reset with live exposure.

The V2.4.1 default spread gate is `MaxSpreadPoints=60.0`, because USDJPY MetaQuotes-Demo can show 45-50 points and `30` may over-block opening decisions.

## V2.4.2 Audit Addendum

The V2.4.2 patch addresses the remaining V2.4.1 architectural findings: retry states now carry a next-state continuation target, BigHarvest and Small Scenario expose phase states, dead open-pending states have handlers, BigHarvest real reserve uses matching HistoryDeals by position id, and SmallScenario reserve uses before/after real-cycle deltas. Recovery diagnostics now include saved/recovered state and open/missing/duplicate position reporting tokens.

## V2.4.3 Audit Addendum

The remaining mixed FSM/legacy paths were removed from the main execution routes. BigHarvest and Small Scenario entry functions are now thin state-transition wrappers, while actual work is performed by phase-specific handlers. Retry cleanup now clears closed leg context, open-pending states retry actual opens, and startup validation is performed after working-parameter configuration.

## V2.4.5 Audit Addendum

V2.4.5 fixes the three critical FSM defects only: terminal states are separated from opening pending states, Small Build New Far uses saved Small context after active Small cleanup, and Old Far is saved then removed from active context after close. The strict FSM integrity check and Python tests assert these routes directly.

## V2.4.6 MaxHarvestLevels Final Decision Audit
V2.4.6 adds an explicit max-level terminal decision path. `OpenBigSmall()` and `RetryOpenNewBig()` route to `STATE_MAX_LEVELS_DECISION` instead of opening new exposure when `Ctx.harvestLevel >= WorkMaxHarvestLevels`. `ProcessBigHarvestCheckFinal()` and `ProcessSmallCheckReserve()` also route residual Far handling to this state at the last allowed level.

`ProcessMaxLevelsDecision()` calculates Far floating P/L, reserve coverage, and logs `[MAX_LEVELS_DECISION]`. With `CloseFarOnMaxLevels=true`, residual Far is closed by the EA via `STOP_MAX_LEVELS_CLOSE_FAR` if reserve is insufficient. Failed closes go to `STATE_STOP_MAX_LEVELS_CLOSE_PENDING` and retry through `RetryStopMaxLevelsClose()`.

## V2.4.7 Audit: Retry Partial Far Safety
V2.4.7 replaces text-based retry cleanup with `PendingActionType`. `PENDING_CLOSE_FAR_PARTIAL` preserves Far identity and only subtracts the retried lot from `Ctx.farLot`, preventing false closed-Far context after partial retry success. Full Far cleanup is restricted to explicit full-close pending actions.

A runtime `STATE_CLOSED_PROFIT` guard now checks `CountManagedOpenPositions()` and blocks a profit terminal state if any managed position remains open. Real HistoryDeals matching uses `PositionSnapshot.identifier` from `POSITION_IDENTIFIER` against `DEAL_POSITION_ID`.

## V2.4.8 Audit: Real Reserve and MT5 State Reconciliation
V2.4.8 adds `ReconciliationEngine.mqh` to detect divergence between `RecoveryContext` and actual MT5 state. It validates Far/Big/Small ticket, `POSITION_IDENTIFIER`, direction and volume, checks harvest-level evidence, emits reserve rebuild diagnostics from HistoryDeals, and routes hard mismatches to `STATE_RECOVERY_MISMATCH`.

## V2.4.9 Audit: Reconciliation False Positive Fix
V2.4.9 changes Reconciliation from fail-fast on small raw volume differences to normalized, severity-based handling. V2.4.10 supersedes auto-sync: Small Reverse now writes actual MT5 volume into context before reconciliation, and lot mismatches use `VolumeMismatchToleranceLots` instead of reserve-money tolerance.

## V2.4.9 P0 Audit: Reserve Ledger Source of Truth

The prior reserve rebuild approach could classify the first Initial Lock profit as a reserve credit. V2.4.9 replaces profit-based reconstruction with an explicit reserve ledger. The reconciliation engine now logs Initial Lock history as skipped, rebuilds reserve from ledger events, and treats reserve-only mismatch as non-fatal diagnostics. `STATE_RECOVERY_MISMATCH` remains reserved for structural MT5/context divergence.

## V2.4.10 P0 Audit: Synthetic Far Volume Removed

Small Reverse now treats MT5 as the source of truth after partial Big close. The expected remainder is logged for diagnostics, but `Ctx.farLot` is populated from `POSITION_VOLUME` through `GetActualPositionVolume()`. Recovery reconciliation also refreshes saved volumes from actual terminal positions, preventing stale saved lot values from creating false reconciliation failures.

## V2.4.11 P0 Audit: Unified Actual Volume Rule

The actual-volume rule is now applied to all partial-close paths, not only Small Reverse. BigHarvest Far partial close and partial-close retry paths refresh context from terminal `POSITION_VOLUME`; full close paths verify actual remaining volume and keep retry pending on `FULL_CLOSE_INCOMPLETE` instead of clearing context prematurely.

## V2.4.12 P0 Audit: Full Close Integrity

Full-close completion is now based only on actual terminal volume and `VolumeMismatchToleranceLots`. Min-lot checks are not used as close-complete criteria. The FSM blocks `STATE_CLOSED_PROFIT` when leg context or managed positions remain, and reconciliation raises `CONTEXT_CLEARED_WITH_LIVE_POSITION` if context was cleared while MT5 still has live managed positions.

## V2.4.13 P0 Audit: Reconciliation Integrity / Orphan Positions

The reconciliation engine now verifies that every managed MT5 position belongs to the active RecoveryContext or a pending/retry close operation. `ValidateNoOrphanManagedPositions()` scans by Symbol and MagicNumber, compares ticket and `POSITION_IDENTIFIER` against Far/Big/Small plus pending/retry tickets, and treats any unmanaged live position as a structural recovery mismatch.

This closes the gap where only a completely empty context was compared against `CountManagedOpenPositions()`. A cleared Far with live Big/Small context now still detects the lost Far as `ORPHAN_MANAGED_POSITION` instead of waiting for a later volume mismatch or allowing the FSM to continue.

## V2.4.15 P0 Audit: Initial Lock Recovery Architecture

Initial Lock is now integrated into the same recovery, reconciliation, and orphan-protection model as Far/Big/Small. The audit gap was that `MinusLock_INITIAL_BUY` and `MinusLock_INITIAL_SELL` were real managed positions during `STATE_INITIAL_LOCK_OPENED` but were not represented in `RecoveryContext`.

The V2.4.15 fix adds Initial BUY/SELL context fields, registers them in `OpenInitialLock()`, persists/restores them through `SaveState()`/`RecoverState()`, validates them through `ValidateInitialLockIntegrity()`, and includes them in orphan ownership matching. When one initial leg closes, the remaining leg is explicitly converted to Far and Initial context is cleared with `INITIAL_LOCK_CONVERTED_TO_FAR` diagnostics.

## V2.4.17 P0 Audit: Known Context Architecture

The EA now has a centralized context-existence model. `HasKnownContext()` covers Initial Lock, Far, Big, Small, pending operations, and retry operations, so reconciliation no longer treats only Far/Big/Small as context.

The cleared-context guard now uses the required form `!HasKnownContext() && CountManagedOpenPositions() > 0`. Startup recovery emits `RECOVERY_CONTEXT_RESTORED` and `RECONCILIATION_CONTEXT_SUMMARY`, allowing future MT5 reports to show whether Initial Lock, Far, Big, Small, Pending, or Retry context existed when reconciliation ran.

## V2.4.17 Full Phase-State Integrity Validation
The remaining reconciliation risk was that broad states were validated but intermediate money-moving phases were not. `StateIntegrityEngine.mqh` now defines a phase matrix for every `EAState`, including BigHarvest close phases, Small scenario phases, final/max-level closes and pending/retry states.

The validator logs `STATE_INTEGRITY_MATRIX` and either `STATE_INTEGRITY_PASS` or `STATE_INTEGRITY_FAIL`. Required legs are checked for ticket, identifier, direction and `POSITION_VOLUME` parity; forbidden legs raise `UNEXPECTED_POSITION_PRESENT`; missing required legs raise `EXPECTED_POSITION_MISSING`. Pending and retry phases raise `INVALID_PENDING_CONTEXT` or `INVALID_RETRY_CONTEXT` if their operation context is incomplete.

On failure, execution is stopped in `STATE_INTEGRITY_ERROR`, making phase mismatches distinct from generic recovery mismatch and preventing unsafe continuation after restarts, partial execution, broker errors or VPS interruptions.

## V2.4.18 Pending State Contract Architecture
The V2.4.17 integrity engine could validate a pending state before the FSM had prepared the matching pending context. V2.4.18 fixes that by making Pending Context creation explicit and validated before each Pending transition.

`PendingContractEngine.mqh` defines a State ↔ PendingAction matrix. `RetryOpenNewBig()` now prepares `PENDING_OPEN_SMALL` before `STATE_OPEN_NEW_SMALL_PENDING`, and `RetryOpenNewSmall()` clears pending context before returning to `STATE_BIG_SMALL_OPENED`. The integrity engine also calls `ValidatePendingStateContract()` so a pending state with the wrong action is rejected as `INVALID_PENDING_CONTRACT` / `STATE_ACTION_MISMATCH`.

BigHarvest phase shape was tightened: `STATE_BIG_HARVEST_CLOSE_SMALL` forbids Big context, and `STATE_BIG_HARVEST_CALC_NET`, `STATE_BIG_HARVEST_CLOSE_FAR`, and `STATE_BIG_HARVEST_CHECK_FINAL` forbid both Big and Small context.
