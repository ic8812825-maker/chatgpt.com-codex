# HSB.0R — P2 execution contracts

## Small confirmation

Touch определяется close-side ценой роли SMALL_BASE относительно нормализованного SmallTransitionControlPrice с configurable offset. Требуются два последовательных свежих snapshot после первого touch и minimum retrace/hold condition, заданные конфигурацией. Debounce key = CycleID+PlanID+TransitionLevel; после persisted trigger повторный trigger запрещён.

## Retry

Retry разрешён только для того же ActionID, если action не completed, history и ActionRegistry не показывают order/deal completion, ownership/state revision совпадают и reconciliation вернул PENDING. Новый ActionID для retry запрещён. Duplicate request — CONFLICT.

## Timeout

Каждый action имеет SubmittedAt, LastTransactionAt, MaxPendingDuration и RetryCount. Истечение не считается failure/completion: переход в RECONCILING. После reconciliation outcome PENDING допускается ограниченный retry; CONFLICT/REJECTED ведёт в TERMINAL_SAFE. Market snapshot freshness проверяется перед каждой отправкой.

Manual intervention: freeze opens, persist evidence bundle, show reason/action/identity, require operator acknowledgement; auto-resume запрещён. Owners: Execution/ActionRegistry, FillAccumulator, Scenarios/SmallTransition. Tests: debounce, duplicate tick, placed-without-fill, delayed fill, timeout/restart.
