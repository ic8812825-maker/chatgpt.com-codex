# Повторное открытие Этапа 3.1.5

```text
SECOND_INDEPENDENT_REVIEW=FAIL
PUBLISHED_3_1_5_38_PASS=SUPERSEDED
STAGE_3_1_5_STATUS=REOPENED_FOR_CORRECTION
NEXT_ALLOWED_STAGE=NONE
STAGE_3_1_6_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```

Причины: expected был actual во всех 80 scenarios; partial/reconciliation scenarios повторялись;
Allocation Ledger терялся после restart; consume не изменял state; source harvest повторно
распределялся; IN deal ошибочно попадал в realized; Final Close принимал foreign snapshot и не все
pending states; mutations копировали Policy в Observables вместо денежных операций; pytest-owner
validator принимался без исполнения.
