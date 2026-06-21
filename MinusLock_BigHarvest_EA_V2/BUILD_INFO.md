# MinusLock BigHarvest EA V2 Build Info

Build date: 2026-06-18 UTC
Branch: work
Target folder: MinusLock_BigHarvest_EA_V2
Commit purpose: V2.4.1 RiskGate lifecycle, real BigHarvest reserve, retry pending states, recovery reconciliation and defaults

Included features:
- Initial BUY/SELL lock with rollback
- Initial profit ignored
- Big-Harvest
- Small-at-Far V2.4
- Risk Compression Reverse
- New Big < Old Far rule
- SmallReserveShare reserve add
- FarDistanceMode
- REAL_PRICE_DISTANCE
- EffectiveFarDistancePoints
- Cycle Math CSV report
- Reverse Geometry Validator
- STOP_MAX_LEVELS / UNCLOSED_CYCLE
- Reverse limit close-new-Far handling
- Invalid geometry emergency handling
- Retry FSM state definitions
- Restart recovery through GlobalVariables
- Internal SIMULATION engine
- Real Recovery P/L Validation
- REAL_CYCLE_MATH log and CSV fields


V2.4.1 updates:
- RiskGate blocks only new openings; closes and retry/pending states continue even when spread is high.
- Pending close states have retry handlers with MaxCloseRetryAttempts and RetryLogIntervalSeconds.
- BigHarvest reserve and CloseFarBudget use real HistoryDeals net P/L when available.
- RecoverState persists/reconciles extra context and real open positions after restart.
- Spread blocked logs are throttled with RiskGateLogIntervalSeconds.
- Defaults updated: CloseFarShare=0.40, ReserveShare=0.60, MaxReverseCycles=7, MaxSpreadPoints=60.0.


V2.4.2 updates:
- Pending FSM now stores pendingOperation/pendingNextState/pendingTicket/pendingLot/pendingAttempts.
- Retry continues to the next scenario phase instead of restarting BigHarvest or Small Scenario.
- BigHarvest and Small Scenario phase states added.
- STATE_OPEN_NEW_BIG_PENDING and STATE_OPEN_NEW_SMALL_PENDING have handlers.
- BigHarvest reserve is calculated by matching closed Big/Small HistoryDeals via DEAL_POSITION_ID.
- SmallScenarioRealNet uses real before/after delta.
- Recovery persistence and diagnostics expanded.


V2.4.3 updates:
- ProcessBigHarvest, ProcessSmallAtFarTouch and ProcessSmallScenario are thin phase-FSM proxies only.
- Added ProcessBigHarvestCloseBig as the atomic Big close phase.
- Small Scenario starts from ProcessSmallCloseSmall and proceeds through atomic phases.
- Retry close success clears closed Big/Small/Far context.
- OPEN_NEW_*_PENDING states perform actual open retry attempts.
- Startup order is ConfigureWorkingParameters -> ValidateInputs -> ValidateWorkingParameters -> ValidateFSMIntegrity.
- FSM integrity check added at startup.

V2.4.5 updates:
- Terminal states are separated from OPEN_NEW_*_PENDING and only break.
- savedSmallDirection/savedSmallClosePrice/savedSmallTouchPrice/savedSmallOpenPrice/savedSmallLot added and persisted.
- oldFarTicket/oldFarLot/oldFarDirection/oldFarOpenPrice added and persisted.
- ProcessSmallBuildNewFar uses saved Small context and fails if savedSmallDirection is DIR_NONE.
- ProcessSmallCloseOldFar saves old Far and clears active Ctx.far* after close.
- Strict FSM safety tests added.

## V2.4.6 MaxHarvestLevels Final Decision
- Added `CloseFarOnMaxLevels=true` as the default safety policy for the last allowed harvest level.
- Added explicit `STATE_MAX_LEVELS_DECISION` and `STATE_STOP_MAX_LEVELS_CLOSE_PENDING` so the residual Far is either final-closed, stop-closed, or routed to manual intervention with a full `[MAX_LEVELS_DECISION]` log.
- RiskGate continues to block only new Big/Small openings; it does not block MaxHarvestLevels residual-Far closing.

