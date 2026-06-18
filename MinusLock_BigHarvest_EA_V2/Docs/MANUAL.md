# MinusLock BigHarvest EA — технический мануал

Документ описывает MQL5-советник, реализованный строго на базе `manual/big_harvest_system_manual_ru.md`.

## 1. Назначение

Советник разруливает оставшуюся минусовую позицию `Far` через цикл `Big-Harvest`:

1. Открывается начальный замок `BUY StartLot` + `SELL StartLot`.
2. Первая плюсовая позиция закрывается при достижении `InitialTriggerPoints`.
3. Прибыль первого плюса не участвует в разруливании: `InitialProfitIgnored = true`, `Reserve = 0`.
4. Оставшаяся минусовая позиция становится `Far`.
5. От `Far` строятся `Big` и `Small` по геометрии мануала.
6. В Big-сценарии чистая прибыль делится: 90% на денежное закрытие `Far`, 10% в `Reserve`.
7. После каждого уровня проверяется `FinalCloseAllowed`.

## 2. Параметры

Ключевые `input`-параметры находятся в `Include/Config.mqh`:

```mql5
StartLot = 1.00
BigRatio = 1.30
SmallRatio = 0.37
CloseBigOnSmall = 0.30
RemainBigOnSmall = 0.70
CloseFarShare = 0.90
ReserveShare = 0.10
BigMoveStartPoints = 100
BigMoveStepPoints = 50
MaxHarvestLevels = 7
FarDistancePoints = 200
LotStep = 0.01
```

## 3. Начальный замок

Советник открывает две позиции с одним `MagicNumber`:

```text
MinusLock_INITIAL_BUY
MinusLock_INITIAL_SELL
```

Плюсовая позиция определяется через прибыль в пунктах:

```text
ProfitPoints = ABS(CurrentPrice - OpenPrice) / Point
```

Для BUY используется выход по Bid, для SELL — выход по Ask.

## 4. Big/Small геометрия

Если `Far = SELL`, то:

```text
Big = BUY
Small = SELL
```

Если `Far = BUY`, то:

```text
Big = SELL
Small = BUY
```

Лоты:

```text
BigLot = NormalizeLotNearest(FarLot × 1.30)
SmallLot = NormalizeLotNearest(BigLot × 0.37)
```

## 5. Big-сценарий

При достижении `BigMovePoints` в сторону `Big` советник:

1. Закрывает `Big` полностью.
2. Закрывает `Small` полностью.
3. Считает `NetProfit = ProfitBig - LossSmall - Costs`.
4. Считает `CloseFarBudget = NetProfit × 0.90`.
5. Считает `ReserveAdd = NetProfit × 0.10`.
6. Закрывает `Far` только через денежный бюджет:

```text
CloseFarLotRaw = CloseFarBudget / (FarDistancePoints × PointValuePerLot)
CloseFarLotRounded = FloorToLotStep(CloseFarLotRaw)
CloseFarLotFinal = MIN(FarLot, CloseFarLotRounded)
```

Важно: `CloseFarShare` — это доля денег от чистой прибыли, а не доля лота `Far`.

## 6. Small-сценарий и DUAL_TAIL

При движении цены против `Big` в сторону `Small` советник:

1. Закрывает `Small` полностью.
2. Закрывает 30% `Big`.
3. Оставшиеся 70% `Big` рассматривает как новый `Far`.
4. Проверяет `DUAL_TAIL`.

Если старый `Far` всё ещё открыт и одновременно появился новый хвост из оставшегося `Big`, советник переводится в `STATE_DUAL_TAIL` и не строит новый уровень.

## 7. FinalCloseAllowed

После каждого Big-harvest:

```text
FarRemainLoss = FarRemainLot × FarDistancePoints × PointValuePerLot
FinalCloseAllowed = TotalReserve >= FarRemainLoss
```

Если условие выполнено, остаток `Far` закрывается полностью, цикл завершается:

```text
Status = CLOSED_PROFIT
```

## 8. Безопасность

По умолчанию:

```mql5
AllowRealTrading = false
```

