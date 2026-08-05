# Persistence и restart contract

Версия 1.0. Статус: нормативный.

## Versioned snapshot

Поля: SchemaVersion, MoneyStateVersion, CycleID, State, StateRevision, RuntimeMode, immutable Plan, PendingAction, roles, tickets, identifiers, volumes, prices, Economic/Allocation/Event digests, reconciliation status, timestamp, checksum.

## Commit protocol

write temp → compute checksum → flush → verify readback → atomic promote current → retain previous valid snapshot. Terminal Global Variables могут хранить индексы/locks, но не являются единственным атомарным store без commit protocol.

- `HSBI-PERSIST-001`: snapshot commit атомарен относительно StateRevision.
- `HSBI-PERSIST-002`: pending action сохраняется до send request.
- `HSBI-PERSIST-003`: previous valid snapshot сохраняется для recovery.
- `HSBI-PERSIST-004`: corrupted/unknown schema не угадывается; система terminal-safe.
- `HSBI-PERSIST-005`: ledger/event digests сверяются с actual history.
- `HSBI-PERSIST-006`: clean start требует отсутствие snapshot, managed facts и pending records.

## Restart

Всегда: load latest valid → verify checksum/version → load previous if latest torn → read actual positions/orders/deals → run reconciliation → only then choose CLEAN_START/RECONCILED/PENDING/CONFLICT. Restart поддерживается на каждом FSM state, включая partial fills и allocation pending.

## Контракт

Вход: committed state/events и actual MT5 facts. Выход: validated recovery candidate. Preconditions: exclusive project namespace. Postconditions: no state advance before reconciliation. Owner: Persistence/SnapshotStore/EventStore/Recovery. Тесты: crash each write phase, checksum corruption, schema migration, stale snapshot, altered history. Открытое решение: backend (Common files/Files/database-like append log) и retention.