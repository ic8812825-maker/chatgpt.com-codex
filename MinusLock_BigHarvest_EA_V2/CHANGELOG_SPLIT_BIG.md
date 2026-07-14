# CHANGELOG Split Big

## 2026-07-14

Status: **SPLIT BIG IMPLEMENTED** / **SPLIT SMALL NOT IMPLEMENTED**.

- Safe defaults restored: Legacy enabled, Split disabled, real trading disabled.
- Added Split Big route from `STATE_FAR_ACTIVE`.
- Added `PrepareSplitBigLevel()` from actual Far lot.
- Added BigCore, SmallBase and BigTrend role opening.
- Added rollback paths for SmallBase and BigTrend opening failures.
- Added Big target from BigCore open price.
- Added separate full-close states for BigCore, BigTrend and SmallBase.
- Added Split lifecycle net by position identifiers with symbol/magic isolation.
- Added immediate full Far check before partial.
- Added partial Far budget/carry handling and Reserve credit after partial/skip.
- Added local pytest suites for unit/static/scenario behavior.
- Added Split Big-only set files.

Limitations:

- Split Small / DynamicReverseSmall is not implemented.
- MetaEditor and Strategy Tester were not run in the Linux container.

## 2026-07-14 — Architecture integrity fix

- Added dedicated Split pending states and Split max-level decision state.
- Split StateIntegrity now validates BigCore, BigTrend and SmallBase instead of legacy Big/Small.
- PositionResolution now resolves Split roles by ticket, identifier, role comment/CycleId/Level and time-window fallback.
- Reconciliation now recognizes Split topologies and does not classify valid Split roles as orphan positions.
- Split pending/retry contracts now cover open and close paths for Split roles and Far partial/full close.
- Partial Far carry now uses actual history deals when available; missing history routes to `STATE_SPLIT_PARTIAL_HISTORY_PENDING`.
- Full Far close uses `SPLIT_FINAL_CLOSE_PROFIT` and clears Split context before `STATE_CLOSED_PROFIT` guard.
- Added architecture pytest coverage for topology, restart/idempotency, reserve persistence, partial actual accounting, pending and multicurrency isolation.

Status remains: **SPLIT BIG IMPLEMENTED**, **SPLIT SMALL NOT IMPLEMENTED**, **REAL_TRADING_ALLOWED = NO** until MT5 compile/tester confirmation.
