# Этап 7. Финализация Recovery Safety, Reserve Reset и StateIntegrity после восстановления

## Идентификаторы

- START_SHA: `5247c71e70ec42fe58ea73117f2239fe68d744c0`
- FINAL_SHA: фиксируется финальной проверкой Git после коммита отчёта.
- Compare: `https://github.com/ic8812825-maker/chatgpt.com-codex/compare/5247c71e70ec42fe58ea73117f2239fe68d744c0...work`
- Ветка: `work`
- Проект: `MinusLock_BigHarvest_EA_V2`

## Изменённые файлы

- `Include/Types.mqh`
- `Include/StateMachine.mqh`
- `Include/TradeEngine.mqh`
- `Tests/unit/test_split_recovery_order_model.py`
- `Tests/static/test_split_architecture_static.py`
- `Docs/SPLIT_BIG_FINAL_RECOVERY_SAFETY_REPORT_RU.md`

## Таблица требований ReserveEventType

| EventType | Far | LegacyBig | LegacySmall | BigCore | BigTrend | SmallBase | ReverseSmall | HarvestLevel | Комментарий |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RESERVE_EVENT_SPLIT_BIG_HARVEST_ADD` | YES | NO | NO | YES | YES | YES | NO | YES | Полный Split harvest context обязателен. |
| `RESERVE_EVENT_SPLIT_BIG_FINAL_DEBIT` | YES | NO | NO | YES | YES | YES | NO | YES | Используется frozen Split snapshot. |
| `RESERVE_EVENT_BIG_HARVEST_ADD` | YES | YES | YES | NO | NO | NO | NO | YES | Legacy Big/Small context. |
| `RESERVE_EVENT_REVERSE_TRANSITION_ADD` | YES | NO | NO | conditional | conditional | NO | conditional | NO | Требуется reverse/split identifier, участвующий в переходе. |
| `RESERVE_EVENT_RESET` | NO | NO | NO | NO | NO | NO | NO | NO | Reset не требует Far/Split/Legacy identifiers. |
| Остальные | YES | NO | NO | NO | NO | NO | NO | NO | Без общего fallback на Split identifiers. |

Функция `ValidateReserveTransactionContextByEventType()` выполняет event-type-specific validation, а `ReserveEventTypeRequirementsToString()` печатает таблицу требований в логах вместе с `ValidationResult`.

## Reserve Reset

`ApplyReserveReset()` переведён на транзакционный маршрут через `StartReserveTransaction()` и `RESERVE_EVENT_RESET`. Перед запуском вызывается `CanStartReserveReset()`:

1. допустимы только `STATE_IDLE`, `STATE_STOP`, `STATE_CLOSED_PROFIT`, `STATE_CLOSED_RECOVERY_LOSS`;
2. `RecoveryInProgress == false`;
3. нет активной `ActiveReserveTransaction`;
4. `CountManagedOpenPositions() == 0`;
5. `HasOpenLegContext() == false`.

При блокировке пишется `RESERVE_RESET_BLOCKED` с причиной. Reset без Far допустим и покрыт unit-моделью для фаз `PREPARED`, `PREPARED` с уже записанным Ledger, `LEDGER_WRITTEN`, `CACHE_UPDATED`, `COMPLETED` и дельт `100→0`, `0→100`, `100→50`.

## Recovery Failure Marker

Marker сохраняет только отдельные ключи `RecoveryFailure*` и не вызывает полный `SaveState()`:

- `RecoveryFailureActive`;
- `RecoveryFailureReasonCode`;
- `RecoveryFailureTime`;
- `RecoveryFailureOriginalState`;
- `RecoveryFailureCycleIdHigh32/Low32`;
- `RecoveryFailureTransactionIdHigh32/Low32`;
- `RecoveryFailureEventKeyHigh32/Low32`.

`MarkRecoveryFailure(reason, originalState)` сначала сохраняет исходный persisted state, а только затем переводит runtime `State` в `STATE_RECOVERY_MISMATCH`. Успешный recovery вызывает `ClearRecoveryFailureMarker()` только после ledger, transaction, state-context, reconciliation и StateIntegrity checks.

## StateIntegrity и reconciliation

Финальная часть `RecoverState()` теперь проверяет:

1. `reconcileOk`;
2. terminal result через `RecoveryTerminalResultIsSuccessful()`;
3. результат `ValidateCurrentStateIntegrity()`.

Если reconciliation или integrity fail, `RecoverState()` возвращает `false`, логирует `RECOVERY_ABORTED`, сохраняет failure marker с исходным state и не пишет `RECOVERY_COMPLETE Result=PASS`.

## RecoveryInProgress gate

Добавлен централизованный gate `TradingOperationAllowedDuringRecovery(operationName, isRecoveryContinuation)`.

Заблокированы новые операции во время recovery:

- `RunStateMachine`;
- `OpenInitialLock`;
- `OpenPosition`;
- `OpenBigSmall`;
- `OpenSplitRole`;
- новая `StartReserveTransaction` с новым EventKey.

Разрешено продолжение уже сохранённой reserve transaction с тем же EventKey и read-only/reconciliation операции.

## Флаг готовности Split Harvest Net

В `RecoveryContext` добавлен `actualSplitHarvestNetCalculated`. Он сохраняется как `ActualSplitHarvestNetCalculated`, восстанавливается в `RecoverState()`, сбрасывается при очистке контекста и выставляется после `CalculateSplitLifecycleNet()`.

`STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR` теперь требует `actualSplitHarvestNetCalculated == true`, а не `actualSplitHarvestNet != 0.0`. Поэтому `actualSplitHarvestNet = 0.0` является валидным рассчитанным результатом, если флаг готовности установлен.

## Аудит денежных проверок `!= 0.0`

Проверка `actualSplitHarvestNet != 0.0` была заменена на calculated-флаг, потому что нулевой lifecycle net является допустимым результатом расчёта. Остальные найденные проверки нулевых денежных значений используются как арифметические guards или budget/lot thresholds и не являются индикатором готовности расчёта.

## Результаты тестов

- `pytest -q Tests/unit Tests/static Tests/scenario` → `78 passed`.
- `python Tests/validate_v2_static.py` → `PASS`.
- `python Tests/default_parameters_v241_check.py` → `PASS`.
- `python Tests/fsm_integrity_check.py` → `PASS`.
- `python Tests/terminal_states_separated_from_pending_check.py` → `PASS`.

## MetaEditor и MT5

Linux-контейнер не содержит `MetaEditor`/`terminal64.exe`/`wine`; реальная компиляция и Strategy Tester не запускались.

- METAEDITOR_COMPILE = NOT_RUN
- MT5_STRATEGY_TESTER = NOT_RUN
- REAL_TRADING_ALLOWED = NO

## Статусы

| Статус | Результат |
| --- | --- |
| RESERVE_EVENT_TYPE_CONTEXT_RULES | PASS |
| RESERVE_RESET_WITHOUT_FAR | PASS |
| RESERVE_RESET_PREPARED_RESTART | PASS |
| RESERVE_RESET_LEDGER_RESTART | PASS |
| RESERVE_RESET_CACHE_RESTART | PASS |
| RESERVE_RESET_COMPLETED_RESTART | PASS |
| RECOVERY_FAILURE_ORIGINAL_STATE | PASS |
| RECOVERY_FAILURE_REASON_PERSISTENCE | PASS |
| RECOVERY_FAILURE_NON_DESTRUCTIVE | PASS |
| RECOVERY_STATE_INTEGRITY_RESULT | PASS |
| RECOVERY_RECONCILIATION_RESULT | PASS |
| RECOVERY_OPERATION_GATE | PASS |
| ZERO_SPLIT_HARVEST_NET_READY | PASS |
| RESERVE_CREDIT_EXACTLY_ONCE | PASS |
| RESERVE_DEBIT_EXACTLY_ONCE | PASS |
| LEGACY_REGRESSION | PASS |
| PYTHON_TESTS | PASS |
| MQL5_INTERNAL_TESTS | NOT_RUN |
| METAEDITOR_COMPILE | NOT_RUN |
| MT5_STRATEGY_TESTER | NOT_RUN |
| REAL_TRADING_ALLOWED | NO |

## Ограничения

- MetaEditor compile и MT5 Strategy Tester требуют Windows/MT5 окружение и не были выполнены в текущем Linux-контейнере.
- `REAL_TRADING_ALLOWED = NO` до фактических `METAEDITOR_COMPILE = PASS` и `MT5_STRATEGY_TESTER = PASS`.
- Safe defaults сохранены: `UseSplitBigGeometry=false`, `UseLegacySingleBigGeometry=true`, `AllowRealTrading=false`.

## Вердикт

Этап 7 закрывает оставшиеся recovery-safety дефекты: RESET больше не требует FarIdentifier, failure marker сохраняет исходный State и числовую причину без разрушения основного persistence, RecoverState не возвращает success после reconciliation/integrity failure, новые операции блокируются во время recovery, а нулевой рассчитанный Split Harvest Net отделён от отсутствующего расчёта.
