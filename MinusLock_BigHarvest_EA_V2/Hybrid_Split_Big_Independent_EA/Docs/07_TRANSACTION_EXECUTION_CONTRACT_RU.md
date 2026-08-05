# Transaction Execution Contract

Версия 1.0. Статус: нормативный.

## Цепочка

`Plan → Action → Persist Action → Send Request → OnTradeTransaction → Accumulate fills → Confirm completion → Read actual position → Apply ledgers → Persist result → Advance FSM`.

## IDs и ownership

CycleID, PlanID, ActionID, EventID, ParentActionID, PositionIdentifier, OrderTicket, DealTicket обязательны. Перед action OwnershipGuard проверяет Symbol, Magic, CycleID, ticket, identifier, role, direction, expected/actual volume, StateRevision, PlanID и ActionID.

- `HSBI-TX-001`: `PLACED` не completed.
- `HSBI-TX-002`: `DONE_PARTIAL` не completed; fills накапливаются до target либо terminal outcome.
- `HSBI-TX-003`: один ActionID имеет один commit outcome.
- `HSBI-TX-004`: duplicate identical event → NO-OP; conflicting same key → CONFLICT.
- `HSBI-TX-005`: opening `DEAL_ENTRY_IN` не является harvest source.
- `HSBI-TX-006`: state advance до actual deal запрещён.
- `HSBI-TX-007`: reject, requote, timeout, no money, invalid volume, market closed, price changed и connection failure имеют typed reason codes.

## Partial fills и restart

FillAccumulator хранит requested, cumulative filled, VWAP, deals и fees. После restart pending Action восстанавливается из snapshot и history; повторная отправка запрещена до reconciliation. Unknown deal блокирует новые actions.

## Контракт

Вход: immutable Action и fresh execution snapshot. Выход: typed PENDING/COMPLETED/REJECTED/CONFLICT outcome. Preconditions: ownership PASS, no other pending, persisted StateRevision. Postconditions: actual position and ledgers согласованы. Error route: RECONCILING/TERMINAL_SAFE. Owner: Execution/TransactionEngine, ActionRegistry, FillAccumulator, OwnershipGuard. Тесты: all retcodes, delayed/duplicate/out-of-order events, partial fills, restart. Открытые вопросы: retry policy и broker-specific OUT_BY.