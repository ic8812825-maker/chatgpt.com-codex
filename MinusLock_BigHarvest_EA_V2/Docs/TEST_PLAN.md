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
StartLot = 0.10
InitialTriggerPoints = 100
AllowRealTrading = false
```

Ожидание:

1. Открывается `BUY 1.00` с комментарием `MinusLock_INITIAL_BUY`.
2. Открывается `SELL 1.00` с комментарием `MinusLock_INITIAL_SELL`.
3. При движении вверх на 100 пунктов закрывается только BUY, SELL становится Far.
4. При движении вниз на 100 пунктов закрывается только SELL, BUY становится Far.
5. В логах зафиксировано, что первый плюс игнорируется.

## 4. Тест StartLot = 0.10 по мануалу

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
6. PASS requires `STATE_CLOSED_PROFIT`, `RealRecoveryPL > 0`, no managed open positions, no `STOP_MAX_LEVELS`, and final system close comment `FINAL_CLOSE_PROFIT` or `CLOSED_PROFIT`.

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
1. Reproduce the Small Reverse 0.68/0.69 case; expected result is that `ProcessSmallBuildNewFar()` uses actual MT5 volume, so regular `FAR_VOLUME_MISMATCH` does not appear during normal progression.
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

## V2.4.10 Actual Volume Regression Tests

Run all Python checks plus the new V2.4.10 checks:

- `actual_volume_after_partial_close_check.py`
- `synthetic_volume_forbidden_check.py`
- `recovery_uses_actual_volume_check.py`
- `volume_integrity_guard_check.py`
- `reconciliation_volume_stability_check.py`

MT5 Strategy Tester must confirm that Small Reverse no longer produces the synthetic 0.68/0.69 Far volume mismatch and that regular `FAR_VOLUME_MISMATCH` messages do not appear during normal progression.

## V2.4.11 Actual Volume Test Plan

Run all Python checks, including:

- `bigharvest_far_partial_uses_actual_volume_check.py`
- `partial_close_no_theoretical_lot_subtraction_check.py`
- `full_close_incomplete_guard_check.py`
- `refresh_leg_volume_from_terminal_check.py`

MT5 Strategy Tester must verify that BigHarvest Far partial close and retry no longer generate false `FAR_VOLUME_MISMATCH`, and that full close leaves no residual terminal volume before context is cleared.

## V2.4.12 Full Close Integrity Tests

Run all Python checks, including:

- `full_close_volume_tolerance_check.py`
- `full_close_not_min_lot_check.py`
- `verify_full_close_check.py`
- `closed_profit_requires_full_close_check.py`
- `context_cleared_with_live_position_check.py`

MT5 Strategy Tester must confirm that full closes never clear Far context while `POSITION_VOLUME > VolumeMismatchToleranceLots`, and that no false `STATE_CLOSED_PROFIT` occurs with residual managed positions.

## V2.4.13 Orphan Position Protection Tests

Static tests added:

- `orphan_position_detection_check.py` verifies `ValidateNoOrphanManagedPositions()` and required orphan diagnostics.
- `orphan_position_recovery_mismatch_check.py` verifies orphan detection forces `STATE_RECOVERY_MISMATCH`.
- `orphan_position_identifier_check.py` verifies `POSITION_IDENTIFIER` is used for ownership matching.
- `orphan_position_after_close_check.py` verifies close paths invoke orphan checks without waiting for the periodic interval.
- `orphan_position_after_recover_check.py` verifies startup/recovery paths call orphan validation after `RecoverState()`.

MT5 acceptance test remains USDJPY M30 2026.04.01–2026.06.17 Every Tick with the baseline BigHarvest parameters. Experts log must contain no `ORPHAN_MANAGED_POSITION` during normal operation.

## V2.4.15 Initial Lock Recovery Tests

Static tests added:

- `initial_lock_context_fields_check.py` verifies Initial Lock fields in `RecoveryContext`.
- `initial_lock_save_restore_check.py` verifies Initial Lock persistence and recovery registration tokens.
- `initial_lock_orphan_protection_check.py` verifies Initial legs are known to orphan protection by ticket and identifier.
- `initial_lock_reconciliation_check.py` verifies `ValidateInitialLockIntegrity()` diagnostics.
- `initial_lock_state_consistency_check.py` verifies state-aware position consistency validation.

Manual MT5 scenarios to repeat: restart while both initial legs are open, restart after one initial leg is closed and the remaining leg is Far, and restart during Initial-plus conversion. Expected result: no false `ORPHAN_MANAGED_POSITION`, no false `STATE_RECOVERY_MISMATCH`, and no duplicate Far.

## V2.4.17 Known Context Tests

Static tests added:

- `known_context_check.py` verifies centralized context helpers and `HasKnownContext()`.
- `known_context_diagnostics_check.py` verifies `KNOWN_CONTEXT_PRESENT` diagnostics.
- `reconciliation_context_summary_check.py` verifies `RECONCILIATION_CONTEXT_SUMMARY` and `RECOVERY_CONTEXT_RESTORED` startup diagnostics.
- `context_cleared_guard_check.py` verifies `CONTEXT_CLEARED_WITH_LIVE_POSITION` uses only `!HasKnownContext() && CountManagedOpenPositions() > 0`.

MT5 acceptance remains USDJPY M30 2026.04.01–2026.06.17 Every Tick with MaxSpreadPoints=60 and real trading mode enabled in tester.

## V2.4.17 Full Phase-State Integrity Validation
Additional static checks:
- `state_integrity_engine_check.py` verifies the new module, include wiring, `ValidateCurrentStateIntegrity()`, and `STATE_INTEGRITY_ERROR`.
- `phase_state_matrix_check.py` verifies every `EAState` has a matrix entry.
- `pending_state_integrity_check.py` verifies pending states require pending context.
- `retry_state_integrity_check.py` verifies retry states require retry context.
- `state_shape_validation_check.py` verifies required/forbidden position diagnostics and reconciliation/startup integration.

Manual MT5 acceptance remains USDJPY M30, 2026-04-01 through 2026-06-17, Every Tick, MaxSpreadPoints=60, real market-order mode. The Experts log must not show unexpected `STATE_INTEGRITY_FAIL` entries during normal execution.

## V2.4.18 Pending Contract Tests
Static tests added:
- `pending_contract_engine_check.py` verifies the new contract module, helper functions and contract diagnostics.
- `pending_open_big_contract_check.py` verifies `STATE_OPEN_NEW_BIG_PENDING` uses `PENDING_OPEN_BIG` and is prepared before state transition.
- `pending_open_small_contract_check.py` verifies `STATE_OPEN_NEW_SMALL_PENDING` uses `PENDING_OPEN_SMALL`.
- `pending_close_big_contract_check.py` and `pending_close_small_contract_check.py` verify close-pending ticket/action ownership.
- `state_action_matrix_check.py` verifies the State ↔ PendingAction matrix.
- `open_new_small_pending_context_check.py` verifies the Small Reverse/New Big/New Small handoff prepares `PENDING_OPEN_SMALL` before entering `STATE_OPEN_NEW_SMALL_PENDING`.
- `bigharvest_phase_forbids_closed_legs_check.py` verifies BigHarvest phases forbid closed Big/Small legs where required.

MT5 acceptance remains USDJPY M30, 2026-04-01 through 2026-06-17, Every Tick, MaxSpreadPoints=60, real market-order mode. Experts must show no false `STATE_INTEGRITY_ERROR` after New Big opens and before New Small opens.

## V2.4.19 Position Resolution Tests
Static tests added:
- `position_resolution_engine_check.py` verifies the resolver module, result structure, logs and include wiring.
- `retry_open_big_resolution_check.py` verifies New Big cannot fall back to virtual context.
- `retry_open_small_resolution_check.py` verifies New Small must be resolved before the cycle completes.
- `open_bigsmall_resolution_check.py` verifies initial Big/Small pair opens use resolution for both legs.
- `position_resolution_fail_check.py` verifies failed resolution routes to `STATE_POSITION_RESOLUTION_ERROR`.
- `state_requires_resolved_position_check.py` and `open_new_small_requires_big_context_check.py` verify pending-open state integrity requires real ticket/identifier context.

MT5 acceptance and optimization remain required on MT5: USDJPY M30, 2026-04-01 through 2026-06-17, Every Tick, MaxSpreadPoints=60, plus the requested parameter-selection campaign. This Linux container cannot run MetaEditor or Strategy Tester.

## V2.4.20 Position Resolution + Small Scenario Promote Fix
Static tests added:
- `position_resolution_lookback_config_check.py` verifies `PositionResolutionLookbackSeconds=10` is declared and used.
- `position_resolution_reference_only_check.py` verifies `PositionResolutionResult` and `PositionSnapshot` are not passed by value.
- `position_resolution_excludes_existing_context_check.py` verifies fallback resolution excludes known context and rejects ambiguous matches.
- `position_resolution_time_window_check.py` verifies operation-start/open-time window logic.
- `promote_remaining_big_to_far_check.py` verifies remaining Big fields become the new `Ctx.far*` and Big/Small context is cleared.
- `small_scenario_promote_no_integrity_error_check.py` verifies `ProcessSmallBuildNewFar()` promotes instead of entering `STATE_INTEGRITY_ERROR`.
- `recover_promoted_big_as_far_check.py` verifies recovery/reconciliation can rebuild promoted Big as Far.

Manual MT5 acceptance remains required: USDJPY M30, 2026-04-01 through 2026-06-17, Every Tick, Deposit 10000, Hedging. Required checks: no false `STATE_INTEGRITY_ERROR` after Small scenario, no stuck Far at test end, new Far near the terminal remainder after partial Big close, no `STATE_RECOVERY_MISMATCH`, and no `STATE_POSITION_RESOLUTION_ERROR` unless the opened position truly cannot be resolved.

## V2.4.21 Real Recovery Profit + Final Close Pass Criteria

- The pass criterion is now `FinalBalance > CycleStartBalance`; account-level profit versus the initial deposit is diagnostic only.
- `InitialIgnoredProfit` from the first Initial Lock plus close is excluded from `realRecoveryPL`, reserve accounting, `OnTester()`, and `STATE_CLOSED_PROFIT` eligibility.
- `CalcRealRecoveryPL()` uses `CurrentBalance - CycleStartBalance` as the source of truth; closed-deal profit/loss fields remain diagnostics.
- `OnTester()` returns `Ctx.realRecoveryPL` only when `IsRealRecoveryPass()` confirms `STATE_CLOSED_PROFIT`, no managed open positions, a profitable system close comment, and positive recovery P/L. Otherwise it returns `-1.0`.
- `ProcessFinalClose()` forecasts `ProjectedRecoveryPLAfterFinalClose`; negative or zero recovery projection is routed as `FINAL_CLOSE_STOP` and cannot enter `STATE_CLOSED_PROFIT`.
- `STATE_CLOSED_RECOVERY_LOSS` records terminal cycles where all positions are closed but `realRecoveryPL <= 0`.
- CSV diagnostics now include `InitialDeposit`, `AccountPL`, `RecoveryPL`, `PassByAccountPL`, `PassByRecoveryPL`, `LastCloseWasSystemClose`, and `FinalCloseType` so a positive account P/L cannot hide a failed recovery cycle.

## V2.4.22 Offline Parameter Optimizer Ranking Fix

- Added `Tools/offline_optimizer.py`, `offline_scenarios.py`, `score_parameters.py`, and `generate_set_files.py` for deterministic parameter screening without MT5.
- The optimizer preserves the EA acceptance rule: `RecoveryPL = FinalBalance - CycleStartBalance`; AccountPL and InitialIgnoredProfit are diagnostics only.
- Synthetic scenarios cover Big wins, Small wins, alternating moves, false reversals, adverse trend, MaxLevels stress, and worst-case ordering.
- V2.4.22 ranking is now two-stage: rows receive `Verdict` first, then only `ACCEPT` rows can enter TOP ACCEPT, category selection, or production `.set` generation.
- Rejected rows receive a hard ranking penalty, stay in TOP REJECTED diagnostics, and are marked `IsSelectableForSetFile=NO`.
- The offline search now evaluates 100,000 broad samples plus a 10,000-run local mini-search around the best accepted/current-leader zone.
- `Optimization_Report.csv` records `StabilityScore`, `RobustnessScore`, `FinalRank`, `CoverageRatio`, and `IsSelectableForSetFile`; `Best_Parameters.md` explains selected Safe / Balanced / LowLot candidates and the AGGRESSIVE_NOT_FOUND marker when no accepted aggressive row exists.
- Generated `.set` files under `Sets/` are created only from `Verdict=ACCEPT` rows; missing categories receive explicit NOT_FOUND marker files for manual MT5 Strategy Tester planning.

## Adaptive ATR Geometry Test Plan

### Manual compatibility

Configuration: `GeometryMode=GEOMETRY_MANUAL`.

Expected:
- EA uses input `InitialTriggerPoints`, `BigMoveStartPoints`, `BigMoveStepPoints`, and `FarDistancePoints` directly.
- ATR does not influence trading geometry.
- Existing manual-mode tests remain reproducible.

### ATR SAFE

Given `ATRPoints=190`, `InitialRoundStep=10`, `BigStartRoundStep=10`, `BigStepRoundStep=5`, and `FarDistanceRoundStep=50`.

Expected Work geometry: `190 / 190 / 75 / 250`.

### ATR BALANCED

Given `ATRPoints=190`, `InitialRoundStep=10`, `BigStartRoundStep=10`, `BigStepRoundStep=5`, and `FarDistanceRoundStep=50`.

Expected Work geometry: `190 / 220 / 75 / 300`.

### ATR PROFIT

Given `ATRPoints=190`, `InitialRoundStep=10`, `BigStartRoundStep=10`, `BigStepRoundStep=5`, and `FarDistanceRoundStep=50`.

Expected Work geometry: `200 / 230 / 85 / 300`.

### ATR fallback

Simulate unavailable ATR data.

Expected:
- No EA stop solely because of ATR.
- Manual geometry fallback is used.
- Logs include `ADAPTIVE_GEOMETRY_ERROR` and `WARNING: Adaptive geometry failed. Manual geometry fallback used.`

### Freeze per cycle

Change ATR while a recovery cycle has open Initial/Far/Big/Small, pending, or retry context.

Expected:
- `WorkInitialTriggerPoints`, `WorkBigMoveStartPoints`, `WorkBigMoveStepPoints`, and `WorkFarDistancePoints` do not change during the active cycle.

### ClearCycleGeometry

After a cycle is fully completed and there are no managed positions, leg tickets, pending actions, or retry operation.

Expected:
- `ClearCycleGeometry()` clears `cycleATRPoints`, all Work geometry fields, `geometryModeUsed`, and `geometryCalculatedTime` before the next independent cycle.
- If active context still exists, log `CLEAR_CYCLE_GEOMETRY_SKIPPED reason=ACTIVE_CONTEXT_OR_POSITIONS`.
