# 05. Геометрическая модель и контрольные цены

Версия HSB.0R-C.6. Статус: нормативный source of truth.

## Typed control prices
Каждый объект содержит Price, Bid, Ask, Side, TickSize, Digits, Timestamp, MaxAge, SourceSnapshotID.
- CurrentClosePrice: BUY→Bid, SELL→Ask.
- NextBigControlPrice: уровень следующего Big proof.
- SmallTransitionControlPrice: close-side цена подтверждения Small.
- AdverseRiskControlPrice: adverse money-risk boundary.
- GapStressPrice: gap scenario.
- FinalClosePrice: свежая цена немедленного закрытия.
Stale, nonfinite, wrong-side или off-grid price блокирует решение.

## Broker grid
`NormalizePrice=round(price/TickSize)×TickSize`; points переводятся в price через SYMBOL_POINT, но tick size имеет приоритет валидности. Lots используют min/max/step отдельно.

## Big levels
`DistanceBig(k)=BigMoveStartPoints+(k-1)×BigMoveStepPoints`. Far SELL: `BigLevel=FarReference+Distance×Point`; Far BUY: minus. Каждый уровень нормализуется по tick grid и повторно проверяется на правильную сторону и минимальную дистанцию.

## Control proof range
RecoveryPL и catch-up проверяются на каждом broker-valid tick от CurrentClosePrice до NextBigControlPrice и дополнительно на AdverseRisk/GapStress. Пропуск точки или stale snapshot = reject.

## Small confirmation
Touch alone запрещён. Условия: (1) close-side crossing SmallTransitionControlPrice; (2) новый fresh snapshot; (3) configurable hold duration или retrace distance; (4) persisted DebounceKey=`CycleID+PlanID+TriggerLevel+Direction`; (5) active transition отсутствует. Повтор идентичного trigger=NO-OP, конфликт=RECONCILIATION.

## Initial geometry
Initial BUY запрашивается по Ask, SELL по Bid; actual fill prices являются source of truth. После actual close прибыльной стороны remaining position становится FAR, а Initial Profit исключается.

## Error/restart
После restart trigger восстанавливается только из snapshot+actual market+action journal; comment не является source. Gap через несколько уровней не разрешает пропустить revalidation. Owner: Planning/GeometrySolver и MarketSnapshot. Тесты: Far BUY/SELL, tick sizes, stale, gap, debounce, repeated snapshots.
> **Граница реализации HSB.1V (2026-08-10).** Описанный production lifecycle остаётся нормативной спецификацией, а не реализованным сценарием. В каркасе нет production execution, broker-money runtime и production persistence. Действуют: ровно один Far; promotion только из actual BigCore residual; FinalReserve запрещён для Partial Far; allocations не прибавляются к actual money повторно; Final Close определяется только actual money; только COMPLETED_FILL снимает transaction barrier; retry сохраняет ActionID; conflict ведёт в RECONCILING; unresolved critical error — в TERMINAL_SAFE; no auto-resume; REAL_LIMITED и HSB.2 запрещены.
