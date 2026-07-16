# Big Scenario Full Engineering Audit

## 1. Scope and verdict

Project: `MinusLock_BigHarvest_EA_V2`.

This audit covers the complete Big-only recovery path from the initial lock to final recovery close and the offline parameter search that keeps `StartLot=1.00` fixed. The code path was checked in:

- `MinusLock_BigHarvest_EA.mq5`
- `Include/StateMachine.mqh`
- `Include/RecoveryMath.mqh`
- `Include/TradeEngine.mqh`
- `Include/PositionUtils.mqh`
- `Include/LotUtils.mqh`
- `Include/GeometryEngine.mqh`
- `Include/RiskManager.mqh`
- `Include/Logger.mqh`
- `Include/Types.mqh`
- `Include/Config.mqh`
- `Docs/MANUAL.md`
- `Docs/BIG_SCENARIO_ENGINEERING_AUDIT.md`
- `Reports/BigScenario_Trace_Report.md`
- `Reports/BigScenario_Trace.csv`
- `Tools/simulate_big_scenario_trace.py`
- `Tools/optimize_big_scenario_min_levels.py`

Final audit verdict: **PASS with MT5-validation requirement**. The Big-scenario math is internally consistent: `BigScenarioNet` is the sum of closed Big and Small results, it is split into `CloseFarBudget` and `ReserveAdd`, partial Far close is budget-only, reserve is applied after the partial close phase and is used for final close eligibility. The offline optimizer found one-level Big-only trend candidates at fixed `StartLot=1.00`; they are engineering candidates and still require MetaTrader Strategy Tester confirmation.

## 2. Full Big-scenario map

```text
STATE_IDLE
  -> OpenInitialLock()
  -> Initial BUY + Initial SELL opened with StartLot
  -> CheckInitialPlusClose()
  -> profitable Initial leg closes after WorkInitialTriggerPoints
  -> initial profit is ignored, not added to reserve
  -> remaining losing Initial leg becomes Far
  -> STATE_FAR_ACTIVE
  -> OpenBigSmall()
  -> Big opens opposite Far, Small opens same direction as Far
  -> STATE_BIG_SMALL_OPENED
  -> CheckBigScenario()
  -> price reaches GetBigMovePoints(level) in Big direction
  -> STATE_BIG_HARVEST
  -> ProcessBigHarvest()
  -> STATE_BIG_HARVEST_CLOSE_BIG
  -> ProcessBigHarvestCloseBig(): close Big fully
  -> STATE_BIG_HARVEST_CLOSE_SMALL
  -> ProcessBigHarvestCloseSmall(): close Small fully
  -> STATE_BIG_HARVEST_CALC_NET
  -> ProcessBigHarvestCalcNet(): calculate BigScenarioNet and split
  -> STATE_BIG_HARVEST_CLOSE_FAR
  -> ProcessBigHarvestCloseFar(): partial Far close from CloseFarBudget only
  -> STATE_BIG_HARVEST_CHECK_FINAL
  -> ProcessBigHarvestCheckFinal(): add reserve and check final close
  -> STATE_FINAL_CLOSE if TotalReserve covers remaining Far
  -> STATE_FAR_ACTIVE if next Big level is needed
  -> STATE_MAX_LEVELS_DECISION / STATE_STOP_MAX_LEVELS if levels are exhausted
```

## 3. Function/file table

