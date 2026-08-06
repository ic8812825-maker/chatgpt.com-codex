# 09. Initial Lock и создание исходного Far

Версия HSB.0R-C.10. Статус: нормативный source of truth.

## Identity и scope
Каждая leg связана с AccountLogin+Symbol+Magic+CycleID+PositionIdentifier+Role. Generation 1 допускает один активный cycle на Symbol+Magic. Comment не является source of truth.

## Последовательность
1. Clean-start reconciliation подтверждает отсутствие managed positions/orders/pending actions.
2. Создать immutable InitialPlan и persist BUY Action.
3. Отправить BUY, дождаться OnTradeTransaction и actual fill; partial fill остаётся pending.
4. Persist SELL Action, отправить SELL, дождаться actual fill.
5. Если SELL не завершён, выполнить отдельный rollback BUY action; до actual rollback deal цикл не считается чистым.
6. После trigger определить прибыльную leg broker-money моделью.
7. Persist close INITIAL_PLUS; FSM не продвигается на request/PLACED/DONE_PARTIAL.
8. Только после completed close deal пометить Initial Profit excluded.
9. Actual remaining position с неизменным identifier назначается FAR и snapshot commit.

## Exclusion
Initial Profit не входит в RealizedCycleNet, FinalReserve, PartialFarBudget, TransitionBudget или Carry. Opening DEAL_ENTRY_IN не является harvest source.

## Retry/timeout
Retry использует тот же ActionID только после history recheck, reconciliation=PENDING и отсутствия completed deal. Timeout ведёт в reconciliation; delayed event обрабатывается idempotently.

## Restart/error
Restart восстанавливает Plan, PendingAction, fills и actual positions. Два Far, missing leg, foreign identity или восстановление только по comment запрещены и ведут terminal-safe/manual review.

Preconditions: fresh market, valid lot, risk PASS, IDLE. Postconditions: ровно один FAR, initial plus excluded, no pending. Owner: Scenarios/InitialLock+Execution. Tests: обе стороны, rollback, partial/delayed fill, retry, timeout, restart на каждом шаге.