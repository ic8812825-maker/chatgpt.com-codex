# 13. Small Transition и единственный NewFar

Версия HSB.0R-C.14. Статус: нормативный source of truth.

## Trigger confirmation
Close-side touch + repeated fresh snapshot + configurable hold/retrace + persisted DebounceKey + no active transition. Duplicate trigger=NO-OP; stale/conflict→RECONCILIATION.

## Immutable plan и loss caps
TransitionPlan связывает identity, StateRevision, control prices, planned Core reduction и четыре Transition Loss caps. `TransitionLoss=max(0,-ΣActualClosingDealNet)`; allowed=min(absolute,equity,OldFar-risk,cumulative-cycle caps). Failed cap blocks transition before irreversible action.

## Единственный порядок
Revalidation→persist plan→close SMALL_BASE 100%→confirm actual deals→close OldFar 100%→confirm→close BIG_TREND 100%→confirm→close planned BIG_CORE part→confirm all fills→read actual remaining original BIG_CORE→validate all NewFar gates→promote same ticket/identifier→persist next cycle→reconcile→FAR.

Каждый close — отдельная persisted Action. Partial fill, timeout, delayed/unknown event или mismatch блокирует следующий шаг. Retry same ActionID только по transaction contract.

## Инварианты
OldFar/SMALL_BASE/BIG_TREND закрыты; exactly one managed position remains; это original BIG_CORE; `0<N<F`; no DUAL_TAIL; requested residual не используется; следующий basket запрещён до reconciliation.

## Restart/error
Plan, completed ActionIDs, fills, source deals и debounce восстанавливаются. Две позиции, altered identifier, exceeded loss cap или missing deal→CONFLICT/TERMINAL_SAFE/manual review, no auto-resume.

Owner Scenarios/SmallTransition+Planning/NewFarSolver+Execution+Money. Tests: оба направления, false touch, debounce, loss caps, partial/delayed/retry/timeout, every restart point, actual≠requested residual, two consecutive transitions.