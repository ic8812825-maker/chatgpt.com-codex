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
