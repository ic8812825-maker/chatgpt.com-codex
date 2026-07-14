# SplitGeometry Big — отчёт Этапа 6: порядок RecoverState и Reserve Transaction Recovery

## Git

- Репозиторий: `https://github.com/ic8812825-maker/chatgpt.com-codex`
- Ветка: `work`
- Целевая папка: `MinusLock_BigHarvest_EA_V2`
- START_SHA: `1fa91d5123031707bfb9db2f60c023d4196262f5`
- FINAL_SHA: будет указан в финальном сообщении после публикации отчётного коммита.
- Compare: `https://github.com/ic8812825-maker/chatgpt.com-codex/compare/1fa91d5123031707bfb9db2f60c023d4196262f5...FINAL_SHA`

## Коммиты Этапа 6

1. `d8fcd2b` — Перестроен порядок восстановления Reserve Transaction  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/d8fcd2b
2. `2235929` — Добавлены тесты порядка RecoverState и crash-window  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/2235929
3. Итоговый отчётный коммит — будет указан после публикации.

## Изменённые файлы

- `Include/StateMachine.mqh` — перестроен порядок `RecoverState()`, добавлены `RecoveryInProgress`, phase-aware Ledger/cache validation, `ValidateLedgerEntryAgainstTransaction()`, route для `RESERVE_TX_COMPLETED`, persistence `NextReserveTransactionId`, non-destructive recovery failure marker, расширенная проверка Split close context и transaction-based `ApplyReserveReset()`.
- `Tests/unit/test_split_recovery_order_model.py` — поведенческая модель полного recovery pipeline: serialized globals → load context/pending → load Ledger → load transaction → phase-aware validation → transaction recovery → strict validation → state context validation.
- `Tests/static/test_split_architecture_static.py` — static guard порядка вызовов `RecoverState()` и защиты от регрессии Stage 6.
- `Docs/SPLIT_BIG_RECOVERY_ORDER_REPORT_RU.md` — этот отчёт.

## Старый проблемный порядок RecoverState

```text
Load part of RecoveryContext
→ Load Ledger
→ VerifyReserveLedgerPersistence()
→ LoadReserveTransaction()
→ ValidateRequiredRecoveredContextForState()
→ RecoverPendingReserveTransaction()
→ load pending/retry fields later
→ reconciliation
```

Проблемы старого порядка:

- Ledger мог сравниваться с `Ctx.totalReserve` до знания активной транзакции.
- Нормальный crash-window `LEDGER_WRITTEN` с `cache=reserveBefore` мог считаться mismatch.
- `STATE_SPLIT_PARTIAL_HISTORY_PENDING` мог проверяться до загрузки pending fields.
- Ошибка recovery могла вызвать обычный `SaveState()` и перезаписать неполный context.

## Новый порядок RecoverState

```text
1. Reset runtime memory.
2. Restore original EAState.
3. Load all RecoveryContext fields.
4. Load all pending and retry fields.
5. Load Ledger entries.
6. Load NextReserveEventId.
7. Load Reserve Transaction.
8. Load NextReserveTransactionId.
9. Fail-fast по отсутствующим/повреждённым полям.
10. ValidateReserveLedgerStructureOnly().
11. ValidateReserveTransactionRequiredFields().
12. ValidateLedgerAndCacheForTransactionPhase().
13. RecoverPendingReserveTransaction().
14. VerifyReserveLedgerPersistence().
15. ValidateRequiredRecoveredContextForState().
16. Position Resolution.
17. Reconciliation.
18. StateIntegrity.
19. RecoveryInProgress=false.
20. Continue FSM.
```

## Phase-aware правила

### Нет активной transaction

```text
LedgerReserve == Ctx.totalReserve
```

### PREPARED

```text
Ledger may not contain EventKey;
Ctx.totalReserve == reserveBefore;
```

Допустимое crash-window:

```text
Ledger already contains EventKey while phase is still PREPARED;
entry must match transaction completely;
phase is normalized to LEDGER_WRITTEN.
```

### LEDGER_WRITTEN

```text
Ledger contains exactly one EventKey;
entry fully matches transaction;
Ctx.totalReserve == reserveBefore OR reserveAfter.
```

### CACHE_UPDATED

```text
Ledger contains EventKey;
entry fully matches transaction;
Ctx.totalReserve == reserveAfter.
```

### COMPLETED

```text
Ledger contains EventKey;
entry fully matches transaction;
Ctx.totalReserve == reserveAfter;
active marker is cleared so a new EventKey is allowed.
```

## Полная сверка Ledger entry с transaction

Проверяются не только EventKey, но и:

```text
eventId == expectedLedgerEventId;
eventType;
amount;
reserveBefore;
reserveAfter;
symbolHash;
magicNumber;
cycleId;
harvestLevel;
reverseCycle;
FarIdentifier;
BigIdentifier;
SmallIdentifier;
BigCoreIdentifier;
BigTrendIdentifier;
SmallBaseIdentifier;
ReverseSmallIdentifier.
```

