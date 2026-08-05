# Глоссарий и размерности Hybrid Split Big

Версия 1.0. Статус: нормативный.

## Назначение

Установить единственное значение терминов, типов и размерностей. Любая формула или MQL5-функция обязана использовать эти определения.

## Основные типы

| Термин | Символ | Тип/размерность | Source of truth | Правило |
|---|---|---|---|---|
| Lot | L | `double`, lot | MT5 position/deal | volume grid |
| Price | P | `double`, price | Bid/Ask/tick | tick-size grid |
| Point | pt | price increment | SYMBOL_POINT | не равен pip |
| Pip | pip | market convention | symbol contract | не использовать без conversion |
| Money | M | account currency | OrderCalcProfit/deals | signed |
| Percent | % | percent | config | делить на 100 перед ratio |
| Ratio | r | dimensionless | plan/config | не lot |
| Ticket | — | `ulong` | MT5 order/position/deal | временная сущность |
| Identifier | — | `ulong` | POSITION_IDENTIFIER | ownership continuity |
| CycleID | — | `ulong` | persisted generator | один recovery cycle |
| PlanID | — | `ulong` | immutable plan registry | уникален в cycle |
| ActionID | — | `ulong` | action registry | один irreversible intent |
| EventID | — | `ulong` | event store | один observed event |
| StateRevision | — | `ulong` | snapshot | увеличивается при commit |
| Timestamp | t | datetime | server time | не identity |

## Projected и actual

- Projected — расчёт до сделки; не изменяет ledger и роли.
- Requested — отправленный объём/цена.
- Filled — подтверждённая сумма deals.
- Actual — восстановленное состояние positions/orders/deals после transaction.

## Знаки

Profit положителен, loss отрицателен. Commission/fee обычно отрицательны, но в ledger сохраняются как возвращены MT5. `DealNet = Profit + Swap + Commission + Fee`.

## Округление

Цена нормализуется по `SYMBOL_TRADE_TICK_SIZE`, объём — по `SYMBOL_VOLUME_STEP` и границам min/max. Округление Partial Far всегда вниз; SmallBase может округляться безопасно вверх только при повторной проверке всех gates; каждое правило фиксируется owner-модулем.

## Запрет смешения

- `HSBI-MATH-001`: points не сравниваются с price без умножения на point.
- `HSBI-MATH-002`: lots не складываются с ratios.
- `HSBI-MATH-003`: money не подменяется points.
- `HSBI-MATH-004`: projected не записывается как actual.
- `HSBI-ID-001`: ticket не равен identifier.
- `HSBI-MONEY-001`: allocation bucket не является дополнительной прибылью.
- `HSBI-MONEY-002`: FinalReserve уже является подмножеством realized money и не прибавляется повторно.

## Контракт

Вход: symbol properties, snapshot и нормативные термины. Выход: типизированные значения. Preconditions: валидные broker properties. Postconditions: формулы dimension-safe. Error route: invalid dimension → plan rejected. Restart: типы и IDs сохраняются без преобразования. Будущий owner: `Core/Types`, `Core/Identity`, `Money/BrokerMoneyModel`. Тесты: unit tests для conversion, signs и rounding. Открытые вопросы: pip convention и безопасные rounding-политики конкретных legs.