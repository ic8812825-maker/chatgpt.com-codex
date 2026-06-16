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
BigMoveLevel1 = 100
BigMoveLevel2 = 150
BigMoveLevel3 = 200
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
BigMoveLevel1 = 100
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

## Dynamic Parameters
Verify `WorkBigRatio`, `WorkSmallRatio`, `WorkCloseBigOnSmall`, `WorkRemainBigOnSmall`, `WorkCloseFarShare`, `WorkReserveShare`, `WorkMaxHarvestLevels`, `WorkMaxReverseCycles`, and `WorkFarDistanceMode` in normal and `PRESET_ACTIVE` modes.

## Position Comments / Comment Library
Run static checks for `CommentUtils.mqh`, `ValidateComment`, and `ERROR_EMPTY_COMMENT`; confirm every open path uses generated comments.

## Visual Status Panel
In visual tester confirm the upper-right panel updates state, tickets, lots, reserve, PL, spread, margin, and risk-gate status without duplicate labels.

## Full Trade Flow Validation
Exercise price-up and price-down initial cycles, Big harvest, Small-at-Far rebuild, STOP_MAX_LEVELS, invalid reverse geometry, and final-close paths; inspect CSV columns `OpenComment`, `CloseComment`, `PositionRole`, `CommentValid`, `PanelState`, `LastOpenComment`, and `LastCloseReason`.
