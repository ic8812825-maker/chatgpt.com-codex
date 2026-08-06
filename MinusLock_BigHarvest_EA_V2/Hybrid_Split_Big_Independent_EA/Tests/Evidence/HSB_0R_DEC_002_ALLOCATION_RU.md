# HSBI-DEC-002 — allocation shares

Статус: `DEFERRED_WITH_SAFE_CONTRACT`.

Для каждого положительного allocatable source deal: `ReserveAllocation + PartialAllocation + TransitionAllocation + CarryAllocation + Residual = AllocatableDealNet`. Все доли находятся в `[0,1]`, сумма explicit shares не превышает 1, `ResidualShare=1-ΣExplicitShares`.

Opening `DEAL_ENTRY_IN`, Initial Profit и отрицательный DealNet не распределяются как harvest profit. Каждый bucket хранит SourceDealKey, EventKey, CycleID и доступный/зарезервированный/потреблённый остаток. FinalReserve никогда не финансирует Partial Far. Повторный SourceDealKey — NO-OP; конфликт — RECONCILIATION.

Research allocation допускается только как конфигурация; real default отсутствует. MQL5 owners: `Money/EconomicLedger`, `Money/AllocationLedger`. Тесты: conservation per deal, multi-source conservation, duplicate/conflict, bucket isolation.
