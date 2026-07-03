# Big Scenario Engineering Audit — MinusLock_BigHarvest_EA_V2

## 1. Scope and audited files

This audit covers the Big scenario only. Trading formulas were not changed; only diagnostic log/CSV evidence was added.

Audited files:

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

## 2. Executive conclusion

| Item | Status | Evidence |
|---|---|---|
| `CloseFarBudget` is calculated only from Big-scenario net variable | PASS | `ProcessBigHarvestCalcNet()` sets `pendingCloseFarBudget = realBigHarvestNet * WorkCloseFarShare`. |
| `ReserveAdd` is calculated only from Big-scenario net variable | PASS | `ProcessBigHarvestCalcNet()` sets `pendingReserveAdd = realBigHarvestNet * WorkReserveShare`. |
| Partial Far close lot is calculated only from `CloseFarBudget` | PASS | `pendingCloseFarLot = CalcCloseFarLotRounded(CalcCloseFarLotRaw(pendingCloseFarBudget, effectiveFarDistancePoints), farLot)`. |
| Reserve is not used for partial Far close | PASS | `ProcessBigHarvestCloseFar()` closes only `pendingCloseFarLot`; reserve is credited later in `ProcessBigHarvestCheckFinal()`. |
| Reserve is used for final close authorization | PASS | `CalcFinalCloseAllowed(totalReserve, farLot, effectiveFarDistancePoints)` compares reserve with remaining Far loss. |
| Big-scenario realized net is strictly closed Big only | FAIL | Current code sets `realBigHarvestNet = realClosedBigProfit + realClosedSmallProfit`; this includes closed Small result. |
| CloseFar rounded lot cannot exceed budget when far loss per lot is positive | PASS | `CalcCloseFarLotRounded()` uses `NormalizeLotDown()` and caps at current Far lot. |
| Multi-symbol isolation in Big scenario | PASS | Position selection/close/history use `_Symbol + MagicNumber`. |

### Main finding

The current implementation does **not** use a pure closed-Big-only net for the split. It calculates:

```mql5
realBigHarvestNet = realClosedBigProfit + realClosedSmallProfit;
```

This is a methodology mismatch with the requested invariant `BigNetProfit = closed Big net only`. It may be intentional in the current EA design because the Big phase closes both Big and Small before the split, but under this audit specification it is a **FAIL** and should be treated as a candidate for a separate, explicitly approved minimal fix.

No trading logic was changed in this audit.

## 3. Big scenario call map

| Step | File | Function / state | Inputs | Ctx writes | Positions opened/closed | Money / lot calculations | Next state |
|---:|---|---|---|---|---|---|---|
| 1 | `MinusLock_BigHarvest_EA.mq5` | `OnTick()` | tick, current state | refreshes risk/diagnostics | none | none | calls state machine |
| 2 | `Include/StateMachine.mqh` | `StateMachineTick()` | `State` | dispatch only | none | none | state-specific handler |
| 3 | `Include/StateMachine.mqh` | initial lock path | initial BUY/SELL snapshots | `initialBuy*`, `initialSell*`, `cycleStartBalance` | opens initial lock elsewhere | start balance / initial geometry | `STATE_INITIAL_LOCK_OPENED` |
| 4 | `Include/StateMachine.mqh` | initial plus close / Far conversion path | initial legs | Far fields populated from losing initial leg | closes profitable initial leg | ignores initial profit for RecoveryPL | `STATE_FAR_ACTIVE` |
| 5 | `Include/StateMachine.mqh` | `OpenBigSmall()` | Far context, level | `bigTicket`, `smallTicket`, lots/directions | opens Big and Small | `CalcBigLot()`, `CalcSmallLot()`, `GetBigMovePoints()` | `STATE_BIG_SMALL_OPENED` |
| 6 | `Include/StateMachine.mqh` | `CheckBigOrSmallScenario()` | Far/Big/Small snapshots | no close yet | none | profit points vs target | `STATE_BIG_HARVEST` or Small path |
| 7 | `Include/StateMachine.mqh` | `ProcessBigHarvest()` | Big scenario state | diagnostics only | none | none | `STATE_BIG_HARVEST_CLOSE_BIG` |
| 8 | `Include/StateMachine.mqh` | `ProcessBigHarvestCloseBig()` | Big/Far/Small snapshots | `pendingBigPositionId`, `currentBigMovePoints`, `effectiveFarDistancePoints` | closes Big fully | move/far-distance diagnostics | `STATE_BIG_HARVEST_CLOSE_SMALL` |
| 9 | `Include/StateMachine.mqh` | `ProcessBigHarvestCloseSmall()` | Small context | clears Small context | closes Small fully | none | `STATE_BIG_HARVEST_CALC_NET` |
| 10 | `Include/StateMachine.mqh` | `ProcessBigHarvestCalcNet()` | closed Big/Small position ids | `pendingRealNet`, `pendingReserveAdd`, `pendingCloseFarBudget`, `pendingCloseFarLot` | none | history net, split, partial Far lot | `STATE_BIG_HARVEST_CLOSE_FAR` |
| 11 | `Include/StateMachine.mqh` | `ProcessBigHarvestCloseFar()` | `pendingCloseFarLot` | refreshes `Ctx.farLot` | closes Far partially | uses only `pendingCloseFarLot` | `STATE_BIG_HARVEST_CHECK_FINAL` |
| 12 | `Include/StateMachine.mqh` | `ProcessBigHarvestCheckFinal()` | `pendingReserveAdd`, Far context | credits reserve, final-close flags | none | reserve coverage / remaining Far loss | final close, next level, max-level decision, or continue |

