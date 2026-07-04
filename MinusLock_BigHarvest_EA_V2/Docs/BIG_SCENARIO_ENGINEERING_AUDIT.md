# Big Scenario Engineering Audit

## 1. Scope and non-trading-change rule

This document audits the Big-scenario path of `MinusLock_BigHarvest_EA_V2` without changing trading logic. The reviewed path is:

`Initial Lock -> Far assignment -> Big/Small open -> Big-direction move -> Big and Small close -> approved net split -> partial Far close -> reserve add -> final-close check or next Big level`.

The audit covers these files:

- `MinusLock_BigHarvest_EA.mq5`
- `Include/StateMachine.mqh`
- `Include/RecoveryMath.mqh`
- `Include/TradeEngine.mqh`
- `Include/PositionUtils.mqh`
- `Include/GeometryEngine.mqh`
- `Include/RiskManager.mqh`
- `Include/Logger.mqh`
- `Include/Types.mqh`
- `Include/Config.mqh`
- `Include/LotUtils.mqh`
- `Include/SimulationEngine.mqh`
- `Docs/MANUAL.md`
- `Docs/TEST_PLAN.md`
- `Tests/*`

## 2. Approved Big Scenario Net Model

**PASS: `BigScenarioNet = ClosedBigNet + ClosedSmallNet` is the approved model of the system.**

In the Big-scenario branch the EA closes the profitable Big leg and the paired Small leg as a single scenario event. The working harvest base is therefore the combined clean result of both closed legs:

```text
ClosedBigNet      = net result of the closed Big leg only
ClosedSmallNet    = net result of the closed Small leg only
BigScenarioNet    = ClosedBigNet + ClosedSmallNet
CloseFarBudget    = BigScenarioNet * CloseFarShare
ReserveAdd        = BigScenarioNet * ReserveShare
```

This is not a defect. The split base is explicitly the approved Big+Small net, not closed Big alone. The diagnostic name `BigScenarioNet` is used in reports, logs and simulation output to avoid ambiguity.

## 3. Call map

| Step | File / function | Inputs | Ctx changes | Positions | Money / lots | State effect |
|---|---|---|---|---|---|---|
| Tick entry | `MinusLock_BigHarvest_EA.mq5 / OnTick()` | Current symbol tick, inputs, existing `Ctx` | None directly beyond delegated calls | None directly | None directly | Delegates to state machine. |
| State dispatch | `Include/StateMachine.mqh / StateMachineTick()` | `Ctx.state`, symbol positions | May move state-specific workflow forward | None directly | None directly | Calls handlers for initial, recovery and close states. |
| Initial plus close | `Include/StateMachine.mqh / CheckInitialPlusClose()` | Initial BUY/SELL tickets, current price | Selects plus leg and surviving minus leg | Closes plus Initial | Records ignored initial profit where configured | Advances toward Far creation. |
| Far conversion | `Include/StateMachine.mqh / ConvertInitialLockToFar()` | Remaining Initial position | Sets Far ticket, direction and lot | Surviving Initial becomes Far | Far floating loss is tracked separately | Prepares level opening. |
| Big/Small open | `Include/StateMachine.mqh / OpenBigSmall()` | Far lot, ratios, geometry | Stores Big/Small tickets, lots and level | Opens Big opposite Far and Small with Far direction | Uses rounded Big/Small lots | Enters active recovery level. |
| Big scenario detection | `Include/StateMachine.mqh / CheckBigScenario()` | Big ticket, Small ticket, prices | Starts Big-scenario processing when target reached | Big and Small selected by symbol+magic tickets | Captures candidate close values | Enters Big harvest processing. |
| Scenario close | `Include/StateMachine.mqh / ProcessBigHarvestCalcNet()` | Closed Big and Small deal results | Updates realized scenario diagnostics | Big closes fully; Small closes according to Big branch | Computes `ClosedBigNet`, `ClosedSmallNet`, `BigScenarioNet` | Proceeds to split. |
| Split | `Include/StateMachine.mqh / ProcessBigHarvestCalcNet()` | `BigScenarioNet`, `CloseFarShare`, `ReserveShare` | Calculates budgets | None | `CloseFarBudget`, `ReserveAdd` | Proceeds to partial Far close. |
| Partial Far close | `Include/StateMachine.mqh / ProcessBigHarvestCalcNet()` plus trade helpers | `CloseFarBudget`, Far loss-per-lot, lot step | Reduces Far lot only by budget-derived lot | Partially closes Far | `CloseFarLotRaw`, rounded close lot, remaining Far | Keeps cycle alive or prepares final close. |
| Reserve add | `Include/StateMachine.mqh / ProcessBigHarvestCalcNet()` | `ReserveAdd` | Increases `Ctx.totalReserve` | None | Reserve only receives scenario split remainder | Reserve is available for final close checks only. |
| Final decision | `Include/StateMachine.mqh / CheckFinalCloseAllowed()` and close handlers | Far remaining loss, reserve, recovery result | May close cycle or advance level | Full close only if allowed | Uses reserve coverage / recovery PL diagnostics | Final close or next Big level. |
| Logging/CSV | `Include/Logger.mqh` | `Ctx`, symbol, scenario diagnostics | None | None | Writes traceable scenario fields | Audit observability only. |