При `false` торговые операции выполняются во внутреннем виртуальном SIMULATION-хранилище советника: позиции получают виртуальные тикеты, читаются теми же утилитами поиска и могут частично/полностью закрываться без отправки ордеров брокеру. Для реальной торговли требуется вручную включить `AllowRealTrading = true`.

Дополнительно советник блокирует работу при превышении:

- `MaxSpreadPoints`
- `MaxMarginPercent`

## 9. Обязательные логи

Каждый Big-harvest уровень пишет поля:

```text
Level
FarLot
BigLot
SmallLot
BigMovePoints
ProfitBig
LossSmall
NetProfit
CloseFarBudget
CloseFarLotRaw
CloseFarLotRounded
FarRemainLot
ReserveAdd
TotalReserve
FinalCloseAllowed
CycleFinalPL
State
```

## Small-at-Far Scenario

Small-сценарий больше не исполняется сразу при первом движении в сторону Small. Если Small достиг защитного движения, советник переводит цикл в `STATE_WAIT_SMALL_TO_FAR` и ждёт, пока текущая цена дойдёт до цены открытия старого `Far` с учётом `SmallFarTouchOffsetPoints`. Для `Small=BUY` условие касания: `CurrentPrice >= OldFarOpenPrice + offset`; для `Small=SELL`: `CurrentPrice <= OldFarOpenPrice - offset`.

После касания старого Far выполняется `ProcessSmallAtFarTouch`: Small закрывается на 100%, старый Far закрывается на 100%, Big закрывается только на `CloseBigOnSmall`, а остаток Big становится новым Far. Затем обязательно сначала проверяется `FinalCloseAllowed` для нового Far. Если резерва хватает, новый Far закрывается полностью и состояние становится `STATE_CLOSED_PROFIT`; если резерва не хватает, только тогда открывается новый Big/Small от нового Far. В нормальном Small-at-Far сценарии `DUAL_TAIL` не должен появляться, потому что старый Far ликвидируется до назначения нового Far.

---

## Reverse Geometry Protection

После `Small-at-Far Scenario` советник обязан проверить качество нового переворота до открытия новой пары Big/Small.

### Параметры защиты

```mql5
input int    MaxReverseCycles              = 3;
input double MinReverseStrength            = 0.10;
input double WarningReverseStrength        = 0.15;
input double StrongReverseStrength         = 0.25;
input double MinProjectedReserveCoverage   = 1.00;
input bool   StopOnInvalidReverseGeometry  = true;
input bool   StopOnReverseLimit            = true;
input bool   AllowNegativeSmallReverseNet  = false;
```

### Geometry Validator

Переворот разрешается только если новая геометрия улучшает систему:

```text
NewFarLot < OldFarLot
NewBigLot > NewFarLot
NewSmallLot < NewBigLot
ReverseStrength >= MinReverseStrength
```

`ReverseStrength` считается так:

```text
ReverseStrength = (NewBigLot - NewFarLot) / NewFarLot
```

Статусы качества:

```text
STRONG  = ReverseStrength >= StrongReverseStrength
OK      = ReverseStrength >= WarningReverseStrength
WARNING = ReverseStrength >= MinReverseStrength
INVALID = ReverseStrength < MinReverseStrength
```

Если `NewFarLot >= OldFarLot`, новый хвост не сжался. Это запрещённая геометрия, потому что переворот ухудшает систему и может привести к деградации хвоста.

### Small Geometry Validator

Small-at-Far дополнительно проверяет денежный результат переворота:

```text
SmallReverseNet = SmallPL + OldFarPL + ClosedBigPL
```

По умолчанию `SmallReverseNet` должен быть больше нуля. Если `AllowNegativeSmallReverseNet = true`, отрицательное значение допускается только как `STATE_REVERSE_WARNING` и обязательно логируется.

### Reverse Risk Validator

Проекция покрытия резерва:

```text
ProjectedReserveCoverage = (TotalReserve + ExpectedNextReserve) / ExpectedNextFarLoss
```

Если покрытие ниже `MinProjectedReserveCoverage`, советник пишет `STATE_REVERSE_WARNING`. Это предупреждение не открывает новую пару до завершения всех остальных проверок.

### MaxReverseCycles

