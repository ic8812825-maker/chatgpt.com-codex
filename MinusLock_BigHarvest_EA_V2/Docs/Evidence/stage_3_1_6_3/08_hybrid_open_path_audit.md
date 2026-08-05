# 3.1.6.3.8 — открытие Hybrid-корзины

## Фактический маршрут

`STATE_FAR_ACTIVE → PrepareSplitBigLevel() → STATE_SPLIT_BIG_OPEN_CORE → последующие Split open states`.

При `UseHybridSplitBigGeometry=true` Hybrid solver подменяет рассчитанные lots внутри Split context, но верхний маршрут и states остаются Split. Корзина открывается ролями `BigCore`, `BigTrend`, `SmallBase`; direction определяется относительно Far.

## Проверки и поведение

- Lots нормализуются Hybrid/lot helpers и дополнительно проверяются по broker min/max/step.
- Margin, projected recovery, catch-up и monotonicity gates присутствуют до/в процессе подготовки.
- Открытия выполняются последовательными state handlers через `OpenPosition()`.
- При отказах используются pending/rollback/manual routes, но actual-deal event barrier отсутствует.
- Tickets/identifiers читаются из фактически найденных позиций после open, однако связь с request parent EventID отсутствует.
- Basket может считаться открытой после synchronous wrapper + position resolution, а не после единого reconciled transaction set.

## Смешение поколений

- Activation: Split flag + Hybrid modifier.
- States/comments сохраняют `SPLIT_*` семантику.
- `GeometryEngine` и `HybridGeometrySolver` являются двумя источниками geometry.
- Legacy work parameters продолжают существовать в общем context и validation.
- Отсутствие BigTrend запрещается обычно, но существует input `AllowCycleWithoutBigTrend`, создающий альтернативную topology.

## Замечания

- `OPEN-001 P1`: Hybrid open path не автономен; он модифицирует Split execution path.
- `OPEN-002 P1`: Нет atomic persisted CandidatePlan → three actual deals transaction.
- `OPEN-003 P1`: Partial fill любого leg не подтверждается через OnTradeTransaction до state advance.
- `OPEN-004 P2`: Два источника lot/geometry расчёта.
- `OPEN-005 P2`: Alternative topology without BigTrend конфликтует со строгой Hybrid role model.

Классификация: `HYBRID_PARTIAL / SPLIT_ACTIVE / MIXED_MODE / UNSAFE`.
