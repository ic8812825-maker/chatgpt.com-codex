# 11. Partial Far

Версия HSB.0R-C.12. Статус: нормативный source of truth.

Единственный источник — PartialFarBudgetAvailable. FinalReserve отсутствует во входах и никогда не потребляется Partial Far.

`CloseLotRaw=Budget/FarCloseLossPerLot`; `CloseLot=FloorToBrokerStep(CloseLotRaw)`. После rounding повторно проверяются `0≤CloseLot≤FarLots`, executable close cost≤reserved budget и residual Far=0 либо ≥Vmin.

Lifecycle: calculate→reserve by SourceDealKey/ConsumptionKey→persist→ownership revalidation→request→OnTradeTransaction→accumulate partial fills→actual completed deal(s)→`ActualConsumed=max(0,-ΣActualDealNet)`→release unused reservation→persist residual Far. Positive DealNet не создаёт автоматическую дополнительную reservation.

Partial fill не завершает action. Retry только same ActionID после history/reconciliation; timeout→RECONCILING. Ticket и PositionIdentifier FAR сохраняются. Mismatch, over-consume, missing source, foreign cycle или duplicate conflict блокируют действие.

BUY Far закрывается по Bid, SELL Far по Ask, costs/swap/commission/buffer включены. Full affordability передаётся единой Final Close authority. Restart восстанавливает reservation, fills и consumption exactly once. Owner Scenarios/PartialFar+Money+Execution. Tests: floor 0.01/coarse step, min residual, BUY/SELL, partial/delayed, retry, restart, no Reserve consumption.