| Stage | File | Function | Responsibility | RecoveryContext changes |
|---|---|---|---|---|
| Init and tick loop | `MinusLock_BigHarvest_EA.mq5` | `OnInit`, `OnTick` | Validate inputs, recover state, run reconciliation, run FSM | Starts from restored or reset context |
| Initial lock | `Include/StateMachine.mqh` | `OpenInitialLock`, `CheckInitialPlusClose` | Open BUY/SELL and convert loser to Far | Sets `initial*`, then `far*`, `initialProfitIgnored=true` |
| Geometry | `Include/RecoveryMath.mqh`, `Include/GeometryEngine.mqh` | `GetBigMovePoints`, `Work*Points` | Calculate Big trigger distance | Reads `Ctx.work*` geometry fields |
| Big/Small open | `Include/StateMachine.mqh` | `OpenBigSmall` | Open Big opposite Far and Small same as Far | Sets `bigTicket`, `smallTicket`, lots, directions, level |
| Big trigger | `Include/StateMachine.mqh` | `CheckBigScenario` | Detect Big-side movement | Moves to `STATE_BIG_HARVEST` |
| Big close | `Include/StateMachine.mqh` | `ProcessBigHarvestCloseBig` | Close Big fully and capture real identifiers | Clears Big context after verified full close |
| Small close | `Include/StateMachine.mqh` | `ProcessBigHarvestCloseSmall` | Close Small fully | Clears Small context after verified full close |
| Net/split | `Include/StateMachine.mqh` | `ProcessBigHarvestCalcNet` | Calculate `BigScenarioNet`, `CloseFarBudget`, `ReserveAdd`, `pendingCloseFarLot` | Sets pending net/budget/reserve/Far-close lot |
| Far partial | `Include/StateMachine.mqh` | `ProcessBigHarvestCloseFar` | Close Far by `pendingCloseFarLot` only | Refreshes actual remaining Far lot |
| Reserve/final | `Include/StateMachine.mqh` | `ProcessBigHarvestCheckFinal` | Apply reserve and decide final/next level/max levels | Credits `Ctx.totalReserve`, sets final state transition |
| Math | `Include/RecoveryMath.mqh` | `CalcBigLot`, `CalcSmallLot`, `CalcCloseFarBudget`, `CalcReserveAdd`, `CalcCloseFarLotRaw`, `CalcCloseFarLotRounded`, `CalcFinalCloseAllowed` | Atomic formulas | No direct mutation |
| Lot rounding | `Include/LotUtils.mqh` | `NormalizeLotDown`, `NormalizeLotUp`, `NormalizeLotNearest`, `NormalizeVolumeToStep` | Broker/user lot step alignment | No direct mutation |
| Trading | `Include/TradeEngine.mqh` | `OpenPosition`, `ClosePositionByTicket*` | Executes real/simulated opens and closes | Mutations happen through state functions after verification |
| Logging | `Include/Logger.mqh` | `LogCycleMathDetailed`, CSV helpers | Diagnostics and audit CSV | No trading mutation |

## 4. Real code fragments and conclusions

### 4.1 Big level formula

Файл: `Include/RecoveryMath.mqh`  
Функция: `GetBigMovePoints`

```mql5
int GetBigMovePoints(const int level)
{
   if(level <= 0)
      return 0;

   return WorkBigMoveStartPoints() + (level - 1) * WorkBigMoveStepPoints();
}
```

Conclusion: the actual formula is:

```text
L1 = WorkBigMoveStartPoints
L2 = WorkBigMoveStartPoints + WorkBigMoveStepPoints
L3 = WorkBigMoveStartPoints + 2 × WorkBigMoveStepPoints
Ln = WorkBigMoveStartPoints + (n - 1) × WorkBigMoveStepPoints
```

### 4.2 Big/Small lot formulas

Файл: `Include/RecoveryMath.mqh`  
Функции: `CalcBigLot`, `CalcSmallLot`

```mql5
double CalcBigLot(double farLot)
{
   return NormalizeLotNearest(farLot * BigRatio);
}

double CalcSmallLot(double bigLot)
{
   return NormalizeLotUp(bigLot * WorkSmallRatio);
}
```

Conclusion: Big is rounded to nearest lot step; Small is rounded up. The optimizer mirrors this with `round_nearest()` and `round_up()`.

### 4.3 Big/Small/Far direction rules

Файл: `Include/StateMachine.mqh`  
Функция: `OpenBigSmall`

