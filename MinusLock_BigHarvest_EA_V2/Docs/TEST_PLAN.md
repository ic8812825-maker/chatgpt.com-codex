# MinusLock BigHarvest EA — TEST PLAN

## 1. Статические проверки

1. Проверить наличие всех файлов структуры:
   - `MinusLock_BigHarvest_EA.mq5`
   - `Include/Config.mqh`
   - `Include/Types.mqh`
   - `Include/LotUtils.mqh`
   - `Include/PositionUtils.mqh`
   - `Include/TradeEngine.mqh`
   - `Include/StateMachine.mqh`
   - `Include/RecoveryMath.mqh`
   - `Include/RiskManager.mqh`
   - `Include/Logger.mqh`
2. Проверить, что `Config.mqh` содержит параметры из ТЗ.
3. Проверить, что `StateMachine.mqh` содержит состояния начального замка, Far, Big/Small, Big-harvest, Small-сценария, FinalClose и DUAL_TAIL.

## 2. Компиляция в MetaEditor

1. Скопировать каталог `MinusLock_BigHarvest_EA` в каталог `MQL5/Experts` терминала.
2. Открыть `MinusLock_BigHarvest_EA.mq5` в MetaEditor.
3. Выполнить Compile.
4. Ожидание: 0 errors, 0 critical warnings. Любой warning, влияющий на торговую логику, должен быть исправлен.

## 3. Тест начального замка

Параметры:

```text
StartLot = 1.00
InitialTriggerPoints = 100
AllowRealTrading = false
```

Ожидание:

1. Открывается `BUY 1.00` с комментарием `MinusLock_INITIAL_BUY`.
2. Открывается `SELL 1.00` с комментарием `MinusLock_INITIAL_SELL`.
3. При движении вверх на 100 пунктов закрывается только BUY, SELL становится Far.
4. При движении вниз на 100 пунктов закрывается только SELL, BUY становится Far.
5. В логах зафиксировано, что первый плюс игнорируется.

## 4. Тест StartLot = 1.00 по мануалу

Условия:

```text
FarDistancePoints = 200
BigMoveStartPoints = 100
BigMoveStepPoints = 50
MaxHarvestLevels = 7
LotStep = 0.01
```

Ожидаемая таблица Big-harvest:

| Level | FarStart | BigMove |  Big | Small | NetProfit | CloseFar | FarRemain | Reserve | FinalClose |
| ----: | -------: | ------: | ---: | ----: | --------: | -------: | --------: | ------: | ---------- |
|     1 |     1.00 |     100 | 1.30 |  0.48 |     82.00 |     0.36 |      0.64 |    8.20 | NO         |
|     2 |     0.64 |     150 | 0.83 |  0.31 |     78.00 |     0.35 |      0.29 |   16.00 | NO         |
|     3 |     0.29 |     200 | 0.38 |  0.14 |     48.00 |     0.21 |      0.08 |   20.80 | YES        |

Финальный результат:

```text
CycleFinalPL = 20.80 - 16.00 = +4.80
```

## 5. Small-сценарий

Для `Far = 1.00` ожидается:

```text
Big = 1.30
Small = 0.48
CloseBig = 0.39
RemainBig = 0.91
NetSmall = +9 при движении 100 пунктов без costs
```

Если старый Far остаётся открытым вместе с новым хвостом из 70% Big, советник должен перейти в `STATE_DUAL_TAIL` и не открывать следующий уровень.


## 6. Локальный pre-flight без MetaEditor

В Linux-контейнере без MetaEditor выполнить:

```bash
python scripts/verify_big_harvest_ea.py
git diff --check
```

Этот pre-flight не заменяет MetaEditor Compile и Strategy Tester, но проверяет структуру проекта, обязательные параметры, обязательные поля журнала, Big-harvest математику для StartLot 1/2/5, Small-сценарий, DUAL_TAIL и risk-gates.

## Small-at-Far Scenario

Small-сценарий больше не исполняется сразу при первом движении в сторону Small. Если Small достиг защитного движения, советник переводит цикл в `STATE_WAIT_SMALL_TO_FAR` и ждёт, пока текущая цена дойдёт до цены открытия старого `Far` с учётом `SmallFarTouchOffsetPoints`. Для `Small=BUY` условие касания: `CurrentPrice >= OldFarOpenPrice + offset`; для `Small=SELL`: `CurrentPrice <= OldFarOpenPrice - offset`.

