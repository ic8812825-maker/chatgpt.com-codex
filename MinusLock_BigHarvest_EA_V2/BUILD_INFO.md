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
