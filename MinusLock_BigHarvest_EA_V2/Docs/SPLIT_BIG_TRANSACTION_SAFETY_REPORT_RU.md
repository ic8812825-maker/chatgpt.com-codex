# SplitGeometry Big — отчёт Этапа 5: Reserve Transaction safety

## Git

- Репозиторий: `https://github.com/ic8812825-maker/chatgpt.com-codex`
- Ветка: `work`
- Целевая папка: `MinusLock_BigHarvest_EA_V2`
- START_SHA: `67aaaa050d6e90388fff20042f18eba6be662d10`
- FINAL_SHA: будет указан в финальном сообщении после публикации коммита отчёта.
- Compare: `https://github.com/ic8812825-maker/chatgpt.com-codex/compare/67aaaa050d6e90388fff20042f18eba6be662d10...FINAL_SHA`

## Коммиты Этапа 5

1. `a6b396d` — Исправлена безопасная миграция и восстановление Reserve Transaction  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/a6b396d
2. `b40faf3` — Добавлены тесты транзакционной атомарности Reserve  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/b40faf3
3. Итоговый коммит отчёта — будет указан в финальном сообщении.

## Изменённые файлы

- `Include/Types.mqh` — добавлены `ReserveTransactionPhase`, `ReserveFailPoint`, `ReserveTransaction`.
- `Include/StateMachine.mqh` — исправлена граница legacy migration, добавлен fail-fast `recoveryLoadOk`, state-specific context validation, persistent Reserve Transaction, фазовое восстановление и EventId continuity.
- `Tests/unit/test_split_reserve_transaction_model.py` — поведенческая модель transaction/restart/failpoint/idempotency.
- `Tests/static/test_split_architecture_static.py` — static guard для Stage 5.
- `Docs/SPLIT_BIG_TRANSACTION_SAFETY_REPORT_RU.md` — этот отчёт.

## Структура Reserve Transaction

```text
active
transactionId
eventType
phase
amount
reserveBefore
reserveAfter
snapshot
eventKeyHash
eventKeyHashHigh/eventKeyHashLow
expectedLedgerEventId
startedAt
```

Фазы:

```text
RESERVE_TX_NONE
RESERVE_TX_PREPARED
RESERVE_TX_LEDGER_WRITTEN
RESERVE_TX_CACHE_UPDATED
RESERVE_TX_COMPLETED
```

## Порядок Reserve credit/debit

```text
PREPARED:
  freeze snapshot, EventKey, reserveBefore/reserveAfter, transactionId, expectedLedgerEventId
LEDGER_WRITTEN:
  append Ledger once if EventKey absent
CACHE_UPDATED:
  update Ctx.totalReserve cache to reserveAfter
COMPLETED:
  verify Ledger/cache and clear active transaction marker
```

Повторный вызов того же EventKey проверяется и через активную transaction, и через Ledger.

## Порядок recovery

```text
RecoverState
→ load exact 64-bit fields with recoveryLoadOk
→ stop immediately on persistence error
→ validate required context by EAState
→ load Reserve Ledger
→ load active Reserve Transaction
→ RecoverPendingReserveTransaction
→ only then proceed to reconciliation/FSM continuation
```

## Legacy migration

Граница исправлена:

```text
abs(legacy) < 2^53  -> migration allowed
abs(legacy) >= 2^53 -> migration blocked
```

Сценарий `2^53 + 1 -> double -> 2^53` теперь блокируется, потому что stored double равен неоднозначной границе `2^53`.

## Failpoint-тесты

Проверены фазы:

```text
RESERVE_FAIL_AFTER_PREPARED
RESERVE_FAIL_AFTER_LEDGER_WRITE
RESERVE_FAIL_AFTER_CACHE_UPDATE
RESERVE_FAIL_BEFORE_COMPLETED
```

Ожидание выполнено:

```text
одна Ledger entry;
одно изменение Reserve;
после recovery transaction завершена;
EventId последовательны.
```

## Required context checks

Проверены state-specific требования:

```text
STATE_FAR_ACTIVE
STATE_SPLIT_GEOMETRY_ACTIVE
STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR
```

Повреждённый context приводит к `STATE_RECOVERY_MISMATCH` и не допускает Reconciliation/торговые операции.

## EventId continuity

Ledger теперь требует:

```text
EventId[0] = 1
EventId[i] = EventId[i-1] + 1
NextReserveEventId > max(EventId)
```

Нарушение фиксируется как `RESERVE_LEDGER_EVENT_ID_GAP`.

## Результаты тестов

```text
pytest -q Tests/unit Tests/static Tests/scenario
53 passed
```

```text
python Tests/validate_v2_static.py
PASS
```

```text
python Tests/default_parameters_v241_check.py
PASS
```

```text
python Tests/fsm_integrity_check.py
PASS
```

```text
python Tests/terminal_states_separated_from_pending_check.py
PASS
```

## MetaEditor

MetaEditor/MT5 в Linux-контейнере не обнаружены.

```text
METAEDITOR_COMPILE = NOT_RUN
MetaTrader 5 build = NOT_RUN
MetaEditor build = NOT_RUN
Главный MQ5 = MinusLock_BigHarvest_EA.mq5
Compile log = NOT_RUN
REAL_TRADING_ALLOWED = NO
```

## MT5 Strategy Tester

MT5 Strategy Tester недоступен в контейнере.

```text
MT5_STRATEGY_TESTER = NOT_RUN
REAL_TRADING_ALLOWED = NO
```

## Ограничения

- MetaEditor compile и MT5 Strategy Tester должны быть выполнены отдельно на Windows/VPS.
- Runtime MT5 restart/failpoint tests не запускались в контейнере; покрыты поведенческими Python-моделями.
- Persistence/ReserveTransaction оставлены в `StateMachine.mqh`, чтобы не увеличивать риск include-order регрессий; дальнейший перенос в `Persistence64.mqh`, `ReserveLedger.mqh`, `ReserveTransaction.mqh` возможен отдельным refactor-этапом.
- Split Small / DynamicReverseSmall / Small-пила / Small-разворот / BigCore remainder → NewFar не реализованы.

## Статусы

```text
LEGACY_MIGRATION_BOUNDARY = PASS
RECOVERY_LOAD_FAIL_FAST = PASS
STATE_REQUIRED_CONTEXT = PASS
RESERVE_TRANSACTION_PREPARE = PASS
RESERVE_TRANSACTION_LEDGER_COMMIT = PASS
RESERVE_TRANSACTION_CACHE_COMMIT = PASS
RESERVE_TRANSACTION_RECOVERY = PASS
RESERVE_CREDIT_EXACTLY_ONCE = PASS
RESERVE_DEBIT_EXACTLY_ONCE = PASS
RESERVE_FAILPOINT_TESTS = PASS
EVENT_ID_CONTINUITY = PASS
PYTHON_TESTS = PASS
METAEDITOR_COMPILE = NOT_RUN
MT5_STRATEGY_TESTER = NOT_RUN
REAL_TRADING_ALLOWED = NO
```

## Итоговый вердикт

Этап 5 закрывает критические риски: неоднозначная legacy migration на границе `2^53` блокируется, RecoverState останавливается при persistence-ошибке, Reserve credit/debit выполняются через persistent transaction и восстанавливаются exactly once после сбоя на любой фазе. До реальной MetaEditor/MT5 проверки проект остаётся `DEVELOPMENT / CONTROLLED TESTING ONLY`.