После касания старого Far выполняется `ProcessSmallAtFarTouch`: Small закрывается на 100%, старый Far закрывается на 100%, Big закрывается только на `CloseBigOnSmall`, а остаток Big становится новым Far. Затем обязательно сначала проверяется `FinalCloseAllowed` для нового Far. Если резерва хватает, новый Far закрывается полностью и состояние становится `STATE_CLOSED_PROFIT`; если резерва не хватает, только тогда открывается новый Big/Small от нового Far. В нормальном Small-at-Far сценарии `DUAL_TAIL` не должен появляться, потому что старый Far ликвидируется до назначения нового Far.

---

## Reverse Geometry Protection Tests

1. **Valid reverse**
   - `OldFarLot = 1.00`, `BigLot = 1.30`, `CloseBigLotRounded = 0.39`.
   - Ожидание: `NewFarLot = 0.91`, `NewBigLot = 1.18`, `NewSmallLot = 0.44`, `ReverseStrength ≈ 0.2967`, статус `STRONG`.

2. **Invalid NewFar**
   - `NewFarLot >= OldFarLot`.
   - Ожидание: `STATE_INVALID_REVERSE_GEOMETRY`, reason `NewFarLot >= OldFarLot`, новый Big/Small не открывать.

3. **Invalid NewBig**
   - `NewBigLot <= NewFarLot`.
   - Ожидание: `STATE_INVALID_REVERSE_GEOMETRY`, reason `NewBigLot <= NewFarLot`.

4. **Weak ReverseStrength**
   - `NewFarLot = 1.00`, `NewBigLot = 1.05`.
   - Ожидание: `STATE_INVALID_REVERSE_GEOMETRY`, reason `ReverseStrength below minimum`.

5. **Small Geometry Validator**
   - Проверить `SmallReverseNet = SmallPL + OldFarPL + ClosedBigPL`.
   - Если `SmallReverseNet <= 0` и `AllowNegativeSmallReverseNet = false`, ожидание: `STATE_INVALID_SMALL_GEOMETRY`.

6. **Reverse Risk Validator**
   - Проверить `ProjectedReserveCoverage`.
   - Если значение ниже `MinProjectedReserveCoverage`, ожидание: `STATE_REVERSE_WARNING` в логах.

7. **MaxReverseCycles**
   - `reverseCycleCount = 4`, `MaxReverseCycles = 3`.
   - Ожидание: `STATE_REVERSE_LIMIT`, новый Big/Small не открывать при `StopOnReverseLimit = true`.

8. **FinalClose priority**
   - Если `FinalCloseAllowed = true`, ожидание: NewFar закрывается полностью, `STATE_CLOSED_PROFIT`, новый Big/Small не открывается.

---

## Cycle Math Internal Report Tests

1. Проверить, что журнал содержит строки `CYCLE_MATH |` для сценариев `BIG_HARVEST`, `SMALL_AT_FAR` и `STOP_MAX_LEVELS`.
2. Проверить, что при `EnableCycleMathCsv=true` создаётся файл `MQL5/Files/MinusLock_CycleMath.csv`.
3. Проверить обязательные CSV-колонки: `Time`, `Symbol`, `Level`, `Scenario`, `FarLotBefore`, `BigLot`, `SmallLot`, `NetProfit`, `CloseFarBudget`, `ReserveAdd`, `TotalReserve`, `FarRemainLoss`, `FinalCloseAllowed`, `State`, `Balance`, `Equity`, `Margin`, `FreeMargin`.
4. Проверить расширенные поля: `ProfitBig`, `LossSmall`, `SmallPL`, `OldFarPL`, `ClosedBigPL`, `SmallReverseNet`, `CloseFarLotRaw`, `CloseFarLotRounded`, `FarRemainLot`, `ReverseStrength`, `ProjectedReserveCoverage`, `ActionAfterValidation`, `StopReason`, `NetProfitTheoretical`, `NetProfitRealized`, `CostsRealized`, `TotalReserveBefore`, `TotalReserveAfter`, `ReserveUsedForFinalClose`.
5. Strategy Tester parameter comparison:
   - A: `CloseFarShare=0.90`, `ReserveShare=0.10`.
   - B: `CloseFarShare=0.70`, `ReserveShare=0.30`.
   - C: `CloseFarShare=0.50`, `ReserveShare=0.50`.
