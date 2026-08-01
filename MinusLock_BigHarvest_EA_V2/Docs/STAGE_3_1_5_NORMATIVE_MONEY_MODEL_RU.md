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
