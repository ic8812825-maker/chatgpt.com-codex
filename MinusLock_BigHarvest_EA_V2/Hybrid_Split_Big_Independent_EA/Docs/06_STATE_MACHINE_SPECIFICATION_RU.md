# 06. State Machine Hybrid Split Big

Версия HSB.0R-C.7. Статус: нормативный source of truth.

## Состояния
STATE_DISABLED, IDLE, INITIAL_PLAN_READY, INITIAL_OPENING_BUY, INITIAL_OPENING_SELL, INITIAL_LOCK_ACTIVE, INITIAL_PLUS_CLOSING, FAR_ACTIVE, CANDIDATE_PLANNED, BASKET_OPENING_CORE, BASKET_OPENING_TREND, BASKET_OPENING_SMALL, BASKET_ACTIVE, BIG_HARVEST_PLANNED, BIG_HARVEST_EXECUTING, ALLOCATION_PENDING, FINAL_CLOSE_PLANNED, FINAL_CLOSE_EXECUTING, PARTIAL_FAR_PLANNED, PARTIAL_FAR_EXECUTING, SMALL_CONFIRMING, SMALL_TRANSITION_PLANNED, SMALL_CLOSING, OLD_FAR_CLOSING, BIG_TREND_CLOSING, BIG_CORE_REDUCING, NEW_FAR_VALIDATING, ACTION_REQUEST_SENT, ACTION_ORDER_PENDING, ACTION_PARTIAL_FILL, ACTION_RETRY_PENDING, RECONCILING, EMERGENCY, MANUAL_REVIEW, TERMINAL_SAFE, CYCLE_CLOSED.

## Главный инвариант
REQUEST_SENT≠ACTION_COMPLETED; PLACED≠COMPLETED; DONE_PARTIAL≠COMPLETED; TIMEOUT≠FAILURE; TIMEOUT≠COMPLETED. FSM меняется только после подтверждённого transaction outcome, actual position read, ledger application и persisted result.

## Переход action
Planned→Persisted→RequestSent→OrderPending/PartialFill→Completed→PostconditionVerified→PersistedResult→NextState. Reject/requote/timeout/delayed mismatch→RECONCILING. Retry pending сохраняет тот же ActionID.

## Small
BASKET_ACTIVE→SMALL_CONFIRMING только при fresh repeated snapshot и debounce. Затем immutable plan→последовательные closing states. Partial fill не разрешает переход к следующей роли.

## Emergency
Любой critical identity/persistence/margin/unknown-position conflict→EMERGENCY→TERMINAL_SAFE/MANUAL_REVIEW. Автоматический resume запрещён.

## Restart
Каждое состояние задаёт допустимые роли, PendingAction, PlanID, StateRevision и timeout. Restart сначала reconciliation; угадывание состояния запрещено. Owner Core/StateMachine; tests: reachability, forbidden transitions, delayed/duplicate/partial/retry/restart.
> **Граница реализации HSB.1V (2026-08-10).** Описанный production lifecycle остаётся нормативной спецификацией, а не реализованным сценарием. В каркасе нет production execution, broker-money runtime и production persistence. Действуют: ровно один Far; promotion только из actual BigCore residual; FinalReserve запрещён для Partial Far; allocations не прибавляются к actual money повторно; Final Close определяется только actual money; только COMPLETED_FILL снимает transaction barrier; retry сохраняет ActionID; conflict ведёт в RECONCILING; unresolved critical error — в TERMINAL_SAFE; no auto-resume; REAL_LIMITED и HSB.2 запрещены.