6. Для каждого варианта записать: `CLOSED_PROFIT` или `STOP_MAX_LEVELS`, Net Profit, Max Drawdown Equity, уровень `FinalCloseAllowed`, `TotalReserve` и `FarRemainLoss` перед финальным закрытием.
7. PASS: `STATE_CLOSED_PROFIT`, `FinalCloseAllowed=YES`, нет `STOP_MAX_LEVELS`, нет end-of-test по позициям советника, `OnTester > 0`.
8. FAIL: `STATE_UNCLOSED_CYCLE`, `STOP_MAX_LEVELS`, `OnTester=-1`, end-of-test, `FinalCloseAllowed` ни разу не стал `YES`.

## Python Candidate 50/50 MT5 Confirmation

Run the MT5 confirmation plan in `ai_tests/reports/mt5_confirmation_plan.md`.

Required comparisons:

1. Current 90/10 baseline: expected `STOP_MAX_LEVELS` or FAIL on the known bad sequence.
2. Python candidate 50/50: expected by Python model to reach `STATE_CLOSED_PROFIT`; must be confirmed in MT5 with real costs.
3. Neighbor 60/40: compare against 50/50 by `OnTester`, final state, `TotalReserve`, `FarRemainLoss`, and drawdown.

Do not mark the strategy as confirmed until MT5 Strategy Tester verifies `STATE_CLOSED_PROFIT`, no open positions at the end, and `OnTester > 0`.

## Far Distance Mode Tests

Before accepting any parameter variant, verify that Level 1 includes the initial 100 points:

```text
InitialTriggerPoints = 100
BigMoveStartPoints = 100
BigMoveStepPoints = 50
MaxHarvestLevels = 7
L1 = 100
L2 = 150
L3 = 200
L4 = 250
L5 = 300
L6 = 350
L7 = 400
EffectiveFarDistancePoints = 200
```

Run these modes for 90/10, 60/40 and 50/50:

```text
FIXED_200
INITIAL_PLUS_CURRENT
INITIAL_PLUS_CUMULATIVE
REAL_PRICE_DISTANCE
```

Required CYCLE_MATH fields in Experts journal and `MinusLock_CycleMath.csv`:

```text
InitialFarDistancePoints
CurrentBigMovePoints
CumulativeBigMovePoints
EffectiveFarDistancePoints
FarDistanceMode
FarOpenPrice
CurrentClosePrice
```

After `Small-at-Far`, confirm that the new Far starts from current price and does not inherit the old initial 100 points.


## Real Recovery P/L Validation Tests

1. Run the known 70/30 case: `CloseFarShare=0.70`, `ReserveShare=0.30`, `FarDistanceMode=REAL_PRICE_DISTANCE`, `AllowRealTrading=true`.
2. If the MT5 report balance is negative, expected `OnTester=-1` even when theoretical `CycleFinalPL` is positive.
3. Confirm `REAL_CYCLE_MATH |` appears in Experts journal.
4. Confirm `MinusLock_CycleMath.csv` contains: `InitialIgnoredProfit`, `CycleStartBalance`, `CurrentBalance`, `RealRecoveryPL`, `RealClosedProfit`, `RealClosedLoss`, `RealCommission`, `RealSwap`, `RealCosts`, `TheoreticalCyclePL`, `LastSystemCloseComment`, `PassByRealPL`.
5. Confirm the first profitable initial lock leg is excluded from `RealRecoveryPL` because `CycleStartBalance` is recorded after that close.
6. PASS requires `STATE_CLOSED_PROFIT`, `RealRecoveryPL > 0`, no managed open positions, no `STOP_MAX_LEVELS`, and final system close comment `FINAL_CLOSE` or `CLOSED_PROFIT`.

## Small Scenario V2.4 Required Tests