```mql5
Ctx.bigDirection = (Ctx.farDirection == DIR_BUY) ? DIR_SELL : DIR_BUY;
Ctx.smallDirection = Ctx.farDirection;
Ctx.bigLot = CalcBigLot(Ctx.farLot);
Ctx.smallLot = CalcSmallLot(Ctx.bigLot);
```

Conclusion: if Far is BUY, Big is SELL and Small is BUY. If Far is SELL, Big is BUY and Small is SELL. This is symmetric for upward and downward price movement.

### 4.4 Big-scenario phase entry

Файл: `Include/StateMachine.mqh`  
Функция: `ProcessBigHarvest`

```mql5
void ProcessBigHarvest()
{
   LogInfo(StringFormat("BIG_SCENARIO_START Level=%d FarTicket=%I64u BigTicket=%I64u SmallTicket=%I64u FarLot=%.2f BigLot=%.2f SmallLot=%.2f TotalReserve=%.2f",
                        Ctx.harvestLevel, Ctx.farTicket, Ctx.bigTicket, Ctx.smallTicket, Ctx.farLot, Ctx.bigLot, Ctx.smallLot, Ctx.totalReserve));
   SetState(STATE_BIG_HARVEST_CLOSE_BIG, "BigHarvest phase FSM start");
}
```

Conclusion: Big harvest is phase-based; it does not calculate profit immediately. It first routes to atomic Big close.

### 4.5 Big close and effective Far distance

Файл: `Include/StateMachine.mqh`  
Функция: `ProcessBigHarvestCloseBig`

```mql5
Ctx.currentBigMovePoints = CalcMovePointsBetween(Ctx.bigOpenPrice, bigClosePrice);
Ctx.cumulativeBigMovePoints += Ctx.currentBigMovePoints;
Ctx.currentClosePrice = bigClosePrice;
Ctx.effectiveFarDistancePoints = CalcEffectiveFarDistancePoints(
   Ctx.initialFarDistancePoints,
   Ctx.currentBigMovePoints,
   Ctx.cumulativeBigMovePoints,
   Ctx.currentClosePrice,
   Ctx.farOpenPrice
);

if(!ClosePositionByTicket(Ctx.bigTicket, Ctx.bigLot))
{
   SetPendingOperation(PENDING_CLOSE_BIG_FULL, "BIG_HARVEST_CLOSE_BIG", STATE_CLOSE_BIG_PENDING, Ctx.bigTicket, Ctx.bigLot, "RETRY_CLOSE_BIG", STATE_BIG_HARVEST_CLOSE_SMALL, "BigHarvest phase close Big failed; retry pending");
   return;
}
```

Conclusion: the close price and Big movement are captured before Big is closed; `effectiveFarDistancePoints` is therefore available for budget-to-Far-lot conversion.

### 4.6 Small close

Файл: `Include/StateMachine.mqh`  
Функция: `ProcessBigHarvestCloseSmall`

```mql5
if(!ClosePositionByTicket(Ctx.smallTicket, Ctx.smallLot))
{
   SetPendingOperation(PENDING_CLOSE_SMALL_FULL, "BIG_HARVEST_CLOSE_SMALL", STATE_CLOSE_SMALL_PENDING, Ctx.smallTicket, Ctx.smallLot, "RETRY_CLOSE_SMALL", STATE_BIG_HARVEST_CALC_NET, "BigHarvest phase close Small failed; retry pending");
   return;
}

if(!VerifyFullClose(Ctx.smallTicket, "BIG_HARVEST_CLOSE_SMALL"))
{
   Ctx.smallLot = NormalizeVolumeToStep(GetActualPositionVolume(Ctx.smallTicket));
   SetPendingOperation(PENDING_CLOSE_SMALL_FULL, "BIG_HARVEST_CLOSE_SMALL", STATE_CLOSE_SMALL_PENDING, Ctx.smallTicket, Ctx.smallLot, "RETRY_CLOSE_SMALL", STATE_BIG_HARVEST_CALC_NET, "FULL_CLOSE_INCOMPLETE after BigHarvest Small close; retry pending");
   return;
}
```

Conclusion: Small is closed fully and verified before net calculation.

