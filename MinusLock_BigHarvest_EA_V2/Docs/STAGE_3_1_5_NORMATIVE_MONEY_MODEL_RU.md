# Этап 3.1.5 — нормативная денежная модель

```text
STAGE_3_1_4_STATUS=CLOSED
STAGE_3_1_5_AUTHORIZED=YES
STAGE_3_1_5_STARTED=YES
START_EXPECTED_HEAD=78fdcbc1bdbc982cde0898e65420cae1f759aa40
REPOSITORY_SCOPE=MinusLock_BigHarvest_EA_V2/{Docs,Tests,Tools}
PRODUCTION_TRADING_LOGIC_CHANGED=NO
```

Нормативный документ определяет статическую денежную семантику, но не доказывает исполнение MT5.

## Baseline проверок

Начальная ветка `work` синхронизирована с `origin/work`. Полный `pytest` до изменений остановлен
на collection: отсутствуют внешние `pandas` и `openpyxl`; это ограничение окружения и соседних
repository suites, а не результат Этапа 3.1.5.

## Термины, размерности и идентичность

Допустимые размерности: `LOT`, `PRICE`, `POINT`, `TICK`, `ACCOUNT_MONEY`, `RATIO`,
`INTEGER_RANK`, `BOOLEAN`, `EVENT_ID`, `DEAL_TICKET`, `POSITION_IDENTIFIER`.
`ProjectedMoney` — оценка; `DealNet` — подтверждённый экономический результат;
`RealizedCycleNet` — сумма уникальных managed deals; `FloatingLegCloseNow` — прогноз закрытия
actual volume; `RecoveryPLCloseNow` — realized плюс floating. Денежная идентичность задаётся
`AccountLogin + Symbol + Magic + CycleID`; позиция дополнительно имеет `PositionIdentifier/LegID`.
Сравнение lot с money, requested с actual и points с price без явного преобразования запрещено.

## Изоляция managed cycle

В Economic Ledger допускаются только записи с точным совпадением Account, Symbol, Magic и CycleID.
Manual trade, другой советник/символ/цикл, deposit, withdrawal, credit/balance correction исключаются.
`AccountBalanceNow-CycleStartBalance` запрещён как источник cycle P/L. При Initial Lock прибыль
закрытой плюсовой стартовой ноги помечается `INITIAL_IGNORED` до старта recovery cycle и не может
попасть в realized, Reserve, PartialFarBudget, Carry либо final-close gate.

## Projected broker money

Production semantic source — `OrderCalcProfit`. BUY закрывается по Bid, SELL — по Ask;
`SpreadPrice=Ask-Bid`, обе цены лежат на TickSize grid. Worst-case slippage сначала неблагоприятно
смещает control price и только затем вызывается расчёт. Oracle воспроизводит эту side-aware
семантику через Decimal и раздельные TickValueProfit/TickValueLoss; он не заменяет MT5.

## Actual deals и realized money

`DealNet=DEAL_PROFIT+DEAL_SWAP+DEAL_COMMISSION+DEAL_FEE` с фактическими знаками MT5.
IN, OUT, INOUT и OUT_BY сохраняются как entry type; каждый фактический DealTicket применяется
ровно один раз. Несколько fills агрегируются по actual volume/price/cost, а requested volume не
подменяет actual. Preview никогда не кредитует realized ledger и не завершает действие.

## Costs без двойного учёта

Spread учитывается только Bid/Ask. Projected slippage включается только в control price; actual
slippage — диагностическая разница, поскольку actual deal profit уже использует deal price.
Projected commission/fee являются estimate и заменяются actual после reconciliation. Commission,
swap и fee суммируются с их broker sign; знак по имени поля не инвертируется.

## Opening costs, partial fills и residual

`AllocatedEntryCost=UnallocatedEntryCost*ActualClosedVolume/PositionVolumeBefore`.
Распределение ведётся Decimal; последняя закрывающая часть получает весь rounding residual.
Частичный fill оставляет остаток volume и unallocated cost открытой позиции. Полное закрытие требует
нулевого остатка обоих полей после reconciliation.
