# R12A-UNBLOCK — normative Ledger / Batch / Fill contract

## Scope and decision boundary

This document defines the **new R12A static qualification contract only**. It does not reinterpret historical R10/R11/R12 roots, alter production accounting, or prove broker authenticity.

## Decision 1: persisted ledger

`Ledger = ordered set of LedgerEntry` for all consumed execution records of the state snapshot.

`LedgerEntry` has exactly: `dealId`, `eventId`, `positionTicket`, `intentId`, `volume`, `price`, `direction`, `symbol`, `magic`, `timestamp`, `transactionId`, `actionId`, `stateRevision`, `snapshotRevision`, `confirmed`.

Canonical ordering is `dealId ASC` using Unicode code-point order. `dealId` and `eventId` are unique. Input record order is non-normative.

Canonicalization version `R12A-LEDGER-1` is UTF-8 JSON: an object `{version,entries}` with keys lexicographically sorted, array in canonical order, no insignificant whitespace. Strings are Unicode NFC; integers/timestamps are base-10 with no leading `+` or zeroes; decimal values are normalized decimal plain notation (trailing fractional zeroes removed; `-0` becomes `0`); booleans are JSON `true`/`false`; null and empty strings are forbidden for entry identity fields.

`authoritativeLedgerRoot = SHA-256(UTF8(canonicalLedger))`. The R12A oracle is a standalone canonicalizer, not a production helper.

## Decision 2: batch atomicity

Phases are `PRE_COMMIT`, `COMMITTING`, `COMMITTED`, `ROLLED_BACK`, `FAILED`, `PARTIAL`.

For this predicate, `PRE_COMMIT` is **NOT_APPLICABLE** only when deals/events are empty. `COMMITTING`, `COMMITTED`, and `PARTIAL` have a batch identity `(transactionId, actionId)` and require observed records to share it. `ROLLED_BACK` and `FAILED` require no settled deals/events.

A full atomic commit requires a one-to-one set equality of expected intent IDs and observed deal intent IDs, unique deals/events, no foreign transaction/action, and all observed records confirmed. `PARTIAL` is not atomic and therefore fails this predicate. A replay is not a new batch: its deal IDs must already be consumed.

## Decision 3: per-ticket fill

`PARTIAL_FILL_ALLOWED`. One intent may have multiple deals. `filledVolume = Σ volumes of unique valid deals bound to the intent and its positionTicket`; `remainingVolume = requestedVolume - filledVolume`.

All fill volumes must be positive and on `broker.volumeStep`. Tolerance is exactly zero after decimal grid normalization. `0 <= filledVolume <= requestedVolume`; overfill, duplicate deal/event, wrong intent, wrong ticket and off-grid fill fail. Exact settlement is required only by the batch-atomicity full-commit rule; partial state remains valid for fill accounting but is not atomic commit.