## V2.4.7 Retry Partial Far and Closed-Profit Guard
- Added `PendingActionType` so retry cleanup no longer infers operation type from `pendingOperation` text.
- Partial Far retry now preserves `farTicket`, `farDirection`, and `farOpenPrice` and only reduces `farLot` by the retried lot.
- Added persisted reserve-applied flags and `pendingSmallReserveAdd` to prevent repeated reserve application after restart/retry.
- Added a runtime guard that blocks `STATE_CLOSED_PROFIT` while managed positions are still open.
- Real-deal matching now uses `POSITION_IDENTIFIER` stored in `PositionSnapshot.identifier` for `DEAL_POSITION_ID` comparisons.

## V2.4.8 Reconciliation Engine
- Added `Include/ReconciliationEngine.mqh` with startup and periodic checks comparing `RecoveryContext` against MT5 positions and history.
- Added `STATE_RECOVERY_MISMATCH`, `ReserveMismatchTolerance`, and `ReconciliationIntervalSeconds`.
- Added Far/Big/Small ticket, identifier, direction and volume validation plus reserve rebuild diagnostics from HistoryDeals.

## V2.4.9 Reconciliation Soft Volume Sync
- Added `NormalizeVolumeToStep()` as the shared volume normalization helper for reconciliation checks.
- Reconciliation now compares normalized context/actual volumes and uses `RECON_TOLERANCE_USED` diagnostics.
- V2.4.10 supersedes one-step auto-sync: normal Small Reverse writes actual MT5 volume before reconciliation, and remaining lot mismatches use `VolumeMismatchToleranceLots`.
- Reserve rebuild now classifies positive closed recovery deals by Magic/Symbol/DEAL_ENTRY_OUT when broker close comments are blank.

## V2.4.9 P0 Reserve Ledger / Reconciliation Fix

- Reserve reconstruction no longer treats every profitable HistoryDeal as reserve; Initial Lock profit is explicitly skipped and logged as `RESERVE_REBUILD_SKIP_INITIAL_LOCK`.
- Reserve changes are routed through `ApplyReserveCredit()` / `ApplyReserveDebit()` and recorded in `ReserveLedgerEntry` rows for deterministic rebuild.
- Reserve mismatch is now diagnostic (`RECONCILIATION WARNING RESERVE_REBUILD_UNVERIFIED`) and does not enter `STATE_RECOVERY_MISMATCH` unless structural position reconciliation also fails.
- Periodic reconciliation stops repeating full checks after a fatal `STATE_RECOVERY_MISMATCH` and emits a single repeat warning instead of flooding logs.

## V2.4.10 P0 Actual Volume After Small Reverse

- New Far volume after Small Reverse is now read from the actual remaining MT5 position via `GetActualPositionVolume()` instead of synthetic `CalcRemainBigLotOnSmall()` math.
- `ProcessSmallCloseBigPart()` logs `BIG_PARTIAL_CLOSE_VERIFY` with expected, actual and difference values after partial Big close.
- Added `VolumeMismatchToleranceLots` for lot-volume integrity; `ReserveMismatchTolerance` remains money-only.
- `RecoverState()` reconciliation now overwrites saved leg volume with actual terminal volume and logs SavedVolume/ActualVolume.
- `GetEffectiveLotStep()` prefers broker `SYMBOL_VOLUME_STEP` and logs `LOT_STEP_OVERRIDE_WARNING` if user `LotStep` differs.

## V2.4.11 P0 Actual Volume After Every Partial Close

