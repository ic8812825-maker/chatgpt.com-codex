# Manual Test Cases — MinusLock BigHarvest EA

## TC-01: первый плюс не участвует в разруливании

**Шаги:**
1. Запустить советник с `StartLot = 1.00`.
2. Дождаться открытия `MinusLock_INITIAL_BUY` и `MinusLock_INITIAL_SELL`.
3. Довести одну позицию до `InitialTriggerPoints` прибыли.

**Ожидание:**
- Плюсовая позиция закрыта полностью.
- Оставшаяся позиция записана как `Far`.
- `InitialProfitIgnored = true`.
- `totalReserve = 0.0`.

## TC-02: Level 1 Big-harvest для Far = 1.00

**Вход:**

```text
FarLot = 1.00
BigMovePoints = 100
PointValuePerLot = 1
```

**Ожидание:**

```text
BigLot = 1.30
SmallLot = 0.48
ProfitBig = 130.00
LossSmall = 48.00
NetProfit = 82.00
CloseFarBudget = 73.80
CloseFarLotRaw = 0.369
CloseFarLotRounded = 0.36
FarRemainLot = 0.64
ReserveAdd = 8.20
TotalReserve = 8.20
FinalCloseAllowed = false
```

## TC-03: полный цикл StartLot = 1.00

**Ожидание:**

```text
Level 1 FarRemain = 0.64, Reserve = 8.20
Level 2 FarRemain = 0.29, Reserve = 16.00
Level 3 FarRemain = 0.08, Reserve = 20.80
FarRemainLoss = 16.00
CycleFinalPL = +4.80
State = STATE_CLOSED_PROFIT
```

## TC-04: Small-сценарий не ломается математически

**Вход:**

```text
Far = 1.00
Big = 1.30
Small = 0.48
SmallMovePoints = 100
```

**Ожидание:**

```text
CloseBig = 0.39
RemainBig = 0.91
ProfitSmall = 48.00
LossClosedBig = 39.00
NetSmall = +9.00
```

## TC-05: DUAL_TAIL protection

**Шаги:**
1. Открыть `Far`.
2. Открыть `Big/Small`.
3. Смоделировать Small-сценарий.

**Ожидание:**
- `Small` закрыт полностью.
- 30% `Big` закрыто.
- При наличии старого `Far` и оставшихся 70% `Big` советник переходит в `STATE_DUAL_TAIL`.
- Новый уровень не открывается.

## Small-at-Far Scenario

Small-сценарий больше не исполняется сразу при первом движении в сторону Small. Если Small достиг защитного движения, советник переводит цикл в `STATE_WAIT_SMALL_TO_FAR` и ждёт, пока текущая цена дойдёт до цены открытия старого `Far` с учётом `SmallFarTouchOffsetPoints`. Для `Small=BUY` условие касания: `CurrentPrice >= OldFarOpenPrice + offset`; для `Small=SELL`: `CurrentPrice <= OldFarOpenPrice - offset`.

После касания старого Far выполняется `ProcessSmallAtFarTouch`: Small закрывается на 100%, старый Far закрывается на 100%, Big закрывается только на `CloseBigOnSmall`, а остаток Big становится новым Far. Затем обязательно сначала проверяется `FinalCloseAllowed` для нового Far. Если резерва хватает, новый Far закрывается полностью и состояние становится `STATE_CLOSED_PROFIT`; если резерва не хватает, только тогда открывается новый Big/Small от нового Far. В нормальном Small-at-Far сценарии `DUAL_TAIL` не должен появляться, потому что старый Far ликвидируется до назначения нового Far.

---

## Reverse Geometry Protection

### Case RG-1: Valid reverse

```text
OldFarLot = 1.00
BigLot = 1.30
CloseBigLotRounded = 0.39
NewFarLot = 0.91
NewBigLot = 1.18
NewSmallLot = 0.44
```

Ожидание:

```text
GeometryValid = true
ReverseStrength ≈ 0.2967
ReverseStrengthStatus = STRONG
```

### Case RG-2: NewFar не сжался

```text
OldFarLot = 1.00
NewFarLot = 1.00
```

Ожидание:

```text
STATE_INVALID_REVERSE_GEOMETRY
GeometryInvalidReason = NewFarLot >= OldFarLot
ActionAfterValidation = STOP_INVALID_REVERSE_GEOMETRY
```

### Case RG-3: NewBig не сильнее NewFar

```text
NewFarLot = 1.00
NewBigLot = 1.00
```

Ожидание:

```text
STATE_INVALID_REVERSE_GEOMETRY
GeometryInvalidReason = NewBigLot <= NewFarLot
```

### Case RG-4: Weak ReverseStrength

```text
NewFarLot = 1.00
NewBigLot = 1.05
ReverseStrength = 0.05
```

Ожидание:

```text
STATE_INVALID_REVERSE_GEOMETRY
GeometryInvalidReason = ReverseStrength below minimum
```

### Case RG-5: Reverse limit

```text
reverseCycleCount = 4
MaxReverseCycles = 3
```

Ожидание:

```text
STATE_REVERSE_LIMIT
новый Big/Small не открывается
```

### Case RG-6: FinalClose priority

Если `FinalCloseAllowed = true`, советник закрывает NewFar полностью, выставляет `STATE_CLOSED_PROFIT` и не открывает новый Big/Small.
