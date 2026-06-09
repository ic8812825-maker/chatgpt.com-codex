# МАНУАЛ СИСТЕМЫ BIG-HARVEST

## Основные параметры

| Параметр         |        Значение | Смысл                                       |
| ---------------- | --------------: | ------------------------------------------- |
| BigRatio         |            130% | Big = Far × 1.30                            |
| SmallRatio       |             37% | Small = Big × 0.37                          |
| CloseBigOnSmall  |             30% | при Small-сценарии закрыть 30% Big          |
| RemainBigOnSmall |             70% | остаток Big становится новым Far            |
| CloseFarShare    |             90% | 90% чистой прибыли Big-сценария идёт на Far |
| ReserveShare     |             10% | 10% чистой прибыли идёт в резерв            |
| BigMovePoints    | 100 / 150 / 200 | цели Big-harvest                            |
| LotStep          |            0.01 | минимальный шаг лота                        |

---

# 1. Главная идея системы

Есть дальняя убыточная позиция:

```text
Far = 100%
```

Против неё открывается усиленный Big:

```text
Big = Far × 130%
```

И страховочный Small:

```text
Small = Big × 37%
```

То есть на 1.00 Far:

```text
Big = 1.30
Small = 0.48
```

Big должен быть сильнее Far, а Small должен быть достаточно большим, чтобы при развороте Small-сценарий не ломался.

---

# 2. Big-сценарий

Big-сценарий — это когда цена идёт в сторону Big.

На каждом Big-harvest:

```text
Big закрывается 100%
Small закрывается 100%
```

Дальше считается чистая прибыль:

```text
NetProfit = ProfitBig - LossSmall
```

Потом прибыль делится:

```text
90% NetProfit → на частичное закрытие Far
10% NetProfit → в резерв
```

Важно:

```text
CloseFarShare = 90% — это НЕ 90% лота Far.
Это 90% денег от чистой прибыли.
```

Правильная формула:

```text
CloseFarBudget = NetProfit × 0.90
```

```text
CloseFarLotRaw = CloseFarBudget / FarDistancePoints
```

```text
CloseFarLotRounded = FLOOR(CloseFarLotRaw, LotStep)
```

```text
FarRemain = FarStart - CloseFarLotRounded
```

---

# 3. Small-сценарий

Small-сценарий — это когда цена пошла против Big, в сторону Small.

Тогда:

```text
Small закрывается 100%
Big закрывается 30%
70% Big остаётся и становится новым Far
```

Формулы:

```text
CloseBigLot = BigLot × 30%
```

```text
RemainBigLot = BigLot × 70%
```

```text
NewFar = RemainBigLot
```

Проверка на 1.00 Far:

```text
Far = 1.00
Big = 1.30
Small = 1.30 × 37% = 0.481 ≈ 0.48
CloseBig = 1.30 × 30% = 0.39
RemainBig = 1.30 × 70% = 0.91
```

При движении 100 пунктов в сторону Small:

```text
ProfitSmall = 0.48 × 100 = +48
LossClosedBig = 0.39 × 100 = -39
NetSmall = +9
```

Новый Far:

```text
NewFar = 0.91
```

То есть Small-сценарий рабочий:

```text
Small > CloseBig
NetSmall > 0
NewFar < OldFar
```

---

# 4. Почему нельзя усиливать Big бесконтрольно

Главное правило:

```text
Big > Small
Total Big > Total Far
но Small-сценарий не должен ломаться
```

Если сделать Big слишком большим, например 140–160%, то при уходе цены в сторону Small остаток Big может создать плохой новый Far и сломать переворот.

Поэтому текущий безопасный баланс:

```text
Big = 130%
Small = 37%
CloseBig = 30%
RemainBig = 70%
```

---

# 5. Repeat Harvest

Repeat Harvest — это повторное открытие Big/Small от остатка Far.

После каждого Big-сценария:

```text
Far уменьшается
новый Big считается от нового Far
новый Small считается от нового Big
```

Система не увеличивает BigRatio, а усиливается за счёт движения:

```text
1 harvest = 100 пунктов
2 harvest = 150 пунктов
3 harvest = 200 пунктов
```

Это безопаснее, чем увеличивать Big-лот.

---

# 6. FinalCloseAllowed

После каждого уровня проверяется:

```text
FarRemainLoss = FarRemain × FarDistancePoints
```

```text
FinalCloseAllowed = TotalReserve >= FarRemainLoss
```

Если:

```text
FinalCloseAllowed = YES
```

то:

```text
остаток Far закрывается полностью
цикл завершается
Status = CLOSED_PROFIT
новые уровни больше не строятся
```

---

# 7. Пример StartLot = 1.00

Условия:

```text
Start Far = 1.00
FarDistance = 200 пунктов
LotStep = 0.01
BigMovePoints = 100 / 150 / 200
```

## Level 1

```text
FarStart = 1.00
Big = 1.00 × 1.30 = 1.30
Small = 1.30 × 0.37 = 0.481 → 0.48
BigMove = 100
```

```text
ProfitBig = 1.30 × 100 = 130
LossSmall = 0.48 × 100 = 48
NetProfit = 82
```

