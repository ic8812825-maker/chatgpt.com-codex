# R12A-FIX-01 — фактическое соответствие evaluator контракту

## Граница этапа

Baseline: `b58d4bf3a789039a056f378f0fad003c514a214c`.

Изменён только новый статический R12A evaluator. Замороженные R10–R12 artifacts, production `.mq5/.mqh`, Oracle V3, FSM, торговая и экономическая логика не изменялись.

## Исправление batch identity

`BATCH_ATOMICITY` теперь формирует identity из `context.transactionId` и `context.actionId` и отклоняет каждый deal/event, чья пара не равна context-паре. Causal проверки включают `VALID_BATCH`, отдельные несовпадения transaction/action и их совместное несовпадение.

`PRE_COMMIT` возвращает `NOT_APPLICABLE` только когда одновременно нет deals и events; наличие settled records в `PRE_COMMIT` является fail-closed отказом. `PARTIAL` и `REPLAY` отклоняются, а `COMMITTING`/`COMMITTED` проверяют identity, confirmed и равенство множеств intent/deal.

## Ledger и fill

Ledger evaluator сравнивает предъявленный root с SHA-256, вычисленным независимым canonicalizer из замороженного R12A normative contract; проверка длины строки не является verdict. Fill evaluator допускает partial/multiple fills, но использует Decimal, нулевую tolerance, volume grid, unique deal/event и intent/ticket binding.

## Coverage

AST audit использует отдельную карту source obligations и проверяет, что каждый field ownership matrix читается в соответствующей функции с `return fail(...)`-ветвью. Он больше не проверяет только сам факт наличия токена в историческом R12 evaluator.

## Статус

```text
R12A_CONTRACT=PASS
ACTUAL_EVALUATOR_COVERAGE=PASS
SECOND_BLOCK_SOURCE_MUTATIONS=NOT_STARTED
SECOND_BLOCK_ACCEPTANCE=NOT_GRANTED
QUALIFICATION_CORE_READY=NO
ORACLE_V3_FINAL_ACCEPTANCE=NOT_GRANTED
FULL_ECONOMIC_CORRECTNESS=NOT_PROVEN
LIFECYCLE_EXECUTED_BY_NATIVE_MODEL=NO
MODEL_CHANGES_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
METAEDITOR=NOT_RUN
MT5=NOT_RUN
```

Полная source-mutation suite намеренно не запускалась и не заявляется этим промежуточным этапом.
