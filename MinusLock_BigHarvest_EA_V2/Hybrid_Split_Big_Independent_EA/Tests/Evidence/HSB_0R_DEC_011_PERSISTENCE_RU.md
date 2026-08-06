# HSBI-DEC-011 — persistence backend

Статус: `RESOLVED`.

Generation 1 использует versioned files в FILE_COMMON либо утверждённом FILE_DATA namespace, append-only event/action journal и Terminal Global Variables только как минимальные recovery markers. Source of truth — последний полностью подтверждённый snapshot commit плюс journal и actual MT5 history.

Формат: UTF-8 JSON-lines journal и versioned snapshot document; имена включают AccountLogin, Symbol, Magic, CycleID, SchemaVersion. Commit protocol: write `.tmp` → canonical serialize → SHA-256 checksum → flush/close → reread/verify → promote commit marker/index → retain previous valid snapshot. Lock: per-identity lock file with owner token and expiry; stale lock требует reconciliation.

При corruption: current rejected, previous valid loaded only как candidate, затем reconciliation с positions/orders/deals; auto-trading blocked. Owner: `Persistence/SnapshotStore`, `EventStore`, `Recovery`. Tests: torn write, checksum, stale lock, previous fallback, multi-symbol isolation.
