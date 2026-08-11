# 16. Persistence и restart contract

Версия HSB.0R-C.17. Статус: нормативный source of truth.

## Backend
Versioned file snapshot + append-only action/event journal + previous valid snapshot + per-identity lock. Terminal Global Variables допускаются только как минимальные discovery/lock markers. Истинная filesystem atomic rename не заявляется; нормативный термин — crash-consistent versioned commit protocol.

## Snapshot
SchemaVersion, MoneyStateVersion, AccountLogin, Symbol, Magic, CycleID, State, StateRevision, RuntimeMode, immutable Plan, PendingAction/attempts, roles, tickets, identifiers, volumes, prices/control snapshot, EconomicLedgerDigest, AllocationLedgerDigest, EventHistoryDigest, ReconciliationStatus, Timestamp, PreviousCommitID, ChecksumSHA256.

## Canonical commit
Acquire identity lock→canonical serialize→write temp version→SHA-256→flush/close→reread/verify bytes+checksum→append prepared journal record→write commit marker/current pointer→reread marker→retain previous valid version→release lock. Crash at любой точке оставляет либо предыдущий committed snapshot, либо проверяемый candidate; torn temp не становится current.

## Restart
Locate markers→load latest marker→verify schema/checksum/digests→fallback previous valid→load journal→read actual MT5 positions/orders/deals→reconciliation→CLEAN_START/RECONCILED/PENDING/CONFLICT/TERMINAL_SAFE. PendingAction восстанавливается до send/retry.

## Corruption
Unknown schema, checksum mismatch, altered history, lock conflict, inconsistent digests или two-current markers не угадываются: no trading, terminal-safe/manual review. Migration требует отдельной versioned procedure.

Owner Persistence/SnapshotStore/EventStore/Recovery. Tests: crash injection на каждом шаге, corrupted latest/fallback previous, stale snapshot, journal replay, per-identity lock, schema mismatch, altered history.
> **Граница реализации HSB.1V (2026-08-10).** Описанный production lifecycle остаётся нормативной спецификацией, а не реализованным сценарием. В каркасе нет production execution, broker-money runtime и production persistence. Действуют: ровно один Far; promotion только из actual BigCore residual; FinalReserve запрещён для Partial Far; allocations не прибавляются к actual money повторно; Final Close определяется только actual money; только COMPLETED_FILL снимает transaction barrier; retry сохраняет ActionID; conflict ведёт в RECONCILING; unresolved critical error — в TERMINAL_SAFE; no auto-resume; REAL_LIMITED и HSB.2 запрещены.