Денежные поля сравниваются с `ReserveMismatchTolerance`.

## Partial/history pending recovery

`PendingActionType`, `PendingOperationStartTime`, `PendingCloseFarLot`, `PendingPartialFarBudgetAvailable`, `PendingTicket`, pending identifiers и retry fields загружаются до вызова `ValidateRequiredRecoveredContextForState()`. Это предотвращает ложную блокировку `STATE_SPLIT_PARTIAL_HISTORY_PENDING` при restart.

## Recovery failure marker

При ошибке загрузки или phase-aware validation используется marker:

```text
RecoveryFailureActive = true;
RecoveryFailureTime;
RecoveryFailureOriginalState;
RecoveryFailureReasonCode/log reason.
```

Обычный полный `SaveState()` в ранней ошибке `RecoverState()` не вызывается, чтобы не перезаписать tickets, identifiers, pending context, Ledger, transaction, geometry, CycleId и `totalReserve` неполными значениями.

## ApplyReserveReset

Выбран безопасный вариант: `ApplyReserveReset()` больше не вызывает прямой `AppendReserveLedgerEntry(RESERVE_EVENT_RESET, ...)`, а строит `ReserveEventContextSnapshot` и запускает `StartReserveTransaction(snapshot, delta)`. Если активная Reserve Transaction уже есть, reset блокируется.

## MQL5 internal simulation hooks

Добавлены тестовые функции, доступные только при `UseInternalSimulation == true`:

```text
TestReserveRecoveryPrepared();
TestReserveRecoveryPreparedWithLedger();
TestReserveRecoveryLedgerWritten();
TestReserveRecoveryCacheUpdated();
TestReserveRecoveryCompleted();
TestPartialPendingRecoveryOrder();
```

Они не выполняют реальные сделки и не включаются производственным путём.

## Результаты crash-window тестов

```text
Restart после PREPARED = PASS
PREPARED with Ledger already written = PASS
Restart после LEDGER_WRITTEN with cache reserveBefore = PASS
Restart после LEDGER_WRITTEN with cache reserveAfter = PASS
Restart после CACHE_UPDATED = PASS
Restart в COMPLETED = PASS
Corrupted Ledger entry = PASS / STATE_RECOVERY_MISMATCH
Partial history pending order = PASS
Pending load failure = PASS / no reconciliation / no full SaveState
New EventKey after COMPLETED recovery = PASS
```

## Результаты команд

```text
pytest -q Tests/unit Tests/static Tests/scenario
65 passed
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

## Известные ограничения

- Реальная MetaEditor-компиляция и Strategy Tester должны быть выполнены на Windows/VPS.
- Runtime MT5 restart-тесты не запускались в контейнере; покрытие выполнено поведенческими Python-моделями и static guards.
- Split Small / DynamicReverseSmall / Small-пила / Small-разворот / BigCore remainder → NewFar не реализованы.
- Safe defaults сохранены: `UseSplitBigGeometry=false`, `UseLegacySingleBigGeometry=true`, `AllowRealTrading=false`.

## Статусы

```text
RECOVERY_FULL_LOAD_BEFORE_VALIDATION = PASS
RECOVERY_LOAD_FAIL_FAST = PASS
PHASE_AWARE_LEDGER_VALIDATION = PASS
PREPARED_CRASH_WINDOW_RECOVERY = PASS
LEDGER_WRITTEN_RECOVERY = PASS
CACHE_UPDATED_RECOVERY = PASS
COMPLETED_RECOVERY = PASS
LEDGER_ENTRY_TRANSACTION_MATCH = PASS
NEXT_TRANSACTION_ID_PERSISTENCE = PASS
STATE_REQUIRED_CONTEXT_COMPLETE = PASS
PARTIAL_PENDING_RESTART = PASS
RECOVERY_FAILURE_NON_DESTRUCTIVE = PASS
RESERVE_CREDIT_EXACTLY_ONCE = PASS
RESERVE_DEBIT_EXACTLY_ONCE = PASS
LEGACY_REGRESSION = PASS
PYTHON_TESTS = PASS
MQL5_INTERNAL_TESTS = NOT_RUN
METAEDITOR_COMPILE = NOT_RUN
MT5_STRATEGY_TESTER = NOT_RUN
REAL_TRADING_ALLOWED = NO
```

## Итоговый вердикт

Этап 6 закрывает оставшиеся критические дефекты recovery order: весь context и pending/retry загружаются до проверок, Ledger проходит только структурную проверку до загрузки transaction, промежуточные фазы Reserve Transaction восстанавливаются phase-aware, COMPLETED очищает active marker, Ledger entry полностью сверяется с transaction, а recovery failure не разрушает persisted context. До реальной MetaEditor/MT5 проверки проект остаётся `DEVELOPMENT / CONTROLLED TESTING ONLY`.