## 4. Profit split and reserve usage findings

| Finding | Status | Evidence / rationale |
|---|---|---|
| Big-scenario harvest base is approved Big+Small net. | PASS | The approved model is `BigScenarioNet = ClosedBigNet + ClosedSmallNet`. |
| `CloseFarBudget` is derived from `BigScenarioNet`. | PASS | The split formula is `CloseFarBudget = BigScenarioNet * CloseFarShare`. |
| `ReserveAdd` is derived from `BigScenarioNet`. | PASS | The split formula is `ReserveAdd = BigScenarioNet * ReserveShare`. |
| `CloseFarBudget + ReserveAdd = BigScenarioNet` when shares sum to `1.00`. | PASS | Static checks and the trace simulator verify the invariant per level. |
| Reserve is not used for partial Far close. | PASS | Partial Far close lot is budget-driven; reserve increases after the split and is used for final close coverage, not for partial Far cost. |
| Partial Far actual cost remains within `CloseFarBudget`. | PASS | The trace simulator rounds partial close lot down to lot step and asserts `CloseFarActualCost <= CloseFarBudget`. |
| Multi-symbol Big scenario isolation. | PASS | Position helpers and diagnostics are scoped by symbol+magic; static tests assert the guard tokens. |

## 5. Dynamic trace simulator

A no-MT5 trace simulator was added at `Tools/simulate_big_scenario_trace.py`. It models the approved Big-scenario arithmetic only; it does not import or modify EA trading logic.

Default command:

```bash
python3 Tools/simulate_big_scenario_trace.py
```

Generated outputs:

- `Reports/BigScenario_Trace.csv`
- `Reports/BigScenario_Trace_Report.md`

The simulator validates these invariants on every level:

```text
BigScenarioNet = ClosedBigNet + ClosedSmallNet
CloseFarBudget = BigScenarioNet * CloseFarShare
ReserveAdd = BigScenarioNet * ReserveShare
CloseFarBudget + ReserveAdd = BigScenarioNet
CloseFarActualCost <= CloseFarBudget
ReserveAfter >= PreviousReserve
FarLotAfter = FarLotBefore - CloseFarLotRounded
```

## 6. Numeric scenario used by the trace

Default parameters:

```text
StartLot = 1.00
BigRatio = 1.15
SmallRatio = 0.25
CloseBigOnSmall = 0.40
RemainBigOnSmall = 0.60
LotStep = 0.01
PointValuePerLot = 1.00
FarDistancePoints = 200
BigMovePoints = 100
MaxLevels = 25
```

### 90/10 profile

`CloseFarShare = 0.90`, `ReserveShare = 0.10` sends most of `BigScenarioNet` to partial Far close.

Trace result:

```text
TotalClosedFarLot = 0.93
RemainingFarLot = 0.07
ReserveAfter = 21.50
LevelsToFinalClose = 6
RecoveryPL = 7.50
FinalAction = FINAL_CLOSE
```

### 20/80 profile

`CloseFarShare = 0.20`, `ReserveShare = 0.80` sends most of `BigScenarioNet` to reserve.

Trace result:

```text
TotalClosedFarLot = 0.22
RemainingFarLot = 0.78
ReserveAfter = 190.40
LevelsToFinalClose = 3
RecoveryPL = 34.40
FinalAction = FINAL_CLOSE
```

### Comparison conclusion

90/10 closes materially more Far lot and leaves materially less remaining Far. 20/80 accumulates reserve faster and can reach final-close coverage earlier in this synthetic profile. Both profiles preserve the required rule: partial Far close is funded only by `CloseFarBudget`, and reserve is not consumed by the partial Far close.