## 4. Exact formulas and audited evidence

### 4.1 Big level geometry

`GetBigMovePoints(level)` uses:

```mql5
WorkBigMoveStartPoints() + (level - 1) * WorkBigMoveStepPoints()
```

Therefore:

- L1 = `WorkBigMoveStartPoints()`
- L2 = `WorkBigMoveStartPoints() + WorkBigMoveStepPoints()`
- L3 = `WorkBigMoveStartPoints() + 2 * WorkBigMoveStepPoints()`

No cumulative bug like `L2 = L1 + L2` or `L3 = L1 + L2 + L3` was found.

### 4.2 Lot formulas

From `RecoveryMath.mqh`:

```mql5
BigLot   = NormalizeLotNearest(FarLot * BigRatio)
SmallLot = NormalizeLotUp(BigLot * WorkSmallRatio)
```

Partial Far close:

```mql5
CloseFarLotRaw = CloseFarBudget / (FarDistancePoints * PointValuePerLot())
CloseFarLotRounded = NormalizeLotDown(CloseFarLotRaw)
CloseFarLotRounded <= FarLot
```

Because Far close rounding is down, `CloseFarActualCost <= CloseFarBudget` when `PointValuePerLot()` and `effectiveFarDistancePoints` are positive.

### 4.3 Big-scenario net and split

`CalculateRealNetForClosedPositions()` filters by:

- `DEAL_MAGIC == MagicNumber`
- `DEAL_SYMBOL == _Symbol`
- `DEAL_ENTRY == DEAL_ENTRY_OUT`
- `DEAL_POSITION_ID` matching Big or Small position identifiers

It calculates:

```mql5
dealNet = DEAL_PROFIT + DEAL_COMMISSION + DEAL_SWAP;
```

Then `ProcessBigHarvestCalcNet()` assigns:

```mql5
realBigHarvestNet = realClosedBigProfit + realClosedSmallProfit;
pendingReserveAdd = realBigHarvestNet * WorkReserveShare;
pendingCloseFarBudget = realBigHarvestNet * WorkCloseFarShare;
```

Audit interpretation:

- The history net is symbol/magic isolated: **PASS**.
- Commission/swap are included in net: **PASS**.
- The variable named `realBigHarvestNet` includes Small net: **FAIL versus this audit specification**.

### 4.4 Profit split

The split is internally consistent:

```text
CloseFarBudget + ReserveAdd = realBigHarvestNet * (WorkCloseFarShare + WorkReserveShare)
```

`ValidateWorkingParameters()` requires `WorkCloseFarShare + WorkReserveShare == 1.0` within tolerance, so the split is complete if the input validation passes.

### 4.5 Reserve usage

Reserve credit path:

```mql5
ApplyReserveCredit(RESERVE_EVENT_BIG_HARVEST_ADD, Ctx.pendingReserveAdd);
```

This happens in `ProcessBigHarvestCheckFinal()`, after `ProcessBigHarvestCloseFar()`.

Partial Far close path:

```mql5
ClosePositionByTicket(Ctx.farTicket, Ctx.pendingCloseFarLot)
```

`pendingCloseFarLot` is derived from `pendingCloseFarBudget`, not from `Ctx.totalReserve`. No code path was found where `Ctx.totalReserve`, ledger reserve, or reserve coverage is added to partial Far close budget.

Reserve final-close path:

```mql5
CalcFinalCloseAllowed(Ctx.totalReserve, Ctx.farLot, Ctx.effectiveFarDistancePoints)
```

and final close uses reserve coverage/remaining Far loss to decide whether a full recovery completion is allowed.

## 5. Direction audit

The code establishes Big/Small relative to Far:

- Far is the losing initial leg.
- Big is opened opposite Far.
- Small is opened in Far direction.

For price down after initial lock:

- Initial BUY is losing and becomes Far = BUY.
- Big is SELL, i.e. in direction of the move and opposite Far.
- Small is BUY, i.e. in Far direction.

For price up after initial lock:

- Initial SELL is losing and becomes Far = SELL.
- Big is BUY, i.e. in direction of the move and opposite Far.
- Small is SELL, i.e. in Far direction.

## 6. Numerical example

Parameters:

```text
StartLot = 1.00
BigRatio = 1.15
SmallRatio = 0.25
CloseFarShare = 0.90
ReserveShare = 0.10
CloseBigOnSmall = 0.40
RemainBigOnSmall = 0.60
LotStep = 0.01
Assume FarDistancePoints = 200
Assume Big move = 100 points
Assume PointValuePerLot = 1.00 account currency per point per lot
```

Level 1:

```text
FarLot = 1.00
BigLot = NormalizeNearest(1.00 * 1.15) = 1.15
SmallLot = NormalizeUp(1.15 * 0.25) = 0.29
Big gross/net example = 1.15 * 100 * 1.00 = 115.00
If Small closes at -29.00, current code realBigHarvestNet = 115.00 - 29.00 = 86.00
Requested pure BigNetProfit would be 115.00
Current CloseFarBudget = 86.00 * 0.90 = 77.40
Current ReserveAdd = 86.00 * 0.10 = 8.60
Pure-Big requested CloseFarBudget would be 103.50
Pure-Big requested ReserveAdd would be 11.50
Far loss per lot = 200 * 1.00 = 200.00
Current CloseFarLotRaw = 77.40 / 200.00 = 0.387
Current CloseFarLotRoundedDown = 0.38
Current RemainingFarLot = 1.00 - 0.38 = 0.62
Current CloseFarActualCost = 0.38 * 200.00 = 76.00 <= 77.40
```

This example demonstrates the key audit finding: partial Far close is budget-safe, but the base budget currently uses `Big + Small` net rather than pure closed-Big net.

## 7. Invariant table