### 4.7 BigScenarioNet formula and split

Файл: `Include/StateMachine.mqh`  
Функция: `ProcessBigHarvestCalcNet`

```mql5
bool foundDeals = CalculateRealNetForClosedPositions(Ctx.pendingBigPositionId, Ctx.pendingSmallPositionId, Ctx.pendingOperationStartTime, realClosedBigProfit, realClosedSmallProfit, realCommission, realSwap);
double realBigHarvestNet = realClosedBigProfit + realClosedSmallProfit;
Ctx.pendingRealNet = realBigHarvestNet;

if(foundDeals && realBigHarvestNet > 0.0)
{
   Ctx.pendingReserveAdd = realBigHarvestNet * WorkReserveShare;
   Ctx.pendingCloseFarBudget = realBigHarvestNet * WorkCloseFarShare;
}
```

Conclusion:

```text
BigScenarioNet = ClosedBigNet + ClosedSmallNet
CloseFarBudget = BigScenarioNet × CloseFarShare
ReserveAdd = BigScenarioNet × ReserveShare
CloseFarBudget + ReserveAdd = BigScenarioNet, because WorkCloseFarShare + WorkReserveShare is validated as 1.0
```

### 4.8 CloseFarBudget-only Far partial close

Файл: `Include/StateMachine.mqh`  
Функция: `ProcessBigHarvestCalcNet`

```mql5
Ctx.pendingCloseFarLot = CalcCloseFarLotRounded(CalcCloseFarLotRaw(Ctx.pendingCloseFarBudget, Ctx.effectiveFarDistancePoints), Ctx.farLot);
double closeFarLotRaw = CalcCloseFarLotRaw(Ctx.pendingCloseFarBudget, Ctx.effectiveFarDistancePoints);
double closeFarActualCost = CalcFarRemainLoss(Ctx.pendingCloseFarLot, Ctx.effectiveFarDistancePoints);
```

Файл: `Include/RecoveryMath.mqh`  
Функции: `CalcCloseFarLotRaw`, `CalcCloseFarLotRounded`

```mql5
double CalcCloseFarLotRaw(double closeFarBudget, double farDistancePoints)
{
   double lossPerLot = farDistancePoints * PointValuePerLot();

   if(lossPerLot <= 0.0)
      return 0.0;

   return closeFarBudget / lossPerLot;
}

double CalcCloseFarLotRounded(double rawLot, double farLot)
{
   double rounded = NormalizeLotDown(rawLot);

   if(rounded > farLot)
      rounded = farLot;

   return NormalizeLotDown(rounded);
}
```

Conclusion: partial Far close is financed only by `pendingCloseFarBudget`. It is rounded down, so `CloseFarActualCost <= CloseFarBudget` unless broker execution violates assumptions; the code logs an explicit CSV stop reason if the invariant is exceeded.

### 4.9 Reserve is not used for partial Far close

Файл: `Include/StateMachine.mqh`  
Функции: `ProcessBigHarvestCloseFar`, `ProcessBigHarvestCheckFinal`

```mql5
if(!ClosePositionByTicket(Ctx.farTicket, Ctx.pendingCloseFarLot))
{
   SetPendingOperation(PENDING_CLOSE_FAR_PARTIAL, "BIG_HARVEST_CLOSE_FAR", STATE_CLOSE_NEW_FAR_PENDING, Ctx.farTicket, Ctx.pendingCloseFarLot, "RETRY_CLOSE_FAR_BUDGET", STATE_BIG_HARVEST_CHECK_FINAL, "BigHarvest close Far budget failed; retry pending");
   return;
}
```

```mql5
if(!Ctx.pendingReserveApplied)
{
   ApplyReserveCredit(RESERVE_EVENT_BIG_HARVEST_ADD, Ctx.pendingReserveAdd);
   Ctx.pendingReserveApplied = true;
}
```