После каждого успешного Small-at-Far увеличивается:

```text
reverseCycleCount += 1
```

Если `reverseCycleCount > MaxReverseCycles` и `StopOnReverseLimit = true`, советник переходит в `STATE_REVERSE_LIMIT` и новый Big/Small не открывает.

### Обязательный порядок после Small-at-Far

```text
1. Рассчитать NewFarLot.
2. Рассчитать NewBigLot.
3. Рассчитать NewSmallLot.
4. ValidateReverseGeometry.
5. ValidateSmallGeometry.
6. ValidateReverseRisk.
7. Проверить MaxReverseCycles.
8. Проверить FinalCloseAllowed.
9. Если FinalCloseAllowed = YES — закрыть NewFar и STATE_CLOSED_PROFIT.
10. Если проверки OK и FinalCloseAllowed = NO — открыть новый Big/Small.
```

Запрещено открывать новый Big/Small до проверки геометрии, risk projection, reverse-limit и `FinalCloseAllowed`.

---

## Cycle Math Internal Report

Советник пишет внутренний математический отчёт цикла в журнал Strategy Tester строкой `CYCLE_MATH | ...` и, если `EnableCycleMathCsv = true`, в файл `MQL5/Files/MinusLock_CycleMath.csv`.

### Как читать `CYCLE_MATH`

Минимальные поля:

```text
Level
Scenario
FarLotBefore
BigLot
SmallLot
NetProfit
CloseFarBudget
ReserveAdd
TotalReserve
FarRemainLoss
FinalCloseAllowed
State
```

`Scenario=BIG_HARVEST` означает денежное закрытие Far из бюджета `CloseFarBudget`. `Scenario=SMALL_AT_FAR` означает переворот: Small и старый Far закрыты, часть Big закрыта, остаток Big стал NewFar; `CloseFarBudget=0`, `ReserveAdd=0`. `Scenario=STOP_MAX_LEVELS` означает провал цикла: уровни закончились до `FinalCloseAllowed=YES`.

### Как читать `MinusLock_CycleMath.csv`

CSV содержит время, символ, уровень, сценарий, лоты, прибыль/убыток, резерв, состояние счёта и расширенные поля:

```text
ProfitBig, LossSmall, SmallPL, OldFarPL, ClosedBigPL,
SmallReverseNet, CloseFarLotRaw, CloseFarLotRounded,
FarRemainLot, ReverseStrength, ProjectedReserveCoverage,
ActionAfterValidation, StopReason,
NetProfitTheoretical, NetProfitRealized, CostsRealized,
TotalReserveBefore, TotalReserveAfter, ReserveUsedForFinalClose
```

`NetProfitTheoretical` — расчёт по формуле советника. `NetProfitRealized` выделен отдельным полем для сравнения с фактическим результатом тестера; если история сделок не подтянута в коде, он равен теоретическому значению, а `CostsRealized=0`.

### PASS / FAIL

```text
CLOSED_PROFIT + FinalCloseAllowed=YES + OnTester > 0 = PASS
STOP_MAX_LEVELS или STATE_UNCLOSED_CYCLE или OnTester=-1 = FAIL
```

`STOP_MAX_LEVELS` означает, что система не смогла накопить достаточный `TotalReserve` для покрытия `FarRemainLoss`. Для сравнения агрессивности настроек нужно прогнать варианты `CloseFarShare/ReserveShare`: `0.90/0.10`, `0.70/0.30`, `0.50/0.50`, затем сравнить `TotalReserve`, `FarRemainLoss`, уровень `FinalCloseAllowed` и итоговый Net Profit.

## Python Candidate 50/50

The Python simulation harness found a candidate for MT5 confirmation:

```text
BigRatio = 1.30
SmallRatio = 0.36
CloseBigOnSmall = 0.35
RemainBigOnSmall = 0.65
CloseFarShare = 0.50
ReserveShare = 0.50
MaxHarvestLevels = 5
MaxReverseCycles = 10
```

This is not a final profitable-strategy claim. It is a Python-model candidate that must be confirmed in MT5 Strategy Tester.

When `UseRecommended5050Preset = true`, the EA uses internal working parameters:

```text
WorkSmallRatio
WorkCloseBigOnSmall
WorkRemainBigOnSmall
WorkCloseFarShare
WorkReserveShare
WorkMaxHarvestLevels
WorkMaxReverseCycles
```

All recovery calculations must use these `Work...` values so that the 50/50 preset and normal input mode share the same formulas.

Small-at-Far geometry for Far=1.00 with the 50/50 candidate:

```text
Big = 1.30
Small = 1.30 × 0.36 = 0.47
CloseBig = 1.30 × 0.35 = 0.46
NewFar = 1.30 - 0.46 = 0.84
NewBig = 0.84 × 1.30 = 1.09
NewSmall = 1.09 × 0.36 = 0.39
ReverseStrength = (1.09 - 0.84) / 0.84 ≈ 0.2976 = STRONG
```

## Far Distance Modes with Initial Trigger

The recovery does not start from zero distance. After the initial lock moves by `InitialTriggerPoints`, the losing initial position is already an active Far with an initial distance:

```text
InitialFarDistancePoints = InitialTriggerPoints
```

The EA now separates:

```text
InitialTriggerPoints
BigMovePoints
FarDistancePoints
CumulativeBigMovePoints
EffectiveFarDistancePoints
FarDistanceMode
```

Available `FarDistanceMode` values:

```text
FIXED_200               -> legacy comparison mode, uses FarDistancePoints
INITIAL_PLUS_CURRENT    -> InitialFarDistancePoints + current BigMovePoints
INITIAL_PLUS_CUMULATIVE -> InitialFarDistancePoints + cumulative BigMovePoints
REAL_PRICE_DISTANCE     -> ABS(CurrentClosePrice - FarOpenPrice) / Point
```

Big Harvest levels are calculated automatically:

```text
L(level) = BigMoveStartPoints + (level - 1) * BigMoveStepPoints
```

При `BigMoveStartPoints=100`, `BigMoveStepPoints=50`, `MaxHarvestLevels=7`:

```text
L1=100, L2=150, L3=200, L4=250, L5=300, L6=350, L7=400
```

For Level 1 with `InitialTriggerPoints=100` and `BigMoveStartPoints=100`:

```text
EffectiveFarDistancePoints = 100 + 100 = 200
CloseFarLotRaw = CloseFarBudget / (EffectiveFarDistancePoints × PointValuePerLot)
FarRemainLoss = FarRemainLot × EffectiveFarDistancePoints × PointValuePerLot
```

After `Small-at-Far`, the old Far is closed and the new Far appears at the current price. Therefore the EA resets the new Far distance context:

```text
InitialFarDistancePoints = 0
CumulativeBigMovePoints = 0
FarOpenPrice = CurrentPrice
```

For MT5 confirmation, `REAL_PRICE_DISTANCE` is the preferred mode because it uses the actual price distance instead of a synthetic Python distance assumption.


## Real Recovery P/L Validation

`CycleFinalPL = TotalReserve - FarRemainLoss` remains a theoretical pre-check only. It is useful for deciding whether a final Far close is allowed, but it is not the final Strategy Tester profit.

The EA now tracks real recovery-cycle results after the initial plus is ignored:

```text
InitialIgnoredProfit
CycleStartBalance
CurrentBalance
RealRecoveryPL
RealCyclePL
RealClosedProfit
RealClosedLoss
RealCommission
RealSwap
RealCosts
TheoreticalCyclePL
LastSystemCloseComment
PassByRealPL
```

`CycleStartBalance` is fixed only after the first profitable initial lock leg is closed. Therefore the first plus remains excluded from `TotalReserve`, `RealRecoveryPL`, `RealCyclePL` and `FinalCloseAllowed`.

PASS is allowed only when all conditions are true:

```text
State = STATE_CLOSED_PROFIT
RealRecoveryPL > 0
CountManagedOpenPositions() = 0
LastSystemCloseComment = FINAL_CLOSE or CLOSED_PROFIT
No STOP_MAX_LEVELS
```