| Invariant | Status | File / function | Evidence / comment |
|---|---|---|---|
| `CloseFarBudget + ReserveAdd = BigNetProfit` | FAIL/RISK | `StateMachine.mqh / ProcessBigHarvestCalcNet` | True for `realBigHarvestNet`, but that variable includes Small net; fails if `BigNetProfit` means closed Big only. |
| `CloseFarBudget <= BigNetProfit` | PASS for current net; RISK for naming | `ProcessBigHarvestCalcNet` | Uses share <= 1 after validation. |
| `ReserveAdd <= BigNetProfit` | PASS for current net; RISK for naming | `ProcessBigHarvestCalcNet` | Uses share <= 1 after validation. |
| `CloseFarActualCost <= CloseFarBudget` | PASS | `RecoveryMath.mqh / CalcCloseFarLotRounded` | Raw lot is budget / loss per lot, rounded down. |
| Reserve does not decrease during partial Far close | PASS | `ProcessBigHarvestCloseFar` | No `ApplyReserveDebit()` call in partial Far path. |
| `FarLotAfter = FarLotBefore - ActualCloseFarLot` | PASS/RISK | `ProcessBigHarvestCloseFar` | Terminal volume is refreshed after broker close; exact result depends on broker fill. |
| Big is fully closed in Big scenario | PASS | `ProcessBigHarvestCloseBig` | Full close then `VerifyFullClose()`. |
| Small is closed in Big scenario before net calculation | PASS | `ProcessBigHarvestCloseSmall` | Full close then `VerifyFullClose()`. |
| RecoveryPL excludes Initial ignored profit | PASS | real recovery history path | Initial lock comments are skipped. |
| FinalClose allowed only when recovery/final projection is positive | PASS | `ProcessFinalClose` | Forecast checks projected recovery PL > 0 before final close. |
| Reserve is used only for final close / completion decision | PASS | `ProcessBigHarvestCheckFinal`, `ProcessFinalClose` | Reserve is checked against remaining Far loss for final close. |
| Multi-symbol Big scenario isolation | PASS | `PositionUtils`, `TradeEngine`, history net | Position and history filters use `_Symbol + MagicNumber`. |

## 8. Required diagnostics added

Non-trading diagnostics added in this audit:

- `BIG_SCENARIO_START`
- `BIG_CLOSED`
- `BIG_NET_PROFIT`
- `BIG_PROFIT_SPLIT`
- `CLOSE_FAR_BUDGET`
- `RESERVE_ADD`
- `PARTIAL_FAR_CLOSE`
- `FAR_REMAINING`
- `RESERVE_AFTER`
- `BIG_SCENARIO_END`
- `BIG_SCENARIO_AUDIT` CSV row

These diagnostics do not change the order of orders, formulas, lots, closes, reserve debits/credits, or state transitions.

## 9. Found errors

### ERROR-1: `realBigHarvestNet` includes Small net

Current implementation:

```mql5
realBigHarvestNet = realClosedBigProfit + realClosedSmallProfit;
```

Why it is an error under this audit specification:

- The specification requires Big profit to be closed-Big-only.
- The current split uses Big plus Small net after both positions are closed.
- Therefore the split is not strictly `closed Big net -> close Far + reserve`.

Minimal fix proposal, not applied in this audit:

```mql5
BigNetProfit = realClosedBigProfit;
SmallNet should be logged separately and handled by explicitly approved policy.
CloseFarBudget = BigNetProfit * WorkCloseFarShare;
ReserveAdd = BigNetProfit * WorkReserveShare;
```

Required follow-up tests before applying:

- Strategy Tester comparing current `realBigHarvestNet` policy vs pure `BigNetProfit` policy.
- Static check ensuring `pendingCloseFarBudget` and `pendingReserveAdd` use pure Big net only.
- Regression test for RecoveryPL and final close behavior.

## 10. Risks

| Risk | Severity | Notes |
|---|---|---|
| Current Big split uses Small net too | HIGH | May reduce or increase CloseFarBudget/ReserveAdd depending on Small close result. |
| Existing variable name `realBigHarvestNet` hides Big+Small semantics | MEDIUM | Diagnostics now logs both `BigNetProfit` and `SmallNet`. |
| Broker partial fill/slippage can alter actual Far remaining lot | MEDIUM | Code refreshes Far volume after close; CSV/logs should be reviewed in MT5. |
| Internal simulation path maps firstNet/secondNet to aggregate profit/loss | MEDIUM | Static audit only; MT5 real history path is stricter by position id. |

## 11. MT5 validation plan

Required Strategy Tester runs:

1. USDJPY / M30 / 2025.02.24—2025.03.31 / `StartLot=1.00` / `CloseFarShare=0.90` / `ReserveShare=0.10` / `GeometryMode=GEOMETRY_MANUAL`.
2. Same test with `CloseFarShare=0.20` / `ReserveShare=0.80`.

Compare:

- BigLevel
- RecoveryPL
- cumulative CloseFarLot
- Reserve after each Big scenario
- FinalClose
- MaxDD
- `BIG_SCENARIO_AUDIT` CSV rows
- Experts log tokens listed above

MT5 execution could not be performed in the current Linux container because MetaEditor/MT5/Wine are unavailable.
