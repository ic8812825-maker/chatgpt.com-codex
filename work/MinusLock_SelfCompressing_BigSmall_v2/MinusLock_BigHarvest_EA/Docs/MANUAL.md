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
BigMoveLevel1 = 100
BigMoveLevel2 = 150
BigMoveLevel3 = 200
FarDistancePoints = 200
MaxHarvestLevels = 3
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
