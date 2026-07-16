# Отчёт валидации Big/Small

START_SHA=5fc693fcdb33476a3e423a411c989568471c00df
BRANCH=work
PROJECT_FOLDER=MinusLock_BigHarvest_EA_V2
COMPARE_URL=https://github.com/ic8812825-maker/chatgpt.com-codex/compare/5fc693fcdb33476a3e423a411c989568471c00df...work

## Реализовано в этом проходе

Процентная комиссия больше не зависит от прибыли: база выбирается явно, а отключённая или недоступная база блокирует projection. Close-now принимает accrued swap и принудительно использует нулевой holding period. Big Recovery gate требует строго превысить положительный порог и tolerance. Reserve Catch-Up отдельно использует фактические ReserveAfter и CarryAfter. Поведенческая модель исполняет запросы открытия/закрытия, отказы, partial fill, restart и exactly-once ledger. MQL5 harness больше не содержит безусловных PASS.

## Честные статусы

```text
BROKER_MONEY_MODEL=PARTIAL_READY_FOR_COMPILE
COMMISSION_MODEL=IMPLEMENTED_NOT_COMPILED
SWAP_MODEL=IMPLEMENTED_NOT_COMPILED
BIG_RECOVERY_IMPROVEMENT=IMPLEMENTED_NOT_COMPILED
BIG_RESERVE_CATCH_UP=IMPLEMENTED_NOT_COMPILED
HARVEST_EXACTLY_ONCE=PARTIAL
PARTIAL_FAR_MONEY_SAFETY=IMPLEMENTED_NOT_COMPILED
FINAL_CLOSE_GATE=IMPLEMENTED_NOT_COMPILED
SMALL_TRANSITION_MONEY=PARTIAL
NEW_FAR_COMPRESSION=IMPLEMENTED_NOT_COMPILED
FINITE_REVERSE_COUNT=FAIL_MONEY_MODEL_INCOMPLETE
FALSE_REVERSE_PROTOCOL=FAIL_INCOMPLETE
SCENARIO_ISOLATION=IMPLEMENTED_NOT_COMPILED
PYTHON_BEHAVIOR_MODEL=PASS
MQL5_HARNESS=READY_FOR_COMPILE
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN
BIG_SCENARIO_BROKEN=UNKNOWN
SMALL_SCENARIO_BROKEN=UNKNOWN
BIG_SMALL_INTERACTION_BROKEN=UNKNOWN
REAL_TRADING_ALLOWED=NO
```

MetaEditor и MT5 отсутствуют в текущем Linux-контейнере. Поэтому MQL5 runtime PASS, исправность сценариев и пригодность для торговли не заявляются. Разрешён только режим дальнейшей разработки и тестирования.
