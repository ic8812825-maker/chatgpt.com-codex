# 3.1.6.3.5 — аудит OnTradeTransaction и actual deals

## Результат поиска

В production `.mq5/.mqh` проекта обработчик `OnTradeTransaction` отсутствует. Поиск имени на текущем HEAD возвращает только планирующую документацию, но не production handler.

## Фактическое подтверждение действий

`TradeEngine.mqh`:

- `OpenPosition()` возвращает результат `CTrade.Buy/Sell`.
- `ClosePositionByTicket()` возвращает результат `CTrade.PositionClose/PositionClosePartial`.
- `ClosePositionByTicketWithComment()` считает вызов успешным при `DONE`, `DONE_PARTIAL` или `PLACED`.
- ResultOrder/ResultDeal/ResultVolume/ResultPrice журналируются, но event-driven reconciliation сделки не выполняется.
- `TRADE_RETCODE_PLACED` не является actual deal confirmation.
- `DONE_PARTIAL` принимается wrapper как success; дальнейшее поведение зависит от state handler и последующего чтения позиции/history.

## Матрица transaction semantics

| Требование | Факт | Статус |
|---|---|---|
| Order transaction handler | отсутствует | MISSING |
| Deal add handler | отсутствует | MISSING |
| Position update handler | отсутствует | MISSING |
| Symbol/Magic/CycleID/identifier event filter | нет event handler | MISSING |
| DEAL_ENTRY_IN/OUT/INOUT/OUT_BY | местами читается history постфактум, но не transaction dispatcher | PARTIAL |
| Duplicate event protection | Reserve ledger имеет собственный key; общего deal event key в runtime нет | PARTIAL |
| Parent EventID | отсутствует в trade transaction path | MISSING |
| Actual volume/price/cost event reconciliation | постфактум через history/position helpers | PARTIAL |
| FSM advance only after actual deal | не обеспечено | FAIL |

## Критическое нарушение

```text
NO_STATE_ADVANCE_BEFORE_ACTUAL_DEAL = FAIL
```

Функции FSM часто вызывают close/open wrapper и при true немедленно очищают context или переводят State. Это происходит без обязательного ожидания отдельного MT5 transaction event.

## Замечания

| ID | Критичность | Содержание |
|---|---|---|
| TX-001 | P1 | Полностью отсутствует `OnTradeTransaction`; normative actual-deal lifecycle этапа 3.1.5 не подключён к production event path. |
| TX-002 | P1 | `TRADE_RETCODE_PLACED` может быть принят как завершённое действие. |
| TX-003 | P1 | `DONE_PARTIAL` не маршрутизируется через единый transaction reconciliation barrier. |
| TX-004 | P1 | FSM advance/cleanup возможны до подтверждения всех actual deals. |
| TX-005 | P2 | Логи ResultDeal не создают exactly-once deal ledger. |

## Классификация

`OnTradeTransaction = NOT_MAPPED / MISSING`.
`Actual-deal production integration = MAPPED_PARTIAL / UNSAFE`.
Production MQL5 не изменялся.
