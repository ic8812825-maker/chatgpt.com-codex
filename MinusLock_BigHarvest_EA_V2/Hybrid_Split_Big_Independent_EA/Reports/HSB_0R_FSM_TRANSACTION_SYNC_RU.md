# Синхронизация FSM, transaction, persistence и reconciliation

Нормативное дополнение к Docs/06, 07, 16, 17 и 18.

- FSM advance разрешён только после completed transaction outcome и проверки actual position state.
- `PLACED`, accepted и `DONE_PARTIAL` не завершают Action.
- PendingAction содержит CycleID, PlanID, ActionID, ParentActionID, StateRevision, expected identity/volume, SubmittedAt, retry/timeout fields.
- `OnTradeTransaction` накапливает fills по ActionID; ledger применяется exactly-once после ownership and completion reconciliation.
- Retry сохраняет ActionID и возможен только после history/reconciliation proof отсутствия исполнения.
- Timeout ведёт в STATE_RECONCILING, а не автоматически в failure или retry.
- Snapshot backend: versioned file + SHA-256 + previous valid + append-only journal; Global Variables — markers only.
- Restart priority: actual positions/orders/deals + snapshot + journal. Outcomes: RECONCILED, PENDING, CONFLICT, REJECTED, TERMINAL_SAFE, CLEAN_START.
- Emergency states отделены от profitable close; после critical error opening и auto-resume запрещены.
- Reconciliation не назначает Far, не создаёт basket и не угадывает роль по comment.

Будущие owners: Core/StateMachine, Execution/TransactionEngine, Persistence/SnapshotStore, Persistence/Reconciliation. Production-код не создан.