- BigHarvest Far partial close now refreshes `Ctx.farLot` from actual terminal `POSITION_VOLUME` via `RefreshFarVolumeFromTerminal()` instead of `oldLot - closeLot` math.
- Partial-close retry paths for Big and Far use `RefreshBigVolumeFromTerminal()` / `RefreshFarVolumeFromTerminal()`; theoretical `Ctx.*Lot - Ctx.retryLot` updates are removed.
- Full Far closes verify actual remaining volume; if MT5 still reports volume, the EA logs `FULL_CLOSE_INCOMPLETE` and keeps/re-enters retry pending instead of clearing context.
- Added `RefreshLegVolumeFromTerminal()` plus `ClearFarContext()`/leg clear helpers to centralize volume refresh and cleanup.

## V2.4.12 P0 Full Close Integrity

- Added `IsPositionFullyClosed()` and `VerifyFullClose()` so full closes are confirmed only by `POSITION_VOLUME <= VolumeMismatchToleranceLots`, never by `SYMBOL_VOLUME_MIN` or broker min lot.
- Full Far close paths now verify zero actual terminal volume before `ClearFarContext()`; otherwise they log `FULL_CLOSE_INCOMPLETE` and keep/re-enter retry pending.
- `STATE_CLOSED_PROFIT` now checks managed positions, leg context, and `VerifyFullClose()` for non-zero leg tickets before allowing terminal profit state.
- Reconciliation now logs `CONTEXT_CLEARED_WITH_LIVE_POSITION` and routes to `STATE_RECOVERY_MISMATCH` when context says all legs are gone but managed MT5 positions still exist.

## V2.4.13 P0 Reconciliation Integrity: Orphan Position Protection

- Added `ValidateNoOrphanManagedPositions()` to scan all managed MT5 positions by MagicNumber/Symbol and require ownership by Far, Big, Small, pending ticket, retry ticket, or stored position identifier.
- Orphan positions now log `ORPHAN_MANAGED_POSITION DETECTED` with ticket, identifier, volume, direction, and comment, then force `STATE_RECOVERY_MISMATCH`.
- The orphan guard runs after close paths, after `RecoverState()`, and during/after reconciliation so partial context loss cannot hide live managed exposure.

## V2.4.15 P0 Initial Lock Recovery Architecture

- Added Initial Lock legs to `RecoveryContext` with tickets, identifiers, lots, open prices, and `initialLockRecovered` diagnostics.
- `OpenInitialLock()` registers Initial BUY/SELL context immediately; `RecoverState()` restores or rebuilds Initial Lock state after restart; `CheckInitialPlusClose()` converts the remaining Initial leg into Far and clears Initial context.
- Reconciliation now includes `ValidateInitialLockIntegrity()` and `ValidateStatePositionConsistency()`, and orphan protection treats Initial BUY/SELL as owned managed positions.

## V2.4.17 P0 Known Context Architecture

- Added centralized `HasKnownContext()` and leg-specific context helpers for Initial BUY/SELL, Far, Big, Small, pending, and retry objects.
- Replaced the cleared-context reconciliation guard with `!HasKnownContext() && CountManagedOpenPositions() > 0`.
- Added `KNOWN_CONTEXT_PRESENT`, `RECOVERY_CONTEXT_RESTORED`, and `RECONCILIATION_CONTEXT_SUMMARY` diagnostics so startup and reconciliation show the complete context shape before trading logic proceeds.

## V2.4.17 Full Phase-State Integrity Validation
- Added `Include/StateIntegrityEngine.mqh` with `ValidateCurrentStateIntegrity()` and a formal FSM state-shape matrix.
- Added terminal `STATE_INTEGRITY_ERROR` for states whose required positions, forbidden positions, pending context, or retry context do not match the current FSM phase.
- Runtime validation now runs after recovery, reconciliation, and `SetState()` transitions so phase states are checked before trading continues.
- New diagnostics: `STATE_INTEGRITY_PASS`, `STATE_INTEGRITY_FAIL`, `EXPECTED_POSITION_MISSING`, `UNEXPECTED_POSITION_PRESENT`, `INVALID_PENDING_CONTEXT`, `INVALID_RETRY_CONTEXT`, and `INVALID_STATE_SHAPE`.
