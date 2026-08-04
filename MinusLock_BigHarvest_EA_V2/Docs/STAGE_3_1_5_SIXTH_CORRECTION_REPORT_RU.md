# Шестая корректирующая серия Этапа 3.1.5

Опубликованный verdict 3.1.5.106 пересмотрен шестой независимой проверкой.

```text
PUBLISHED_STAGE_3_1_5_106_PASS=SUPERSEDED
STAGE_3_1_5_STATUS=REOPENED_FOR_CORRECTION
NEXT_ALLOWED_STAGE=NONE
STAGE_3_1_6_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```

## Воспроизведённые дефекты

- возможно over-allocation относительно actual source net из-за маскировки отрицательного остатка;
- source-pool допускает foreign EventKey и несовпадающие event metadata;
- persisted Event Store принимает foreign event и невозможную пару `PERSISTED/revision=0`;
- allocation route может расходиться с родительским event;
- opening-cost state не подтверждён полной fill history;
- отдельные mutations засчитывают корректный отказ, вручную назначают observables и используют `FAULT_INPUT_OR_RULE`;
- final validator не исполняет все перечисленные exploit probes.

Это исходное failure evidence, а не PASS. Производственный MQL5 не изменяется.
