# Reconciliation и terminal-safe

Версия 1.0. Статус: нормативный.

Источники истины по приоритету: actual MT5 positions, orders, deals; committed snapshot; event/action ledgers. Comments — только диагностика.

Outcomes: `RECONCILED, PENDING, CONFLICT, REJECTED, TERMINAL_SAFE, CLEAN_START`.

- `HSBI-RECON-001`: reconciliation не создаёт новую корзину.
- `HSBI-RECON-002`: Far не угадывается и один из двух Far не выбирается автоматически.
- `HSBI-RECON-003`: missing deal не считается completed.
- `HSBI-RECON-004`: duplicate money event не начисляется повторно.
- `HSBI-RECON-005`: altered history/source ownership → CONFLICT.
- `HSBI-RECON-006`: до RECONCILED/CLEAN_START новые opens запрещены.
- `HSBI-RECON-007`: TERMINAL_SAFE запрещает promotion/allocation/opens; разрешённые protective closes определяются отдельной emergency policy.

Проверяются Symbol, Magic, CycleID, role, ticket, identifier, direction, volume, StateRevision, pending ActionID, fill totals, ledgers и digests. Orphan/missing/duplicate Far, unknown deal, conflicting snapshot и manual intervention регистрируются явно.

Контракт: вход — snapshot и actual facts; выход — typed outcome + diff + reason codes. Preconditions: history range доступен. Postconditions: reconciled state точно соответствует MT5. Restart: reconciliation обязательна. Owner: Persistence/Reconciliation. Тесты: every mismatch class, manual close, delayed deal, duplicate Far, foreign positions. Открытые вопросы: retry/timeouts и allowed protective actions.