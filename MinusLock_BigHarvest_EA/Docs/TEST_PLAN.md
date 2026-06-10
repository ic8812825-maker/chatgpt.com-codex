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
