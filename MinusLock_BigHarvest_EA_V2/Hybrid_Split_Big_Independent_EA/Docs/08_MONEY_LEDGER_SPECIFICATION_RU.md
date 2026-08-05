# Economic Ledger и Allocation Ledger

Версия 1.0. Статус: нормативный.

## DealNet

`DealNet=DEAL_PROFIT+DEAL_SWAP+DEAL_COMMISSION+DEAL_FEE`. Поля сохраняются с фактическим знаком MT5. Источник — confirmed deal, не projection.

## Economic Ledger

Поля: DealTicket, OrderTicket, PositionIdentifier, Symbol, Magic, CycleID, ActionID, EventID, Role, EntryType, Volume, Price, Profit, Swap, Commission, Fee, DealNet, Timestamp, SourceDealKey.

## Allocation Ledger

Buckets: FinalReserve, PartialFarBudget, TransitionBudget, Carry, Residual. Для каждого source deal:

`ReserveAllocated+PartialAllocated+TransitionAllocated+CarryAllocated+Residual=DealNetAvailableForAllocation`.

`AllocatedTotal<=RealizedSourceTotal`.

- `HSBI-MONEY-010`: opening DEAL_ENTRY_IN не финансирует allocation.
- `HSBI-MONEY-011`: Initial Profit не входит в recovery Economic Ledger.
- `HSBI-MONEY-012`: FinalReserve не финансирует Partial Far.
- `HSBI-MONEY-013`: bucket не прибавляется повторно к RealizedCycleNet.
- `HSBI-MONEY-014`: EventKey, SourceDealKey и ConsumptionKey обеспечивают exactly-once.
- `HSBI-MONEY-015`: identical replay → NO-OP; conflicting replay → reconciliation.
- `HSBI-MONEY-016`: allocation и consumption атомарны относительно persisted revision.

## Restart и ошибки

Ledgers append-only; snapshot хранит digests и last committed event. Altered history, negative unexplained residual, over-allocation или reused source → CONFLICT. Никакие суммы не восстанавливаются из comments.

## Контракт

Вход: actual deals и approved allocation policy. Выход: immutable economic entries и balanced allocations. Preconditions: identity valid, event complete. Postconditions: conservation. Owner: Money/EconomicLedger, AllocationLedger. Тесты: signs, IN/OUT/INOUT/OUT_BY, duplicate, multi-source, restart, fee/swap. Открытые вопросы: production allocation shares и treatment positive PartialFar deal.