If the theoretical cycle is positive but real closed deals, commission, swap, spread or slippage make `RealRecoveryPL <= 0`, `OnTester()` returns `-1`. This prevents false positive results such as a positive internal `CycleFinalPL` while the MT5 report balance is negative.

Final system closes use explicit comments:

```text
FINAL_CLOSE
CLOSED_PROFIT
STOP_MAX_LEVELS
```

The journal and CSV include `REAL_CYCLE_MATH | ...` so MT5 reports can be audited against the internal recovery result.

## Small Scenario V2.4

Small Scenario V2.4 implements a Risk Compression Reverse. The EA waits for the Small leg to reach the old Far open price, then closes Small, closes old Far, partially closes Big, and promotes the remaining Big volume to the new Far.

## Risk Compression Reverse

The required compression rule is:

```text
NewFar = OldBig * RemainBigOnSmall
NewBig = NewFar * BigRatio
NewBig < OldFar
BigRatio^2 * RemainBigOnSmall < 1
```

Recommended parameters:

```text
BigRatio = 1.20
SmallRatio = 0.35
CloseBigOnSmall = 0.35
RemainBigOnSmall = 0.65
SmallReserveShare = 0.05
```

## New Far Calculation

The new Far is the remaining Big after the actual partial close. Its open price is the original Big open price, not the current price. The effective Far distance is based on real price distance from current close price to `bigOpenPrice`.

## New Big < Old Far Rule

The EA validates `BigRatio^2 * RemainBigOnSmall < 1` at startup. If this is not true, the EA refuses to start because a Small reverse would not compress risk.

## Small Reserve Logic

After Small-at-Far closes Small, old Far, and the selected Big part, the EA calculates `SmallScenarioRealNet`. If the result is positive, it adds:

```text
SmallReserveAdd = SmallScenarioRealNet * SmallReserveShare
```

If the result is zero or negative, no Small reserve is added.

## Real Reserve From HistoryDeals

For live trading the recovery accounting is based on closed deal history using `HistorySelect`, `HistoryDealGetDouble(DEAL_PROFIT)`, `HistoryDealGetDouble(DEAL_COMMISSION)`, `HistoryDealGetDouble(DEAL_SWAP)`, `HistoryDealGetString(DEAL_COMMENT)`, `HistoryDealGetInteger(DEAL_MAGIC)`, and symbol filtering. Theoretical values remain diagnostic only.

## Reverse Limit Handling

When `StopOnReverseLimit=true`, a reverse-limit event closes the new Far with comment `STOP_REVERSE_LIMIT_CLOSE_NEW_FAR`. Success moves to `STATE_REVERSE_LIMIT_CLOSED`; failure moves to `STATE_REVERSE_LIMIT_CLOSE_PENDING`.

## Invalid Geometry Handling

When reverse geometry is invalid and `CloseAllOnInvalidGeometry=true`, the EA attempts to close all managed positions and moves to `STATE_INVALID_GEOMETRY_CLOSED`. If disabled, it moves to `STATE_MANUAL_INTERVENTION_REQUIRED` and does not open new positions.

## Restart Recovery

The EA persists key context with GlobalVariables via `SaveState()` and restores it with `RecoverState()` on startup. If saved state and live positions conflict, it enters `STATE_RECOVERY_PENDING`.

## Retry FSM

The EA defines retry/pending states for multi-step operations: `STATE_CLOSE_BIG_PENDING`, `STATE_CLOSE_SMALL_PENDING`, `STATE_CLOSE_OLD_FAR_PENDING`, `STATE_CLOSE_BIG_PART_PENDING`, `STATE_CLOSE_NEW_FAR_PENDING`, `STATE_OPEN_NEW_BIG_PENDING`, `STATE_OPEN_NEW_SMALL_PENDING`, `STATE_RECOVERY_PENDING`, and `STATE_MANUAL_INTERVENTION_REQUIRED`.

## Recommended Parameters

The recommended compression preset is visible in the input defaults, but the EA does not silently override user inputs unless `UseRecommended5050Preset=true`.

## User Parameters vs Recommended Preset

When `UseRecommended5050Preset=false`, `Work*` values are copied directly from user inputs. Preset substitutions happen only inside the explicit `if(UseRecommended5050Preset)` block.
