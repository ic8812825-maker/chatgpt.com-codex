# Спецификация Partial Far

Версия 1.0. Статус: нормативный.

## Закон и расчёт

`FinalReserve` не используется. Единственный источник — `PartialFarBudgetAvailable`.

`CloseLotRaw=PartialFarBudgetAvailable/FarCloseLossPerLot`.
`CloseLot=FloorToBrokerStep(CloseLotRaw)`.
После rounding: `0<=CloseLot<=FarLots` и `ProjectedCloseCost(CloseLot)<=Budget`.

`FarCloseLossPerLot` рассчитывается broker-money моделью на executable close side с commission, swap, fee, slippage/buffer. После actual deal `ActualConsumedBudget=max(0,-ActualDealNet)`; unused reservation освобождается, overrun фиксируется как conflict/cost variance, но не списывается из Reserve.

- `HSBI-PF-001`: FinalReserve отсутствует во входах solver.
- `HSBI-PF-002`: reservation precedes request.
- `HSBI-PF-003`: budget consumption применяется exactly once по ConsumptionKey.
- `HSBI-PF-004`: residual Far равен 0 либо >= volume min.
- `HSBI-PF-005`: Far ticket/identifier continuity сохраняется при partial close.
- `HSBI-PF-006`: full-affordability route передаётся Final Close authority, а не закрывается как Partial.

## Пример

ДЕМОНСТРАЦИОННЫЙ ПРОФИЛЬ: budget=120 money, loss/lot=400 → raw=0.30; step=0.01 → 0.30. Если actual DealNet=-118, consume=118, 2 возвращаются. Если residual 0.005 при min 0.01 — candidate запрещён/маршрутизируется безопасно.

## Restart/errors

Pending reservation, ActionID и accumulated fills сохраняются. Duplicate deal — NO-OP. Mismatch ticket/identifier, over-consume, missing source или partial fill без completion → RECONCILING.

## Контракт

Owner: Scenarios/PartialFar, Money/PartialFarBudget, Execution. Тесты: BUY/SELL, floor, min residual, full-route, partial fill, restart, double consumption. Открытые вопросы: tolerance и positive-deal treatment.