## 7. Invariant table

| Invariant | Status | Source / test | Comment |
|---|---|---|---|
| `BigScenarioNet = ClosedBigNet + ClosedSmallNet` | PASS | `Tools/simulate_big_scenario_trace.py`, `Tests/big_scenario_approved_net_model_check.py` | Approved model. |
| `CloseFarBudget = BigScenarioNet * CloseFarShare` | PASS | `Tests/big_profit_split_check.py`, trace simulator | Budget is scenario-net based. |
| `ReserveAdd = BigScenarioNet * ReserveShare` | PASS | `Tests/big_profit_split_check.py`, trace simulator | Reserve add is scenario-net based. |
| `CloseFarBudget + ReserveAdd = BigScenarioNet` | PASS | `Tests/big_scenario_trace_simulation_check.py` | Requires shares sum to `1.00`. |
| `CloseFarActualCost <= CloseFarBudget` | PASS | `Tests/far_partial_budget_check.py`, trace simulator | Partial Far lot is rounded down in trace checks. |
| Reserve does not decrease during partial Far close | PASS | `Tests/reserve_not_used_for_partial_far_check.py`, trace simulator | Reserve is only increased by `ReserveAdd` during the split. |
| `FarLotAfter = FarLotBefore - CloseFarLotRounded` | PASS | Trace simulator | Per-level invariant. |
| Big closes fully in Big scenario | PASS | `Tests/big_scenario_state_flow_check.py` | Diagnostic flow includes `BIG_CLOSED`. |
| Small close is included in approved scenario net | PASS | `Tests/big_scenario_approved_net_model_check.py` | `ClosedSmallNet` is explicit in diagnostics. |
| Final close depends on recovery / reserve coverage | PASS | `Include/StateMachine.mqh`, trace report | Reserve is evaluated for final close, not partial Far funding. |
| Symbol+magic scoping | PASS | `Tests/big_scenario_multisymbol_guard_check.py` | Multi-symbol guard coverage. |

## 8. CSV and log observability

The diagnostic CSV/log vocabulary is now explicit:

```text
ClosedBigNet
ClosedSmallNet
BigScenarioNet
CloseFarBudget
ReserveAdd
CloseFarLot
RemainingFarLot
ReserveCoverage
```

The Big-scenario log token is:

```text
BIG_SCENARIO_NET ClosedBigNet=... ClosedSmallNet=... BigScenarioNet=...
```

This avoids implying that the split base is closed Big alone.

## 9. Found issues and risks

### Found issues

No trading-math defect was found under the clarified approved model. The prior audit wording that treated Big+Small as an error has been corrected.

### Remaining risks

| Risk | Severity | Mitigation |
|---|---|---|
| The approved Big+Small model depends on unambiguous diagnostics. | Medium | Logs, CSV aliases, report terms and static tests now use `BigScenarioNet`, `ClosedBigNet`, `ClosedSmallNet`. |
| Synthetic trace is not a substitute for MT5 execution. | Medium | MT5 Strategy Tester remains required for live-execution validation. |
| Broker lot-step / commission details may differ from trace assumptions. | Medium | Trace uses configurable `LotStep`, `PointValuePerLot`, `FarDistancePoints`, and `BigMovePoints`; MT5 validation must confirm broker-specific values. |

## 10. Final conclusion

The approved Big scenario model is mathematically traceable:

```text
BigScenarioNet = ClosedBigNet + ClosedSmallNet
BigScenarioNet = CloseFarBudget + ReserveAdd
Partial Far Close uses only CloseFarBudget
Reserve remains untouched by partial Far close and is accumulated for final close coverage
```

The generated trace CSV and Markdown report prove the model level-by-level for 90/10 and 20/80 splits without requiring MT5.

## Configured vs Runtime Geometry note

Big-scenario diagnostics depend on the active cycle's work geometry. For audit clarity, geometry logs and CSV now separate `ConfiguredGeometryMode` from `RuntimeGeometryMode`. After terminal cleanup such as `STATE_STOP_MAX_LEVELS`, the runtime mode is reported as `NO_ACTIVE_CYCLE` with `GeometrySource=CLEARED` and `GeometryClearReason=STATE_STOP_MAX_LEVELS`; this prevents a cleared ATR cycle from being misread as an active manual-mode Big scenario.
