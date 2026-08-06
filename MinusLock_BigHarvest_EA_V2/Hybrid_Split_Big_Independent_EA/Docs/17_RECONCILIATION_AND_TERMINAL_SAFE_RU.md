# 17. Reconciliation и terminal-safe recovery routes

Версия HSB.0R-C.18. Статус: нормативный source of truth.

Источники истины: actual MT5 positions, orders, deals; committed versioned snapshot; append-only action/event/economic/allocation ledgers. Comment — только диагностика.

Outcomes: RECONCILED, PENDING, CONFLICT, REJECTED, TERMINAL_SAFE, CLEAN_START.

Проверяются AccountLogin, Symbol, Magic, CycleID, role, ticket, identifier, direction, actual volume, StateRevision, PlanID, PendingAction/ActionID, expected/actual fills, SourceDeal/Event/Consumption keys, ledgers/digests и control snapshot.

## Обязательные routes
- pending timeout: history recheck→PENDING/CONFLICT, не failure/completed;
- delayed transaction: применить idempotently к тому же ActionID;
- duplicate event: identical NO-OP, different payload CONFLICT;
- partial fill: action остаётся pending, следующий FSM step запрещён;
- retry: same ActionID после reconciliation=PENDING;
- altered history/source: CONFLICT;
- corrupted snapshot: previous valid candidate либо TERMINAL_SAFE;
- two-Far: не выбирать автоматически, TERMINAL_SAFE/manual review;
- missing/unknown position/deal: REJECTED/CONFLICT;
- manual intervention: explicit diff/reason, no silent adoption.

Reconciliation не создаёт корзину, не назначает NewFar, не распределяет деньги повторно и не считает missing deal выполненным. До RECONCILED/CLEAN_START opens запрещены. После critical error автоматический resume запрещён; только explicit administrator decision после нового reconciliation.

Owner Persistence/Reconciliation+Execution metadata. Tests: все mismatch classes, delayed/duplicate/partial/retry/timeout, manual close, altered history, corruption, two Far, unknown foreign position.