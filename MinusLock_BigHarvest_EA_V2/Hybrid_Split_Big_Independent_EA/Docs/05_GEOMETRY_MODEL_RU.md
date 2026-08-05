# Геометрическая модель Hybrid Split Big

Версия 1.0. Статус: нормативный.

## Initial geometry

Initial BUY открывается по Ask, Initial SELL по Bid. Spread входит в фактическую геометрию. После подтверждённых fills фиксируется immutable initial anchor. При движении цены на trigger прибыльная leg определяется broker-money расчётом close-now, закрывается и исключается; оставшаяся leg становится FAR только после actual deal.

## Big geometry

`DistanceBig(k)=BigMoveStartPoints+(k-1)×BigMoveStepPoints`.

Для FAR SELL Big-направление вверх: `BigLevelPrice(k)=FarReferencePrice+DistanceBig(k)×Point`. Для FAR BUY — вниз со знаком minus. Уровень нормализуется по tick size; trigger side определяется реальной стороной закрытия legs, а не Mid.

## Small geometry

Small control price строится около OldFar reference с утверждённым offset. Для FAR SELL/SMALL_BASE SELL возврат проверяется по стороне, влияющей на close/transition; FAR BUY зеркален. Один trigger создаёт один immutable transition plan. Во время active/pending transition новые triggers игнорируются.

## Control prices

- Current: свежие Bid/Ask.
- Big control: точка Harvest/recovery proof.
- Small control: цена подтверждённого reversal.
- Final Close: текущий executable Bid/Ask snapshot.
- Worst/gap/margin stress: отдельные adverse snapshots.

- `HSBI-GEO-001`: price и points не смешиваются.
- `HSBI-GEO-002`: любой level нормализуется по `SYMBOL_TRADE_TICK_SIZE`, digits и point.
- `HSBI-GEO-003`: lot candidates нормализуются по min/max/step.
- `HSBI-GEO-004`: manual/adaptive — конфигурации одной Hybrid-системы, не runtime systems.
- `HSBI-GEO-005`: после rounding повторяются money, risk, margin, catch-up и compression gates.
- `HSBI-GEO-006`: trigger не может повторно инициировать pending action.

## Пример

ДЕМОНСТРАЦИОННЫЙ ПРОФИЛЬ, НЕ PRODUCTION DEFAULT: point=0.00001, FarReference=1.10000, start=100 points, step=50. FAR SELL: L1=1.10100, L2=1.10150. FAR BUY: L1=1.09900, L2=1.09850. При tick size 0.00005 каждое значение округляется на tick grid до gate evaluation.

## Контракт

Вход: Far identity/reference, level, symbol grid, mode configuration. Выход: immutable normalized levels/control snapshots. Preconditions: valid symbol properties, reconciled Far. Postconditions: deterministic levels. Запрещено: Mid как универсальная execution price, old trigger после StateRevision, level outside broker grid. Error route: geometry reject → no order. Restart: levels входят в persisted plan. Owner: Planning/GeometrySolver. Тесты: BUY/SELL symmetry, tick sizes, gaps, stale snapshot. Открытые вопросы: exact Small confirmation и adaptive formulas.