# Итоговый отчёт end-to-end Big/Small

START_SHA=1ad00b774cc79fe0199a086ece848d505428f83c
BRANCH=work
PROJECT_FOLDER=MinusLock_BigHarvest_EA_V2
COMPARE_URL=https://github.com/ic8812825-maker/chatgpt.com-codex/compare/1ad00b774cc79fe0199a086ece848d505428f83c...work

## Реализация

Big gate разделяет managed Symbol+Magic volume и broker-total directional volume. Projected margin использует текущую margin, полную новую basket margin и opening commission/spread/slippage/buffers. Small five-leg contract проверяет точные нормализованные объёмы. Каждая фактическая Small operation сохраняет persisted audit, а итоговая reconciliation проверяет deals, residual positions, New Far, orphan positions, Reserve Ledger и Recovery result. Finite reverse строит отдельную projection каждого цикла. False Reverse рассчитывает полный basket и выполняется отдельным persisted FSM. MQL5 harness переведён на `TestMarketEvent` и вызывает `RunStateMachine()` вместо прямого назначения ожидаемых State.

## Статусы

```text
BIG_MAGIC_ISOLATION=PYTHON_PASS_MQL5_NOT_RUN
BIG_ATOMIC_MARGIN_GATE=PYTHON_PASS_MQL5_NOT_RUN
BIG_RECOVERY_IMPROVEMENT=PYTHON_PASS_MQL5_NOT_RUN
BIG_RESERVE_CATCH_UP_PROJECTED=PYTHON_PASS_MQL5_NOT_RUN
BIG_RESERVE_CATCH_UP_ACTUAL=PYTHON_PASS_MQL5_NOT_RUN
BIG_PARTIAL_FAR=IMPLEMENTED_MQL5_NOT_RUN
BIG_FINAL_CLOSE=IMPLEMENTED_MQL5_NOT_RUN
HARVEST_ALL_PHASE_RESTART=PYTHON_PASS_MQL5_NOT_RUN

SMALL_FIVE_LEG_LOT_CONTRACT=PYTHON_PASS_MQL5_NOT_RUN
SMALL_PRETRADE_GATE=IMPLEMENTED_MQL5_NOT_RUN
SMALL_POSTTRADE_RECONCILIATION=PYTHON_PASS_MQL5_NOT_RUN
SMALL_NEW_FAR_COMPRESSION=PYTHON_PASS_MQL5_NOT_RUN
SMALL_DYNAMIC_FINITE_REVERSE=PYTHON_PASS_MQL5_NOT_RUN
FALSE_REVERSE_EVALUATION=PYTHON_PASS_MQL5_NOT_RUN
FALSE_REVERSE_EXECUTION=IMPLEMENTED_MQL5_NOT_RUN
FALSE_REVERSE_RECONCILIATION=IMPLEMENTED_MQL5_NOT_RUN

BIG_SMALL_SCENARIO_ISOLATION=PYTHON_PASS_MQL5_NOT_RUN
MQL5_END_TO_END_HARNESS=READY_FOR_COMPILE_NOT_RUN
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN

BIG_SCENARIO_BROKEN=UNKNOWN
SMALL_SCENARIO_BROKEN=UNKNOWN
BIG_SMALL_INTERACTION_BROKEN=UNKNOWN
REAL_TRADING_ALLOWED=NO
```

## Невыполненное

В Linux-контейнере отсутствуют MetaEditor, Wine/MetaTrader и MT5 Strategy Tester. MQL5 harness создан, но не компилировался и не запускался, поэтому его сценарии нельзя объявить PASS. Отсутствуют реальные MetaEditor compile logs и Strategy Tester HTML/Journal/Expert/CSV. Broker-dependent conversion, execution, margin release и deal history остаются runtime-риском до Windows/VPS проверки.

Разрешённый режим: **только дальнейшая разработка и тестирование**.
