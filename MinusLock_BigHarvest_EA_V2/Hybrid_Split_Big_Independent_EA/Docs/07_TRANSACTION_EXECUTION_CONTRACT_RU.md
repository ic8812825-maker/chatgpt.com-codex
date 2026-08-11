# 07. Event-driven transaction execution contract

Версия HSB.0R-C.8. Статус: нормативный source of truth.

## Цепочка
Plan→Action→Persist Action→OwnershipGuard→Send Request→OnTradeTransaction→FillAccumulator→CompletionDecision→Read actual positions/orders/deals→Apply Economic/Allocation Ledger→Persist result→Advance FSM.

## Идентификаторы
CycleID, PlanID, ActionID, ParentActionID, EventID, PositionIdentifier, OrderTicket, DealTicket, StateRevision. EventKey и SourceDealKey обеспечивают idempotency.

## OwnershipGuard
Перед action: AccountLogin, Symbol, Magic, CycleID, Ticket, PositionIdentifier, Role, Direction, ExpectedVolume, ActualVolume, StateRevision, PlanID, ActionID. Mismatch→ACTION_BLOCKED→RECONCILIATION.

## Outcomes
ACCEPTED/PLACED означают pending; DONE_PARTIAL означает incomplete; DONE только кандидат на completion и требует deals+actual state. Reject, requote, no money, invalid volume, market closed, price changed, connection failure типизированы и не продвигают FSM.

## Retry
Только тот же ActionID; completed deal отсутствует; history перечитана; reconciliation=PENDING; state допускает retry; duplicate request исключён; ownership и snapshot повторно валидны. Новая попытка записывается как child attempt с ParentActionID, но экономическое действие остаётся тем же.

## Timeout/delayed events
TIMEOUT не равен failure/completed. Timeout ставит reconciliation barrier. Delayed transaction обрабатывается по EventKey; identical duplicate=NO-OP; конфликт того же key→CONFLICT→TERMINAL_SAFE. FillAccumulator суммирует volume и DealNet до exact completion criterion.

## Restart
PendingAction и attempts восстанавливаются до любых новых request; сначала history/positions/orders reconciliation. Owner Execution/TransactionEngine, ActionRegistry, FillAccumulator, OwnershipGuard. Tests: partial, duplicate, delayed, timeout, retry, crash between every phase.
> **Граница реализации HSB.1V (2026-08-10).** Описанный production lifecycle остаётся нормативной спецификацией, а не реализованным сценарием. В каркасе нет production execution, broker-money runtime и production persistence. Действуют: ровно один Far; promotion только из actual BigCore residual; FinalReserve запрещён для Partial Far; allocations не прибавляются к actual money повторно; Final Close определяется только actual money; только COMPLETED_FILL снимает transaction barrier; retry сохраняет ActionID; conflict ведёт в RECONCILING; unresolved critical error — в TERMINAL_SAFE; no auto-resume; REAL_LIMITED и HSB.2 запрещены.