1. Small-сценарий с успешным переворотом.
2. Проверка NewBig < OldFar.
3. Проверка BigRatio² × RemainBigOnSmall < 1.
4. Проверка добавления 5% в резерв.
5. Проверка закрытия NewFar, если резерва хватает.
6. Проверка открытия нового Big/Small, если резерва не хватает.
7. Проверка reverse-limit.
8. Проверка invalid geometry.
9. Проверка восстановления после перезапуска.
10. Проверка rollback initial lock.
11. Проверка отказа брокера при закрытии одной ноги.
12. Проверка запрета автоподмены параметров recommended preset.

Required local checks:

```bash
python3 Tests/small_reverse_compression_check.py
python3 Tests/small_reserve_add_check.py
python3 Tests/recommended_preset_guard_check.py
python3 Tests/restart_recovery_static_check.py
python3 Tests/retry_fsm_static_check.py
python3 Tests/reverse_limit_close_check.py
python3 Tests/invalid_geometry_emergency_check.py
```

## V2.4.1 RiskGate Architecture Fix Tests

1. Verify high spread blocks only new openings (`OpenInitialLock`, `OpenBigSmall`).
2. Verify `ProcessBigHarvest`, `ProcessSmallAtFarTouch`, `ProcessFinalClose`, reverse-limit close and invalid-geometry emergency close still execute when spread is above `MaxSpreadPoints`.
3. Force broker close failure and verify `STATE_CLOSE_BIG_PENDING`, `STATE_CLOSE_SMALL_PENDING`, `STATE_CLOSE_OLD_FAR_PENDING`, `STATE_CLOSE_BIG_PART_PENDING`, `STATE_CLOSE_NEW_FAR_PENDING`, and `STATE_REVERSE_LIMIT_CLOSE_PENDING` retry on following ticks.
4. Verify BigHarvest reserve is updated only from HistoryDeals-derived `RealBigHarvestNet` and not from projected theoretical P/L.
5. Restart the terminal/VPS with open managed positions and verify `RecoverState()` reconciles saved GlobalVariables with real positions or moves to `STATE_RECOVERY_PENDING` / `STATE_MANUAL_INTERVENTION_REQUIRED`.
6. Confirm spread-block logs are throttled by `RiskGateLogIntervalSeconds` and state changes are logged once.
7. Confirm default V2.4.1 parameters: `MaxSpreadPoints=60`, `CloseFarShare=0.40`, `ReserveShare=0.60`, `MaxReverseCycles=7`, `AllowRealTrading=true`, `UseInternalSimulation=false`, `UseMarketOrders=true`.

## V2.4.2 Pending FSM / Real Reserve Tests

1. Force `STATE_CLOSE_SMALL_PENDING` after BigHarvest Big close and confirm retry continues to `STATE_BIG_HARVEST_CALC_NET`, not back to the scenario root.
2. Force Small Scenario partial-close retry and confirm it continues to `STATE_SMALL_BUILD_NEW_FAR`.
3. Verify `STATE_OPEN_NEW_BIG_PENDING` and `STATE_OPEN_NEW_SMALL_PENDING` have handlers.
4. Verify BigHarvest reserve is calculated from matching closed Big/Small deal `DEAL_POSITION_ID` values.
5. Verify no BigHarvest reserve is added when matching HistoryDeals are absent.
6. Verify SmallScenario reserve uses `smallScenarioRealAfter - smallScenarioRealBefore`.
7. Restart during pending operation and verify saved pending state, ticket, lot, attempts, and next state restore.

## V2.4.3 Full Phase FSM Tests

1. Verify `ProcessBigHarvest()` contains only the transition to `STATE_BIG_HARVEST_CLOSE_BIG`.
2. Verify `STATE_BIG_HARVEST_CLOSE_BIG` calls `ProcessBigHarvestCloseBig()` and closes only Big.
3. Verify `ProcessSmallAtFarTouch()` / `ProcessSmallScenario()` contain no close/reserve business logic and only route to `STATE_SMALL_CLOSE_SMALL`.
4. Verify retry close success clears the relevant Big/Small/Far context fields.
5. Verify `STATE_OPEN_NEW_BIG_PENDING` and `STATE_OPEN_NEW_SMALL_PENDING` execute open retry functions.
6. Verify preset validation order is `ConfigureWorkingParameters()` -> `ValidateInputs()` -> `ValidateWorkingParameters()` -> `ValidateFSMIntegrity()`.