```text
ReserveAdd = 82 × 10% = 8.20
CloseFarBudget = 82 × 90% = 73.80
CloseFarLotRaw = 73.80 / 200 = 0.369
CloseFarLotRounded = 0.36
FarRemain = 1.00 - 0.36 = 0.64
```

## Level 2

```text
FarStart = 0.64
Big = 0.64 × 1.30 = 0.832 → 0.83
Small = 0.83 × 0.37 = 0.307 → 0.31
BigMove = 150
```

```text
ProfitBig = 0.83 × 150 = 124.50
LossSmall = 0.31 × 150 = 46.50
NetProfit = 78.00
```

```text
ReserveAdd = 7.80
TotalReserve = 8.20 + 7.80 = 16.00
CloseFarBudget = 70.20
CloseFarLotRaw = 70.20 / 200 = 0.351
CloseFarLotRounded = 0.35
FarRemain = 0.64 - 0.35 = 0.29
```

## Level 3

```text
FarStart = 0.29
Big = 0.29 × 1.30 = 0.377 → 0.38
Small = 0.38 × 0.37 = 0.141 → 0.14
BigMove = 200
```

```text
ProfitBig = 0.38 × 200 = 76.00
LossSmall = 0.14 × 200 = 28.00
NetProfit = 48.00
```

```text
ReserveAdd = 4.80
TotalReserve = 20.80
CloseFarBudget = 43.20
CloseFarLotRaw = 43.20 / 200 = 0.216
CloseFarLotRounded = 0.21
FarRemain = 0.29 - 0.21 = 0.08
```

Проверка полного закрытия:

```text
FarRemainLoss = 0.08 × 200 = 16.00
TotalReserve = 20.80
```

```text
FinalClosePL = 20.80 - 16.00 = +4.80
```

Значит:

```text
FinalCloseAllowed = YES
```

Цикл закрывается в плюс.

---

# 8. Итоговая таблица StartLot = 1.00

| Level | FarStart | BigMove |  Big | Small | NetProfit | CloseFar | FarRemain | TotalReserve | FinalClose |
| ----: | -------: | ------: | ---: | ----: | --------: | -------: | --------: | -----------: | ---------- |
|     1 |     1.00 |     100 | 1.30 |  0.48 |     82.00 |     0.36 |      0.64 |         8.20 | NO         |
|     2 |     0.64 |     150 | 0.83 |  0.31 |     78.00 |     0.35 |      0.29 |        16.00 | NO         |
|     3 |     0.29 |     200 | 0.38 |  0.14 |     48.00 |     0.21 |      0.08 |        20.80 | YES        |

Итог:

```text
цикл закрыт на Level 3
финальный результат: +4.80
```

---

# 9. Пример StartLot = 2.00

| Level | FarStart | BigMove |  Big | Small | NetProfit | CloseFar | FarRemain | TotalReserve | FinalClose |
| ----: | -------: | ------: | ---: | ----: | --------: | -------: | --------: | -----------: | ---------- |
|     1 |     2.00 |     100 | 2.60 |  0.96 |    164.00 |     0.73 |      1.27 |        16.40 | NO         |
|     2 |     1.27 |     150 | 1.65 |  0.61 |    156.00 |     0.70 |      0.57 |        32.00 | NO         |
|     3 |     0.57 |     200 | 0.74 |  0.27 |     94.00 |     0.42 |      0.15 |        41.40 | YES        |

```text
FarRemainLoss = 0.15 × 200 = 30.00
FinalClosePL = 41.40 - 30.00 = +11.40
```

---

# 10. Пример StartLot = 5.00

| Level | FarStart | BigMove |  Big | Small | NetProfit | CloseFar | FarRemain | TotalReserve | FinalClose |
| ----: | -------: | ------: | ---: | ----: | --------: | -------: | --------: | -----------: | ---------- |
|     1 |     5.00 |     100 | 6.50 |  2.41 |    409.00 |     1.84 |      3.16 |        40.90 | NO         |
|     2 |     3.16 |     150 | 4.11 |  1.52 |    388.50 |     1.74 |      1.42 |        79.75 | NO         |
|     3 |     1.42 |     200 | 1.85 |  0.68 |    234.00 |     1.05 |      0.37 |       103.15 | YES        |

```text
FarRemainLoss = 0.37 × 200 = 74.00
FinalClosePL = 103.15 - 74.00 = +29.15
```

---

# 11. Вердикт

Текущая версия:

```text
BigRatio = 130%
SmallRatio = 37%
CloseBigOnSmall = 30%
RemainBigOnSmall = 70%
CloseFarShare = 90%
ReserveShare = 10%
BigMovePoints = 100 / 150 / 200
```

является лучшим найденным вариантом.

Почему:

```text
1. Big-сценарий закрывает цикл на 3 уровне.
2. Small-сценарий не ломается.
3. Новый Far после Small = 91% от старого Far.
4. Резерв остаётся положительным.
5. Не нужно опасно увеличивать BigRatio.
```

Главное правило:

```text
усиливаем систему не Big-лотом, а BigMovePoints.
```

Это сохраняет Small-сценарий и даёт быстрое закрытие через Repeat Harvest.