Conclusion: reserve is credited only in `ProcessBigHarvestCheckFinal`, after `ProcessBigHarvestCloseFar`. Therefore `Ctx.totalReserve` is not the funding source for partial Far close. It is used only for final close eligibility through `CalcFinalCloseAllowed()`.

### 4.10 Final close reserve check

Файл: `Include/RecoveryMath.mqh`  
Функция: `CalcFinalCloseAllowed`

```mql5
bool CalcFinalCloseAllowed(double totalReserve, double farRemainLot, double farDistancePoints)
{
   double farRemainLoss = CalcFarRemainLoss(farRemainLot, farDistancePoints);
   return totalReserve >= farRemainLoss;
}
```

Файл: `Include/StateMachine.mqh`  
Функция: `ProcessBigHarvestCheckFinal`

```mql5
double farRemainLoss = CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints);
Ctx.finalCloseAllowed = CalcFinalCloseAllowed(Ctx.totalReserve, Ctx.farLot, Ctx.effectiveFarDistancePoints);
```

Conclusion: reserve is used for the full residual Far close decision, not for partial Far close.

### 4.11 Lot-step rounding

Файл: `Include/LotUtils.mqh`

```mql5
double NormalizeLotDown(double lot)
{
   double step = GetEffectiveLotStep();
   double minLot = GetMinLot();
   double maxLot = GetMaxLot();

   if(step <= 0.0 || lot <= 0.0)
      return 0.0;

   double result = MathFloor((lot + 0.000000001) / step) * step;

   if(result < minLot)
      return 0.0;

   if(result > maxLot)
      result = maxLot;

   return NormalizeDouble(result, VolumeDigits());
}
```

Conclusion: budget-derived Far lots are rounded down and cannot exceed the budget under the mathematical model.

## 5. StateMachine transitions

| From | Trigger | To | Function |
|---|---|---|---|
| `STATE_FAR_ACTIVE` | Need next recovery level | `STATE_BIG_SMALL_OPENED` | `OpenBigSmall()` |
| `STATE_BIG_SMALL_OPENED` | Big target touched | `STATE_BIG_HARVEST` | `CheckBigScenario()` |
| `STATE_BIG_HARVEST` | Phase start | `STATE_BIG_HARVEST_CLOSE_BIG` | `ProcessBigHarvest()` |
| `STATE_BIG_HARVEST_CLOSE_BIG` | Big fully closed | `STATE_BIG_HARVEST_CLOSE_SMALL` | `ProcessBigHarvestCloseBig()` |
| `STATE_BIG_HARVEST_CLOSE_SMALL` | Small fully closed | `STATE_BIG_HARVEST_CALC_NET` | `ProcessBigHarvestCloseSmall()` |
| `STATE_BIG_HARVEST_CALC_NET` | Net/split calculated | `STATE_BIG_HARVEST_CLOSE_FAR` | `ProcessBigHarvestCalcNet()` |
| `STATE_BIG_HARVEST_CLOSE_FAR` | Budget Far close done | `STATE_BIG_HARVEST_CHECK_FINAL` | `ProcessBigHarvestCloseFar()` |
| `STATE_BIG_HARVEST_CHECK_FINAL` | Far fully closed | `STATE_CLOSED_PROFIT` / `STATE_CLOSED_RECOVERY_LOSS` | `ProcessBigHarvestCheckFinal()` |
| `STATE_BIG_HARVEST_CHECK_FINAL` | Reserve covers Far | `STATE_FINAL_CLOSE` | `ProcessBigHarvestCheckFinal()` |
| `STATE_BIG_HARVEST_CHECK_FINAL` | More levels allowed | `STATE_FAR_ACTIVE` | `ProcessBigHarvestCheckFinal()` |
| `STATE_BIG_HARVEST_CHECK_FINAL` | Max levels reached | `STATE_MAX_LEVELS_DECISION` | `ProcessBigHarvestCheckFinal()` |

## 6. RecoveryContext changes per Big level

For each Big level:

1. `Ctx.harvestLevel` identifies the current level.
2. `Ctx.bigLot = CalcBigLot(Ctx.farLot)` and `Ctx.smallLot = CalcSmallLot(Ctx.bigLot)` during `OpenBigSmall()`.
3. `Ctx.pendingBigPositionId` and `Ctx.pendingSmallPositionId` are captured before closing Big/Small.
4. `Ctx.currentBigMovePoints`, `Ctx.cumulativeBigMovePoints`, `Ctx.currentClosePrice`, `Ctx.effectiveFarDistancePoints` are updated in the Big close phase.
5. `Ctx.pendingRealNet` receives `BigScenarioNet`.
6. `Ctx.pendingCloseFarBudget` and `Ctx.pendingReserveAdd` receive the split.
7. `Ctx.pendingCloseFarLot` receives the budget-derived rounded Far close lot.
8. `Ctx.farLot` is refreshed from terminal after partial Far close.
9. `Ctx.totalReserve` is credited only in final-check phase.
10. `Ctx.finalCloseAllowed` is calculated from `Ctx.totalReserve` and remaining Far loss.

## 7. Level-by-level Big scenario trace fields

The optimizer and trace outputs use this level schema:

```text
Level
FarLotBefore
FarDirection
BigLot
BigDirection
SmallLot
SmallDirection
BigMovePoints
ClosedBigNet
ClosedSmallNet
BigScenarioNet
CloseFarBudget
ReserveAdd
CloseFarLotRaw
CloseFarLotRounded
CloseFarActualCost
FarLotAfter
ReserveAfter
RecoveryPL
ReserveCoverage
NextAction
```

Example best offline level from the new search:

| Level | FarLotBefore | BigLot | SmallLot | BigMovePoints | ClosedBigNet | ClosedSmallNet | BigScenarioNet | CloseFarBudget | ReserveAdd | CloseFarLotRounded | CloseFarActualCost | FarLotAfter | ReserveAfter | RecoveryPL | ReserveCoverage | NextAction |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1.00 | 1.25 | 0.32 | 250 | 312.50 | -80.00 | 232.50 | 162.75 | 69.75 | 0.90 | 162.00 | 0.10 | 69.75 | 51.75 | 3.875 | FINAL_CLOSE |

## 8. Invariant checklist

| Invariant | Verdict | Evidence |
|---|---|---|
| `BigScenarioNet = ClosedBigNet + ClosedSmallNet` | PASS | `realBigHarvestNet = realClosedBigProfit + realClosedSmallProfit` |
| `CloseFarBudget = BigScenarioNet × CloseFarShare` | PASS | `Ctx.pendingCloseFarBudget = realBigHarvestNet * WorkCloseFarShare` |
| `ReserveAdd = BigScenarioNet × ReserveShare` | PASS | `Ctx.pendingReserveAdd = realBigHarvestNet * WorkReserveShare` |
| `CloseFarBudget + ReserveAdd = BigScenarioNet` | PASS | `ValidateWorkingParameters()` requires split sum 1.0; optimizer checks split invariant |
| Partial Far close uses only `CloseFarBudget` | PASS | `pendingCloseFarLot` is derived only from `pendingCloseFarBudget` |
| Reserve is not used for partial Far close | PASS | `ApplyReserveCredit()` is called after partial Far close in check-final phase |
| Reserve is used for full residual close | PASS | `CalcFinalCloseAllowed(totalReserve, farLot, farDistance)` |
| Remaining Far is preserved | PASS | `RefreshFarVolumeFromTerminal()` updates `Ctx.farLot` after partial close |
| Directions are symmetric | PASS | Big direction is opposite Far; Small direction equals Far |
| LotStep is respected | PASS | `NormalizeLotNearest`, `NormalizeLotUp`, `NormalizeLotDown`, `NormalizeVolumeToStep` |
| Small-scenario sanity | PASS | Optimizer rejects `BigRatio² × RemainBigOnSmall >= 1` |

## 9. Reserve audit

Reserve paths checked:

- `Ctx.totalReserve`
- `Ctx.pendingReserveAdd`
- `ReserveCoverage`
- `ProjectedReserveCoverage`
- `FinalCloseAllowed`

Verdict: **Reserve is not used for partial Far close.** It is credited after the Far partial close and is used to decide whether the remaining Far can be fully closed. This matches the system requirement.

## 10. Found errors

No code-level Big-scenario invariant violation was found in the audited path. The main engineering risk is not a formula bug; it is parameter sensitivity. Too small `CloseFarShare`, too high `SmallRatio`, or too large `FarDistancePoints` can push the cycle to many levels or `STATE_STOP_MAX_LEVELS`.

## 11. Risks

1. Offline model excludes broker spread, commission, slippage and partial-fill edge cases.
2. One-level candidates can require a large Big move and may increase exposure if the market reverses before Big target.
3. `CloseFarShare=0.70` can still complete quickly in the Big-only model because reserve covers the residual Far, but lower CloseFarShare is less suitable for paths that do not reach final close quickly.
4. Aggressive BigRatio values must stay below the Small-scenario compression boundary.
5. MT5 Strategy Tester validation is still mandatory before live use.

## 12. Final verdict

Big-scenario implementation is mathematically consistent and auditable. The Python optimizer found `StartLot=1.00` parameter sets that complete the Big-only trend path in one Big level under deterministic assumptions while preserving Small-scenario compression. The best set is exported to `Sets/Unverified/BigScenario_Best_1.set (UNVERIFIED, NOT_FOR_MT5_TESTING)`; it should be treated as a Strategy Tester candidate, not a live-trading approval.

## 13. MT5 Strategy Tester invalidation addendum

The later MT5 Strategy Tester report for `Sets/Unverified/BigScenario_Best_1.set` (UNVERIFIED) is the source of truth and invalidates the previous offline one-level completion claim.

Observed MT5 facts:

- Same public parameters: `StartLot=1.00`, `BigRatio=1.11`, `SmallRatio=0.25`, `CloseFarShare=0.75`, `ReserveShare=0.25`, `BigMoveStartPoints=250`, `BigMoveStepPoints=40`, `FarDistancePoints=180`.
- MT5 result: `OnTester=-1`.
- MT5 path reached at least `MinusLock_BIG_L11`.
- MT5 ended with open managed exposure closed by end-of-test orders.

First divergence versus the previous Python model occurs at Big level 1:

```text
Python L1:
BigScenarioNet = 207.50
CloseFarBudget = 155.63
Far loss basis = fixed 180 points
CloseFarLotRounded = 0.86
NextAction = FINAL_CLOSE

MT5 L1:
ClosedBigNet = 147.73
ClosedSmallNet = -40.90
BigScenarioNet = 106.83
CloseFarBudget = 80.12
Far partial close = 0.29 lot for -78.27
NextAction = open BIG_L2
```

Root causes:

1. The Python optimizer hard-coded `PointValuePerLot=1.0`, while MT5 USDJPY with EUR deposit has dynamic tick/point value.
2. The Python optimizer used fixed `FarDistancePoints=180`, while the EA was configured with `FarDistanceMode=REAL_PRICE_DISTANCE`; L1 MT5 prices imply a much larger effective distance between Far open and Big close.
3. The Python optimizer assumed exact target-point execution, while MT5 uses real bid/ask open/close prices.
4. The Python optimizer assumed a Big-only trend path; the MT5 order/deal sequence shows mixed path behavior with subsequent Small/reverse-style transitions and direction changes.
5. The Python optimizer did not replay `HistoryDeals`, swap/commission, end-of-test closure, or strict `OnTester` pass conditions.

Updated verdict: **the Big-scenario formula audit remains useful, but the current Python optimizer is invalid for selecting working MT5 parameters.** It is retained only as an algebraic trace until it is redesigned around MT5 deal replay or Strategy Tester CSV ingestion. See `Reports/BigScenario_MT5_Divergence_Report.md` and `Reports/BigScenario_MT5_Divergence.csv`.