## V2.4.5 Critical FSM Safety Checks

1. Verify terminal states only `break` and never call open/retry-open functions.
2. Verify `STATE_OPEN_NEW_BIG_PENDING` and `STATE_OPEN_NEW_SMALL_PENDING` are separate cases.
3. Verify Small context is saved before active Small cleanup.
4. Verify `ProcessSmallBuildNewFar()` uses `savedSmallDirection` / `savedSmallTouchPrice`, not active `smallDirection`.
5. Verify Old Far is copied to `oldFar*` fields and active `Ctx.far*` is cleared after close.
6. Verify saved Small and old Far fields are stored/restored by `SaveState()` / `RecoverState()`.

## V2.4.6 MaxHarvestLevels Final Decision Tests
1. Run USDJPY M30, 2026-04-01 through 2026-06-17, Every Tick, Deposit 10000, hedging account, `MaxHarvestLevels=7`, `MaxSpreadPoints=60`, `CloseFarOnMaxLevels=true`.
2. Confirm that after L7 the EA does not open L8 and logs `[MAX_LEVELS_DECISION]`.
3. Confirm the residual Far is closed by `MAX_LEVELS_FINAL_CLOSE` when reserve covers loss, or by `STOP_MAX_LEVELS_CLOSE_FAR` when reserve is insufficient.
4. Confirm there is no residual managed Far closed only by the Strategy Tester `end of test` / `окончание теста` comment.
5. Confirm `STATE_STOP_MAX_LEVELS_CLOSE_PENDING` retries failed Far closes and RiskGate does not block this close path.

## V2.4.7 Retry Partial Far Tests
1. Simulate BigHarvest Far budget close where the first partial Far close fails and retry succeeds; expected result is residual Far context preserved with reduced `farLot`.
2. Verify `PendingActionType` drives retry cleanup and `StringFind(Ctx.pendingOperation, ...)` is not used to classify Big/Small/Far cleanup.
3. Verify `STATE_CLOSED_PROFIT` is blocked when managed positions remain open.
4. Verify real deal accounting uses `POSITION_IDENTIFIER` / `DEAL_POSITION_ID`, not position ticket as a surrogate.
5. Verify reserve flags prevent BigHarvest and Small reserve additions from being applied twice after restart/retry.

## V2.4.8 Reconciliation Tests
1. Start EA after a saved-state restore and confirm `RunReconciliation()` is executed.
2. Confirm journal contains `RECONCILIATION PASS` for a clean context.
3. Manually change or remove a managed position and confirm `RECONCILIATION FAIL` and `STATE_RECOVERY_MISMATCH`.
4. Verify Far/Big/Small volume mismatches and identifier mismatches are detected.
5. Verify reserve mismatch uses `ReserveMismatchTolerance` and blocks continuation when exceeded.

## V2.4.9 Reconciliation Regression Tests
1. Reproduce `ctxFarLot=0.68` / `actualFarVolume=0.69` with `LotStep=0.01`; expected result is `RECON WARNING` + `RECON_AUTO_SYNC_FAR_VOLUME`, not `STATE_RECOVERY_MISMATCH`.
2. Confirm `RECON_TOLERANCE_USED=0.01` when `ReserveMismatchTolerance=0.01`.
3. Confirm normalized volume comparison is used for Far/Big/Small and direct raw-volume fatal checks are absent.
4. Confirm reserve rebuild classifies positive closed recovery deals even when broker close comments are blank.

## V2.4.9 Reserve Reconciliation Tests

Run all Python checks in `Tests/`, including:

- `reserve_rebuild_skips_initial_profit_check.py`
- `reserve_mismatch_not_fatal_check.py`
- `reserve_ledger_credit_debit_check.py`
- `reserve_rebuild_from_ledger_check.py`
- `reconciliation_stops_after_fatal_error_check.py`

MT5 validation must confirm that the first Initial Lock profit does not produce `RECONCILIATION FAIL RESERVE_MISMATCH`, the EA continues beyond L1, and reserve mismatches without structural position errors remain warnings only.
