# 08. Economic Ledger и Allocation Ledger

Версия HSB.0R-C.9. Статус: нормативный source of truth.

## DealNet
`DealNet=DEAL_PROFIT+DEAL_SWAP+DEAL_COMMISSION+DEAL_FEE`. Поля сохраняются отдельно со знаком MT5. Source truth — actual closing deals.

## Economic Ledger
Поля: DealTicket, OrderTicket, PositionIdentifier, AccountLogin, Symbol, Magic, CycleID, PlanID, ActionID, EventID, Role, EntryType, Volume, Price, Profit, Swap, Commission, Fee, DealNet, Timestamp, SourceDealKey. Opening DEAL_ENTRY_IN и Initial Profit не создают harvest allocation.

## Allocation Ledger
Buckets: FinalReserve, PartialFarBudget, TransitionBudget, Carry, Residual. Shares configuration в [0,1]; после округления money per-source: `Reserve+Partial+Transition+Carry+Residual=AllocatableDealNet`. `AllocatedTotal≤RealizedSourceTotal`. Negative DealNet учитывается Economic Ledger, но allocatable amount=0, если отдельно не утверждён loss-consumption contract.

## Keys/exactly-once
SourceDealKey связывает source; EventKey идентифицирует transaction event; ConsumptionKey связывает consumption с bucket/source/action. Identical replay=NO-OP. Same key different payload=CONFLICT→RECONCILIATION. Foreign cycle/source consumption запрещено.

## Isolation
FinalReserve никогда не потребляется Partial Far. PartialFarBudget не используется Final Close, если не перечислен как explicitly allowed final source. TransitionBudget только для Transition Loss. Carry сохраняет источник. Residual остаётся нераспределённым.

## Transition и Final Close
`TransitionLoss=max(0,-ΣActualClosingDealNet)` и ограничивается четырьмя caps. Final Close использует `RecoveryPLCloseNow` без повторного добавления buckets; threshold включает minimum+buffer+tolerance. Emergency accounting имеет отдельный reason и не маркируется recovery profit.

## Reservation/restart
Allocation и consumption проходят reserve→persist→actual event→consume/release→persist. Crash восстанавливается по ledgers, journal и actual history. Owner Money/EconomicLedger/AllocationLedger. Tests: per-source positive/negative/residual, duplicates, conflicts, restart, FinalReserve isolation.
> **Граница реализации HSB.1V (2026-08-10).** Описанный production lifecycle остаётся нормативной спецификацией, а не реализованным сценарием. В каркасе нет production execution, broker-money runtime и production persistence. Действуют: ровно один Far; promotion только из actual BigCore residual; FinalReserve запрещён для Partial Far; allocations не прибавляются к actual money повторно; Final Close определяется только actual money; только COMPLETED_FILL снимает transaction barrier; retry сохраняет ActionID; conflict ведёт в RECONCILING; unresolved critical error — в TERMINAL_SAFE; no auto-resume; REAL_LIMITED и HSB.2 запрещены.
